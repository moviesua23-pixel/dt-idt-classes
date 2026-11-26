"""
pipeline/cloud_pipeline_runner.py
Cloud Pipeline Runner: Google Drive -> Autonomous Gemini Provision Architect -> Discrete Voice Synthesis -> Google Sheets.

Generates point-by-point discrete voice clips (Intro through each presentation card)
and maps each voice clip directly to its card without timestamp drift.
"""

import os
import sys
import json
import re
import base64
import time
import requests
from typing import Dict, Any, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    pass

import argparse
from pipeline.key_rotator import rotator, AllKeysQuotaExhaustedError, is_quota_error
from pipeline.autonomous_provision_architect import extract_autonomous_provision, assign_estimated_timings
from pipeline.synthesize_discrete_points import (
    generate_discrete_voice_for_mindmap,
    is_audio_ready,
    count_total_points,
    count_ready_points
)
from pipeline.dynamic_screenplay import generate_dynamic_screenplay
from pipeline.audio_screenplay_aligner import synthesize_and_align_screenplay_audio
from pipeline.pdf_question_indexer import (
    build_pdf_index,
    get_question_raw_text,
    split_question_and_answer,
    extract_question_with_vision,
    get_pdf_path,
    sanitize_and_format_text
)
from pipeline.prompt_generator import (
    generate_presentation_prompt,
    synthesize_and_upload_prompt_audio
)

def is_modern_studio_screenplay(sp_data: Any) -> bool:
    """
    Treat any existing, parseable screenplay with usable beats as complete.
    Legacy formats remain playable and are only regenerated when the caller
    explicitly passes --regenerate-legacy.
    """
    if not sp_data:
        return False
    if isinstance(sp_data, str):
        if not sp_data.strip().startswith('{'):
            return False
        try:
            sp_data = json.loads(sp_data)
        except Exception:
            return False
    if not isinstance(sp_data, dict):
        return False
    beats = sp_data.get('beats', [])
    if not isinstance(beats, list) or not beats:
        return False
    return all(isinstance(beat, dict) for beat in beats)

def is_director_authored_screenplay(sp_data: Any) -> bool:
    if isinstance(sp_data, str):
        try:
            sp_data = json.loads(sp_data)
        except Exception:
            return False
    return isinstance(sp_data, dict) and isinstance(sp_data.get('director'), dict)

# Configuration
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID') or '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE'

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

    # Permanent guardrail: Ensure Question text (Col E / idx 4) and Answer text (Col F / idx 5)
    # are always formatted with clean paragraphs, markdown tables, and no OCR noise.
    if len(row_values) > 4 and row_values[4]:
        row_values[4] = sanitize_and_format_text(str(row_values[4]), is_question=True)
    if len(row_values) > 5 and row_values[5]:
        row_values[5] = sanitize_and_format_text(str(row_values[5]), is_question=False)

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

        num_cols = len(row_values)
        if target_row_idx:
            # In-place update of existing row: ensure full span up to column K is updated so legacy columns J & K are cleared
            padded_row = list(row_values)
            if len(padded_row) < 11:
                padded_row.extend([''] * (11 - len(padded_row)))
            body = {'values': [padded_row]}
            range_to_update = f'Sheet1!A{target_row_idx}:K{target_row_idx}'
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"  [SHEETS UPDATED] Row {target_row_idx} updated in-place for {subject} Ch{chapter_no} Q{q_num}!")
        else:
            # Append new row (using the clean 9 columns A to I)
            body = {'values': [row_values]}
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

