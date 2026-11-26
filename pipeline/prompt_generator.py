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
1. Universal Domain Principle: ANY and EVERY word or concept related to tax, law, statutory provisions, finance, accounting, computation, asset types, legal terms, sections, sub-sections, rules, dates, years, and assessment years MUST be in standard ENGLISH.
   Examples of mandatory English: Section 48, Section 54, Section 143(2), Assessment Year 2026-27, Financial Year 2025-26, Cost of Acquisition, Fair Market Value, Long Term Capital Gain, Full Value of Consideration, Indexed Cost of Acquisition, Cost of Improvement, Transfer Expenses, Capital Gains Account Scheme, Deductions, Capital Asset, Transfer, Net Profit, Depreciation.
2. Malayalam is used STRICTLY for friendly teacher explanations, conversational scaffolding, and connectives (Manglish code-switching standard in Kerala CA coaching, written in English alphabet).
3. Never transliterate legal terms, sections, or dates into Malayalam characters.

PRESENTATION SCRIPT SYNTAX RULES:
The script MUST be organized into 2 to 4 SLIDES.
Follow this exact DSL format:

SLIDE 1: <Descriptive Slide Title in English> (Cards Design)
theme (<theme_color>)
heading (<Statutory Section / Provision in English>) (<Statutory Framework / Subtitle in English>)
shape (man) (CA Rajesh) (left center) (dialogue: "<Teacher explanation in Manglish introducing the doctrine>")
shape (list, cards) (<List Title in English>) (right center) [
  (<Item 1: Short summary in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Item 2: Short summary in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Item 3: Short summary in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Item 4: Short summary in English>) (dialogue: "<Teacher explanation in Manglish>")
]

SLIDE 2: <Descriptive Slide Title in English> (Timeline Design)
theme (<theme_color>)
heading (<Process Title in English>) (<Statutory Reference in English>)
shape (woman) (Tax Officer) (left center) (dialogue: "<Teacher explanation in Manglish>")
shape (list, timeline) (<Timeline Title in English>) (right center) [
  (<Step 1: Description in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Step 2: Description in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Step 3: Description in English>) (dialogue: "<Teacher explanation in Manglish>")
  (<Step 4: Description in English>) (dialogue: "<Teacher explanation in Manglish>")
]

SLIDE 3: <Descriptive Slide Title in English> (Clause Design)
theme (<theme_color>)
heading (<Title in English>) (<Statutory Conditions & Provisos in English>)
shape (list, clause) (<Eligibility / Conditions Title in English>) (center) [
  (Clause A: <Condition in English>) (dialogue: "<Teacher explanation in Manglish>")
  (Clause B: <Condition in English>) (dialogue: "<Teacher explanation in Manglish>")
  (Clause C: <Condition in English>) (dialogue: "<Teacher explanation in Manglish>")
  (Clause D: <Condition in English>) (dialogue: "<Teacher explanation in Manglish>")
]

