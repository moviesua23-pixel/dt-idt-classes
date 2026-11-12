import os
import sys
import json
import wave
import time
import base64
import requests
from pydub import AudioSegment
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.genai import types

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    pass

from pipeline.key_rotator import rotator

APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzGZ4dcDYAGR_wr8h5IaUVinNdavEN3seXqyFNmnEth4fWj0b84_0JCb6VxZSZNh0Mx0Q/exec'
VOICE_DT_FOLDER_ID = '14S7L1TjFZA925i470aKlK0BGMhY6I6aS'
VOICE_IDT_FOLDER_ID = '1yLl7cXjhCXstOhnaw3-csHItmZ_YelaE'

SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')
scopes = ['https://www.googleapis.com/auth/drive']

if os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
elif os.environ.get('GCP_SA_KEY'):
    sa_info = json.loads(os.environ['GCP_SA_KEY'])
    creds = service_account.Credentials.from_service_account_info(sa_info, scopes=scopes)
else:
    creds = None

drive_service = build('drive', 'v3', credentials=creds) if creds else None

def get_or_create_drive_subfolder(parent_id, folder_name):
    if not drive_service:
        return "FOLDER_ID_PLACEHOLDER"
    try:
        q = f"'{parent_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        res = drive_service.files().list(q=q, fields='files(id, name)').execute()
        files = res.get('files', [])
        if files:
            return files[0]['id']
    except Exception:
        pass
    meta = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    res = drive_service.files().create(body=meta, fields='id, name').execute()
    try:
        drive_service.permissions().create(fileId=res['id'], body={'role': 'reader', 'type': 'anyone'}).execute()
    except Exception:
        pass
    return res['id']

def upload_audio_to_drive(file_path, parent_folder_id, file_name):
    """Uploads discrete MP3 file to Google Drive using base64 payload."""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64_content = base64.b64encode(data).decode('utf-8')
    payload = {
        'folderId': parent_folder_id,
        'fileName': file_name,
        'mimeType': 'audio/mp3',
        'base64': b64_content
    }
    try:
        resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=30)
        res_json = resp.json()
        if res_json.get('status') == 'success':
            file_id = res_json.get('fileId')
            if drive_service and file_id:
                try:
                    drive_service.permissions().create(
                        fileId=file_id,
                        body={'role': 'reader', 'type': 'anyone'}
                    ).execute()
                except Exception:
                    pass
            return file_id
        raise Exception(f"Upload failed: {res_json.get('message')}")
    except Exception as e:
        print(f"    [WARN] Drive upload via Apps Script notice ({e}). Generating fallback stream ID.")
        return f"DRIVE_PT_{file_name.replace('.mp3', '')}_READY"

from pipeline.key_rotator import rotator, AllKeysQuotaExhaustedError, is_quota_error

def is_audio_ready(drive_id: str) -> bool:
    """Checks whether a point already has a valid Google Drive file ID."""
    if not drive_id or not isinstance(drive_id, str):
        return False
    if drive_id.startswith('DRIVE_PT') or drive_id == 'DRIVE_FOLDER_READY':
        return False
    return True

def count_total_points(mindmap: dict) -> int:
    """Counts total discrete points (Root + all branch points)."""
    total = 1
    for b in mindmap.get('branches', []):
        total += len(b.get('points', []))
    return total

def count_ready_points(mindmap: dict) -> int:
    """Counts how many points currently have verified Drive audio IDs."""
    ready = 0
    if is_audio_ready(mindmap.get('root', {}).get('drive_audio_id')):
        ready += 1
    for b in mindmap.get('branches', []):
        for p in b.get('points', []):
            if is_audio_ready(p.get('drive_audio_id')):
                ready += 1
    return ready

