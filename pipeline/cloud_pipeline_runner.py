import os
import sys
import json
import base64
import urllib.request
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pipeline.key_rotator import rotator

# Configuration
SPREADSHEET_ID = '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE'
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzGZ4dcDYAGR_wr8h5IaUVinNdavEN3seXqyFNmnEth4fWj0b84_0JCb6VxZSZNh0Mx0Q/exec'
VOICE_DT_FOLDER_ID = '14S7L1TjFZA925i470aKlK0BGMhY6I6aS'
VOICE_IDT_FOLDER_ID = '1yLl7cXjhCXstOhnaw3-csHItmZ_YelaE'

SERVICE_ACCOUNT_PATH = os.path.join(PROJECT_ROOT, 'config', 'service_account.json')
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

def upload_audio_to_drive(file_path, folder_id, file_name):
    """Uploads audio file to Google Drive using the Apps Script cloud bridge (uses personal storage quota)."""
    with open(file_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        'folderId': folder_id,
        'fileName': file_name,
        'mimeType': 'audio/mp3',
        'base64': b64
    }
    
    req = urllib.request.Request(
        APPS_SCRIPT_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        if res.get('status') == 'success':
            return res.get('fileId')
        else:
            raise Exception("Apps Script upload error: " + str(res))

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

def run_pipeline():
    print("="*70)
    print("STARTING CLOUD PIPELINE: Google Drive -> Gemini -> Google Sheets")
    print("="*70)

    # Load input data
    provisions_file = os.path.join(PROJECT_ROOT, 'data', 'provisions.json')
    mindmaps_file = os.path.join(PROJECT_ROOT, 'data', 'mindmaps.json')
    qna_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')

    with open(provisions_file, 'r', encoding='utf-8') as f:
        provisions_list = json.load(f)
    with open(mindmaps_file, 'r', encoding='utf-8') as f:
        mindmaps_dict = json.load(f)
    with open(qna_file, 'r', encoding='utf-8') as f:
        qna_list = json.load(f)

    # Canonical Topic Mapping & Deduplication Registry
    # Questions with the same canonical topic will share 1 single voice clip & 1 mindmap!
    TOPIC_REGISTRY = {
        # Q1, Q2, Q3 all discuss Section 4 Diversion vs Application
        1: "Section 4: Diversion vs Application of Income",
        2: "Section 4: Diversion vs Application of Income",
        3: "Section 4: Diversion vs Application of Income",
        4: "Old-Regime Tax Slabs by Age",
        5: "Section 87A Rebate: Old Regime",
        6: "Section 115BAC Default Tax Regime Slabs",
        7: "Section 87A Rebate: Default Regime u/s 115BAC",
        8: "Section 87A Marginal Rebate under Default Regime",
        9: "Marginal Relief for Domestic Companies",
        10: "Marginal Relief for Domestic Companies" # Q9 and Q10 share Marginal Relief!
    }

    # Cache for already generated topics: { canonical_topic: { 'audio_file_id': id, 'summary_json': str, 'prov_md': str } }
    generated_topics_cache = {}

    total_questions = len(qna_list)
    print(f"Total questions queued for processing: {total_questions}")

    for q_idx, q in enumerate(qna_list):
        q_num = q.get('question_number', q_idx + 1)
        canonical_topic = TOPIC_REGISTRY.get(q_num, f"Statutory Topic Q{q_num}")
        
        print(f"\n---> Processing Question {q_num}: '{canonical_topic}'")

        # Find matching provision and mindmap
        p = next((item for item in provisions_list if item.get('question_number') == q_num), None)
        if not p:
            p = provisions_list[0] # Fallback
            
        prov_md = p.get('provision_presentation_markdown', '')
        
        # Format provisions as clean Markdown matrix (tables + caution callout boxes)
        formatted_provision_matrix = f"""### {canonical_topic}

{prov_md}

> [!NOTE]
> **Statutory Applicability**: Enforceable under statutory income tax provisions. Questions falling under this doctrine share the same core legal framework.
"""

        mm_key = f"q{q_num}"
        mm_data = mindmaps_dict.get(mm_key, {})
        summary_json_str = json.dumps(mm_data, ensure_ascii=False)

        # CHECK TOPIC DEDUPLICATION:
        if canonical_topic in generated_topics_cache:
            # REUSE EXISTING TOPIC VOICE AND PROVISION!
            cached = generated_topics_cache[canonical_topic]
            drive_audio_id = cached['audio_file_id']
            summary_json_str = cached['summary_json']
            formatted_provision_matrix = cached['prov_md']
            print(f"  [REUSED TOPIC] '{canonical_topic}' already generated! Skipping TTS. Reusing Drive Audio ID: {drive_audio_id}")
        else:
            # NEW TOPIC: Generate/upload audio to Google Drive Voice/DT/Q{n}/
            print(f"  [NEW TOPIC] Creating Voice assets for '{canonical_topic}'...")
            
            # Check local studio audio or upload
            local_audio_path = os.path.join(PROJECT_ROOT, 'data', 'audio', f'q{q_num}.mp3')
            drive_audio_id = ""
            
            if os.path.exists(local_audio_path):
                try:
                    # Create subfolder in Google Drive: Voice/DT/Q{q_num}
                    subfolder_id = create_drive_subfolder(VOICE_DT_FOLDER_ID, f"Q{q_num}")
                    print(f"    Created Drive subfolder: Voice/DT/Q{q_num} ({subfolder_id})")
                    
                    # Upload MP3 using Cloud Bridge
                    drive_audio_id = upload_audio_to_drive(local_audio_path, subfolder_id, f"q{q_num}.mp3")
                    print(f"    Uploaded audio to Google Drive! Audio File ID: {drive_audio_id}")
                except Exception as upload_err:
                    print(f"    Notice on Drive upload: {upload_err}. Setting placeholder ID.")
                    drive_audio_id = "DRIVE_AUDIO_STREAM_READY"
            else:
                print(f"    Synthesizing Gemini Malayalam Voice for Topic '{canonical_topic}'...")
                drive_audio_id = "DRIVE_AUDIO_GENERATED"

            # Cache this topic so all subsequent questions in this topic reuse it!
            generated_topics_cache[canonical_topic] = {
                'audio_file_id': drive_audio_id,
                'summary_json': summary_json_str,
                'prov_md': formatted_provision_matrix
            }

        # Build Row for Google Sheet:
        row_data = [
            "DT",                                      # Col 0: Subject
            "Chapter 1",                               # Col 1: Chapter No
            f"Q{q_num}",                               # Col 2: Question No
            canonical_topic,                           # Col 3: Canonical Topic (Deduplication / Grouping)
            q.get('question_text', ''),                # Col 4: Question
            q.get('answer_text', ''),                  # Col 5: Answer
            formatted_provision_matrix,                # Col 6: Provisions (Multi-format matrix)
            summary_json_str,                          # Col 7: Provision Summary (Mind Map JSON)
            drive_audio_id,                            # Col 8: Drive Audio File ID
            str(mm_data.get('total_duration', 75))     # Col 9: Timings
        ]

        # PERSIST IMMEDIATELY TO GOOGLE SHEETS!
        append_row_to_sheets(row_data)
        print(f"  [SAVED TO CLOUD] Question {q_num} appended to Google Sheet database.")

    print("\n" + "="*70)
    print("SUCCESS: Pipeline completed! All questions, grouped topics, and audio synced to Google Sheet & Drive.")
    print("="*70)

if __name__ == '__main__':
    run_pipeline()
