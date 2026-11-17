"""Quality gate for generated provision-specific Study Board screenplays."""

from __future__ import annotations

import argparse
import calendar
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_LAYOUTS = {
    "example_scene", "decision_tree", "checklist_gate", "timeline_windows",
    "flow_actors", "compare_regimes", "slab_ladder", "ledger", "waterfall",
    "deemed_value", "case_card", "statute_quote", "takeaway", "fork", "meter",
    "timeline", "split", "compare", "story_scene", "headline", "statute_quote",
    "case_card", "threshold", "computation", "rule_card", "tax_split",
}
DATE_RE = re.compile(r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:FY|AY|P\.Y\.|A\.Y\.)\s*\d{4}\s*[-–/]\s*\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\b", re.I)
SECTION_RE = re.compile(r"\b(?:section|sec\.?|u/s|rule)\s*[0-9]+[A-Z]?(?:\([0-9A-Za-z]+\))*", re.I)
MONEY_RE = re.compile(r"(?:₹|\bINR\b)\s*([0-9][0-9,]*(?:\.\d+)?)\s*(lacs?|lakhs?|crores?)?|\b([0-9][0-9,]*(?:\.\d+)?)\s*(lacs?|lakhs?|crores?)\b", re.I)
NAME_RE = re.compile(r"\b(?:Mr\.?|Mrs\.?|Ms\.?|Shri|Smt\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?!\.)")

def canonical_qid(qid: str) -> str:
    match = re.search(r"(?:dt-)?c(\d+)[-_]q(\d+)", qid, re.I)
    if not match:
        raise ValueError(f"Invalid question id: {qid}")
    return f"dt-c{int(match.group(1))}-q{int(match.group(2))}"

