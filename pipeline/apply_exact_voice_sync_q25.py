# -*- coding: utf-8 -*-
import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"C:\Users\HP\OneDrive\Desktop\VISHNU\DT and IDT Classes"

# Measured audio-grounded screenplay based on exact speech phrase boundaries
screenplay = {
    "question_id": "dt-c2-q25",
    "audio_url": "data/audio/dt-c2-q25.mp3",
    "duration_sec": 127.64,
    "sync_offset_sec": 0.0,
    "context_pill": "§ 54 · Two Residential Houses & § 51 Advance Forfeiture",
    "fallback": False,
    "beats": [
        {
            "id": "b1",
            "layout": "fork",
            "start": 0.0,
            "end": 26.65,
            "voice_sync_text": "സെക്ഷൻ 51 പ്രകാരം, നെഗോഷ്യേഷൻ സമയത്ത് ലഭിച്ച അഡ്വാൻസ് മണി ഫോർഫീറ്റ് ചെയ്യുമ്പോൾ, അതിന്റെ ടാക്സ് ട്രീറ്റ്മെന്റ് എപ്പോൾ സംഭവിച്ചു എന്നതിനെ ആശ്രയിച്ചിരിക്കുന്നു. ഒന്നാം തീയതി ഏപ്രിൽ 2014-ന് മുൻപാണെങ്കിൽ, അത് കോസ്റ്റ് ഓഫ് അക്വിസിഷനിൽ നിന്ന് കുറയ്ക്കണം. എന്നാൽ ഒന്നാം തീയതി ഏപ്രിൽ 2014-ലോ അതിനുശേഷമോ ആണെങ്കിൽ, സെക്ഷൻ 56(2)(ix) പ്രകാരം ഇൻകം ഫ്രം അദർ സോഴ്സസ് ആയി ടാക്സ് ചെയ്യപ്പെടും.",
            "title": {
                "text": "Advance Money Forfeiture Cut-off",
                "at": 0.3
            },
            "divider": {
                "text": "When was the advance forfeited?",
                "at": 6.0
            },
            "branches": [
                {
                    "side": "left",
                    "label": "Before 01-04-2014",
                    "at": 10.1,
                    "facts": [
                        {
                            "text": "Deduct from Cost u/s 51",
                            "at": 13.8
                        }
                    ],
                    "outcome": {
                        "text": "Reduces Cost of Acquisition",
                        "at": 14.5
                    }
                },
                {
                    "side": "right",
                    "label": "On/After 01-04-2014",
                    "at": 17.0,
                    "facts": [
                        {
                            "text": "Taxable under IFOS u/s 56(2)(ix)",
                            "at": 19.9
                        }
                    ],
                    "outcome": {
                        "text": "Income from Other Sources",
                        "at": 21.5
                    }
                }
            ],
            "active": {
                "side": "left",
                "at": 13.8
            },
            "serves": ["p1", "p2", "c1", "c2", "f2", "d1", "n3", "t1"]
        },
        {
            "id": "b2",
            "layout": "statute_quote",
            "start": 26.90,
            "end": 46.79,
            "voice_sync_text": "ഇനി സെക്ഷൻ 54-ലേക്ക് വരാം. ജനറൽ റൂൾ അനുസരിച്ച് ഒരു റെസിഡൻഷ്യൽ വീടിന് മാത്രമേ ഇളവ് ലഭിക്കൂ. എന്നാൽ സെക്ഷൻ 54 സബ് സെക്ഷൻ ഒന്നിന്റെ ഫസ്റ്റ് പ്രൊവൈസോ പ്രകാരം, ചാർജബിൾ ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടി രൂപയിൽ കൂടുന്നില്ലെങ്കിൽ, അസ്സസ്സീക്ക് ഇന്ത്യയിൽ രണ്ട് റെസിഡൻഷ്യൽ വീടുകളിൽ നിക്ഷേപിക്കാനുള്ള അവസരം ലഭിക്കുന്നു.",
            "title": {
                "text": "Section 54(1) · First Proviso",
                "at": 27.2
            },
            "quote": {
                "text": "Capital gains up to [[₹ 2 Crore]] unlock [[two residential houses]]",
                "at": 37.1
            },
            "serves": ["p3", "c3", "n6", "t3"]
        },
        {
            "id": "b3",
            "layout": "meter",
            "start": 47.04,
            "end": 66.53,
            "voice_sync_text": "ഇവിടെ ത്രെഷോൾഡ് മീറ്റർ നോക്കൂ. സ്റ്റാറ്റ്യൂട്ടറി ലിമിറ്റ് രണ്ട് കോടി രൂപയാണ്. നമ്മുടെ കമ്പ്യൂട്ടേഷനിൽ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ വരുന്നത് 34 ലക്ഷത്തി 25,000 രൂപ മാത്രമാണ്. ഇത് രണ്ട് കോടി രൂപയിൽ താഴെയായതുകൊണ്ട്, അസ്സസ്സീക്ക് രണ്ട് വീടുകളിലും സെക്ഷൻ 54 എക്സംപ്ഷൻ പൂർണ്ണമായും ക്ലെയിം ചെയ്യാം.",
            "title": {
                "text": "Statutory Threshold Gauge",
                "at": 47.3
            },
            "limit": {
                "text": "Statutory Limit",
                "value": 20000000,
                "at": 49.5
            },
            "reading": {
                "text": "Long-Term Capital Gain",
                "value": 3425000,
                "at": 52.3,
                "fmt": "inr"
            },
            "outcome": {
                "text": "ELIGIBLE FOR 2 RESIDENTIAL HOUSES",
                "tone": "ok",
                "at": 61.6
            },
            "serves": ["c3", "n5", "n6"]
        },
        {
            "id": "b4",
            "layout": "case_card",
            "start": 66.78,
            "end": 87.27,
            "voice_sync_text": "ഡൽഹിയിലെ വീടിന്റെ കാര്യത്തിൽ രജിസ്ട്രേഷൻ പൂർത്തിയായില്ല എന്നതുകൊണ്ട് എക്സംപ്ഷൻ നിഷേധിക്കാമോ? ഒരിക്കലുമില്ല! ലാൻഡ്മാർക്ക് കേസായ ബൽരാജ് വേഴ്സസ് സി.ഐ.ടി.-യിൽ ഡൽഹി ഹൈക്കോടതി വ്യക്തമാക്കിയത്, മുഴുവൻ തുകയും നൽകി പൊസഷൻ കൈപ്പറ്റിയാൽ സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ലഭിക്കും. അതിനാൽ രജിസ്റ്റേർഡ് ഡീഡ് ഇല്ലെങ്കിലും സെക്ഷൻ 54 ഇളവ് ലഭ്യമാണ്.",
            "title": {
                "text": "Judicial Precedent · Legal Title",
                "at": 67.0
            },
            "gap": {
                "text": "Delhi house purchase agreement fully paid, but deed unregistered on 31-03-2026",
                "at": 67.2
            },
            "case": {
                "text": "Balraj v. CIT (2002)",
                "at": 73.8
            },
            "court": {
                "text": "Delhi High Court Benchmark",
                "at": 76.8
            },
            "principle": {
                "text": "Substantial ownership u/s 53A TPA satisfies Section 54 without registered deed",
                "at": 78.8
            },
            "effect": {
                "text": "Exemption Allowed for Delhi House (₹ 7,00,000)",
                "at": 83.2
            },
            "serves": ["c4", "f4", "cl1", "cl2", "t2"]
        },
        {
            "id": "b5",
            "layout": "ledger",
            "start": 87.52,
            "end": 112.73,
            "voice_sync_text": "ഇനി സ്റ്റാറ്റ്യൂട്ടറി കമ്പ്യൂട്ടേഷൻ ലെഡ്ജർ നോക്കാം. സെയിൽ കൺസിഡറേഷൻ 43 ലക്ഷം രൂപ. ലെസ്സ്: അഡ്ജസ്റ്റഡ് കോസ്റ്റ് ഓഫ് അക്വിസിഷൻ 8 ലക്ഷത്തി 75,000 രൂപ. ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ 34 ലക്ഷത്തി 25,000 രൂപ. ലെസ്സ്: ഡൽഹി വീടിന്റെ എക്സംപ്ഷൻ 7 ലക്ഷം രൂപ, ചെന്നൈ വീടിന്റെ എക്സംപ്ഷൻ 5 ലക്ഷം രൂപ. നെറ്റ് ടാക്സബിൾ ക്യാപിറ്റൽ ഗെയിൻ 22 ലക്ഷത്തി 25,000 രൂപ.",
            "title": {
                "text": "Statutory Capital Gains Ledger",
                "at": 87.8
            },
            "rows": [
                {
                    "sign": "plus",
                    "label": "Full Value of Consideration (FVC)",
                    "value": 4300000,
                    "at": 90.8,
                    "fmt": "inr"
                },
                {
                    "sign": "minus",
                    "label": "Less: Adjusted Cost (₹ 9L - ₹ 25k)",
                    "value": 875000,
                    "at": 94.4,
                    "fmt": "inr"
                },
                {
                    "sign": "plus",
                    "label": "Gross Long-Term Capital Gain",
                    "value": 3425000,
                    "at": 98.4,
                    "fmt": "inr"
                },
                {
                    "sign": "minus",
                    "label": "Less: Delhi House Exemption (Balraj v. CIT)",
                    "value": 700000,
                    "at": 103.1,
                    "fmt": "inr"
                },
                {
                    "sign": "minus",
                    "label": "Less: Chennai House Exemption (Second House)",
                    "value": 500000,
                    "at": 105.9,
                    "fmt": "inr"
                }
            ],
            "total": {
                "label": "Taxable Long-Term Capital Gain",
                "value": 2225000,
                "at": 108.7,
                "fmt": "inr"
            },
            "serves": ["f1", "f3", "f5", "c5", "d2", "d3", "d4", "n1", "n2", "n4", "n7", "n8", "n9", "n10"]
        },
        {
            "id": "b6",
            "layout": "takeaway",
            "start": 112.98,
            "end": 127.63,
            "voice_sync_text": "അതുകൊണ്ട് മൂന്ന് പ്രധാന നിയമങ്ങൾ എപ്പോഴും ഓർക്കുക: 2014-ന് മുൻപുള്ള അഡ്വാൻസ് ഫോർഫീച്ചർ കോസ്റ്റ് കുറയ്ക്കുന്നു, രണ്ട് കോടിയിൽ താഴെയുള്ള ഗെയിൻ രണ്ട് വീടുകൾക്ക് ഇളവ് നൽകുന്നു, രജിസ്ട്രേഷൻ ഇല്ലെങ്കിലും സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ഉണ്ടെങ്കിൽ സെക്ഷൻ 54 ലഭ്യമാകും.",
            "title": {
                "text": "Golden Statutory Rules",
                "at": 113.3
            },
            "subtitle": {
                "text": "Pre-2014 advance reduces cost; ₹ 2 Cr unlocks two residential houses",
                "at": 116.3
            },
            "serves": ["n10"]
        }
    ],
    "omitted": []
}

# 1. Save screenplay JSON
json_path = os.path.join(PROJECT_ROOT, "redesign_demo", "data", "screenplays", "dt-c2-q25.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(screenplay, f, indent=2, ensure_ascii=False)
print(f"Saved audio-measured screenplay to {json_path}")

# 2. Update explainer_engine.js
engine_path = os.path.join(PROJECT_ROOT, "redesign_demo", "frontend", "explainer_engine.js")
with open(engine_path, "r", encoding="utf-8") as f:
    engine_js = f.read()

fixture_str = "FIXTURES[\"dt-c2-q25\"] = " + json.dumps(screenplay, indent=2, ensure_ascii=False) + ";"
pattern = r'FIXTURES\["dt-c2-q25"\]\s*=\s*\{[\s\S]+?\};\n(?=FIXTURES\["dt_c2_q25"\])'

if re.search(pattern, engine_js):
    new_engine_js = re.sub(pattern, fixture_str + "\n", engine_js)
    with open(engine_path, "w", encoding="utf-8") as f:
        f.write(new_engine_js)
    print("Updated FIXTURES['dt-c2-q25'] in explainer_engine.js!")
else:
    print("Warning: regex pattern did not match in explainer_engine.js")
