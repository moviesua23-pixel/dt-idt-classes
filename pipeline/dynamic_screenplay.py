"""Two-stage provision director and strict, layout-specific screenplay writer."""

from __future__ import annotations

import json
import re
from typing import Any

from google import genai
from google.genai import types

from pipeline.key_rotator import rotator

ARCHETYPES = [
    "threshold_test", "date_cutoff_before_after", "deemed_value_substitution",
    "conditions_checklist", "two_regime_comparison", "rate_slab_ladder",
    "exemption_reinvestment_timeline", "computation_ledger",
    "set_off_carry_forward_waterfall", "tds_flow", "case_law_precedent",
    "exception_override", "classification_decision_tree",
]

LAYOUTS = [
    "example_scene", "decision_tree", "checklist_gate", "timeline_windows",
    "flow_actors", "compare_regimes", "slab_ladder", "ledger", "waterfall",
    "deemed_value", "case_card", "statute_quote", "takeaway",
]

ARCHETYPE_LAYOUTS = {
    "threshold_test": ["example_scene", "checklist_gate", "deemed_value", "ledger", "takeaway"],
    "date_cutoff_before_after": ["example_scene", "timeline_windows", "compare_regimes", "ledger", "takeaway"],
    "deemed_value_substitution": ["example_scene", "deemed_value", "ledger", "statute_quote", "takeaway"],
    "conditions_checklist": ["example_scene", "checklist_gate", "decision_tree", "ledger", "takeaway"],
    "two_regime_comparison": ["example_scene", "compare_regimes", "decision_tree", "ledger", "takeaway"],
    "rate_slab_ladder": ["example_scene", "slab_ladder", "ledger", "statute_quote", "takeaway"],
    "exemption_reinvestment_timeline": ["example_scene", "timeline_windows", "checklist_gate", "ledger", "takeaway"],
    "computation_ledger": ["example_scene", "ledger", "deemed_value", "statute_quote", "takeaway"],
    "set_off_carry_forward_waterfall": ["example_scene", "waterfall", "ledger", "decision_tree", "takeaway"],
    "tds_flow": ["example_scene", "flow_actors", "timeline_windows", "ledger", "takeaway"],
    "case_law_precedent": ["example_scene", "case_card", "decision_tree", "statute_quote", "takeaway"],
    "exception_override": ["example_scene", "decision_tree", "checklist_gate", "statute_quote", "takeaway"],
    "classification_decision_tree": ["example_scene", "decision_tree", "compare_regimes", "ledger", "takeaway"],
}

def obj(properties: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": properties, "required": required or list(properties), "additionalProperties": False}

def string_list() -> dict:
    return {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 8}

DIRECTOR_SCHEMA = obj({
    "archetype": {"type": "string", "enum": ARCHETYPES},
    "justification": {"type": "string"},
    "protagonist": {"type": "string"},
    "actors": string_list(),
    "key_numbers": string_list(),
    "key_dates": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
    "visual_metaphor": {"type": "string"},
    "beat_plan": {"type": "array", "minItems": 3, "maxItems": 8, "items": obj({
        "beat_goal": {"type": "string"},
        "layout": {"type": "string", "enum": LAYOUTS},
        "anchor_phrases": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 8},
    })},
}, ["archetype", "justification", "protagonist", "actors", "key_numbers", "key_dates", "visual_metaphor", "beat_plan"])

ITEM = obj({
    "label": {"type": "string"}, "detail": {"type": "string"},
    "value": {"type": "string"}, "date": {"type": "string"},
    "status": {"type": "string"}, "icon": {"type": "string", "enum": ["person", "house", "plot", "shares", "factory", "money_bag", "document", "gavel", "bank", "calendar", "padlock", "scales"]},
}, ["label"])