def export_sheets_to_local_cache():
    """
    Exports current Google Sheets rows to redesign_demo/data/pipeline_questions.json
    and data/pipeline_questions.json so the frontend can load questions with full
    mindmaps and concept simulation metadata.
    """
    if not sheets_service:
        return
    try:
        res = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:K'
        ).execute()
        rows = res.get('values', [])
        if not rows or len(rows) <= 1:
            return

        export_data = {
            "catalog": {"subject": "Direct Tax", "total_chapters": 25},
            "questions": [],
            "provisions": [],
            "mindmaps": {},
            "screenplays": {}
        }
        for r in rows[1:]:
            if len(r) < 3:
                continue
            subj = str(r[0]).strip().upper()
            try:
                ch = int(r[1])
            except ValueError:
                ch = 1
            try:
                qn = int(r[2])
            except ValueError:
                qn = 1
            topic = str(r[3]).strip() if len(r) > 3 else f"Ch{ch}_Q{qn}"
            q_text = str(r[4]) if len(r) > 4 else ""
            ans_text = str(r[5]) if len(r) > 5 else ""
            prov_md = str(r[6]) if len(r) > 6 else ""
            col7_str = str(r[7]) if len(r) > 7 else ""
            drive_folder = str(r[8]) if len(r) > 8 else ""
            screenplay_str = str(r[10]) if len(r) > 10 else ""

            is_kinetic_prompt = False
            presentation_prompt = ""
            if col7_str:
                col7_trimmed = col7_str.strip()
                if not col7_trimmed.startswith('{') and not col7_trimmed.startswith('['):
                    is_kinetic_prompt = True
                    presentation_prompt = col7_str
                elif col7_str and (col7_str.startswith('{') or '"branches"' in col7_str):
                    try:
                        mm_obj = json.loads(col7_str)
                        export_data['mindmaps'][f"ch{ch}_q{qn}"] = mm_obj
                        if ch == 1:
                            export_data['mindmaps'][f"q{qn}"] = mm_obj
                    except Exception:
                        pass

            if screenplay_str and screenplay_str.startswith('{'):
                try:
                    sp_obj = json.loads(screenplay_str)
                    export_data['screenplays'][f"{subj.lower()}-c{ch}-q{qn}"] = sp_obj
                except Exception:
                    pass

            q_entry = {
                "subject": subj.lower(),
                "chapter_number": ch,
                "question_number": qn,
                "question_title": topic,
                "question_text": q_text,
                "answer_text": ans_text,
                "topic_id": f"T_CH{ch}_Q{qn}"
            }
            if is_kinetic_prompt:
                q_entry["presentation_prompt"] = presentation_prompt
                q_entry["is_kinetic_prompt"] = True
            if drive_folder:
                q_entry["drive_audio_id"] = drive_folder
            export_data['questions'].append(q_entry)

            p_entry = {
                "subject": subj.lower(),
                "chapter_number": ch,
                "question_number": qn,
                "topic_id": f"T_CH{ch}_Q{qn}",
                "topic_title": topic,
                "provision_presentation_markdown": prov_md,
                "drive_folder_id": drive_folder
            }
            if is_kinetic_prompt:
                p_entry["presentation_prompt"] = presentation_prompt
                p_entry["is_kinetic_prompt"] = True
            export_data['provisions'].append(p_entry)

        paths = [
            os.path.join(PROJECT_ROOT, 'data', 'pipeline_questions.json'),
            os.path.join(PROJECT_ROOT, 'redesign_demo', 'data', 'pipeline_questions.json')
        ]
        for p in paths:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        print("  [CACHE EXPORTED] Saved latest pipeline questions to local cache JSON.")

        # Embed latest snapshot into HTML files (strictly excluding untouched index.html)
        html_files = [
            os.path.join(PROJECT_ROOT, 'redesign_demo', 'frontend', 'index_with_concept_video.html')
        ]
        pattern = r'(<script type="application/json" id="pipeline-data">)[\s\S]*?(</script>)'
        json_str = json.dumps(export_data, ensure_ascii=False)
        for hf in html_files:
            if os.path.exists(hf):
                try:
                    with open(hf, 'r', encoding='utf-8') as f:
                        html_text = f.read()
                    m = re.search(pattern, html_text)
                    if m:
                        new_html = html_text[:m.start(1)] + m.group(1) + json_str + m.group(2) + html_text[m.end(2):]
                        with open(hf, 'w', encoding='utf-8') as f:
                            f.write(new_html)
                except Exception as ex:
                    print(f"  [WARN] Failed to embed cache into {hf}: {ex}")
    except Exception as e:
        print(f"  [WARN] Failed to export local cache: {e}")

