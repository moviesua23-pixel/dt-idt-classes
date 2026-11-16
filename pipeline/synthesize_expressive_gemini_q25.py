# -*- coding: utf-8 -*-
import os
import sys
import json
import wave
import subprocess
import time
from pydub import AudioSegment

PROJECT_ROOT = r"C:\Users\HP\OneDrive\Desktop\VISHNU\DT and IDT Classes"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator
from google import genai
from google.genai import types

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = os.path.join(PROJECT_ROOT, "redesign_demo", "build", "dt-c2-q25", "cache", "gemini_clips")
os.makedirs(TEMP_DIR, exist_ok=True)

MODEL_NAME = 'gemini-2.5-flash-preview-tts'
VOICE_NAME = 'Aoede'
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2

# Pure, expressive Malayalam pedagogical scripts for Q25 featuring the Mr. Hari character example
SCRIPTS = [
    {
        "id": "b1",
        "layout": "fork",
        "voice_sync_text": (
            "സെക്ഷൻ 51-ന്റെ പ്രൊവിഷൻ മനസ്സിലാക്കാൻ നമുക്ക് ഹരിയുടെ ഒരു സിമ്പിൾ എക്സാമ്പിൾ നോക്കാം. "
            "ഹരി 2002-ൽ 9 ലക്ഷം രൂപയ്ക്ക് ഡൽഹിയിൽ ഒരു റെസിഡൻഷ്യൽ ഹൗസ് വാങ്ങി. "
            "2005 മെയ് മാസത്തിൽ പരി എന്ന ബയറുമായി നെഗോഷ്യേഷൻ നടത്തുമ്പോൾ 25,000 രൂപ അഡ്വാൻസ് മണി വാങ്ങി. "
            "പക്ഷെ പിന്നീട് ആ ഡീൽ കാൻസലാവുകയും ഹരി ആ അഡ്വാൻസ് ഫോർഫീറ്റ് ചെയ്യുകയും ചെയ്തു. "
            "ഇവിടെ ഒരു കട്ട്-ഓഫ് ഡേറ്റ് ഓർക്കുക: ഒന്നാം തീയതി ഏപ്രിൽ 2014-ന് മുൻപാണ് ഫോർഫീച്ചർ എങ്കിൽ, "
            "സെക്ഷൻ 51 പ്രകാരം അത് കോസ്റ്റ് ഓഫ് അക്വിസിഷനിൽ നിന്ന് കുറയ്ക്കണം! "
            "അതുകൊണ്ട് ഹരിയുടെ അഡ്ജസ്റ്റഡ് കോസ്റ്റ് 9 ലക്ഷത്തിൽ നിന്ന് 25,000 കുറച്ച് 8 ലക്ഷത്തി 75,000 രൂപയായി മാറുന്നു!"
        )
    },
    {
        "id": "b2",
        "layout": "statute_quote",
        "voice_sync_text": (
            "ഇനി 2025 ജൂൺ മാസത്തിൽ ഹരി ഈ വീട് 43 ലക്ഷം രൂപയ്ക്ക് വിൽക്കുന്നു. "
            "അപ്പോൾ ഹരിയുടെ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ വരുന്നത് 43 ലക്ഷം മൈനസ് 8 ലക്ഷത്തി 75,000, "
            "അതായത് 34 ലക്ഷത്തി 25,000 രൂപ! "
            "ഇവിടെ ഹരി ചോദിക്കുന്നു: 'എനിക്ക് സെക്ഷൻ 54 പ്രകാരം ഒരു വീടിന് പകരം രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങി എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാൻ പറ്റുമോ?' "
            "സെക്ഷൻ 54 സബ് സെക്ഷൻ ഒന്നിന്റെ ഫസ്റ്റ് പ്രൊവൈസോ പറയുന്നത് നോക്കൂ: "
            "ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടി രൂപയിൽ കവിയുന്നില്ലെങ്കിൽ, "
            "അസ്സസ്സീക്ക് ഇന്ത്യയിൽ രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങാനുള്ള സ്റ്റാറ്റ്യൂട്ടറി ഓപ്ഷൻ ലഭിക്കും!"
        )
    },
    {
        "id": "b3",
        "layout": "meter",
        "voice_sync_text": (
            "ഇവിടെ നമ്മുടെ ത്രെഷോൾഡ് മീറ്റർ നോക്കൂ! സ്റ്റാറ്റ്യൂട്ടറി ലിമിറ്റ് രണ്ട് കോടി രൂപയാണ്. "
            "ഹരിയുടെ ക്യാപിറ്റൽ ഗെയിൻ എത്രയാണ്? വെറും 34 ലക്ഷത്തി 25,000 രൂപ മാത്രം! "
            "ഇത് രണ്ട് കോടി രൂപയേക്കാൾ വളരെ താഴെയാണ്. "
            "അതുകൊണ്ട് ദാ, നമ്മുടെ പാഡ്‌ലോക്ക് ഓപ്പൺ ആയി! "
            "ഹരിക്ക് ജീവിതത്തിൽ ഒരിക്കൽ മാത്രം ലഭിക്കുന്ന ടു റെസിഡൻഷ്യൽ ഹൗസസ് ഓപ്ഷൻ ഇവിടെ അൺലോക്ക് ആയിരിക്കുന്നു!"
        )
    },
    {
        "id": "b4",
        "layout": "case_card",
        "voice_sync_text": (
            "ഹരി രണ്ട് വീടുകൾ വാങ്ങി. ഒന്ന് ചെന്നൈയിൽ 5 ലക്ഷം രൂപയ്ക്ക്, മറ്റൊന്ന് ഡൽഹിയിൽ 7 ലക്ഷം രൂപയ്ക്ക്. "
            "പക്ഷെ ഇവിടെ ഒരു വലിയ പ്രശ്നം വന്നു! "
            "ഡൽഹിയിലെ വീടിന്റെ മുഴുവൻ തുകയും നൽകി ഹരി കൈവശം വെച്ചെങ്കിലും, അതിന്റെ സെയിൽ ഡീഡ് രജിസ്റ്റർ ചെയ്തിട്ടില്ല! "
            "അസ്സസ്സിങ് ഓഫീസർ ചോദിക്കുന്നു: 'രജിസ്ട്രേഷൻ ഇല്ലാത്ത വീടിന് എങ്ങനെ സെക്ഷൻ 54 കൊടുക്കും?' "
            "ഇവിടെയാണ് ഡൽഹി ഹൈക്കോടതിയുടെ ലാൻഡ്മാർക്ക് കേസായ ബൽരാജ് വേഴ്സസ് സി.ഐ.ടി. വരുന്നത്! "
            "കോടതി വ്യക്തമാക്കി: സെക്ഷൻ 53A പ്രകാരം പൊസഷനും മുഴുവൻ പെയ്മെന്റും ഉണ്ടെങ്കിൽ സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ആയി. "
            "അതിനാൽ രജിസ്റ്റേർഡ് ഡീഡ് ഇല്ലെങ്കിലും ഡൽഹി വീടിന് സെക്ഷൻ 54 എക്സംപ്ഷൻ പൂർണ്ണമായും ലഭിക്കും!"
        )
    },
    {
        "id": "b5",
        "layout": "ledger",
        "voice_sync_text": (
            "ഇനി ഫൈനൽ ക്യാപിറ്റൽ ഗെയിൻസ് ലെഡ്ജർ നോക്കാം. ഫുൾ വാല്യൂ ഓഫ് കൺസിഡറേഷൻ 43 ലക്ഷം രൂപ. "
            "ലെസ്സ്: അഡ്ജസ്റ്റഡ് കോസ്റ്റ് ഓഫ് അക്വിസിഷൻ 8 ലക്ഷത്തി 75,000 രൂപ. "
            "ഗ്രോസ് ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ 34 ലക്ഷത്തി 25,000 രൂപ. "
            "ഇനി ഇതിൽ നിന്ന് രണ്ട് വീടുകളുടെയും എക്സംപ്ഷൻ കുറയ്ക്കാം: ഡൽഹി വീടിന് 7 ലക്ഷം, ചെന്നൈ വീടിന് 5 ലക്ഷം. "
            "ആകെ എക്സംപ്ഷൻ 12 ലക്ഷം രൂപ! ബാക്കി വരുന്ന തുക നോക്കൂ: "
            "34 ലക്ഷത്തി 25,000-ൽ നിന്ന് 12 ലക്ഷം കുറച്ചാൽ കൃത്യം 22 ലക്ഷത്തി 25,000 രൂപ! "
            "സ്റ്റുഡന്റ്സ് ഓർക്കുക, ഈ 22 ലക്ഷത്തി 25,000 രൂപ ടാക്സബിൾ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ ആണ്!"
        )
    },
    {
        "id": "b6",
        "layout": "takeaway",
        "voice_sync_text": (
            "അതുകൊണ്ട് എക്സാമിനായി മൂന്ന് ഗോൾഡൻ റൂൾസ് എപ്പോഴും ഓർക്കുക: "
            "ഒന്ന്, 2014-ന് മുൻപുള്ള അഡ്വാൻസ് ഫോർഫീച്ചർ കോസ്റ്റ് കുറയ്ക്കുന്നു. "
            "രണ്ട്, ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടിയിൽ താഴെയാണെങ്കിൽ രണ്ട് വീടുകൾക്ക് എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാം. "
            "മൂന്ന്, രജിസ്ട്രേഷൻ പൂർത്തിയായില്ലെങ്കിലും സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ഉണ്ടെങ്കിൽ സെക്ഷൻ 54 ലഭിക്കും. "
            "ബാക്കി വരുന്ന ഗെയിൻ കൃത്യമായി ടാക്സ് ചെയ്യപ്പെടും!"
        )
    }
]

