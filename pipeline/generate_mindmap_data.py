import os
import sys
import json
import re
import time
import argparse
import shutil
from typing import Dict, Any, List, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import rotator
from google.genai import types

DEFAULT_MODEL = "gemini-3-flash-preview"
MODEL_FALLBACKS = [
    "gemini-3-flash-preview",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest"
]

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROVISIONS_PATH = os.path.join(DATA_DIR, "provisions.json")
STORYBOARDS_PATH = os.path.join(DATA_DIR, "ppt_storyboards.json")
QNA_PATH = os.path.join(DATA_DIR, "extracted_qna.json")
MINDMAPS_PATH = os.path.join(DATA_DIR, "mindmaps.json")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
ALIGNMENTS_PATH = os.path.join(DATA_DIR, "audio_alignments.json")

QUESTION_TO_MINDMAP = {
    "1": "q1",
    "2": "q1",
    "3": "q1",
    "4": "q4",
    "5": "q5",
    "6": "q6",
    "7": "q7",
    "8": "q8",
    "9": "q9",
    "10": "q10"
}

TOPIC_KEYS = ["q1", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
ALLOWED_ICONS = {"scales", "shield", "calculator", "percent", "cap", "warning", "gear", "check", "user", "building", "rupee"}
ALLOWED_POINT_TYPES = {"rule", "rate", "levy", "condition", "formula", "example", "trap", "authority", "table"}

def clean_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

def extract_highlights_from_text(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    # Amounts, percentages, section citations
    patterns = re.findall(
        r'(?:₹\s*[\d,]+(?:\.\d+)?(?:\s*(?:Cr|Crores|Lakhs|L))?|\b\d+(?:\.\d+)?%\b|Section\s+\w+(?:\(\w+\))*|Sec\.\s*\w+(?:\(\w+\))*|\bAY\s+\d{4}-\d{2}\b|\bPY\s+\d{4}-\d{2}\b)',
        text,
        re.IGNORECASE
    )
    res = []
    seen = set()
    for p in patterns:
        p_strip = p.strip()
        if p_strip.lower() not in seen:
            seen.add(p_strip.lower())
            res.append(p_strip)
    return res

def validate_numeric_in_source(topic_data: Dict[str, Any], source_text: str) -> Tuple[bool, List[str]]:
    normalized_source = source_text.lower().replace(",", "")
    warnings = []
    for b in topic_data.get("branches", []):
        for pt in b.get("points", []):
            texts = [pt.get("title", ""), pt.get("body", "")]
            if "highlights" in pt:
                texts.extend(pt["highlights"])
            if "table_data" in pt and pt["table_data"]:
                for row in pt["table_data"].get("rows", []):
                    texts.extend([str(c) for c in row])
            if "example_calc" in pt and pt["example_calc"]:
                texts.extend(pt["example_calc"].get("steps", []))
            for t in texts:
                patterns = re.findall(r'(?:₹\s*[\d,]+(?:\.\d+)?(?:\s*(?:Cr|Crores|Lakhs|L))?|\b\d+%\b|\b\d+(?:,\d+)*(?:\.\d+)?\b)', str(t))
                for token in patterns:
                    token_norm = token.replace("₹", "").replace(",", "").strip().lower()
                    if token_norm in {"1", "2", "3", "4", "0"}:
                        continue
                    if token_norm and token_norm not in normalized_source:
                        warnings.append(f"Point '{pt.get('id')}' contains '{token}' not clearly found in source.")
    return len(warnings) > 0, warnings

def get_audio_sentence_alignments(topic_key: str, audio_path: str, storyboard: Dict[str, Any]) -> List[Dict[str, Any]]:
    alignments = {}
    if os.path.exists(ALIGNMENTS_PATH):
        try:
            with open(ALIGNMENTS_PATH, "r", encoding="utf-8") as f:
                alignments = json.load(f)
        except Exception:
            alignments = {}

    if topic_key in alignments and len(alignments[topic_key]) >= 4:
        return alignments[topic_key]

    print(f"[{topic_key}] Aligning spoken audio sentences via Gemini audio analysis...", flush=True)
    if os.path.exists(audio_path):
        try:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            
            client = rotator.get_client()
            prompt = """
Listen carefully to this Malayalam audio file.
Provide the exact start and end timestamps in seconds [start, end] for every distinct spoken Malayalam sentence/clause in the audio.
Return a JSON array of objects:
[
  {"start": 0.0, "end": 3.5, "text": "spoken Malayalam sentence"},
  ...
]
Timestamps must be non-overlapping, strictly increasing, and cover the audio from 0.0s to the end.
"""
            resp = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"),
                    prompt
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            cleaned = clean_json_text(resp.text)
            parsed = json.loads(cleaned)
            if isinstance(parsed, list) and len(parsed) >= 4:
                alignments[topic_key] = parsed
                with open(ALIGNMENTS_PATH, "w", encoding="utf-8") as f:
                    json.dump(alignments, f, ensure_ascii=False, indent=2)
                print(f"[{topic_key}] Successfully aligned {len(parsed)} audio sentences.")
                return parsed
        except Exception as e:
            print(f"[{topic_key}] Gemini audio alignment error: {e}. Falling back to storyboard segmentation.", flush=True)

    # Fallback: storyboard slide narration sentence splitting
    fallback = []
    slides = storyboard.get("slides", [])
    for s in slides:
        st0 = float(s.get("t0", 0.0))
        st1 = float(s.get("t1", 0.0))
        narr = s.get("malayalam_narration", "").strip()
        raw_sents = re.split(r'(?<=[^\d])\.|\.\s+(?=[A-Za-z\u0D00-\u0D7F])', narr)
        sents = [st.strip() for st in raw_sents if st.strip()]
        if not sents:
            sents = [s.get("slide_title", "")]
        span = (st1 - st0) / len(sents)
        for si, sent in enumerate(sents):
            fallback.append({
                "start": round(st0 + si * span, 2),
                "end": round(st0 + (si + 1) * span if si < len(sents) - 1 else st1, 2),
                "text": sent
            })
    
    alignments[topic_key] = fallback
    with open(ALIGNMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(alignments, f, ensure_ascii=False, indent=2)
    return fallback

def snap_authoritative_timestamps(
    mindmap_dict: Dict[str, Any],
    storyboard: Dict[str, Any],
    prov: Dict[str, Any],
    aligned_sentences: List[Dict[str, Any]]
) -> Tuple[Dict[str, Any], bool]:
    total_dur = float(prov.get("duration_seconds") or prov.get("dur") or 80.0)
    mindmap_dict["total_duration"] = total_dur
    mindmap_dict["audio_file"] = prov.get("audio_file", f"{mindmap_dict.get('topic_id', 'q1')}.mp3")
    
    slides = storyboard.get("slides", [])
    if len(slides) != 4:
        raise ValueError(f"Storyboard must have 4 slides, found {len(slides)}")
    
    b1_t1 = float(slides[0].get("t1", 20.0))
    mindmap_dict["root"]["t0"] = 0.0
    mindmap_dict["root"]["t1"] = round(min(5.0, b1_t1), 2)
    
    branches = mindmap_dict.get("branches", [])
    if isinstance(branches, dict):
        branches = list(branches.values())
        mindmap_dict["branches"] = branches
    
    review_needed = False
    
    for bi, (b, s) in enumerate(zip(branches, slides)):
        st0 = float(s.get("t0", 0.0))
        st1 = float(s.get("t1", 0.0))
        if bi == 3:
            st1 = total_dur
            
        b["t0"] = round(st0, 2)
        b["t1"] = round(st1, 2)
        
        # Ensure icon is valid
        if b.get("icon") not in ALLOWED_ICONS:
            default_branch_icons = ["shield", "scales", "calculator", "warning"]
            b["icon"] = default_branch_icons[bi % len(default_branch_icons)]
            
        if not b.get("badge"):
            b["badge"] = s.get("section_badge") or f"§ Part {bi+1}"
            
        # Standardize points
        points = b.get("points", [])
        if not points and "nodes" in b:
            # Flatten legacy nodes
            for n in b.get("nodes", []):
                for p_item in n.get("points", []):
                    if "title" not in p_item:
                        p_item["title"] = p_item.get("text", "")[:40]
                    if "body" not in p_item:
                        p_item["body"] = p_item.get("text", "")
                    points.append(p_item)
            b["points"] = points

        # Get aligned sentences falling within this slide range [st0, st1]
        slide_sents = [sent for sent in aligned_sentences if (sent["start"] >= st0 - 1.0 and sent["start"] < st1 - 0.5)]
        if not slide_sents:
            slide_sents = [{"start": st0, "end": st1, "text": s.get("malayalam_narration", "")}]
            
        # Partition points into spoken vs reference
        spoken_pts = []
        ref_pts = []
        for pt in points:
            # Normalize icon and highlights
            if pt.get("icon") not in ALLOWED_ICONS:
                type_icon_map = {
                    "rule": "shield", "rate": "percent", "levy": "rupee",
                    "condition": "scales", "formula": "calculator", "example": "cap",
                    "trap": "warning", "authority": "building", "table": "scales"
                }
                pt["icon"] = type_icon_map.get(pt.get("type"), "check")
                
            if "body" not in pt and "text" in pt:
                pt["body"] = pt["text"]
            if "title" not in pt:
                pt["title"] = pt.get("body", "")[:35]
                
            if not pt.get("highlights"):
                pt["highlights"] = extract_highlights_from_text(pt.get("body", "") + " " + pt.get("title", ""))
                
            is_spoken = pt.get("spoken") is True or (pt.get("reference") is not True and pt.get("t0") is not None)
            if is_spoken:
                spoken_pts.append(pt)
            else:
                ref_pts.append(pt)
        
        if not spoken_pts:
            take_spoken = min(len(points), len(slide_sents), 3)
            spoken_pts = points[:take_spoken]
            ref_pts = points[take_spoken:]

        num_spk = len(spoken_pts)
        num_sents = len(slide_sents)
        
        # Check monotonic timestamps
        valid_existing = True
        for pi, pt in enumerate(spoken_pts):
            pt0 = pt.get("t0")
            pt1 = pt.get("t1")
            if pt0 is None or pt1 is None or float(pt0) >= float(pt1) or float(pt0) < st0 - 0.25 or float(pt1) > st1 + 0.25:
                valid_existing = False
                break
            if pi > 0 and float(pt0) < float(spoken_pts[pi-1].get("t1", 0)) - 0.05:
                valid_existing = False
                break
        
        # Reserve the end portion of the branch for flow_summary
        flow_reserve = 0.20 * (st1 - st0)
        cards_end_t = st1 - flow_reserve if b.get("flow_summary") else st1
        
        if valid_existing and num_spk > 0:
            for pi, pt in enumerate(spoken_pts):
                pt["spoken"] = True
                pt["reference"] = False
                pt["t0"] = round(float(pt["t0"]), 2)
                pt["t1"] = round(min(cards_end_t, float(pt["t1"])), 2)
                if pt["t0"] >= pt["t1"]:
                    pt["t1"] = round(pt["t0"] + 2.0, 2)
                if not pt.get("voice_sync_text"):
                    pt["voice_sync_text"] = slide_sents[min(pi, num_sents - 1)]["text"]
        else:
            review_needed = True
            span = (cards_end_t - st0) / max(1, num_spk)
            cur_t = st0
            for pi, pt in enumerate(spoken_pts):
                pt["spoken"] = True
                pt["reference"] = False
                pt["t0"] = round(cur_t, 2)
                pt["t1"] = round(cur_t + span if pi < num_spk - 1 else cards_end_t, 2)
                cur_t += span
                pt["voice_sync_text"] = slide_sents[min(pi, num_sents - 1)]["text"]

        for pt in ref_pts:
            pt["spoken"] = False
            pt["reference"] = True
            pt["t0"] = None
            pt["t1"] = None
            pt["voice_sync_text"] = None

        b["points"] = spoken_pts + ref_pts

        # Snap flow summary steps
        flow_steps = b.get("flow_summary", [])
        if not flow_steps or len(flow_steps) < 3:
            # Synthesize standard calculation / decision flow steps
            step_templates = [
                {"label": "1. Verify Assessee Scope", "sub": "Residential & Legal Status", "icon": "scales"},
                {"label": "2. Determine Slabs/Rates", "sub": "Category Exemption Limit", "icon": "calculator"},
                {"label": "3. Compute Base Tax", "sub": "Progressive Brackets", "icon": "percent"},
                {"label": "4. Apply Relief & 4% Cess", "sub": "Rebate 87A + HEC", "icon": "rupee"}
            ]
            flow_steps = step_templates
            b["flow_summary"] = flow_steps

        flow_t0 = cards_end_t
        flow_span = (st1 - flow_t0) / len(flow_steps)
        cur_ft = flow_t0
        for fi, fs in enumerate(flow_steps):
            if fs.get("icon") not in ALLOWED_ICONS:
                fs["icon"] = "gear" if fi == 0 else "check"
            fs["t0"] = round(cur_ft, 2)
            fs["t1"] = round(cur_ft + flow_span if fi < len(flow_steps) - 1 else st1, 2)
            cur_ft += flow_span

    return mindmap_dict, review_needed

def build_gemini_prompt(
    topic_key: str,
    prov: Dict[str, Any],
    storyboard: Dict[str, Any],
    qna_item: Optional[Dict[str, Any]],
    aligned_sentences: List[Dict[str, Any]]
) -> str:
    doctrine = prov.get("core_principle") or prov.get("topic_title") or ""
    sections = ", ".join(prov.get("statutory_sections", []))
    raw_md = prov.get("provision_presentation_markdown", "")
    q_text = qna_item.get("question_text", "") if qna_item else ""
    a_text = qna_item.get("answer_text", "") if qna_item else ""
    
    slides_summary = []
    for s in storyboard.get("slides", []):
        st0, st1 = s.get("t0"), s.get("t1")
        matching_sents = [sent for sent in aligned_sentences if sent["start"] >= st0 - 0.5 and sent["start"] < st1]
        sent_bullet = "\n    ".join([f"[{sent['start']}s - {sent['end']}s]: \"{sent['text']}\"" for sent in matching_sents[:6]])
        slides_summary.append(
            f"Branch {s.get('slide_number')} [{st0}s - {st1}s]: '{s.get('slide_title')}'\n"
            f"  Spoken Audio Sentences ({len(matching_sents)} sentences):\n    {sent_bullet}"
        )
    slides_str = "\n\n".join(slides_summary)
    
    prompt = f"""You are a senior statutory Direct Tax expert and visual infographic architect for CA / CMA Final students.
Generate a high-yield, deeply detailed Infographic Mind Map decision tree for topic {topic_key}.
Every section must render as an Infographic Block with:
1. Section Title Pill (dark navy rounded pill, title max 6 words, badge e.g. '§ 115BAC(6)', icon).
2. Point Cards Grid: 2 to 4 cards side-by-side with overlapping SVG icon badge, colored header ribbon, 16px body, highlighted numbers/rates/sections.
3. Full tables for slabs/surcharges (never summarized into a range!).
4. Worked Example calculation panel in Branch 3.
5. Crucial Exam Traps in Branch 4 (Mistake vs Statutory Rule).
6. Flow Summary Row: 3 to 5 small step boxes left to right with arrows between them illustrating computation order.

TOPIC ID: {topic_key}
STATUTORY SECTIONS: {sections}
DOCTRINE: {doctrine}

SOURCE PROVISION LAW & STATUTORY TABLES:
{raw_md}

EXAM QUESTION & ICAI SOLUTION CONTEXT:
Question: {q_text[:350]}
Solution: {a_text[:500]}

AUDIO BRANCHES & TIMESTAMPED SPOKEN MALAYALAM SENTENCES:
{slides_str}

ALLOWED ICONS (MUST BE EXACT KEYS ONLY):
["scales", "shield", "calculator", "percent", "cap", "warning", "gear", "check", "user", "building", "rupee"]

ALLOWED POINT TYPES:
["rule", "rate", "levy", "condition", "formula", "example", "trap", "authority", "table"]

SCHEMA TEMPLATE:
{{
  "topic_id": "{topic_key}",
  "section_code": "{sections}",
  "doctrine": "{doctrine}",
  "total_duration": 80.0,
  "audio_file": "{prov.get('audio_file', topic_key + '.mp3')}",
  "review_flag": false,
  "root": {{
    "id": "root",
    "title": "Short Doctrine Title",
    "badge": "§ Section Code",
    "summary": "",
    "t0": 0.0,
    "t1": 5.0
  }},
  "branches": [
    {{
      "branch_id": "b1_applicability",
      "branch_title": "Applicability Scope",
      "badge": "§ 115BAC(6)",
      "icon": "shield",
      "t0": 0.0,
      "t1": 20.35,
      "points": [
        {{
          "id": "p_b1_1",
          "type": "rule",
          "icon": "shield",
          "title": "Opt-Out Option Required",
          "body": "Assessee must specifically exercise the option to shift out of the default regime under Section 115BAC(6) to use these rates.",
          "highlights": ["Section 115BAC(6)"],
          "table_data": null,
          "example_calc": null,
          "trap_data": null,
          "spoken": true,
          "reference": false,
          "t0": 0.0,
          "t1": 6.0,
          "voice_sync_text": "Malayalam audio sentence"
        }},
        {{
          "id": "p_b1_2",
          "type": "condition",
          "icon": "scales",
          "title": "Basic Exemption Slabs",
          "body": "Basic Exemption Limit depends on the age and residential status: Resident < 60 gets ₹ 2,50,000; Senior Citizens get ₹ 3,00,000; Super Seniors get ₹ 5,00,000.",
          "highlights": ["₹ 2,50,000", "₹ 3,00,000", "₹ 5,00,000"],
          "spoken": true,
          "reference": false,
          "t0": 6.0,
          "t1": 13.0,
          "voice_sync_text": "Malayalam audio sentence"
        }}
      ],
      "flow_summary": [
        {{ "label": "Check Status", "sub": "Individual / HUF", "icon": "user", "t0": 14.0, "t1": 16.0 }},
        {{ "label": "Exercise Opt-Out", "sub": "Section 115BAC(6)", "icon": "shield", "t0": 16.0, "t1": 18.0 }},
        {{ "label": "Determine Exemption", "sub": "₹ 2.5L / ₹ 3L / ₹ 5L", "icon": "scales", "t0": 18.0, "t1": 20.35 }}
      ]
    }},
    {{
      "branch_id": "b2_slabs",
      "branch_title": "Tax Rates & Thresholds Matrix",
      "badge": "§ Finance Act",
      "icon": "calculator",
      "t0": 20.75,
      "t1": 46.6,
      "points": [
        {{
          "id": "p_b2_1",
          "type": "rate",
          "icon": "percent",
          "title": "Progressive Brackets",
          "body": "Income exceeding basic exemption is taxed progressively at 5%, 20%, and 30%.",
          "highlights": ["5%", "20%", "30%"],
          "spoken": true,
          "reference": false,
          "t0": 21.0,
          "t1": 31.0,
          "voice_sync_text": "Malayalam audio sentence"
        }},
        {{
          "id": "p_b2_2",
          "type": "table",
          "icon": "scales",
          "title": "Complete Slab Table",
          "body": "Full statutory slab table for Resident Individuals < 60 Years and Non-Residents.",
          "highlights": ["₹ 2,50,000", "5%", "20%", "30%"],
          "spoken": false,
          "reference": true,
          "t0": null,
          "t1": null,
          "voice_sync_text": null,
          "table_data": {{
            "title": "Category 1: Resident < 60 Years & Non-Residents",
            "headers": ["Income Bracket", "Rate", "Tax on Bracket"],
            "rows": [
              ["Up to ₹ 2,50,000", "Nil", "₹ 0"],
              ["₹ 2,50,001 – ₹ 5,00,000", "5%", "₹ 12,500"],
              ["₹ 5,00,001 – ₹ 10,00,000", "20%", "₹ 1,00,000"],
              ["Above ₹ 10,00,000", "30%", "Balance × 30%"]
            ]
          }}
        }}
      ],
      "flow_summary": [
        {{ "label": "Up to Exemption", "sub": "Nil Tax", "icon": "check", "t0": 40.0, "t1": 42.0 }},
        {{ "label": "Next ₹ 2.5L", "sub": "Taxed @ 5%", "icon": "percent", "t0": 42.0, "t1": 44.0 }},
        {{ "label": "Next ₹ 5L", "sub": "Taxed @ 20%", "icon": "calculator", "t0": 44.0, "t1": 46.6 }}
      ]
    }},
    {{
      "branch_id": "b3_calc",
      "branch_title": "Additional Levies & Relief",
      "badge": "§ 87A & HEC",
      "icon": "rupee",
      "t0": 47.0,
      "t1": 66.85,
      "points": [
        {{
          "id": "p_b3_1",
          "type": "rule",
          "icon": "shield",
          "title": "Rebate under Section 87A",
          "body": "Resident Individual with Total Income not exceeding ₹ 5,00,000 receives 100% tax rebate up to ₹ 12,500.",
          "highlights": ["₹ 5,00,000", "₹ 12,500", "Section 87A"],
          "spoken": true,
          "reference": false,
          "t0": 47.0,
          "t1": 56.0,
          "voice_sync_text": "Malayalam audio sentence"
        }},
        {{
          "id": "p_b3_2",
          "type": "levy",
          "icon": "percent",
          "title": "Health & Education Cess",
          "body": "Mandatory 4% Health and Education Cess is calculated on aggregate tax and surcharge after deducting Section 87A rebate.",
          "highlights": ["4%", "HEC"],
          "spoken": true,
          "reference": false,
          "t0": 56.0,
          "t1": 62.0,
          "voice_sync_text": "Malayalam audio sentence"
        }},
        {{
          "id": "p_b3_3",
          "type": "example",
          "icon": "cap",
          "title": "Worked Computation Example",
          "body": "Step-by-step statutory calculation for Total Income ₹ 16,00,000.",
          "highlights": ["₹ 16,00,000", "₹ 3,04,200"],
          "spoken": false,
          "reference": true,
          "t0": null,
          "t1": null,
          "voice_sync_text": null,
          "example_calc": {{
            "title": "Computation: Mr. Arjun (Age 52), TI ₹ 16,00,000",
            "inputs": "Resident | Age 52 | TI ₹ 16,00,000",
            "steps": [
              "Up to ₹ 2,50,000: Nil",
              "₹ 2,50,001 – ₹ 5,00,000 @ 5%: ₹ 12,500",
              "₹ 5,00,001 – ₹ 10,00,000 @ 20%: ₹ 1,00,000",
              "Above ₹ 10,00,000 @ 30%: ₹ 1,80,000",
              "Base Tax = ₹ 2,92,500 (No 87A rebate as TI > ₹ 5L)",
              "Add: 4% HEC = ₹ 11,700",
              "Total Tax Payable = ₹ 3,04,200"
            ]
          }}
        }}
      ],
      "flow_summary": [
        {{ "label": "Compute Slab Tax", "sub": "Step 1", "icon": "calculator", "t0": 62.0, "t1": 63.5 }},
        {{ "label": "Less: Rebate 87A", "sub": "Max ₹ 12,500", "icon": "shield", "t0": 63.5, "t1": 65.0 }},
        {{ "label": "Add: 4% HEC", "sub": "Final Tax", "icon": "rupee", "t0": 65.0, "t1": 66.85 }}
      ]
    }},
    {{
      "branch_id": "b4_pitfall",
      "branch_title": "Crucial Exam Traps",
      "badge": "§ Negative Marking",
      "icon": "warning",
      "t0": 67.25,
      "t1": 91.06,
      "points": [
        {{
          "id": "p_b4_1",
          "type": "trap",
          "icon": "warning",
          "title": "Non-Resident Senior Citizens",
          "body": "Higher basic exemption of ₹ 3L or ₹ 5L applies ONLY to Resident individuals. Non-Residents get only ₹ 2.5L exemption regardless of age.",
          "highlights": ["Resident", "Non-Residents", "₹ 2.5L", "₹ 3L"],
          "spoken": true,
          "reference": false,
          "t0": 73.0,
          "t1": 86.0,
          "voice_sync_text": "Malayalam audio sentence"
        }},
        {{
          "id": "p_b4_2",
          "type": "trap",
          "icon": "warning",
          "title": "Cess Calculation Sequence",
          "body": "Section 87A rebate must be deducted first. 4% HEC is calculated only on the net tax liability.",
          "highlights": ["Section 87A", "4% HEC"],
          "spoken": false,
          "reference": true,
          "t0": null,
          "t1": null,
          "voice_sync_text": null,
          "trap_data": {{
            "mistake": "Adding 4% Health & Education Cess before deducting Section 87A rebate.",
            "statutory_rule": "Cess is levied on net tax liability AFTER subtracting Section 87A rebate and surcharge."
          }}
        }}
      ],
      "flow_summary": [
        {{ "label": "Check Residency", "sub": "Resident vs NR", "icon": "user", "t0": 86.0, "t1": 88.0 }},
        {{ "label": "Exemption Cap", "sub": "NR capped @ ₹ 2.5L", "icon": "scales", "t0": 88.0, "t1": 89.5 }},
        {{ "label": "Avoid Cess Order Trap", "sub": "HEC on Net Tax", "icon": "warning", "t0": 89.5, "t1": 91.06 }}
      ]
    }}
  ]
}}
"""
    return prompt

def generate_mindmap_for_topic(
    topic_key: str,
    prov: Dict[str, Any],
    storyboard: Dict[str, Any],
    qna_item: Optional[Dict[str, Any]],
    model_name: str,
    dry_run: bool = False
) -> Tuple[Optional[Dict[str, Any]], int, bool, str]:
    if dry_run:
        print(f"[DRY RUN] Would generate mindmap for {topic_key}")
        return None, 0, False, model_name
        
    audio_path = os.path.join(AUDIO_DIR, prov.get("audio_file", f"{topic_key}.mp3"))
    aligned_sentences = get_audio_sentence_alignments(topic_key, audio_path, storyboard)
    
    prompt = build_gemini_prompt(topic_key, prov, storyboard, qna_item, aligned_sentences)
    source_corpus = (
        prov.get("provision_presentation_markdown", "") + " " +
        (qna_item.get("question_text", "") if qna_item else "") + " " +
        (qna_item.get("answer_text", "") if qna_item else "")
    )
    
    active_model = model_name
    max_retries = 3
    retries = 0
    feedback = ""
    
    while retries < max_retries:
        models_to_try = [active_model] + [m for m in MODEL_FALLBACKS if m != active_model]
        resp_text = None
        
        for m in models_to_try:
            try:
                client = rotator.get_client()
                full_prompt = prompt if not feedback else f"{prompt}\n\nIMPORTANT PREVIOUS ATTEMPT FIX REQUIRED:\n{feedback}"
                resp = client.models.generate_content(
                    model=m,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.15,
                        response_mime_type="application/json",
                        http_options={"timeout": 90000}
                    )
                )
                if resp.text:
                    resp_text = resp.text
                    active_model = m
                    break
            except Exception as e:
                print(f"[{topic_key}] Model {m} error: {str(e)[:100]}", flush=True)
                time.sleep(1)
                
        if not resp_text:
            retries += 1
            feedback = "Empty or failed response from model."
            continue
            
        try:
            cleaned = clean_json_text(resp_text)
            parsed = json.loads(cleaned)
        except Exception as je:
            retries += 1
            feedback = f"JSON parse error: {je}. Return strictly valid JSON."
            continue
            
        try:
            snapped, snap_rev = snap_authoritative_timestamps(parsed, storyboard, prov, aligned_sentences)
        except Exception as se:
            retries += 1
            feedback = f"Timestamp snapping error: {se}."
            continue
            
        num_rev, warnings = validate_numeric_in_source(snapped, source_corpus)
        final_review = snap_rev or num_rev
        snapped["review_flag"] = final_review
        
        if num_rev:
            for w in warnings:
                print(f"[{topic_key}] WARNING: {w}", flush=True)
                
        return snapped, retries, final_review, active_model
        
    return None, retries, False, active_model

def main():
    parser = argparse.ArgumentParser(description="Generate AI Infographic Mind Maps for TaxMaster")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model name")
    parser.add_argument("--only", help="Run only specific topic, e.g. q4")
    parser.add_argument("--force", action="store_true", help="Force regenerate existing topics")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without calling API")
    args = parser.parse_args()
    
    print("=======================================================")
    print("TAXMASTER INFOGRAPHIC MIND MAP GENERATION PIPELINE")
    print(f"Model: {args.model} (Fallbacks: {MODEL_FALLBACKS})")
    print(f"Target file: {MINDMAPS_PATH}")
    print("=======================================================\n")
    
    with open(PROVISIONS_PATH, "r", encoding="utf-8") as f:
        provisions_list = json.load(f)
    prov_by_qn = {p["question_number"]: p for p in provisions_list}
    
    with open(STORYBOARDS_PATH, "r", encoding="utf-8") as f:
        storyboards = json.load(f)
        
    qna_list = []
    if os.path.exists(QNA_PATH):
        with open(QNA_PATH, "r", encoding="utf-8") as f:
            qna_list = json.load(f)
    qna_by_qn = {q.get("question_number"): q for q in qna_list}
    
    existing_mindmaps = {}
    if os.path.exists(MINDMAPS_PATH):
        try:
            with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
                existing_mindmaps = json.load(f)
        except Exception:
            existing_mindmaps = {}
            
    target_topics = TOPIC_KEYS
    if args.only:
        target_topics = [args.only]
        
    results_summary = []
    updated_mindmaps = dict(existing_mindmaps)
    updated_mindmaps["question_to_mindmap"] = QUESTION_TO_MINDMAP
    
    for t_key in target_topics:
        qn = int(t_key.replace("q", ""))
        prov = prov_by_qn.get(qn)
        storyboard = storyboards.get(t_key)
        qna_item = qna_by_qn.get(qn)
        
        if not prov or not storyboard:
            print(f"Skipping {t_key}: Missing provision or storyboard data.")
            continue
            
        print(f"Generating Infographic mind map for {t_key} ({prov.get('core_principle')[:40]}...)...", flush=True)
        data, retries, rev_flag, used_model = generate_mindmap_for_topic(
            t_key, prov, storyboard, qna_item, args.model, args.dry_run
        )
        
        if data:
            updated_mindmaps[t_key] = data
            results_summary.append({
                "topic": t_key, "status": "SUCCESS", "retries": retries,
                "review_flag": rev_flag, "model": used_model
            })
            print(f"[{t_key}] SUCCESS (Retries: {retries}, Review Flag: {rev_flag}, Model: {used_model})", flush=True)
            
            if not args.dry_run:
                temp_path = MINDMAPS_PATH + ".tmp"
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(updated_mindmaps, f, ensure_ascii=False, indent=2)
                shutil.move(temp_path, MINDMAPS_PATH)
        else:
            status = "DRY_RUN" if args.dry_run else "FAILED"
            results_summary.append({
                "topic": t_key, "status": status, "retries": retries,
                "review_flag": False, "model": used_model
            })
            print(f"[{t_key}] {status}", flush=True)

    if not args.dry_run and os.path.exists(MINDMAPS_PATH):
        backup_path = MINDMAPS_PATH + ".bak"
        shutil.copyfile(MINDMAPS_PATH, backup_path)
        print(f"\nFinal mindmaps file saved at {MINDMAPS_PATH} (backup at {backup_path})", flush=True)
        
    print("\n" + "="*75, flush=True)
    print(f"{'Topic':<8} | {'Status':<16} | {'Retries':<8} | {'Review Flag':<12} | {'Model Used'}", flush=True)
    print("="*75, flush=True)
    for r in results_summary:
        print(f"{r['topic']:<8} | {r['status']:<16} | {r['retries']:<8} | {str(r['review_flag']):<12} | {r['model']}", flush=True)
    print("="*75, flush=True)

if __name__ == "__main__":
    main()
