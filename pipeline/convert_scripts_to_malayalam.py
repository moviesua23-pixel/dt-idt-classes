import os
import sys
import json
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator

def convert():
    sb_file = os.path.join(PROJECT_ROOT, 'data', 'ppt_storyboards.json')
    with open(sb_file, 'r', encoding='utf-8') as f:
        sb = json.load(f)

    for key in ['q5', 'q9', 'q10']:
        print(f"Translating {key} to Malayalam Unicode script...")
        topic = sb[key]
        for slide in topic.get('slides', []):
            old_txt = slide.get('malayalam_narration', '')
            # If already Malayalam, skip
            if any('\u0D00' <= char <= '\u0D7F' for char in old_txt):
                continue
                
            prompt = f"""Rewrite this spoken tax lecture narration into natural, friendly spoken Malayalam Unicode script (മലയാളം ലിപിയിൽ എഴുതുക).
Keep tax technical terms (Section 87A, Surcharge, Domestic Company, Turnover, 7%, 12%, 1 Crore) natural.
Output ONLY the rewritten Malayalam text:

{old_txt}"""
            
            for attempt in range(len(rotator.keys) * 2):
                client = rotator.get_client()
                try:
                    resp = client.models.generate_content(
                        model='gemini-flash-lite-latest',
                        contents=prompt
                    )
                    ml_txt = resp.text.strip().replace('```', '')
                    slide['malayalam_narration'] = ml_txt
                    print(f"  Slide {slide.get('slide_number')} converted!")
                    break
                except Exception as e:
                    print(f"  Retry slide {slide.get('slide_number')}: {e}")
                    time.sleep(1)

    with open(sb_file, 'w', encoding='utf-8') as f:
        json.dump(sb, f, indent=2, ensure_ascii=False)
    print("Conversion complete!")

if __name__ == '__main__':
    convert()
