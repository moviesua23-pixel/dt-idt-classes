"""
pipeline/batch_vision_extractor.py
Batch Visual Extraction Tool for CA Final DT and IDT.
Iterates through chapters/questions, extracts them with 100% visual fidelity
using PyMuPDF rasterization + Gemini Vision with key rotation, and syncs
both data/extracted_qna.json and Google Sheets.
"""

import os
import sys
import json
import time
import argparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    pass

from pipeline.pdf_question_indexer import build_pdf_index, extract_question_with_vision, sanitize_and_format_text
from pipeline.cloud_client import CloudClient, SPREADSHEET_ID

def run_batch_vision(subject="DT", chapter=None, question=None, force=False):
    print("\n=======================================================")
    print("=== BATCH VISION EXTRACTOR (100% VISUAL FIDELITY) ===")
    print(f"=== Subject: {subject} | Chapter: {chapter or 'ALL'} | Question: {question or 'ALL'} ===")
    print("=======================================================\n")

    # 1. Load full PDF index
    full_index = build_pdf_index()
    queue = []
    for item in full_index:
        if subject and item['subject'].upper() != subject.upper():
            continue
        if chapter and item['chapter_no'] != chapter:
            continue
        if question and item['question_no'] != question:
            continue
        queue.append(item)

    print(f"Total target questions to process: {len(queue)}")

    # 2. Load extracted_qna.json
    qna_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')
    qna_list = []
    if os.path.exists(qna_file):
        try:
            with open(qna_file, 'r', encoding='utf-8') as f:
                qna_list = json.load(f)
        except Exception:
            qna_list = []

    qna_map = {}
    for q in qna_list:
        sub = str(q.get('subject') or 'DT').upper()
        ch = int(q.get('chapter_number') or q.get('chapter_no') or 1)
        qn = int(q.get('question_number') or 0)
        qna_map[(sub, ch, qn)] = q

    # 3. Load Google Sheet mapping for sync
    cc = CloudClient()
    sheet_rows = []
    try:
        res = cc.sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:H'
        ).execute()
        sheet_rows = res.get('values', [])
    except Exception as e:
        print(f"[WARN] Could not fetch Google Sheet rows: {e}")

    sheet_index_map = {}
    for idx, r in enumerate(sheet_rows[1:], start=2):
        s = r[0].strip().upper() if len(r) > 0 else ''
        c = int(r[1].strip()) if len(r) > 1 and r[1].strip().isdigit() else None
        q = int(r[2].strip()) if len(r) > 2 and r[2].strip().isdigit() else None
        if s and c is not None and q is not None:
            sheet_index_map[(s, c, q)] = idx

    success_count = 0
    sheet_updates = []

    for idx, item in enumerate(queue):
        s = item['subject']
        c = item['chapter_no']
        q = item['question_no']
        key = (s, c, q)

        existing = qna_map.get(key)
        if existing and existing.get('vision_verified') and not force:
            print(f"[{idx+1}/{len(queue)}] {s} Ch{c} Q{q} already vision-verified. Skipping.")
            continue

        print(f"\n---> [{idx+1}/{len(queue)}] Visually extracting {s} Ch{c} Q{q} (Pages {item['start_page']}-{item['end_page']})...")
        vis_data = extract_question_with_vision(s, c, q)
        if not vis_data:
            print(f"  [ERROR] Vision extraction failed for {s} Ch{c} Q{q}.")
            continue

        vis_rec = {
            "subject": s,
            "chapter_number": c,
            "question_number": q,
            "question_title": vis_data.get('question_title', f"Ch{c} Question {q}"),
            "question_text": sanitize_and_format_text(vis_data.get('question_text', ''), is_question=True),
            "answer_text": sanitize_and_format_text(vis_data.get('answer_text', ''), is_question=False),
            "vision_verified": True
        }

        # Update in-memory and file
        qna_map[key] = vis_rec
        found = False
        for i, existing_item in enumerate(qna_list):
            if (str(existing_item.get('subject') or 'DT').upper() == s and
                int(existing_item.get('chapter_number') or 1) == c and
                int(existing_item.get('question_number') or 0) == q):
                qna_list[i] = vis_rec
                found = True
                break
        if not found:
            qna_list.append(vis_rec)

        with open(qna_file, 'w', encoding='utf-8') as f:
            json.dump(qna_list, f, indent=2, ensure_ascii=False)

        # Queue Google Sheet sync
        if key in sheet_index_map:
            sheet_row_num = sheet_index_map[key]
            sheet_updates.append({
                'range': f'Sheet1!E{sheet_row_num}:F{sheet_row_num}',
                'values': [[vis_rec['question_text'], vis_rec['answer_text']]]
            })

        success_count += 1
        print(f"  [OK] Successfully extracted and saved {s} Ch{c} Q{q}!")
        time.sleep(1)

    # Batch update Google Sheet
    if sheet_updates:
        print(f"\n---> Syncing {len(sheet_updates)} updated questions to Google Sheets...")
        try:
            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': sheet_updates
            }
            cc.sheets.spreadsheets().values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            print("  [OK] Google Sheets updated successfully!")
        except Exception as e:
            print(f"  [WARN] Failed to batch update Google Sheets: {e}")

    print("\n=======================================================")
    print(f"=== BATCH VISION COMPLETE: {success_count}/{len(queue)} UPGRADED ===")
    print("=======================================================\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Batch Vision Extractor for DT and IDT")
    parser.add_argument('--subject', default='DT', help="DT or IDT")
    parser.add_argument('--chapter', type=int, default=None, help="Target Chapter Number")
    parser.add_argument('--question', type=int, default=None, help="Target Question Number")
    parser.add_argument('--force', action='store_true', help="Force re-extraction even if already vision-verified")
    args = parser.parse_args()

    run_batch_vision(args.subject, args.chapter, args.question, args.force)
