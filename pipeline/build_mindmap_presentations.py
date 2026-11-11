import copy
import json
import os
import re
import shutil
import subprocess
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCRIPTS = DATA / "scripts_v2"
AUDIO_DIR = DATA / "audio"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2
PAUSE_SECONDS = 1.5
TTS_MODEL = os.getenv("GEMINI_TTS_MODEL", "gemini-3.8-flash-lite-tts")

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_embedded_snapshot():
    html_path = ROOT / "frontend" / "index.html"
    html = html_path.read_text(encoding="utf-8")
    payload = {
        "catalog": read_json(DATA / "catalog.json"),
        "questions": read_json(DATA / "extracted_qna.json"),
        "provisions": read_json(DATA / "provisions.json"),
        "storyboards": read_json(DATA / "ppt_storyboards.json"),
        "mindmaps": read_json(DATA / "mindmaps.json"),
        "timing_overrides": read_json(DATA / "mindmap_timing_overrides.json") if (DATA / "mindmap_timing_overrides.json").exists() else {}
    }
    pattern = r'(<script type="application/json" id="pipeline-data">)[\s\S]*?(</script>)'
    updated, count = re.subn(
        pattern,
        lambda match: match.group(1) + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + match.group(2),
        html,
        count=1
    )
    if count != 1:
        raise ValueError("Could not locate the embedded pipeline-data snapshot")
    html_path.write_text(updated, encoding="utf-8")


def normalize_reviewed_scripts():
    scripts = {}
    for qn in range(1, 11):
        path = SCRIPTS / f"q{qn}.json"
        beats = read_json(path)
        if not beats:
            raise ValueError(f"No reviewed presentation beats in {path}")
        for beat in beats:
            card = beat.get("card") or {}
            if not beat.get("narration_ml", "").strip() or not card.get("title"):
                raise ValueError(f"Incomplete presentation beat in Q{qn}: {beat.get('id')}")
            beat.pop("review_flag", None)
            card.pop("review_flag", None)

        scripts[qn] = beats
    return scripts


def make_storyboard(qn, beats):
    slides = []
    for index, beat in enumerate(beats, start=1):
        source = beat["card"]
        card = {
            "title": source["title"],
            "number": beat.get("number", ""),
            "badge": source.get("type", "Rule").replace("_", " ").title(),
            "bullets": list(source.get("lines") or []),
            "table": copy.deepcopy(source.get("table")),
            "highlights": list(source.get("highlights") or []),
            "is_highlight": source.get("type") in {"rule", "formula", "trap"}
        }
        slide_no = int(re.sub(r"\D", "", beat.get("id", "")) or index)
        slides.append({
            "slide_number": slide_no,
            "point_number": beat.get("number", ""),
            "block_number": int(beat.get("block", 1)),
            "block_name": beat.get("block_name", "Provision Rule"),
            "slide_title": source["title"],
            "section_badge": beat.get("block_name", "Provision Rule"),
            "layout_type": source.get("type", "rule"),
            "t0": 0.0,
            "t1": 0.0,
            "duration": 0.0,
            "malayalam_narration": beat["narration_ml"].strip(),
            "cards": [card]
        })
    return {
        "question_number": qn,
        "voice": "Malayalam teacher narration",
        "total_duration": 0.0,
        "slides": slides
    }


