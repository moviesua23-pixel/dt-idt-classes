# -*- coding: utf-8 -*-
"""
pipeline/prompt_generator.py
Generates Universal Statutory Kinetic Presentation Prompts from Column 6 Provision Summaries,
synthesizes expressive Aoede neural voice for each slide/actor, concatenates audio,
and uploads to Google Drive.
"""

import os
import sys
import re
import json
import time
from typing import Dict, Any, List, Optional
from pydub import AudioSegment
from google.genai import types

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator
from pipeline.synthesize_discrete_points import (
    synthesize_point_audio,
    upload_audio_to_drive,
    VOICE_DT_FOLDER_ID,
    VOICE_IDT_FOLDER_ID
)

# Universal Domain Principle prompt instructions for Gemini
PROMPT_GENERATOR_SYSTEM_PROMPT = """You are an expert CA Final Direct Tax and Indirect Tax faculty at TaxMaster.
You convert statutory tax provision summaries into high-impact, visual presentation studio scripts for CA students.

AUDIO & PRONUNCIATION RULES (STRICT):
1. Universal Domain Principle: ANY and EVERY word or concept related to tax, law, statutory provisions, finance, accounting, computation, asset types, legal terms, sections, sub-sections, rules, dates, years, and assessment years MUST be in ENGLISH.
   Examples of mandatory English: Section 48, Section 54EC, Assessment Year 2024-25, Financial Year 2023-24, Cost of Acquisition, Fair Market Value, Long Term Capital Gain, Full Value of Consideration, Indexed Cost, Deductions, Capital Asset, Transfer, Expenditure.
2. Malayalam is used STRICTLY for friendly teacher explanations, conversational scaffolding, and connectives (Manglish code-switching standard in Kerala CA coaching).
3. Never transliterate legal terms or section numbers into Malayalam characters.

PRESENTATION SCRIPT SYNTAX RULES:
Each script must contain 2 to 4 SLIDES.
- Slide 1: High-level statutory doctrine & overview.
  Must use: (heading, title: "Title in English", subtitle: "Section Ref in English", pos: center)
  Must end with: DIALOGUE: <Teacher explanation in Manglish>

- Slide 2: Core entities / assets / provisions with vector shapes.
  Must use:
  shape (<shape_keyword>) (<Entity Label in English>) (<pos>) (<intro>)
  Common valid shape keywords: land_property, factory, building, business_structure, audit_tax, tax_calculation, rupee_coin, cash_bundle, balance_sheet, document_verified, corporate_governance, car_automobile, transfer_ship.
  Grid positions: left center, right center, center, left top, right top.
  Intro animations: pop, fade, drop.
  Must end with: DIALOGUE: <Teacher explanation in Manglish>

- Slide 3: Detailed clauses, permissible items, or step-by-step checklist.
  Must use one of:
  shape (list, cards) (<Title in English>) [ (<Item 1 in English>) (<Item 2 in English>) (<Item 3 in English>) ]
  or
  shape (list, timeline) (<Process Title in English>) [ (<Step 1>) (<Step 2>) (<Step 3>) ]
  or
  shape (list, clause) (<Clauses Title in English>) [ (<Clause 1>) (<Clause 2>) ]
  or
  (calculation, title: "<Computation Title in English>", items: ["<Term 1> = <Amount>", "<Term 2> = <Amount>"])
  Must end with: DIALOGUE: <Teacher explanation in Manglish>

Output ONLY the raw script text without markdown code blocks, backticks, or extra preambles.
"""

def generate_presentation_prompt(
    canonical_topic: str,
    prov_summary_md: str,
    q_text: str = "",
    ans_text: str = "",
    subject: str = "DT"
) -> str:
    """
    Calls Gemini API via KeyRotator to generate a structured Kinetic Presentation Prompt
    explaining the Column 6 Provision Summary.
    """
    user_content = f"""Subject: {subject}
Statutory Topic: {canonical_topic}

Column 6 Statutory Provision Summary:
{prov_summary_md}

Exam Question Context (if relevant):
{q_text[:600]}

Exam Answer Context (if relevant):
{ans_text[:600]}

Generate the kinetic presentation studio script with 3 slides explaining this provision clearly and visually.
Follow the exact syntax: SLIDE 1:, (heading, ...), DIALOGUE:, SLIDE 2:, shape (...), DIALOGUE:, SLIDE 3:, shape (list, cards) [ ... ], DIALOGUE:.
Output only the script text.
"""

    models_to_try = [
        'gemini-3.8-flash',
        'gemini-3.5-flash',
        'gemini-3.5-flash-lite'
    ]

    def _call(client):
        last_err = None
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=[user_content],
                    config=types.GenerateContentConfig(
                        system_instruction=PROMPT_GENERATOR_SYSTEM_PROMPT,
                        temperature=0.3,
                        max_output_tokens=2048
                    )
                )
                return response.text.strip()
            except Exception as e:
                last_err = e
                continue
        raise last_err

    raw_script = rotator.execute_with_retry(_call)
    # Strip backticks if returned inside code blocks
    raw_script = re.sub(r'^```[\w]*\s*', '', raw_script)
    raw_script = re.sub(r'\s*```$', '', raw_script)
    return raw_script.strip()

