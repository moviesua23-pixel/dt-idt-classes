# -*- coding: utf-8 -*-
"""
pipeline/apply_whisper_alignment_to_q32.py
Applies exact Whisper measured timestamps to dt-c2-q32 screenplay.
"""

import os
import sys
import json
import re
import librosa
from google.oauth2 import service_account
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.audio_screenplay_aligner import align_screenplay_to_measured_audio, generate_alignment_log_summary

SP_PATH = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", "dt-c2-q32.json")
WHISPER_PATH = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q32", "cache", "whisper_alignment.json")
CLIPS_DIR = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q32", "cache", "gemini_clips")

with open(SP_PATH, "r", encoding="utf-8") as f:
    sp = json.load(f)

# Load existing whisper transcripts and re-run b5 in English mode if b5 was empty
with open(WHISPER_PATH, "r", encoding="utf-8") as f:
    transcripts = json.load(f)

# Let's verify b5 in transcripts
if not transcripts.get("b5", {}).get("words"):
    from faster_whisper import WhisperModel
    print("Re-transcribing b5 with English model for precise word timings...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    audio, _ = librosa.load(os.path.join(CLIPS_DIR, "b5.mp3"), sr=16000)
    segs, info = model.transcribe(audio, language="en", vad_filter=False, word_timestamps=True)
    b5_words = []
    b5_segs = []
    for s in segs:
        seg_data = {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(), "words": []}
        if s.words:
            for w in s.words:
                w_data = {"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)}
                seg_data["words"].append(w_data)
                b5_words.append(w_data)
        b5_segs.append(seg_data)
    transcripts["b5"] = {
        "duration": round(float(librosa.get_duration(y=audio, sr=16000)), 2),
        "segments": b5_segs,
        "words": b5_words
    }
    with open(WHISPER_PATH, "w", encoding="utf-8") as f:
        json.dump(transcripts, f, indent=2, ensure_ascii=False)

# Re-run b4 in English mode if needed
if transcripts.get("b4") and len(transcripts["b4"]["words"]) < 10:
    from faster_whisper import WhisperModel
    print("Re-transcribing b4 with English model for precise word timings...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    audio, _ = librosa.load(os.path.join(CLIPS_DIR, "b4.mp3"), sr=16000)
    segs, info = model.transcribe(audio, language="en", vad_filter=False, word_timestamps=True)
    b4_words = []
    b4_segs = []
    for s in segs:
        seg_data = {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(), "words": []}
        if s.words:
            for w in s.words:
                w_data = {"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)}
                seg_data["words"].append(w_data)
                b4_words.append(w_data)
        b4_segs.append(seg_data)
    transcripts["b4"] = {
        "duration": round(float(librosa.get_duration(y=audio, sr=16000)), 2),
        "segments": b4_segs,
        "words": b4_words
    }
    with open(WHISPER_PATH, "w", encoding="utf-8") as f:
        json.dump(transcripts, f, indent=2, ensure_ascii=False)

# Execute acoustic alignment
aligned_sp = align_screenplay_to_measured_audio(sp, transcripts)

# Manual fine-tuning with acoustic anchors from whisper transcription
# Beat 1 (0.00 -> 23.40s)
b1 = aligned_sp["beats"][0]
b1["start"] = 0.0
b1["end"] = 23.40
b1["title"]["at"] = 0.3
b1["story_steps"][0]["at"] = 1.32  # "Gama Ltd's industrial undertaking"
b1["divider"]["at"] = 7.52         # "Shifting processil avaru..."
b1["branches"][0]["at"] = 9.5
b1["branches"][0]["facts"][0]["at"] = 9.94   # "land"
b1["branches"][0]["facts"][1]["at"] = 11.92  # "plant and machinery"
b1["branches"][0]["outcome"]["at"] = 12.80
b1["branches"][1]["at"] = 13.0
b1["branches"][1]["facts"][0]["at"] = 13.32  # "furniture"
b1["branches"][1]["facts"][1]["at"] = 14.50
b1["branches"][1]["outcome"]["at"] = 15.50
b1["result_card"]["at"] = 16.12               # "Pakshe section 54 is a very important trap"

# Beat 2 (23.65 -> 46.81s)
b2 = aligned_sp["beats"][1]
b2["start"] = 23.65
b2["end"] = 46.81
b2["title"]["at"] = 23.95
b2["quote"]["at"] = 24.25                     # "Section 54G clear aayi parayunnu"
b2["context_bubble"]["at"] = 38.71            # "1 year before or 3 years after" (23.65 + 15.06s)

# Beat 3 (47.06 -> 70.10s)
b3 = aligned_sp["beats"][2]
b3["start"] = 47.06
b3["end"] = 70.10
b3["title"]["at"] = 47.36
b3["breakdown"][0]["at"] = 50.96              # Land ₹4L (47.06 + 3.90s)
b3["breakdown"][1]["at"] = 53.08              # Building ₹7L (47.06 + 6.02s)
b3["breakdown"][2]["at"] = 54.94              # Plant & Machinery ₹17L (47.06 + 7.88s)
b3["meter_display"]["at"] = 57.40             # Total ₹28L (47.06 + 10.34s)
b3["breakdown"][3]["at"] = 59.72              # Furniture ₹2L Excluded (47.06 + 12.66s)
b3["outcome"] = {"text": "Eligible for Set-off against STCG & LTCG", "at": 64.12, "tone": "ok"}

# Beat 4 (70.35 -> 99.39s)
b4 = aligned_sp["beats"][3]
b4["start"] = 70.35
b4["end"] = 99.39
b4["title"]["at"] = 70.65
if "callout" in b4 and isinstance(b4["callout"], dict):
    b4["callout"]["at"] = 71.50                    # "Tax optimizationte golden trick ivideyanu!"
# Building & Plant STCG total 25 lakhs (70.35 + 15.06s = 85.41s)
b4["ledger_rows"][0]["at"] = 85.41            # Building STCG ₹14L
b4["ledger_rows"][1]["at"] = 86.43            # Plant & Machinery STCG ₹11L
b4["ledger_rows"][2]["at"] = 87.51            # Total Deemed STCG ₹25L
b4["ledger_rows"][3]["at"] = 89.43            # Less: Section 54G Exemption −₹25L
b4["ledger_rows"][4]["at"] = 91.07            # Net STCG ₹0
b4["ledger_rows"][5]["at"] = 91.97            # Land LTCG ₹4L (Balance ₹3L set off at 21.62s)
b4["ledger_rows"][6]["at"] = 93.95            # Less: Balance Section 54G Exemption −₹3L
b4["ledger_rows"][7]["at"] = 95.19            # Taxable LTCG on Land ₹1L
b4["ledger_rows"][8]["at"] = 95.80            # Furniture STCG ₹1L
b4["net_total"]["at"] = 97.91                 # Total Taxable Capital Gains ₹2L (just 2 lakhs mathram at 27.56s)

# Beat 5 (99.64 -> 125.40s)
b5 = aligned_sp["beats"][4]
b5["start"] = 99.64
b5["end"] = 125.40
b5["title"]["at"] = 99.94
b5["rules"][0]["at"] = 103.48                 # Rule 1: Furniture Excluded (99.64 + 3.84s)
b5["rules"][1]["at"] = 107.82                 # Rule 2: Section 50 STCG Eligible (99.64 + 8.18s)
b5["rules"][2]["at"] = 114.82                 # Rule 3: Beneficial Set-off Order (99.64 + 15.18s)

aligned_sp["duration_sec"] = 125.40

# Save aligned screenplay to file
with open(SP_PATH, "w", encoding="utf-8") as f:
    json.dump(aligned_sp, f, indent=2, ensure_ascii=False)

print(f"Successfully saved voice-synchronized screenplay to {SP_PATH}!")
timing_summary = generate_alignment_log_summary(aligned_sp)
print("\n" + timing_summary)

# Update explainer_engine.js FIXTURES["dt-c2-q32"]
ENGINE_JS_PATH = os.path.join(PROJECT_ROOT, "redesign_demo", "frontend", "explainer_engine.js")
with open(ENGINE_JS_PATH, "r", encoding="utf-8") as f:
    engine_code = f.read()

fixture_str = f'FIXTURES["dt-c2-q32"] = {json.dumps(aligned_sp, indent=2, ensure_ascii=False)};'

# Replace existing FIXTURES["dt-c2-q32"] or append
pattern = r'FIXTURES\["dt-c2-q32"\]\s*=\s*\{[\s\S]*?\n\s*\};'
if re.search(pattern, engine_code):
    engine_code = re.sub(pattern, fixture_str, engine_code, count=1)
    print("Updated existing FIXTURES['dt-c2-q32'] in explainer_engine.js!")
else:
    engine_code = engine_code.replace('FIXTURES["ch2_q14"] = FIXTURES["dt-c2-q14"];', f'FIXTURES["ch2_q14"] = FIXTURES["dt-c2-q14"];\n{fixture_str}')
    print("Inserted FIXTURES['dt-c2-q32'] into explainer_engine.js!")

with open(ENGINE_JS_PATH, "w", encoding="utf-8") as f:
    f.write(engine_code)

# Sync to Google Sheets (Row 47 = Q32)
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '14O9I8ZAjnIp8i4SFtM0xZX-y62f5BNtdh25ibSC7ChE')

if os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)

    # Find row for DT Ch 2 Q 32
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:C'
    ).execute()
    rows = res.get('values', [])
    target_row = None
    for idx, r in enumerate(rows, start=1):
        if len(r) >= 3 and str(r[0]).strip().upper() == "DT" and str(r[1]).strip() == "2" and str(r[2]).strip() == "32":
            target_row = idx
            break

    if target_row:
        sp_json_str = json.dumps(aligned_sp, ensure_ascii=False)
        body = {'values': [[timing_summary, sp_json_str]]}
        sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Sheet1!J{target_row}:K{target_row}',
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"Successfully updated Google Sheets Row {target_row} (Cols J & K) for DT Ch 2 Q 32!")
    else:
        print("Could not find row for DT Ch 2 Q 32 in Google Sheets!")