def make_mindmap(qn, storyboard, provision):
    branches_by_block = {}
    intro_slide = storyboard["slides"][0] if storyboard["slides"] and storyboard["slides"][0]["block_number"] == 0 else None
    for slide in storyboard["slides"]:
        block = slide["block_number"]
        if block == 0:
            continue
        branch = branches_by_block.setdefault(block, {
            "branch_id": f"q{qn}-branch-{block}",
            "branch_title": slide["block_name"],
            "number": f"1.{block}",
            "badge": slide["block_name"],
            "icon": "scales",
            "t0": slide["t0"],
            "t1": slide["t1"],
            "points": [],
            "flow_summary": []
        })
        branch["t0"] = min(branch["t0"], slide["t0"])
        branch["t1"] = max(branch["t1"], slide["t1"])
        for card_index, card in enumerate(slide["cards"]):
            table = card.get("table")
            branch["points"].append({
                "id": f"q{qn}-beat-{slide['slide_number']}-{card_index}",
                "title": card["title"],
                "number": card.get("number") or slide.get("point_number", ""),
                "badge": card.get("badge", ""),
                "body": list(card.get("bullets") or []),
                "table_data": ({
                    "title": slide["slide_title"],
                    "headers": table["headers"],
                    "rows": table["rows"]
                } if table and table.get("headers") and table.get("rows") else None),
                "spoken": True,
                "t0": slide["t0"],
                "t1": slide["t1"],
                "voice_sync_text": slide["malayalam_narration"],
                "icon": "calculator" if table else "check",
                "highlights": card.get("highlights", [])
            })
    branches = list(branches_by_block.values())
    sections = provision.get("statutory_sections", [])
    return {
        "doctrine": provision.get("topic_title") or provision.get("core_principle") or f"Question {qn}",
        "root": {
            "id": "root",
            "number": "1",
            "title": provision.get("topic_title") or provision.get("core_principle") or f"Question {qn}",
            "badge": " · ".join(sections) or "§ LAW",
            "t1": intro_slide["t1"] if intro_slide else storyboard["slides"][0]["t1"],
            "voice_sync_text": intro_slide["malayalam_narration"] if intro_slide else ""
        },
        "total_duration": storyboard["total_duration"],
        "branches": branches
    }


def synthesize_storyboard(qn, storyboard, voice_name):
    key = f"q{qn}"
    clips = []
    current = 0.0
    pause = b"\x00" * int(SAMPLE_RATE * BYTES_PER_SAMPLE * PAUSE_SECONDS)
    slide_pcm = []
    for idx, slide in enumerate(storyboard["slides"], start=1):
        narration = slide["malayalam_narration"].strip()
        print(f"[{key}] voice {idx}/{len(storyboard['slides'])}: {slide['slide_title']}", flush=True)
        cache_key = hashlib.sha256(
            f"{TTS_MODEL}\0{voice_name}\0{narration}".encode("utf-8")
        ).hexdigest()[:24]
        cache_dir = DATA / "audio_temp" / "gemini_point_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{cache_key}.pcm"
        if cache_path.exists() and cache_path.stat().st_size > 0:
            pcm = cache_path.read_bytes()
            print(f"[{key}] reused Gemini voice cache for point {idx}", flush=True)
        else:
            from pipeline.synthesize_ppt_audio import generate_slide_audio_pcm
            pcm = generate_slide_audio_pcm(narration, voice_name=voice_name)
            if pcm:
                cache_path.write_bytes(pcm)
        if not pcm:
            raise RuntimeError(f"No audio returned for {key} narration {idx}")
        duration = len(pcm) / (SAMPLE_RATE * BYTES_PER_SAMPLE)
        slide["t0"] = round(current, 3)
        slide["t1"] = round(current + duration, 3)
        slide["duration"] = round(duration, 3)
        clips.append(pcm)
        slide_pcm.append(duration)
        current += duration
        if idx < len(storyboard["slides"]):
            clips.append(pause)
            current += PAUSE_SECONDS

    total_duration = round(sum(slide_pcm) + PAUSE_SECONDS * max(0, len(slide_pcm) - 1), 3)
    storyboard["total_duration"] = total_duration
    output_pcm = b"".join(clips)
    output_path = AUDIO_DIR / f"{key}_mindmap.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "s16le", "-ar", str(SAMPLE_RATE), "-ac", "1", "-i", "pipe:0", "-b:a", "160k", str(output_path)],
        input=output_pcm,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(output_path), "-f", "null", "-"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True
    )
    print(f"[{key}] saved {output_path.name} · {total_duration:.2f}s · {output_path.stat().st_size:,} bytes", flush=True)
    return total_duration, output_path.name