SYNTAX GUIDELINES:
- Valid theme colors: indigo, blue, amber, emerald, rose, purple, cyan, slate.
- Valid positions: left center, right center, center, left top, right top.
- Valid list designs: cards, timeline, clause, pills, obsidian.
- Valid character shapes: shape (man) (<Name>), shape (woman) (<Name>).
- Valid domain vector shapes if needed: shape (land_property), shape (factory), shape (building), shape (tax_calculation), shape (balance_sheet), shape (document_verified), shape (money_bag), shape (rupee_coin), shape (car_automobile).
- Each list item inside [ ... ] MUST have its title and an inline (dialogue: "...") tag.
- Output ONLY the raw script text. Do not wrap in markdown code fences (no ```).
"""

def generate_presentation_prompt(
    canonical_topic: str,
    prov_summary_md: str,
    q_text: str = "",
    ans_text: str = "",
    subject: str = "DT",
    chapter_no: Optional[int] = None,
    q_num: Optional[int] = None
) -> str:
    """
    Calls Gemini API via KeyRotator to generate a structured Kinetic Presentation Prompt
    explaining the Column 6 Provision Summary in the exact Studio DSL format.
    Caches prompts to disk to save quota across resumption runs.
    """
    prompt_cache_file = None
    if chapter_no is not None and q_num is not None:
        cache_dir = os.path.join(PROJECT_ROOT, 'data', 'prompts', subject.lower(), f'ch{chapter_no}')
        os.makedirs(cache_dir, exist_ok=True)
        prompt_cache_file = os.path.join(cache_dir, f"q{q_num}.prompt.txt")
        if os.path.exists(prompt_cache_file):
            try:
                with open(prompt_cache_file, 'r', encoding='utf-8') as f:
                    cached_prompt = f.read().strip()
                if cached_prompt and not cached_prompt.startswith('{') and not cached_prompt.startswith('['):
                    print(f"  [PROMPT CACHE] Reusing cached Kinetic Studio prompt for {subject} Ch{chapter_no} Q{q_num}")
                    return cached_prompt
            except Exception:
                pass

    user_content = f"""Subject: {subject}
Statutory Topic: {canonical_topic}

Column 6 Statutory Provision Summary:
{prov_summary_md}

Exam Question Context (if relevant):
{q_text[:600]}

Exam Answer Context (if relevant):
{ans_text[:600]}

Generate the kinetic presentation studio script with 3 slides explaining this statutory provision clearly and visually.
Follow the exact syntax:
SLIDE 1: ... (Cards Design)
theme (...)
heading (...) (...)
shape (man) (...) (left center) (dialogue: "...")
shape (list, cards) (...) (right center) [
  (...) (dialogue: "...")
]

SLIDE 2: ... (Timeline Design)
theme (...)
heading (...) (...)
shape (woman) (...) (left center) (dialogue: "...")
shape (list, timeline) (...) (right center) [
  (...) (dialogue: "...")
]

SLIDE 3: ... (Clause Design)
theme (...)
heading (...) (...)
shape (list, clause) (...) (center) [
  (...) (dialogue: "...")
]

Output only the raw script text.
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
    cleaned_prompt = raw_script.strip()

    if prompt_cache_file and cleaned_prompt:
        try:
            with open(prompt_cache_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_prompt)
        except Exception:
            pass

    return cleaned_prompt

def extract_dialogues_from_prompt(prompt_text: str) -> List[Dict[str, Any]]:
    """
    Extracts all dialogues from the prompt grouped by slide, preserving reading order.
    Extracts from both inline `(dialogue: "...")` tags (across shapes and list items)
    and standalone `DIALOGUE: ...` lines.
    """
    slide_blocks = re.split(r'(?i)(?:^|\n)\s*(?:SLIDE|SCENE)\s*(\d+)?:?\s*', prompt_text)
    slides = []
    current_slide = 1

    i = 1
    while i < len(slide_blocks):
        s_num_str = slide_blocks[i]
        content = slide_blocks[i+1] if i + 1 < len(slide_blocks) else ""
        i += 2

        slide_idx = int(s_num_str) if s_num_str and s_num_str.isdigit() else current_slide
        current_slide = slide_idx + 1

        dialogues = []
        # 1. Matches (dialogue: "...") or (dialogue: '...')
        for m in re.finditer(r'\(dialogue\s*:\s*["\']([\s\S]+?)["\']\)', content, re.IGNORECASE):
            text = " ".join(m.group(1).split()).strip()
            if text:
                dialogues.append(text)

        # 2. Standalone DIALOGUE: ... lines
        for line in content.splitlines():
            line_s = line.strip()
            m_diag = re.match(r'^(?:DIALOGUE|NARRATION|SPEECH|TEACHER)\s*:\s*["\']?(.*?)["\']?$', line_s, re.IGNORECASE)
            if m_diag:
                text = " ".join(m_diag.group(1).split()).strip()
                if text and text not in dialogues:
                    dialogues.append(text)

        if dialogues:
            slides.append({
                "slide_idx": slide_idx,
                "dialogues": dialogues,
                "combined": " ".join(dialogues)
            })

    # Fallback if no slide header was detected
    if not slides:
        all_inline = [
            " ".join(m.group(1).split()).strip()
            for m in re.finditer(r'\(dialogue\s*:\s*["\']([\s\S]+?)["\']\)', prompt_text, re.IGNORECASE)
            if " ".join(m.group(1).split()).strip()
        ]
        if all_inline:
            slides.append({
                "slide_idx": 1,
                "dialogues": all_inline,
                "combined": " ".join(all_inline)
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
    Synthesizes expressive Aoede voice for each slide's dialogues, concatenates them into
    a master presentation audio file, and uploads to Google Drive.
    Returns: Google Drive Audio File ID.
    """
    if not output_dir:
        output_dir = os.path.join(PROJECT_ROOT, 'data', 'audio', subject.lower(), f'ch{chapter_no}', f'q{q_num}')
    os.makedirs(output_dir, exist_ok=True)

    slides = extract_dialogues_from_prompt(prompt_text)
    if not slides:
        print(f"  [WARN] No dialogues found in prompt for Q{q_num}. Generating placeholder audio.")
        slides = [{
            "slide_idx": 1,
            "dialogues": [f"Statutory explanation for Chapter {chapter_no} Question {q_num} under {subject}."],
            "combined": f"Statutory explanation for Chapter {chapter_no} Question {q_num} under {subject}."
        }]

    slide_audio_segments = []
    item_pause = AudioSegment.silent(duration=280)   # 280ms pause between list items / actors
    slide_pause = AudioSegment.silent(duration=500)  # 500ms pause between slides

    for s_info in slides:
        s_idx = s_info['slide_idx']
        dialogues = s_info['dialogues']

        current_slide_segs = []
        for d_idx, d_text in enumerate(dialogues):
            clip_path = os.path.join(output_dir, f"slide_{s_idx}_part_{d_idx+1}.mp3")
            if os.path.exists(clip_path) and os.path.getsize(clip_path) > 1000:
                print(f"    [TTS Slide {s_idx} Part {d_idx+1}/{len(dialogues)}] Reusing existing audio clip: {os.path.basename(clip_path)}")
            else:
                print(f"    [TTS Slide {s_idx} Part {d_idx+1}/{len(dialogues)}] Synthesizing Aoede voice ({len(d_text.split())} words)...")
                synthesize_point_audio(d_text, clip_path)
            if os.path.exists(clip_path):
                seg = AudioSegment.from_mp3(clip_path)
                current_slide_segs.append(seg)
                current_slide_segs.append(item_pause)

        if current_slide_segs:
            slide_combined = current_slide_segs[0]
            for seg in current_slide_segs[1:]:
                slide_combined += seg
            slide_audio_segments.append(slide_combined)
            slide_audio_segments.append(slide_pause)

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
