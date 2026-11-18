"""Two-stage provision director and strict, layout-specific screenplay writer."""

from __future__ import annotations

import json
import ast
import os
import re
from typing import Any

from google import genai
from google.genai import types

from pipeline.key_rotator import rotator
from pipeline.validate_screenplay import validate_screenplay, number_keys, money_phrases, stringify, date_keys, DATE_RE, _date_key_supported
from pipeline.synthesize_ppt_audio import TTS_STYLE

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
    # Gemini's response_schema subset rejects JSON Schema's
    # additionalProperties field; keep objects closed in the writer prompt and
    # validate the returned object in Python instead.
    return {"type": "object", "properties": properties, "required": required or list(properties)}

def string_list() -> dict:
    return {"type": "array", "items": {"type": "string"}}

DIRECTOR_SCHEMA = obj({
    "archetype": {"type": "string", "enum": ARCHETYPES},
    "justification": {"type": "string"},
    "protagonist": {"type": "string"},
    "actors": string_list(),
    "key_numbers": string_list(),
    "key_dates": {"type": "array", "items": {"type": "string"}},
    "visual_metaphor": {"type": "string"},
    "beat_plan": {"type": "array", "items": obj({
        "beat_goal": {"type": "string"},
        "layout": {"type": "string", "enum": LAYOUTS},
        "anchor_phrases": {"type": "array", "items": {"type": "string"}},
    })},
}, ["archetype", "justification", "protagonist", "actors", "key_numbers", "key_dates", "visual_metaphor", "beat_plan"])

ITEM = obj({
    "label": {"type": "string"}, "detail": {"type": "string"},
    "value": {"type": "string"}, "date": {"type": "string"},
    "amount": {"type": "number"}, "pass": {"type": "boolean"},
    "from": {"type": "string"}, "to": {"type": "string"},
    "sign": {"type": "string", "enum": ["+", "-", "="]},
    "window_start": {"type": "string"}, "window_end": {"type": "string"},
    "status": {"type": "string"}, "icon": {"type": "string", "enum": ["person", "house", "plot", "shares", "factory", "money_bag", "document", "gavel", "bank", "calendar", "padlock", "scales"]},
}, ["label"])

DATA_SCHEMAS = {
    "example_scene": obj({"actors": {"type": "array", "items": ITEM}, "transaction": {"type": "string"}, "facts": {"type": "array", "items": ITEM}}, ["actors", "transaction", "facts"]),
    "decision_tree": obj({"root": {"type": "string"}, "branches": {"type": "array", "items": ITEM}}, ["root", "branches"]),
    "checklist_gate": obj({"conditions": {"type": "array", "items": ITEM}, "outcome": {"type": "string"}}, ["conditions", "outcome"]),
    "timeline_windows": obj({"events": {"type": "array", "items": ITEM}, "window_label": {"type": "string"}}, ["events", "window_label"]),
    "flow_actors": obj({"actors": {"type": "array", "items": ITEM}, "edges": {"type": "array", "items": ITEM}}, ["actors", "edges"]),
    "compare_regimes": obj({"regimes": {"type": "array", "items": ITEM}}, ["regimes"]),
    "slab_ladder": obj({"tiers": {"type": "array", "items": ITEM}}, ["tiers"]),
    "ledger": obj({"rows": {"type": "array", "items": ITEM}, "total": {"type": "string"}}, ["rows", "total"]),
    "waterfall": obj({"stages": {"type": "array", "items": ITEM}}, ["stages"]),
    "deemed_value": obj({"actual": ITEM, "deemed": ITEM, "rule": {"type": "string"}}, ["actual", "deemed", "rule"]),
    "case_card": obj({"case_name": {"type": "string"}, "court": {"type": "string"}, "principle": {"type": "string"}, "application": {"type": "string"}}, ["case_name", "principle", "application"]),
    "statute_quote": obj({"rule": {"type": "string"}, "citation": {"type": "string"}, "application": {"type": "string"}}, ["rule", "citation", "application"]),
    "takeaway": obj({"rules": {"type": "array", "items": ITEM}}, ["rules"]),
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
    models = [
        "gemini-3.8-flash", "gemini-3.5-flash", "gemini-3-flash-preview",
        "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash",
    ]
    failures = []
    for model in models:
        print(f"  [SCREENPLAY API] {label}: trying {model}", flush=True)
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
            result = rotator.execute_with_retry(
                call,
                timeout_ms=int(os.getenv("GEMINI_SCREENPLAY_TIMEOUT_MS", "30000")),
                retry_transient=False,
            )
            if isinstance(result, dict):
                return result
            failures.append(f"{model}: returned {type(result).__name__}, expected object")
        except Exception as exc:
            failures.append(f"{model}: {type(exc).__name__}: {exc}")
    raise RuntimeError(f"{label} structured generation failed for all models: " + " | ".join(failures))

def _director_prompt(question: str, answer: str, provision: str, voiceover: str, feedback: str = "") -> str:
    return f"""You are the visual director for a CA tax-law explainer. Choose an explanation structure based on the provision's actual mechanism and question facts. Return only the supplied JSON schema. Do not write the voice-over.\n\nQuestion:\n{question[:6000]}\n\nAnswer:\n{answer[:6000]}\n\nProvision summary:\n{provision[:5000]}\n\nExisting voice-over/source narration:\n{voiceover[:6000]}\n\nRules: choose exactly one listed archetype; justify in one sentence tied to facts in this question. List source-grounded people, amounts, dates, and legal anchors. Plan 3-8 ordered beats total, never 9 or more; count the beats before returning. Combine closely related points into one beat when needed so every distinct provision point is covered within eight beats. Beat 1 must be 'example_scene' and establish a broad view of the full example. End the plan with layout 'takeaway'. Select each middle layout to fit that beat's concept; vary the structures when the facts call for it, and do not follow a fixed archetype sequence. Anchor phrases must be short English statutory terms, section references, names, or exact numerals/amounts that Whisper can recognize. Choose layouts only from the schema. Do not invent legal tests, dates, amounts, or case citations.\n\nQuality-gate feedback from the prior attempt (if any):\n{feedback}"""

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
            # Keep the provider-facing schema compact. The layout-specific
            # payload is JSON-encoded in this field and parsed/validated below.
            "visual_data": {"type": "string"},
        }, ["layout", "title", "voice_sync_text", "visual_data"])
    required = ["question_id", "context_pill", "example_summary", *[f"beat_{i}" for i in range(1, len(plan["beat_plan"]) + 1)]]
    return obj(properties, required)

