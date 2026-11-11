import os
import sys
import json
import re
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import rotator
from google.genai import types

def generate_storyboard_for_provision(p):
    """
    Calls Gemini API to create a structured PowerPoint presentation deck (4 slides)
    with clean visual elements, bullet points, numbers/rates, and matching Malayalam script for each slide.
    """
    prompt = f"""
You are a senior ICAI Direct Tax Faculty and Keynote Slide Designer.
Design a clean, professional 4-slide PowerPoint presentation explaining this statutory tax topic to CA Final students:

TOPIC: {p.get('core_principle') or p.get('doctrine')}
SECTIONS: {', '.join(p.get('statutory_sections') or p.get('secs') or [])}
STATUTORY DETAILS:
{p.get('provision_presentation_markdown') or p.get('rawMarkdown') or ''}

REQUIREMENTS:
1. DESIGN PHILOSOPHY: Clean PowerPoint presentation on a PURE WHITE background with high contrast dark text.
2. Structure into EXACTLY 3 or 4 slides:
   - Slide 1: Concept Overview & Statutory Applicability
   - Slide 2: Rules Matrix / Tax Rates / Thresholds Table
   - Slide 3: Practical Calculation / Marginal Relief / Relief Formula (if applicable) OR Landmark Judicial Benchmark
   - Slide 4: Key Exam Takeaways / Crucial Pitfalls to Avoid in the exam
3. For EACH SLIDE provide:
   - "slide_number": integer (1, 2, 3, 4)
   - "slide_title": Concise, bold title in English (e.g., "DOMESTIC COMPANIES: APPLICABLE TAX RATES")
   - "section_badge": Relevant statutory section (e.g., "Section 115BAA / Finance Act")
   - "layout_type": "cards" | "comparison" | "table" | "formula_steps"
   - "cards": list of 2 to 4 visual cards/boxes. Each card has:
       - "title": Short title (e.g., "Turnover <= 400 Cr", "Surcharge 7%")
       - "badge": Optional small tag (e.g., "25% Rate", "1 to 10 Cr")
       - "bullets": list of 1 to 3 concise bullet points in English
       - "is_highlight": boolean (whether this card should highlight when explained)
   - "formula_box": (Optional, for Slide 3 calculation): {{"formula_text": "...", "example_calc": "..."}}
   - "malayalam_narration": Spoken Malayalam script for THIS SPECIFIC SLIDE ONLY.
     Must be clear, friendly, conversational Malayalam explaining exactly the points shown on this slide.
     Length: 2 to 4 spoken sentences (approx 15-25 seconds per slide).

OUTPUT FORMAT: Return strictly valid JSON with no markdown wrapping:
{{
  "topic_id": "{p.get('topic_id', 'q' + str(p.get('question_number')))}",
  "topic_title": "{p.get('core_principle', '')}",
  "slides": [
    ...
  ]
}}
"""

    client = rotator.get_client()
    models_to_try = ['gemini-flash-lite-latest', 'gemini-3-flash-preview', 'gemini-3.8-flash']
    
    for attempt in range(len(rotator.keys) * 2):
        for model in models_to_try:
            try:
                print(f"Requesting Gemini model={model} for Q{p.get('question_number')}...")
                resp = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                text = resp.text.strip()
                if text.startswith('```'):
                    text = re.sub(r'^```json\s*', '', text)
                    text = re.sub(r'^```\s*', '', text)
                    text = re.sub(r'\s*```$', '', text)
                data = json.loads(text)
                return data
            except Exception as e:
                print(f"Failed with {model}: {e}")
                time.sleep(1)
        client = rotator.get_client()
    return None

def main():
    prov_file = os.path.join(PROJECT_ROOT, 'data', 'provisions.json')
    with open(prov_file, 'r', encoding='utf-8') as f:
        provisions = json.load(f)

    out_file = os.path.join(PROJECT_ROOT, 'data', 'ppt_storyboards.json')
    storyboards = {}
    if os.path.exists(out_file):
        try:
            with open(out_file, 'r', encoding='utf-8') as f:
                storyboards = json.load(f)
        except Exception:
            pass

    canonical_qns = [1, 4, 5, 6, 7, 8, 9, 10]
    canonical_provs = [p for p in provisions if p.get('question_number') in canonical_qns]

    for p in canonical_provs:
        qn = p.get('question_number')
        key = f"q{qn}"
        if key in storyboards and len(storyboards[key].get('slides', [])) >= 3:
            print(f"Storyboard for {key} already exists, skipping.")
            continue
        print(f"\n--- Generating PPT Storyboard for Q{qn}: {p.get('core_principle')} ---")
        sb = generate_storyboard_for_provision(p)
        if sb:
            storyboards[key] = sb
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(storyboards, f, indent=2, ensure_ascii=False)
            print(f"Successfully generated and saved storyboard for {key} ({len(sb.get('slides', []))} slides)")
        else:
            print(f"Failed to generate storyboard for {key}")

if __name__ == '__main__':
    main()
