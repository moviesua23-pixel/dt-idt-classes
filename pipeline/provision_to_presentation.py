#!/usr/bin/env python3
"""
pipeline/provision_to_presentation.py
Converts any pasted statutory tax provision (Direct Tax / Indirect Tax) into a complete
multi-slide educational video presentation with:
1. Real-life relatable story formulated by Gemini AI.
2. Multi-slide pedagogical screenplay (slide count & archetype selection from 15 templates).
3. Slot customization adapted to the story (names, amounts, headers, dates).
4. Authentic Malayalam teacher dialogues (Manglish standard CA Final style).
5. Actual Malayalam voice audio synthesis (.mp3) for each slide.
6. Synchronized presentation screenplay JSON for web playback.
"""

import os
import sys
import json
import re
import argparse
import subprocess
import asyncio
from typing import Dict, Any, List, Optional

try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Voice Clarity & Text Normalization Engine
# -------------------------------------------------------------------------
def normalize_script_for_clarity(text: str) -> str:
    """
    Normalizes statutory presentation dialogue for crystal-clear TTS pronunciation:
    - Expands numeric dates like 01/04/2014 or 1-4-2014 into spoken English: '1st April 2014'
    - Normalizes Indian currency formatting: ₹ 5 Lakhs -> 5 Lakh Rupees
    - Adds natural phonetic spacing around English/Malayalam hyphenated suffixes (e.g. 'Plot-ൽ' -> 'Plot - ൽ')
    - Cleans up weird generative artifacts (e.g. 'magnetic plot', 'dynamic asset')
    """
    if not text:
        return ""
    t = text
    
    # 1. Expand numeric dates to English words (critical for clear pronunciation)
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    def _date_sub(m):
        d, mo, yr = int(m.group(1)), int(m.group(2)), m.group(3)
        suf = 'st' if d in (1, 21, 31) else ('nd' if d in (2, 22) else ('rd' if d in (3, 23) else 'th'))
        return f"{d}{suf} {months[mo]} {yr}"
    t = re.sub(r'\b(0?[1-9]|[12][0-9]|3[01])[-/.](0?[1-9]|1[0-2])[-/.]((?:19|20)\d{2})\b', _date_sub, t)
    
    # 2. Currency symbol normalization
    t = re.sub(r'₹\s*([0-9]+(?:\.[0-9]+)?)\s*(?:Cr|Crore|Crores)\b', r'\1 Crore Rupees', t, flags=re.IGNORECASE)
    t = re.sub(r'₹\s*([0-9]+(?:\.[0-9]+)?)\s*(?:Lakh|Lakhs|Lac|Lacs)\b', r'\1 Lakh Rupees', t, flags=re.IGNORECASE)
    t = re.sub(r'₹\s*([0-9,]+)', r'\1 Rupees', t)
    
    # 3. Clean section references
    t = re.sub(r'\bu/s\.?\s*', 'Section ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bSec\.?\s*', 'Section ', t, flags=re.IGNORECASE)
    
    # 4. Remove hallucinated template terms
    t = re.sub(r'\bmagnetic plot\b', 'commercial plot', t, flags=re.IGNORECASE)
    t = re.sub(r'\bdynamic asset\b', 'asset', t, flags=re.IGNORECASE)
    
    # 5. Phonetic boundary smoothing for mixed English + Malayalam suffixes
    # Giving a tiny phonetic breathing room prevents the neural voice from swallowing English consonants
    t = re.sub(r'([A-Za-z0-9])-(ൽ|ന്റെ|ക്ക്|ന്|നെ|യോ|ഉം)', r'\1 - \2', t)
    
    # 6. Spacing cleanup
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def synthesize_malayalam_voice(script: str, output_mp3_path: str, voice_name: str = "Aoede") -> float:
    """
    Synthesizes studio-grade expressive Malayalam teacher narration audio for a presentation slide
    strictly using Gemini Expressive Voice TTS (gemini-3.1-flash-tts-preview) with automatic KeyRotator.
    Zero robotic fallback.
    Returns the exact audio duration in seconds.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp3_path)), exist_ok=True)
    clean_text = normalize_script_for_clarity(script)
    
    # Supported expressive Gemini voices: Aoede (default, warm & clear), Kore, Puck
    selected_voice = voice_name if voice_name in ["Aoede", "Kore", "Puck", "Fenrir", "Charon"] else "Aoede"
    
    from pipeline.phase3_audio import generate_gemini_audio
    dur, engine = generate_gemini_audio(clean_text, output_mp3_path, voice_name=selected_voice)
    if os.path.exists(output_mp3_path) and os.path.getsize(output_mp3_path) > 1000:
        print(f"   [Gemini Expressive Voice] Synthesized via {engine}: {dur:.1f}s")
        return dur
        
    raise RuntimeError(f"Gemini Expressive Voice generation failed for: {output_mp3_path}")


# -------------------------------------------------------------------------
# Heuristic Multi-Slide Presentation Generator Fallback
# -------------------------------------------------------------------------
def parse_val_to_num(v: Any) -> int:
    if isinstance(v, (int, float)):
        return int(v)
    if not v:
        return 0
    s = str(v).lower().replace(',', '').replace('₹', '').strip()
    if 'crore' in s or 'cr' in s:
        nums = re.findall(r'[\d\.]+', s)
        if nums:
            return int(float(nums[0]) * 10000000)
    if 'lakh' in s or 'lac' in s:
        nums = re.findall(r'[\d\.]+', s)
        if nums:
            return int(float(nums[0]) * 100000)
    nums = re.findall(r'\d+', s)
    if nums:
        return int(nums[0])
    return 0

def normalize_slide_slots(archetype_id: str, raw_slots: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes slide slots from Gemini or heuristic outputs into canonical kinetic schemas:
    - Normalizes alias keys ('chunks' -> 'steps', 'streams' -> 'inputs', 'whole_val' -> 'start_amount')
    - Standardizes conditions ([{ label, passed }]) to prevent gate lockouts or placeholder displays
    - Strictly coerces numeric strings ('₹ 5 Lakhs', '3000000') into pure integers
    """
    slots = dict(raw_slots or {})
    
    if archetype_id == "conditions_gate":
        conds = slots.get("conditions") or slots.get("checklist") or slots.get("criteria") or []
        norm_conds = []
        for idx, c in enumerate(conds):
            if isinstance(c, dict):
                label = c.get("label") or c.get("text") or c.get("title") or c.get("criterion") or f"Criterion {idx+1}"
                passed = c.get("passed") if "passed" in c else (c.get("met") if "met" in c else (c.get("is_met") if "is_met" in c else True))
                norm_conds.append({"label": str(label), "passed": bool(passed)})
            elif isinstance(c, str):
                norm_conds.append({"label": c, "passed": True})
        if norm_conds:
            slots["conditions"] = norm_conds
            
    elif archetype_id == "take_away":
        start_amt = slots.get("start_amount") if "start_amount" in slots else (slots.get("whole_val") if "whole_val" in slots else slots.get("whole_amount"))
        if start_amt is not None:
            slots["start_amount"] = parse_val_to_num(start_amt)
        if "whole_label" in slots and "start_label" not in slots:
            slots["start_label"] = slots["whole_label"]
        raw_steps = slots.get("steps") or slots.get("chunks") or slots.get("deductions") or []
        norm_steps = []
        for s in raw_steps:
            if isinstance(s, dict):
                lbl = s.get("label") or s.get("title") or s.get("text") or "Deduction Step"
                amt = parse_val_to_num(s.get("amount") if "amount" in s else s.get("val", 0))
                norm_steps.append({"label": str(lbl), "amount": amt})
        if norm_steps:
            slots["steps"] = norm_steps
            
    elif archetype_id == "split_into_parts":
        whole = slots.get("whole_amount") if "whole_amount" in slots else slots.get("whole_val")
        if whole is not None:
            slots["whole_amount"] = parse_val_to_num(whole)
        raw_parts = slots.get("parts") or slots.get("chunks") or slots.get("branches") or []
        norm_parts = []
        for p in raw_parts:
            if isinstance(p, dict):
                lbl = p.get("label") or p.get("title") or p.get("text") or "Allocation Branch"
                amt = parse_val_to_num(p.get("amount") if "amount" in p else p.get("val", 0))
                norm_parts.append({"label": str(lbl), "amount": amt})
        if norm_parts:
            slots["parts"] = norm_parts

    elif archetype_id == "merge_into_one":
        raw_inputs = slots.get("inputs") or slots.get("streams") or slots.get("items") or []
        norm_inputs = []
        for i in raw_inputs:
            if isinstance(i, dict):
                lbl = i.get("label") or i.get("title") or i.get("text") or "Input Stream"
                amt = parse_val_to_num(i.get("amount") if "amount" in i else i.get("val", 0))
                norm_inputs.append({"label": str(lbl), "amount": amt})
        if norm_inputs:
            slots["inputs"] = norm_inputs
        if "merged_label" in slots and "result_label" not in slots:
            slots["result_label"] = slots["merged_label"]

    elif archetype_id == "add_up":
        raw_items = slots.get("items") or slots.get("rows") or slots.get("steps") or []
        norm_items = []
        for it in raw_items:
            if isinstance(it, dict):
                lbl = it.get("label") or it.get("title") or it.get("text") or "Component"
                amt = parse_val_to_num(it.get("amount") if "amount" in it else it.get("val", 0))
                norm_items.append({"label": str(lbl), "amount": amt})
        if norm_items:
            slots["items"] = norm_items

    elif archetype_id == "compare_two":
        if "val_a" in slots:
            slots["val_a"] = parse_val_to_num(slots["val_a"])
        elif "val_1" in slots:
            slots["val_a"] = parse_val_to_num(slots["val_1"])
        if "val_b" in slots:
            slots["val_b"] = parse_val_to_num(slots["val_b"])
        elif "val_2" in slots:
            slots["val_b"] = parse_val_to_num(slots["val_2"])
        if "cap_amount" in slots and slots["cap_amount"]:
            slots["cap_amount"] = parse_val_to_num(slots["cap_amount"])

    elif archetype_id == "give_and_receive":
        if "item_value" in slots:
            slots["item_value"] = parse_val_to_num(slots["item_value"])
        if "payment_amount" in slots:
            slots["payment_amount"] = parse_val_to_num(slots["payment_amount"])

    elif archetype_id == "chain_passing":
        if "tag_value" in slots:
            slots["tag_value"] = parse_val_to_num(slots["tag_value"])
        elif "item_value" in slots:
            slots["tag_value"] = parse_val_to_num(slots["item_value"])

    elif archetype_id == "formula_builder":
        raw_chips = slots.get("chips") or slots.get("items") or []
        norm_chips = []
        for idx, ch in enumerate(raw_chips):
            if isinstance(ch, dict):
                has_val = ("val" in ch or "amount" in ch)
                has_label = bool(ch.get("label") or ch.get("title"))
                op = ch.get("op")
                
                if op and not has_val and not has_label:
                    norm_chips.append({"op": "−" if op == "-" else op})
                elif op and (has_val or has_label):
                    if op != "+" or idx > 0:
                        norm_chips.append({"op": "−" if op == "-" else op})
                    norm_chips.append({
                        "label": ch.get("label") or ch.get("title") or "",
                        "val": parse_val_to_num(ch.get("val") or ch.get("amount", 0)),
                        "is_total": bool(ch.get("is_total", False))
                    })
                else:
                    norm_chips.append({
                        "label": ch.get("label") or ch.get("title") or "",
                        "val": parse_val_to_num(ch.get("val") or ch.get("amount", 0)),
                        "is_total": bool(ch.get("is_total", False))
                    })
        if norm_chips:
            slots["chips"] = norm_chips

    elif archetype_id == "time_range":
        if "span_length" in slots:
            slots["span_length"] = parse_val_to_num(slots["span_length"])
        if "event_offset" in slots:
            slots["event_offset"] = parse_val_to_num(slots["event_offset"])
        if "is_inside" in slots:
            slots["is_inside"] = bool(slots["is_inside"])

    return slots