DATA_SCHEMAS = {
    "example_scene": obj({"actors": {"type": "array", "items": ITEM, "minItems": 1, "maxItems": 4}, "transaction": {"type": "string"}, "facts": {"type": "array", "items": ITEM, "minItems": 1, "maxItems": 5}}, ["actors", "transaction", "facts"]),
    "decision_tree": obj({"root": {"type": "string"}, "branches": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 4}}, ["root", "branches"]),
    "checklist_gate": obj({"conditions": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 6}, "outcome": {"type": "string"}}, ["conditions", "outcome"]),
    "timeline_windows": obj({"events": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 6}, "window_label": {"type": "string"}}, ["events", "window_label"]),
    "flow_actors": obj({"actors": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 4}, "edges": {"type": "array", "items": ITEM, "minItems": 1, "maxItems": 5}}, ["actors", "edges"]),
    "compare_regimes": obj({"regimes": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 3}}, ["regimes"]),
    "slab_ladder": obj({"tiers": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 6}}, ["tiers"]),
    "ledger": obj({"rows": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 7}, "total": {"type": "string"}}, ["rows", "total"]),
    "waterfall": obj({"stages": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 5}}, ["stages"]),
    "deemed_value": obj({"actual": ITEM, "deemed": ITEM, "rule": {"type": "string"}}, ["actual", "deemed", "rule"]),
    "case_card": obj({"case_name": {"type": "string"}, "court": {"type": "string"}, "principle": {"type": "string"}, "application": {"type": "string"}}, ["case_name", "principle", "application"]),
    "statute_quote": obj({"rule": {"type": "string"}, "citation": {"type": "string"}, "application": {"type": "string"}}, ["rule", "citation", "application"]),
    "takeaway": obj({"rules": {"type": "array", "items": ITEM, "minItems": 2, "maxItems": 4}}, ["rules"]),
}

def voiceover_context(mindmap: dict[str, Any] | None, answer: str) -> str:
    parts: list[str] = []
    if isinstance(mindmap, dict):
        root = mindmap.get("root") or {}
        if root.get("voice_sync_text"):
            parts.append(root["voice_sync_text"])
        for branch in mindmap.get("branches", []):
            for point in branch.get("points", []):
                if point.get("voice_sync_text"):
                    parts.append(point["voice_sync_text"])
    return "\n".join(parts)[:9000] or (answer or "")[:9000]

def _generate_json(prompt: str, schema: dict, label: str) -> dict:
    models = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.1-pro-preview"]
    last_error = None
    for model in models:
        def call(client: genai.Client, m=model):
            response = client.models.generate_content(
                model=m,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.25,
                ),
            )
            return json.loads(response.text or "{}")
        try:
            result = rotator.execute_with_retry(call)
            if isinstance(result, dict):
                return result
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"{label} structured generation failed: {last_error}")

def _director_prompt(question: str, answer: str, provision: str, voiceover: str) -> str:
    return f"""You are the visual director for a CA tax-law explainer. Choose an explanation structure based on the provision's actual mechanism and question facts. Return only the supplied JSON schema. Do not write the voice-over.\n\nQuestion:\n{question[:6000]}\n\nAnswer:\n{answer[:6000]}\n\nProvision summary:\n{provision[:5000]}\n\nExisting voice-over/source narration:\n{voiceover[:6000]}\n\nRules: choose exactly one listed archetype; justify in one sentence tied to facts in this question. List source-grounded people, amounts, dates, and legal anchors. Plan 3-8 ordered beats that explain every distinct provision point and example step. Beat 1 must be 'example_scene' and establish a broad view of the full example. End the plan with layout 'takeaway'. Choose layouts only from the schema. Do not invent legal tests, dates, amounts, or case citations."""

def _writer_schema(plan: dict) -> dict:
    properties = {
        "question_id": {"type": "string"},
        "context_pill": {"type": "string"},
        "example_summary": {"type": "string"},
    }
    for index, planned in enumerate(plan["beat_plan"], 1):
        layout = planned["layout"]
        properties[f"beat_{index}"] = obj({
            "layout": {"type": "string", "enum": [layout]},
            "title": obj({"text": {"type": "string"}}),
            "voice_sync_text": {"type": "string"},
            "visual_data": DATA_SCHEMAS[layout],
        }, ["layout", "title", "voice_sync_text", "visual_data"])
    required = ["question_id", "context_pill", "example_summary", *[f"beat_{i}" for i in range(1, len(plan["beat_plan"]) + 1)]]
    return obj(properties, required)

