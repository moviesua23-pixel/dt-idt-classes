import os
import sys
import json
import shutil
import time

PROJECT_ROOT = r"c:\Users\HP\OneDrive\Desktop\VISHNU\DT and IDT Classes"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.synthesize_discrete_points import upload_audio_to_drive, drive_service

CH3_Q3_FOLDER_ID = "1cwN4esYaF_KZ-SuMOIJoDrga0yJjrwVh"
AUDIO_DIR = os.path.join(PROJECT_ROOT, "data", "audio", "dt", "ch3", "q3")

CUE_MAPPINGS = [
    # Slide 1
    {"slide": 1, "part": 1, "old": "slide_1_part_1.mp3", "new": "slide1_01_man.mp3", "shape": "man", "label": "CA Rajesh"},
    {"slide": 1, "part": 2, "old": "slide_1_part_2.mp3", "new": "slide1_02_card1.mp3", "shape": "card", "label": "Card 1"},
    {"slide": 1, "part": 3, "old": "slide_1_part_3.mp3", "new": "slide1_03_card2.mp3", "shape": "card", "label": "Card 2"},
    {"slide": 1, "part": 4, "old": "slide_1_part_4.mp3", "new": "slide1_04_card3.mp3", "shape": "card", "label": "Card 3"},
    {"slide": 1, "part": 5, "old": "slide_1_part_5.mp3", "new": "slide1_05_card4.mp3", "shape": "card", "label": "Card 4"},

    # Slide 2
    {"slide": 2, "part": 1, "old": "slide_2_part_1.mp3", "new": "slide2_01_officer.mp3", "shape": "officer", "label": "Tax Officer"},
    {"slide": 2, "part": 2, "old": "slide_2_part_2.mp3", "new": "slide2_02_step1.mp3", "shape": "timeline_step", "label": "Stage 1"},
    {"slide": 2, "part": 3, "old": "slide_2_part_3.mp3", "new": "slide2_03_step2.mp3", "shape": "timeline_step", "label": "Stage 2"},
    {"slide": 2, "part": 4, "old": "slide_2_part_4.mp3", "new": "slide2_04_step3.mp3", "shape": "timeline_step", "label": "Stage 3"},
    {"slide": 2, "part": 5, "old": "slide_2_part_5.mp3", "new": "slide2_05_step4.mp3", "shape": "timeline_step", "label": "Stage 4"},

    # Slide 3
    {"slide": 3, "part": 1, "old": "slide_3_part_1.mp3", "new": "slide3_01_clause_a.mp3", "shape": "clause", "label": "Clause A"},
    {"slide": 3, "part": 2, "old": "slide_3_part_2.mp3", "new": "slide3_02_clause_b.mp3", "shape": "clause", "label": "Clause B"},
    {"slide": 3, "part": 3, "old": "slide_3_part_3.mp3", "new": "slide3_03_clause_c.mp3", "shape": "clause", "label": "Clause C"},
    {"slide": 3, "part": 4, "old": "slide_3_part_4.mp3", "new": "slide3_04_clause_d.mp3", "shape": "clause", "label": "Clause D"},
]

def upload_all_discrete():
    print(f"Preparing to upload {len(CUE_MAPPINGS)} discrete audio files to Google Drive folder Ch3_Q3 ({CH3_Q3_FOLDER_ID})...")

    # Load existing timings.json to preserve duration_ms, start_ms, and dialogue text
    timings_path = os.path.join(AUDIO_DIR, "timings.json")
    with open(timings_path, 'r', encoding='utf-8') as f:
        slides_timings = json.load(f)

    # First copy/ensure new names exist locally
    for m in CUE_MAPPINGS:
        old_path = os.path.join(AUDIO_DIR, m['old'])
        new_path = os.path.join(AUDIO_DIR, m['new'])
        if os.path.exists(old_path) and not os.path.exists(new_path):
            shutil.copy2(old_path, new_path)
            print(f"  Created local alias: {m['new']}")

    # Check already uploaded files in Drive folder
    q = f"'{CH3_Q3_FOLDER_ID}' in parents and trashed=false"
    res = drive_service.files().list(q=q, fields='files(id, name)').execute()
    drive_existing = {f['name']: f['id'] for f in res.get('files', [])}
    print(f"Found {len(drive_existing)} existing files in Drive folder.")

    uploaded_map = {}

    for idx, m in enumerate(CUE_MAPPINGS, 1):
        target_file = os.path.join(AUDIO_DIR, m['new'])
        if not os.path.exists(target_file):
            target_file = os.path.join(AUDIO_DIR, m['old'])

        file_name = m['new']
        if file_name in drive_existing:
            file_id = drive_existing[file_name]
            print(f"[{idx}/{len(CUE_MAPPINGS)}] {file_name} already in Drive! ID: {file_id}")
        else:
            print(f"[{idx}/{len(CUE_MAPPINGS)}] Uploading {file_name} ({os.path.getsize(target_file)} bytes) to Drive...")
            file_id = upload_audio_to_drive(target_file, CH3_Q3_FOLDER_ID, file_name)
            print(f"  ✓ Uploaded: {file_id}")
            time.sleep(1) # Brief pause between uploads

        uploaded_map[file_name] = file_id

    # Update slides_timings manifest with discrete file details
    for s in slides_timings:
        s_idx = s['slide_idx']
        for cue in s.get('cues', []):
            part = cue['part']
            m = next((item for item in CUE_MAPPINGS if item['slide'] == s_idx and item['part'] == part), None)
            if m:
                new_name = m['new']
                fid = uploaded_map.get(new_name, "")
                cue['file_name'] = new_name
                cue['shape'] = m['shape']
                cue['label'] = m['label']
                cue['drive_file_id'] = fid
                cue['stream_url'] = f"https://drive.google.com/uc?export=download&id={fid}"
                cue['audio_file'] = f"dt/ch3/q3/{new_name}"

    with open(timings_path, 'w', encoding='utf-8') as f:
        json.dump(slides_timings, f, indent=2)
    print(f"\n✓ Updated {timings_path} with all discrete Drive File IDs!")

    # Update pipeline_questions.json files
    pq_paths = [
        os.path.join(PROJECT_ROOT, "data", "pipeline_questions.json"),
        os.path.join(PROJECT_ROOT, "redesign_demo", "data", "pipeline_questions.json")
    ]
    for pth in pq_paths:
        if os.path.exists(pth):
            with open(pth, 'r', encoding='utf-8') as f:
                pq_data = json.load(f)
            q_list = pq_data.get('questions', []) if isinstance(pq_data, dict) else pq_data
            found = False
            for q_item in q_list:
                if isinstance(q_item, dict) and q_item.get('subject', '').lower() == 'dt' and q_item.get('chapter_number') == 3 and q_item.get('question_number') == 3:
                    q_item['audio_timings'] = slides_timings
                    q_item['drive_folder_id'] = CH3_Q3_FOLDER_ID
                    found = True
                    break
            if found:
                with open(pth, 'w', encoding='utf-8') as f:
                    json.dump(pq_data, f, indent=2)
                print(f"✓ Updated {pth} with discrete audio_timings.")

if __name__ == '__main__':
    upload_all_discrete()
