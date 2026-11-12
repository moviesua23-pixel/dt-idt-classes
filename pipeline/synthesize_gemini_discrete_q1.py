import os
import sys
import json
import wave
import time
import base64
import requests
from pydub import AudioSegment

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

sys.stdout.reconfigure(encoding='utf-8')

from pipeline.key_rotator import rotator
from google.genai import types

APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzGZ4dcDYAGR_wr8h5IaUVinNdavEN3seXqyFNmnEth4fWj0b84_0JCb6VxZSZNh0Mx0Q/exec'
USER_Q1_FOLDER_ID = '1gIAoMsQdG8YVUy6HcNsZdvRYvlGxxU6e'
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'audio', 'q1')
TEMP_DIR = os.path.join(PROJECT_ROOT, 'data', 'audio_temp', 'q1_gemini_discrete')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

MODEL_NAME = 'gemini-2.5-flash-preview-tts'
VOICE_NAME = 'Aoede'
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2

# Natural, pedagogical, expressive Malayalam scripts with authentic English statutory terms
SCRIPTS = {
    "pt_0": (
        "നമസ്കാരം! ഇന്ന് നമ്മൾ പഠിക്കുന്നത് ഇൻകം ടാക്സ് ആക്റ്റിലെ സെക്ഷൻ നാല് പ്രകാരമുള്ള "
        "ഏറ്റവും പ്രധാനപ്പെട്ട രണ്ട് ലീഗൽ ഡോക്ട്രിനുകളാണ്: Diversion of Income വേഴ്സസ് Application of Income. "
        "ടാക്സബിലിറ്റി നിശ്ചയിക്കുന്നതിൽ ഈ വ്യത്യാസം വളരെ നിർണ്ണായകമാണ്."
    ),
    "pt_1": (
        "ആദ്യമായി, Diversion by Overriding Title എന്താണെന്ന് നോക്കാം. "
        "ഇവിടെ ഒരു നിയമപരമായ ഓവർറൈഡിംഗ് ടൈറ്റിൽ കാരണം, വരുമാനം അസസ്സീയുടെ കയ്യിൽ എത്തുന്നതിന് മുൻപ് തന്നെ "
        "സോഴ്സിൽ വെച്ച് മറ്റൊരിടത്തേക്ക് മാറ്റപ്പെടുന്നു. "
        "ഇത് അസസ്സീയുടെ വരുമാനമായി കണക്കാക്കില്ല, അതിനാൽ തന്നെ ഇതിന് നികുതി നൽകേണ്ടതില്ല."
    ),
    "pt_2": (
        "രണ്ടാമതായി, Application of Income. "
        "ഇവിടെ വരുമാനം ആദ്യം അസസ്സീക്ക് നിയമപരമായി വന്നുചേരുന്നു. "
        "അതിനുശേഷം അസസ്സീ സ്വന്തം ഇഷ്ടപ്രകാരം ആ പണം മറ്റൊരാൾക്ക് നൽകുകയോ ചെലവഴിക്കുകയോ ചെയ്യുന്നു. "
        "ഇത് പൂർണ്ണമായും ടാക്സബിൾ ആണ്, യാതൊരു ഡിഡക്ഷനും ലഭിക്കില്ല."
    ),
    "pt_3": (
        "മൂന്നാമതായി, ജുഡീഷ്യൽ ബെഞ്ച്മാർക്കുകളും നിർണ്ണായക ഘടകങ്ങളും. "
        "ഒരു തുക ഡൈവേർഷൻ ആണോ ആപ്ലിക്കേഷൻ ആണോ എന്ന് തീരുമാനിക്കുന്നത് ബാധ്യത എപ്പോൾ, ആര് ഉണ്ടാക്കി എന്നതിനെ ആശ്രയിച്ചാണ്. "
        "കോടതി വിധി പ്രകാരം പങ്കാളി ഭാര്യക്ക് വിഹിതം നൽകുന്നത് ഓവർറൈഡിംഗ് ടൈറ്റിൽ ആയതിനാൽ ഡൈവേർഷൻ ആണ്. "
        "എന്നാൽ ഫീസിൽ നിന്നും ട്രസ്റ്റ് ഉണ്ടാക്കുന്നത് അസസ്സീയുടെ സ്വന്തം തീരുമാനമായതിനാൽ ആപ്ലിക്കേഷൻ മാത്രമാണ്."
    )
}

