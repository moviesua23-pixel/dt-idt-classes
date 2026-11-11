import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pymupdf
import json
import re
from pipeline.key_rotator import rotator

def update_state(phase, percent, status_text):
    state_file = os.path.join(PROJECT_ROOT, 'data', 'state.json')
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            pass
    state[phase] = {"percent": percent, "status": status_text}
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def run_phase1(max_questions=10):
    pdf_path = os.path.join(PROJECT_ROOT, 'AIR1 DT Question Bank.pdf')
    doc = pymupdf.open(pdf_path)
    
    # We will gather text across Chapter 1 pages (PDF pages 7 to 12)
    # 0-indexed: 6 to 11
    pages_text = []
    for p in range(6, 12):
        pages_text.append(f"--- PDF PAGE {p+1} ---\n" + doc[p].get_text())
    combined_text = "\n\n".join(pages_text)
    
    update_state("phase1", 10, "Sending Chapter 1 pages to Gemini for structured extraction...")
    print("Extracting Questions 1 to 10 from Chapter 1...")
    
    client = rotator.get_client()
    prompt = f"""You are an expert Direct Tax examiner and parser.
Parse all Questions and Answers from the following text of Chapter 1 (Basic Concepts, Tax Rates and Exempt Income).

CRITICAL INSTRUCTIONS:
1. Extract questions up to Question {max_questions}.
2. Separate the Question text from the Answer text accurately.
3. If an answer contains a computation or tax calculation table, format it cleanly in Markdown table format (| Particulars | Amount |).
4. Preserve all statutory references (Sections, assessment years, case names).
5. Output strictly a JSON array of objects:
[
  {{
    "chapter_number": 1,
    "chapter_title": "Basic Concepts, Tax Rates and Exempt Income",
    "question_number": 1,
    "question_title": "Concise concept title",
    "question_text": "Complete question text...",
    "answer_text": "Complete solution text with markdown tables..."
  }}
]
Do NOT wrap in any extra text or commentary.

TEXT:
{combined_text}
"""

    resp = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    raw = resp.text.strip()
    if '```' in raw:
        raw = re.sub(r'^```[a-z]*\n', '', raw, flags=re.MULTILINE)
        raw = raw.replace('```', '')
    
    questions = json.loads(raw.strip())
    # Sort by question_number
    questions = sorted(questions, key=lambda x: x.get('question_number', 0))[:max_questions]
    
    out_file = os.path.join(PROJECT_ROOT, 'data', 'extracted_qna.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
        
    update_state("phase1", 100, f"Successfully extracted {len(questions)} questions with answers.")
    print(f"Phase 1 Complete: {len(questions)} questions extracted and saved.")
    return questions

if __name__ == '__main__':
    run_phase1()
