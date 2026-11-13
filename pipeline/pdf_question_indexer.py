import os
import sys
import json
import re
try:
    import pymupdf
except ImportError:
    pymupdf = None

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def get_pdf_path(subject="DT"):
    if str(subject).upper() == 'IDT':
        candidates = [
            os.path.join(PROJECT_ROOT, 'AIR1 IDT Question Bank.pdf'),
            os.path.join(PROJECT_ROOT, 'IDT Question Bank.pdf'),
            os.path.join(PROJECT_ROOT, 'pdfs', 'AIR1 IDT Question Bank.pdf'),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
    return os.path.join(PROJECT_ROOT, 'AIR1 DT Question Bank.pdf')

PDF_PATH = get_pdf_path('DT')
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

    if not q_entry or pymupdf is None or not os.path.exists(PDF_PATH):
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

def sanitize_and_format_text(text: str, is_question: bool = False) -> str:
    """
    Sanitizes raw extracted text from the PDF:
    - Strips 'Question X' from the beginning of the question.
    - Strips 'Answer / Solution' header from the beginning of the answer.
    - Cleans page breaks and running headers.
    - Fixes font glyph corruptions: replaces %, ¢, =, t, ~, z with ₹ before numbers.
    - Fixes common OCR errors (e.g. '55(P) Ltd.' -> 'SS(P) Ltd.').
    - Formats sub-questions ((i), (ii), etc.) into distinct markdown list items.
    - Converts tabular computations into clean Markdown tables.
    - Preserves clean paragraph breaks (\n\n).
    """
    if not text:
        return ''

    # 1. Strip Question X prefix from question, or Answer/Solution header from answer
    if is_question:
        text = re.sub(r'^\s*Question\s+\d+[:\.\s\-]*\n?', '', text, flags=re.IGNORECASE).strip()
    else:
        text = re.sub(r'^\s*(?:Answer|Solution|SOLUTION|ANSWER)\s*[:\-\n]*', '', text, flags=re.IGNORECASE).strip()

    # 2. Strip running book headers, footers and OCR boundary noise
    header_patterns = [
        r'CA Final Notes & Updates',
        r'BY CA ATUL AGARWAL\s*(?:\(AIR-1\))?',
        r'AIR1CA Career Institute\s*(?:\(ACI\))?',
        r'Page\s+\d+\.\d+',
        r'Capital Gains\s*\n',
        r'SST\s*\n',
        r'ESSE\s*\n',
        r'ear a\s*\n\s*a\s*\n\s*ee\s*\n',
        r'\bTTT\b.*',
        r'__—=d_,'
    ]
    for hp in header_patterns:
        text = re.sub(hp, '', text, flags=re.IGNORECASE)

    # 3. Currency and corrupted glyph corrections
    text = re.sub(r'\b55\s*\(P\)\s*Ltd\.', 'SS(P) Ltd.', text)
    text = re.sub(r'(?:[%¢=t~]|[\uFFFD\u00A2\u20AC])\s*(?=\d)', '₹ ', text)
    text = re.sub(r'\b8\s+(?=\d{1,3}(?:,\d{2,3})+)', '₹ ', text)
    text = re.sub(r'[\uFFFD\u201C\u201D\u2018\u2019]', '"', text)
    text = re.sub(r'(\d+)\s*=\s*(₹)', r'\1 x \2', text)

    # 4. Pre-split inline transitions after punctuation so Notes and Computations start as new paragraphs
    text = re.sub(r'(?<=[.!?])\s+(Note\s*\d*:|Note:|Computation of\b|Taxability\b|Particulars\b)', r'\n\n\1', text)

    # 5. Clean up inline whitespace per line
    raw_lines = text.splitlines()
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in raw_lines]

    # 6. Format computation tables if 'Particulars' is detected
    formatted_lines = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.lower() == 'particulars':
            curr_header = '₹'
            i += 1
            if i < n and lines[i].lower() in ['z', 'x', '4', '`', '₹', 'rs.', 'rs']:
                i += 1

            table_rows = []
            while i < n:
                l = lines[i]
                if not l or l.startswith('(') or l.lower().startswith('note') or l.lower().startswith('question'):
                    break
                # Skip OCR noise rows
                if l.lower() in ['ttt', '__—=d_,'] or re.match(r'^[_\—=\-d,\s]+$', l):
                    i += 1
                    continue
                if i + 1 < n and re.match(r'^[₹\s]*[\d,]+(?:\.\d+)?$', lines[i+1]):
                    amt = lines[i+1].replace('₹', '').strip()
                    table_rows.append((l, amt))
                    i += 2
                elif re.search(r'[\d,]{4,}', l):
                    m = re.search(r'^(.*?)\s+([₹\s]*[\d,]+(?:\.\d+)?)$', l)
                    if m:
                        table_rows.append((m.group(1).strip(), m.group(2).replace('₹', '').strip()))
                    else:
                        table_rows.append((l, ''))
                    i += 1
                else:
                    table_rows.append((l, ''))
                    i += 1

            if table_rows:
                formatted_lines.append(f'\n| Particulars | {curr_header} |')
                formatted_lines.append('| :--- | :---: |')
                for p_col, a_col in table_rows:
                    if p_col.strip():
                        formatted_lines.append(f'| {p_col} | {a_col} |')
                formatted_lines.append('\n')
            continue

        # 6. Format sub-questions / list items
        subq_m = re.match(r'^\(([ivxIVX]+|\d+|[a-zA-Z])\)\s*(.*)$', line)
        if subq_m:
            sub_id = subq_m.group(1)
            sub_text = subq_m.group(2).strip()
            if not sub_text and i + 1 < n and not lines[i+1].startswith('(') and lines[i+1].lower() != 'particulars':
                sub_text = lines[i+1].strip()
                i += 1
            formatted_lines.append(f'\n\n- **({sub_id})** {sub_text}')
            i += 1
            continue

        # Detect paragraph transitions
        if re.match(r'^(?:One\s+Mr\.|Mr\.|Mrs\.|In\s+this\s+background|You\s+are\s+required|Compute\b|Determine\b|Examine\b)', line):
            formatted_lines.append(f'\n\n{line}')
            i += 1
            continue

        formatted_lines.append(line)
        i += 1

    # 7. Reconstruct natural paragraph flow
    res = []
    current_para = []
    for l in formatted_lines:
        l_str = l.strip()
        if not l_str:
            if current_para:
                res.append(' '.join(current_para))
                current_para = []
        elif l_str.startswith('|'):
            # Filter out empty or noise table rows like '| TTT | |' or '| | |' or '| __—=d_, | |'
            if re.search(r'\bTTT\b', l_str, re.IGNORECASE) or re.search(r'__—=d_,', l_str):
                continue
            cells = [c.strip() for c in l_str.split('|') if c.strip()]
            if not cells:
                continue
            if not all(re.match(r'^:?-+:?$', c) for c in cells) and all(not re.search(r'[a-zA-Z0-9]', c) for c in cells):
                continue

            if current_para:
                res.append(' '.join(current_para))
                current_para = []
            if res and res[-1].startswith('|'):
                res[-1] += '\n' + l_str
            else:
                res.append(l_str)
        elif l_str.startswith('- **('):
            if current_para:
                res.append(' '.join(current_para))
                current_para = []
            current_para.append(l_str)
        elif re.match(r'^(?:Note\s*\d*:|Note:|Computation of\b|Taxability\b|One\s+Mr\.|Mr\.|Mrs\.|In\s+this\s+background|You\s+are\s+required|Compute\b|Determine\b|Examine\b)', l_str, re.IGNORECASE):
            if current_para:
                res.append(' '.join(current_para))
                current_para = []
            current_para.append(l_str)
        else:
            current_para.append(l_str)
    if current_para:
        res.append(' '.join(current_para))

    final_text = '\n\n'.join(res)
    # Ensure any table rows separated by multiple newlines are tightly collapsed into valid markdown tables
    while re.search(r'(\|[^\n]+\|)\s*\n\s*\n\s*(?=\|[^\n]+\|)', final_text):
        final_text = re.sub(r'(\|[^\n]+\|)\s*\n\s*\n\s*(?=\|[^\n]+\|)', r'\1\n', final_text)
    final_text = re.sub(r'\n{3,}', '\n\n', final_text).strip()
    return final_text

