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

PEDAGOGICAL_PROMPT = """You are a senior, beloved CA Final Tax Professor and Visual Explainer Architect for Indian Direct Tax.
Your student needs to master this complex statutory provision.

Question/Context:
{question_text}

Answer/Statutory Solution:
{answer_text}

Statutory Matrix:
{provision_matrix}

========================================================================================
CRITICAL PEDAGOGICAL RULE 1: CREATE A DISTINCT, COMPLETE STORY EXAMPLE
========================================================================================
- DO NOT reuse the exact names or identical figures from the exam question!
- Create a distinct, memorable persona / enterprise (e.g. 'Apex Engineering Ltd', 'Rajesh / Zenith Textiles', 'Kavya Motors').
- Use different realistic amounts and years that mirror the legal principles of the section.
- For Section 54G, include 4 distinct assets sold (Land, Building, Plant & Machinery, Furniture) and new assets acquired in the non-urban area.

========================================================================================
CRITICAL PEDAGOGICAL RULE 2: FIRST JOB OF PRESENTATION IS A COMPLETE OVERVIEW UPFRONT (BEAT 1)
========================================================================================
- The FIRST BEAT (Beat 1) MUST provide a complete, crystal-clear overview of the entire story example!
- Every amount and situation MUST be laid out transparently right upfront:
  * Who is the assessee and what is the situation (e.g. Shifting industrial undertaking from urban corporation limits to rural non-urban area)?
  * EVERY asset sold, including Sale Proceeds and WDV/Cost:
    - Land (Long-term non-depreciable asset)
    - Building (Depreciable asset u/s 50)
    - Plant & Machinery (Depreciable asset u/s 50)
    - Furniture (Depreciable asset, but strictly excluded from Section 54G!)
  * EVERY new asset acquired in the non-urban area (Land, Building, Plant & Machinery, Furniture).
- The student must see the full financial and factual chessboard before diving into statutory analysis!

========================================================================================
CRITICAL PEDAGOGICAL RULE 3: TEACH THE STATUTORY PROVISION STEP-BY-STEP USING THE EXAMPLE
========================================================================================
Follow a logical 5-beat sequential journey:
- Beat 1 ("fork"): COMPLETE FACT OVERVIEW & ASSET FILTER
  Lay out the complete story scenario and separate the 3 Eligible Specified Assets (Land, Building, Plant & Machinery) from the 1 Ineligible Non-Specified Asset (Furniture & Fixtures).
- Beat 2 ("statute_quote"): STATUTORY MANDATE & TIME HORIZON GATE
  Show Section 54G(1) statutory conditions: Transfer of industrial undertaking from urban area + Reinvestment window (within 1 year before or 3 years after the date of transfer). Verify that the example's acquisition satisfies this window!
- Beat 3 ("meter"): REINVESTMENT POOL & ELIGIBILITY CEILING
  Compute the Eligible Reinvestment Pool (Land + Building + Plant acquired; Furniture strictly excluded).
- Beat 4 ("ledger"): STEP-BY-STEP COMPUTATION & THE GOLDEN OPTIMIZATION TRICK
  Step-by-step computation of capital gains:
  * Building STCG u/s 50
  * Plant & Machinery STCG u/s 50
  * Total Deemed STCG eligible for Section 54G
  * Less: Section 54G Exemption Priority 1 (Against 30% STCG)
  * Net STCG = Nil
  * Land LTCG (Sale − Cost)
  * Less: Balance Section 54G Exemption
  * Taxable LTCG on Land (12.5% u/s 112)
  * Furniture STCG (Sale − WDV) [No Section 54G exemption!]
  CRITICAL TEACHER INSIGHT: Explain the Golden Optimization Trick via a callout banner:
  "The statute does NOT compel pro-rata apportionment! The assessee can exhaust the deduction in the most beneficial manner. Always exhaust Section 54G against 30% Short-Term Capital Gains first before offsetting 12.5% Long-Term Capital Gains!"
  Calculate the Net Taxable Capital Gains!
- Beat 5 ("takeaway"): 3 GOLDEN EXAM RULES
  Summarize the 3 non-negotiable statutory doctrines for CA Final exams:
  01: Strict Asset Basket (Furniture strictly excluded from sale and reinvestment)
  02: Section 50 Deemed STCG is fully eligible for Section 54G exemption
  03: Most Beneficial Set-Off Priority (wiping out higher tax bracket STCG first)

========================================================================================
CRITICAL PEDAGOGICAL RULE 4: STRICT 1:1 VOICE-TO-SCREEN CORRESPONDENCE
========================================================================================
- WHATEVER IS SPOKEN IN voice_sync_text MUST BE SHOWN ON SCREEN IN DIRECT 1:1 CORRESPONDENCE!
- When the teacher mentions an asset, an amount, a condition, or a rule, that element MUST appear visually on screen.
- Never mention numbers or facts in voice that are missing from the visual layout!
- Provide a callout banner or note during verbal explanations so the screen is never dead or unaligned.

========================================================================================
========================================================================================
CRITICAL PEDAGOGICAL RULE 5: AUTHENTIC, WARM MALAYALAM TEACHER DIALOGUE (NATURAL MANGLISH)
========================================================================================
- The voice MUST sound like a REAL, ENERGETIC, PASSIONATE KERALA CA FACULTY teaching in a live CA Final classroom!
- DO NOT generate robotic, awkward, or machine-translated Malayalam sentences.
- NEVER use clumsy translated words like 'tanted', 'athinukku', 'conditions fill cheyyan', or 'decide cheythu'.
- USE NATURAL, IDIOMATIC SPOKEN CLASSROOM MALAYALAM PHRASING:
  * "Students, welcome back! Namukku Section 54G Capital Gains Exemption nannayi padikkaam..."
  * "Concept crystal clear aavaan namukk Apex Engineering Ltd-inte oru practical case study nokkaam..."
  * "Kando, ivide company 4 assets aanu transfer cheythath..."
  * "First asset: Land, sale consideration Rs 20 Lakhs, cost of acquisition Rs 15 Lakhs, so Long-term Capital Gain Rs 5 Lakhs..."
  * "Second asset: Factory Building, sale proceeds Rs 25 Lakhs, Written Down Value Rs 9 Lakhs, so Section 50 prakaram Deemed Short-term Capital Gain Rs 16 Lakhs..."
  * "Ennaal Furniture non-specified asset aayathukond athinu Section 54G exemption oru kaaranavashaalum labhikkilla!"
  * "Transfer date-inu shesham verum 4 months-il reinvestment nadannathinaal ithu 3-year statutory window-kkullil perfect aayi qualify cheyyunnu!"
  * "Income-tax Act-il pro-rata set-off niyamam illathathinaal 30% slab rate ulla Short-term Capital Gain aadyam wipe out cheythu tax liability minimize cheyyaam!"
- Keep EVERY statutory term, section, sub-section, asset name, and amount in English Latin script.
- The delivery must be warm, enthusiastic, engaging, and pedagogically crystal clear.

========================================================================================
CRITICAL PEDAGOGICAL RULE 6: VISUAL REPRESENTATION OF EVERY SPOKEN ASSET & AMOUNT
========================================================================================
- IN BEAT 1 ("fork"): story_steps MUST CONTAIN 4 CARDS SHOWING EVERY ASSET SOLD WITH ITS NUMBERS!
  * Card 1: Land: Sale, Cost, LTCG
  * Card 2: Building: Sale, WDV, Deemed STCG
  * Card 3: Plant & Machinery: Sale, WDV, Deemed STCG
  * Card 4: Furniture: Sale, WDV, STCG (Flagged as Non-Specified / Ineligible)
  * Divider: "Asset Classification & Eligibility Filter under Section 54G"
  * Left Branch: Eligible Specified Assets (Land, Building, Plant & Machinery)
  * Right Branch: Ineligible Non-Specified Asset (Furniture & Fixtures)
  * Result Card: Exam Trap Alert (Furniture strictly excluded from Section 54G basket!)
- IN BEAT 3 ("meter"): breakdown MUST show each new asset acquired with its exact figure!
- IN BEAT 4 ("ledger"): ledger_rows MUST show the step-by-step math and the Golden Optimization Trick callout!
- IN BEAT 5 ("takeaway"): rules MUST show the 3 Golden Rules!

========================================================================================
OUTPUT FORMAT: PURE JSON
========================================================================================
Return STRICT VALID JSON matching this exact structure:
{{
  "context_pill": "Section 54G | Shifting of Industrial Undertaking",
  "beats": [
    {{
      "id": "b1",
      "layout": "fork",
      "voice_sync_text": "Students, welcome back! Namukku Section 54G Capital Gains Exemption nannayi padikkaam. Concept crystal clear aavaan namukk Apex Engineering Ltd-inte oru practical case study nokkaam. Kando, Apex Engineering Ltd urban corporation limit-il ulla thangalude factory oru non-urban rural area-yilekku shift cheyyan theerumaanichu. Shifting-inte bhaagamaayi March 2026-il company 4 assets aanu sell cheythath: First, Land, sale consideration Rs 20 Lakhs, cost of acquisition Rs 15 Lakhs, so Long-term Capital Gain Rs 5 Lakhs. Second, Factory Building, sale proceeds Rs 25 Lakhs, Written Down Value Rs 9 Lakhs, so Section 50 prakaram Deemed Short-term Capital Gain Rs 16 Lakhs. Third, Plant & Machinery, sale value Rs 18 Lakhs, Written Down Value Rs 9 Lakhs, so Short-term Capital Gain Rs 9 Lakhs. Fourth, Furniture, sale Rs 3 Lakhs, Written Down Value Rs 2 Lakhs, so Short-term Capital Gain Rs 1 Lakh. Ippo asset classification filter nokkoo: Section 54G prakaram Land, Building, and Plant & Machinery maathrame Eligible Specified Assets aayi qualify cheyyoo! Ennaal Furniture non-specified asset aayathukond athinu Section 54G exemption oru kaaranavashaalum labhikkilla!",
      "title": {{"text": "Asset Eligibility Filter under Section 54G"}},
      "story_steps": [
        {{"badge": "Asset 1: Land", "title": "Sale: Rs 20L | Cost: Rs 15L", "sub": "Long-term Capital Gain: Rs 5 Lakhs", "val": 500000}},
        {{"badge": "Asset 2: Building", "title": "Sale: Rs 25L | WDV: Rs 9L", "sub": "Deemed STCG u/s 50: Rs 16 Lakhs", "val": 1600000}},
        {{"badge": "Asset 3: Plant & Mach.", "title": "Sale: Rs 18L | WDV: Rs 9L", "sub": "Deemed STCG u/s 50: Rs 9 Lakhs", "val": 900000}},
        {{"badge": "Asset 4: Furniture", "title": "Sale: Rs 3L | WDV: Rs 2L", "sub": "STCG: Rs 1 Lakh (Non-Specified)", "val": 100000}}
      ],
      "divider": {{"text": "Asset Classification & Eligibility Filter under Section 54G"}},
      "branches": [
        {{"side": "left", "label": "Eligible Specified Assets", "facts": [{{"text": "Land, Building, Plant & Machinery"}}, {{"text": "Total Qualifying Gains: Rs 30 Lakhs"}}, {{"text": "Qualifies for Section 54G Exemption"}}], "outcome": {{"text": "Eligible for Section 54G Exemption"}}}},
        {{"side": "right", "label": "Ineligible Non-Specified Asset", "facts": [{{"text": "Office Furniture & Fixtures"}}, {{"text": "Excluded from Section 54G Definition"}}, {{"text": "Neither transfer nor reinvestment qualifies"}}], "outcome": {{"text": "No Exemption! Full STCG Taxable"}}}}
      ],
      "result_card": {{"badge": "Exam Trap Alert", "title": "Furniture Strictly Excluded", "sub": "Furniture is strictly excluded from Section 54G exemption basket!"}}
    }},
    {{
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Malayalam teacher narration text for beat 2 explaining the statutory mandate and reinvestment window...",
      "title": {{"text": "Statutory Mandate & Reinvestment Window u/s 54G(1)"}},
      "quote": {{
        "text": "Where the capital gain arises from the transfer of a capital asset, being plant, machinery, land or building or any rights in building or land, used for the purpose of an industrial undertaking situated in an urban area... and the assessee has within a period of one year before or three years after the date on which the transfer took place purchased new machinery or plant or acquired building or land...",
        "citation": "Section 54G(1) of the Income-tax Act, 1961",
        "emphasis": "plant, machinery, land or building... 1 year before or 3 years after"
      }},
      "context_bubble": {{
        "badge": "Statutory Reinvestment Window",
        "speaker": "Section 54G(1)",
        "theme": "Time Horizon Condition",
        "text": "Reinvestment Window: 1 Year Before or 3 Years After Transfer Date"
      }}
    }},
    {{
      "id": "b3",
      "layout": "meter",
      "voice_sync_text": "Malayalam teacher narration text for beat 3 calculating the eligible reinvestment pool...",
      "title": {{"text": "Section 54G Eligible Reinvestment Pool"}},
      "meter_display": {{
        "min_val": 0,
        "max_val": 3500000,
        "current_val": 3100000,
        "unit": "₹",
        "threshold": 2500000,
        "labels": {{"start": "₹ 0", "threshold_label": "STCG Threshold: ₹ 25L", "current_label": "Total Eligible Investment: ₹ 31L"}}
      }},
      "breakdown": [
        {{"label": "New Land Acquired", "val": 500000, "status": "Qualifies u/s 54G"}},
        {{"label": "New Building Acquired", "val": 800000, "status": "Qualifies u/s 54G"}},
        {{"label": "New Plant & Machinery", "val": 1800000, "status": "Qualifies u/s 54G"}},
        {{"label": "New Furniture Purchased", "val": 300000, "status": "Ineligible (Excluded from 54G)"}}
      ],
      "outcome": {{"text": "Eligible to Set-off against both STCG & LTCG", "tone": "ok"}}
    }},
    {{
      "id": "b4",
      "layout": "ledger",
      "voice_sync_text": "Malayalam teacher narration text for beat 4 explaining the golden optimization trick and computing the taxable gains...",
      "title": {{"text": "Computation of Taxable Capital Gains for AY 2026-27"}},
      "callout": {{
        "badge": "Golden Optimization Trick",
        "text": "Act-il pro-rata set-off niyamam illa: Higher tax bracket Short-term Capital Gain first wipe out cheyyanam!"
      }},
      "ledger_rows": [
        {{"label": "Building STCG u/s 50 (Sale − WDV)", "amount": 1600000, "type": "income"}},
        {{"label": "Plant & Machinery STCG u/s 50 (Sale − WDV)", "amount": 900000, "type": "income"}},
        {{"label": "Total Deemed STCG Eligible for Section 54G", "amount": 2500000, "type": "subtotal"}},
        {{"label": "Less: Section 54G Exemption (Priority 1: Against 30% STCG)", "amount": -2500000, "type": "deduction"}},
        {{"label": "Net STCG on Industrial Assets", "amount": 0, "type": "subtotal"}},
        {{"label": "Land LTCG (Sale − Cost)", "amount": 500000, "type": "income"}},
        {{"label": "Less: Balance Section 54G Exemption", "amount": -400000, "type": "deduction"}},
        {{"label": "Taxable LTCG on Land (Taxable @ 12.5% u/s 112)", "amount": 100000, "type": "taxable"}},
        {{"label": "Furniture STCG (Sale − WDV) [No 54G Exemption]", "amount": 100000, "type": "taxable"}}
      ],
      "net_total": {{
        "label": "Total Taxable Capital Gains",
        "val": 200000,
        "detail": "Taxable Remainder"
      }}
    }},
    {{
      "id": "b5",
      "layout": "takeaway",
      "voice_sync_text": "Malayalam teacher narration text for beat 5 giving the 3 Golden Rules...",
      "title": {{"text": "3 Golden Rules for Section 54G Exam Mastery"}},
      "rules": [
        {{"num": "01", "heading": "Strict Asset Basket (Furniture Excluded)", "body": "Furniture-nu Section 54G-il sthanamilla. Neither transfer nor reinvestment in Furniture qualifies."}},
        {{"num": "02", "heading": "Section 50 Deemed STCG is Fully Eligible", "body": "Section 50 prakaram depreciable assets STCG aayal polum, Section 54G exemption valid aanu."}},
        {{"num": "03", "heading": "Most Beneficial Set-Off Priority", "body": "Tax liability minimize cheyyan deduction aadyam 30% STCG-kk ethireyum, balance 12.5% LTCG-kk ethireyum set-off cheyyam!"}}
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
            if res and res.get('beats'):
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