def synthesize_point_audio(text: str, out_mp3_path: str):
    """
    Synthesizes a single point audio STRICTLY using Gemini Expressive Neural TTS (Aoede),
    rotating through all active keys.
    Zero robotic fallback (gTTS is completely disabled).
    If all keys hit quota limits (429), raises AllKeysQuotaExhaustedError to pause pipeline gracefully.
    """
    tts_models = [
        'gemini-3.1-flash-tts-preview',
        'gemini-3.8-flash-tts',
        'gemini-3.8-flash-lite-tts',
        'gemini-2.5-flash-preview-tts'
    ]

    def _gemini_tts_call(client):
        last_model_err = None
        for tts_model in tts_models:
            try:
                resp = client.models.generate_content(
                    model=tts_model,
                    contents=[text],
                    config=types.GenerateContentConfig(
                        response_modalities=['AUDIO'],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Aoede')
                            )
                        )
                    )
                )
                if resp.candidates and resp.candidates[0].content and resp.candidates[0].content.parts:
                    pcm_data = resp.candidates[0].content.parts[0].inline_data.data
                    temp_wav = out_mp3_path.replace('.mp3', '.wav')
                    with wave.open(temp_wav, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(24000)
                        wf.writeframes(pcm_data)
                        
                    seg = AudioSegment.from_wav(temp_wav)
                    seg.export(out_mp3_path, format='mp3')
                    if os.path.exists(temp_wav):
                        os.remove(temp_wav)
                    return f'gemini_expressive_{tts_model}'
            except Exception as e:
                last_model_err = e
                if is_quota_error(e):
                    # Raise quota error immediately so rotator rotates the key
                    raise e
                time.sleep(0.5)
                continue
        raise RuntimeError(f"Gemini Expressive TTS models failed to produce audio: {last_model_err}")

    try:
        return rotator.execute_with_retry(_gemini_tts_call)
    except AllKeysQuotaExhaustedError:
        raise
    except Exception as err:
        print(f"  [ERROR] Gemini Expressive Voice generation failed: {err}")
        raise err

def generate_discrete_voice_for_mindmap(q_num: int, mindmap: dict, output_dir: str, upload_to_drive: bool = True, subject: str = 'DT', chapter_no: int = 1):
    """
    Assigns sequential identification numbers (pt_0, pt_1, ...) to every presentation element,
    synthesizes each point's voice clip, and uploads each to Google Drive.
    Supports point-by-point resumption: skips points that are already uploaded.
    If Gemini quota runs out across all keys, records partial progress and raises AllKeysQuotaExhaustedError.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    subfolder_id = mindmap.get('drive_folder_id')
    if upload_to_drive and drive_service and (not subfolder_id or subfolder_id.startswith('DRIVE')):
        try:
            root_folder = VOICE_IDT_FOLDER_ID if str(subject).strip().upper() == 'IDT' else VOICE_DT_FOLDER_ID
            folder_name = f"Q{q_num}" if chapter_no == 1 else f"Ch{chapter_no}_Q{q_num}"
            subfolder_id = get_or_create_drive_subfolder(root_folder, folder_name)
            print(f"Using Google Drive Subfolder: Voice/{subject}/{folder_name} (ID: {subfolder_id})")
        except Exception as e:
            print(f"Drive subfolder notice: {e}")
            subfolder_id = "DRIVE_FOLDER_READY"

    mindmap['drive_folder_id'] = subfolder_id
    total_expected = count_total_points(mindmap)

    try:
        # 1. Root / Intro (Identification Number: 0)
        root = mindmap.get('root', {})
        root['pt_idx'] = 0
        if is_audio_ready(root.get('drive_audio_id')):
            print(f"\n[Point 0 - Intro] Already uploaded to Drive! ID: {root['drive_audio_id']}")
        else:
            root_text = root.get('voice_sync_text', f"ഇന്ന് നമ്മൾ {mindmap.get('doctrine', 'നിയമം')} പഠിക്കാം.")
            root_mp3 = os.path.join(output_dir, "pt_0.mp3")
            print(f"\n[Point 0 - Intro] Synthesizing voice clip with Gemini TTS...")
            engine = synthesize_point_audio(root_text, root_mp3)
            root['audio_file'] = f"{subject.lower()}/ch{chapter_no}/q{q_num}/pt_0.mp3"
            print(f"  -> Synthesized pt_0.mp3 via {engine} ({os.path.getsize(root_mp3)} bytes)")
            
            if subfolder_id and not subfolder_id.startswith('DRIVE') and os.path.exists(root_mp3):
                try:
                    root_drive_id = upload_audio_to_drive(root_mp3, subfolder_id, "pt_0.mp3")
                    root['drive_audio_id'] = root_drive_id
                    print(f"  -> Uploaded pt_0.mp3 to Drive! ID: {root_drive_id}")
                except Exception as e:
                    print(f"  -> Drive upload error for pt_0: {e}")
                    root['drive_audio_id'] = "DRIVE_PT_0_STREAM"

        # 2. Branches & Points (Sequential Identification Numbers: 1, 2, 3...)
        current_idx = 1
        branches = mindmap.get('branches', [])
        for b_i, b in enumerate(branches, 1):
            print(f"\n---> Branch {b_i}: {b.get('branch_title')}")
            points = b.get('points', [])
            for p_i, p in enumerate(points, 1):
                p['pt_idx'] = current_idx
                if is_audio_ready(p.get('drive_audio_id')):
                    print(f"  [Point {current_idx}] Already uploaded to Drive! ID: {p['drive_audio_id']}")
                else:
                    p_text = p.get('voice_sync_text', p.get('title', ''))
                    p_mp3 = os.path.join(output_dir, f"pt_{current_idx}.mp3")
                    print(f"  [Point {current_idx}] Synthesizing: '{p.get('title')}' with Gemini TTS...")
                    engine = synthesize_point_audio(p_text, p_mp3)
                    p['audio_file'] = f"{subject.lower()}/ch{chapter_no}/q{q_num}/pt_{current_idx}.mp3"
                    print(f"    -> Synthesized pt_{current_idx}.mp3 via {engine} ({os.path.getsize(p_mp3)} bytes)")
                    
                    if subfolder_id and not subfolder_id.startswith('DRIVE') and os.path.exists(p_mp3):
                        try:
                            p_drive_id = upload_audio_to_drive(p_mp3, subfolder_id, f"pt_{current_idx}.mp3")
                            p['drive_audio_id'] = p_drive_id
                            print(f"    -> Uploaded pt_{current_idx}.mp3 to Drive! ID: {p_drive_id}")
                        except Exception as e:
                            print(f"    -> Drive upload error for pt_{current_idx}: {e}")
                            p['drive_audio_id'] = f"DRIVE_PT_{current_idx}_STREAM"
                    else:
                        p['drive_audio_id'] = f"DRIVE_PT_{current_idx}_STREAM"

                current_idx += 1
                time.sleep(0.3)

        ready_count = count_ready_points(mindmap)
        mindmap['total_points_count'] = current_idx
        mindmap['completed_points_count'] = ready_count
        mindmap['is_partially_complete'] = (ready_count < current_idx)
        print(f"\nSUCCESS: Verified {ready_count}/{current_idx} discrete point voice clips for Q{q_num}!")
        return mindmap

    except AllKeysQuotaExhaustedError:
        ready_count = count_ready_points(mindmap)
        mindmap['total_points_count'] = total_expected
        mindmap['completed_points_count'] = ready_count
        mindmap['is_partially_complete'] = True
        print(f"  [CHECKPOINT] Quota exhausted during voice synthesis for Q{q_num}. Preserving {ready_count}/{total_expected} completed points.")
        raise

if __name__ == "__main__":
    from pipeline.autonomous_provision_architect import extract_autonomous_provision
    with open(os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json'), 'r', encoding='utf-8') as f:
        qna = json.load(f)[0]
    
    print("Extracting autonomous provision for Q1...")
    res = extract_autonomous_provision(1, qna['question_text'], qna['answer_text'])
    if res:
        mm = res['mindmap']
        out_dir = os.path.join(PROJECT_ROOT, 'data', 'audio', 'q1')
        updated_mm = generate_discrete_voice_for_mindmap(1, mm, out_dir, upload_to_drive=True)
        with open(os.path.join(PROJECT_ROOT, 'data', 'audio', 'q1', 'q1_discrete_mindmap.json'), 'w', encoding='utf-8') as mf:
            json.dump(updated_mm, mf, indent=2, ensure_ascii=False)
        print("Saved updated discrete mindmap to data/audio/q1/q1_discrete_mindmap.json!")
