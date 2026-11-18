"""Quality gate for generated provision-specific Study Board screenplays."""

from __future__ import annotations

import argparse
import calendar
import json
import re
import os
from difflib import SequenceMatcher
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
DATE_RE = re.compile(r"\b(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|(?:FY|AY|P\.Y\.|A\.Y\.|assessment\s+year)\s*\d{4}\s*[-–/]\s*\d{2,4}|(?:\d{1,2}(?:st|nd|rd|th)?|\d{3}(?:st|nd|rd|th|t))\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*,?\s+\d{4}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*,?\s*\d{4})\b", re.I)
SECTION_RE = re.compile(r"\b(?:section|sec\.?|u/s|rule)\s*[0-9]+[A-Z]?(?:\([0-9A-Za-z]+\))*", re.I)
MONEY_RE = re.compile(r"(?:₹|\bINR\b)\s*([0-9][0-9,]*(?:\.\d+)?)\s*(lacs?|lakhs?|crores?|l\b|cr\b)?|\b([0-9][0-9,]*(?:\.\d+)?)\s*(lacs?|lakhs?|crores?|l\b|cr\b)\b", re.I)
PERCENT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*%")
NAME_RE = re.compile(r"\b(?:Mr\.?|Mrs\.?|Ms\.?|Shri|Smt\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?!\.)")

def canonical_qid(qid: str) -> str:
    match = re.search(r"(idt|dt)-?c(\d+)[-_]q(\d+)", qid, re.I) or re.search(r"(?:^|[-_])c(\d+)[-_]q(\d+)", qid, re.I)
    if not match:
        raise ValueError(f"Invalid question id: {qid}")
    if len(match.groups()) == 3:
        subject, chapter, question = match.groups()
    else:
        subject, chapter, question = "dt", *match.groups()
    return f"{subject.casefold()}-c{int(chapter)}-q{int(question)}"

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
            if unit.startswith(("lac", "lakh")) or unit == "l":
                amount *= 100000
            elif unit.startswith("crore") or unit == "cr":
                amount *= 10000000
            found.add(str(int(amount)))
        except ValueError:
            pass
    # Tax answers frequently lose the rupee symbol during PDF/OCR extraction.
    # Accept unmistakable Indian-grouped figures such as 25,00,000 and 34,500.
    for raw in re.findall(r"(?<![\w/])\d{1,3}(?:,\d{2})*,\d{3}(?!\d)", text):
        try:
            found.add(str(int(raw.replace(",", ""))))
        except ValueError:
            pass
    return found

def money_phrases(text: str) -> list[str]:
    phrases = []
    for match in MONEY_RE.finditer(text):
        phrase = match.group(0).strip()
        if phrase and number_keys(phrase):
            phrases.append(phrase)
    for match in re.finditer(r"(?<![\w/])\d{1,3}(?:,\d{2})*,\d{3}(?!\d)", text):
        phrase = match.group(0)
        if number_keys(phrase):
            phrases.append(phrase)
    return list(dict.fromkeys(phrases))

def derive_amounts(source: str) -> dict[str, str]:
    """Return supported arithmetic results using at most three source values."""
    values = sorted(int(value) for value in number_keys(source) if value.isdigit())
    derived: dict[str, str] = {str(value): f"source amount {value}" for value in values}
    rates = [float(rate) for rate in PERCENT_RE.findall(source)]
    max_value = 10**12
    for rate in rates:
        for value in values:
            result = round(value * rate / 100)
            if result:
                derived.setdefault(str(result), f"{value} * {rate:g}%")
    for i, first in enumerate(values):
        for j in range(i + 1, len(values)):
            second = values[j]
            for result, expression in (
                (first + second, f"{first} + {second}"),
                (abs(first - second), f"abs({first} - {second})"),
                (first * second, f"{first} * {second}"),
            ):
                if 0 < result <= max_value:
                    derived.setdefault(str(result), expression)
            for rate in rates:
                for base, other in ((first, second), (second, first)):
                    result = round(base * rate / 100 + other)
                    if 0 < result <= max_value:
                        derived.setdefault(str(result), f"{other} + {base} * {rate:g}%")
    for i, first in enumerate(values):
        for j in range(i + 1, len(values)):
            second = values[j]
            for third in values[j + 1:]:
                result = first + second + third
                if result <= max_value:
                    derived.setdefault(str(result), f"{first} + {second} + {third}")
                for result, expression in (
                    (abs(first + second - third), f"abs({first} + {second} - {third})"),
                    (abs(first - second + third), f"abs({first} - {second} + {third})"),
                    (abs(first * second * third), f"{first} * {second} * {third}"),
                ):
                    if 0 < result <= max_value:
                        derived.setdefault(str(result), expression)
    return derived

