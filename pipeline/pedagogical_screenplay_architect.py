\"\"\"
pipeline/pedagogical_screenplay_architect.py
Pedagogical Screenplay Architect:
Takes a statutory provision, designs a rich concrete pedagogical example story,
synthesizes natural expressive speech via Gemini Aoede / ElevenLabs / Google TTS,
transcribes acoustic energy & timestamps, and outputs an interactive white-canvas Screenplay.
\"\"\"

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

PEDAGOGICAL_PROMPT = \"\"\"You are a senior, beloved CA Final Tax Professor and Visual Explainer Architect for Indian Direct Tax.
Your student needs to master this complex statutory provision.

Question/Context:
{question_text}

Answer/Statutory Solution:
{answer_text}

Statutory Matrix:
{provision_matrix}

========================================================================================
TASK 1: CREATE A CONCRETE PEDAGOGICAL EXAMPLE (NO DRY BULLETS!)
========================================================================================
Create a 4 to 6 beat sequential story/lesson following a relatable character (e.g. Hari, Ananya, Rajesh) buying/selling an asset, claiming an exemption, or facing an assessing officer.
Each beat MUST use a specific layout suited to that pedagogical step:
- \"fork\": For dual paths, cut-off dates (e.g. before vs after cut-off), or story evolution.
- \"statute_quote\": For the core statutory proviso, legal question, or threshold trigger.
- \"meter\": For financial limit checks (e.g. Rs 2 Crore, Rs 10 Lakh), padlocks, and qualification.
- \"case_card\": For landmark High Court / Supreme Court precedents or disputes with AO.
- \"ledger\": For step-by-step mathematical computations, deductions, and taxable remainder.
- \"takeaway\": For 3 numbered Golden Rules summarizing the statutory doctrine for exams.

========================================================================================
TASK 2: MANGLISH TEACHER NARRATION RULES (STRICT DOMAIN PRINCIPLE)
========================================================================================
- ALL Sections, Sub-sections, Rules, and Acts MUST be in English Latin script (e.g. 'Section 51', 'Section 54(1)').
- ALL Dates and Years MUST be in English Latin script (e.g. '1st April 2014', 'Year 2002', 'Assessment Year 2024-25').
- ALL Financial figures and amounts MUST be in English Latin numbers (e.g. 'Rs 9,00,000', 'Rs 25,000', 'Rs 2 Crore').
- ALL Tax and Statutory Terms MUST be in English Latin (e.g. 'Cost of Acquisition', 'Capital Gain', 'Long-term Capital Gain', 'Exemption', 'Substantial Ownership').
- Malayalam is used naturally for conversational teacher scaffolding, connectives, and narrative explanations.

========================================================================================
OUTPUT FORMAT: PURE JSON
========================================================================================
Return STRICT VALID JSON matching this exact structure:
{{
  \"context_pill\": \"Section Badge and Topic\",
  \"beats\": [
    {{
      \"id\": \"b1\",
      \"layout\": \"fork\",
      \"voice_sync_text\": \"Malayalam teacher narration text for beat 1...\",
      \"title\": {{\"text\": \"Beat Title\", \"at\": 0.5}},
      \"story_steps\": [
        {{\"badge\": \"Step 1\", \"title\": \"Acquisition\", \"sub\": \"Details\", \"val\": 900000, \"at\": 4.5}}
      ],
      \"divider\": {{\"text\": \"Cut-off Date: 01-04-2014\", \"at\": 20.0}},
      \"branches\": [
        {{\"side\": \"left\", \"label\": \"Before Cut-off\", \"facts\": [{{\"text\": \"Deduct from Cost\", \"at\": 25.0}}], \"outcome\": {{\"text\": \"Reduces Cost\", \"at\": 27.0}}}},
        {{\"side\": \"right\", \"label\": \"On/After Cut-off\", \"facts\": [{{\"text\": \"Taxable IFOS\", \"at\": 22.0}}], \"outcome\": {{\"text\": \"IFOS Taxable\", \"at\": 24.0}}}}
      ],
      \"result_card\": {{\"badge\": \"Result\", \"title\": \"Adjusted Cost\", \"val\": 875000, \"at\": 32.0}}
    }}
  ]
}}
\"\"\"

def generate_pedagogical_screenplay_plan(q_num: int, q_text: str, ans_text: str, prov_matrix: str) -> Optional[Dict[str, Any]]:
    prompt = PEDAGOGICAL_PROMPT.format(
        question_text=q_text[:3000],
        answer_text=ans_text[:3000],
        provision_matrix=prov_matrix[:3000]
    )
    for _ in range(len(rotator.keys)):
        client = rotator.get_active_client()
        try:
            resp = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type=\"application/json\",
                    temperature=0.3
                )
            )
            return json.loads(resp.text.strip())
        except Exception as e:
            if \"429\" in str(e) or \"RESOURCE_EXHAUSTED\" in str(e):
                rotator.mark_active_exhausted()
                continue
            return None
    return None

def build_full_screenplay_for_question(subject: str, ch_no: int, q_num: int, q_text: str, ans_text: str, prov_matrix: str) -> Optional[Dict[str, Any]]:
    qid = f\"{subject.lower()}-c{ch_no}-q{q_num}\"
    print(f\"  [SCREENPLAY ARCHITECT] Designing pedagogical example and layouts for {qid}...\")
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
        current_time = b['end'] + 0.25

    return {
        \"question_id\": qid,
        \"audio_url\": f\"data/audio/{qid}.mp3\",
        \"duration_sec\": round(current_time, 2),
        \"sync_offset_sec\": 0.0,
        \"context_pill\": plan.get('context_pill', f\"§ Ch {ch_no} Q {q_num}\"),
        \"fallback\": False,
        \"beats\": beats
    }