def split_question_and_answer(raw_text):
    """
    Splits sliced text into Question and Answer parts using common book headers,
    and returns sanitized, formatted Markdown for both parts.
    """
    cleaned_lines = []
    for line in raw_text.splitlines():
        l_str = line.strip()
        if not l_str:
            cleaned_lines.append('')
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
        q_raw = cleaned_text[:split_idx].strip()
        ans_raw = cleaned_text[split_idx:].strip()
    else:
        lines = [l for l in cleaned_text.splitlines() if l.strip()]
        pivot = max(1, len(lines) // 3)
        q_raw = "\n".join(lines[:pivot]).strip()
        ans_raw = "\n".join(lines[pivot:]).strip()

    q_formatted = sanitize_and_format_text(q_raw, is_question=True)
    ans_formatted = sanitize_and_format_text(ans_raw, is_question=False)
    return q_formatted, ans_formatted

def extract_question_with_vision(subject: str, chapter_no: int, question_no: int):
    """
    3-Stage Visual Pipeline:
    1. Look up start_page and end_page from PDF index.
    2. Render high-resolution JPEG images of the page range using PyMuPDF.
    3. Pass images to Gemini 3.5 Flash with strict structural instructions to extract
       tables, subheadings, aligned NIL amounts, and separate paragraphs with 100% fidelity.
    Falls back gracefully to text slicing if offline or on error.
    """
    index = build_pdf_index()
    q_entry = None
    for item in index:
        if item["subject"] == subject and item["chapter_no"] == chapter_no and item["question_no"] == question_no:
            q_entry = item
            break

    pdf_file = get_pdf_path(subject)
    if not q_entry or pymupdf is None or not os.path.exists(pdf_file):
        raw_text = get_question_raw_text(subject, chapter_no, question_no)
        if raw_text:
            q_f, a_f = split_question_and_answer(raw_text)
            return {"question_text": q_f, "answer_text": a_f}
        return None

    try:
        from google.genai import types
        from pipeline.key_rotator import rotator

        doc = pymupdf.open(pdf_file)
        start_p = q_entry["start_page"] - 1 # 0-indexed
        end_p = q_entry["end_page"] - 1

        parts = []
        for p in range(start_p, end_p + 1):
            page = doc[p]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes('jpeg')
            parts.append(types.Part.from_bytes(data=img_bytes, mime_type='image/jpeg'))

        prompt = f"""You are an expert CA Final Direct Tax examiner and parser.
Look at the attached page images covering Question {question_no}.

Your task is to extract Question {question_no} and its complete Answer / Solution with 100% fidelity to the visual layout.

MANDATORY RULES:
1. QUESTION TEXT:
   - Extract the complete question narrative.
   - Do NOT prepend "Question {question_no}:" or "Q{question_no}:" to the text.
2. COMPUTATION TABLES:
   - Format all computation tables as GitHub Flavored Markdown tables.
   - Table headers must be | Particulars | ₹ |
   - CRITICAL: Look closely at amounts and columns in the image. Every line item must pair with its exact amount.
   - If an item has 'NIL' as its cost/amount (e.g. Less: Cost of acquisition [Note 2]), put 'NIL' in the amount column (| Less: Cost of acquisition [Note 2] | NIL |), NEVER as an orphan row!
   - Table section subheadings must be bold (e.g. | **1000 Original shares** | | or | **200 Right shares** | |).
   - Multiplication signs must be "×" (e.g. 1000 × ₹ 300, 200 × ₹ 30), NOT "=" or "*".
   - Subtotals and Grand totals must be bold (e.g. | **Capital Gains (A+B+C)** | **2,59,000** |).
   - If there is a second computation table, format it cleanly as a separate table with header above it.
3. NOTES & PARAGRAPHS:
   - Every Note (e.g. Note 1:, Note 2:, Note:) MUST be formatted in its own distinct paragraph separated by blank lines (\\n\\n).
   - Section headers like "Computation of capital gains in the hands of Mr. Q" must be on their own line with blank lines around them.
4. JSON OUTPUT:
   Output ONLY a valid JSON object with no markdown fences, no surrounding commentary:
{{
  "chapter_number": {chapter_no},
  "question_number": {question_no},
  "question_title": "Concise concept title",
  "question_text": "...",
  "answer_text": "..."
}}
"""

        def _call(client):
            return client.models.generate_content(
                model='gemini-3.5-flash',
                contents=parts + [prompt],
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    temperature=0.1
                )
            )

        resp = rotator.execute_with_retry(_call)
        raw = resp.text.strip()
        parsed = json.loads(raw)
        return parsed
    except Exception as e:
        print(f"[VISION EXTRACTOR] Gemini vision call encountered: {e}. Falling back to text slicing...")
        raw_text = get_question_raw_text(subject, chapter_no, question_no)
        if raw_text:
            q_f, a_f = split_question_and_answer(raw_text)
            return {"question_text": q_f, "answer_text": a_f}
        return None

if __name__ == '__main__':
    idx = build_pdf_index(force=True)
    q11_text = get_question_raw_text('DT', 1, 11)
    if q11_text:
        q, ans = split_question_and_answer(q11_text)
        print(f"Sample Q11 sliced successfully. Lengths: Q={len(q)}, Ans={len(ans)}")
