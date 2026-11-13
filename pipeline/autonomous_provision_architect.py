"""
pipeline/autonomous_provision_architect.py
Autonomous Provision-Specific Presentation Architect powered by Gemini API.

Inspects any Direct Tax (DT) or Indirect Tax (IDT) question and statutory provision,
and autonomously designs an organic, custom presentation structure and mindmap
tailored specifically to that law—without artificial category limits.
"""

import os
import sys
import json
import re
import time
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import rotator, AllKeysQuotaExhaustedError, is_quota_error

AUTONOMOUS_PROMPT_TEMPLATE = """You are a distinguished Senior CA Final Tax Professor and Expert Visual Learning Architect for Indian Direct Tax and Indirect Tax.

========================================================================================
ABSOLUTE CORE MANDATE 1: PURE STATUTORY LAW ONLY (ZERO EXAM FACTS)
========================================================================================
You are creating a timeless, standalone visual lecture on the STATUTORY LAW / DOCTRINE itself.
The question and answer below are provided SOLELY for you to identify WHICH statutory sections, rules, and judicial doctrines are involved.

DO NOT SOLVE OR EXPLAIN THE EXAM QUESTION!
1. NEVER mention the assessee's name or company name (e.g. NEVER mention 'Mr. Ankur', 'Yahoo Movies Limited', 'Mr. Mahesh', 'ABC Ltd', 'Mr. X', etc.).
2. NEVER mention problem-specific transaction figures (e.g. '₹ 5,00,000', '₹ 11,00,000', etc.).
3. NEVER write or speak phrases like:
   - 'In this question...' / 'According to the given question...'
   - 'ഈ ചോദ്യത്തിൽ...' / 'ചോദ്യത്തിൽ പറഞ്ഞിരിക്കുന്ന...'
   - 'അതുകൊണ്ട് അങ്കുറിന്...' / 'അസ്സസ്സീക്ക് ലഭിച്ച തുക...'
4. Every single card, markdown table, and Malayalam voice script must explain EXCLUSIVELY:
   - The statutory section rules, conditions, and thresholds.
   - Judicial benchmarks and precedents (e.g. Supreme Court / High Court tests).
   - Universal tax treatments, rates, and exemptions.

========================================================================================
ABSOLUTE CORE MANDATE 2: 100% STATUTORY COVERAGE (ZERO PROVISIONS AVOIDED)
========================================================================================
Identify EVERY SINGLE statutory provision, section, sub-section, rule, proviso, explanation, threshold, and judicial precedent contained in or relied upon by the question and solution.
DO NOT omit or drop any provision! Even if a question touches 4, 5, or 6 distinct provisions across different heads of income (e.g. PGBP + Capital Gains + TDS + Set-off + Chapter VI-A), EVERY ONE of them must be captured in your summary.

========================================================================================
ABSOLUTE CORE MANDATE 3: CONCISE EXECUTIVE SUMMARY (NO ESSAY BLOAT)
========================================================================================
Do NOT explain provisions in long narrative essays or theoretical paragraphs.
Students need a high-yield, structured, scannable statutory summary:
1. TABLE FIRST: Use concise Markdown tables to map provisions, conditions, and tax treatments.
2. POINT CHECKLISTS: Use short 1-2 line bullet points for statutory tests (max 2-3 bullets per section).
3. LENGTH TARGET: Keep 'provision_presentation_markdown' compact and dense (~1,000 to 1,600 characters total).

========================================================================================
ABSOLUTE CORE MANDATE 4: VOICE PRONUNCIATION & LANGUAGE STANDARDS (UNIVERSAL ENGLISH)
========================================================================================
All voice scripts ('voice_sync_text') MUST strictly follow the Kerala CA Education teaching standard:
1. SECTIONS & SUB-SECTIONS IN ENGLISH:
   - Always write in standard English Latin script: 'Section 49(1)', 'Section 2(42A)', 'Section 55(2)(aa)', 'Section 112A', 'Rule 8'.
   - NEVER transliterate sections into Malayalam script (e.g. NEVER write 'സെക്ഷൻ 49(1)' or 'സെക്ഷൻ നാൽപ്പത്തിയൊമ്പത്'). Write purely: 'Section 49(1)'.
2. DATES & YEARS IN ENGLISH:
   - Always write dates, financial years, and assessment years in English: '1st April 2001', '31st March 2024', 'Assessment Year 2024-25', 'Financial Year 2023-24'.
   - NEVER translate dates into Malayalam words (NEVER write 'ഒന്നാം തിയ്യതി ഏപ്രിൽ മാസം' or 'വർഷം 2001-ൽ').
3. UNIVERSAL DOMAIN RULE FOR ALL TAX, STATUTORY, LEGAL & FINANCIAL TERMS:
   - Do NOT limit this to a fixed list. ANY and EVERY word or concept related to tax, law, statutory provisions, finance, accounting, or computation MUST remain in standard English.
   - Examples across all topics: 'Tax', 'Income Tax', 'Capital Gains', 'Capital Asset', 'Cost of Acquisition', 'Fair Market Value', 'Indexed Cost of Acquisition', 'Stamp Duty Value', 'Full Value of Consideration', 'Assessee', 'Previous Owner', 'Transfer', 'Exemption', 'Deduction', 'Set-off', 'Carry Forward', 'Clubbing', 'PGBP', 'Depreciation', 'Written Down Value', 'Slump Sale', 'Deemed Dividend', 'TDS', 'TCS', 'Advance Tax', 'Tax Audit', 'Reassessment', 'Appeal', 'Penalty'.
   - NEVER coin artificial Malayalam equivalents (do NOT write 'മൂലധന നേട്ടം', 'നികുതി', 'വാങ്ങിയ വില').
4. SPOKEN SENTENCE STYLE:
   - Use friendly, spoken Malayalam for sentence framing, connecting words, and explanations ('ഇവിടെ നമ്മൾ ശ്രദ്ധിക്കേണ്ടത്...', 'ഇതിന്റെ legal rule എന്താണെന്ന് നോക്കാം...').
   - Embed all technical statutory terms, sections, and dates cleanly in English.

Analyze the statutory provisions behind this problem and solution:

---
QUESTION {question_number}:
{question_text}

SOLUTION / STATUTORY BASIS:
{answer_text}
---

STRUCTURAL DESIGN RULES BASED ON QUESTION TYPE:
A. IF MULTI-PROVISION / MULTI-TOPIC (contains 2 to 6 provisions from different areas/heads):
   - In 'provision_presentation_markdown':
     1. Create a Master "Statutory Summary Matrix" table at the top:
        | Area / Head | Statutory Section / Rule | Operative Threshold / Condition | Tax Treatment / Legal Consequence |
     2. Follow with compact micro-checklists (strictly 2 bullets per section) stating key exceptions or traps.
     3. If provisions integrate into a computation, provide a clean 3-4 line mathematical sequence.
   - In 'mindmap':
     Create a dedicated branch for EACH distinct provision (e.g. Branch 1: § 43B, Branch 2: § 40(a)(ia), Branch 3: § 50C, Branch 4: § 71, Branch 5: § 80JJAA). This ensures every provision gets its own visual card and independent audio point!

B. IF SINGLE-PROVISION / SINGLE-TOPIC:
   - In 'provision_presentation_markdown':
     1. Create a clean classification table, rate matrix, or comparison grid.
     2. Provide a 2-3 bullet checklist of core statutory conditions.
     3. Add a callout box (> [!WARNING] or > [!IMPORTANT]) for statutory traps or judicial benchmarks.
   - In 'mindmap':
     Create 3 to 4 branches covering the organic aspects of that provision (e.g. Scope, Eligibility Criteria, Disqualifications, Tax Impact).

You must output a STRICT, VALID JSON object with the following schema:
{{
  "canonical_topic": "Definitive, standardized name of this statutory doctrine (e.g. 'Section 4: Diversion vs Application of Income' or 'Integrated Multi-Provision Assessment: PGBP, Capital Gains & Set-off'). Multiple questions on the exact same doctrine must share this name.",
  "statutory_sections": ["Section ...", "Section ...", "Rule ..."],
  "core_principle": "A concise 1-sentence executive summary of the statutory rule or multi-provision framework.",
  "provision_presentation_markdown": "A high-yield, structured GitHub Flavored Markdown summary. Table-first, followed by crisp bullets and clean callout boxes (> [!NOTE], > [!IMPORTANT], > [!WARNING]). Strictly NO essay paragraphs and NO exam question facts.",
  "mindmap": {{
    "doctrine": "Name of the statutory doctrine or multi-provision framework",
    "root": {{
      "id": "root",
      "number": "1",
      "title": "Title of the doctrine",
      "badge": "Key statutory citations (e.g. Sec 49(1) · Sec 48 or Sec 43B · Sec 50C · Sec 40(a)(ia))",
      "voice_sync_text": "Spoken Malayalam introduction by the professor introducing the statutory provisions to be learned (approx. 10-15 seconds). Pure law only."
    }},
    "branches": [
      {{
        "branch_id": "branch-1",
        "branch_title": "Name of provision or aspect (e.g. Section 43B Statutory Dues or Section 49(1) Previous Owner Cost)",
        "badge": "Section badge",
        "icon": "scales",
        "points": [
          {{
            "id": "beat-1-1",
            "title": "Operative Rule Title",
            "number": "1.1.1",
            "badge": "Rule",
            "body": [
              "Exact statutory condition bullet 1",
              "Exact legal consequence or formula bullet 2"
            ],
            "table_data": null,
            "voice_sync_text": "Punchy 2-3 sentence Malayalam teacher explanation of this specific card's legal rule (approx. 20-30 seconds). Clear, professional CA teaching style with standard English tax terms. ABSOLUTELY NEVER mention question-specific facts, question numbers, company names, or individual names."
          }}
        ],
        "flow_summary": []
      }}
    ]
  }}
}}

CRITICAL FORMATTING RULES:
1. For multi-provision questions, create up to 5 or 6 branches so NO provision from the question/answer is left out.
2. Icons can be: scales, shield, calculator, percent, cap, warning, gear, check, user, building, rupee.
3. Every point must include a high-quality, punchy 'voice_sync_text' in natural spoken Malayalam scaffolding, with ALL sections, dates, and legal/tax/financial terms strictly in English Latin script (Mandate 4).
4. If a point naturally contains numerical tables or thresholds, populate 'table_data' with {{ "headers": [...], "rows": [[...], [...]] }}, otherwise set to null.
5. In 'provision_presentation_markdown':
   - Table-first and bullet-checklist format. Keep it concise, high-yield, and scannable.
   - NEVER use Unicode box-drawing characters (├──, └──, │, ─) or ASCII pseudo-diagrams, pipes, or arrows.
   - All markdown bold/italics syntax MUST be properly paired and closed on the same line (e.g. `**Bold Text**`).
   - For callout titles, write: `> [!IMPORTANT] Title Name: Description` (clean plain title, no unclosed markdown asterisks).
   - Mathematical or tax formulas must either be in standard plain text (e.g. `Total Income - ₹ 12,00,000`) or standard closed LaTeX `$formula$` without raw unescaped `&` or `%`.
6. Return ONLY the raw JSON object, without backticks or markdown fences.
"""

