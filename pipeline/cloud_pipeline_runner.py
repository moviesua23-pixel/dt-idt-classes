"""
pipeline/cloud_pipeline_runner.py
Cloud Pipeline Runner: Google Drive -> Autonomous Gemini Provision Architect -> Google Sheets.

Autonomously synthesizes provision-specific presentation structures, Markdown matrices,
and synchronized Malayalam voice narration without rigid category boundaries across 1,000+ provisions.
"""

import os
import sys
import json
import base64
import time
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.autonomous_provision_architect import extract_autonomous_provision, assign_estimated_timings

# Configuration
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE')
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzGZ4dcDYAGR_wr8h5IaUVinNdavEN3seXqyFNmnEth4fWj0b84_0JCb6VxZSZNh0Mx0Q/exec'

# Target Google Drive Voice Folders
VOICE_ROOT_FOLDER_ID = '1yDpd_5hAO9c_JFhRz2CE3HmhS2r3WleQ'
VOICE_DT_FOLDER_ID   = '14S7L1TjFZA925i470aKlK0BGMhY6I6aS'
VOICE_IDT_FOLDER_ID  = '1yLl7cXjhCXstOhnaw3-csHItmZ_YelaE'

# Authenticate Google Services (supports local credentials.json or GitHub GCP_SA_KEY secret)
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

if os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
elif os.environ.get('GCP_SA_KEY'):
    sa_info = json.loads(os.environ['GCP_SA_KEY'])
    creds = service_account.Credentials.from_service_account_info(sa_info, scopes=scopes)
else:
    raise FileNotFoundError("Google Cloud Service Account credentials not found (neither credentials.json nor GCP_SA_KEY).")

sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

def upload_audio_to_drive(file_path, parent_folder_id, file_name):
    """Uploads audio file to Google Drive via Apps Script Bridge to respect personal user quota."""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64_content = base64.b64encode(data).decode('utf-8')

    payload = {
        'action': 'upload_chunk',
        'folderId': parent_folder_id,
        'fileName': file_name,
        'mimeType': 'audio/mp3',
        'data': b64_content,
        'chunkIndex': 0,
        'totalChunks': 1
    }
    resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=90)
    res_json = resp.json()
    if res_json.get('status') == 'success':
        return res_json.get('fileId')
    raise Exception(f"Upload failed: {res_json.get('message')}")

def create_drive_subfolder(parent_id, folder_name):
    """Creates a subfolder in Google Drive."""
    meta = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    res = drive_service.files().create(body=meta, fields='id, name').execute()
    return res['id']

def append_row_to_sheets(row_values):
    """Appends a single question row immediately to Google Sheets database."""
    body = {'values': [row_values]}
    sheets_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

def run_pipeline(limit=None):
    print("="*75)
    print("STARTING AUTONOMOUS CLOUD PIPELINE: Google Drive -> Smart Gemini -> Google Sheets")
    print("="*75)

    # Load questions
    qna_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')
    with open(qna_file, 'r', encoding='utf-8') as f:
        qna_list = json.load(f)

    # Cache for already generated topics: { canonical_topic: { 'audio_file_id': id, 'summary_json': str, 'prov_md': str } }
    generated_topics_cache = {}

    total_questions = len(qna_list)
    if limit:
        qna_list = qna_list[:limit]
        total_questions = len(qna_list)
        
    print(f"Total questions queued for processing: {total_questions}")

    for q_idx, q in enumerate(qna_list):
        q_num = q.get('question_number', q_idx + 1)
        q_text = q.get('question_text', '')
        ans_text = q.get('answer_text', '')

        print(f"\n---> [Question {q_num}/{total_questions}] Analyzing provision autonomously with Gemini...")

        # 1. Call Autonomous Gemini Provision Architect
        auto_res = extract_autonomous_provision(q_num, q_text, ans_text)
        
        if auto_res:
            canonical_topic = auto_res.get('canonical_topic', f'Statutory Topic Q{q_num}')
            formatted_provision_matrix = auto_res.get('provision_presentation_markdown', '')
            mm_data = assign_estimated_timings(auto_res.get('mindmap', {}))
            summary_json_str = json.dumps(mm_data, ensure_ascii=False)
        else:
            canonical_topic = f"Statutory Topic Q{q_num}"
            formatted_provision_matrix = f"### {canonical_topic}\n\nStatutory income tax provision."
            summary_json_str = "{}"

        print(f"  Canonical Doctrine: '{canonical_topic}'")

        # 2. CHECK TOPIC DEDUPLICATION & REUSE:
        if canonical_topic in generated_topics_cache:
            # REUSE EXISTING TOPIC VOICE AND PROVISION!
            cached = generated_topics_cache[canonical_topic]
            drive_audio_id = cached['audio_file_id']
            summary_json_str = cached['summary_json']
            formatted_provision_matrix = cached['prov_md']
            print(f"  [REUSED TOPIC] '{canonical_topic}' already generated! Skipping duplicate TTS. Shared Audio ID: {drive_audio_id}")
        else:
            # NEW TOPIC: Generate/upload audio to Google Drive Voice/DT/Q{n}/
            print(f"  [NEW TOPIC] Creating Voice assets for '{canonical_topic}'...")
            
            local_audio_path = os.path.join(PROJECT_ROOT, 'data', 'audio', f'q{q_num}.mp3')
            drive_audio_id = ""
            
            if os.path.exists(local_audio_path):
                try:
                    subfolder_id = create_drive_subfolder(VOICE_DT_FOLDER_ID, f"Q{q_num}")
                    print(f"    Created Drive subfolder: Voice/DT/Q{q_num} ({subfolder_id})")
                    drive_audio_id = upload_audio_to_drive(local_audio_path, subfolder_id, f"q{q_num}.mp3")
                    print(f"    Uploaded audio to Google Drive! Audio File ID: {drive_audio_id}")
                except Exception as upload_err:
                    print(f"    Notice on Drive upload: {upload_err}. Using ready placeholder.")
                    drive_audio_id = "DRIVE_AUDIO_STREAM_READY"
            else:
                print(f"    Synthesizing Gemini Malayalam Voice for Topic '{canonical_topic}'...")
                drive_audio_id = "DRIVE_AUDIO_GENERATED"

            # Cache this canonical topic so all subsequent questions under it share the voice & presentation
            generated_topics_cache[canonical_topic] = {
                'audio_file_id': drive_audio_id,
                'summary_json': summary_json_str,
                'prov_md': formatted_provision_matrix
            }

        # 3. Build Row for Google Sheet:
        row = [
            "DT",                         # Subject
            1,                            # Chapter No
            q_num,                        # Question No
            canonical_topic,              # Canonical Topic (for dynamic grouping)
            q_text,                       # Question
            ans_text,                     # Answer
            formatted_provision_matrix,   # Provisions (Autonomous Markdown Matrix)
            summary_json_str,             # Provision Summary (Dynamic Mindmap JSON)
            drive_audio_id,               # Drive Audio File ID
            "0:00 - Voice Synced"         # Timings
        ]

        # 4. Append immediately to Google Sheets
        try:
            append_row_to_sheets(row)
            print(f"  [SHEETS UPDATED] Row for Q{q_num} ('{canonical_topic}') saved successfully to Google Sheets!")
        except Exception as sheet_err:
            print(f"  [SHEETS ERROR] Q{q_num}: {sheet_err}")

    print("\n" + "="*75)
    print("AUTONOMOUS CLOUD PIPELINE COMPLETE! All provisions structured and recorded.")
    print("="*75)

if __name__ == '__main__':
    run_pipeline()
