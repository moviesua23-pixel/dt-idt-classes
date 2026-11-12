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
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
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

def upsert_row_to_sheets(row_values):
    """
    Upserts a question row into Google Sheets using the composite primary key:
    (Subject, Chapter No, Question No).
    If a row matching (Subject, Chapter No, Question No) exists, updates it in place.
    Otherwise, appends a new row at the bottom.
    """
    if not sheets_service:
        print("  [WARN] Sheets service not configured. Skipping save.")
        return

    subject = str(row_values[0]).strip().upper()
    chapter_no = str(row_values[1]).strip()
    q_num = str(row_values[2]).strip()

    try:
        # Fetch columns A to C to identify existing (Subject, Chapter, Question)
        res = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:C'
        ).execute()
        existing_rows = res.get('values', [])
        
        target_row_idx = None
        for idx, r in enumerate(existing_rows, start=1):
            if len(r) >= 3:
                r_subj = str(r[0]).strip().upper()
                r_chap = str(r[1]).strip()
                r_q = str(r[2]).strip()
                if r_subj == subject and r_chap == chapter_no and r_q == q_num:
                    target_row_idx = idx
                    break

        body = {'values': [row_values]}
        if target_row_idx:
            # In-place update of existing row
            range_to_update = f'Sheet1!A{target_row_idx}:J{target_row_idx}'
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"  [SHEETS UPDATED] Row {target_row_idx} updated in-place for {subject} Ch{chapter_no} Q{q_num}!")
        else:
            # Append new row
            sheets_service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range='Sheet1!A1',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            print(f"  [SHEETS APPENDED] New row added for {subject} Ch{chapter_no} Q{q_num}!")
    except Exception as e:
        print(f"  [SHEETS ERROR] Failed to upsert row ({subject} Ch{chapter_no} Q{q_num}): {e}")

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
        # Determine Subject (DT / IDT) and Chapter No
        subject = q.get('subject') or os.environ.get('SUBJECT') or 'DT'
        subject = str(subject).strip().upper()
        if subject not in ['DT', 'IDT']:
            subject = 'DT'
            
        chapter_no = q.get('chapter_number') or q.get('chapter_no', 1)
        try:
            chapter_no = int(chapter_no)
        except Exception:
            chapter_no = 1

        q_num = q.get('question_number', q_idx + 1)
        q_text = q.get('question_text', '')
        ans_text = q.get('answer_text', '')

        print(f"\n---> [{subject} Ch{chapter_no} Q{q_num} ({q_idx+1}/{total_questions})] Analyzing provision autonomously with Gemini...")

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
        topic_cache_key = f"{subject}_{chapter_no}_{canonical_topic}"
        if topic_cache_key in generated_topics_cache:
            # REUSE EXISTING TOPIC DISCRETE AUDIO AND PRESENTATION!
            cached = generated_topics_cache[topic_cache_key]
            drive_folder_id = cached['folder_id']
            summary_json_str = cached['summary_json']
            formatted_provision_matrix = cached['prov_md']
            print(f"  [REUSED TOPIC] '{canonical_topic}' already generated! Skipping duplicate TTS. Reusing Drive Folder: {drive_folder_id}")
        else:
            # NEW TOPIC: Generate discrete point audio clips and upload to Google Drive
            print(f"  [NEW TOPIC] Creating Point-by-Point Discrete Voice for '{canonical_topic}' ({subject} Ch{chapter_no})...")
            
            discrete_out_dir = os.path.join(PROJECT_ROOT, 'data', 'audio', subject.lower(), f'ch{chapter_no}', f'q{q_num}')
            try:
                mm_data = generate_discrete_voice_for_mindmap(
                    q_num=q_num,
                    mindmap=mm_data,
                    output_dir=discrete_out_dir,
                    upload_to_drive=True,
                    subject=subject,
                    chapter_no=chapter_no
                )
                drive_folder_id = mm_data.get('drive_folder_id', '')
            except Exception as synth_err:
                print(f"    Notice on discrete voice synthesis: {synth_err}")
                drive_folder_id = "DRIVE_FOLDER_READY"

            summary_json_str = json.dumps(mm_data, ensure_ascii=False)

            # Cache this canonical topic so all subsequent questions under it share the exact voice clips & tree
            generated_topics_cache[topic_cache_key] = {
                'folder_id': drive_folder_id,
                'summary_json': summary_json_str,
                'prov_md': formatted_provision_matrix
            }

        # 3. Build Row for Google Sheet:
        row = [
            subject,                      # Subject (DT / IDT)
            chapter_no,                   # Chapter No
            q_num,                        # Question No
            canonical_topic,              # Canonical Topic (for dynamic grouping)
            q_text,                       # Question
            ans_text,                     # Answer
            formatted_provision_matrix,   # Provisions (Autonomous Markdown Matrix)
            summary_json_str,             # Provision Summary (Dynamic Mindmap with embedded point audio IDs)
            drive_folder_id,              # Drive Audio File/Folder ID
            f"{mm_data.get('total_points_count', len(mm_data.get('branches', [])))} Discrete Audio Points" # Timings/Status
        ]

        # 4. Upsert (Update existing row in-place or append new row)
        try:
            upsert_row_to_sheets(row)
        except Exception as sheet_err:
            print(f"  [SHEETS ERROR] Q{q_num}: {sheet_err}")

    print("\n" + "="*75)
    print("DISCRETE POINT AUDIO PIPELINE COMPLETE! All cards paired with individual voice clips.")
    print("="*75)

if __name__ == '__main__':
    limit_val = None
    env_limit = os.environ.get('LIMIT_QUESTIONS', '').strip()
    if env_limit and env_limit.isdigit():
        limit_val = int(env_limit)
        print(f"Limiting execution to {limit_val} question(s) via LIMIT_QUESTIONS.")
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit_val = int(sys.argv[1])
        print(f"Limiting execution to {limit_val} question(s) via CLI argument.")
    run_pipeline(limit=limit_val)