def _writer_prompt(qid: str, question: str, answer: str, provision: str, voiceover: str, plan: dict) -> str:
    return f"""Write the screenplay for the CA Study Board. Return only the supplied strict JSON schema. This is a SCREENPLAY writer stage; do not change the director's beat count, order, or layout.\n\nCanonical question id: {qid}\nDirector plan (follow beat-for-beat):\n{json.dumps(plan, ensure_ascii=False)}\n\nQuestion:\n{question[:6000]}\nAnswer:\n{answer[:6000]}\nProvision summary:\n{provision[:5000]}\nVoice-over/source narration:\n{voiceover[:6000]}\n\nWrite one clear narration segment per planned beat. Use a broad example that walks through every point, but use only names, sections, dates, and amounts supported by the supplied material. Include each listed anchor phrase verbatim in its beat's voice_sync_text so the acoustic aligner can place the matching visual. Keep visible text concise and specific. Populate the exact layout-specific visual_data fields. For example_scene, decompose every actor and key fact into labeled elements. The last takeaway beat summarizes the teaching points. No at/start/end timestamps; the acoustic aligner assigns all timing."""

def generate_dynamic_screenplay(qid: str, question: str, answer: str, provision: str, mindmap: dict[str, Any] | None = None) -> dict:
    voiceover = voiceover_context(mindmap, answer)
    plan = _generate_json(_director_prompt(question, answer, provision, voiceover), DIRECTOR_SCHEMA, "Director")
    if plan.get("archetype") not in ARCHETYPES or not isinstance(plan.get("beat_plan"), list):
        raise ValueError("Director returned an invalid archetype or beat plan")
    allowed = ARCHETYPE_LAYOUTS[plan["archetype"]]
    if len(plan["beat_plan"]) < 3 or len(plan["beat_plan"]) > 8 or plan["beat_plan"][0].get("layout") != "example_scene" or plan["beat_plan"][-1].get("layout") != "takeaway":
        raise ValueError("Director plan must open with an example scene, contain 3-8 beats, and end with a takeaway")
    if any(beat.get("layout") not in allowed for beat in plan["beat_plan"]):
        raise ValueError("Director selected a layout outside its archetype's visual vocabulary")
    writer = _generate_json(_writer_prompt(qid, question, answer, provision, voiceover, plan), _writer_schema(plan), "Screenplay writer")
    beats = [writer.get(f"beat_{i}") for i in range(1, len(plan["beat_plan"]) + 1)]
    if any(not isinstance(beat, dict) for beat in beats) or [b.get("layout") for b in beats] != [b["layout"] for b in plan["beat_plan"]]:
        raise ValueError("Screenplay writer changed the director's beat count or layout order")
    for i, beat in enumerate(beats):
        beat["start"] = 0.0
        beat["end"] = 0.0
        beat["id"] = f"b{i + 1}"
        beat["title"]["at"] = 0.0
        beat["director_goal"] = plan["beat_plan"][i]["beat_goal"]
        beat["anchor_phrases"] = plan["beat_plan"][i]["anchor_phrases"]
        beat["animation_role"] = "key_fact" if i in (0, len(beats) - 1) else "explanation"
    return {
        "question_id": qid,
        "audio_url": "",
        "duration_sec": 0.0,
        "sync_offset_sec": 0.0,
        "context_pill": writer.get("context_pill") or f"{plan['archetype'].replace('_', ' ').title()} · {qid}",
        "example_summary": writer.get("example_summary", ""),
        "director": {key: plan[key] for key in ("archetype", "justification", "protagonist", "actors", "key_numbers", "key_dates", "visual_metaphor")},
        "fallback": False,
        "beats": beats,
    }
