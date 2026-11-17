"""Bundle generated screenplays and assemble the static Study Board site."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from urllib.parse import unquote, urlsplit
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "redesign_demo" / "data"
FRONTEND = ROOT / "redesign_demo" / "frontend"


def canonical_qid(value: str, fallback: str | None = None) -> str:
    text = str(value or "").strip()
    match = re.search(r"(?:dt-)?c(\d+)[-_]q(\d+)", text, re.I) or re.search(r"ch(\d+)[-_]q(\d+)", text, re.I)
    if match:
        return f"dt-c{int(match.group(1))}-q{int(match.group(2))}"
    if fallback:
        return canonical_qid(fallback)
    raise ValueError(f"Not a canonical screenplay question id: {value!r}")


def bundle_screenplays() -> dict:
    source = DATA / "screenplays"
    records: dict[str, dict] = {}
    for path in sorted(source.glob("*.json")):
        screenplay = json.loads(path.read_text(encoding="utf-8"))
        qid = canonical_qid(screenplay.get("question_id", path.stem), path.stem)
        screenplay["question_id"] = qid
        audio_url = str(screenplay.get("audio_url") or "").strip()
        parsed_audio = urlsplit(audio_url)
        if audio_url and not parsed_audio.scheme and not parsed_audio.netloc and not parsed_audio.path.startswith("/"):
            audio_path = Path(unquote(parsed_audio.path))
            if audio_path.parts[:1] == ("data",):
                audio_path = Path(*audio_path.parts[1:])
            if not (DATA / audio_path).is_file():
                screenplay.pop("audio_url", None)
                print(f"Omitting unavailable audio for {qid}: {audio_url}")
        records[qid] = screenplay
    output = DATA / "screenplays.bundle.json"
    output.write_text(json.dumps({"version": 1, "screenplays": records}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return records


def assemble_site(site_dir: Path) -> None:
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    for item in FRONTEND.iterdir():
        if item.is_file():
            target_name = "index.html" if item.name == "index_explainer_studio.html" else item.name
            shutil.copy2(item, site_dir / target_name)
    for relative in ("screenplays", "screenplays.bundle.json", "pipeline_questions.json", "mindmaps.json", "provisions.json", "catalog.json", "audio", "img"):
        source = DATA / relative
        if source.exists():
            destination = site_dir / "data" / relative
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, help="Also assemble a deployable static site at this path")
    args = parser.parse_args()
    records = bundle_screenplays()
    print(f"Bundled {len(records)} screenplays at {DATA / 'screenplays.bundle.json'}")
    if args.site_dir:
        assemble_site(args.site_dir.resolve())
        print(f"Assembled Pages site at {args.site_dir.resolve()}")


if __name__ == "__main__":
    main()
