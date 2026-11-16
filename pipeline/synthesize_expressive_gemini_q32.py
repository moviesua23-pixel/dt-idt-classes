# -*- coding: utf-8 -*-
"""
pipeline/synthesize_expressive_gemini_q32.py
Synthesizes the 5 pedagogical screenplay beats of Q32 into redesign_demo/data/audio/dt-c2-q32.mp3
using pipeline.phase3_audio.generate_gemini_audio
"""
import os
import sys
import json
import time
from pydub import AudioSegment

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.phase3_audio import generate_gemini_audio

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q32", "cache", "gemini_clips")
os.makedirs(TEMP_DIR, exist_ok=True)

def load_screenplay_beats():
    sp_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", "dt-c2-q32.json")
    with open(sp_path, "r", encoding="utf-8") as f:
        sp = json.load(f)
    return sp.get("beats", [])

def main():
    print("=== SYNTHESIZING EXPRESSIVE GEMINI VOICE FOR Q32 ===")
    beats = load_screenplay_beats()
    clips = []
    beat_durations = {}

    for b in beats:
        beat_id = b["id"]
        clip_path = os.path.join(TEMP_DIR, f"{beat_id}.mp3")
        if os.path.exists(clip_path) and os.path.getsize(clip_path) > 5000:
            print(f"Beat {beat_id} already cached, loading...", flush=True)
            seg = AudioSegment.from_file(clip_path)
            dur = len(seg) / 1000.0
        else:
            print(f"Synthesizing Beat {beat_id}...", flush=True)
            generate_gemini_audio(b["voice_sync_text"], clip_path, voice_name="Aoede")
            seg = AudioSegment.from_file(clip_path)
            dur = len(seg) / 1000.0
            print(f"  -> Beat {beat_id} synthesized: {dur:.2f}s", flush=True)
            time.sleep(1.0)
        clips.append(seg)
        beat_durations[beat_id] = dur

    print("\nStitching final audio with breath pauses (350ms)...")
    silence = AudioSegment.silent(duration=350)
    full_audio = AudioSegment.empty()
    for i, c in enumerate(clips):
        full_audio += c
        if i < len(clips) - 1:
            full_audio += silence

    out_mp3 = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "audio", "dt-c2-q32.mp3")
    os.makedirs(os.path.dirname(out_mp3), exist_ok=True)
    full_audio.export(out_mp3, format="mp3", bitrate="192k")
    total_dur = len(full_audio) / 1000.0
    print(f"SUCCESS! Exported dt-c2-q32.mp3 ({total_dur:.2f}s) to {out_mp3}")

    # Update timing offsets in dt-c2-q32.json
    sp_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", "dt-c2-q32.json")
    with open(sp_path, "r", encoding="utf-8") as f:
        sp = json.load(f)

    curr_t = 0.0
    for b in sp["beats"]:
        b_dur = beat_durations.get(b["id"], 20.0)
        b["start"] = round(curr_t, 2)
        b["end"] = round(curr_t + b_dur, 2)
        curr_t += b_dur + 0.35

    sp["duration_sec"] = round(curr_t - 0.35, 2)
    with open(sp_path, "w", encoding="utf-8") as f:
        json.dump(sp, f, indent=2, ensure_ascii=False)
    print(f"Updated screenplay timings in {sp_path} (duration: {sp['duration_sec']}s)")

if __name__ == "__main__":
    main()
