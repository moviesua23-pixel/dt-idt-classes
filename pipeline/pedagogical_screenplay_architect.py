"""
pipeline/pedagogical_screenplay_architect.py
Pedagogical Screenplay Architect:
Takes a statutory provision, designs a rich concrete pedagogical example story
(using distinct character/company names and different realistic figures than the question),
provides a complete overview upfront in Beat 1, and teaches the statute step-by-step
with strict 1:1 voice-to-screen synchronization.
"""

import os
import sys
import json
import re
import time
from typing import Dict, Any, List, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator, AllKeysQuotaExhaustedError
from google import genai
from google.genai import types

PEDAGOGICAL_PROMPT = """You are a senior, beloved CA Final Tax Professor and Visual Explainer Architect for Indian Direct Tax and Indirect Tax.
Your student needs to master the statutory provision and solve the legal issue presented in this question.

Context / Question:
{question_text}

Answer / Statutory Solution:
{answer_text}

Statutory Matrix:
{provision_matrix}

========================================================================================
CRITICAL PEDAGOGICAL RULE 1: CREATE A DISTINCT, COMPLETE PEDAGOGICAL EXAMPLE STORY
========================================================================================
- DO NOT reuse the exact names or identical figures from the exam question!
- Create a distinct, memorable persona / enterprise (e.g. 'Apex Engineering Ltd', 'Rajesh / Zenith Textiles', 'Kavya Motors', 'Anand Agro Products', etc.).
- Invent a concrete, realistic case scenario with specific figures, assets/transactions, and dates that reflect the core legal dispute or statutory mechanism of the section.
- Every situation and number used in your example must be mathematically coherent and legally precise.

========================================================================================
CRITICAL PEDAGOGICAL RULE 2: FIRST JOB OF PRESENTATION IS A COMPLETE OVERVIEW UPFRONT (BEAT 1)
========================================================================================
- Beat 1 MUST provide a complete, crystal-clear overview of the entire story example!
- Every amount, asset, date, and factual situation MUST be laid out transparently right upfront:
  * Who is the assessee and what is their business/situation?
  * What is the core transaction or event triggering the tax provision?
  * What are all the relevant assets, figures, considerations, costs, or turnover numbers involved?
  * What is the classification or statutory filter (e.g., eligible vs ineligible, business vs capital, taxable vs exempt)?
- The student must see the full financial and factual chessboard before diving into statutory analysis!

========================================================================================
CRITICAL PEDAGOGICAL RULE 3: TEACH THE STATUTORY PROVISION STEP-BY-STEP USING THE EXAMPLE
========================================================================================
Organize the lecture into 4 to 6 logical sequential beats matching the statutory architecture:
- Beat 1 ("fork"): COMPLETE FACT OVERVIEW & ASSET / TRANSACTION FILTER
  Lay out the complete story scenario and separate the qualifying elements from the non-qualifying elements.
  Must include `intro_cards` for the opening narrative, followed by sequential `story_steps` for each transaction/asset, and classification `branches`.
- Beat 2 ("statute_quote" or "checklist" or "case_card"): STATUTORY MANDATE & CONDITIONS GATE
  Show the governing statutory section, sub-section, or legal conditions/time limits (e.g. reinvestment window, holding period, condition tests).
- Beat 3 ("meter" or "compare"): ELIGIBILITY CEILING / STATUTORY THRESHOLD / QUALIFYING POOL
  If there is a numerical limit, cap, threshold, or qualifying investment pool, visualize the gauge/bar with breakdown items.
- Beat 4 ("ledger"): STEP-BY-STEP MATHEMATICAL COMPUTATION & TAX OPTIMIZATION INSIGHT
  Show the step-by-step arithmetic computation of taxable amounts/deductions/exemptions with row-by-row breakdown and a total row. Include a callout banner highlighting the golden exam optimization trick or key legal interpretation.
- Beat 5 ("takeaway"): 3 GOLDEN EXAM RULES / DOCTRINES
  Summarize the 3 non-negotiable statutory principles or exam traps the student must remember for CA Final/Inter exams.

========================================================================================
CRITICAL PEDAGOGICAL RULE 4: STRICT 1:1 VOICE-TO-SCREEN CORRESPONDENCE (UNIVERSAL LAW)
========================================================================================
- WHATEVER IS SPOKEN IN voice_sync_text MUST BE SHOWN ON SCREEN IN DIRECT 1:1 CORRESPONDENCE!
- When the teacher mentions an asset, an amount, a condition, a date, or a rule, that element MUST appear visually on screen.
- NEVER mention numbers, facts, or entities in voice that are missing from the visual layout!
- NEVER speak for more than 5 seconds without an animated visual element popping up!
- In Beat 1 ("fork"), include 2 to 3 "intro_cards" that pop up sequentially when the teacher speaks the opening setup sentences:
  * Card 1: Statutory Focus / Core Provision (e.g. Section and subject)
  * Card 2: Assessee Persona / Enterprise Setup (e.g. Assessee name and business context)
  * Card 3: Transaction / Event Trigger (e.g. Event date, nature of sale/transfer/deal)
  Set "out_at" to exit right before the specific asset cards in story_steps begin!

========================================================================================
CRITICAL PEDAGOGICAL RULE 5: AUTHENTIC, WARM MALAYALAM TEACHER DIALOGUE (NATURAL MANGLISH)
========================================================================================
- Sound like a REAL, ENERGETIC, PASSIONATE KERALA CA FACULTY teaching in a live CA Final classroom!
- Natural Manglish code-switching: Friendly Malayalam teacher scaffolding with standard English legal/tax terminology.
- MANDATORY LANGUAGE RULES:
  * SECTIONS & PROVISIONS: In English ('Section 54G', 'Section 50', 'Section 45(2)'). Never transliterate into Malayalam script.
  * DATES & YEARS: In English ('1st April 2001', 'Assessment Year 2026-27', 'Financial Year 2025-26', 'March 2026'). Never translate dates into Malayalam words.
  * TAX & FINANCIAL TERMS: In English ('Capital Gains', 'Short-term Capital Gain', 'Long-term Capital Gain', 'Written Down Value', 'Sale Consideration', 'Cost of Acquisition', 'Exemption', 'Deduction', 'Turnover').
  * SEQUENTIAL ORDINAL CUES: Use natural Malayalam ordinal markers to cleanly introduce each asset or step:
    'Onnamathathu...', 'Randamathathu...', 'Moonnamathathu...', 'Naalaamathathu...', or 'Aadyam...', 'Aduthathayi...', 'Avasanam...'
  * NO ROBOTIC OR BROKEN WORDS: Use 'athayath' (NOT 'ithathayath'), 'ormavekkoo' (NOT 'ormathoykkoo'), 'taxable aanu' (NOT 'taxable aane'), 'vaangiya' / 'purchase cheytha' (NOT 'purchase chethya').

========================================================================================
OUTPUT FORMAT: PURE JSON
========================================================================================
Return STRICT VALID JSON matching this exact structure:
{{
  "context_pill": "Section Name | Topic Name",
  "beats": [
    {{
      "id": "b1",
      "layout": "fork",
      "voice_sync_text": "Malayalam teacher narration text introducing the section, the example assessee, each asset/transaction sequentially with ordinal cues, and the classification filter...",
      "title": {{"text": "Complete Scenario Overview & Eligibility Filter"}},
      "intro_cards": [
        {{"badge": "Statutory Focus", "title": "Section Name", "sub": "Core Legal Provision", "at": 2.5, "out_at": 25.0}},
        {{"badge": "Case Study Setup", "title": "Assessee Name", "sub": "Business / Scenario Context", "at": 8.0, "out_at": 25.0}},
        {{"badge": "Transfer / Trigger Event", "title": "Event Details", "sub": "Transaction Summary & Assets Involved", "at": 18.0, "out_at": 25.0}}
      ],
      "story_steps": [
        {{"badge": "Step 1: Item Name", "title": "Sale: Rs X | Cost/WDV: Rs Y", "sub": "Gain / Legal Status: Rs Z", "val": 100000}},
        {{"badge": "Step 2: Item Name", "title": "Sale: Rs X | Cost/WDV: Rs Y", "sub": "Gain / Legal Status: Rs Z", "val": 200000}}
      ],
      "divider": {{"text": "Eligibility Classification / Legal Division"}},
      "branches": [
        {{"side": "left", "label": "Qualifying / Eligible Branch", "facts": [{{"text": "Qualifying items/conditions"}}, {{"text": "Qualifying totals"}}], "outcome": {{"text": "Eligible for Benefit / Exemption"}}}},
        {{"side": "right", "label": "Ineligible / Excluded Branch", "facts": [{{"text": "Ineligible items"}}, {{"text": "Statutory exclusion rule"}}], "outcome": {{"text": "Ineligible / Taxable"}}}}
      ],
      "result_card": {{"badge": "Exam Trap Alert", "title": "Critical Exclusion / Rule", "sub": "Why the excluded item fails statutory test"}}
    }},
    {{
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Malayalam teacher narration explaining the statutory text, conditions, and time horizon...",
      "title": {{"text": "Statutory Mandate & Conditions u/s ..."}},
      "quote": {{
        "text": "Exact statutory wording or core legal provision...",
        "citation": "Section ... of the Income-tax Act, 1961",
        "emphasis": "key condition or time period in the quote"
      }},
      "context_bubble": {{
        "badge": "Statutory Condition",
        "speaker": "Section ...",
        "theme": "Time Horizon / Gate Condition",
        "text": "Summary of condition or time window"
      }}
    }},
    {{
      "id": "b3",
      "layout": "meter",
      "voice_sync_text": "Malayalam teacher narration calculating the qualifying threshold or reinvestment pool...",
      "title": {{"text": "Qualifying Pool / Statutory Ceiling"}},
      "meter_display": {{
        "min_val": 0,
        "max_val": 3000000,
        "current_val": 2500000,
        "unit": "₹",
        "threshold": 2000000,
        "labels": {{"start": "₹ 0", "threshold_label": "Threshold / Cap: ₹ ...", "current_label": "Total Qualifying: ₹ ..."}}
      }},
      "breakdown": [
        {{"label": "Item 1", "val": 1000000, "status": "Qualifies u/s ..."}},
        {{"label": "Item 2", "val": 1500000, "status": "Qualifies u/s ..."}},
        {{"label": "Item 3", "val": 200000, "status": "Ineligible / Excluded"}}
      ],
      "outcome": {{"text": "Statutory Eligibility / Outcome Result", "tone": "ok"}}
    }},
    {{
      "id": "b4",
      "layout": "ledger",
      "voice_sync_text": "Malayalam teacher narration calculating the step-by-step numbers and explaining the golden tax optimization trick...",
      "title": {{"text": "Computation of Taxable Amount for AY ..."}},
      "callout": {{
        "badge": "Golden Optimization Trick",
        "text": "Key tax saving principle or set-off priority explained in plain terms"
      }},
      "ledger_rows": [
        {{"label": "Computation Line 1", "amount": 1000000, "type": "income"}},
        {{"label": "Less: Exemption / Deduction Priority 1", "amount": -800000, "type": "deduction"}},
        {{"label": "Net Subtotal", "amount": 200000, "type": "subtotal"}},
        {{"label": "Taxable Balance @ X%", "amount": 200000, "type": "taxable"}}
      ],
      "net_total": {{
        "label": "Total Taxable Income / Gain",
        "val": 200000,
        "detail": "Final Taxable Amount"
      }}
    }},
    {{
      "id": "b5",
      "layout": "takeaway",
      "voice_sync_text": "Malayalam teacher narration delivering the 3 Golden Rules for exam mastery...",
      "title": {{"text": "3 Golden Rules for Exam Mastery"}},
      "rules": [
        {{"num": "01", "heading": "First Rule Heading", "body": "First rule description in Malayalam and English"}},
        {{"num": "02", "heading": "Second Rule Heading", "body": "Second rule description in Malayalam and English"}},
        {{"num": "03", "heading": "Third Rule Heading", "body": "Third rule description in Malayalam and English"}}
      ]
    }}
  ]
}}
"""