def synthesize_clip(client, text, tag):
    print(f"\n[Synthesizing {tag}]...", flush=True)
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=[text],
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
                )
            )
        )
    )
    if not resp.candidates or not resp.candidates[0].content or not resp.candidates[0].content.parts:
        raise RuntimeError(f"No audio returned for {tag}")
        
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_path = os.path.join(TEMP_DIR, f"{tag}.wav")
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(BYTES_PER_SAMPLE)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
        
    seg = AudioSegment.from_wav(wav_path)
    mp3_path = os.path.join(OUTPUT_DIR, f"{tag}.mp3")
    seg.export(mp3_path, format="mp3", bitrate="128k")
    dur_sec = round(len(seg) / 1000.0, 2)
    print(f"  -> Generated {mp3_path} ({len(pcm)} bytes PCM, {dur_sec}s duration)", flush=True)
    return mp3_path, dur_sec

def upload_to_drive(file_path, file_name):
    print(f"  -> Uploading {file_name} to Google Drive folder {USER_Q1_FOLDER_ID}...", flush=True)
    with open(file_path, 'rb') as f:
        data = f.read()
    b64_content = base64.b64encode(data).decode('utf-8')
    payload = {
        'folderId': USER_Q1_FOLDER_ID,
        'fileName': file_name,
        'mimeType': 'audio/mp3',
        'base64': b64_content
    }
    resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=90)
    res_json = resp.json()
    if res_json.get('status') == 'success':
        file_id = res_json.get('fileId')
        print(f"    Uploaded successfully! Drive ID: {file_id}", flush=True)
        return file_id
    raise Exception(f"Upload failed: {res_json.get('message')}")

def main():
    print("=== SYNTHESIZING EXPRESSIVE GEMINI AOEDE DISCRETE AUDIO FOR Q1 ===", flush=True)
    client = rotator.get_client()
    
    drive_ids = {}
    durations = {}
    for tag in ["pt_0", "pt_1", "pt_2", "pt_3"]:
        mp3_path, dur = synthesize_clip(client, SCRIPTS[tag], tag)
        durations[tag] = dur
        time.sleep(1.0)
        
        file_id = upload_to_drive(mp3_path, f"{tag}.mp3")
        drive_ids[tag] = file_id
        time.sleep(1.0)
        
    print("\nAll 4 clips generated and uploaded successfully!", flush=True)
    print("Drive IDs:", drive_ids, flush=True)
    print("Durations:", durations, flush=True)
    
    # Update q1_discrete_mindmap.json
    mindmap_file = os.path.join(PROJECT_ROOT, 'data', 'audio', 'q1', 'q1_discrete_mindmap.json')
    with open(mindmap_file, 'r', encoding='utf-8') as f:
        mm = json.load(f)
        
    mm['root']['drive_audio_id'] = drive_ids['pt_0']
    mm['root']['voice_sync_text'] = SCRIPTS['pt_0']
    mm['root']['duration'] = durations['pt_0']
    
    mm['branches'][0]['points'][0]['drive_audio_id'] = drive_ids['pt_1']
    mm['branches'][0]['points'][0]['voice_sync_text'] = SCRIPTS['pt_1']
    mm['branches'][0]['points'][0]['duration'] = durations['pt_1']
    
    mm['branches'][1]['points'][0]['drive_audio_id'] = drive_ids['pt_2']
    mm['branches'][1]['points'][0]['voice_sync_text'] = SCRIPTS['pt_2']
    mm['branches'][1]['points'][0]['duration'] = durations['pt_2']
    
    mm['branches'][2]['points'][0]['drive_audio_id'] = drive_ids['pt_3']
    mm['branches'][2]['points'][0]['voice_sync_text'] = SCRIPTS['pt_3']
    mm['branches'][2]['points'][0]['duration'] = durations['pt_3']
    
    mm['total_duration'] = sum(durations.values())
    
    with open(mindmap_file, 'w', encoding='utf-8') as f:
        json.dump(mm, f, indent=2, ensure_ascii=False)
        
    # Also update data/mindmaps.json
    all_mm_file = os.path.join(PROJECT_ROOT, 'data', 'mindmaps.json')
    with open(all_mm_file, 'r', encoding='utf-8') as f:
        all_mm = json.load(f)
    all_mm['q1'] = mm
    all_mm['question_to_mindmap']['1'] = 'q1'
    with open(all_mm_file, 'w', encoding='utf-8') as f:
        json.dump(all_mm, f, indent=2, ensure_ascii=False)
        
    print("\nUpdated data/mindmaps.json and data/audio/q1/q1_discrete_mindmap.json successfully!", flush=True)

    # Push updated mindmap JSON to Google Sheet Row 2 Column H
    print("\nPushing updated mindmap JSON to Google Sheet Row 2...", flush=True)
    sheet_payload = {
        "action": "updateMindmap",
        "questionNumber": 1,
        "row": 2,
        "mindmapJson": json.dumps(mm, ensure_ascii=False),
        "driveFolderId": USER_Q1_FOLDER_ID
    }
    resp = requests.post(APPS_SCRIPT_URL, json=sheet_payload, timeout=60)
    print("Google Sheet sync response:", resp.text, flush=True)

if __name__ == "__main__":
    main()
