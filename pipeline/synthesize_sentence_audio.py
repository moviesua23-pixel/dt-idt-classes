import os
import sys
import json
import wave
import subprocess
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.synthesize_ppt_audio import generate_slide_audio_pcm
from pipeline.audit_sentence_timings import split_sentences as split_into_sentences

AUDIO_V2_DIR = os.path.join(PROJECT_ROOT, "data", "audio_v2")
TEMP_DIR = os.path.join(PROJECT_ROOT, "data", "audio_temp_v2")
os.makedirs(AUDIO_V2_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

STORYBOARD_PATH = os.path.join(PROJECT_ROOT, "data", "ppt_storyboards.json")
MINDMAPS_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")
TIMING_OUTPUT = os.path.join(PROJECT_ROOT, "data", "measured_sentence_timings.json")

GAP_DURATION_SEC = 0.250  # Fixed 250ms silence between sentences
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2  # 16-bit PCM

def synthesize_topic_v2(topic_key="q4"):
    """
    Method A: Per-sentence re-synthesis with Gemini Aoede.
    Generates audio for each sentence, records exact duration,
    joins them with a 250ms silence gap, and outputs data/audio_v2/qN.mp3.
    """
    print(f"\n[METHOD A] Synthesizing exact sentence audio for {topic_key.upper()}...", flush=True)
    with open(STORYBOARD_PATH, "r", encoding="utf-8") as f:
        storyboards = json.load(f)
    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)

    sb = storyboards.get(topic_key, {})
    slides = sb.get("slides", [])
    if not slides:
        print(f"No slides found for {topic_key}")
        return None

    all_sentence_clips = []
    cumulative_time = 0.0
    slide_boundaries = []
    beat_timings = []

    silence_bytes = b'\x00' * int(SAMPLE_RATE * BYTES_PER_SAMPLE * GAP_DURATION_SEC)

    for slide in slides:
        s_num = slide.get("slide_number", 1)
        narration = slide.get("malayalam_narration", "")
        sentences = split_into_sentences(narration)
        slide_start_time = cumulative_time

        print(f"  Slide {s_num}: {len(sentences)} sentences", flush=True)

        for s_idx, sentence_text in enumerate(sentences, 1):
            print(f"    Synthesizing s{s_num}_{s_idx} ({len(sentence_text)} chars)...", end="", flush=True)
            pcm_bytes = generate_slide_audio_pcm(sentence_text)
            if not pcm_bytes:
                print(" FAILED!", flush=True)
                return None
            
            clip_dur = len(pcm_bytes) / (SAMPLE_RATE * BYTES_PER_SAMPLE)
            t0 = cumulative_time
            t1 = t0 + clip_dur

            print(f" OK ({clip_dur:.2f}s: {t0:.2f}s -> {t1:.2f}s)", flush=True)

            all_sentence_clips.append(pcm_bytes)
            # Add 250ms gap
            all_sentence_clips.append(silence_bytes)

            beat_timings.append({
                "slide_number": s_num,
                "sentence_idx": s_idx,
                "text": sentence_text,
                "t0": round(t0, 3),
                "t1": round(t1, 3),
                "duration": round(clip_dur, 3)
            })

            cumulative_time = t1 + GAP_DURATION_SEC
            time.sleep(0.3)

        slide_end_time = cumulative_time - GAP_DURATION_SEC  # without trailing gap
        slide_boundaries.append({
            "slide_number": s_num,
            "t0": round(slide_start_time, 3),
            "t1": round(slide_end_time, 3),
            "duration": round(slide_end_time - slide_start_time, 3)
        })

    # Join all PCM data
    total_pcm = b"".join(all_sentence_clips)
    raw_pcm_path = os.path.join(TEMP_DIR, f"{topic_key}_joined.pcm")
    with open(raw_pcm_path, "wb") as f:
        f.write(total_pcm)

    # Encode to MP3 using ffmpeg
    out_mp3_path = os.path.join(AUDIO_V2_DIR, f"{topic_key}.mp3")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "s16le",
        "-ar", str(SAMPLE_RATE),
        "-ac", "1",
        "-i", raw_pcm_path,
        "-b:a", "192k",
        out_mp3_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[OK] Generated {out_mp3_path} (Total Length: {cumulative_time - GAP_DURATION_SEC:.2f}s)", flush=True)

    result_data = {
        "topic": topic_key,
        "audio_file": out_mp3_path,
        "total_duration": round(cumulative_time - GAP_DURATION_SEC, 3),
        "slides": slide_boundaries,
        "beats": beat_timings
    }

    # Save to measured timings
    existing = {}
    if os.path.exists(TIMING_OUTPUT):
        try:
            with open(TIMING_OUTPUT, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = {}
    existing[topic_key] = result_data
    with open(TIMING_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return result_data

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "q4"
    synthesize_topic_v2(target)