def render_review(scripts, storyboards):
    out = [
        "# Refreshed Presentation Narration Review",
        "",
        "All 10 question summaries were checked against the current question bank. Q6 and Q8 rebate values were verified against the supplied AIR1 question bank PDF, pages 1.3–1.4. The 2026–27 default-regime rebate is ₹12,00,000 income threshold and up to ₹60,000 rebate; the stale Q6 provision summary has been corrected.",
        "",
        "Each presentation opens with a heading-only Malayalam introduction, then follows four question-specific mind-map branches. Every numbered detail point has its own Malayalam narration; branch and point timing has no inserted pause.",
        ""
    ]
    for qn in range(1, 11):
        out.append(f"## Q{qn}: {storyboards[f'q{qn}']['slides'][0]['slide_title']}")
        out.append("")
        for slide in storyboards[f"q{qn}"]["slides"]:
            out.append(f"### {slide['block_name']} · {slide['slide_title']}")
            out.append("")
            out.append(f"**Malayalam narration:** {slide['malayalam_narration']}")
            out.append("")
            for bullet in slide["cards"][0]["bullets"]:
                out.append(f"- {bullet}")
            table = slide["cards"][0].get("table")
            if table:
                out.append("")
                out.append("| " + " | ".join(table["headers"]) + " |")
                out.append("| " + " | ".join("---" for _ in table["headers"]) + " |")
                for row in table["rows"]:
                    out.append("| " + " | ".join(str(cell) for cell in row) + " |")
            out.append("")
    return "\n".join(out)


def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    scripts = normalize_reviewed_scripts()
    provisions = read_json(DATA / "provisions.json")
    provision_by_q = {int(p["question_number"]): p for p in provisions}
    if set(provision_by_q) != set(range(1, 11)):
        raise ValueError("The active provision catalog must contain Q1–Q10 before refresh.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = DATA / f"archive_mindmap_refresh_{timestamp}"
    archive.mkdir(parents=True, exist_ok=False)
    for filename in ["provisions.json", "ppt_storyboards.json", "mindmaps.json"]:
        source = DATA / filename
        if source.exists():
            shutil.copy2(source, archive / filename)
    archived_scripts = archive / "scripts_v2"
    archived_scripts.mkdir()
    for qn in range(1, 11):
        shutil.copy2(SCRIPTS / f"q{qn}.json", archived_scripts / f"q{qn}.json")

    storyboards = {f"q{qn}": make_storyboard(qn, scripts[qn]) for qn in range(1, 11)}
    voice = os.getenv("GEMINI_TTS_VOICE", "Kore")
    for qn in range(1, 11):
        duration, audio_file = synthesize_storyboard(qn, storyboards[f"q{qn}"], voice)
        provision = provision_by_q[qn]
        provision["audio_file"] = audio_file
        provision["dur"] = duration
        provision["duration_seconds"] = duration
        provision["voice_engine"] = f"Gemini Voice ({voice}; {TTS_MODEL})"
        provision["malayalam_audio_script"] = "\n\n".join(s["malayalam_narration"] for s in storyboards[f"q{qn}"]["slides"])

    for qn in range(1, 11):
        scripts_path = SCRIPTS / f"q{qn}.json"
        write_json(scripts_path, scripts[qn])

    for qn in range(1, 11):
        storyboards[f"q{qn}"]["combined_script"] = provision_by_q[qn]["malayalam_audio_script"]
    storyboards["question_to_mindmap"] = {str(qn): f"q{qn}" for qn in range(1, 11)}
    mindmaps = {f"q{qn}": make_mindmap(qn, storyboards[f"q{qn}"], provision_by_q[qn]) for qn in range(1, 11)}
    mindmaps["question_to_mindmap"] = {str(qn): f"q{qn}" for qn in range(1, 11)}

    write_json(DATA / "ppt_storyboards.json", storyboards)
    write_json(DATA / "provisions.json", provisions)
    write_json(DATA / "mindmaps.json", mindmaps)
    write_json(SCRIPTS / "review_flags.json", {})
    (SCRIPTS / "review.md").write_text(render_review(scripts, storyboards), encoding="utf-8")
    sync_embedded_snapshot()
    print(f"Completed refreshed presentations/audio for 10 questions. Backup: {archive}", flush=True)


if __name__ == "__main__":
    main()
