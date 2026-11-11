import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pymupdf
import json
import re
from pipeline.key_rotator import rotator

def run_pre_phase():
    data_dir = os.path.join(PROJECT_ROOT, 'data')
    os.makedirs(data_dir, exist_ok=True)
    pdf_path = os.path.join(PROJECT_ROOT, 'AIR1 DT Question Bank.pdf')
    doc = pymupdf.open(pdf_path)
    toc_text = doc[2].get_text() # Page 3 (0-indexed 2)

    client = rotator.get_client()
    prompt = f"""You are an expert tax educator and AI parser.
Analyze this Table of Contents from a Direct Tax CA Final Question Bank:
{toc_text}

Extract the structured list of all chapters. Return ONLY valid JSON:
{{
  "subject": "Direct Tax",
  "total_chapters": 25,
  "chapters": [
    {{
      "chapter_number": 1,
      "title": "Basic Concepts, Tax Rates and Exempt Income",
      "page_range": "1.1 - 1.18"
    }}
  ]
}}
"""

    resp = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    raw = resp.text.strip()
    if '```' in raw:
        raw = re.sub(r'^```[a-z]*\n', '', raw, flags=re.MULTILINE)
        raw = raw.replace('```', '')
    
    catalog = json.loads(raw.strip())
    
    out_file = os.path.join(data_dir, 'catalog.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        
    print(f"Pre-Phase Complete: {len(catalog.get('chapters', []))} chapters indexed.")
    return catalog

if __name__ == '__main__':
    run_pre_phase()
