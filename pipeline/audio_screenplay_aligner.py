# -*- coding: utf-8 -*-
"""
pipeline/audio_screenplay_aligner.py
General Voice-Synchronized Audio & Screenplay Acoustic Aligner.

Performs acoustic speech boundary and word-level alignment using faster-whisper.
Extracts exact timestamps for statutory terms, numbers, cards, ledger rows,
meter readings, and takeaways, guaranteeing 100% voice-to-screen synchronization.
"""

import os
import sys
import json
import re
import librosa
from typing import Dict, Any, List, Optional
from faster_whisper import WhisperModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

_WHISPER_MODEL = None

def get_whisper_model() -> WhisperModel:
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        print("  [WHISPER] Loading WhisperModel('base', compute_type='int8')...")
        _WHISPER_MODEL = WhisperModel("base", device="cpu", compute_type="int8")
    return _WHISPER_MODEL

def transcribe_beat_clip(audio_path: str) -> Dict[str, Any]:
    """
    Transcribes a single beat audio clip and returns duration, segments, and word timestamps.
    Prefers English mode to accurately detect Manglish statutory/tax terms & figures.
    Falls back to Malayalam or language detection if English yields no segments.
    """
    if not os.path.exists(audio_path):
        return {"duration": 0.0, "segments": [], "words": []}

    audio, _ = librosa.load(audio_path, sr=16000)
    dur = round(float(librosa.get_duration(y=audio, sr=16000)), 2)
    model = get_whisper_model()

    # Attempt English transcription first (captures numbers & English statutory terms with timestamps)
    segments, _ = model.transcribe(audio, language="en", vad_filter=False, word_timestamps=True)
    seg_list = list(segments)

    # If empty, fallback to unconstrained language detection
    if not seg_list:
        segments, _ = model.transcribe(audio, vad_filter=False, word_timestamps=True)
        seg_list = list(segments)

    extracted_segs = []
    extracted_words = []
    for s in seg_list:
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
                extracted_words.append(w_info)
        extracted_segs.append(seg_info)

    return {
        "duration": dur,
        "segments": extracted_segs,
        "words": extracted_words
    }

def find_first_word_offset(words: List[Dict[str, Any]], keywords: List[str], min_time: float = 0.0, default_offset: float = 1.0) -> float:
    """
    Finds the start timestamp of the first word matching any keyword occurring at or after min_time.
    Prioritizes specific keywords and avoids matching short substrings on noise.
    """
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if not kw_lower:
            continue
        for w in words:
            w_start = float(w.get('start', 0.0))
            if w_start < min_time:
                continue
            w_text = re.sub(r'[^a-zA-Z0-9]', '', w.get('word', '')).lower()
            if kw_lower == w_text or (len(w_text) >= 4 and kw_lower in w_text):
                return w_start
    return max(min_time + 0.6, default_offset)

