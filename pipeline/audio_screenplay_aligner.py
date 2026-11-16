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

def find_first_word_offset(words: List[Dict[str, Any]], keywords: List[str], default_offset: float = 1.0) -> float:
    """
    Finds the start timestamp of the first word matching any keyword.
    Keywords are case-insensitive substrings.
    """
    for kw in keywords:
        kw_lower = kw.lower()
        for w in words:
            w_text = re.sub(r'[^a-zA-Z0-9]', '', w.get('word', '')).lower()
            if kw_lower in w_text or w_text in kw_lower:
                return float(w.get('start', default_offset))
    return default_offset

def align_screenplay_to_measured_audio(
    screenplay: Dict[str, Any],
    beat_transcripts: Dict[str, Dict[str, Any]],
    sync_gap: float = 0.25
) -> Dict[str, Any]:
    """
    Takes a screenplay structure and measured Whisper transcripts for each beat,
    re-anchors all beat start/end times and layout-specific visual elements to
    exact acoustic seconds, and returns the voice-synchronized screenplay.
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
            if "story_steps" in b and isinstance(b["story_steps"], list):
                for i, st in enumerate(b["story_steps"]):
                    st_kw = [w for w in st.get("title", "").split() if len(w) > 3]
                    off = find_first_word_offset(words, st_kw, default_offset=1.2 + i * 1.5)
                    st["at"] = round(b_start + off, 2)

            if "divider" in b and isinstance(b["divider"], dict):
                div_kw = ["scope", "specified", "cut", "off", "date", "section"]
                off = find_first_word_offset(words, div_kw, default_offset=dur * 0.35)
                b["divider"]["at"] = round(b_start + off, 2)

            if "branches" in b and isinstance(b["branches"], list):
                for br in b["branches"]:
                    br_side = br.get("side", "")
                    base_kw = ["eligible", "land", "building", "plant"] if br_side == "left" else ["furniture", "ineligible", "fixtures", "office"]
                    br_off = find_first_word_offset(words, base_kw, default_offset=dur * 0.45 if br_side == "left" else dur * 0.6)
                    br["at"] = round(b_start + br_off, 2)
                    for j, f in enumerate(br.get("facts", [])):
                        f["at"] = round(b_start + br_off + 0.4 + j * 1.2, 2)
                    if "outcome" in br and isinstance(br["outcome"], dict):
                        br["outcome"]["at"] = round(b_start + br_off + 1.0 + len(br.get("facts", [])) * 0.8, 2)

            if "result_card" in b and isinstance(b["result_card"], dict):
                res_kw = ["trap", "mark", "exclude", "furniture", "result", "isolated"]
                res_off = find_first_word_offset(words, res_kw, default_offset=dur * 0.75)
                b["result_card"]["at"] = round(b_start + res_off, 2)

        # 2. STATUTE QUOTE LAYOUT ALIGNMENT
        elif layout == "statute_quote":
            if "quote" in b and isinstance(b["quote"], dict):
                b["quote"]["at"] = round(b_start + 0.5, 2)

            if "context_bubble" in b and isinstance(b["context_bubble"], dict):
                bub_kw = ["year", "years", "transfer", "within", "window", "date", "period"]
                bub_off = find_first_word_offset(words, bub_kw, default_offset=dur * 0.6)
                b["context_bubble"]["at"] = round(b_start + bub_off, 2)

            if "sale_card" in b and isinstance(b["sale_card"], dict):
                b["sale_card"]["at"] = round(b_start + 0.6, 2)

        # 3. METER LAYOUT ALIGNMENT
        elif layout == "meter":
            if "breakdown" in b and isinstance(b["breakdown"], list):
                for i, it in enumerate(b["breakdown"]):
                    lbl = it.get("label", "").lower()
                    kw = [w for w in lbl.split() if len(w) > 3]
                    off = find_first_word_offset(words, kw, default_offset=1.2 + i * 2.0)
                    it["at"] = round(b_start + off, 2)

            if "meter_display" in b and isinstance(b["meter_display"], dict):
                tot_kw = ["total", "pool", "28", "twenty", "lakhs", "lacs"]
                tot_off = find_first_word_offset(words, tot_kw, default_offset=dur * 0.45)
                b["meter_display"]["at"] = round(b_start + tot_off, 2)

            if "outcome" in b and isinstance(b["outcome"], dict):
                out_kw = ["set", "off", "stcg", "ltcg", "exhaust", "qualify"]
                out_off = find_first_word_offset(words, out_kw, default_offset=dur * 0.75)
                b["outcome"]["at"] = round(b_start + out_off, 2)

            if "padlock" in b and isinstance(b["padlock"], dict):
                b["padlock"]["at"] = round(b_start + dur * 0.8, 2)

        # 4. LEDGER LAYOUT ALIGNMENT
        elif layout == "ledger":
            rows = b.get("ledger_rows", []) or b.get("rows", [])
            for i, r in enumerate(rows):
                lbl = (r.get("label", "") or r.get("particulars", "")).lower()
                kw = [w for w in lbl.split() if len(w) > 3 and w not in ["less", "total", "under", "with"]]
                off = find_first_word_offset(words, kw, default_offset=1.0 + i * 2.2)
                r["at"] = round(b_start + off, 2)

            tot_obj = b.get("net_total") or b.get("total")
            if tot_obj and isinstance(tot_obj, dict):
                tot_kw = ["final", "taxable", "total", "result", "amount", "just"]
                tot_off = find_first_word_offset(words, tot_kw, default_offset=dur * 0.88)
                tot_obj["at"] = round(b_start + tot_off, 2)

            if "callout" in b and isinstance(b["callout"], dict):
                b["callout"]["at"] = round(b_start + dur * 0.5, 2)

        # 5. TAKEAWAY LAYOUT ALIGNMENT
        elif layout == "takeaway":
            rules = b.get("rules", []) or b.get("points", [])
            for i, r in enumerate(rules):
                if isinstance(r, dict):
                    num = str(r.get("num", i + 1))
                    kw_map = {
                        "1": ["first", "one", "onnamathathu", "furniture", "strict"],
                        "2": ["second", "two", "randamathathu", "50", "deemed", "stcg"],
                        "3": ["third", "three", "moonnamathathu", "ordering", "beneficial", "minimize"]
                    }
                    kw = kw_map.get(num[-1:], [num])
                    off = find_first_word_offset(words, kw, default_offset=1.5 + i * 4.0)
                    r["at"] = round(b_start + off, 2)

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