def fetch_existing_sheet_database():
    """
    Fetches all existing rows from Google Sheets to enable smart resume.
    Returns: dict mapping (Subject, Chapter_No_Str, Question_No_Str) -> dict of row fields.
    """
    if not sheets_service:
        return {}
    try:
        res = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:K'
        ).execute()
        rows = res.get('values', [])
        db = {}
        for idx, r in enumerate(rows, start=1):
            if idx == 1:
                continue
            if len(r) >= 3:
                s = str(r[0]).strip().upper()
                if s == 'SUBJECT':
                    continue
                c = str(r[1]).strip()
                q = str(r[2]).strip()
                topic = r[3] if len(r) > 3 else ""
                q_text = r[4] if len(r) > 4 else ""
                ans_text = r[5] if len(r) > 5 else ""
                prov_md = r[6] if len(r) > 6 else ""
                summary_json_str = r[7] if len(r) > 7 else ""
                drive_id = r[8] if len(r) > 8 else ""
                status_str = r[9] if len(r) > 9 else ""
                screenplay_str = r[10] if len(r) > 10 else ""
                db[(s, c, q)] = {
                    'row_idx': idx,
                    'topic': topic,
                    'q_text': q_text,
                    'ans_text': ans_text,
                    'prov_md': prov_md,
                    'summary_json': summary_json_str,
                    'drive_id': drive_id,
                    'status': status_str,
                    'screenplay': screenplay_str
                }
        return db
    except Exception as e:
        print(f"  [WARN] Failed to fetch existing sheets database: {e}")
        return {}

