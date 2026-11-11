import os
import sys
import json
import re
import time
from typing import Dict, Any, List, Optional, Tuple, Set

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import rotator
from google.genai import types

PROVISIONS_PATH = os.path.join(PROJECT_ROOT, "data", "provisions.json")
SCRIPTS_V2_DIR = os.path.join(PROJECT_ROOT, "data", "scripts_v2")
os.makedirs(SCRIPTS_V2_DIR, exist_ok=True)

MODEL_NAME = "gemini-3-flash-preview"

FORBIDDEN_WORDS = ["Mr.", "Mr ", "Mrs.", "Ltd.", "Ltd ", "Example", "Case Study", "Illustration"]

BLOCK_NAMES = {
    1: "Scope/Applicability",
    2: "Rates/Matrix",
    3: "Computation/Relief",
    4: "Exam Cautions"
}

def extract_markdown_table_rows(markdown_text: str) -> List[List[str]]:
    """Extracts data rows from markdown tables."""
    rows = []
    lines = markdown_text.split('\n')
    in_table = False
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('|') and line_s.endswith('|'):
            # check if it is header separator |:---|:---|
            if re.match(r'^\|(?:\s*:?-+:?\s*\|)+$', line_s):
                in_table = True
                continue
            cols = [c.strip() for c in line_s.split('|')[1:-1]]
            if in_table:
                clean_cols = [re.sub(r'[*_]', '', c).strip() for c in cols]
                if any(clean_cols):
                    rows.append(clean_cols)
        else:
            in_table = False
    return rows

