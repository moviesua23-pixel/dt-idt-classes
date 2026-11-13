import os
import sys
import json
import re
import pymupdf

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

PDF_PATH = os.path.join(PROJECT_ROOT, 'AIR1 DT Question Bank.pdf')
INDEX_FILE = os.path.join(PROJECT_ROOT, 'data', 'question_index.json')

def build_pdf_index(force=False):
    """
    Scans the 638-page PDF to map out all chapters and questions.
    Returns a list of question entries:
    [
      {
        "id": "DT Ch1 Q1",
        "subject": "DT",
        "chapter_no": 1,
        "question_no": 1,
        "start_page": 7,      # 1-indexed
        "start_offset": 75,
        "end_page": 7,
        "end_offset": 1287
      }, ...
    ]
    """
    if os.path.exists(INDEX_FILE) and not force:
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                index = json.load(f)
            if len(index) >= 500:
                return index
        except Exception:
            pass

    print("[INDEXER] Scanning AIR1 DT Question Bank.pdf across all 638 pages...")
    doc = pymupdf.open(PDF_PATH)
    total_pages = len(doc)

    ch_pattern = re.compile(r'CHAPTER\s*-\s*(\d+)', re.IGNORECASE)
    q_pattern = re.compile(r'\bQuestion\s+(\d+)\b', re.IGNORECASE)

    raw_markers = []
    current_ch = 1

    for p_idx in range(total_pages):
        page_num = p_idx + 1
        txt = doc[p_idx].get_text()

        # Check for chapter start
        ch_match = ch_pattern.search(txt)
        if ch_match:
            current_ch = int(ch_match.group(1))

        # Check for additional questions section (pages ~625+)
        if page_num >= 625 and 'Additional Questions' in txt and current_ch < 26:
            current_ch = 26

        # Find questions on this page
        for m in q_pattern.finditer(txt):
            q_num = int(m.group(1))
            raw_markers.append({
                "subject": "DT",
                "chapter_no": current_ch,
                "question_no": q_num,
                "page": page_num,
                "offset": m.start()
            })

    # Deduplicate and sort markers
    sorted_markers = []
    seen = set()
    for m in raw_markers:
        key = (m["subject"], m["chapter_no"], m["question_no"])
        if key not in seen:
            seen.add(key)
            sorted_markers.append(m)

    # Sort strictly by (subject, chapter_no, question_no)
    sorted_markers.sort(key=lambda x: (x["chapter_no"], x["question_no"]))

    # Now calculate boundaries (start and end page/offset for each question)
    index = []
    num_markers = len(sorted_markers)
    for i in range(num_markers):
        curr = sorted_markers[i]
        ch = curr["chapter_no"]
        q_num = curr["question_no"]
        start_p = curr["page"]
        start_off = curr["offset"]

        if i + 1 < num_markers:
            nxt = sorted_markers[i + 1]
            end_p = nxt["page"]
            end_off = nxt["offset"]
        else:
            end_p = total_pages
            end_off = len(doc[total_pages - 1].get_text())

        index.append({
            "id": f"{curr['subject']} Ch{ch} Q{q_num}",
            "subject": curr["subject"],
            "chapter_no": ch,
            "question_no": q_num,
            "start_page": start_p,
            "start_offset": start_off,
            "end_page": end_p,
            "end_offset": end_off
        })

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

    print(f"[INDEXER] Successfully indexed {len(index)} questions across 25 chapters into {INDEX_FILE}.")
    return index

def get_question_raw_text(subject, chapter_no, question_no):
    """
    Extracts the precise raw text for a specific question from the PDF
    without making any external API calls.
    """
    index = build_pdf_index()
    q_entry = None
    for item in index:
        if item["subject"] == subject and item["chapter_no"] == chapter_no and item["question_no"] == question_no:
            q_entry = item
            break

    if not q_entry:
        return None

    doc = pymupdf.open(PDF_PATH)
    start_p = q_entry["start_page"] - 1 # 0-indexed
    end_p = q_entry["end_page"] - 1

    chunks = []
    for p in range(start_p, end_p + 1):
        txt = doc[p].get_text()
        if p == start_p and p == end_p:
            chunk = txt[q_entry["start_offset"]:q_entry["end_offset"]]
        elif p == start_p:
            chunk = txt[q_entry["start_offset"]:]
        elif p == end_p:
            chunk = txt[:q_entry["end_offset"]]
        else:
            chunk = txt
        chunks.append(chunk)

    raw_text = "\n".join(chunks).strip()
    return raw_text

def split_question_and_answer(raw_text):
    """
    Splits sliced text into Question and Answer parts using common book headers.
    """
    cleaned_lines = []
    for line in raw_text.splitlines():
        l_str = line.strip()
        if not l_str:
            continue
        if re.search(r'(CA Final Notes & Updates|BY CA ATUL AGARWAL|AIR1CA Career Institute|Page\s+\d+\.\d+)', l_str, re.IGNORECASE):
            continue
        cleaned_lines.append(l_str)
    cleaned_text = "\n".join(cleaned_lines)

    patterns = [
        r'\n\s*(?:Answer|Solution|SOLUTION|ANSWER)\s*[:\-\n]',
        r'\n\s*Computation of\b',
        r'\n\s*Tax liability\b'
    ]

    split_idx = -1
    for pat in patterns:
        m = re.search(pat, cleaned_text)
        if m:
            split_idx = m.start()
            break

    if split_idx != -1:
        q_part = cleaned_text[:split_idx].strip()
        ans_part = cleaned_text[split_idx:].strip()
    else:
        lines = cleaned_text.splitlines()
        pivot = max(1, len(lines) // 3)
        q_part = "\n".join(lines[:pivot]).strip()
        ans_part = "\n".join(lines[pivot:]).strip()

    return q_part, ans_part

if __name__ == '__main__':
    idx = build_pdf_index(force=True)
    q11_text = get_question_raw_text('DT', 1, 11)
    if q11_text:
        q, ans = split_question_and_answer(q11_text)
        print(f"Sample Q11 sliced successfully. Lengths: Q={len(q)}, Ans={len(ans)}")