def synthesize_clip(client, text, beat_id):
    print(f"Synthesizing Beat {beat_id} with Gemini Voice ({VOICE_NAME})...", flush=True)
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=[text],
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
                )
            )
        )
    )
    if not resp.candidates or not resp.candidates[0].content or not resp.candidates[0].content.parts:
        raise RuntimeError(f"No audio returned for {beat_id}: {resp}")
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_path = os.path.join(TEMP_DIR, f"{beat_id}.wav")
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(BYTES_PER_SAMPLE)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    seg = AudioSegment.from_wav(wav_path)
    dur = len(seg) / 1000.0
    print(f"  -> Beat {beat_id} generated: {dur:.2f}s ({len(pcm)} bytes)", flush=True)
    return seg, dur

def main():
    print("=== SYNTHESIZING EXPRESSIVE GEMINI VOICE FOR Q25 ===")
    clips = []
    for item in SCRIPTS:
        beat_id = item["id"]
        wav_path = os.path.join(TEMP_DIR, f"{beat_id}.wav")
        if os.path.exists(wav_path):
            print(f"Loading cached {beat_id} from {wav_path}...")
            seg = AudioSegment.from_wav(wav_path)
            dur = len(seg) / 1000.0
        else:
            seg, dur = rotator.execute_with_retry(synthesize_clip, item["voice_sync_text"], beat_id)
            time.sleep(1.0)
        clips.append({
            "id": beat_id,
            "layout": item["layout"],
            "seg": seg,
            "dur": dur,
            "voice_sync_text": item["voice_sync_text"]
        })

    # Stitch clips with 250ms silence
    silence = AudioSegment.silent(duration=250)
    assembled = AudioSegment.empty()
    timed_beats = []
    current_time = 0.0

    for idx, c in enumerate(clips):
        start_t = round(current_time, 2)
        end_t = round(current_time + c["dur"], 2)
        timed_beats.append({
            "id": c["id"],
            "layout": c["layout"],
            "start": start_t,
            "end": end_t,
            "dur": c["dur"],
            "voice_sync_text": c["voice_sync_text"]
        })
        assembled += c["seg"]
        current_time = end_t
        if idx < len(clips) - 1:
            assembled += silence
            current_time = round(current_time + 0.250, 2)

    total_duration = round(len(assembled) / 1000.0, 2)
    print(f"\nTotal Assembled Audio Duration: {total_duration}s")
    for tb in timed_beats:
        print(f"  Beat {tb['id']} ({tb['layout']}): {tb['start']:.2f}s -> {tb['end']:.2f}s (dur={tb['dur']:.2f}s)")

    # Export MP3
    audio_out_dir = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "audio")
    os.makedirs(audio_out_dir, exist_ok=True)
    mp3_path = os.path.join(audio_out_dir, "dt-c2-q25.mp3")

    temp_stitched_wav = os.path.join(TEMP_DIR, "dt-c2-q25_final.wav")
    assembled.export(temp_stitched_wav, format="wav")

    subprocess.run([
        "ffmpeg", "-y", "-i", temp_stitched_wav,
        "-b:a", "192k",
        "-ar", "24000",
        mp3_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Exported master MP3 to: {mp3_path}")

    # Build Screenplay JSON with exact proportional visual animation triggers
    t = {b["id"]: b for b in timed_beats}

    screenplay = {
        "question_id": "dt-c2-q25",
        "audio_url": "data/audio/dt-c2-q25.mp3",
        "duration_sec": total_duration,
        "sync_offset_sec": 0.0,
        "context_pill": "§ 54 · Two Residential Houses & § 51 Advance Forfeiture",
        "fallback": False,
        "beats": [
            {
                "id": "b1",
                "layout": "fork",
                "start": t["b1"]["start"],
                "end": t["b1"]["end"],
                "voice_sync_text": t["b1"]["voice_sync_text"],
                "title": {"text": "Advance Money Forfeiture Cut-off", "at": round(t["b1"]["start"] + 0.5, 2)},
                "divider": {"text": "When was the advance forfeited?", "at": round(t["b1"]["start"] + 1.5, 2)},
                "branches": [
                    {
                        "side": "left",
                        "label": "Before 01-04-2014",
                        "facts": [{"text": "Deduct from Cost u/s 51", "at": round(t["b1"]["start"] + 5.0, 2)}],
                        "outcome": {"text": "Reduces Cost of Acquisition", "at": round(t["b1"]["start"] + 7.5, 2)}
                    },
                    {
                        "side": "right",
                        "label": "On/After 01-04-2014",
                        "facts": [{"text": "Taxable under IFOS u/s 56(2)(ix)", "at": round(t["b1"]["start"] + 11.0, 2)}],
                        "outcome": {"text": "Income from Other Sources", "at": round(t["b1"]["start"] + 13.5, 2)}
                    }
                ],
                "active": {"side": "left", "at": round(t["b1"]["start"] + 6.0, 2)},
                "serves": ["p1", "p2", "c1", "c2", "f2", "d1", "n3", "t1"]
            },
            {
                "id": "b2",
                "layout": "statute_quote",
                "start": t["b2"]["start"],
                "end": t["b2"]["end"],
                "voice_sync_text": t["b2"]["voice_sync_text"],
                "title": {"text": "Section 54(1) · First Proviso", "at": round(t["b2"]["start"] + 0.5, 2)},
                "quote": {"text": "Capital gains up to [[₹ 2 Crore]] unlock [[two residential houses]]", "at": round(t["b2"]["start"] + 2.5, 2)},
                "serves": ["p3", "c3", "n6", "t3"]
            },
            {
                "id": "b3",
                "layout": "meter",
                "start": t["b3"]["start"],
                "end": t["b3"]["end"],
                "voice_sync_text": t["b3"]["voice_sync_text"],
                "title": {"text": "Statutory Threshold Gauge", "at": round(t["b3"]["start"] + 0.5, 2)},
                "limit": {"text": "Statutory Limit", "value": 20000000, "at": round(t["b3"]["start"] + 1.5, 2)},
                "reading": {"text": "Long-Term Capital Gain", "value": 3425000, "at": round(t["b3"]["start"] + 3.5, 2), "fmt": "inr"},
                "outcome": {"text": "ELIGIBLE FOR 2 RESIDENTIAL HOUSES", "tone": "ok", "at": round(t["b3"]["start"] + 7.0, 2)},
                "serves": ["c3", "n5", "n6"]
            },
            {
                "id": "b4",
                "layout": "case_card",
                "start": t["b4"]["start"],
                "end": t["b4"]["end"],
                "voice_sync_text": t["b4"]["voice_sync_text"],
                "title": {"text": "Judicial Precedent · Legal Title", "at": round(t["b4"]["start"] + 0.5, 2)},
                "case": {"text": "Balraj v. CIT (2002)", "at": round(t["b4"]["start"] + 2.0, 2)},
                "court": {"text": "Delhi High Court Benchmark", "at": round(t["b4"]["start"] + 2.5, 2)},
                "gap": {"text": "Delhi house purchase agreement fully paid, but deed unregistered on 31-03-2026", "at": round(t["b4"]["start"] + 5.0, 2)},
                "principle": {"text": "Substantial ownership u/s 53A TPA satisfies Section 54 without registered deed", "at": round(t["b4"]["start"] + 8.5, 2)},
                "effect": {"text": "Exemption Allowed for Delhi House (₹ 7,00,000)", "at": round(t["b4"]["start"] + 13.0, 2)},
                "serves": ["c4", "f4", "cl1", "cl2", "t2"]
            },
            {
                "id": "b5",
                "layout": "ledger",
                "start": t["b5"]["start"],
                "end": t["b5"]["end"],
                "voice_sync_text": t["b5"]["voice_sync_text"],
                "title": {"text": "Statutory Capital Gains Ledger", "at": round(t["b5"]["start"] + 0.5, 2)},
                "rows": [
                    {"sign": "plus", "label": "Full Value of Consideration (FVC)", "value": 4300000, "at": round(t["b5"]["start"] + 2.0, 2), "fmt": "inr"},
                    {"sign": "minus", "label": "Less: Adjusted Cost (₹ 9L - ₹ 25k)", "value": 875000, "at": round(t["b5"]["start"] + 4.5, 2), "fmt": "inr"},
                    {"sign": "plus", "label": "Gross Long-Term Capital Gain", "value": 3425000, "at": round(t["b5"]["start"] + 7.5, 2), "fmt": "inr"},
                    {"sign": "minus", "label": "Less: Delhi House Exemption (Balraj v. CIT)", "value": 700000, "at": round(t["b5"]["start"] + 11.0, 2), "fmt": "inr"},
                    {"sign": "minus", "label": "Less: Chennai House Exemption (Second House)", "value": 500000, "at": round(t["b5"]["start"] + 14.5, 2), "fmt": "inr"}
                ],
                "total": {"label": "Taxable Long-Term Capital Gain", "value": 2225000, "at": round(t["b5"]["start"] + 18.0, 2), "fmt": "inr"},
                "serves": ["f1", "f3", "f5", "c5", "d2", "d3", "d4", "n1", "n2", "n4", "n7", "n8", "n9", "n10"]
            },
            {
                "id": "b6",
                "layout": "takeaway",
                "start": t["b6"]["start"],
                "end": t["b6"]["end"],
                "voice_sync_text": t["b6"]["voice_sync_text"],
                "title": {"text": "Golden Statutory Rules", "at": round(t["b6"]["start"] + 0.5, 2)},
                "subtitle": {"text": "Pre-2014 advance reduces cost; ₹ 2 Cr unlocks two residential houses", "at": round(t["b6"]["start"] + 3.0, 2)},
                "serves": ["n10"]
            }
        ],
        "omitted": []
    }

    # Save to screenplay json
    json_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", "dt-c2-q25.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(screenplay, f, indent=2, ensure_ascii=False)
    print(f"Updated screenplay JSON at: {json_path}")

    # Update explainer_engine.js FIXTURES["dt-c2-q25"]
    engine_path = os.path.join(PROJECT_ROOT, "redesign_demo", "frontend", "explainer_engine.js")
    with open(engine_path, "r", encoding="utf-8") as f:
        engine_js = f.read()

    import re
    fixture_str = "FIXTURES[\"dt-c2-q25\"] = " + json.dumps(screenplay, indent=2, ensure_ascii=False) + ";"
    pattern = r'FIXTURES\["dt-c2-q25"\]\s*=\s*\{[\s\S]+?\};\n(?=FIXTURES\["dt_c2_q25"\])'
    
    if re.search(pattern, engine_js):
        new_engine_js = re.sub(pattern, fixture_str + "\n", engine_js)
        with open(engine_path, "w", encoding="utf-8") as f:
            f.write(new_engine_js)
        print("Updated FIXTURES['dt-c2-q25'] in explainer_engine.js successfully!")
    else:
        print("Warning: regex match failed for FIXTURES['dt-c2-q25'] in explainer_engine.js")

if __name__ == "__main__":
    main()
