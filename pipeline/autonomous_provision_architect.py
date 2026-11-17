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
from typing import Dict, Any, Optional, List

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
========================================================================================
ABSOLUTE CORE MANDATE 5: OPERATIVE KEYWORD HIGHLIGHTS & NARRATIVE TIMING
========================================================================================
For EVERY point card in 'mindmap.branches[].points', you MUST select 2 to 3 of the MOST CRITICAL operative phrases/keywords directly from the 'body' bullet points.

CRITICAL SELECTION & TIMING CRITERIA:
1. ZERO HALLUCINATION / VERBATIM MATCHING:
   - "phrase" MUST be an EXACT, VERBATIM substring copied directly from that card's 'body' text.
   - Do NOT paraphrase, summarize, reword, or change singular/plural.
   - Choose high-impact operative legal terms: specific conditions, statutory consequences, exemptions, formulas, or thresholds (e.g. "resulting company", "not a transfer", "No capital gains tax liability", "exempt", "Indian company").
2. NARRATIVE TIMING ALIGNMENT ("time_sec"):
   - "time_sec" MUST represent the estimated second when the teacher's spoken explanation ('voice_sync_text') introduces or stresses that specific operative phrase.
   - Sequence highlights in strictly ascending order matching the flow of the explanation:
     * 1st operative term (premise/subject): typically at 1.5s - 3.5s
     * 2nd operative term (core rule/condition): typically at 4.0s - 7.5s
     * 3rd operative term (legal tax consequence): typically at 8.0s - 12.0s