def _writer_prompt(qid: str, question: str, answer: str, provision: str, voiceover: str, plan: dict, feedback: str = "") -> str:
    layout_specs = "\n".join(f"{i+1}. {beat['layout']} visual_data fields: {json.dumps(DATA_SCHEMAS[beat['layout']], ensure_ascii=False)}" for i, beat in enumerate(plan["beat_plan"]))
    return f"""Write the screenplay for the CA Study Board. Return only the supplied strict JSON schema. This is a SCREENPLAY writer stage; do not change the director's beat count, order, or layout.\n\nCanonical question id: {qid}\nDirector plan (follow beat-for-beat):\n{json.dumps(plan, ensure_ascii=False)}\n\nLayout-specific visual data formats (visual_data must be a JSON object encoded as a string):\n{layout_specs}\n\nQuestion:\n{question[:6000]}\nAnswer:\n{answer[:6000]}\nProvision summary:\n{provision[:5000]}\nVoice-over/source narration:\n{voiceover[:6000]}\n\nNarration language and persona: speak the explanatory narration in natural Malayalam in a warm, patient Indian tax-teacher voice, using a concrete example story throughout. Keep statutory terms, section references, names, acronyms, amounts, percentages, numerals, and years in English/Latin script or Manglish exactly as in the source. Match the existing Stage 2 voice style: {TTS_STYLE}\n\nWrite one clear narration segment per planned beat. Use a broad example that walks through every point, but use only names, sections, dates, and amounts supported by the supplied material. Include each listed English anchor phrase verbatim in its beat's voice_sync_text so the acoustic aligner can place the matching visual. Also place every listed anchor that contains a numeral/amount verbatim in that beat's visible visual_data. Every amount, percentage, year, or date spoken in a beat MUST appear verbatim in that same beat's visible visual_data (as a label, value, or element); if it is not needed for teaching, omit it from the narration. Before returning, compare the numbers in each voice_sync_text against that beat's visual_data and add any missing source-supported figures to its displayed facts/rows/value/detail fields. Do not turn section numbers, dates, or amounts into standalone calculations that change their meaning. Keep visible text concise and specific. Populate the exact layout-specific visual_data fields. Return visual_data as valid JSON text matching the listed format. For example_scene, decompose every actor and key fact into labeled elements. The last takeaway beat summarizes the teaching points. No at/start/end timestamps; the acoustic aligner assigns all timing.\n\nQuality-gate feedback from the prior attempt (if any):\n{feedback}"""