def generate_multi_slide_heuristic(provision_text: str, subject: str = "DT", domain: str = "Real Estate") -> Dict[str, Any]:
    """Generates a complete 3-slide pedagogical screenplay using rule-based analysis."""
    text_lower = provision_text.lower()
    
    # Extract numbers
    numbers = [int(re.sub(r'[^\d]', '', n)) for n in re.findall(r'₹?\s*[\d,]+', provision_text) if len(re.sub(r'[^\d]', '', n)) >= 4]
    val1 = numbers[0] if len(numbers) > 0 else 4000000
    val2 = numbers[1] if len(numbers) > 1 else 6000000

    if "stamp duty" in text_lower or "50c" in text_lower or "sdv" in text_lower or "benchmark" in text_lower:
        return {
            "title": "Section 50C - Deemed Full Value of Consideration",
            "subject": subject,
            "story_summary": "Rahul agreed to sell his residential commercial land in Kochi to Anita for ₹40 Lakhs. However, the State Valuation Authority standard benchmark was ₹60 Lakhs. Under Section 50C, the higher benchmark value overrides the agreed price for Capital Gains computation.",
            "slides": [
                {
                    "slide_number": 1,
                    "slide_title": "Step 1: Asset Sale & Agreed Price Handover",
                    "scene_purpose": "Rahul hands over property title deeds to Anita in exchange for agreed ₹40 Lakhs payment.",
                    "archetype_id": "give_and_receive",
                    "dialogue_manglish": "Nammal Rahul-inte case edukkuka. Rahul Kochi-yile tande commercial plot Anita-kk ₹40 Lakhs-inaa transfer cheythu. Anita agreed consideration full-aayi settlement cheythu.",
                    "slots": {
                        "title": "Step 1: Real Estate Transfer Agreement",
                        "giver": "Rahul (Seller)",
                        "receiver": "Anita (Buyer)",
                        "item_label": "Commercial Plot",
                        "item_icon": "house",
                        "item_value": val1,
                        "payment_amount": val1,
                        "tag_text": "Agreed Sale Handover Complete",
                        "note": "Actual consideration received fulfills sale deed agreement."
                    }
                },
                {
                    "slide_number": 2,
                    "slide_title": "Step 2: Actual Price vs Stamp Duty Benchmark Comparison",
                    "scene_purpose": "Comparing agreed price ₹40L against official Government Stamp Duty Value ₹60L on tilting balance scale.",
                    "archetype_id": "compare_two",
                    "dialogue_manglish": "Pakshe Sub-Registrar Office-le official Stamp Duty Value ₹60 Lakhs aayirunnu. Agreed price benchmark-nekkal kuravanu! Ithil higher value aaya ₹60 Lakhs adopt cheyyanam.",
                    "slots": {
                        "title": "Step 2: Valuation Benchmark Review",
                        "label_a": "Agreed Price",
                        "val_a": val1,
                        "label_b": "Stamp Duty Value",
                        "val_b": val2,
                        "mode": "higher",
                        "cap_amount": None,
                        "note": "Sub-Registrar valuation authority standard verified."
                    }
                },
                {
                    "slide_number": 3,
                    "slide_title": "Step 3: Section 50C Statutory Takeaway Principle",
                    "scene_purpose": "The core rule takeaway: higher benchmark is deemed as Full Value of Consideration for Capital Gains.",
                    "archetype_id": "key_statement",
                    "dialogue_manglish": "Section 50C prakaaram actual sale price Stamp Duty Value-nekkal kuravanengil, higher benchmark thanne Deemed Full Value of Consideration aayi Capital Gains calculate cheyyam.",
                    "slots": {
                        "title": "Section 50C Core Statutory Rule",
                        "statement": "Where sale price is less than Stamp Duty Value, the official benchmark becomes Deemed Full Value of Consideration.",
                        "highlight_phrase": "Deemed Full Value of Consideration",
                        "support_line": "Higher standard benchmark overrides actual deed value for Capital Gains.",
                        "icon_type": "scale"
                    }
                }
            ]
        }
    elif "within" in text_lower or "years" in text_lower or "54" in text_lower or "period" in text_lower or "timeline" in text_lower:
        return {
            "title": "Section 54 - Capital Gains Reinvestment Window",
            "subject": subject,
            "story_summary": "Priya sold her residential house and realized long-term capital gains. To claim tax exemption under Section 54, she reinvested the proceeds into a new residential house within 18 months, safely inside the 2-year statutory relief window.",
            "slides": [
                {
                    "slide_number": 1,
                    "slide_title": "Step 1: Residential House Sale",
                    "scene_purpose": "Priya sells residential house to realize capital gains.",
                    "archetype_id": "give_and_receive",
                    "dialogue_manglish": "Priya tande residential house ₹50 Lakhs-in transfer cheythu long-term capital gains generate cheythu. Ee gain tax-free aakkan Section 54 exemption claim cheyyam.",
                    "slots": {
                        "title": "Step 1: Residential House Transfer",
                        "giver": "Priya (Assessee)",
                        "receiver": "Purchaser",
                        "item_label": "Residential House",
                        "item_icon": "house",
                        "item_value": 5000000,
                        "payment_amount": 5000000,
                        "tag_text": "Capital Asset Transfer Complete",
                        "note": "Capital gains realized on transfer date."
                    }
                },
                {
                    "slide_number": 2,
                    "slide_title": "Step 2: 24-Month Statutory Reinvestment Timeline",
                    "scene_purpose": "Timeline axis showing 24-month window and new house purchase event at 18 months.",
                    "archetype_id": "time_range",
                    "dialogue_manglish": "Section 54 prakaaram transfer date muthal 2 years-inte window labhikkum. Priya 18 months-inullil puthiya house purchase cheythu, relief window-kkullil event complete aayi.",
                    "slots": {
                        "title": "Step 2: Prescribed Reinvestment Window",
                        "start_label": "House Transfer Date",
                        "span_length": 24,
                        "span_unit": "Months",
                        "span_label": "2-Year Exemption Window",
                        "event_label": "New House Purchase",
                        "event_offset": 18,
                        "is_inside": True,
                        "note": "Investment successfully executed before statutory expiry."
                    }
                },
                {
                    "slide_number": 3,
                    "slide_title": "Step 3: Section 54 Exemption Granted",
                    "scene_purpose": "Statutory principle confirming 100% Capital Gains relief.",
                    "archetype_id": "key_statement",
                    "dialogue_manglish": "Time limit-il thanne reinvestment nadathiyathukondu, Priya-kk capital gains exemption fully allowed aayi, tax liability zero aakunnu.",
                    "slots": {
                        "title": "Section 54 Statutory Exemption Verified",
                        "statement": "Reinvestment executed within the prescribed 2-year statutory period qualifies for full Capital Gains tax exemption.",
                        "highlight_phrase": "full Capital Gains tax exemption",
                        "support_line": "Statutory compliance verified across transfer and acquisition dates.",
                        "icon_type": "house"
                    }
                }
            ]
        }
    elif "conditions" in text_lower or "checklist" in text_lower or "16(2)" in text_lower or "eligible if" in text_lower:
        return {
            "title": "GST Section 16(2) - Input Tax Credit Eligibility Gate",
            "subject": subject,
            "story_summary": "Apex Logistics received an industrial equipment consignment. To unlock Input Tax Credit (ITC), the entity verified all 4 statutory conditions: tax invoice possession, goods receipt, supplier tax payment, and return filing.",
            "slides": [
                {
                    "slide_number": 1,
                    "slide_title": "Step 1: Business Consignment Procurement",
                    "scene_purpose": "Delivery of industrial equipment with tax invoice.",
                    "archetype_id": "give_and_receive",
                    "dialogue_manglish": "Apex Logistics machinery supplier-il ninnu ₹15 Lakhs value-il tax invoice sametham consignment receive cheyyunnu.",
                    "slots": {
                        "title": "Step 1: Equipment Procurement Handover",
                        "giver": "Machinery Supplier",
                        "receiver": "Apex Logistics",
                        "item_label": "Industrial Unit",
                        "item_icon": "goods",
                        "item_value": 1500000,
                        "payment_amount": 1500000,
                        "tag_text": "Commercial Inward Supply",
                        "note": "Tax invoice issued under GST law."
                    }
                },
                {
                    "slide_number": 2,
                    "slide_title": "Step 2: 4-Part Statutory Eligibility Portal",
                    "scene_purpose": "Checking 4 statutory conditions to open the mechanical portal gate.",
                    "archetype_id": "conditions_gate",
                    "dialogue_manglish": "GST Section 16(2) prakaaram 4 mandatory conditions satisfy cheyyanam: invoice possession, receipt of goods, supplier tax payment, and return filing. Ivide ellam met aanu!",
                    "slots": {
                        "title": "Step 2: Section 16(2) Criteria Checklist",
                        "door_label": "Input Tax Credit Portal",
                        "all_required": True,
                        "conditions": [
                            {"label": "Possession of Tax Invoice", "passed": True},
                            {"label": "Physical Receipt of Goods", "passed": True},
                            {"label": "Supplier Tax Payment Confirmed", "passed": True},
                            {"label": "Return under Section 39 Furnished", "passed": True}
                        ],
                        "note": "All 4 statutory checklist criteria verified."
                    }
                },
                {
                    "slide_number": 3,
                    "slide_title": "Step 3: Input Tax Credit Portal Unlocked",
                    "scene_purpose": "Statutory principle confirming seamless ITC credit in electronic ledger.",
                    "archetype_id": "key_statement",
                    "dialogue_manglish": "Ellaa conditions-um satisfy cheythal maathrame Input Tax Credit portal unlock aayi electronic credit ledger-il credit labhikkoo.",
                    "slots": {
                        "title": "GST ITC Eligibility Concluded",
                        "statement": "Input Tax Credit is strictly admissible only upon complete fulfillment of all four cumulative statutory conditions.",
                        "highlight_phrase": "admissible only upon complete fulfillment",
                        "support_line": "Cumulative statutory compliance verified under Section 16(2).",
                        "icon_type": "scale"
                    }
                }
            ]
        }
    else:
        # Default General Multi-Slide
        return {
            "title": f"{subject} Statutory Provision Analysis",
            "subject": subject,
            "story_summary": f"Practical educational scenario examining compliance with {subject} statutory rules through systematic multi-step verification.",
            "slides": [
                {
                    "slide_number": 1,
                    "slide_title": "Step 1: Baseline Transaction Setup",
                    "scene_purpose": "Establishing primary transaction entities and initial values.",
                    "archetype_id": "give_and_receive",
                    "dialogue_manglish": f"Nammal ee {subject} provision examine cheyyumpol, primary commercial transaction setup koodi manasilakkanam.",
                    "slots": {
                        "title": "Step 1: Commercial Settlement",
                        "giver": "Transferor Entity",
                        "receiver": "Transferee Entity",
                        "item_label": "Primary Asset",
                        "item_icon": "goods",
                        "item_value": val1,
                        "payment_amount": val1,
                        "tag_text": "Commercial Agreement Setup",
                        "note": "Transaction terms documented."
                    }
                },
                {
                    "slide_number": 2,
                    "slide_title": "Step 2: Procedural Assessment Stages",
                    "scene_purpose": "3-stage progression roadmap applying adjustments and compliance review.",
                    "archetype_id": "step_sequence",
                    "dialogue_manglish": "Athinu sesham rule prakaaram 3 procedural assessment stages follow cheythu statutory adjustments verify cheyyunnu.",
                    "slots": {
                        "title": "Step 2: Statutory Assessment Stages",
                        "steps": [
                            {"num": "1", "title": "Eligibility Audit", "desc": "Check statutory criteria & threshold limits"},
                            {"num": "2", "title": "Valuation Review", "desc": "Apply relevant benchmarks & allowances"},
                            {"num": "3", "title": "Final Order", "desc": "Conclude net liability and confirm order"}
                        ],
                        "note": "Assessment progression verified step-by-step."
                    }
                },
                {
                    "slide_number": 3,
                    "slide_title": "Step 3: Core Statutory Principle",
                    "scene_purpose": "Universal headline takeaway with marker sweep.",
                    "archetype_id": "key_statement",
                    "dialogue_manglish": f"Ee {subject} statutory rule-inte core principle nammal exam-il exact wording-il thanne apply cheyyanam.",
                    "slots": {
                        "title": f"{subject} Statutory Rule Established",
                        "statement": provision_text[:140] + ("..." if len(provision_text) > 140 else ""),
                        "highlight_phrase": "statutory rule",
                        "support_line": "Statutory principle verified across taxable entities.",
                        "icon_type": "scale"
                    }
                }
            ]
        }


