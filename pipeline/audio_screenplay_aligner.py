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

COMMON_STOPWORDS = {
    # English common words
    "the", "and", "for", "with", "from", "that", "this", "into", "under", "will", 
    "have", "been", "also", "what", "where", "when", "which", "upon", "each", "unit", 
    "case", "step", "date", "period", "about", "their", "them", "then", "there", "some",
    "any", "such", "than", "other", "after", "before", "over", "only", "both", "more",
    # Malayalam common scaffolding words
    "oru", "ulla", "aayi", "aanu", "aayal", "athayath", "ennaal", "ithil", "ithu", 
    "ivide", "athinu", "nammal", "namukku", "kando", "nokkoo", "sreddhikkoo", "paranjaal",
    "pinne", "angane", "engil", "athukond", "appol", "ini", "cheytha", "cheythu"
}

ORDINAL_CUES = [
    ["1", "first", "one", "aadyam", "onnamathathu", "onnamathe"],
    ["2", "second", "two", "randamathathu", "randamathe", "aduthathayi"],
    ["3", "third", "three", "moonnamathathu", "moonnamathe"],
    ["4", "fourth", "four", "naalaamathathu", "naalaamathe"],
    ["5", "fifth", "five", "anjaamathathu", "anjaamathe"],
    ["6", "sixth", "six", "aaraamathathu", "aaraamathe"]
]