def extract_autonomous_provision(question_number: int, question_text: str, answer_text: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    """
    Calls Gemini API to autonomously inspect the provision and generate its custom structure.
    """
    prompt = AUTONOMOUS_PROMPT_TEMPLATE.format(
        question_number=question_number,
        question_text=question_text[:3000],
        answer_text=answer_text[:3000]
    )

    models_to_try = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash"
    ]

    def _call_gemini(client, model_name):
        return client.models.generate_content(
            model=model_name,
            contents=prompt
        )

    for attempt in range(max_retries):
        for model in models_to_try:
            try:
                response = rotator.execute_with_retry(_call_gemini, model)
                
                raw = response.text.strip()
                if "```" in raw:
                    raw = re.sub(r"^```[a-z]*\n", "", raw, flags=re.MULTILINE)
                    raw = raw.replace("```", "")
                
                data = json.loads(raw.strip())
                
                if "canonical_topic" in data and "provision_presentation_markdown" in data and "mindmap" in data:
                    print(f"  [SUCCESS] Autonomously synthesized structure for Q{question_number}: '{data['canonical_topic']}' using {model}")
                    return data
            except AllKeysQuotaExhaustedError:
                raise
            except Exception as e:
                print(f"  [DEBUG] Model {model} attempt error: {e}")
                time.sleep(1)
                continue

    print(f"  [WARN] Failed to autonomously generate structure for Q{question_number} after {max_retries} attempts.")
    return None

