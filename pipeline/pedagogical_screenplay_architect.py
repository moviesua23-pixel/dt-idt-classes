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
CRITICAL PEDAGOGICAL RULE 3: SITUATIONAL VISUAL MODELING & ELASTIC BEATS (UNIVERSAL ARCHITECTURE)
========================================================================================
- ELASTIC BEAT ARCHITECTURE (4 TO 8 BEATS AS REQUIRED):
  * DO NOT artificially constrain or restrict the screenplay to exactly 5 beats!
  * If a tax case or statutory provision involves multiple assets, properties, or legal disputes
    (e.g., Section 50C deemed full value + Section 54 residential flats + Section 54EC bond investments + Section 71 inter-head set-off, or multi-asset industrial shifting with qualifying vs non-qualifying assets),
    use 6, 7, or 8 focused beats so every provision and computation has dedicated visual space.
  * For single-point statutory questions (e.g., simple transfer or forfeiture rule), 4 or 5 beats are appropriate.

- SITUATIONAL VISUAL STORYTELLING (NOT JUST PLAIN TEXT CARDS):
  * When explaining the example, the visual scene MUST depict the concrete physical or legal reality:
    1. Factory / Industrial Shifting: Layout "story_scene" with scene_type "factory_shift". Shows Urban limit on left with factory and transferred assets, relocation motion arrow in center, and Non-Urban Rural zone on right with new factory and qualifying reinvestment pool.
    2. Landlord & Tenant / Rental Income: Layout "story_scene" with scene_type "rental_and_gift" or "rental_computation". Shows property, tenant paying rent with money flow arrow, municipal tax deduction, NAV, standard deduction 24(a), and interest 24(b).
    3. Stamp Duty Benchmark & Deemed Consideration: Layout "story_scene" with scene_type "sdv_comparison". Shows actual consideration vs Stamp Duty Value (SDV) vertical comparison bars, 110% safe harbor threshold test, Section 50C deemed full value stamp, and gross LTCG pill.
    4. Adjoining Flats / Single Habitable Unit: Layout "story_scene" with scene_type "adjacent_flats_merge". Shows dual flat blueprints, divider wall fading out, merging as one habitable unit, CIT v. Ananda Basappa judicial ruling gavel, and Section 54 exemption pill.
    5. Statutory Reinvestment Timeline: Layout "story_scene" with scene_type "bond_investment" or layout "timeline". Shows horizontal chronological milestone nodes (Transfer date, Payment date, Allotment date, 6-Month statutory deadline), milestone brackets, Hindustan Unilever Bom HC landmark gavel card, and Section 54EC exemption pill.
    6. Factual Overview & Asset Filtering: Layout "fork". Uses intro_cards for opening setup, sequential story_steps for each asset/item, divider line, and classification branches (Qualifying vs Ineligible).
    7. Statutory Threshold / Reinvestment Pool: Layout "meter". Visualizes statutory ceiling gauge bar with breakdown cards and padlock/outcome pill.
    8. Mathematical Computation: Layout "ledger". Step-by-step arithmetic computation of taxable amounts with signs (+, −, =), count animation, and tax optimization alert callout.
    9. Golden Takeaways: Layout "takeaway". 3 non-negotiable statutory rules or exam traps.

========================================================================================
CRITICAL PEDAGOGICAL RULE 4: 1:1 VOICE-TO-SCREEN FIDELITY & COMPLETE SITUATIONAL DECOMPOSITION
========================================================================================
- WHATEVER IS SPOKEN IN voice_sync_text MUST BE SHOWN ON SCREEN IN DIRECT 1:1 CORRESPONDENCE!
- In "story_scene" beats, you MUST decompose the entire scenario into ALL of its constituent entities, and map every single one to a distinct key in the "elements" dictionary:
  * The Actor / Assessee (e.g. "assessee_person", "seller_vijay", "landlord_ramesh", "enterprise_apex")
  * The Asset / Property / Machinery (e.g. "residential_house", "urban_factory", "qualifying_land")
  * Every Historical Milestone / Improvement (e.g. "purchase_original_cost", "fmv_sdv_benchmark", "forfeited_advance", "construction_improvement")
  * The Counterparty (e.g. "buyer_party", "tenant_kumar", "donee_son", "rural_authority")
  * The Cash Flow / Cheque / Movement (e.g. "cheque_advance_payment", "rent_annual_flow", "relocation_transit")
  * The Statutory Benchmark / Gavel / Outcome (e.g. "sdv_gavel_benchmark", "safe_harbor_breach", "deemed_consideration_stamp")