def section_key(value: str) -> str:
    match = re.search(r"([0-9]+[A-Z]?(?:\([0-9A-Za-z]+\))*)", value, re.I)
    return match.group(1).casefold() if match else re.sub(r"\s+", " ", value).casefold()

def date_keys(text: str) -> set[str]:
    text = re.sub(r"\b(\d{1,2})%\s+Augus[₹t]?", r"\1 August", text, flags=re.I)
    text = re.sub(r"\b(\d{1,2})\*\s+(?=(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))", r"\1 ", text, flags=re.I)
    months = {name.casefold(): index for index, name in enumerate(calendar.month_name) if name}
    months.update({name.casefold(): index for index, name in enumerate(calendar.month_abbr) if name})
    result = set()
    for raw in DATE_RE.findall(text):
        value = raw.casefold().replace("–", "-")
        fiscal = re.search(r"(?:fy|ay|p\.y\.|a\.y\.|assessment\s+year)\s*(\d{4})\s*[-/]\s*(\d{2,4})", value)
        if fiscal:
            result.add(f"period:{fiscal.group(1)}-{fiscal.group(2)[-2:]}")
            continue
        month = next((idx for name, idx in months.items() if re.search(rf"\b{name}\b", value)), None)
        if month:
            parts = re.findall(r"\d+", value)
            if len(parts) == 1:
                result.add(f"{int(parts[0]):04d}-{month:02d}")
                continue
            if len(parts) >= 2:
                year = int(parts[-1]); day = int(parts[0])
                if day > 31 and len(str(day)) == 3:
                    day = int(str(day)[:2])
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
    for fiscal in re.findall(r"\b(20\d{2})\s*[-–/]\s*(\d{2,4})\b", text):
        result.add(f"period:{fiscal[0]}-{fiscal[1][-2:]}")
    financial_year_ends = re.findall(r"financial\s+year[^\n.]{0,120}?\bMar(?:ch)?\s*,?\s*(20\d{2})\b", text, re.I)
    for year_text in financial_year_ends:
        year = int(year_text)
        result.add(f"period:{year - 1}-{str(year)[-2:]}")
    return result

def _date_key_supported(key: str, source_dates: set[str]) -> bool:
    if key in source_dates:
        return True
    # A month/year label is supported by a source date in that same month;
    # the reverse is intentionally rejected because it would invent a day.
    return bool(re.fullmatch(r"20\d{2}-\d{2}", key) and any(value.startswith(key + "-") for value in source_dates))

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
    if layouts and max(layouts.count(layout) for layout in set(layouts)) / len(layouts) > 0.40:
        issues.append("layout concentration exceeds 40% of beats")
    for layout in layouts:
        if layout not in SUPPORTED_LAYOUTS:
            issues.append(f"unsupported layout: {layout}")
    similarity_threshold = float(os.getenv("STUDY_BOARD_LAYOUT_SIMILARITY_THRESHOLD", "0.82"))
    current_set = set(layouts)
    for other in same_chapter or []:
        other_id = str(other.get("question_id", ""))
        if other_id == qid:
            continue
        other_layouts = [str(beat.get("layout", "")) for beat in other.get("beats", [])]
        other_set = set(other_layouts)
        jaccard = len(current_set & other_set) / max(1, len(current_set | other_set))
        sequence = SequenceMatcher(None, layouts, other_layouts).ratio()
        similarity = (jaccard + sequence) / 2
        if layouts and similarity >= similarity_threshold:
            print(f"[SCREENPLAY SIMILARITY WARNING] {qid} resembles {other_id} (Jaccard {jaccard:.2f}, sequence {sequence:.2f}, combined {similarity:.2f})")
            break

    money_out = number_keys(output)
    money_source = number_keys(source)
    derived = derive_amounts(source)
    for amount in sorted(money_out - set(derived)):
        issues.append(f"unsupported amount: {amount}")
    for amount in sorted(money_out & (set(derived) - money_source)):
        print(f"[VALIDATOR DERIVED] {amount} = {derived[amount]}")
    source_date_keys = date_keys(source)
    for date in sorted(key for key in date_keys(output) if not _date_key_supported(key, source_date_keys)):
        issues.append(f"unsupported date: {date}")
    source_sections = {section_key(item) for item in SECTION_RE.findall(source)}
    for section in SECTION_RE.findall(output):
        key = section_key(section)
        base_match = re.match(r"([0-9]+[A-Z]?)", key, re.I)
        base_supported = bool(base_match and base_match.group(1).casefold() in source_sections)
        parent_supported = bool(re.fullmatch(r"[0-9]+[A-Z]?", key, re.I) and any(source_key.startswith(key.casefold() + "(") for source_key in source_sections))
        if key not in source_sections and not base_supported and not parent_supported:
            issues.append(f"unsupported section/rule: {section}")
    for text in string_values(screenplay):
        for name in NAME_RE.findall(text):
            if name.casefold().strip() not in source_lower:
                issues.append(f"unsupported named party: {name.strip()}")
    director = screenplay.get("director") or {}
    protagonist = str(director.get("protagonist", "")).strip()
    generic_roles = {"assessee", "the assessee", "taxpayer", "the taxpayer", "company", "firm", "buyer", "seller", "payer", "payee", "government", "authority", "tax authority", "tax department", "income tax department"}
    protagonist_tokens = set(re.findall(r"[a-z0-9]+", protagonist.casefold()))
    source_tokens = set(re.findall(r"[a-z0-9]+", source_lower))
    supported_by_source_tokens = bool(protagonist_tokens and protagonist_tokens.issubset(source_tokens))
    if protagonist and protagonist.casefold() not in source_lower and protagonist.casefold() not in generic_roles and not supported_by_source_tokens:
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
            missing = ", ".join(sorted(spoken_numbers - visible_numbers))
            issues.append(f"{beat.get('id', f'beat-{index+1}')} speaks amount(s) {missing} that are not shown visually")
        spoken_dates = date_keys(beat.get("voice_sync_text", ""))
        visible_dates = date_keys(stringify(beat.get("visual_data", {})))
        if spoken_dates and not spoken_dates.issubset(visible_dates):
            issues.append(f"{beat.get('id', f'beat-{index+1}')} speaks a date that is not shown visually")
        if beat.get("layout") == "example_scene" and (number_keys(source) or date_keys(source)) and not (number_keys(beat_text) or DATE_RE.search(beat_text)):
            issues.append("opening example scene has no visible example amount or date")
        if not beat.get("voice_sync_text"):
            issues.append(f"{beat.get('id', f'beat-{index+1}')} has no narration")
    return list(dict.fromkeys(issues))