def validate_script_data(lines: List[Dict[str, Any]], prov_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    if not isinstance(lines, list) or len(lines) == 0:
        return False, ["Script is empty or not a list"]

    prov_md = prov_data.get('provision_presentation_markdown', '')
    prov_sec = " ".join(prov_data.get('statutory_sections', []))
    prov_princ = prov_data.get('core_principle', '')
    source_corpus = f"{prov_sec} {prov_princ} {prov_md}"
    
    # Check block distribution
    blocks_count = {1: 0, 2: 0, 3: 0, 4: 0}
    ids_seen = set()

    for idx, item in enumerate(lines):
        lid = item.get('id', '')
        if not lid or lid in ids_seen:
            errors.append(f"Line {idx}: Invalid or duplicate id: {lid}")
        ids_seen.add(lid)

        b = item.get('block')
        if b not in [1, 2, 3, 4]:
            errors.append(f"Line {lid}: block must be integer 1, 2, 3, or 4 (got {b})")
        else:
            blocks_count[b] += 1

        # Check narration_ml
        narration = item.get('narration_ml', '').strip()
        if not narration:
            errors.append(f"Line {lid}: missing narration_ml")
        else:
            words = narration.split()
            word_count = len(words)
            if word_count < 14 or word_count > 37:
                errors.append(f"Line {lid}: narration word count ({word_count}) must be 15-35 words")

        # Check forbidden words
        card = item.get('card', {})
        card_str = json.dumps(card)
        full_line_str = f"{narration} {card_str}"
        for fw in FORBIDDEN_WORDS:
            if fw.lower() in full_line_str.lower():
                errors.append(f"Line {lid}: Contains forbidden word '{fw}'")

        # Check card structure
        if not isinstance(card, dict):
            errors.append(f"Line {lid}: card must be an object")
            continue

        ctitle = card.get('title', '').strip()
        if not ctitle:
            errors.append(f"Line {lid}: card.title is missing")
        else:
            if len(ctitle.split()) > 7:
                errors.append(f"Line {lid}: card.title '{ctitle}' exceeds 6 words")

        ctype = card.get('type', '')
        if ctype not in ['rule', 'rate', 'table', 'formula', 'authority', 'caution']:
            errors.append(f"Line {lid}: card.type '{ctype}' not in [rule, rate, table, formula, authority, caution]")

        clines = card.get('lines', [])
        if not isinstance(clines, list) or len(clines) < 2 or len(clines) > 7:
            errors.append(f"Line {lid}: card.lines must contain 3 to 6 statements (got {len(clines)})")
        else:
            for ci, cl in enumerate(clines):
                if len(cl.split()) > 30:
                    errors.append(f"Line {lid}: card line {ci+1} is too long ({len(cl.split())} words, max ~25)")

    # Check 4 blocks, each 2 to 5 lines
    for b in [1, 2, 3, 4]:
        count = blocks_count.get(b, 0)
        if count < 2 or count > 6:
            errors.append(f"Block {b} ({BLOCK_NAMES[b]}) has {count} lines; must have 2 to 5 lines")

    return (len(errors) == 0), errors

def generate_script_prompt(prov_data: Dict[str, Any]) -> str:
    qn = prov_data.get('question_number')
    sections = ", ".join(prov_data.get('statutory_sections', []))
    principle = prov_data.get('core_principle', '')
    markdown = prov_data.get('provision_presentation_markdown', '')
    table_rows = extract_markdown_table_rows(markdown)

    table_instruction = ""
    if table_rows:
        table_instruction = f"""
STATUTORY TABLE REQUIREMENT:
The provision contains a statutory table with {len(table_rows)} rows:
{json.dumps(table_rows, indent=2)}
Every single one of these table rows MUST appear verbatim inside card.table in one or more cards (usually in Block 2 Rates/Matrix).
"""

    return f"""You are an elite statutory tax curriculum architect for CA / CMA Final exams.
Build an exact, script-first statutory concept mind-map breakdown for Topic Q{qn}.

SOURCE PROVISION (THE ONLY PERMISSIBLE SOURCE):
Statutory Sections: {sections}
Core Statutory Doctrine: {principle}
Statutory Presentation Markdown:
{markdown}

STRICT ARCHITECTURAL AND CONTENT CONSTRAINTS:
1. ONLY STATUTORY LAW: Use ONLY the statutory rules, rates, slabs, limits, conditions, exceptions, and authorities from the provision text above.
2. ABSOLUTELY NO QUESTION / CASE-STUDY CONTENT: NEVER use any names (e.g. Mr. X, Mr. Arjun, X Ltd), question amounts (e.g. ₹ 16,00,000), or words like "Example", "Case Study", "Illustration", "Mr.", "Ltd.".
3. PRECISE AND COMPLETE: Every single threshold, rate, limit, condition, exception, formula, and legal authority present in the provision MUST appear.
4. EXACT 4-BLOCK STRUCTURE:
   - Block 1: Scope/Applicability (2 to 4 lines)
   - Block 2: Rates/Matrix (2 to 5 lines - include the full statutory table if present)
   - Block 3: Computation/Relief (2 to 4 lines - sequential computational rules, rebate, marginal relief)
   - Block 4: Exam Cautions (2 to 4 lines - conditions, non-applicability, traps)
5. ONE LINE = ONE VOICE CLIP = ONE CARD:
   - "id": Sequential "L01", "L02", "L03", ...
   - "block": Integer 1, 2, 3, or 4
   - "block_name": Exactly one of "Scope/Applicability", "Rates/Matrix", "Computation/Relief", "Exam Cautions"
   - "narration_ml": EXACTLY ONE spoken sentence in clear Malayalam with English legal terms (e.g., "Total Income", "Section 115BAC", "Assessment Year", "Surcharge") and numbers written as in the provision. Strictly 15 to 35 words. Expresses ONE focused statutory thought.
   - "card":
     - "title": Max 6 words, clear and professional.
     - "type": One of: "rule", "rate", "table", "formula", "authority", "caution".
     - "lines": Array of 3 to 6 crisp, complete statutory statements (each up to 25 words).
     - "table": Optional. If card type is "table", provide {{"headers": [...], "rows": [[...], ...]}} matching the statutory provision table.
     - "highlights": Array of 2 to 5 key statutory terms, section numbers, or figures in this card.

{table_instruction}

Output ONLY valid JSON formatted as a top-level list of line objects:
[
  {{
    "id": "L01",
    "block": 1,
    "block_name": "Scope/Applicability",
    "narration_ml": "...",
    "card": {{
      "title": "...",
      "type": "rule",
      "lines": ["...", "...", "..."],
      "highlights": ["..."]
    }}
  }}
]
"""

def generate_and_validate_topic(prov_data: Dict[str, Any], max_retries: int = 4) -> Optional[List[Dict[str, Any]]]:
    qn = prov_data.get('question_number')
    print(f"\n=================== Generating Script for Q{qn} ===================", flush=True)
    
    prompt = generate_script_prompt(prov_data)
    
    for attempt in range(max_retries):
        print(f"-> Attempt {attempt + 1}/{max_retries} for Q{qn}...", flush=True)
        try:
            client = rotator.get_client()
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            raw_text = resp.text.strip()
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text)
                raw_text = re.sub(r'\s*```$', '', raw_text)
            
            lines = json.loads(raw_text)
            if not isinstance(lines, list):
                if isinstance(lines, dict) and "lines" in lines:
                    lines = lines["lines"]
                else:
                    raise ValueError("JSON output is not a list of lines")

            # Validate
            is_valid, errors = validate_script_data(lines, prov_data)
            if is_valid:
                print(f"-> Q{qn} SUCCESS: Validated {len(lines)} lines across 4 blocks.", flush=True)
                return lines
            else:
                print(f"   Validation issues ({len(errors)}):", flush=True)
                for err in errors[:5]:
                    print(f"     - {err}", flush=True)
                prompt += f"\n\nPREVIOUS ATTEMPT FAILED WITH ERRORS:\n" + "\n".join(errors[:8]) + "\nPlease fix these errors and regenerate the JSON strictly complying with all rules."
        except Exception as e:
            print(f"   Attempt {attempt + 1} exception: {e}", flush=True)
            time.sleep(2)

    return None

def main():
    if not os.path.exists(PROVISIONS_PATH):
        print(f"Error: {PROVISIONS_PATH} not found!")
        return

    with open(PROVISIONS_PATH, 'r', encoding='utf-8') as f:
        provisions = json.load(f)

    all_results = {}
    for prov in provisions:
        qn = prov.get('question_number')
        topic_key = f"q{qn}"
        lines = generate_and_validate_topic(prov)
        if lines:
            out_path = os.path.join(SCRIPTS_V2_DIR, f"{topic_key}.json")
            with open(out_path, 'w', encoding='utf-8') as out_f:
                json.dump(lines, out_f, indent=2, ensure_ascii=False)
            print(f"Saved: {out_path} ({len(lines)} lines)")
            all_results[topic_key] = lines
        else:
            print(f"FAILED to generate valid script for {topic_key}!")

    print(f"\nFinished. Successfully generated scripts for {len(all_results)}/10 topics.")

if __name__ == "__main__":
    main()