# -------------------------------------------------------------------------
# Gemini AI Multi-Slide Story & Screenplay Architect
# -------------------------------------------------------------------------
def generate_multi_slide_with_gemini(provision_text: str, subject: str = "DT", domain: str = "Real Estate") -> Dict[str, Any]:
    """Uses Gemini API to formulate story, determine slide count, and select archetypes with customized slots."""
    prompt = f"""
You are an expert Direct Tax & Indirect Tax faculty and master presentation architect for CA Final / Inter students.
Convert this statutory tax provision into an engaging, multi-slide educational video presentation explaining the rule through a simple, relatable real-life situation.

Statutory Provision:
"{provision_text}"

Subject: {subject}
Domain: {domain} (e.g. Real Estate, Shares & Securities, Goods & Logistics, General Business)

Available 15 Kinetic Animation Templates:
--- 10 SPECIFIC REAL-LIFE ACTION TEMPLATES ---
1. give_and_receive: Handover of an asset between two parties with monetary payment or unilateral transfer/gift.
   Slots: title, giver, receiver, item_label, item_icon ('house'|'shares'|'goods'), item_value (num e.g. 5000000), payment_amount (num e.g. 5000000), tag_text, note.
2. swap: Two parties exchanging different assets with crossing paths.
   Slots: title, party_a, party_b, item_a_label, item_a_val (num), item_a_icon, item_b_label, item_b_val (num), item_b_icon, note.
3. split_into_parts: A single whole entity cracking and dividing into 2 to 5 branch cards.
   Slots: title, whole_label, whole_amount (num e.g. 6000000), parts ([{{"label": "Branch 1", "amount": 2500000}}]), note.
4. merge_into_one: Multiple input streams sliding inward and fusing into one consolidated entity.
   Slots: title, inputs ([{{"label": "Stream 1", "amount": 2800000}}]), result_label, note.
5. add_up: Sequential dropping rows with a live running odometer total.
   Slots: title, items ([{{"label": "Component 1", "amount": 1200000}}]), note.
6. take_away: Slicing deduction chunks from a gross revenue/income pool to leave a net remainder.
   Slots: title, start_label, start_amount (num e.g. 3000000), steps ([{{"label": "Pre-2014 Advance Forfeited (Sec 51)", "amount": 500000}}]), result_label, note.
7. compare_two: Tilting balance scale comparing agreed/declared value against standard statutory benchmark.
   Slots: title, label_a, val_a (num), label_b, val_b (num), mode ('higher'|'lower'), cap_amount (num or null), note.
8. time_range: Timeline horizontal axis checking whether a reinvestment or action occurred within a statutory window.
   Slots: title, start_label, span_length (num), span_unit ('Days'|'Months'|'Years'), span_label, event_label, event_offset (num), is_inside (bool), note.
9. conditions_gate: Multi-criteria checklist cards with a mechanical portal gate swinging open (met) or locking (failed).
   Slots: title, conditions ([{{"label": "Explicit statutory condition (e.g. Compulsory Acquisition of Industrial Undertaking)", "passed": true}}]), open_caption, closed_caption, note.
10. chain_passing: Succession chain of 3 to 4 owners where an asset hops along and base cost is carried over.
   Slots: title, item_label, tag_label, tag_value (num), owners ([{{"name": "Owner Name", "year": "YYYY"}}]), note.

--- 5 GENERAL CATCH-ALL TEMPLATES (Use when no specific real-life action fits) ---
G1. key_statement: Central bold headline with yellow highlighter marker sweep across the critical legal takeaway.
   Slots: title, statement, highlight_phrase, support_line, icon_type ('house'|'shares'|'goods'|'scale').
G2. step_sequence: Numbered roadmap milestones with traveling pulse orb showing legal progression.
   Slots: title, steps ([{{num, title, desc}}]), note.
G3. formula_builder: Modular mathematical equation chips assembling with arithmetic live count-up.
   Slots: title, chips ([{{label, val, op, is_total}}]), note.
G4. table_reveal: Matrix table with animated row spotlight highlighting the applicable slab/rate.
   Slots: title, headers, rows, spotlight_row (int 0-indexed), note.
G5. concept_map: Central hub circle branching out into 2-4 sub-rules or legal criteria with selected branch highlight.
   Slots: title, hub_label, branches ([{{label, desc, highlight}}]), note.

STRICT INSTRUCTIONS:
CRITICAL REQUIREMENT FOR AMOUNTS, ENTITY NAMES AND CHECKLIST CRITERIA:
- The presentation MUST be dynamically customized to the EXACT situation and statutory provision!
- In `conditions_gate`: Each item in `conditions` MUST describe the real statutory condition from the situation (e.g. "Compulsory Acquisition of Industrial Land/Building", "Used for Industrial Purpose >= 2 Years", "Reinvestment in New Industrial Asset within 3 Years") and set `passed: true` if satisfied by the taxpayer or `passed: false` if breached. NEVER output generic placeholders like "Criterion 1"!
- In `take_away`: `start_amount` and `steps[].amount` MUST use the real amounts from the situation (e.g. start_amount: 3000000, steps: [{"label": "Pre-2014 Advance Forfeited", "amount": 500000}]). NEVER fallback to default ₹50 Lakhs!
- In all archetypes: Use real names (e.g. Rajesh, Vikram, Anita, Rahul), real amounts (in numbers e.g. 4500000), and specific asset descriptions!

1. First, create a relatable, simple real-life story explaining this statutory rule in plain English (e.g. Rajesh and compulsory acquisition of industrial land, Vikram forfeiting advance money in Kochi, etc.).
2. Determine the exact number of slides needed to thoroughly and clearly explain this complete story from setup to statutory conclusion. DO NOT artificially limit the number of slides—create as many slides as the pedagogical explanation naturally requires (e.g. 3, 4, 5, 6, 7 or more depending on the complexity of the provision). Every key event, calculation, statutory condition, benchmark comparison, or legal consequence should have its own dedicated slide.
3. For EACH slide:
   - Choose the best archetype out of the 15:
     - Check the 10 Specific templates first. If a physical transaction or action occurs, use the matching specific template.
     - If the slide explains a general rule, formula, sequence, or classification, choose from the 5 General templates.
   - Fill customized slots adapted to this exact story (custom names, amounts, labels, icons, notes). DO NOT use generic placeholder names!
   - Write conversational teacher narration in natural Manglish (spoken Malayalam explanation written in English Latin script with English tax terminology, sections, amounts, dates, and legal concepts).
      Example: "Namukku aadyathe scene nokkaam. 2012-il Vikram thante commercial plot Mr. A-kku sell cheyyaan agreement undaakki. Mr. A 5 Lakhs advance aayi nalki..."

Return a strict JSON object with this format:
{{
  "title": "Clear educational presentation title",
  "subject": "{subject}",
  "story_summary": "3-sentence plain English real-life narrative explaining the provision",
  "slides": [
    {{
      "slide_number": 1,
      "slide_title": "Slide header title",
      "scene_purpose": "Setup: Rahul sells commercial plot to Anita",
      "archetype_id": "give_and_receive",
      "dialogue_manglish": "Natural Malayalam teacher explanation with embedded English terms for this slide...",
      "slots": {{
        // customized slot values matching archetype requirements
      }}
    }}
  ]
}}
"""
    models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3-flash-preview"]
    for m in models_to_try:
        try:
            client = rotator.get_client()
            response = client.models.generate_content(
                model=m,
                contents=prompt
            )
            text = response.text.strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                if "slides" in parsed and len(parsed["slides"]) > 0:
                    return parsed
        except Exception as e:
            print(f"Model {m} failed ({e}), trying next fallback...")

    print("Gemini API fallback to heuristic multi-slide generator.")
    return generate_multi_slide_heuristic(provision_text, subject, domain)