def load_questions(path: Path) -> tuple[dict[str, dict], list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = {}
    for question in data.get("questions", []):
        subject = str(question.get("subject") or data.get("catalog", {}).get("subject") or "dt").casefold()
        subject = "idt" if "indirect" in subject or subject == "idt" else "dt"
        qid = f"{subject}-c{int(question.get('chapter_number') or 1)}-q{int(question.get('question_number') or 1)}"
        questions[qid] = question
    embedded_provisions = data.get("provisions", []) if isinstance(data, dict) else []
    return questions, embedded_provisions

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenplay", type=Path)
    parser.add_argument("--screenplay-dir", type=Path, default=ROOT / "redesign_demo" / "data" / "screenplays")
    parser.add_argument("--questions", type=Path, default=ROOT / "redesign_demo" / "data" / "pipeline_questions.json")
    args = parser.parse_args()
    questions, embedded_provisions = load_questions(args.questions)
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
        if screenplay.get("fallback") is True:
            errors.append(f"{file}: fallback:true is not permitted")
        beat_layouts = [str(beat.get("layout", "")) for beat in screenplay.get("beats", []) if isinstance(beat, dict)]
        if beat_layouts and max(beat_layouts.count(layout) for layout in set(beat_layouts)) / len(beat_layouts) > 0.40:
            errors.append(f"{file}: one layout exceeds 40% of beats ({beat_layouts})")
        question = questions.get(qid)
        if not question:
            errors.append(f"{file}: no matching question context for {qid}")
            continue
        chapter = int(question.get("chapter_number") or 1)
        subject_prefix = qid.split("-", 1)[0]
        others = [other for _, other in screenplays if other.get("question_id") != qid and str(other.get("question_id", "")).startswith(f"{subject_prefix}-c{chapter}-")]
        prov_file = ROOT / "redesign_demo" / "data" / "provisions.json"
        if prov_file.is_file():
            provision_data = json.loads(prov_file.read_text(encoding="utf-8"))
            provisions = provision_data.get("provisions", []) if isinstance(provision_data, dict) else provision_data
        else:
            provisions = embedded_provisions
        prov = next((item for item in provisions if ((item.get("chapter_number") is not None and int(item.get("chapter_number")) == chapter) or (chapter == 1 and item.get("chapter_number") is None)) and int(item.get("question_number") or 0) == int(question.get("question_number") or 0)), {})
        combined_provision = "\n".join(filter(None, (
            prov.get("provision_presentation_markdown", ""),
            screenplay.get("source_provision", ""),
        )))
        issues = validate_screenplay(screenplay, question.get("question_text", ""), question.get("answer_text", ""), combined_provision, others)
        if qid != "dt-c2-q25" and re.search(r"\b(?:Hari|Pari)\b", stringify(screenplay), re.I):
            issues.append("Hari/Pari names appear outside Q25")
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