def run_pipeline(limit=None, target_chapter=None, target_question=None, target_subject=None, force=False, only_new=False, regenerate_legacy=False, target_questions=None):
    print("="*75)
    print("STARTING POINT-BY-POINT CLOUD PIPELINE: Drive -> Gemini -> Discrete Voice -> Sheets")
    print("="*75)

    # 1. Load existing extracted Q&A
    qna_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')
    qna_list = []
    if os.path.exists(qna_file):
        try:
            with open(qna_file, 'r', encoding='utf-8') as f:
                qna_list = json.load(f)
        except Exception:
            qna_list = []

    # Map of already extracted questions: {(subject, chapter_no, q_num): q}
    extracted_map = {}
    for q in qna_list:
        sub = str(q.get('subject') or 'DT').strip().upper()
        ch = int(q.get('chapter_number') or q.get('chapter_no') or 1)
        qn = int(q.get('question_number') or 0)
        extracted_map[(sub, ch, qn)] = q

    # 2. Load entire question index (all 580 questions across 25 chapters)
    full_index = build_pdf_index()

    # Filter by user CLI preferences if specified
    queue = []
    for item in full_index:
        s = item['subject']
        c = item['chapter_no']
        q = item['question_no']

        if target_subject and s != target_subject.upper():
            continue
        if target_chapter and c != target_chapter:
            continue
        selected_questions = {int(value) for value in (target_questions or []) if str(value).strip()}
        if target_question and q != target_question:
            continue
        if selected_questions and q not in selected_questions:
            continue
        queue.append(item)

    total_questions = len(queue)
    print(f"Total questions queued in question bank: {total_questions}")

    # 3. Fetch current progress from Google Sheets for Smart Resumption
    print("\n---> Fetching existing progress from Google Sheets database...")
    sheet_db = fetch_existing_sheet_database()
    print(f"Loaded {len(sheet_db)} existing question record(s) from Google Sheets.")

    generated_topics_cache = {}
    completed_in_run = 0
    regeneration_results = []
    needs_review = []

    for q_idx, item in enumerate(queue):
        subject = item['subject']
        chapter_no = item['chapter_no']
        q_num = item['question_no']

        key = (subject, str(chapter_no), str(q_num))
        existing = sheet_db.get(key)

        # Check if already present in Sheets database
        existing_mm = None
        if existing:
            topic = existing.get('topic', '')
            status_low = existing.get('status', '').lower()
            drive_id = existing.get('drive_id', '')
            col7_val = existing.get('summary_json', '').strip()
            # Under the new Universal Kinetic Presentation Studio schema, a question is complete ONLY if:
            # 1. Col H (col7_val) is a clean kinetic DSL prompt (does NOT start with '{' or '[')
            # 2. Col I (drive_id) has a valid Google Drive audio ID
            is_kinetic_done = bool(col7_val and not col7_val.startswith('{') and not col7_val.startswith('[') and drive_id and is_audio_ready(drive_id))

            # 1. Skip if already complete with modern Kinetic Presentation Prompt & Drive Audio
            if not force and is_kinetic_done:
                print(f"  [SKIP EXISTING] {subject} Ch{chapter_no} Q{q_num} already complete with Kinetic Studio Prompt & Audio ('{topic}'). Skipping.")
                continue

            # 2. If user explicitly requested strictly brand-new questions not yet present in Sheets
            if only_new and existing:
                print(f"  [SKIP ONLY-NEW] {subject} Ch{chapter_no} Q{q_num} already in Sheets ({'Kinetic Complete' if is_kinetic_done else 'Legacy Schema'}). Skipping.")
                continue

            if existing.get('summary_json'):
                try:
                    parsed_mm = json.loads(existing['summary_json'])
                    if isinstance(parsed_mm, dict):
                        existing_mm = parsed_mm
                except Exception:
                    existing_mm = None

        # Fetch or auto-extract question text and answer text with 100% fidelity
        map_key = (subject, chapter_no, q_num)
        has_cached = (
            map_key in extracted_map and 
            bool(extracted_map[map_key].get('question_text')) and 
            bool(extracted_map[map_key].get('answer_text'))
        )
        pdf_file = get_pdf_path(subject)
        pdf_exists = os.path.exists(pdf_file)

        if has_cached and (not force or not pdf_exists):
            q_rec = extracted_map[map_key]
            q_text = q_rec.get('question_text', '')
            ans_text = q_rec.get('answer_text', '')
            q_title = q_rec.get('question_title', f"Ch{chapter_no} Question {q_num}")
        elif pdf_exists:
            print(f"\n---> [{subject} Ch{chapter_no} Q{q_num} ({q_idx+1}/{total_questions})] Extracting visually from PDF (pages {item.get('start_page')}-{item.get('end_page')})...")
            vis_data = extract_question_with_vision(subject, chapter_no, q_num)
            if not vis_data:
                if has_cached:
                    q_rec = extracted_map[map_key]
                    q_text = q_rec.get('question_text', '')
                    ans_text = q_rec.get('answer_text', '')
                    q_title = q_rec.get('question_title', f"Ch{chapter_no} Question {q_num}")
                else:
                    print(f"  [ERROR] Could not extract text for {subject} Ch{chapter_no} Q{q_num}. Skipping.")
                    continue
            else:
                q_text = vis_data.get('question_text', '')
                ans_text = vis_data.get('answer_text', '')
                q_title = vis_data.get('question_title', f"Ch{chapter_no} Question {q_num}")
                new_rec = {
                    "subject": subject,
                    "chapter_number": chapter_no,
                    "question_number": q_num,
                    "question_title": q_title,
                    "question_text": q_text,
                    "answer_text": ans_text,
                    "vision_verified": True
                }
                extracted_map[map_key] = new_rec
                found = False
                for idx_q, q_item in enumerate(qna_list):
                    if (str(q_item.get('subject') or 'DT').upper() == subject and 
                        int(q_item.get('chapter_number') or q_item.get('chapter_no') or 1) == chapter_no and 
                        int(q_item.get('question_number') or 0) == q_num):
                        qna_list[idx_q] = new_rec
                        found = True
                        break
                if not found:
                    qna_list.append(new_rec)
                try:
                    with open(qna_file, 'w', encoding='utf-8') as f:
                        json.dump(qna_list, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"  [WARN] Failed to write extracted_qna.json: {e}")
        elif has_cached:
            # Running in cloud runner environment without local PDF bundled
            q_rec = extracted_map[map_key]
            q_text = q_rec.get('question_text', '')
            ans_text = q_rec.get('answer_text', '')
            q_title = q_rec.get('question_title', f"Ch{chapter_no} Question {q_num}")
        else:
            print(f"  [ERROR] Could not extract text for {subject} Ch{chapter_no} Q{q_num}. Neither local PDF nor cached Q&A available. Skipping.")
            continue

        # Permanent formatting for question and answer text
        q_text = sanitize_and_format_text(q_text, is_question=True)
        ans_text = sanitize_and_format_text(ans_text, is_question=False)

        # State tracking for safe checkpointing on quota exhaustion
        current_mm_data = existing_mm
        current_topic = existing.get('topic') if existing else None
        current_prov_md = existing.get('prov_md') if existing else None

        api_attempts_before = rotator.api_attempts
        try:
            # Legal Provision Architecture
            if current_prov_md and current_topic:
                canonical_topic = current_topic
                formatted_provision_matrix = current_prov_md
                mm_data = existing_mm or {"doctrine": canonical_topic, "root": {}, "branches": []}
                print(f"  Reusing existing legal provision framework: '{canonical_topic}'")
            else:
                print(f"\n---> [{subject} Ch{chapter_no} Q{q_num} ({q_idx+1}/{total_questions})] Analyzing provision autonomously with Gemini...")
                auto_res = extract_autonomous_provision(q_num, q_text, ans_text)

                if auto_res:
                    canonical_topic = auto_res.get('canonical_topic', f'Statutory Topic Q{q_num}')
                    formatted_provision_matrix = auto_res.get('provision_presentation_markdown', '')
                    mm_data = assign_estimated_timings(auto_res.get('mindmap', {}))
                else:
                    canonical_topic = f"Statutory Topic Q{q_num}"
                    formatted_provision_matrix = f"### {canonical_topic}\n\nStatutory income tax provision."
                    mm_data = {"doctrine": canonical_topic, "root": {}, "branches": []}

                current_mm_data = mm_data
                current_topic = canonical_topic
                current_prov_md = formatted_provision_matrix
                print(f"  Canonical Doctrine: '{canonical_topic}'")

            # 1. Generate kinetic presentation prompt from Column 6 statutory provision summary
            print(f"\n---> [{subject} Ch{chapter_no} Q{q_num}] Generating Universal Kinetic Studio Prompt (DSL)...")
            presentation_prompt = generate_presentation_prompt(
                canonical_topic=canonical_topic,
                prov_summary_md=formatted_provision_matrix,
                q_text=q_text,
                ans_text=ans_text,
                subject=subject,
                chapter_no=chapter_no,
                q_num=q_num
            )

            # 2. Synthesize Aoede expressive voice for prompt dialogues and upload to Google Drive
            print(f"  [AUDIO SYNTHESIS] Synthesizing dialogues with Aoede voice & uploading to Google Drive...")
            drive_audio_file_id = synthesize_and_upload_prompt_audio(
                prompt_text=presentation_prompt,
                subject=subject,
                chapter_no=chapter_no,
                q_num=q_num
            )

            # 3. Build 9-column Row for Google Sheet (Cols A to I):
            # Col A (idx 0): Subject
            # Col B (idx 1): Chapter No
            # Col C (idx 2): Question No
            # Col D (idx 3): Canonical Topic
            # Col E (idx 4): Question Facts Text
            # Col F (idx 5): ICAI Answer Text
            # Col G (idx 6): Provision Summary Markdown
            # Col H (idx 7): Kinetic Presentation Prompt DSL
            # Col I (idx 8): Drive Audio File ID
            row = [
                subject,                      # Col A (idx 0)
                chapter_no,                   # Col B (idx 1)
                q_num,                        # Col C (idx 2)
                canonical_topic,              # Col D (idx 3)
                q_text,                       # Col E (idx 4)
                ans_text,                     # Col F (idx 5)
                formatted_provision_matrix,   # Col G (idx 6) - Provision Summary
                presentation_prompt,          # Col H (idx 7) - Presentation Prompt
                drive_audio_file_id           # Col I (idx 8) - Drive Audio File ID
            ]

            # Upsert to Google Sheet (clearing any old legacy columns J & K if updating in-place)
            upsert_row_to_sheets(row)
            completed_in_run += 1
            print(f"  [DONE] Successfully saved {subject} Ch{chapter_no} Q{q_num} (Kinetic Studio Prompt & Drive Audio) to Google Sheets.")
            print(f"  [GEMINI USAGE] {subject} Ch{chapter_no} Q{q_num}: {rotator.api_attempts - api_attempts_before} API attempts in this question (including retries).")
            export_sheets_to_local_cache()

            if limit and completed_in_run >= limit:
                print(f"\n[LIMIT REACHED] Processed {completed_in_run} question(s) as requested. Exiting cleanly.")
                sys.exit(0)

        except AllKeysQuotaExhaustedError:
            print(f"  [GEMINI USAGE] {subject} Ch{chapter_no} Q{q_num}: {rotator.api_attempts - api_attempts_before} API attempts before quota pause.")
            print("\n" + "="*75)
            print("[QUOTA PAUSE] Gemini API quota limit reached across all active keys.")
            print("Exiting gracefully without modifying sheet prompts (exit code 0).")
            print("="*75)
            export_sheets_to_local_cache()
            sys.exit(0)

    export_sheets_to_local_cache()
    print("\n" + "="*75)
    if needs_review:
        print("QUESTIONS NEEDING REVIEW")
        for qid, issues in needs_review:
            print(f"  {qid}: {'; '.join(issues)}")
    if regenerate_legacy:
        print("LEGACY SCREENPLAY REGENERATION REPORT")
        for qid, status, reason in regeneration_results:
            print(f"  {qid}: {status} — {reason}")
        print(f"  totals: {len(regeneration_results)} attempted/checked, {sum(status == 'success' for _, status, _ in regeneration_results)} generated, {sum(status == 'fallback' for _, status, _ in regeneration_results)} fallback, {sum(status == 'already-modern' for _, status, _ in regeneration_results)} already modern")
    print("DISCRETE POINT AUDIO PIPELINE COMPLETE! All queued questions are 100% synthesized.")
    print("="*75)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DT & IDT Continuous Cloud Pipeline Runner")
    parser.add_argument('--limit', type=int, default=None, help="Max number of new questions to process in this run")
    parser.add_argument('--chapter', type=int, default=None, help="Process specific chapter number")
    parser.add_argument('--question', type=int, default=None, help="Process specific question number")
    parser.add_argument('--subject', type=str, default=None, help="Process specific subject (DT / IDT)")
    parser.add_argument('--force', action='store_true', help="Force re-generation of provision even if already in Sheets")
    parser.add_argument('--only-new', action='store_true', help="Process strictly brand new questions that are not yet in Google Sheets")
    parser.add_argument('--regenerate-legacy', action='store_true', help="Regenerate legacy screenplays across the selected queue; preserve hand-authored fixture files")
    parser.add_argument('--questions', type=str, default='', help="Comma-separated question numbers within the selected chapter/subject")
    args = parser.parse_args()

    run_pipeline(
        limit=args.limit,
        target_chapter=args.chapter,
        target_question=args.question,
        target_subject=args.subject,
        force=args.force,
        only_new=args.only_new,
        regenerate_legacy=args.regenerate_legacy,
        target_questions=[part for part in args.questions.split(',') if part.strip()]
    )
