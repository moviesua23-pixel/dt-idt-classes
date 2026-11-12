import os
import sys
import json
import wave
import time
import base64
import requests
try:
    import gtts
except ImportError:
    gtts = None
from pydub import AudioSegment
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.genai import types

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
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
    resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=90)
    res_json = resp.json()
    if res_json.get('status') == 'success':
        return res_json.get('fileId')
    raise Exception(f"Upload failed: {res_json.get('message')}")

def synthesize_point_audio(client, text: str, out_mp3_path: str):
    """
    Synthesizes a single point audio using Gemini TTS,
    falling back to Google Malayalam TTS if Gemini quota is exceeded.
    """
    # 1. Try Gemini TTS
    if client:
        try:
            resp = client.models.generate_content(
                model='gemini-2.5-flash-preview-tts',
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
                return 'gemini_tts'
        except Exception:
            pass

    # 2. Google Malayalam Neural TTS fallback
    if gtts is not None:
        tts = gtts.gTTS(text, lang='ml')
        tts.save(out_mp3_path)
        return 'gtts_neural'
    print(f"  [WARN] Neither Gemini TTS succeeded nor is gTTS available to synthesize point.")
    return 'none'

def generate_discrete_voice_for_mindmap(q_num: int, mindmap: dict, output_dir: str, upload_to_drive: bool = True):
    """
    Assigns sequential identification numbers (pt_0, pt_1, ...) to every presentation element,
    synthesizes each point's voice clip, and uploads each to Google Drive.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        client = rotator.get_client()
    except Exception:
        client = None
    
    subfolder_id = None
    if upload_to_drive and drive_service:
        try:
            subfolder_id = get_or_create_drive_subfolder(VOICE_DT_FOLDER_ID, f"Q{q_num}")
            print(f"Using Google Drive Subfolder: Voice/DT/Q{q_num} (ID: {subfolder_id})")
        except Exception as e:
            print(f"Drive subfolder notice: {e}")

    # 1. Root / Intro (Identification Number: 0)
    root = mindmap.get('root', {})
    root['pt_idx'] = 0
    root_text = root.get('voice_sync_text', f"ഇന്ന് നമ്മൾ {mindmap.get('doctrine', 'നിയമം')} പഠിക്കാം.")
    root_mp3 = os.path.join(output_dir, "pt_0.mp3")
    
    print(f"\n[Point 0 - Intro] Synthesizing voice clip...")
    engine = synthesize_point_audio(client, root_text, root_mp3)
    root['audio_file'] = f"q{q_num}/pt_0.mp3"
    print(f"  -> Synthesized pt_0.mp3 via {engine} ({os.path.getsize(root_mp3)} bytes)")
    
    if subfolder_id and os.path.exists(root_mp3):
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
            p_text = p.get('voice_sync_text', p.get('title', ''))
            p_mp3 = os.path.join(output_dir, f"pt_{current_idx}.mp3")
            
            print(f"  [Point {current_idx}] Synthesizing: '{p.get('title')}'...")
            try:
                engine = synthesize_point_audio(client, p_text, p_mp3)
                p['audio_file'] = f"q{q_num}/pt_{current_idx}.mp3"
                print(f"    -> Synthesized pt_{current_idx}.mp3 via {engine} ({os.path.getsize(p_mp3)} bytes)")
                
                if subfolder_id and os.path.exists(p_mp3):
                    p_drive_id = upload_audio_to_drive(p_mp3, subfolder_id, f"pt_{current_idx}.mp3")
                    p['drive_audio_id'] = p_drive_id
                    print(f"    -> Uploaded pt_{current_idx}.mp3 to Drive! ID: {p_drive_id}")
                else:
                    p['drive_audio_id'] = f"DRIVE_PT_{current_idx}_STREAM"
            except Exception as err:
                print(f"    -> Error on point {current_idx}: {err}")
                p['drive_audio_id'] = f"DRIVE_PT_{current_idx}_STREAM"
                
            current_idx += 1
            time.sleep(0.5)

    mindmap['total_points_count'] = current_idx
    mindmap['drive_folder_id'] = subfolder_id
    print(f"\nSUCCESS: Generated & uploaded {current_idx} discrete point voice clips for Q{q_num}!")
    return mindmap

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