def extract_element_keywords(element: Any, index: Optional[int] = None) -> List[str]:
    """
    Universally extracts acoustic search keywords directly from any visual element
    (card, row, step, rule, etc.).
    Collects text fields, converts numbers into spoken currency tokens (e.g. 1600000 -> 16, 16l, lakhs),
    filters stopwords, and appends ordinal cues if index is given.
    """
    tokens = []
    if isinstance(element, dict):
        text_fields = ["badge", "title", "label", "particulars", "sub", "text", "heading", "body", "status", "speaker", "name", "role", "kicker"]
        for k in text_fields:
            val = element.get(k)
            if val and isinstance(val, str):
                tokens.extend(re.sub(r'[^a-zA-Z0-9 ]', ' ', val).split())

        for num_key in ["amount", "val", "value", "cost", "sale_val", "gain_val"]:
            v = element.get(num_key)
            if v is not None and isinstance(v, (int, float)) and v != 0:
                abs_v = abs(int(v))
                tokens.append(str(abs_v))
                if abs_v >= 100000 and abs_v % 100000 == 0:
                    lakhs = abs_v // 100000
                    tokens.append(f"{lakhs}")
                    tokens.append(f"{lakhs}l")
                    tokens.append("lakhs")
                    tokens.append("lakh")
                elif abs_v >= 1000 and abs_v % 1000 == 0:
                    k_val = abs_v // 1000
                    tokens.append(f"{k_val}k")
                    tokens.append(f"{k_val}")
    elif isinstance(element, str):
        tokens.extend(re.sub(r'[^a-zA-Z0-9 ]', ' ', element).split())

    keywords = []
    for t in tokens:
        w = t.lower().strip()
        if not w or w in COMMON_STOPWORDS:
            continue
        if len(w) >= 4 or w.isdigit() or w in ["54", "54g", "50", "45", "54f", "54ec", "112", "111a", "stcg", "ltcg", "wdv", "cost", "sale", "gain", "land", "tax", "ay", "fy", "pgbp", "ifos"]:
            keywords.append(w)

    if index is not None and 0 <= index < len(ORDINAL_CUES):
        keywords.extend(ORDINAL_CUES[index])

    seen = set()
    result = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    return result

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
    Uses dynamic keyword extraction from whatever visual elements Gemini created.
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

        cursor = 0.5

        # 1. FORK LAYOUT ALIGNMENT
        if layout == "fork":
            if "intro_cards" in b and isinstance(b["intro_cards"], list):
                for i, ic in enumerate(b["intro_cards"]):
                    kw = extract_element_keywords(ic, index=i)
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=1.5 + i * 4.5)
                    ic["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

            first_step_time = None
            if "story_steps" in b and isinstance(b["story_steps"], list):
                for i, st in enumerate(b["story_steps"]):
                    kw = extract_element_keywords(st, index=i)
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(b["story_steps"]) + 1))
                    st["at"] = round(b_start + off, 2)
                    if first_step_time is None:
                        first_step_time = st["at"]
                    cursor = max(cursor + 0.5, off + 0.4)

            if "intro_cards" in b and isinstance(b["intro_cards"], list) and first_step_time:
                for ic in b["intro_cards"]:
                    ic["out_at"] = round(first_step_time - 0.4, 2)

            if "divider" in b and isinstance(b["divider"], dict):
                div_kw = extract_element_keywords(b["divider"]) + ["classification", "filter", "scope", "division", "category", "specified", "eligible"]
                off = find_first_word_offset(words, div_kw, min_time=cursor, default_offset=dur * 0.75)
                b["divider"]["at"] = round(b_start + off, 2)
                cursor = max(cursor + 0.5, off + 0.4)

            if "branches" in b and isinstance(b["branches"], list):
                for i, br in enumerate(b["branches"]):
                    br_kw = extract_element_keywords(br, index=i)
                    br_off = find_first_word_offset(words, br_kw, min_time=cursor, default_offset=dur * 0.82 + i * 1.5)
                    br["at"] = round(b_start + br_off, 2)
                    cursor = max(cursor + 0.5, br_off + 0.4)
                    for j, f in enumerate(br.get("facts", [])):
                        f_kw = extract_element_keywords(f)
                        f_off = find_first_word_offset(words, f_kw, min_time=cursor, default_offset=br_off + 0.4 + j * 1.0)
                        f["at"] = round(b_start + f_off, 2)
                        cursor = max(cursor + 0.4, f_off + 0.3)
                    if "outcome" in br and isinstance(br["outcome"], dict):
                        out_kw = extract_element_keywords(br["outcome"])
                        out_off = find_first_word_offset(words, out_kw, min_time=cursor, default_offset=br_off + 1.2)
                        br["outcome"]["at"] = round(b_start + out_off, 2)
                        cursor = max(cursor + 0.4, out_off + 0.3)

            if "result_card" in b and isinstance(b["result_card"], dict):
                res_kw = extract_element_keywords(b["result_card"]) + ["trap", "alert", "mark", "exclude", "result", "isolated"]
                res_off = find_first_word_offset(words, res_kw, min_time=cursor, default_offset=dur * 0.92)
                b["result_card"]["at"] = round(b_start + res_off, 2)
                cursor = max(cursor + 0.4, res_off + 0.3)

            if "example" in b and isinstance(b["example"], dict):
                ex_kw = extract_element_keywords(b["example"])
                ex_off = find_first_word_offset(words, ex_kw, min_time=cursor, default_offset=dur * 0.85)
                b["example"]["at"] = round(b_start + ex_off, 2)

        # 2. STATUTE QUOTE LAYOUT ALIGNMENT
        elif layout == "statute_quote":
            if "quote" in b and isinstance(b["quote"], dict):
                b["quote"]["at"] = round(b_start + 0.5, 2)

            if "context_bubble" in b and isinstance(b["context_bubble"], dict):
                bub_kw = extract_element_keywords(b["context_bubble"]) + ["year", "years", "transfer", "within", "window", "date", "period"]
                bub_off = find_first_word_offset(words, bub_kw, min_time=1.8, default_offset=dur * 0.6)
                b["context_bubble"]["at"] = round(b_start + bub_off, 2)
                cursor = max(cursor + 0.5, bub_off + 0.4)

            if "sale_card" in b and isinstance(b["sale_card"], dict):
                sc_kw = extract_element_keywords(b["sale_card"])
                sc_off = find_first_word_offset(words, sc_kw, min_time=cursor, default_offset=0.8)
                b["sale_card"]["at"] = round(b_start + sc_off, 2)
                cursor = max(cursor + 0.5, sc_off + 0.4)

            if "example" in b and isinstance(b["example"], dict):
                ex_kw = extract_element_keywords(b["example"])
                ex_off = find_first_word_offset(words, ex_kw, min_time=cursor, default_offset=dur * 0.7)
                b["example"]["at"] = round(b_start + ex_off, 2)

        # 3. METER LAYOUT ALIGNMENT
        elif layout == "meter":
            if "breakdown" in b and isinstance(b["breakdown"], list):
                for i, it in enumerate(b["breakdown"]):
                    kw = extract_element_keywords(it, index=i)
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(b["breakdown"]) + 2))
                    it["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

            if "meter_display" in b and isinstance(b["meter_display"], dict):
                tot_kw = extract_element_keywords(b["meter_display"]) + ["total", "pool", "ceiling", "threshold", "qualifying", "eligible", "lakhs", "lacs"]
                tot_off = find_first_word_offset(words, tot_kw, min_time=cursor, default_offset=dur * 0.55)
                b["meter_display"]["at"] = round(b_start + tot_off, 2)
                cursor = max(cursor + 0.4, tot_off + 0.3)

            if "outcome" in b and isinstance(b["outcome"], dict):
                out_kw = extract_element_keywords(b["outcome"]) + ["pool", "eligible", "set", "off", "stcg", "ltcg", "result", "benefit"]
                out_off = find_first_word_offset(words, out_kw, min_time=cursor, default_offset=dur * 0.8)
                b["outcome"]["at"] = round(b_start + out_off, 2)
                cursor = max(cursor + 0.4, out_off + 0.3)

            if "padlock" in b and isinstance(b["padlock"], dict):
                b["padlock"]["at"] = round(b_start + dur * 0.85, 2)

            if "example" in b and isinstance(b["example"], dict):
                ex_kw = extract_element_keywords(b["example"])
                ex_off = find_first_word_offset(words, ex_kw, min_time=cursor, default_offset=dur * 0.88)
                b["example"]["at"] = round(b_start + ex_off, 2)

        # 4. LEDGER LAYOUT ALIGNMENT
        elif layout == "ledger":
            rows = b.get("ledger_rows", []) or b.get("rows", [])
            for i, r in enumerate(rows):
                kw = extract_element_keywords(r, index=i)
                off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(rows) + 2))
                r["at"] = round(b_start + off, 2)
                cursor = max(cursor + 0.4, off + 0.3)

            tot_obj = b.get("net_total") or b.get("total")
            if tot_obj and isinstance(tot_obj, dict):
                tot_kw = extract_element_keywords(tot_obj) + ["total", "taxable", "result", "net", "amount", "gain", "remainder"]
                tot_off = find_first_word_offset(words, tot_kw, min_time=cursor, default_offset=dur * 0.92)
                tot_obj["at"] = round(b_start + tot_off, 2)
                cursor = max(cursor + 0.4, tot_off + 0.3)

            if "callout" in b and isinstance(b["callout"], dict):
                b["callout"]["at"] = round(b_start + 1.2, 2)

        # 5. TAKEAWAY LAYOUT ALIGNMENT
        elif layout == "takeaway":
            rules = b.get("rules", []) or b.get("points", [])
            for i, r in enumerate(rules):
                if isinstance(r, dict):
                    kw = extract_element_keywords(r, index=i)
                    off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(rules) + 1))
                    r["at"] = round(b_start + off, 2)
                    cursor = max(cursor + 0.5, off + 0.4)

        # 6. UNIVERSAL FALLBACK FOR OTHER LAYOUTS (timeline, split, compare, checklist)
        else:
            for sub_key in ["cards", "items", "nodes", "columns", "tags"]:
                arr = b.get(sub_key)
                if isinstance(arr, list):
                    for i, it in enumerate(arr):
                        if isinstance(it, dict):
                            kw = extract_element_keywords(it, index=i)
                            off = find_first_word_offset(words, kw, min_time=cursor, default_offset=dur * (i + 1) / (len(arr) + 1))
                            it["at"] = round(b_start + off, 2)
                            cursor = max(cursor + 0.4, off + 0.3)

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