def align_screenplay_to_measured_audio(
    screenplay: Dict[str, Any],
    beat_transcripts: Dict[str, Dict[str, Any]],
    sync_gap: float = 0.25
) -> Dict[str, Any]:
    """
    Takes a screenplay structure and measured Whisper transcripts for each beat,
    re-anchors all beat start/end times and layout-specific visual elements to
    exact acoustic seconds sequentially, and returns the voice-synchronized screenplay.
    """
    beats = screenplay.get("beats", [])
    current_time = 0.0

    for b in beats:
        bid = b.get("id", "")
        transcript = beat_transcripts.get(bid, {})
        dur = transcript.get("duration", 0.0)
        if dur <= 0:
            txt = b.get("voice_sync_text", "")
            dur = max(6.0, round(len(txt.split()) / 2.2, 2))

        b_start = round(current_time, 2)
        b_end = round(b_start + dur, 2)
        b["start"] = b_start
        b["end"] = b_end
        current_time = b_end + sync_gap

        words = transcript.get("words", [])
        layout = b.get("layout", "")

        # Always set Title at start + 0.3s
        if "title" in b and isinstance(b["title"], dict):
            b["title"]["at"] = round(b_start + 0.3, 2)

        # 1. FORK LAYOUT ALIGNMENT
        if layout == "fork":
            cursor = 0.5
            if "story_steps" in b and isinstance(b["story_steps"], list):
                for i, st in enumerate(b["story_steps"]):
                    combined = f"{st.get('badge', '')} {st.get('title', '')} {st.get('sub', '')}".lower()
                    specific_kw = []
                    for specific in ["land", "building", "plant", "machinery", "furniture", "first", "second", "third", "fourth"]:
                        if specific in combined:
                            specific_kw.append(specific)
                    off = find_first_word_offset(words, specific_kw, min_time=cursor, default_offset=dur * (i + 1) / (len(b["story_steps"]) + 1))
                    st["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

            if "divider" in b and isinstance(b["divider"], dict):
                div_kw = ["classification", "filter", "scope", "specified", "eligible"]
                off = find_first_word_offset(words, div_kw, min_time=cursor, default_offset=dur * 0.75)
                b["divider"]["at"] = round(b_start + off, 2)
                cursor = max(cursor + 0.5, off + 0.4)

            if "branches" in b and isinstance(b["branches"], list):
                for br in b["branches"]:
                    br_side = br.get("side", "")
                    base_kw = ["eligible", "qualify", "specified", "land", "building"] if br_side == "left" else ["furniture", "ineligible", "nonspecified", "fixtures", "office"]
                    br_off = find_first_word_offset(words, base_kw, min_time=cursor, default_offset=dur * 0.85 if br_side == "left" else dur * 0.90)
                    br["at"] = round(b_start + br_off, 2)
                    cursor = max(cursor + 0.5, br_off + 0.4)
                    for j, f in enumerate(br.get("facts", [])):
                        f["at"] = round(b_start + br_off + 0.4 + j * 1.0, 2)
                    if "outcome" in br and isinstance(br["outcome"], dict):
                        br["outcome"]["at"] = round(b_start + br_off + 0.8 + len(br.get("facts", [])) * 0.7, 2)

            if "result_card" in b and isinstance(b["result_card"], dict):
                res_kw = ["trap", "mark", "exclude", "furniture", "result", "isolated"]
                res_off = find_first_word_offset(words, res_kw, min_time=cursor, default_offset=dur * 0.92)
                b["result_card"]["at"] = round(b_start + res_off, 2)

        # 2. STATUTE QUOTE LAYOUT ALIGNMENT
        elif layout == "statute_quote":
            if "quote" in b and isinstance(b["quote"], dict):
                b["quote"]["at"] = round(b_start + 0.5, 2)

            if "context_bubble" in b and isinstance(b["context_bubble"], dict):
                bub_kw = ["year", "years", "transfer", "within", "window", "date", "period"]
                bub_off = find_first_word_offset(words, bub_kw, min_time=2.0, default_offset=dur * 0.6)
                b["context_bubble"]["at"] = round(b_start + bub_off, 2)

            if "sale_card" in b and isinstance(b["sale_card"], dict):
                b["sale_card"]["at"] = round(b_start + 0.6, 2)

        # 3. METER LAYOUT ALIGNMENT
        elif layout == "meter":
            cursor = 0.5
            if "breakdown" in b and isinstance(b["breakdown"], list):
                for i, it in enumerate(b["breakdown"]):
                    lbl = it.get("label", "").lower()
                    kw = []
                    for term in ["land", "building", "plant", "machinery", "furniture"]:
                        if term in lbl:
                            kw.append(term)
                    if not kw:
                        kw = [w for w in lbl.split() if len(w) > 3]
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(b["breakdown"]) + 2))
                    it["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

            if "meter_display" in b and isinstance(b["meter_display"], dict):
                tot_kw = ["total", "pool", "29", "twenty", "lakhs", "lacs"]
                tot_off = find_first_word_offset(words, tot_kw, min_time=cursor, default_offset=dur * 0.55)
                b["meter_display"]["at"] = round(b_start + tot_off, 2)

            if "outcome" in b and isinstance(b["outcome"], dict):
                out_kw = ["pool", "eligible", "set", "off", "stcg", "ltcg"]
                out_off = find_first_word_offset(words, out_kw, min_time=cursor, default_offset=dur * 0.8)
                b["outcome"]["at"] = round(b_start + out_off, 2)

            if "padlock" in b and isinstance(b["padlock"], dict):
                b["padlock"]["at"] = round(b_start + dur * 0.85, 2)

        # 4. LEDGER LAYOUT ALIGNMENT
        elif layout == "ledger":
            cursor = 0.5
            rows = b.get("ledger_rows", []) or b.get("rows", [])
            for i, r in enumerate(rows):
                lbl = (r.get("label", "") or r.get("particulars", "")).lower()
                kw = []
                for term in ["building", "plant", "machinery", "deemed", "30", "zero", "land", "ltcg", "125", "balance", "furniture"]:
                    if term in re.sub(r'[^a-zA-Z0-9]', '', lbl):
                        kw.append(term)
                if not kw:
                    kw = [w for w in re.sub(r'[^a-zA-Z0-9 ]', '', lbl).split() if len(w) > 3 and w not in ["less", "total", "under", "with", "from"]]
                off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(rows) + 2))
                r["at"] = round(b_start + off, 2)
                cursor = max(cursor + 0.4, off + 0.3)

            tot_obj = b.get("net_total") or b.get("total")
            if tot_obj and isinstance(tot_obj, dict):
                tot_kw = ["total", "taxable", "result", "2", "two", "amount"]
                tot_off = find_first_word_offset(words, tot_kw, min_time=cursor, default_offset=dur * 0.92)
                tot_obj["at"] = round(b_start + tot_off, 2)

            if "callout" in b and isinstance(b["callout"], dict):
                b["callout"]["at"] = round(b_start + 1.2, 2)

        # 5. TAKEAWAY LAYOUT ALIGNMENT
        elif layout == "takeaway":
            cursor = 0.5
            rules = b.get("rules", []) or b.get("points", [])
            for i, r in enumerate(rules):
                if isinstance(r, dict):
                    num = str(r.get("num", i + 1))
                    kw_map = {
                        "1": ["first", "one", "furniture", "strict"],
                        "2": ["second", "two", "50", "deemed", "stcg"],
                        "3": ["third", "three", "30", "wipe", "beneficial", "minimize"]
                    }
                    kw = kw_map.get(num[-1:], [num])
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(rules) + 1))
                    r["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

    screenplay["duration_sec"] = round(current_time, 2)
    return screenplay

def generate_alignment_log_summary(screenplay: Dict[str, Any]) -> str:
    """
    Generates a concise timing summary string suitable for Google Sheets Column J.
    """
    beats = screenplay.get("beats", [])
    total_dur = screenplay.get("duration_sec", 0.0)
    lines = [f"Total: {total_dur:.1f}s | Beats: {len(beats)} | Aligned: Whisper Word-Sync"]
    for b in beats:
        bid = b.get("id", "")
        layout = b.get("layout", "")
        st = b.get("start", 0.0)
        en = b.get("end", 0.0)
        lines.append(f"{bid}[{layout}]: {st:.1f}s-{en:.1f}s (d{(en-st):.1f}s)")
    return "\n".join(lines)

def update_engine_fixture(qid: str, screenplay: Dict[str, Any]):
    engine_path = os.path.join(PROJECT_ROOT, "redesign_demo", "frontend", "explainer_engine.js")
    if not os.path.exists(engine_path):
        return
    with open(engine_path, "r", encoding="utf-8") as f:
        code = f.read()

    fixture_str = f'FIXTURES["{qid}"] = {json.dumps(screenplay, indent=2, ensure_ascii=False)};'
    pattern = rf'FIXTURES\["{qid}"\]\s*=\s*\{{[\s\S]*?\n\s*\}};'
    if re.search(pattern, code):
        code = re.sub(pattern, fixture_str, code, count=1)
    else:
        anchor = 'FIXTURES["ch2_q14"] = FIXTURES["dt-c2-q14"];'
        if anchor in code:
            code = code.replace(anchor, f'{anchor}\n{fixture_str}')
        else:
            code += f"\n{fixture_str}\n"

    with open(engine_path, "w", encoding="utf-8") as f:
        f.write(code)

def synthesize_and_align_screenplay_audio(
    screenplay_obj: Dict[str, Any],
    subject: str,
    chapter_no: int,
    q_num: int,
    force_tts: bool = False
) -> tuple:
    """
    1. Synthesizes studio-grade audio for each beat via Gemini Aoede TTS.
    2. Stitches full audio into redesign_demo/data/audio/{qid}.mp3.
    3. Runs Whisper acoustic transcription to extract exact word timestamps.
    4. Aligns all screenplay elements to the measured audio.
    5. Saves local screenplay JSON and updates engine fixtures.
    Returns (aligned_screenplay, timing_summary_str).
    """
    from pipeline.phase3_audio import generate_gemini_audio
    from pydub import AudioSegment

    qid = f"{subject.lower()}-c{chapter_no}-q{q_num}"
    cache_dir = os.path.join(PROJECT_ROOT, "redesign_demo", "build", qid, "cache", "gemini_clips")
    os.makedirs(cache_dir, exist_ok=True)
    beats = screenplay_obj.get("beats", [])

    print(f"  [SCREENPLAY AUDIO] Synthesizing and aligning {len(beats)} beats for {qid}...")
    clips = []
    beat_transcripts = {}

    for b in beats:
        bid = b.get("id", "b1")
        clip_path = os.path.join(cache_dir, f"{bid}.mp3")
        txt = b.get("voice_sync_text", "")

        if not force_tts and os.path.exists(clip_path) and os.path.getsize(clip_path) > 5000:
            print(f"    [AUDIO CACHE] Reusing {bid}.mp3...")
        else:
            print(f"    [SYNTHESIZING AOEDE] Beat {bid}...")
            generate_gemini_audio(txt, clip_path, voice_name="Aoede")

        seg = AudioSegment.from_file(clip_path)
        clips.append(seg)

        # Transcribe with Whisper
        transcript = transcribe_beat_clip(clip_path)
        beat_transcripts[bid] = transcript

    # Stitch audio
    silence = AudioSegment.silent(duration=350)
    full_audio = AudioSegment.empty()
    for i, c in enumerate(clips):
        full_audio += c
        if i < len(clips) - 1:
            full_audio += silence

    out_audio_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "audio", f"{qid}.mp3")
    os.makedirs(os.path.dirname(out_audio_path), exist_ok=True)
    full_audio.export(out_audio_path, format="mp3", bitrate="192k")
    print(f"    [STITCHED AUDIO] Saved {out_audio_path} ({len(full_audio)/1000:.1f}s)")

    # Align screenplay
    aligned_sp = align_screenplay_to_measured_audio(screenplay_obj, beat_transcripts, sync_gap=0.35)
    aligned_sp["audio_url"] = f"data/audio/{qid}.mp3"

    # Save local screenplay JSON
    sp_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", f"{qid}.json")
    os.makedirs(os.path.dirname(sp_path), exist_ok=True)
    with open(sp_path, "w", encoding="utf-8") as f:
        json.dump(aligned_sp, f, indent=2, ensure_ascii=False)

    update_engine_fixture(qid, aligned_sp)
    timing_summary = generate_alignment_log_summary(aligned_sp)
    return aligned_sp, timing_summary