def generate_pedagogical_screenplay_plan(q_num: int, q_text: str, ans_text: str, prov_matrix: str) -> Optional[Dict[str, Any]]:
    prompt = PEDAGOGICAL_PROMPT.format(
        question_text=q_text[:3000],
        answer_text=ans_text[:3000],
        provision_matrix=prov_matrix[:3000]
    )

    models_to_try = [
        'gemini-3.5-flash',
        'gemini-3.8-flash',
        'gemini-3.5-flash-lite',
        'gemini-3.1-flash-lite',
        'gemini-3.1-pro-preview'
    ]
    for model_name in models_to_try:
        def _call(client, m=model_name):
            resp = client.models.generate_content(
                model=m,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )
            return json.loads(resp.text.strip())

        try:
            res = rotator.execute_with_retry(_call)
            if isinstance(res, list):
                res = {"context_pill": f"Statutory Analysis Q{q_num}", "beats": res}
            if res and isinstance(res, dict) and res.get('beats'):
                print(f"  [SCREENPLAY ARCHITECT] Successfully generated screenplay using {model_name}")
                return res
        except Exception as e:
            print(f"  [SCREENPLAY ARCHITECT] Model {model_name} failed: {e}. Trying fallback model...")
            continue

    print("  [SCREENPLAY ARCHITECT ERROR] All candidate models failed to generate screenplay plan.")
    return None

def build_full_screenplay_for_question(subject: str, ch_no: int, q_num: int, q_text: str, ans_text: str, prov_matrix: str) -> Optional[Dict[str, Any]]:
    qid = f"{subject.lower()}-c{ch_no}-q{q_num}"
    print(f"  [SCREENPLAY ARCHITECT] Designing pedagogical example and layouts for {qid}...")
    plan = generate_pedagogical_screenplay_plan(q_num, q_text, ans_text, prov_matrix)
    if not plan or not plan.get('beats'):
        return None

    beats = plan.get('beats', [])
    current_time = 0.0
    for b in beats:
        txt = b.get('voice_sync_text', '')
        word_count = len(txt.split())
        est_duration = max(8.0, round(word_count / 2.2, 2))
        b['start'] = round(current_time, 2)
        b['end'] = round(current_time + est_duration, 2)
        current_time = b['end'] + 0.35

    return {
        "question_id": qid,
        "audio_url": f"data/audio/{qid}.mp3",
        "duration_sec": round(current_time, 2),
        "sync_offset_sec": 0.0,
        "context_pill": plan.get('context_pill', f"§ Ch {ch_no} Q {q_num}"),
        "fallback": False,
        "beats": beats
    }