def assign_estimated_timings(mindmap: Dict[str, Any], wpm: int = 120) -> Dict[str, Any]:
    """
    Calculates estimated t0 and t1 timestamps for the root node, branches, and points
    based on the length of voice_sync_text.
    """
    current_time = 0.0
    
    root = mindmap.get("root", {})
    root_text = root.get("voice_sync_text", "")
    char_count = len(root_text)
    root_dur = max(4.0, round((char_count / 15.0), 2))
    root["t0"] = 0.0
    root["t1"] = root_dur
    current_time = root_dur + 1.0
    
    branches = mindmap.get("branches", [])
    for b_idx, b in enumerate(branches):
        b_t0 = current_time
        points = b.get("points", [])
        
        for p_idx, pt in enumerate(points):
            pt_text = pt.get("voice_sync_text", "")
            pt_chars = len(pt_text)
            pt_dur = max(5.0, round((pt_chars / 14.0), 2))
            pt["spoken"] = True
            pt["t0"] = round(current_time, 2)
            pt["t1"] = round(current_time + pt_dur, 2)
            current_time = pt["t1"] + 0.8
            
        b["t0"] = round(b_t0, 2)
        b["t1"] = round(current_time - 0.8, 2)
        current_time += 1.2
        
    mindmap["total_duration"] = round(current_time, 2)
    return mindmap

if __name__ == "__main__":
    test_q = "Mr. Arjun has a total income of Rs 16,00,000 comprising of income from house property and interest on fixed deposits. Compute his tax liability."
    test_ans = "Under normal provisions of the Income-tax Act, 1961, tax is computed at slab rates applicable for individuals based on age categories..."
    res = extract_autonomous_provision(4, test_q, test_ans)
    if res:
        res["mindmap"] = assign_estimated_timings(res["mindmap"])
        print("\nGenerated Canonical Topic:", res.get("canonical_topic"))
        print("Generated Branches Count:", len(res.get("mindmap", {}).get("branches", [])))
        print("Generated Total Duration:", res.get("mindmap", {}).get("total_duration"), "seconds")