def stringify(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(stringify(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(stringify(item) for item in value)
    return str(value or "")

def string_values(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from string_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from string_values(item)
    elif isinstance(value, str):
        yield value

def number_keys(text: str) -> set[str]:
    found = set()
    for match in MONEY_RE.finditer(text):
        value = match.group(1) or match.group(3) or ""
        unit = (match.group(2) or match.group(4) or "").casefold()
        try:
            amount = float(value.replace(",", ""))
            if unit.startswith(("lac", "lakh")):
                amount *= 100000
            elif unit.startswith("crore"):
                amount *= 10000000
            found.add(str(int(amount)))
        except ValueError:
            pass
    return found

def section_key(value: str) -> str:
    match = re.search(r"([0-9]+[A-Z]?(?:\([0-9A-Za-z]+\))*)", value, re.I)
    return match.group(1).casefold() if match else re.sub(r"\s+", " ", value).casefold()

def date_keys(text: str) -> set[str]:
    months = {name.casefold(): index for index, name in enumerate(calendar.month_name) if name}
    months.update({name.casefold(): index for index, name in enumerate(calendar.month_abbr) if name})
    result = set()
    for raw in DATE_RE.findall(text):
        value = raw.casefold().replace("–", "-")
        fiscal = re.search(r"(?:fy|ay|p\.y\.|a\.y\.)\s*(\d{4})\s*[-/]\s*(\d{2,4})", value)
        if fiscal:
            result.add(f"period:{fiscal.group(1)}-{fiscal.group(2)[-2:]}")
            continue
        month = next((idx for name, idx in months.items() if re.search(rf"\b{name}\b", value)), None)
        if month:
            parts = re.findall(r"\d+", value)
            if len(parts) >= 2:
                year = int(parts[-1]); day = int(parts[0])
                result.add(f"{year:04d}-{month:02d}-{day:02d}")
            continue
        parts = re.findall(r"\d+", value)
        if len(parts) == 3:
            day, month_num, year = map(int, parts)
            if year < 100:
                year += 2000 if year < 70 else 1900
            if 1 <= day <= 31 and 1 <= month_num <= 12:
                result.add(f"{year:04d}-{month_num:02d}-{day:02d}")
        else:
            result.add("".join(parts))
    return result

def _text_objects(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _text_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _text_objects(child)

def validate_screenplay(screenplay: dict, question: str, answer: str, provision: str, same_chapter: list[dict] | None = None) -> list[str]:
    issues: list[str] = []
    qid = canonical_qid(str(screenplay.get("question_id", "")))
    source = " ".join((question or "", answer or "", provision or ""))
    output = stringify(screenplay)
    source_lower = source.casefold()
    beats = screenplay.get("beats") or []
    layouts = [str(beat.get("layout", "")) for beat in beats]

    if len(beats) < 3:
        issues.append("screenplay has fewer than three beats")
    if len(set(layouts)) < 3:
        issues.append("screenplay has fewer than three distinct layouts")
    for layout in layouts:
        if layout not in SUPPORTED_LAYOUTS:
            issues.append(f"unsupported layout: {layout}")
    for other in same_chapter or []:
        other_id = str(other.get("question_id", ""))
        if other_id == qid:
            continue
        if layouts and layouts == [str(beat.get("layout", "")) for beat in other.get("beats", [])]:
            issues.append(f"layout sequence duplicates {other_id}")
            break

    money_out = number_keys(output)
    money_source = number_keys(source)
    for amount in sorted(money_out - money_source):
        issues.append(f"unsupported amount: {amount}")
    for date in sorted(date_keys(output) - date_keys(source)):
        issues.append(f"unsupported date: {date}")
    source_sections = {section_key(item) for item in SECTION_RE.findall(source)}
    for section in SECTION_RE.findall(output):
        if section_key(section) not in source_sections:
            issues.append(f"unsupported section/rule: {section}")
    for text in string_values(screenplay):
        for name in NAME_RE.findall(text):
            if name.casefold().strip() not in source_lower:
                issues.append(f"unsupported named party: {name.strip()}")
    director = screenplay.get("director") or {}
    protagonist = str(director.get("protagonist", "")).strip()
    generic_roles = {"assessee", "taxpayer", "company", "firm", "buyer", "seller", "payer", "payee", "government", "authority", "tax authority", "tax department", "income tax department"}
    if protagonist and protagonist.casefold() not in source_lower and protagonist.casefold() not in generic_roles:
        issues.append(f"unsupported director protagonist: {protagonist}")
    if qid != "dt-c2-q25" and re.search(r"\b(?:Hari|Pari)\b", output, re.I):
        issues.append("Q25-specific Hari/Pari names leaked into another question")

    allowed_roles = {"key_fact", "explanation", "rapid_list", "calm"}
    is_director_screenplay = isinstance(screenplay.get("director"), dict)
    for index, beat in enumerate(beats):
        role = beat.get("animation_role")
        if is_director_screenplay and role not in allowed_roles:
            issues.append(f"{beat.get('id', f'beat-{index+1}')} has no role-derived animation")
        if is_director_screenplay and "style" in beat and role not in allowed_roles:
            issues.append(f"{beat.get('id', f'beat-{index+1}')} uses an ungrounded style combination")
        beat_text = " ".join((beat.get("voice_sync_text", ""), stringify(beat.get("visual_data", {}))))
        spoken_numbers = number_keys(beat.get("voice_sync_text", ""))
        visible_numbers = number_keys(stringify(beat.get("visual_data", {})))
        if spoken_numbers and not spoken_numbers.issubset(visible_numbers):
            issues.append(f"{beat.get('id', f'beat-{index+1}')} speaks an example amount that is not shown visually")
        spoken_dates = date_keys(beat.get("voice_sync_text", ""))
        visible_dates = date_keys(stringify(beat.get("visual_data", {})))
        if spoken_dates and not spoken_dates.issubset(visible_dates):
            issues.append(f"{beat.get('id', f'beat-{index+1}')} speaks a date that is not shown visually")
        if beat.get("layout") == "example_scene" and not (number_keys(beat_text) or DATE_RE.search(beat_text)):
            issues.append("opening example scene has no visible example amount or date")
        if not beat.get("voice_sync_text"):
            issues.append(f"{beat.get('id', f'beat-{index+1}')} has no narration")
    return list(dict.fromkeys(issues))

def load_questions(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = {}
    for question in data.get("questions", []):
        qid = f"dt-c{int(question.get('chapter_number') or 1)}-q{int(question.get('question_number') or 1)}"
        questions[qid] = question
    return questions

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenplay", type=Path)
    parser.add_argument("--screenplay-dir", type=Path, default=ROOT / "redesign_demo" / "data" / "screenplays")
    parser.add_argument("--questions", type=Path, default=ROOT / "redesign_demo" / "data" / "pipeline_questions.json")
    args = parser.parse_args()
    questions = load_questions(args.questions)
    files = [args.screenplay] if args.screenplay else sorted(args.screenplay_dir.glob("*.json"))
    errors = []
    screenplays = []
    for file in files:
        try:
            screenplays.append((file, json.loads(file.read_text(encoding="utf-8"))))
        except Exception as exc:
            errors.append(f"{file}: invalid JSON ({exc})")
    # Existing hand-authored fixtures predate the director schema and must stay
    # byte-for-byte stable. The quality gate targets AI-generated director output.
    if args.screenplay is None:
        legacy_count = sum(1 for _, screenplay in screenplays if not isinstance(screenplay.get("director"), dict))
        screenplays = [(file, screenplay) for file, screenplay in screenplays if isinstance(screenplay.get("director"), dict)]
    else:
        legacy_count = 0
    for file, screenplay in screenplays:
        qid = canonical_qid(str(screenplay.get("question_id", file.stem)))
        question = questions.get(qid)
        if not question:
            errors.append(f"{file}: no matching question context for {qid}")
            continue
        chapter = int(question.get("chapter_number") or 1)
        others = [other for _, other in screenplays if other.get("question_id") != qid and str(other.get("question_id", "")).startswith(f"dt-c{chapter}-")]
        provision_data = json.loads((ROOT / "redesign_demo" / "data" / "provisions.json").read_text(encoding="utf-8"))
        provisions = provision_data.get("provisions", []) if isinstance(provision_data, dict) else provision_data
        prov = next((item for item in provisions if ((item.get("chapter_number") is not None and int(item.get("chapter_number")) == chapter) or (chapter == 1 and item.get("chapter_number") is None)) and int(item.get("question_number") or 0) == int(question.get("question_number") or 0)), {})
        issues = validate_screenplay(screenplay, question.get("question_text", ""), question.get("answer_text", ""), prov.get("provision_presentation_markdown", ""), others)
        errors.extend(f"{file}: {issue}" for issue in issues)
    if errors:
        print("SCREENPLAY VALIDATION FAILED")
        print("\n".join(errors))
        return 1
    suffix = f"; skipped {legacy_count} legacy fixture(s)" if legacy_count else ""
    print(f"Screenplay validation passed for {len(screenplays)} generated screenplay(s){suffix}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
