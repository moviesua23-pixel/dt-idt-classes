# -*- coding: utf-8 -*-
import os
import sys
import json
import librosa
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"C:\Users\HP\OneDrive\Desktop\VISHNU\DT and IDT Classes"
CACHE_DIR = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q25", "cache", "gemini_clips")

print("Initializing WhisperModel...")
model = WhisperModel("base", device="cpu", compute_type="int8")

transcripts = {}
for i in range(1, 7):
    beat_id = f"b{i}"
    wav_path = os.path.join(CACHE_DIR, f"{beat_id}.wav")
    print(f"\n--- Transcribing {beat_id} ({wav_path}) ---")
    audio, _ = librosa.load(wav_path, sr=16000)
    segments, info = model.transcribe(audio, language="ml", word_timestamps=True)
    
    beat_words = []
    seg_list = []
    for s in segments:
        seg_info = {
            "start": round(s.start, 2),
            "end": round(s.end, 2),
            "text": s.text.strip(),
            "words": []
        }
        if s.words:
            for w in s.words:
                w_info = {
                    "word": w.word.strip(),
                    "start": round(w.start, 2),
                    "end": round(w.end, 2)
                }
                seg_info["words"].append(w_info)
                beat_words.append(w_info)
        seg_list.append(seg_info)
        print(f"[{seg_info['start']}s -> {seg_info['end']}s] {seg_info['text']}")
    
    transcripts[beat_id] = {
        "segments": seg_list,
        "words": beat_words
    }

out_path = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q25", "cache", "whisper_alignment.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(transcripts, f, indent=2, ensure_ascii=False)

print(f"\nAll 6 beats successfully transcribed and saved to {out_path}!")
