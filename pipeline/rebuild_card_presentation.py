"""Build fresh, line-synchronized voice and card assets from scripts_v2."""

import json
import os
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCRIPTS = DATA / "scripts_v2"
STAGE_AUDIO = DATA / "audio_rebuild"
STAGE_TEMP = DATA / "audio_temp_rebuild"
STAGE_STORYBOARDS = DATA / "ppt_storyboards_rebuild.json"
STAGE_PROVISIONS = DATA / "provisions_rebuild.json"
STAGE_TIMINGS = DATA / "measured_sentence_timings_rebuild.json"

SAMPLE_RATE = 24_000
SAMPLE_WIDTH = 2
GAP_SECONDS = 0.25
VOICE = "Google Text-to-Speech (Malayalam)"

def update_current_figures(provisions):
    for item in provisions:
        qn = item["question_number"]
        md = item.get("provision_presentation_markdown", "")
        if qn == 6:
            md = md.replace(
                "Rebate u/s 87A: Available up to ₹ 25,000 if Total Income does not exceed ₹ 7,00,000.",
                "Rebate u/s 87A: For a resident individual, the rebate is the lower of income-tax payable or ₹ 60,000 when Total Income does not exceed ₹ 12,00,000 (A.Y. 2026-27).",
            )
            item["provision_presentation_markdown"] = md
        elif qn == 8:
            item["provision_presentation_markdown"] = """### Default regime slabs and Section 87A relief

**A.Y. 2026–27 · Resident individuals**

| Total income | Tax rate |
|:--|--:|
| Up to ₹4,00,000 | Nil |
| ₹4,00,001–₹8,00,000 | 5% |
| ₹8,00,001–₹12,00,000 | 10% |
| ₹12,00,001–₹16,00,000 | 15% |
| ₹16,00,001–₹20,00,000 | 20% |
| ₹20,00,001–₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

**Section 87A:** For an eligible resident individual, rebate is limited to tax payable or ₹60,000, whichever is lower, where total income does not exceed ₹12,00,000.

**Marginal relief:** When total income is just above ₹12,00,000, tax before cess is limited to the amount by which total income exceeds ₹12,00,000. Add 4% health and education cess after relief.
"""

    # Topic ids must be unique so each question gets its own voice and card sequence.
    for item in provisions:
        qn = item["question_number"]
        item["topic_id"] = f"presentation_q{qn}"
        item["audio_file"] = f"q{qn}.mp3"
        item.pop("video_file", None)
        item["voice_engine"] = VOICE
        item["voice"] = VOICE
    return provisions


def make_card_slide(qn, item, index, count, t0, t1):
    card = item.get("card", {})
    block_name = item.get("block_name", f"Point {index}")
    return {
        "slide_number": index,
        "slide_title": card.get("title") or f"Key point {index}",
        "section_badge": block_name,
        "t0": round(t0, 3),
        "t1": round(t1, 3),
        "duration": round(t1 - t0, 3),
        "malayalam_narration": item.get("narration_ml", "").strip(),
        "cards": [{
            "title": card.get("title") or f"Key point {index}",
            "badge": block_name,
            "bullets": card.get("lines", []),
            "table": card.get("table"),
            "highlights": card.get("highlights", []),
            "is_highlight": True,
        }],
    }


def main():
    for staged in (STAGE_AUDIO, STAGE_TEMP):
        if staged.exists():
            shutil.rmtree(staged)
    STAGE_AUDIO.mkdir(parents=True, exist_ok=True)
    STAGE_TEMP.mkdir(parents=True, exist_ok=True)
    provisions = json.loads((DATA / "provisions.json").read_text(encoding="utf-8"))
    q_to_provision = {p["question_number"]: p for p in provisions}
    provisions = update_current_figures(provisions)
    boards = {}
    timing_data = {}
    silence = b"\x00" * int(SAMPLE_RATE * SAMPLE_WIDTH * GAP_SECONDS)

    for qn in range(1, 11):
        script_path = SCRIPTS / f"q{qn}.json"
        lines = json.loads(script_path.read_text(encoding="utf-8"))
        if not lines:
            raise RuntimeError(f"No narration cards in {script_path}")

        out_wav = STAGE_TEMP / f"q{qn}_joined.wav"
        out_mp3 = STAGE_AUDIO / f"q{qn}.mp3"
        slides = []
        beats = []
        cursor = 0.0
        print(f"\nQ{qn}: generating {len(lines)} narration cards with {VOICE}", flush=True)

        with wave.open(str(out_wav), "wb") as wav_out:
            wav_out.setnchannels(1)
            wav_out.setsampwidth(SAMPLE_WIDTH)
            wav_out.setframerate(SAMPLE_RATE)

            for idx, line in enumerate(lines, 1):
                narration = line.get("narration_ml", "").strip()
                if not narration:
                    raise RuntimeError(f"Q{qn} card {idx} has no narration")
                from pipeline.synthesize_discrete_points import synthesize_point_audio
                clip_mp3 = STAGE_TEMP / f"q{qn}_card_{idx:02d}.mp3"
                clip_raw = STAGE_TEMP / f"q{qn}_card_{idx:02d}.raw"
                synthesize_point_audio(narration, str(clip_mp3))
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(clip_mp3), "-ar", str(SAMPLE_RATE),
                    "-ac", "1", "-f", "s16le", str(clip_raw)
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                pcm = clip_raw.read_bytes()
                clip_mp3.unlink(missing_ok=True)
                clip_raw.unlink(missing_ok=True)
                duration = len(pcm) / (SAMPLE_RATE * SAMPLE_WIDTH)
                t0 = cursor
                spoken_end = t0 + duration
                card_end = spoken_end + (GAP_SECONDS if idx < len(lines) else 0)
                slides.append(make_card_slide(qn, line, idx, len(lines), t0, card_end))
                beats.append({
                    "card_number": idx,
                    "line_id": line.get("id", f"L{idx:02d}"),
                    "text": narration,
                    "t0": round(t0, 3),
                    "spoken_t1": round(spoken_end, 3),
                    "card_t1": round(card_end, 3),
                    "duration": round(duration, 3),
                })
                wav_out.writeframes(pcm)
                if idx < len(lines):
                    wav_out.writeframes(silence)
                cursor = card_end
                print(f"  Card {idx}/{len(lines)}: {duration:.2f}s", flush=True)
                time.sleep(0.2)

        subprocess.run([
            "ffmpeg", "-y", "-i", str(out_wav), "-ac", "1", "-ar", str(SAMPLE_RATE),
            "-b:a", "128k", str(out_mp3)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        boards[f"q{qn}"] = {
            "question_number": qn,
            "voice": VOICE,
            "total_duration": round(cursor, 3),
            "slides": slides,
        }
        timing_data[f"q{qn}"] = {
            "topic": f"q{qn}",
            "audio_file": f"q{qn}.mp3",
            "voice": VOICE,
            "total_duration": round(cursor, 3),
            "beats": beats,
        }

        prov = q_to_provision[qn]
        prov["dur"] = round(cursor, 3)
        prov["duration_seconds"] = round(cursor, 3)
        prov["malayalam_audio_script"] = "\n".join(b["text"] for b in beats)

    STAGE_STORYBOARDS.write_text(json.dumps(boards, ensure_ascii=False, indent=2), encoding="utf-8")
    STAGE_PROVISIONS.write_text(json.dumps(provisions, ensure_ascii=False, indent=2), encoding="utf-8")
    STAGE_TIMINGS.write_text(json.dumps(timing_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nFresh audio and card decks are staged for activation.", flush=True)


if __name__ == "__main__":
    main()
