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

Analyze this statutory problem, answer, and underlying legal provisions:
---
QUESTION {question_number}:
{question_text}

SOLUTION / STATUTORY BASIS:
{answer_text}
---

Your mission is to autonomously design a bespoke, highly effective visual learning presentation and mindmap specifically tailored to this statutory provision.

DO NOT restrict yourself to any fixed template, category, or predetermined structure. Tax law contains thousands of diverse provisions:
- If this law involves progressive slabs/rates -> structure it with tiered visual slab matrices.
- If it is a comparative legal doctrine -> structure it with side-by-side distinction criteria and judicial benchmarks.
- If it is a multi-step computation -> structure it with a sequential mathematical ladder and verification thresholds.
- If it is an exemption/qualification rule -> structure it with statutory eligibility gates, disqualifications, and monetary caps.
- If it involves procedural timelines or reassessments -> structure it with chronological milestones and jurisdictional time limits.
- If it is an adjustment mechanism (like MAT u/s 115JB) -> structure it with positive and negative adjustment matrices.

You must output a STRICT, VALID JSON object with the following schema:
{{
  "canonical_topic": "The definitive, standardized name of this statutory doctrine (e.g. 'Section 4: Diversion vs Application of Income', 'Section 115BAC Default Tax Regime Slabs', 'Marginal Relief for Domestic Companies'). Multiple questions testing the same doctrine MUST share this exact canonical name.",
  "statutory_sections": ["Section ...", "Rule ..."],
  "core_principle": "A concise 1-sentence statement of the core statutory rule.",
  "provision_presentation_markdown": "A comprehensive, elegant GitHub Flavored Markdown visual presentation of the statutory provision. Freely use clean Markdown tables, bulleted lists, and GitHub callout boxes (> [!NOTE], > [!IMPORTANT], > [!WARNING]) to highlight rules and common traps. DO NOT mention 'in this question' - explain the statutory law itself.",
  "mindmap": {{
    "doctrine": "Name of the statutory doctrine",
    "root": {{
      "id": "root",
      "number": "1",
      "title": "Title of the doctrine",
      "badge": "Statutory citation (e.g. Section 4 · Section 28)",
      "voice_sync_text": "Spoken Malayalam introduction by the teacher introducing this specific statutory provision (e.g. 'ഇന്ന് നമ്മൾ പഠിക്കുന്നത്...')."
    }},
    "branches": [
      {{
        "branch_id": "branch-1",
        "branch_title": "First organic aspect of this provision",
        "badge": "Short badge",
        "icon": "scales",
        "points": [
          {{
            "id": "beat-1-1",
            "title": "Clear sub-point title",
            "number": "1.1.1",
            "badge": "Rule",
            "body": [
              "Key statutory rule bullet 1",
              "Key statutory rule bullet 2"
            ],
            "table_data": null,
            "voice_sync_text": "Spoken Malayalam teacher explanation of this point (clear, conversational, professional CA teaching style with phonetic English statutory terms)."
          }}
        ],
        "flow_summary": []
      }}
    ]
  }}
}}

CRITICAL RULES:
1. Autonomously choose the number of branches (typically 3 to 5) and points that best reflect the legal anatomy of this specific provision.
2. Icons can be: scales, shield, calculator, percent, cap, warning, gear, check, user, building, rupee.
3. Every point must include a high-quality, professional 'voice_sync_text' in natural Malayalam explaining that card's legal concept.
4. If a point naturally contains numerical tables or thresholds, populate 'table_data' with {{ "headers": [...], "rows": [[...], [...]] }}, otherwise set to null.
5. In 'provision_presentation_markdown':
   - Use clean, standard Markdown tables and bulleted lists (`- ...`).
   - NEVER use ASCII pseudo-diagrams, pipes, or arrows (e.g. DO NOT write '|------', '|-->', '-->'). Use clean nested bullet lists or tables instead.
   - All markdown bold/italics syntax MUST be properly paired and closed on the same line (e.g. `**Bold Text**`). Never leave unclosed `**` at the end or beginning of headings or callout titles.
   - For callout titles, write: `> [!IMPORTANT] Title Name: Description` (clean plain title, no unclosed markdown asterisks).
   - Any mathematical or tax formula must either be in standard plain text (e.g. `Total Income - ₹ 12,00,000`) or standard closed LaTeX `$formula$` without raw unescaped `&` or `%`.
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