def generate_dynamic_screenplay(qid: str, question: str, answer: str, provision: str, mindmap: dict[str, Any] | None = None) -> dict:
    voiceover = voiceover_context(mindmap, answer)
    from pipeline.validate_screenplay import ROOT as PROJECT_ROOT
    existing = []
    directory = PROJECT_ROOT / "redesign_demo" / "data" / "screenplays"
    for path in directory.glob("*.json"):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            if item.get("question_id") != qid and str(item.get("question_id", "")).startswith(qid.rsplit("-q", 1)[0] + "-"):
                existing.append(item)
        except Exception:
            continue
    feedback = ""
    last_errors = []
    reusable_plan = None
    best_candidate = None
    best_errors = []
    best_error_count = float("inf")
    for attempt in range(3):
        try:
            plan = reusable_plan or _generate_json(_director_prompt(question, answer, provision, voiceover, feedback), DIRECTOR_SCHEMA, "Director")
            if plan.get("archetype") not in ARCHETYPES or not isinstance(plan.get("beat_plan"), list):
                reusable_plan = None
                raise ValueError("Director returned an invalid archetype or beat plan")
            reusable_plan = plan
            print(f"[DIRECTOR PLAN] {qid} archetype={plan['archetype']}", flush=True)
            for planned in plan["beat_plan"]:
                print(f"  - {planned.get('layout')}: {planned.get('beat_goal')} | anchors={planned.get('anchor_phrases', [])}", flush=True)
            if len(plan["beat_plan"]) < 3 or len(plan["beat_plan"]) > 8 or plan["beat_plan"][0].get("layout") != "example_scene" or plan["beat_plan"][-1].get("layout") != "takeaway":
                reusable_plan = None
                raise ValueError("Director plan must open with an example scene, contain 3-8 beats, and end with a takeaway")
            layout_counts: dict[str, int] = {}
            for beat in plan["beat_plan"]:
                layout = str(beat.get("layout", ""))
                layout_counts[layout] = layout_counts.get(layout, 0) + 1
            if layout_counts and max(layout_counts.values()) / len(plan["beat_plan"]) > 0.40:
                reusable_plan = None
                raise ValueError("Director plan layout concentration exceeds 40%; choose more distinct middle layouts")
            if any(not isinstance(beat.get("anchor_phrases"), list) or not beat["anchor_phrases"] for beat in plan["beat_plan"]):
                reusable_plan = None
                raise ValueError("Every director beat must provide at least one English acoustic anchor phrase")
            source_context = " ".join((question or "", answer or "", provision or "", voiceover or ""))
            opening_anchors = plan["beat_plan"][0]["anchor_phrases"]
            source_has_example_value = bool(number_keys(source_context) or date_keys(source_context))
            if source_has_example_value and not any(number_keys(anchor) or date_keys(anchor) for anchor in opening_anchors):
                supported_numbers = [value for value in plan.get("key_numbers", []) if number_keys(value) and number_keys(value).issubset(number_keys(source_context))]
                source_date_phrases = [value for value in DATE_RE.findall(source_context) if date_keys(value) and date_keys(value).issubset(date_keys(source_context))]
                supported_dates = [value for value in plan.get("key_dates", []) if date_keys(value) and date_keys(value).issubset(date_keys(source_context))]
                supported_dates.extend(value for value in source_date_phrases if value not in supported_dates)
                example_anchor = next(iter(supported_numbers or supported_dates), None)
                if example_anchor:
                    opening_anchors.append(example_anchor)
                else:
                    reusable_plan = None
                    raise ValueError("Director example scene needs a source-supported visible amount or date anchor")
            source_dates = date_keys(source_context)
            unsupported_plan_dates = {key for key in date_keys(stringify(plan)) if not _date_key_supported(key, source_dates)}
            if unsupported_plan_dates:
                reusable_plan = None
                raise ValueError(f"Director plan contains unsupported date(s): {', '.join(sorted(unsupported_plan_dates))}")
            writer = _generate_json(_writer_prompt(qid, question, answer, provision, voiceover, plan, feedback), _writer_schema(plan), "Screenplay writer")
            beats = [writer.get(f"beat_{i}") for i in range(1, len(plan["beat_plan"]) + 1)]
            if any(not isinstance(beat, dict) for beat in beats) or [b.get("layout") for b in beats] != [b["layout"] for b in plan["beat_plan"]]:
                raise ValueError("Screenplay writer changed the director's beat count or layout order")
            for i, beat in enumerate(beats):
                if isinstance(beat.get("visual_data"), str):
                    payload = beat["visual_data"].strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                    try:
                        beat["visual_data"] = json.loads(payload)
                    except json.JSONDecodeError:
                        beat["visual_data"] = ast.literal_eval(payload)
                visual_numbers = number_keys(stringify(beat.get("visual_data", {})))
                spoken_numbers = number_keys(beat.get("voice_sync_text", ""))
                missing_numbers = spoken_numbers - visual_numbers
                if missing_numbers and isinstance(beat.get("visual_data"), dict):
                    spoken_phrases = money_phrases(beat.get("voice_sync_text", ""))
                    callouts = [phrase for phrase in spoken_phrases if number_keys(phrase) & missing_numbers]
                    if callouts:
                        beat["visual_data"]["spoken_amounts"] = list(dict.fromkeys(callouts))
                visible_dates = date_keys(stringify(beat.get("visual_data", {})))
                spoken_dates = date_keys(beat.get("voice_sync_text", ""))
                missing_dates = spoken_dates - visible_dates
                if beat.get("layout") == "example_scene" and not (number_keys(stringify(beat.get("visual_data", {}))) or visible_dates):
                    spoken_dates |= set().union(*(date_keys(anchor) for anchor in plan["beat_plan"][i].get("anchor_phrases", [])))
                    missing_dates |= spoken_dates - visible_dates
                if missing_dates and isinstance(beat.get("visual_data"), dict):
                    date_phrases = [phrase for phrase in DATE_RE.findall(beat.get("voice_sync_text", "")) if date_keys(phrase) & missing_dates]
                    if beat.get("layout") == "example_scene" and not date_phrases:
                        date_phrases = [phrase for anchor in plan["beat_plan"][i].get("anchor_phrases", []) for phrase in DATE_RE.findall(anchor) if date_keys(phrase) & missing_dates]
                    if date_phrases:
                        beat["visual_data"]["spoken_dates"] = list(dict.fromkeys(date_phrases))
                if beat.get("layout") == "example_scene" and not (number_keys(stringify(beat.get("visual_data", {}))) or date_keys(stringify(beat.get("visual_data", {})))) and isinstance(beat.get("visual_data"), dict):
                    source_dates = date_keys(source_context)
                    supported_key_dates = [phrase for phrase in plan.get("key_dates", []) if date_keys(phrase) and date_keys(phrase).issubset(source_dates)]
                    if supported_key_dates:
                        beat["visual_data"]["spoken_dates"] = list(dict.fromkeys(supported_key_dates))
                beat["start"] = 0.0
                beat["end"] = 0.0
                beat["id"] = f"b{i + 1}"
                beat["title"]["at"] = 0.0
                beat["director_goal"] = plan["beat_plan"][i]["beat_goal"]
                beat["anchor_phrases"] = plan["beat_plan"][i]["anchor_phrases"]
                beat["animation_role"] = "key_fact" if i in (0, len(beats) - 1) else "explanation"
            candidate = {
                "question_id": qid,
                "audio_url": "",
                "duration_sec": 0.0,
                "sync_offset_sec": 0.0,
                "context_pill": writer.get("context_pill") or f"{plan['archetype'].replace('_', ' ').title()} · {qid}",
                "example_summary": writer.get("example_summary", ""),
                "source_provision": provision,
                "director": {key: plan[key] for key in ("archetype", "justification", "protagonist", "actors", "key_numbers", "key_dates", "visual_metaphor", "beat_plan")},
                "fallback": False,
                "beats": beats,
            }
            last_errors = validate_screenplay(candidate, question, answer, f"{provision}\n{voiceover}", existing)
            if not last_errors:
                return candidate
            if len(last_errors) < best_error_count:
                best_candidate = candidate
                best_errors = list(last_errors)
                best_error_count = len(last_errors)
            if any("layout concentration" in issue for issue in last_errors):
                reusable_plan = None
        except Exception as exc:
            last_errors = [str(exc)]
        feedback = "; ".join(last_errors)
        print(f"  [SCREENPLAY QUALITY GATE] attempt {attempt + 1}/3 rejected {qid}: {feedback}")
    if best_candidate is not None:
        best_candidate["needs_review"] = True
        best_candidate["quality_issues"] = best_errors
        print(f"[SCREENPLAY NEEDS REVIEW] {qid}: {'; '.join(best_errors)}", flush=True)
        return best_candidate
    raise ValueError(f"Screenplay generation failed before a candidate could be built for {qid}: {'; '.join(last_errors)}")