def extract_dialogues_from_prompt(prompt_text: str) -> List[Dict[str, Any]]:
    """
    Extracts all DIALOGUE lines from the prompt, grouped by slide.
    """
    lines = prompt_text.splitlines()
    slides = []
    current_slide = 1
    current_dialogue = []

    for line in lines:
        line_s = line.strip()
        m_slide = re.match(r'^(?:SLIDE|SCENE)\s*(\d+)?\s*:?\s*(.*)$', line_s, re.IGNORECASE)
        if m_slide:
            if current_dialogue:
                slides.append({
                    "slide_idx": current_slide,
                    "dialogue": " ".join(current_dialogue)
                })
                current_dialogue = []
            if m_slide.group(1):
                current_slide = int(m_slide.group(1))
            else:
                current_slide = len(slides) + 1
            continue

        m_diag = re.match(r'^(?:DIALOGUE|NARRATION|SPEECH|TEACHER)\s*:\s*["\']?(.*?)["\']?$', line_s, re.IGNORECASE)
        if m_diag:
            text = m_diag.group(1).strip()
            if text:
                current_dialogue.append(text)

    if current_dialogue:
        slides.append({
            "slide_idx": current_slide,
            "dialogue": " ".join(current_dialogue)
        })

    return slides

def synthesize_and_upload_prompt_audio(
    prompt_text: str,
    subject: str,
    chapter_no: int,
    q_num: int,
    output_dir: Optional[str] = None
) -> str:
    """
    Synthesizes expressive Aoede voice for each slide's dialogue, concatenates them into
    a master presentation audio file, and uploads to Google Drive.
    Returns: Google Drive Audio File ID.
    """
    if not output_dir:
        output_dir = os.path.join(PROJECT_ROOT, 'data', 'audio', subject.lower(), f'ch{chapter_no}', f'q{q_num}')
    os.makedirs(output_dir, exist_ok=True)

    dialogues = extract_dialogues_from_prompt(prompt_text)
    if not dialogues:
        print(f"  [WARN] No dialogues found in prompt for Q{q_num}. Generating placeholder audio.")
        dialogues = [{"slide_idx": 1, "dialogue": f"Statutory explanation for Chapter {chapter_no} Question {q_num} under {subject}."}]

    slide_audio_segments = []
    pause = AudioSegment.silent(duration=450) # 450ms natural pause between slides

    for item in dialogues:
        s_idx = item['slide_idx']
        d_text = item['dialogue']
        clip_path = os.path.join(output_dir, f"slide_{s_idx}.mp3")

        print(f"    [TTS Slide {s_idx}] Synthesizing Aoede voice ({len(d_text.split())} words)...")
        synthesize_point_audio(d_text, clip_path)

        if os.path.exists(clip_path):
            seg = AudioSegment.from_mp3(clip_path)
            slide_audio_segments.append(seg)
            slide_audio_segments.append(pause)

    if not slide_audio_segments:
        raise RuntimeError("Failed to generate any slide audio segments.")

    # Combine all slide audio into unified master MP3
    combined = slide_audio_segments[0]
    for seg in slide_audio_segments[1:]:
        combined += seg

    master_mp3_path = os.path.join(output_dir, f"{subject.lower()}_ch{chapter_no}_q{q_num}_presentation.mp3")
    combined.export(master_mp3_path, format="mp3")
    print(f"  [MASTER AUDIO COMPILED] Duration: {len(combined)/1000.0:.1f}s -> {master_mp3_path}")

    # Upload to Google Drive
    parent_folder_id = VOICE_IDT_FOLDER_ID if subject.upper() == 'IDT' else VOICE_DT_FOLDER_ID
    file_name = f"{subject.upper()}_Ch{chapter_no}_Q{q_num}_Presentation.mp3"
    drive_file_id = upload_audio_to_drive(master_mp3_path, parent_folder_id, file_name)
    print(f"  [GOOGLE DRIVE UPLOADED] File ID: {drive_file_id}")
    return drive_file_id