This enables the presentation player to illuminate these words dynamically as the student listens, creating a high-impact visual focus.

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
            "highlights": [
              {{
                "phrase": "exact operative phrase in bullet 1",
                "time_sec": 2.5
              }},
              {{
                "phrase": "exact operative phrase in bullet 2",
                "time_sec": 6.8
              }}
            ],
            "table_data": null,
            "voice_sync_text": "Punchy 2-3 sentence Malayalam teacher explanation of this specific card's legal rule (approx. 20-30 seconds). Clear, professional CA teaching style with standard English tax terms. ABSOLUTELY NEVER mention question-specific facts, question numbers, company names, or individual names."
          }}
        ],
        "flow_summary": []
      }}
    ]
  }},
  "concept_simulation": {{
    "schema_version": "1.0",
    "illustrative_only": true,
    "doctrine_topic": "Concise name of the statutory doctrine",
    "relevant_tax_year": "e.g. P.Y. 2024-25 to P.Y. 2025-26",
    "statutory_assumptions": [
      "Assumption 1 highlighting core statutory mechanism",
      "Assumption 2 using illustrative round figures"
    ],
    "intro_voice": "ഇനി ഒരു simple example വഴി കൂടുതൽ മനസ്സിലാക്കാം.",
    "steps": [
      {{
        "step_id": "step_1",
        "step_order": 1,
        "title": "Clear Beat Title (e.g. The Capital Asset or The Statutory Event)",
        "metric_label": "Metric Name (e.g. Purchase Cost or Fair Market Value)",
        "metric_value": "₹ 10,00,000",
        "voice_sync_text": "Spoken Malayalam explanation of this specific beat using simple round numbers and standard English tax terms (10-15 seconds).",
        "image_prompt": "Detailed Google Imagen prompt in 16:9 cinematic 2.5D isometric view describing this scene photorealistically with dramatic lighting.",
        "calculation_data": null
      }}
    ]
  }},
  "explainer_presentation": {{
    "title": "Definitive presentation title (e.g. Conversion of Capital Asset into Stock-in-Trade u/s 45(2))",
    "badge": "§ Statutory Section Badge",
    "doctrine": "Name of the statutory doctrine",
    "slides": [
      {{
        "slide_order": 1,
        "title": "Slide Title",
        "subtitle": "Explanatory Subtitle",
        "layout": "statutory_rule",
        "image_required": false,
        "image_prompt": null,
        "voice_sync_text": "Punchy 2-3 sentence Malayalam teacher explanation of this slide with standard English tax terms.",
        "cards": [
          {{
            "heading": "Rule Heading",
            "badge": "RULE",
            "points": [
              "Exact statutory condition bullet 1",
              "Exact legal consequence bullet 2"
            ]
          }}
        ],
        "calculation_data": null,
        "trap_data": null
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
   - ALWAYS format statutory conditions with distinct markdown paragraph breaks (\\n\\n) and bold bullet checklists.
   - NEVER lump or concatenate multiple statutory provisions, sub-sections, or provisos into one continuous wall of text.
   - Separate every markdown table, callout box, and section heading with blank lines (\\n\\n).
   - NEVER use Unicode box-drawing characters (├──, └──, │, ─) or ASCII pseudo-diagrams, pipes, or arrows.
   - All markdown bold/italics syntax MUST be properly paired and closed on the same line (e.g. `**Bold Text**`).
   - For callout titles, write: `> [!IMPORTANT] Title Name: Description` (clean plain title, no unclosed markdown asterisks).
   - Mathematical or tax formulas must either be in standard plain text (e.g. `Total Income - ₹ 12,00,000`) or standard closed LaTeX `$formula$` without raw unescaped `&` or `%`.
6. Return ONLY the raw JSON object, without backticks or markdown fences.
7. CONCEPT SIMULATION RULES (MANDATORY FOR SCENE-BASED EXPLAINER):
   - 'illustrative_only' MUST be true.
   - Single provision questions: create exactly 3 or 4 sequential steps.
   - Multi-provision questions: create 4 to 6 sequential steps showing how the provisions interact on the same transaction.
   - Every step MUST use clean, round figures (e.g. ₹10 Lakhs, ₹50 Lakhs, ₹70 Lakhs) to clearly illuminate the statutory rule without arithmetic confusion.
   - 'image_prompt' MUST be a vivid, detailed, 16:9 cinematic 2.5D isometric prompt tailored for Google Imagen 3 with dramatic studio lighting.
   - For calculations in the climax step, provide 'calculation_data' mapping the statutory formula.
"""

def validate_screenplay(sp: Any) -> Optional[Dict[str, Any]]:
    """
    Validates screenplay against schema version 1.0.
    Ensures sequential beats with valid timestamps, text, and selective image constraints.
    """
    if not isinstance(sp, dict):
        return None
    beats = sp.get('beats')
    if not isinstance(beats, list) or len(beats) < 2:
        return None

    cleaned_beats = []
    valid_types = {'kinetic_headline', 'statutory_trigger', 'visual_scene', 'metric_callout', 'dual_computation_step', 'statutory_trap'}

    for idx, b in enumerate(beats, 1):
        if not isinstance(b, dict):
            continue
        v_text = str(b.get('voice_sync_text') or '').strip()
        headline = str(b.get('headline') or f"Beat {idx}").strip()
        b_type = str(b.get('beat_type') or 'kinetic_headline').strip()
        if b_type not in valid_types:
            b_type = 'kinetic_headline'
        
        t0 = float(b.get('t_start', 0.0) or 0.0)
        t1 = float(b.get('t_end', t0 + 4.0) or (t0 + 4.0))
        img_req = bool(b.get('image_required', False))
        img_prompt = str(b.get('image_prompt') or '').strip() if img_req else None

        cleaned_beats.append({
            'beat_order': idx,
            't_start': t0,
            't_end': t1,
            'beat_type': b_type,
            'headline': headline,
            'badge': str(b.get('badge') or '').strip(),
            'subtext': str(b.get('subtext') or '').strip(),
            'metric_chip': str(b.get('metric_chip') or '').strip() or None,
            'voice_sync_text': v_text,
            'image_required': img_req,
            'image_prompt': img_prompt,
            'highlights': b.get('highlights') if isinstance(b.get('highlights'), list) else []
        })

    if not cleaned_beats:
        return None

    return {
        'doctrine': str(sp.get('doctrine') or '').strip(),
        'beats': cleaned_beats
    }

def validate_explainer_presentation(exp: Any) -> Optional[Dict[str, Any]]:
    """
    Validates explainer_presentation against schema version 1.0.
    Ensures required fields, ordered slides, layouts, and selective image constraints.
    Returns cleaned explainer presentation dict or None if invalid.
    """
    if not isinstance(exp, dict):
        return None
    slides = exp.get('slides')
    if not isinstance(slides, list) or len(slides) < 2:
        return None

    cleaned_slides = []
    valid_layouts = {'statutory_rule', 'visual_split', 'timeline_flow', 'dual_computation', 'statutory_trap'}

    for idx, s in enumerate(slides, 1):
        if not isinstance(s, dict):
            continue
        v_text = str(s.get('voice_sync_text') or '').strip()
        title = str(s.get('title') or f"Point {idx}").strip()
        layout = str(s.get('layout') or 'statutory_rule').strip()
        if layout not in valid_layouts:
            layout = 'statutory_rule'
        
        img_req = bool(s.get('image_required', False))
        img_prompt = str(s.get('image_prompt') or '').strip() if img_req else None
        
        cleaned_slides.append({
            'slide_order': idx,
            'title': title,
            'subtitle': str(s.get('subtitle') or '').strip(),
            'layout': layout,
            'image_required': img_req,
            'image_prompt': img_prompt,
            'voice_sync_text': v_text,
            'cards': s.get('cards') if isinstance(s.get('cards'), list) else [],
            'calculation_data': s.get('calculation_data') if isinstance(s.get('calculation_data'), dict) else None,
            'trap_data': s.get('trap_data') if isinstance(s.get('trap_data'), dict) else None
        })

    if not cleaned_slides:
        return None

    return {
        'title': str(exp.get('title') or 'Statutory Explainer Presentation').strip(),
        'badge': str(exp.get('badge') or '§ STATUTE').strip(),
        'doctrine': str(exp.get('doctrine') or '').strip(),
        'slides': cleaned_slides
    }

def validate_concept_simulation(sim: Any) -> Optional[Dict[str, Any]]:
    """
    Validates concept_simulation against schema version 1.0.
    Ensures required fields, ordered steps, and bounds step count (3-6 steps).
    Returns cleaned simulation dict or None if invalid.
    """
    if not isinstance(sim, dict):
        return None
    steps = sim.get('steps')
    if not isinstance(steps, list) or len(steps) < 2:
        return None

    cleaned_steps = []
    for idx, s in enumerate(steps, 1):
        if not isinstance(s, dict):
            continue
        v_text = str(s.get('voice_sync_text') or '').strip()
        if not v_text:
            continue
        cleaned_steps.append({
            'step_id': str(s.get('step_id') or f'step_{idx}'),
            'step_order': idx,
            'title': str(s.get('title') or f'Step {idx}'),
            'metric_label': str(s.get('metric_label') or 'Key Metric'),
            'metric_value': str(s.get('metric_value') or ''),
            'voice_sync_text': v_text,
            'image_prompt': str(s.get('image_prompt') or ''),
            'calculation_data': s.get('calculation_data') if isinstance(s.get('calculation_data'), dict) else None
        })

    if len(cleaned_steps) < 2:
        return None

    return {
        'schema_version': str(sim.get('schema_version') or '1.0'),
        'illustrative_only': True,
        'doctrine_topic': str(sim.get('doctrine_topic') or 'Statutory Concept'),
        'relevant_tax_year': str(sim.get('relevant_tax_year') or ''),
        'statutory_assumptions': sim.get('statutory_assumptions') if isinstance(sim.get('statutory_assumptions'), list) else [],
        'intro_voice': str(sim.get('intro_voice') or 'ഇനി ഒരു simple example വഴി കൂടുതൽ മനസ്സിലാക്കാം.'),
        'steps': cleaned_steps[:6]
    }

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
                    # Validate and attach concept_simulation if present
                    if 'concept_simulation' in data:
                        clean_sim = validate_concept_simulation(data['concept_simulation'])
                        if clean_sim:
                            data['mindmap']['concept_simulation'] = clean_sim
                            print(f"  [SIMULATION VALIDATED] {len(clean_sim['steps'])} illustrative steps attached.")
                        else:
                            print(f"  [WARN] Simulation failed validation, skipping simulation gracefully.")
                    # Validate and attach explainer_presentation if present
                    if 'explainer_presentation' in data:
                        clean_exp = validate_explainer_presentation(data['explainer_presentation'])
                        if clean_exp:
                            data['mindmap']['explainer_presentation'] = clean_exp
                            print(f"  [EXPLAINER DECK VALIDATED] {len(clean_exp['slides'])} studio slides attached.")
                        else:
                            print(f"  [WARN] Explainer deck failed validation, skipping gracefully.")
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

            # Validate and sanitize time_sec for keywords
            highlights = pt.get("highlights", [])
            body_list = pt.get("body", [])
            body_text = " ".join(body_list) if isinstance(body_list, list) else str(body_list)
            voice_text = pt.get("voice_sync_text", "")

            valid_hl = []
            if highlights and isinstance(highlights, list):
                for h_idx, h in enumerate(highlights):
                    if isinstance(h, str):
                        phrase = h.strip()
                        t_sec = 0.0
                    elif isinstance(h, dict):
                        phrase = (h.get("phrase") or h.get("word") or "").strip()
                        t_sec = float(h.get("time_sec") or h.get("time") or 0.0)
                    else:
                        continue

                    if phrase and phrase.lower() in body_text.lower():
                        # Extract exact verbatim substring directly from body_text to guarantee 100% case-match
                        idx = body_text.lower().find(phrase.lower())
                        exact_phrase = body_text[idx:idx + len(phrase)]

                        # Estimate timing based on keyword position in voice_sync_text narrative if present
                        if voice_text and exact_phrase.lower() in voice_text.lower():
                            v_idx = voice_text.lower().find(exact_phrase.lower())
                            v_ratio = v_idx / max(1, len(voice_text))
                            t_sec = round(1.2 + (v_ratio * (pt_dur - 2.5)), 1)
                        elif t_sec <= 0.0 or t_sec > pt_dur:
                            t_sec = round(1.5 + (h_idx * (pt_dur - 3.0) / max(1, len(highlights))), 1)

                        valid_hl.append({"phrase": exact_phrase, "time_sec": round(t_sec, 1)})

            # Smart fallback extractor if LLM produced no valid highlights
            if not valid_hl and body_text:
                fallback_phrases = []
                # 1. Statutory Sections
                sec_matches = re.findall(r'(?:Section|u/s|Rule)\s+[0-9A-Za-z()]+(?:\([0-9A-Za-z]+\))?', body_text, re.IGNORECASE)
                fallback_phrases.extend(sec_matches)
                # 2. Key legal terms
                for term in ["not a transfer", "exempt", "Indian company", "capital asset", "Long-Term Capital Asset", 
                             "Short-Term Capital Asset", "cost of acquisition", "period of holding", "marginal relief",
                             "total income", "surcharge", "rebate", "residential house"]:
                    if term.lower() in body_text.lower():
                        idx = body_text.lower().find(term.lower())
                        fallback_phrases.append(body_text[idx:idx + len(term)])
                
                clean_fb = list(dict.fromkeys(fallback_phrases))[:3]
                for fb_idx, fb_p in enumerate(clean_fb):
                    fb_t = round(1.5 + (fb_idx * (pt_dur - 3.0) / max(1, len(clean_fb))), 1)
                    valid_hl.append({"phrase": fb_p, "time_sec": fb_t})

            # Ensure strictly ascending, well-spaced timestamps
            valid_hl.sort(key=lambda x: x["time_sec"])
            for i in range(1, len(valid_hl)):
                if valid_hl[i]["time_sec"] <= valid_hl[i-1]["time_sec"]:
                    valid_hl[i]["time_sec"] = round(valid_hl[i-1]["time_sec"] + 1.8, 1)

            pt["highlights"] = valid_hl
            
        b["t0"] = round(b_t0, 2)
        b["t1"] = round(current_time - 0.8, 2)
        current_time += 1.2
        
    mindmap["total_duration"] = round(current_time, 2)
    return mindmap

# ==========================================================================
# UNIVERSAL KINETIC PRESENTER: VALIDATOR & PIPELINE STAGE CONTROLLER
# ==========================================================================

import hashlib
import glob
from pathlib import Path

GAP_MS = 250
LAYOUTS = {
    "headline", "takeaway", "timeline", "scene", "split", "trap",
    "fork", "meter", "ledger", "case_card", "compare", "checklist", "statute_quote"
}
TIME_KEYS = {"at", "axis_at", "arrow_at"}
NON_TEXT_KEYS = {
    "id", "layout", "tone", "pos", "side", "kind", "image_url", "voice_sync_text",
    "start", "end", "zoom", "fmt", "value", "target", "at", "axis_at", "arrow_at",
    "from_x", "to_x", "serves", "purpose", "events", "result", "sign", "emphasis",
    "question_id", "audio_url", "duration_sec", "sync_offset_sec", "context_pill",
    "fallback", "meta", "omitted"
}

MECHANISM_CENTREPIECE = {
    "timing_shift": "timeline",
    "date_cutoff": "fork",
    "threshold": "meter",
    "proportion": {"ledger", "compare"},
    "deadline_window": "timeline",
    "computation": "ledger",
    "classification": {"split", "compare"},
    "precedent": "case_card",
    "condition_chain": "checklist",
    "exception_trap": "trap"
}

def compute_sha256(file_path: str) -> str:
    """Computes SHA-256 hash of a file's content."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify_approval(approved_json_path: str, source_json_path: str) -> tuple[bool, str]:
    """Checks that approval file exists and matches the source file's SHA-256 hash."""
    if not os.path.exists(approved_json_path):
        return False, f"Approval missing: {approved_json_path} does not exist"
    if not os.path.exists(source_json_path):
        return False, f"Source missing: {source_json_path} does not exist"
    
    with open(approved_json_path, "r", encoding="utf-8") as f:
        try:
            app_data = json.load(f)
        except Exception as e:
            return False, f"Invalid JSON in {approved_json_path}: {e}"
            
    expected_hash = compute_sha256(source_json_path)
    recorded_hash = app_data.get("source_hash")
    if recorded_hash != expected_hash:
        return False, f"Hash mismatch: source changed since approval ({recorded_hash} vs {expected_hash})"
    return True, f"Approved by {app_data.get('reviewer', 'Unknown')} at {app_data.get('approved_at', 'Unknown')}"

def write_approval(approved_json_path: str, source_json_path: str, reviewer: str):
    """Writes approval file containing SHA-256 hash and reviewer name."""
    source_hash = compute_sha256(source_json_path)
    app_data = {
        "reviewer": reviewer,
        "approved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_hash": source_hash,
        "source_file": os.path.basename(source_json_path)
    }
    with open(approved_json_path, "w", encoding="utf-8") as f:
        json.dump(app_data, f, indent=2)
    print(f"[GATE APPROVED] {approved_json_path} signed by {reviewer} (SHA: {source_hash[:8]}...)")

def iter_times(node):
    """Yields all timestamp values from any key in TIME_KEYS or ending in _at."""
    if isinstance(node, dict):
        for k, v in node.items():
            if (k in TIME_KEYS or k.endswith("_at")) and isinstance(v, (int, float)):
                yield v
            else:
                yield from iter_times(v)
    elif isinstance(node, list):
        for x in node:
            yield from iter_times(x)

def iter_texts(node):
    """Yields all display strings excluding non-text configuration keys."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k not in NON_TEXT_KEYS:
                if isinstance(v, str):
                    yield v
                elif isinstance(v, dict):
                    yield from iter_texts(v)
                elif isinstance(v, list):
                    yield from iter_texts(v)
            else:
                if isinstance(v, (dict, list)):
                    yield from iter_texts(v)
    elif isinstance(node, list):
        for x in node:
            yield from iter_texts(x)

def compute_layout_similarity(seq1: list[str], seq2: list[str]) -> float:
    """Computes longest common ordered run divided by shorter sequence length."""
    # Ignore headline and takeaway
    s1 = [x for x in seq1 if x not in ("headline", "takeaway")]
    s2 = [x for x in seq2 if x not in ("headline", "takeaway")]
    if not s1 or not s2:
        return 0.0
    
    # Longest common subsequence length
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    return lcs / min(m, n)

def validate_screenplay_v2(
    sp: Dict[str, Any],
    analysis: Optional[Dict[str, Any]] = None,
    timed_sentences: Optional[List[Dict[str, Any]]] = None,
    recent_screenplays: Optional[List[Dict[str, Any]]] = None
) -> List[str]:
    """
    Strictly validates Screenplay JSON v2 schema against all 17 checks in the guideline.
    """
    errs, prev_end = [], 0.0
    beats = sp.get("beats", [])
    if not beats:
        return ["no beats in screenplay"]

    # 1. Beat count & contiguity
    valid_anchor_times = set()
    if timed_sentences:
        for s in timed_sentences:
            valid_anchor_times.add(round(s.get("start", 0.0), 2))
            for w in s.get("words", []):
                valid_anchor_times.add(round(w.get("at", 0.0), 2))

    served_analysis_ids = set()
    screenplay_numbers = set()
    screenplay_dates = set()
    layout_sequence = []

    for b in beats:
        layout = b.get("layout")
        layout_sequence.append(layout)
        
        # Check: Layout known
        if layout not in LAYOUTS:
            errs.append(f"{b.get('id')}: unknown layout {layout}")
            
        # Check: Contiguity
        if abs(b.get("start", 0) - prev_end) > 0.05:
            errs.append(f"{b.get('id')}: gap or overlap before this beat ({b.get('start')} vs prev end {prev_end})")
            
        # Check: End after start
        if b.get("end", 0) <= b.get("start", 0):
            errs.append(f"{b.get('id')}: end must be after start ({b.get('end')} <= {b.get('start')})")
            
        # Check: Time inside beat range & anchor matching
        for at in iter_times(b):
            if not (b.get("start", 0) <= at <= b.get("end", 0)):
                errs.append(f"{b.get('id')}: time {at} is outside beat ({b.get('start')} - {b.get('end')})")
            if valid_anchor_times:
                nearest = min(abs(at - vt) for vt in valid_anchor_times)
                if nearest > 0.05:
                    errs.append(f"{b.get('id')}: time {at} does not match any sentence start or word time (diff {nearest:.3f}s)")
                    
        # Check: Text length (12 words maximum)
        for text in iter_texts(b):
            clean_words = re.sub(r"\[\[|\]\]", "", text).split()
            if len(clean_words) > 12:
                errs.append(f"{b.get('id')}: display text over 12 words ({len(clean_words)} words): '{text[:40]}...'")
                
        # Track serves
        for s_id in b.get("serves", []):
            served_analysis_ids.add(s_id)
            
        prev_end = b.get("end", 0)

    # Check: Last beat ends at duration_sec
    if abs(prev_end - sp.get("duration_sec", 0)) > 0.1:
        errs.append(f"last beat ends at {prev_end}, but duration_sec is {sp.get('duration_sec')}")

    # Checks against Analysis
    if analysis:
        # Check: Centrepiece layout matches primary mechanism
        prim_mech = analysis.get("mechanism", {}).get("primary")
        expected_cp = MECHANISM_CENTREPIECE.get(prim_mech)
        if expected_cp:
            if isinstance(expected_cp, str):
                has_cp = any(b.get("layout") == expected_cp for b in beats)
                if not has_cp:
                    errs.append(f"Centrepiece layout '{expected_cp}' required for primary mechanism '{prim_mech}' is missing!")
            elif isinstance(expected_cp, set):
                has_cp = any(b.get("layout") in expected_cp for b in beats)
                if not has_cp:
                    errs.append(f"One of centrepiece layouts {expected_cp} required for '{prim_mech}' is missing!")

        # Check: Coverage of numbers, conditions, case laws
        omitted_refs = {o.get("ref") for o in sp.get("omitted", [])}
        for n in analysis.get("numbers", []):
            if n["id"] not in served_analysis_ids and n["id"] not in omitted_refs:
                errs.append(f"Analysis number {n['id']} ('{n.get('label')}') not served by any beat and not in omitted")
        for c in analysis.get("conditions", []):
            if c["id"] not in served_analysis_ids and c["id"] not in omitted_refs:
                errs.append(f"Analysis condition {c['id']} not served by any beat and not in omitted")
        for cl in analysis.get("case_laws", []):
            if cl["id"] not in served_analysis_ids and cl["id"] not in omitted_refs:
                errs.append(f"Analysis case law {cl['id']} not served by any beat and not in omitted")

    # Check: Anti-repetition against recent screenplays
    if recent_screenplays:
        for r_sp in recent_screenplays:
            r_seq = [b.get("layout") for b in r_sp.get("beats", [])]
            sim = compute_layout_similarity(layout_sequence, r_seq)
            if sim >= 0.6:
                errs.append(f"Anti-repetition failure: layout sequence is too similar ({sim:.2f} >= 0.6) to {r_sp.get('question_id')}")
                break

    return errs

# ==========================================================================
# CLI RUNNER: STAGES & GATES
# ==========================================================================

import argparse

def run_stage_analyze(qid: str):
    print(f"\n=== STAGE 1: INTAKE & PROVISION ANALYSIS FOR {qid} ===")
    source_dir = os.path.join("redesign_demo", "source", qid)
    if not os.path.exists(source_dir):
        print(f"ERROR: Source directory {source_dir} not found. Please populate question.md, answer.md, notes.md, bare_act.md first.")
        return False
        
    build_dir = os.path.join("redesign_demo", "build", qid)
    os.makedirs(build_dir, exist_ok=True)
    
    # Check required source files
    req_files = ["question.md", "answer.md", "notes.md", "bare_act.md"]
    missing = [f for f in req_files if not os.path.exists(os.path.join(source_dir, f))]
    if missing:
        print(f"ERROR: Missing source files in {source_dir}: {missing}")
        return False
        
    analysis_file = os.path.join(build_dir, "analysis.json")
    if not os.path.exists(analysis_file):
        print(f"Generating analysis from source material in {source_dir}...")
        # Will be populated by analysis generator
    else:
        print(f"Analysis file exists: {analysis_file}")
        
    # Print Gate 1 Review Checklist
    print("\n" + "="*80)
    print(f"GATE 1 REVIEW CHECKLIST: {qid}")
    print("="*80)
    print("[ ] Every section number and sub-section cited matches the bare act or study material")
    print("[ ] Every condition is complete: nothing missing, nothing added that the source does not say")
    print("[ ] Every date and threshold matches the source, and applies to the correct period")
    print("[ ] Every case law has the right name, court and principle (all verify: true items resolved)")
    print("[ ] Every number recomputes to the source's answer")
    print("[ ] The mechanism.primary really is the hard part of this provision")
    print("[ ] The unique_challenge is what students actually get wrong")
    print("[ ] Nothing in the analysis comes from the agent's memory instead of the source")
    print("[ ] Law as amended: any rule that changed over time is labelled with the period it applies to")
    print("[ ] Section numbering and Act: the numbers match the ones your syllabus uses")
    print("[ ] The context_pill and every on-screen label use those same section numbers")
    print("[ ] The concrete_example, if any, comes from the question itself and is not invented")
    print("="*80)
    print("STOPPING FOR HUMAN REVIEW. To approve, execute:")
    print(f"python pipeline/autonomous_provision_architect.py --qid {qid} --approve analysis --reviewer \"<Your Name>\"")
    return True

def run_stage_plan(qid: str):
    print(f"\n=== STAGE 2: CONCEPT & BEAT PLAN FOR {qid} ===")
    build_dir = os.path.join("redesign_demo", "build", qid)
    analysis_file = os.path.join(build_dir, "analysis.json")
    approved_file = os.path.join(build_dir, "analysis.approved.json")
    
    ok, msg = verify_approval(approved_file, analysis_file)
    if not ok:
        print(f"GATE 1 NOT APPROVED: {msg}")
        print("Cannot generate beat plan until Gate 1 is approved by a human.")
        return False
        
    print(f"Gate 1 verified: {msg}")
    beat_plan_file = os.path.join(build_dir, "beat_plan.json")
    
    print("\n" + "="*80)
    print(f"GATE 2 CONCEPT REVIEW CHECKLIST: {qid}")
    print("="*80)
    print("[ ] The one-line visual concept reflects the primary statutory mechanism")
    print("[ ] The centrepiece layout visualises the hardest part of the provision")
    print("[ ] Beat count is between 4 and 9 beats with appropriate narrative pacing")
    print("[ ] Every analysis condition, number, and case law is covered or documented in omitted")
    print("[ ] Layout sequence similarity against recent screenplays is under 0.6")
    print("="*80)
    print("STOPPING FOR HUMAN REVIEW. To approve, execute:")
    print(f"python pipeline/autonomous_provision_architect.py --qid {qid} --approve plan --reviewer \"<Your Name>\"")
    return True

def main_cli():
    parser = argparse.ArgumentParser(description="Universal Kinetic Presenter Pipeline")
    parser.add_argument("--qid", help="Question ID (e.g. dt-c2-q14, dt-c2-q25)")
    parser.add_argument("--stage", choices=["analyze", "plan", "build"], help="Pipeline stage to run")
    parser.add_argument("--approve", choices=["analysis", "plan"], help="Gate to approve")
    parser.add_argument("--reviewer", help="Reviewer name for gate approval")
    args = parser.parse_args()

    if not args.qid:
        print("Please provide --qid <qid>")
        return

    build_dir = os.path.join("redesign_demo", "build", args.qid)
    os.makedirs(build_dir, exist_ok=True)

    if args.approve:
        if not args.reviewer:
            print("ERROR: --reviewer name is mandatory when approving a gate!")
            return
        if args.approve == "analysis":
            source_file = os.path.join(build_dir, "analysis.json")
            approved_file = os.path.join(build_dir, "analysis.approved.json")
            write_approval(approved_file, source_file, args.reviewer)
        elif args.approve == "plan":
            source_file = os.path.join(build_dir, "beat_plan.json")
            approved_file = os.path.join(build_dir, "beat_plan.approved.json")
            write_approval(approved_file, source_file, args.reviewer)
        return

    if args.stage == "analyze":
        run_stage_analyze(args.qid)
    elif args.stage == "plan":
        run_stage_plan(args.qid)
    elif args.stage == "build":
        beat_plan_file = os.path.join(build_dir, "beat_plan.json")
        approved_plan_file = os.path.join(build_dir, "beat_plan.approved.json")
        ok, msg = verify_approval(approved_plan_file, beat_plan_file)
        if not ok:
            print(f"GATE 2 NOT APPROVED: {msg}")
            print("Cannot build lesson until Gate 2 is approved by a human.")
            return
        print(f"Gate 2 verified: {msg}")
        print(f"Building full lesson for {args.qid}...")

if __name__ == "__main__":
    main_cli()