# -------------------------------------------------------------------------
# Main Execution Pipeline
# -------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Convert statutory tax provision into a multi-slide presentation with audio")
    parser.add_argument("--provision", required=True, help="Statutory provision text")
    parser.add_argument("--subject", default="DT", help="Subject (DT or IDT)")
    parser.add_argument("--domain", default="Real Estate", help="Real-life domain (Real Estate, Shares, Goods)")
    parser.add_argument("--voice", default="Aoede", help="Gemini Expressive Voice name (Aoede, Kore, Puck)")
    parser.add_argument("--output", default=None, help="Output path for presentation screenplay JSON")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f"STATUTORY PROVISION TO MULTI-SLIDE PRESENTATION PIPELINE")
    print(f"=======================================================")
    print(f"Subject: {args.subject}")
    print(f"Domain:  {args.domain}")
    print(f"Provision Preview: {args.provision[:100]}...\n")

    # Step 1: Generate Story & Multi-Slide Screenplay Architecture
    print("--> Step 1: Formulating Real-Life Story & Selecting 15-Template Archetypes...")
    screenplay_data = generate_multi_slide_with_gemini(args.provision, args.subject, args.domain)
    
    slides = screenplay_data.get("slides", [])
    if not slides:
        print("[ERROR] No slides generated!")
        sys.exit(1)

    print(f"✓ Generated {len(slides)} Slides for presentation: '{screenplay_data.get('title', 'Presentation')}'")
    print(f"  Story: {screenplay_data.get('story_summary', '')}\n")

    # Prepare paths
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', screenplay_data.get("title", "custom_provision")).lower()[:35]
    pres_id = f"{args.subject.lower()}-{safe_title}"
    
    audio_base_dir = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "audio", "presentations", pres_id)
    os.makedirs(audio_base_dir, exist_ok=True)

    # Step 2: Synthesize Malayalam Voice Audio for each slide
    print("--> Step 2: Synthesizing Malayalam Voice Audio Clips for each Slide...")
    processed_slides = []
    
    for idx, slide in enumerate(slides, 1):
        slide_num = slide.get("slide_number", idx)
        arch_id = slide.get("archetype_id", "key_statement")
        dialogue = slide.get("dialogue_manglish", "")
        
        audio_filename = f"slide_{slide_num}.mp3"
        audio_path = os.path.join(audio_base_dir, audio_filename)
        
        print(f"\n[Slide {slide_num}/{len(slides)}] Archetype: {arch_id} | Title: {slide.get('slide_title', '')}")
        print(f"   Dialogue: \"{dialogue[:80]}...\"")
        
        # Synthesize audio
        audio_duration = synthesize_malayalam_voice(dialogue, audio_path, args.voice)
        slide_duration = round(audio_duration + 1.0, 1)
        
        # Calculate synchronized motion cues
        cues = {
            "cue_start": 0.5,
            "cue_action": round(max(1.0, audio_duration * 0.4), 1),
            "cue_conclusion": round(max(2.0, audio_duration * 0.8), 1)
        }
        
        # Clean and normalize slot values to canonical kinetic schemas
        raw_slots = dict(slide.get("slots", {}))
        raw_slots["title"] = raw_slots.get("title") or slide.get("slide_title")
        clean_slots = normalize_slide_slots(arch_id, raw_slots)
        
        processed_slides.append({
            "slide_number": slide_num,
            "slide_title": slide.get("slide_title", f"Slide {slide_num}"),
            "scene_purpose": slide.get("scene_purpose", ""),
            "archetype_id": arch_id,
            "dialogue_manglish": dialogue,
            "audio_file": f"data/audio/presentations/{pres_id}/{audio_filename}",
            "audio_duration": audio_duration,
            "duration": slide_duration,
            "cues": cues,
            "slots": clean_slots
        })

    # Step 3: Save Presentation Document
    out_dir = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays")
    os.makedirs(out_dir, exist_ok=True)
    out_file = args.output or os.path.join(out_dir, f"{pres_id}.json")

    final_presentation = {
        "id": pres_id,
        "title": screenplay_data.get("title", f"{args.subject} Statutory Presentation"),
        "subject": args.subject,
        "domain": args.domain,
        "provision_raw": args.provision,
        "story_summary": screenplay_data.get("story_summary", ""),
        "total_slides": len(processed_slides),
        "total_duration": round(sum(s["duration"] for s in processed_slides), 1),
        "slides": processed_slides
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_presentation, f, indent=2, ensure_ascii=False)

    # Also save as latest presentation for easy web playback
    latest_file = os.path.join(PROJECT_ROOT, "viewer", "latest_presentation.js")
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(f"window.LATEST_PRESENTATION = {json.dumps(final_presentation, indent=2, ensure_ascii=False)};\n")

    print(f"\n=======================================================")
    print(f"[SUCCESS] Multi-Slide Presentation Generated Successfully!")
    print(f"Presentation Title: {final_presentation['title']}")
    print(f"Total Slides:       {len(processed_slides)}")
    print(f"Total Duration:     {final_presentation['total_duration']} seconds")
    print(f"Screenplay Saved:   {out_file}")
    print(f"Web Bundle Saved:   {latest_file}")
    print(f"=======================================================\n")

if __name__ == "__main__":
    main()
