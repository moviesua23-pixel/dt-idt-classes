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
# Voice Synthesis Engine (EdgeTTS & Gemini TTS)
# -------------------------------------------------------------------------
def synthesize_malayalam_voice(script: str, output_mp3_path: str, voice_name: str = "ml-IN-SobhanaNeural") -> float:
    """
    Synthesizes authentic Malayalam teacher narration audio for a presentation slide.
    Uses EdgeTTS (ml-IN-SobhanaNeural / ml-IN-MidhunNeural) for authentic Malayalam speech.
    Returns the exact audio duration in seconds.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp3_path)), exist_ok=True)
    
    # 1. Primary: Authentic Malayalam Neural TTS (EdgeTTS)
    try:
        import edge_tts
        edge_voice = "ml-IN-SobhanaNeural" if "midhun" not in voice_name.lower() else "ml-IN-MidhunNeural"
        
        async def _edge_gen():
            comm = edge_tts.Communicate(script, edge_voice, rate="+5%")
            await comm.save(output_mp3_path)
            
        asyncio.run(_edge_gen())
        
        # Measure duration with ffprobe
        res = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', output_mp3_path],
            capture_output=True, text=True
        )
        dur = float(res.stdout.strip()) if res.stdout.strip() else 10.0
        if os.path.exists(output_mp3_path) and os.path.getsize(output_mp3_path) > 1000:
            print(f"   [TTS] Synthesized via EdgeTTS ({edge_voice}): {dur:.1f}s")
            return dur
    except Exception as e:
        print(f"   [TTS] EdgeTTS error ({e}), trying Gemini Voice fallback...")

    # 2. Fallback: Gemini Voice (with strict verbatim reading instruction)
    try:
        from pipeline.phase3_audio import generate_gemini_audio
        verbatim_script = f"Read the following teacher explanation aloud verbatim in Malayalam with English tax terminology. Speak ONLY this text and nothing else:\n\n{script}"
        dur, engine = generate_gemini_audio(verbatim_script, output_mp3_path, voice_name="Aoede")
        if os.path.exists(output_mp3_path) and os.path.getsize(output_mp3_path) > 2000:
            print(f"   [TTS] Synthesized via {engine}: {dur:.1f}s")
            return dur
    except Exception as e:
        print(f"   [TTS Error] All voice synthesis options failed: {e}")
        return 8.0


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
                            {"text": "Possession of Tax Invoice", "met": True},
                            {"text": "Physical Receipt of Goods", "met": True},
                            {"text": "Supplier Tax Payment Confirmed", "met": True},
                            {"text": "Return under Section 39 Furnished", "met": True}
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
   Slots: title, giver, receiver, item_label, item_icon ('house'|'shares'|'goods'), item_value (num), payment_amount (num), tag_text, note.
2. swap: Two parties exchanging different assets with crossing paths.
   Slots: title, party_a, party_b, item_a (label, icon, val), item_b (label, icon, val), note.
3. split_into_parts: A single whole entity cracking and dividing into 2 to 5 branch cards.
   Slots: title, whole_label, whole_val (num), parts ([{{label, pct, val, tone}}]), note.
4. merge_into_one: Multiple input streams sliding inward and fusing into one consolidated entity.
   Slots: title, streams ([{{label, val, tone}}]), merged_label, note.
5. add_up: Sequential dropping rows with a live running odometer total.
   Slots: title, rows ([{{label, val, tone}}]), note.
6. take_away: Slicing deduction chunks from a gross revenue/income pool to leave a net remainder.
   Slots: title, whole_label, whole_val (num), chunks ([{{label, val}}]), result_label, note.
7. compare_two: Tilting balance scale comparing agreed/declared value against standard statutory benchmark.
   Slots: title, label_a, val_a (num), label_b, val_b (num), mode ('higher'|'lower'), cap_amount, note.
8. time_range: Timeline horizontal axis checking whether a reinvestment or action occurred within a statutory window.
   Slots: title, start_label, span_length (num), span_unit ('Days'|'Months'|'Years'), span_label, event_label, event_offset (num), is_inside (bool), note.
9. conditions_gate: Multi-criteria checklist cards with a mechanical portal gate swinging open (met) or locking (failed).
   Slots: title, door_label, all_required (bool), conditions ([{{text, met}}]), note.
10. chain_passing: Succession chain of 3 to 4 owners where an asset hops along and base cost is carried over.
   Slots: title, item_label, tag_label, tag_value (num), owners ([{{name, year}}]), note.

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
1. First, create a relatable, simple real-life story explaining this statutory rule in plain English (e.g. Rahul selling land in Kochi, Grandfather's succession gift, or ITC 4-part conditions checklist).
2. Determine the exact number of slides needed to thoroughly and clearly explain this complete story from setup to statutory conclusion. DO NOT artificially limit the number of slides—create as many slides as the pedagogical explanation naturally requires (e.g. 3, 4, 5, 6, 7 or more depending on the complexity of the provision). Every key event, calculation, statutory condition, benchmark comparison, or legal consequence should have its own dedicated slide.
3. For EACH slide:
   - Choose the best archetype out of the 15:
     - Check the 10 Specific templates first. If a physical transaction or action occurs, use the matching specific template.
     - If the slide explains a general rule, formula, sequence, or classification, choose from the 5 General templates.
   - Fill customized slots adapted to this exact story (custom names, amounts, labels, icons, notes). DO NOT use generic placeholder names!
   - Write conversational teacher narration in Malayalam with English legal/statutory terminology (Manglish code-switching standard in Kerala CA education: Malayalam connectives + English sections, amounts, dates, and legal concepts).

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
    parser.add_argument("--voice", default="ml-IN-SobhanaNeural", help="Malayalam TTS voice name")
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
        
        # Clean slot values
        clean_slots = dict(slide.get("slots", {}))
        clean_slots["title"] = clean_slots.get("title") or slide.get("slide_title")
        
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
