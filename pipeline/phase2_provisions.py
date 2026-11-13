import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import json
import re
import time
from pipeline.key_rotator import rotator

def run_phase2():
    qna_file = os.path.join(PROJECT_ROOT, "data", "extracted_qna.json")
    with open(qna_file, "r", encoding="utf-8") as f:
        qna = json.load(f)

    out_file = os.path.join(PROJECT_ROOT, "data", "provisions.json")
    prov_map = {}
    if os.path.exists(out_file):
        try:
            with open(out_file, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    if item.get("provision_presentation_markdown"):
                        prov_map[item["question_number"]] = item
        except Exception:
            pass

    total = len(qna)
    print(f"Total questions: {total}. Already have visual tables for: {list(prov_map.keys())}")

    for idx, q in enumerate(qna, 1):
        q_num = q["question_number"]
        if q_num in prov_map:
            print(f"[{idx}/{total}] Q{q_num} already cached with table, skipping.")
            continue
            
        print(f"[{idx}/{total}] Generating elegant table for Question {q_num}...")
        
        prompt = f"""You are a senior Direct Tax professor and expert UI designer for CA Final educational platforms.

========================================================================================
ABSOLUTE CORE MANDATE: PURE STATUTORY PROVISION PRESENTATION (ZERO EXAM FACTS)
========================================================================================
Explain EXCLUSIVELY the statutory law, sections, rules, and judicial doctrines.
DO NOT SOLVE OR EXPLAIN THE EXAM QUESTION!
NEVER mention the assessee's name, company name, or transaction figures.
NEVER say 'in this question' or 'ഈ ചോദ്യത്തിൽ'.
========================================================================================

Analyze this tax problem and solution:
Question: {q.get('question_text')}
Answer: {q.get('answer_text')[:1500]}

Generate:
1. "statutory_sections": List of exact section numbers (e.g. ["Section 4", "Section 115BAC"]).
2. "core_principle": Concise principle name.
3. "provision_presentation_markdown": An ELEGANT, ADAPTIVE VISUAL PRESENTATION IN GITHUB MARKDOWN:
   - For Tax Slabs, Age Categories, Basic Exemption, Tax rates, or Surcharges: Output a clean, beautiful Markdown TABLE with clear columns (e.g. Total Income Slab | Normal (<60) | Senior (60-80) | Super Senior (80+)), followed by bullet highlights for Cess and Rebate.
   - For Comparative Doctrines (e.g. Diversion vs Application of Income, Default vs Old Regime): Output a COMPARISON TABLE with columns: (Basis of Distinction | Concept A | Concept B).
   - For Multi-step conditions or computations: Output concise numbered steps or key-value cards.
   - AVOID dense, long paragraphs of text. Make it easy for a student to grasp in 5 seconds.
4. "malayalam_audio_script": Spoken Malayalam explaining ONLY the statutory provision directly (no mention of "ഈ ചോദ്യം" or person names).

Return STRICTLY a JSON object:
{{
  "question_number": {q_num},
  "statutory_sections": [...],
  "core_principle": "...",
  "provision_presentation_markdown": "...",
  "malayalam_audio_script": "..."
}}
"""
        generated_item = None
        for attempt in range(3):
            try:
                client = rotator.get_client()
                resp = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                raw = resp.text.strip()
                if "```" in raw:
                    raw = re.sub(r"^```[a-z]*\n", "", raw, flags=re.MULTILINE)
                    raw = raw.replace("```", "")
                parsed = json.loads(raw.strip())
                generated_item = parsed
                print(f"  -> Q{q_num} generated! Length: {len(parsed.get('provision_presentation_markdown', ''))}")
                break
            except Exception as e:
                print(f"  -> Attempt {attempt+1} failed for Q{q_num}: {e}. Retrying with next key...")
                time.sleep(2)
                
        if not generated_item:
            print(f"  -> Fallback used for Q{q_num}")
            generated_item = {
                "question_number": q_num,
                "statutory_sections": ["General Provision"],
                "core_principle": q.get("question_title"),
                "provision_presentation_markdown": f"**Core Rule:** {q.get('question_title')}",
                "malayalam_audio_script": "ഡയറക്ട് ടാക്സ് നിയമത്തിലെ ഈ വ്യവസ്ഥ പ്രകാരം നികുതി കണക്കാക്കുന്നു."
            }
            
        prov_map[q_num] = generated_item
        sorted_provs = [prov_map[k] for k in sorted(prov_map.keys())]
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(sorted_provs, f, indent=2, ensure_ascii=False)
        print(f"  -> Saved {len(sorted_provs)} provisions to {out_file}")
            
    print("All provisions have elegant visual tables!")

if __name__ == '__main__':
    run_phase2()