- EVERY element must have a "label" containing the EXACT words, sections, and numbers spoken by the teacher at that exact moment.
- The teacher narration MUST chronologically walk through these elements so that the Whisper acoustic aligner places each element at its exact second, with NO silent visual gaps greater than 4 seconds!
- NEVER speak for more than 4-5 seconds without a new animated visual element popping up!

========================================================================================
CRITICAL PEDAGOGICAL RULE 5: AUTHENTIC, WARM MALAYALAM TEACHER DIALOGUE (NATURAL MANGLISH)
========================================================================================
- Sound like a REAL, ENERGETIC, PASSIONATE KERALA CA FACULTY teaching in a live CA Final classroom!
- Natural Manglish code-switching: Friendly Malayalam teacher scaffolding with standard English legal/tax terminology.
- MANDATORY LANGUAGE RULES:
  * SECTIONS & PROVISIONS: In English ('Section 54G', 'Section 50', 'Section 45(2)', 'Section 50C', 'Section 54EC'). Never transliterate into Malayalam script.
  * DATES & YEARS: In English ('1st April 2001', 'Assessment Year 2026-27', 'Financial Year 2025-26', 'March 2026', '10th August 2025'). Never translate dates into Malayalam words.
  * TAX & FINANCIAL TERMS: In English ('Capital Gains', 'Short-term Capital Gain', 'Long-term Capital Gain', 'Written Down Value', 'Sale Consideration', 'Cost of Acquisition', 'Exemption', 'Deduction', 'Turnover').
  * SEQUENTIAL ORDINAL CUES: Use natural Malayalam ordinal markers to cleanly introduce each asset or step:
    'Onnamathathu...', 'Randamathathu...', 'Moonnamathathu...', 'Naalaamathathu...', or 'Aadyam...', 'Aduthathayi...', 'Avasanam...'
  * NO ROBOTIC OR BROKEN WORDS: Use 'athayath' (NOT 'ithathayath'), 'ormavekkoo' (NOT 'ormathoykkoo'), 'taxable aanu' (NOT 'taxable aane'), 'vaangiya' / 'purchase cheytha' (NOT 'purchase chethya').

========================================================================================
OUTPUT FORMAT: PURE JSON
========================================================================================
Return STRICT VALID JSON matching this structure (elastic 4 to 8 beats as required by the topic):
{{
  "context_pill": "Section Name | Topic Name",
  "beats": [
    {{
      "id": "b1",
      "layout": "story_scene",
      "scene_type": "factory_shift",
      "kicker": "FACTUAL NARRATIVE & STATUTORY CONTEXT",
      "badge": "Case Overview",
      "title": {{"text": "Industrial Undertaking Shifting: Urban to Rural Area"}},
      "voice_sync_text": "Malayalam teacher narration setting up the scenario, assessee enterprise, and urban to rural shifting...",
      "elements": {{
        "divider": {{"label": "Scenario division boundary"}},
        "urban_reg": {{"label": "Urban corporation limit original site"}},
        "urban_factory": {{"label": "Urban industrial factory"}},
        "assets_box": {{"label": "Land Building Plant Machinery Furniture sale proceeds"}},
        "shift_arrow": {{"label": "Shifting relocation across boundary"}},
        "rural_reg": {{"label": "Non-urban rural area new site"}},
        "rural_factory": {{"label": "New rural undertaking factory"}},
        "pool_box": {{"label": "Eligible reinvestment pool Section 54G"}}
      }}
    }},
    {{
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Malayalam teacher narration explaining the statutory text, conditions, and reinvestment time horizon...",
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
        'gemini-flash-lite-latest',
        'gemini-3.1-flash-lite',
        'gemini-3.5-flash-lite',
        'gemini-3.8-flash',
        'gemini-3.5-flash',
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
