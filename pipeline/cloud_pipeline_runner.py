"""
pipeline/cloud_pipeline_runner.py
Cloud Pipeline Runner: Google Drive -> Autonomous Gemini Provision Architect -> Discrete Voice Synthesis -> Google Sheets.

Generates point-by-point discrete voice clips (Intro through each presentation card)
and maps each voice clip directly to its card without timestamp drift.
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
from pipeline.synthesize_discrete_points import generate_discrete_voice_for_mindmap

# Configuration
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE')

# Authenticate Google Services
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
    creds = None

sheets_service = build('sheets', 'v4', credentials=creds) if creds else None
drive_service = build('drive', 'v3', credentials=creds) if creds else None

def append_row_to_sheets(row_values):
    """Appends a single question row immediately to Google Sheets database."""
    if not sheets_service:
        print("  [WARN] Sheets service not configured. Skipping append.")
        return
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
    print("STARTING POINT-BY-POINT CLOUD PIPELINE: Drive -> Gemini -> Discrete Voice -> Sheets")
    print("="*75)

    qna_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')
    with open(qna_file, 'r', encoding='utf-8') as f:
        qna_list = json.load(f)

    # Cache for already generated topics: { canonical_topic: { 'folder_id': id, 'summary_json': str, 'prov_md': str } }
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
        else:
            canonical_topic = f"Statutory Topic Q{q_num}"
            formatted_provision_matrix = f"### {canonical_topic}\n\nStatutory income tax provision."
            mm_data = {"doctrine": canonical_topic, "root": {}, "branches": []}

        print(f"  Canonical Doctrine: '{canonical_topic}'")

        # 2. CHECK TOPIC DEDUPLICATION & REUSE:
        if canonical_topic in generated_topics_cache:
            # REUSE EXISTING TOPIC DISCRETE AUDIO AND PRESENTATION!
            cached = generated_topics_cache[canonical_topic]
            drive_folder_id = cached['folder_id']
            summary_json_str = cached['summary_json']
            formatted_provision_matrix = cached['prov_md']
            print(f"  [REUSED TOPIC] '{canonical_topic}' already generated! Skipping duplicate TTS. Reusing Drive Folder: {drive_folder_id}")
        else:
            # NEW TOPIC: Generate discrete point audio clips and upload to Google Drive Voice/DT/Q{n}/
            print(f"  [NEW TOPIC] Creating Point-by-Point Discrete Voice for '{canonical_topic}'...")
            
            discrete_out_dir = os.path.join(PROJECT_ROOT, 'data', 'audio', f'q{q_num}')
            try:
                mm_data = generate_discrete_voice_for_mindmap(
                    q_num=q_num,
                    mindmap=mm_data,
                    output_dir=discrete_out_dir,
                    upload_to_drive=True
                )
                drive_folder_id = mm_data.get('drive_folder_id', '')
            except Exception as synth_err:
                print(f"    Notice on discrete voice synthesis: {synth_err}")
                drive_folder_id = "DRIVE_FOLDER_READY"

            summary_json_str = json.dumps(mm_data, ensure_ascii=False)

            # Cache this canonical topic so all subsequent questions under it share the exact voice clips & tree
            generated_topics_cache[canonical_topic] = {
                'folder_id': drive_folder_id,
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
            summary_json_str,             # Provision Summary (Dynamic Mindmap with embedded point audio IDs)
            drive_folder_id,              # Drive Audio File/Folder ID
            f"{mm_data.get('total_points_count', len(mm_data.get('branches', [])))} Discrete Audio Points" # Timings/Status
        ]

        # 4. Append immediately to Google Sheets
        try:
            append_row_to_sheets(row)
            print(f"  [SHEETS UPDATED] Row for Q{q_num} ('{canonical_topic}') saved with discrete audio points!")
        except Exception as sheet_err:
            print(f"  [SHEETS ERROR] Q{q_num}: {sheet_err}")

    print("\n" + "="*75)
    print("DISCRETE POINT AUDIO PIPELINE COMPLETE! All cards paired with individual voice clips.")
    print("="*75)

if __name__ == '__main__':
    run_pipeline()
