"""
pipeline/build_perfect_mindmaps.py
Constructs the complete, authoritative, and validated mindmaps.json for Topics q1 through q10.
Adheres strictly to all requirements of Request 10.
"""

import os
import sys
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
TIMING_AUDIT_PATH = os.path.join(DATA_DIR, "mindmap_timing_audit.json")
MINDMAPS_PATH = os.path.join(DATA_DIR, "mindmaps.json")

# Load timing audit
audit = json.load(open(TIMING_AUDIT_PATH, encoding='utf-8'))

ALLOWED_ICONS = {"scales", "shield", "calculator", "percent", "cap", "warning", "gear", "check", "user", "building", "rupee"}

def compute_flow_steps(last_beat_t0, last_beat_t1, step_defs):
    """
    Reveals flow summary steps evenly during the last 30% of the last beat.
    """
    dur = last_beat_t1 - last_beat_t0
    flow_start = last_beat_t1 - (0.30 * dur)
    n = len(step_defs)
    step_dur = (last_beat_t1 - flow_start) / n
    res = []
    for i, s in enumerate(step_defs):
        s_t0 = round(flow_start + (i * step_dur), 2)
        s_t1 = round(flow_start + ((i + 1) * step_dur), 2)
        if i == n - 1:
            s_t1 = round(last_beat_t1, 2)
        res.append({
            "label": s["label"],
            "sub": s["sub"],
            "icon": s["icon"],
            "t0": s_t0,
            "t1": s_t1
        })
    return res

def build_q1():
    # Audio length: 80.81s
    # Slides 1..4
    s1_beats = audit["q1"]["slides"][0]["beats"]
    s2_beats = audit["q1"]["slides"][1]["beats"]
    s3_beats = audit["q1"]["slides"][2]["beats"]
    s4_beats = audit["q1"]["slides"][3]["beats"]
    
    return {
        "question_id": "q1",
        "question_title": "Diversion vs Application of Income: Legal Concepts & SC Benchmarks",
        "audio_file": "data/audio/q1.mp3",
        "total_duration": audit["q1"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_core",
                "branch_title": "Total Income & The Overriding Title Rule",
                "badge": "§ 4 Charging Section",
                "icon": "scales",
                "t0": audit["q1"]["slides"][0]["t0"],
                "t1": audit["q1"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q1_p1_1",
                        "title": "Section 4 Statutory Charge",
                        "body": "Income-tax is charged under Section 4 on the Total Income of the previous year accruing or arising to the assessee.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "scales",
                        "highlights": ["Section 4", "Total Income"]
                    },
                    {
                        "id": "q1_p1_2",
                        "title": "Overriding Legal Title Exception",
                        "body": "Income diverted before reaching the assessee's hands by virtue of an overriding title never forms part of taxable income.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["overriding title", "never forms part"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Gross Inflow", "sub": "Section 4 Scope", "icon": "scales"},
                    {"label": "Title Scrutiny", "sub": "Prior Obligation", "icon": "shield"},
                    {"label": "Taxability Cut", "sub": "Exclude Diversions", "icon": "check"}
                ])
            },
            {
                "branch_id": "b2_distinction",
                "branch_title": "Diversion vs Application Distinction",
                "badge": "§ Statutory Test",
                "icon": "scales",
                "t0": audit["q1"]["slides"][1]["t0"],
                "t1": audit["q1"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q1_p2_1",
                        "title": "Diversion by Anterior Obligation",
                        "body": "In diversion, income is intercepted by an anterior legal obligation before reaching the assessee at source.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["anterior legal obligation", "source"]
                    },
                    {
                        "id": "q1_p2_2",
                        "title": "Diversion Non-Taxability",
                        "body": "Because income is diverted at source, it is not taxable in the hands of the assessee.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["not taxable"]
                    },
                    {
                        "id": "q1_p2_3",
                        "title": "Application of Income Concept",
                        "body": "In application, income first reaches and accrues to the assessee, and is subsequently spent or allocated.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[2]["t0"],
                        "t1": s2_beats[2]["t1"],
                        "voice_sync_text": s2_beats[2]["text"],
                        "icon": "user",
                        "highlights": ["accrues to assessee", "subsequently spent"]
                    },
                    {
                        "id": "q1_p2_4",
                        "title": "Application 100% Taxable",
                        "body": "Application of income is fully taxable in the hands of the assessee under Section 28.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[3]["t0"],
                        "t1": s2_beats[3]["t1"],
                        "voice_sync_text": s2_beats[3]["text"],
                        "icon": "percent",
                        "highlights": ["fully taxable", "Section 28"]
                    },
                    {
                        "id": "q1_p2_ref",
                        "title": "Comparative Statutory Matrix",
                        "body": "Direct comparison between diversion by overriding title and application of income.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "scales",
                        "table_data": {
                            "headers": ["Feature", "Diversion by Overriding Title", "Application of Income"],
                            "rows": [
                                ["Timing of charge", "Before income reaches assessee", "After income reaches assessee"],
                                ["Nature of obligation", "Pre-existing anterior legal obligation", "Voluntary / post-receipt obligation"],
                                ["Title to income", "Assessee never acquires title", "Assessee acquires beneficial title"],
                                ["Tax treatment", "Excluded from total income", "100% taxable under Section 28"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Income Origin", "sub": "Source Stream", "icon": "scales"},
                    {"label": "Anterior Charge", "sub": "Diverts at Source", "icon": "shield"},
                    {"label": "Post Receipt", "sub": "Application Taxable", "icon": "percent"}
                ])
            },
            {
                "branch_id": "b3_judicial",
                "branch_title": "Landmark Judicial Benchmarks",
                "badge": "§ Supreme Court",
                "icon": "cap",
                "t0": audit["q1"]["slides"][2]["t0"],
                "t1": audit["q1"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q1_p3_1",
                        "title": "Sitaldas Tirathdas Judicial Test",
                        "body": "The Supreme Court in CIT v. Sitaldas Tirathdas formulated the definitive test: Does an overriding title divert the income before it reaches the assessee?",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "cap",
                        "highlights": ["CIT v. Sitaldas Tirathdas", "overriding title"]
                    },
                    {
                        "id": "q1_p3_2",
                        "title": "Diversion Characterization",
                        "body": "If an anterior overriding title diverts the source, it is genuine diversion and excluded from total income.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["genuine diversion", "excluded"]
                    },
                    {
                        "id": "q1_p3_3",
                        "title": "Post-Receipt Obligation Rule",
                        "body": "Any obligation arising after income reaches the assessee is mere application of income.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[2]["t0"],
                        "t1": s3_beats[2]["t1"],
                        "voice_sync_text": s3_beats[2]["text"],
                        "icon": "user",
                        "highlights": ["application of income"]
                    },
                    {
                        "id": "q1_p3_ref",
                        "title": "Thakar Das Bhargava Precedent",
                        "body": "Advocate agreed to plead case in Supreme Court on condition fees be paid to a charitable trust created by him.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "cap",
                        "example_calc": {
                            "title": "Precedent Analysis: CIT v. Thakar Das Bhargava (1960) 40 ITR 301 (SC)",
                            "inputs": "Advocate stipulated client must pay professional fee of ₹ 5,00,000 directly to a charitable trust he created.",
                            "steps": [
                                "Step 1: Check origin of obligation — Trust was created by the advocate himself out of professional earnings.",
                                "Step 2: Check client role — The client imposed no prior binding trust obligation on the advocate.",
                                "Step 3: Characterize title — Income accrued as professional fees under Section 28 before being allocated.",
                                "Step 4: Statutory conclusion — Self-imposed obligation constitutes Application of Income, taxable u/s 28."
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Apply SC Test", "sub": "Sitaldas Tirathdas", "icon": "cap"},
                    {"label": "Examine Trust", "sub": "Advocate Created", "icon": "shield"},
                    {"label": "Tax Under Sec 28", "sub": "Application of Income", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps & Pitfalls",
                "badge": "§ ICAI Exam Focus",
                "icon": "warning",
                "t0": audit["q1"]["slides"][3]["t0"],
                "t1": audit["q1"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q1_p4_1",
                        "title": "Voluntary Allocation Trap",
                        "body": "An assessee's voluntary allocation of income to a third party or trust never constitutes diversion.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["voluntary allocation", "never diversion"]
                    },
                    {
                        "id": "q1_p4_2",
                        "title": "Legal Pre-Requisite for Diversion",
                        "body": "Anterior legal obligation created by statute, court decree, or title deed is mandatory to claim diversion.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["Anterior legal obligation", "court decree"]
                    },
                    {
                        "id": "q1_p4_ref",
                        "title": "Exam Trap: Client Payment to Charity",
                        "body": "Common mistake vs statutory rule regarding direct client remittance to charity.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Treating direct payment by client to charity as diversion merely because money bypassed assessee's bank account.",
                            "statutory_rule": "Payment per assessee's direction remains application under Section 28 unless the client created the overriding legal obligation binding the receipt prior to contract."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Spot Voluntary Direction", "sub": "Assessee Choice", "icon": "warning"},
                    {"label": "Verify Anterior Charge", "sub": "Court Decree / Deed", "icon": "shield"},
                    {"label": "Full Chargeability", "sub": "Include in Sec 28", "icon": "check"}
                ])
            }
        ]
    }

def build_q2():
    # Identical audio and beats to q1, but with Jit & Pal X-Rays reference card
    mm = build_q1()
    mm["question_id"] = "q2"
    mm["question_title"] = "Overriding Charge in Purchase Deed: Diversion vs Application (Jit & Pal X-Rays)"
    # Replace branch 3 reference card with Jit & Pal X-Rays
    mm["branches"][2]["points"][3] = {
        "id": "q2_p3_ref",
        "title": "Jit & Pal X-Rays Landmark Precedent",
        "body": "Allahabad High Court ruling on overriding charge incorporated directly into a commercial sale deed.",
        "spoken": False,
        "reference": True,
        "t0": None,
        "t1": None,
        "voice_sync_text": None,
        "icon": "cap",
        "example_calc": {
            "title": "Precedent Analysis: Jit & Pal X-Rays (P.) Ltd. v. CIT (2004) 267 ITR 370 (All)",
            "inputs": "XYZ Ltd. purchased running concern via sale deed stipulating ₹ 15,000 p.a. overriding charge on net profits to vendor's wife.",
            "steps": [
                "Step 1: Inspect sale deed — Overriding charge of ₹ 15,000 p.a. was an integral condition of purchase of the going concern.",
                "Step 2: Trace attachment — The obligation attached to the very source of income (the business concern) at transfer.",
                "Step 3: Characterize title — Assessee never had unencumbered ownership of the profit stream.",
                "Step 4: Statutory conclusion — Valid Diversion of Income by overriding title; ₹ 15,000 excluded from company's taxable income."
            ]
        }
    }
    return mm

def build_q3():
    # Identical audio and beats to q1, but with Nariman B. Bharucha reference card
    mm = build_q1()
    mm["question_id"] = "q3"
    mm["question_title"] = "Partnership Deed Charge to Widow: Diversion vs Application (Nariman B. Bharucha)"
    # Replace branch 3 reference card with Nariman B. Bharucha
    mm["branches"][2]["points"][3] = {
        "id": "q3_p3_ref",
        "title": "Nariman B. Bharucha Landmark Precedent",
        "body": "Bombay High Court ruling on partnership deed provision diverting profits to deceased partner's widow.",
        "spoken": False,
        "reference": True,
        "t0": None,
        "t1": None,
        "voice_sync_text": None,
        "icon": "cap",
        "example_calc": {
            "title": "Precedent Analysis: CIT v. Nariman B. Bharucha & Sons (1981) 130 ITR 863 (Bom)",
            "inputs": "Partnership deed provided that upon father's demise, firm must pay 20% of net profits (₹ 1,00,000) to mother.",
            "steps": [
                "Step 1: Inspect partnership deed — Clause creates a pre-existing overriding charge in favor of the mother.",
                "Step 2: Trace title — 20% profits diverted at source before reaching firm as taxable income.",
                "Step 3: Evaluate possession — Firm received amount merely for and on behalf of mother who held paramount title.",
                "Step 4: Statutory conclusion — Valid Diversion by overriding title; ₹ 1,00,000 excluded from partnership firm income."
            ]
        }
    }
    return mm

def build_q4():
    # Audio length: 91.06s
    s1_beats = audit["q4"]["slides"][0]["beats"]
    s2_beats = audit["q4"]["slides"][1]["beats"]
    s3_beats = audit["q4"]["slides"][2]["beats"]
    s4_beats = audit["q4"]["slides"][3]["beats"]
    
    return {
        "question_id": "q4",
        "question_title": "Optional Old Tax Regime: Slab Rates, Age Exemption Limits & Cess",
        "audio_file": "data/audio/q4.mp3",
        "total_duration": audit["q4"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_framework",
                "branch_title": "Optional Old Tax Regime Framework",
                "badge": "§ 115BAC(1A) Opt-Out",
                "icon": "building",
                "t0": audit["q4"]["slides"][0]["t0"],
                "t1": audit["q4"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q4_p1_1",
                        "title": "Opting Out to Normal Rates",
                        "body": "Assessees opting out of default regime under Section 115BAC(1A) are taxed under progressive normal slab rates.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["Section 115BAC(1A)", "normal slab rates"]
                    },
                    {
                        "id": "q4_p1_2",
                        "title": "Age-Based Progressive Slabs",
                        "body": "The old regime provides progressive slab rates and higher basic exemption thresholds based on age classifications.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "scales",
                        "highlights": ["progressive slab rates", "age classifications"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Opt-Out Election", "sub": "Sec 115BAC(1A)", "icon": "building"},
                    {"label": "Age Verification", "sub": "Determine Category", "icon": "user"},
                    {"label": "Select Slabs", "sub": "Apply Normal Rates", "icon": "scales"}
                ])
            },
            {
                "branch_id": "b2_slabs",
                "branch_title": "Basic Exemption Slabs by Age Bracket",
                "badge": "§ Finance Act Rates",
                "icon": "calculator",
                "t0": audit["q4"]["slides"][1]["t0"],
                "t1": audit["q4"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q4_p2_1",
                        "title": "Three Age Classifications",
                        "body": "The statutory old regime establishes three distinct age tiers for basic tax exemption.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "user",
                        "highlights": ["three distinct age tiers"]
                    },
                    {
                        "id": "q4_p2_2",
                        "title": "Under 60 Exemption Limit",
                        "body": "Individuals below 60 years get basic exemption of ₹ 2,50,000.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "user",
                        "highlights": ["₹ 2,50,000", "below 60 years"]
                    },
                    {
                        "id": "q4_p2_3",
                        "title": "Senior & Super Senior Limits",
                        "body": "Resident Senior Citizens (60 to <80) receive ₹ 3,00,000 and Super Senior Citizens (80+) receive ₹ 5,00,000 basic exemption.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[2]["t0"],
                        "t1": s2_beats[2]["t1"],
                        "voice_sync_text": s2_beats[2]["text"],
                        "icon": "shield",
                        "highlights": ["₹ 3,00,000", "₹ 5,00,000", "Resident"]
                    },
                    {
                        "id": "q4_p2_4",
                        "title": "Progressive Rate Brackets",
                        "body": "Income exceeding the basic exemption limit is taxed progressively at 5%, 20%, and 30%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[3]["t0"],
                        "t1": s2_beats[3]["t1"],
                        "voice_sync_text": s2_beats[3]["text"],
                        "icon": "percent",
                        "highlights": ["5%", "20%", "30%"]
                    },
                    {
                        "id": "q4_p2_ref",
                        "title": "Complete Old Regime Slabs Table",
                        "body": "Full statutory brackets and progressive tax rates for all three taxpayer categories.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "table_data": {
                            "headers": ["Income Bracket", "<60 Years / NR", "Resident 60 to <80", "Resident 80+"],
                            "rows": [
                                ["Up to ₹ 2,50,000", "Nil", "Nil", "Nil"],
                                ["₹ 2,50,001 - ₹ 3,00,000", "5%", "Nil", "Nil"],
                                ["₹ 3,00,001 - ₹ 5,00,000", "5%", "5%", "Nil"],
                                ["₹ 5,00,001 - ₹ 10,00,000", "20%", "20%", "20%"],
                                ["Above ₹ 10,00,000", "30%", "30%", "30%"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Identify Category", "sub": "Age & Status", "icon": "user"},
                    {"label": "Deduct Exemption", "sub": "₹ 2.5L / ₹ 3L / ₹ 5L", "icon": "calculator"},
                    {"label": "Apply Rates", "sub": "5%, 20%, 30%", "icon": "percent"}
                ])
            },
            {
                "branch_id": "b3_cess_calc",
                "branch_title": "Tax Computation, Surcharge & 4% Cess",
                "badge": "§ 4% Health & Education Cess",
                "icon": "percent",
                "t0": audit["q4"]["slides"][2]["t0"],
                "t1": audit["q4"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q4_p3_1",
                        "title": "Statutory 4% Cess Addition",
                        "body": "Health and Education Cess is mandatory at 4% on aggregate income-tax and applicable surcharge.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "percent",
                        "highlights": ["Health and Education Cess", "4%"]
                    },
                    {
                        "id": "q4_p3_2",
                        "title": "Two-Stage Computation Sequence",
                        "body": "Tax liability must be calculated on slab brackets first, then 4% cess is added to determine final net payable.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["slab brackets first", "4% cess"]
                    },
                    {
                        "id": "q4_p3_ref1",
                        "title": "Worked Example: Mr. Arjun (₹ 16,00,000)",
                        "body": "Statutory tax computation across all three age tiers under optional old regime.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 4: Mr. Arjun Total Income ₹ 16,00,000",
                            "inputs": "Gross Total Income = ₹ 16,00,000. Comparative tax at Age 52, Age 64, and Age 83.",
                            "steps": [
                                "Age 52: Tax on ₹ 16L = ₹ 12,500 (5%) + ₹ 1,00,000 (20%) + ₹ 1,80,000 (30%) = ₹ 2,92,500. Add 4% Cess (₹ 11,700) = ₹ 3,04,200.",
                                "Age 64: Tax on ₹ 16L = ₹ 10,000 (5%) + ₹ 1,00,000 (20%) + ₹ 1,80,000 (30%) = ₹ 2,90,000. Add 4% Cess (₹ 11,600) = ₹ 3,01,600.",
                                "Age 83: Tax on ₹ 16L = Nil (up to ₹ 5L) + ₹ 1,00,000 (20%) + ₹ 1,80,000 (30%) = ₹ 2,80,000. Add 4% Cess (₹ 11,200) = ₹ 2,91,200."
                            ]
                        }
                    },
                    {
                        "id": "q4_p3_ref2",
                        "title": "Individual Surcharge Rates (Old Regime)",
                        "body": "Progressive surcharge rates applicable on income-tax for high-income individuals under old regime.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "percent",
                        "table_data": {
                            "headers": ["Total Income Bracket", "Surcharge Rate", "Marginal Relief Status"],
                            "rows": [
                                ["₹ 50 Lakhs to ₹ 1 Crore", "10%", "Available at ₹ 50 Lakhs"],
                                ["₹ 1 Crore to ₹ 2 Crores", "15%", "Available at ₹ 1 Crore"],
                                ["₹ 2 Crores to ₹ 5 Crores", "25%", "Available at ₹ 2 Crores"],
                                ["Exceeding ₹ 5 Crores", "37%", "Available at ₹ 5 Crores"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Compute Slab Tax", "sub": "₹ 2.925L / 2.9L / 2.8L", "icon": "calculator"},
                    {"label": "Add 4% Cess", "sub": "Health & Education", "icon": "percent"},
                    {"label": "Net Tax Payable", "sub": "₹ 3,04,200 / 3,01,600", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Exam Traps: Non-Resident & Age Rules",
                "badge": "§ CBDT Circular 28/2016",
                "icon": "warning",
                "t0": audit["q4"]["slides"][3]["t0"],
                "t1": audit["q4"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q4_p4_1",
                        "title": "Non-Resident Age Restriction",
                        "body": "Non-residents cannot claim higher senior or super senior exemption limits regardless of their age.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["Non-residents cannot claim", "regardless of age"]
                    },
                    {
                        "id": "q4_p4_2",
                        "title": "Residency Exclusivity Condition",
                        "body": "The higher basic exemptions of ₹ 3,00,000 and ₹ 5,00,000 are strictly confined to Resident Individuals.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["₹ 3,00,000", "₹ 5,00,000", "Resident Individuals"]
                    },
                    {
                        "id": "q4_p4_ref",
                        "title": "1st April Age Attainment Rule",
                        "body": "Statutory clarification regarding taxpayers attaining age 60 or 80 on 1st April.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "check",
                        "trap_data": {
                            "mistake": "Classifying an individual born on 1st April as not having attained age 60 during the previous year ending 31st March.",
                            "statutory_rule": "CBDT Circular No. 28/2016: An individual born on 1st April attains that age on the preceding day (31st March), and is entitled to the higher exemption limit for that Assessment Year."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Check Residency", "sub": "Resident vs NR", "icon": "shield"},
                    {"label": "1st April Rule", "sub": "CBDT Circular 28/2016", "icon": "check"},
                    {"label": "Final Exemption", "sub": "₹ 2.5L / ₹ 3L / ₹ 5L", "icon": "calculator"}
                ])
            }
        ]
    }

def build_q5():
    # Audio length: 83.35s
    s1_beats = audit["q5"]["slides"][0]["beats"]
    s2_beats = audit["q5"]["slides"][1]["beats"]
    s3_beats = audit["q5"]["slides"][2]["beats"]
    s4_beats = audit["q5"]["slides"][3]["beats"]
    
    return {
        "question_id": "q5",
        "question_title": "Section 87A Rebate in Optional Old Regime: ₹ 5 Lakhs Threshold & Limits",
        "audio_file": "data/audio/q5.mp3",
        "total_duration": audit["q5"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_core",
                "branch_title": "Section 87A Statutory Framework (Old Regime)",
                "badge": "§ 87A Old Regime",
                "icon": "shield",
                "t0": audit["q5"]["slides"][0]["t0"],
                "t1": audit["q5"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q5_p1_1",
                        "title": "Low & Middle Income Tax Relief",
                        "body": "Section 87A provides tax rebate to alleviate tax burden for low and middle income resident individuals.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["Section 87A", "resident individuals"]
                    },
                    {
                        "id": "q5_p1_2",
                        "title": "Old Regime Income Ceiling",
                        "body": "Under the optional old tax regime, the rebate applies only when Total Income does not exceed ₹ 5,00,000.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "scales",
                        "highlights": ["₹ 5,00,000", "Total Income"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Verify Regime", "sub": "Old Optional", "icon": "building"},
                    {"label": "Income Test", "sub": "TI ≤ ₹ 5,00,000", "icon": "scales"},
                    {"label": "Rebate Eligibility", "sub": "Section 87A", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b2_limits",
                "branch_title": "Rebate Computation & Maximum Cap",
                "badge": "§ Max ₹ 12,500",
                "icon": "calculator",
                "t0": audit["q5"]["slides"][1]["t0"],
                "t1": audit["q5"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q5_p2_1",
                        "title": "Statutory Cap of ₹ 12,500",
                        "body": "Under the old regime, maximum Section 87A rebate is 100% of tax payable or ₹ 12,500, whichever is lower.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "calculator",
                        "highlights": ["₹ 12,500", "whichever is lower"]
                    },
                    {
                        "id": "q5_p2_2",
                        "title": "Zero Tax up to ₹ 5 Lakhs",
                        "body": "Because tax on ₹ 5,00,000 is exactly ₹ 12,500, eligible assessees pay zero tax.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["zero tax", "₹ 12,500"]
                    },
                    {
                        "id": "q5_p2_3",
                        "title": "Cess Calculated After Rebate",
                        "body": "Health and Education Cess at 4% is calculated only on net tax remaining after rebate.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[2]["t0"],
                        "t1": s2_beats[2]["t1"],
                        "voice_sync_text": s2_beats[2]["text"],
                        "icon": "percent",
                        "highlights": ["4%", "after rebate"]
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Calculate Slab Tax", "sub": "5% on > ₹ 2.5L", "icon": "calculator"},
                    {"label": "Deduct Rebate", "sub": "Lower of Tax or ₹ 12.5k", "icon": "shield"},
                    {"label": "Net Tax Result", "sub": "Nil Tax Payable", "icon": "check"}
                ])
            },
            {
                "branch_id": "b3_worked_example",
                "branch_title": "Practical Statutory Assessment",
                "badge": "§ Question 5 Solution",
                "icon": "calculator",
                "t0": audit["q5"]["slides"][2]["t0"],
                "t1": audit["q5"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q5_p3_1",
                        "title": "Step-by-Step Calculation",
                        "body": "In the exam problem, compute tax on income exceeding basic exemption and apply full rebate.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "calculator",
                        "highlights": ["basic exemption", "full rebate"]
                    },
                    {
                        "id": "q5_p3_2",
                        "title": "Zero Net Liability Rule",
                        "body": "Subtracting rebate equals zero tax liability, so no 4% cess is charged.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["zero tax liability", "no 4% cess"]
                    },
                    {
                        "id": "q5_p3_ref",
                        "title": "Worked Example: Mr. Manish (₹ 4,15,000)",
                        "body": "Assessment of tax liability under optional old regime for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 5: Mr. Manish (Age 47, Resident) Total Income ₹ 4,15,000",
                            "inputs": "Gross Total Income = ₹ 4,15,000. Assessee exercises option to opt out of default regime.",
                            "steps": [
                                "Step 1: Compute taxable income exceeding basic exemption = ₹ 4,15,000 - ₹ 2,50,000 = ₹ 1,65,000.",
                                "Step 2: Tax @ 5% on ₹ 1,65,000 = ₹ 8,250.",
                                "Step 3: Less: Rebate u/s 87A = Lower of ₹ 8,250 or ₹ 12,500 = ₹ 8,250.",
                                "Step 4: Net Tax before cess = ₹ 8,250 - ₹ 8,250 = Nil.",
                                "Step 5: Health & Education Cess @ 4% on Nil = Nil. Final Tax Liability = Nil."
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Taxable ₹ 1.65L", "sub": "Above ₹ 2.5L Exemption", "icon": "calculator"},
                    {"label": "Tax @ 5%", "sub": "₹ 8,250", "icon": "percent"},
                    {"label": "Rebate u/s 87A", "sub": "Less ₹ 8,250 = Nil", "icon": "check"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps: Threshold & Entity Exclusions",
                "badge": "§ Statutory Traps",
                "icon": "warning",
                "t0": audit["q5"]["slides"][3]["t0"],
                "t1": audit["q5"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q5_p4_1",
                        "title": "Non-Resident Disqualification",
                        "body": "Non-resident individuals are strictly barred from Section 87A rebate, even if total income is below ₹ 5 Lakhs.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["Non-resident", "strictly barred", "below ₹ 5 Lakhs"]
                    },
                    {
                        "id": "q5_p4_2",
                        "title": "Entity Exclusions & Cliff Edge",
                        "body": "Section 87A is restricted solely to Resident Individuals; HUFs, firms, and companies are completely ineligible.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["Resident Individuals", "HUFs, firms, and companies"]
                    },
                    {
                        "id": "q5_p4_ref",
                        "title": "Exam Trap: Cliff Edge & No Marginal Relief",
                        "body": "Disqualification risks and total loss of rebate exceeding ₹ 5,00,000 in old regime.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Claiming marginal relief under old regime when income slightly exceeds ₹ 5,00,000.",
                            "statutory_rule": "Under old regime, Section 87A has NO marginal relief: if Total Income is ₹ 5,00,010, the assessee loses the entire ₹ 12,500 rebate and pays ₹ 12,502 tax plus cess."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Resident Individual Only", "sub": "HUF / AOP / Firm Out", "icon": "user"},
                    {"label": "Check ₹ 5L Ceiling", "sub": "₹ 5,00,010 Loses All", "icon": "warning"},
                    {"label": "Rebate Clamped", "sub": "Max ₹ 12,500", "icon": "check"}
                ])
            }
        ]
    }

def build_q6():
    # Audio length: 89.57s
    s1_beats = audit["q6"]["slides"][0]["beats"]
    s2_beats = audit["q6"]["slides"][1]["beats"]
    s3_beats = audit["q6"]["slides"][2]["beats"]
    s4_beats = audit["q6"]["slides"][3]["beats"]
    
    return {
        "question_id": "q6",
        "question_title": "Default Tax Regime u/s 115BAC: Slabs, Rebate & Surcharge (A.Y. 2026-27)",
        "audio_file": "data/audio/q6.mp3",
        "total_duration": audit["q6"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_framework",
                "branch_title": "Section 115BAC Default Tax Regime Framework",
                "badge": "§ 115BAC(1A)",
                "icon": "building",
                "t0": audit["q6"]["slides"][0]["t0"],
                "t1": audit["q6"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q6_p1_1",
                        "title": "Default Tax Regime Status",
                        "body": "Section 115BAC(1A) is the default tax regime for Individuals, HUFs, AOPs, BOIs, and AJPs for A.Y. 2026-27.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["Section 115BAC(1A)", "default tax regime", "A.Y. 2026-27"]
                    },
                    {
                        "id": "q6_p1_2",
                        "title": "Concessional Slabs & Deductions",
                        "body": "Offers lower tax rates across streamlined income slabs in exchange for foregoing specified exemptions and deductions.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "scales",
                        "highlights": ["lower tax rates", "foregoing specified exemptions"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Default Status", "sub": "Sec 115BAC(1A)", "icon": "building"},
                    {"label": "Concession Tradeoff", "sub": "No Chap VI-A", "icon": "scales"},
                    {"label": "Apply New Slabs", "sub": "A.Y. 2026-27", "icon": "calculator"}
                ])
            },
            {
                "branch_id": "b2_slabs",
                "branch_title": "Progressive Tax Slabs (A.Y. 2026-27)",
                "badge": "§ ₹ 4 Lakhs Exemption",
                "icon": "calculator",
                "t0": audit["q6"]["slides"][1]["t0"],
                "t1": audit["q6"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q6_p2_1",
                        "title": "Basic Exemption of ₹ 4 Lakhs",
                        "body": "In the default regime, initial income up to ₹ 4,00,000 has Nil tax liability.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "calculator",
                        "highlights": ["₹ 4,00,000", "Nil tax"]
                    },
                    {
                        "id": "q6_p2_2",
                        "title": "Progressive Slab Structure",
                        "body": "Income from 4L to 8L is taxed @ 5%, 8L to 12L @ 10%, 12L to 16L @ 15%, 16L to 20L @ 20%, 20L to 24L @ 25%, and above 24L @ 30%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "percent",
                        "highlights": ["5%", "10%", "15%", "20%", "25%", "30%"]
                    },
                    {
                        "id": "q6_p2_ref",
                        "title": "Complete Section 115BAC Slabs Table",
                        "body": "Full statutory income brackets and tax rates under default regime for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "table_data": {
                            "headers": ["Income Bracket", "Tax Rate", "Cumulative Tax at Top of Bracket"],
                            "rows": [
                                ["Up to ₹ 4,00,000", "Nil", "₹ 0"],
                                ["₹ 4,00,001 - ₹ 8,00,000", "5%", "₹ 20,000"],
                                ["₹ 8,00,001 - ₹ 12,00,000", "10%", "₹ 60,000"],
                                ["₹ 12,00,001 - ₹ 16,00,000", "15%", "₹ 1,20,000"],
                                ["₹ 16,00,001 - ₹ 20,00,000", "20%", "₹ 2,00,000"],
                                ["₹ 20,00,001 - ₹ 24,00,000", "25%", "₹ 3,00,000"],
                                ["Above ₹ 24,00,000", "30%", "30% on excess"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "First ₹ 4L", "sub": "Nil Tax", "icon": "calculator"},
                    {"label": "Next Brackets", "sub": "5% / 10% / 15%", "icon": "percent"},
                    {"label": "Max Slab 30%", "sub": "Above ₹ 24L", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b3_rebate_surcharge",
                "branch_title": "Section 87A Rebate & Surcharge Caps",
                "badge": "§ Rebate up to ₹ 12L",
                "icon": "shield",
                "t0": audit["q6"]["slides"][2]["t0"],
                "t1": audit["q6"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q6_p3_1",
                        "title": "Expanded Section 87A Rebate",
                        "body": "In the default regime, Section 87A rebate provides full relief up to ₹ 60,000 for resident individuals with income up to ₹ 12,00,000.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["Section 87A", "₹ 60,000", "₹ 12,00,000"]
                    },
                    {
                        "id": "q6_p3_2",
                        "title": "Capped Surcharge Rate (25%)",
                        "body": "Maximum surcharge under Section 115BAC is capped at 25% (the 37% highest rate under old regime does not apply).",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "percent",
                        "highlights": ["25%", "37%"]
                    },
                    {
                        "id": "q6_p3_ref",
                        "title": "Worked Example: Mr. X (₹ 16,00,000)",
                        "body": "Assessment of tax liability under Section 115BAC for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 6: Mr. X Total Income ₹ 16,00,000 (A.Y. 2026-27)",
                            "inputs": "Gross Total Income = ₹ 16,00,000. Assessee assessed under default tax regime u/s 115BAC.",
                            "steps": [
                                "First ₹ 4,00,000: Nil",
                                "Next ₹ 4,00,001 - ₹ 8,00,000 @ 5%: ₹ 20,000",
                                "Next ₹ 8,00,001 - ₹ 12,00,000 @ 10%: ₹ 40,000",
                                "Next ₹ 12,00,001 - ₹ 16,00,000 @ 15%: ₹ 60,000",
                                "Total Tax before cess = ₹ 20,000 + ₹ 40,000 + ₹ 60,000 = ₹ 1,20,000",
                                "Add: Health and Education Cess @ 4% = ₹ 4,800",
                                "Final Tax Liability = ₹ 1,24,800"
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Rebate Ceiling", "sub": "TI ≤ ₹ 12L (₹ 60k)", "icon": "shield"},
                    {"label": "Surcharge Cap", "sub": "Max 25% (No 37%)", "icon": "percent"},
                    {"label": "Add 4% Cess", "sub": "Final Net Liability", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps: Foregone Deductions & Universal Slabs",
                "badge": "§ Deduction Restrictions",
                "icon": "warning",
                "t0": audit["q6"]["slides"][3]["t0"],
                "t1": audit["q6"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q6_p4_1",
                        "title": "Loss of Chapter VI-A Deductions",
                        "body": "In Section 115BAC, major deductions like 80C, 80D, and self-occupied housing interest u/s 24(b) are completely disallowed.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["Section 115BAC", "80C, 80D", "24(b) disallowed"]
                    },
                    {
                        "id": "q6_p4_2",
                        "title": "Universal Exemption Limit",
                        "body": "Basic exemption of ₹ 4 Lakhs applies uniformly to all individuals regardless of senior citizen status.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["₹ 4 Lakhs", "uniformly to all"]
                    },
                    {
                        "id": "q6_p4_ref",
                        "title": "Exam Trap: Foregone Deductions",
                        "body": "Common mistake vs statutory rule regarding Chapter VI-A under default regime.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Claiming Section 80C, 80D, or Section 24(b) self-occupied interest under default regime Section 115BAC.",
                            "statutory_rule": "Section 115BAC(2) disallows all Chapter VI-A deductions (except 80CCD(2), 80CCH(2), 80JJAA) and Section 24(b) self-occupied loss."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Deductions Disallowed", "sub": "No 80C, 80D, 24(b)", "icon": "warning"},
                    {"label": "Universal Slabs", "sub": "No Age Bias", "icon": "shield"},
                    {"label": "Compare Tax Regimes", "sub": "Pick Lowest Tax", "icon": "check"}
                ])
            }
        ]
    }

def build_q7():
    # Audio length: 76.90s
    s1_beats = audit["q7"]["slides"][0]["beats"]
    s2_beats = audit["q7"]["slides"][1]["beats"]
    s3_beats = audit["q7"]["slides"][2]["beats"]
    s4_beats = audit["q7"]["slides"][3]["beats"]
    
    return {
        "question_id": "q7",
        "question_title": "Section 87A Rebate under Default Regime: ₹ 12 Lakhs Threshold (A.Y. 2026-27)",
        "audio_file": "data/audio/q7.mp3",
        "total_duration": audit["q7"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_framework",
                "branch_title": "Default Regime Section 87A Rebate Framework",
                "badge": "§ 87A Default Regime",
                "icon": "shield",
                "t0": audit["q7"]["slides"][0]["t0"],
                "t1": audit["q7"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q7_p1_1",
                        "title": "Middle-Class Tax Relief Scope",
                        "body": "Section 87A rebate provides substantial relief to middle-income earners under the default tax regime.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["Section 87A", "default tax regime"]
                    },
                    {
                        "id": "q7_p1_2",
                        "title": "Zero Tax up to ₹ 12 Lakhs",
                        "body": "If annual income falls within statutory threshold, the tax payable is reduced to zero.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["reduced to zero"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Verify Regime", "sub": "Section 115BAC", "icon": "building"},
                    {"label": "Income Test", "sub": "TI ≤ ₹ 12,00,000", "icon": "scales"},
                    {"label": "Zero Tax Result", "sub": "Rebate Applicable", "icon": "check"}
                ])
            },
            {
                "branch_id": "b2_slabs",
                "branch_title": "Tax Rates & Slabs up to ₹ 12 Lakhs (A.Y. 2026-27)",
                "badge": "§ Slabs up to ₹ 12L",
                "icon": "calculator",
                "t0": audit["q7"]["slides"][1]["t0"],
                "t1": audit["q7"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q7_p2_1",
                        "title": "A.Y. 2026-27 Slabs",
                        "body": "Examine the tax slabs applicable for Assessment Year 2026-27.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "calculator",
                        "highlights": ["Assessment Year 2026-27"]
                    },
                    {
                        "id": "q7_p2_2",
                        "title": "First ₹ 4 Lakhs Exemption",
                        "body": "First ₹ 4,00,000 of total income is taxed at 0%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["₹ 4,00,000", "0%"]
                    },
                    {
                        "id": "q7_p2_3",
                        "title": "Tax on 4L-8L and 8L-12L",
                        "body": "Income from 4 to 8 Lakhs is taxed at 5% and 8 to 12 Lakhs at 10%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[2]["t0"],
                        "t1": s2_beats[2]["t1"],
                        "voice_sync_text": s2_beats[2]["text"],
                        "icon": "percent",
                        "highlights": ["4 to 8 Lakhs", "5%", "8 to 12 Lakhs", "10%"]
                    },
                    {
                        "id": "q7_p2_ref",
                        "title": "Rebate Computation Matrix (up to ₹ 12L)",
                        "body": "Progressive tax accumulation and maximum rebate matching under Section 87A.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "table_data": {
                            "headers": ["Income Bracket", "Tax Rate", "Tax Amount", "Cumulative Tax"],
                            "rows": [
                                ["Up to ₹ 4,00,000", "Nil", "₹ 0", "₹ 0"],
                                ["₹ 4,00,001 - ₹ 8,00,000", "5%", "₹ 20,000", "₹ 20,000"],
                                ["₹ 8,00,001 - ₹ 12,00,000", "10%", "₹ 40,000", "₹ 60,000"],
                                ["Total Tax on ₹ 12,00,000", "-", "-", "₹ 60,000"],
                                ["Less: Rebate u/s 87A", "-", "-", "(-) ₹ 60,000"],
                                ["Net Tax Liability", "-", "-", "Nil"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "0 - 4 Lakhs", "sub": "0% Tax (Nil)", "icon": "calculator"},
                    {"label": "4 - 8 Lakhs", "sub": "5% Tax (₹ 20,000)", "icon": "percent"},
                    {"label": "8 - 12 Lakhs", "sub": "10% Tax (₹ 40,000)", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b3_limits",
                "branch_title": "₹ 60,000 Maximum Rebate & Cess Rule",
                "badge": "§ Max ₹ 60,000",
                "icon": "calculator",
                "t0": audit["q7"]["slides"][2]["t0"],
                "t1": audit["q7"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q7_p3_1",
                        "title": "Resident Individual ₹ 12L Limit",
                        "body": "Resident Individuals with Total Income up to ₹ 12,00,000 are eligible for rebate up to ₹ 60,000.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["Total Income", "₹ 12,00,000", "₹ 60,000"]
                    },
                    {
                        "id": "q7_p3_2",
                        "title": "Zero Tax Liability Result",
                        "body": "Consequently, net tax liability on Total Income up to ₹ 12,00,000 becomes NIL.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "check",
                        "highlights": ["NIL"]
                    },
                    {
                        "id": "q7_p3_3",
                        "title": "4% Cess Chargeability Rule",
                        "body": "4% Health & Education Cess applies only if there is a positive tax liability after rebate.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[2]["t0"],
                        "t1": s3_beats[2]["t1"],
                        "voice_sync_text": s3_beats[2]["text"],
                        "icon": "percent",
                        "highlights": ["4% Cess"]
                    },
                    {
                        "id": "q7_p3_ref",
                        "title": "Worked Example: Mr. Mahesh (₹ 11,00,000)",
                        "body": "Assessment of tax liability under Section 115BAC for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 7: Mr. Mahesh (Age 32, Resident) Total Income ₹ 11,00,000",
                            "inputs": "Gross Total Income = ₹ 11,00,000 under default tax regime u/s 115BAC.",
                            "steps": [
                                "First ₹ 4,00,000: Nil",
                                "Next ₹ 4,00,001 - ₹ 8,00,000 @ 5%: ₹ 20,000",
                                "Balance ₹ 8,00,001 - ₹ 11,00,000 @ 10% on ₹ 3,00,000: ₹ 30,000",
                                "Total Tax before rebate = ₹ 20,000 + ₹ 30,000 = ₹ 50,000",
                                "Less: Rebate u/s 87A = Lower of ₹ 50,000 or ₹ 60,000 = ₹ 50,000",
                                "Net Tax Liability = Nil (No Cess applicable)"
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Income ≤ ₹ 12L", "sub": "Total Income Check", "icon": "calculator"},
                    {"label": "Max Rebate ₹ 60k", "sub": "Covers Full Slab Tax", "icon": "shield"},
                    {"label": "Net Tax Nil", "sub": "Zero Cess Payable", "icon": "check"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Exam Traps: Standard Deduction & Age Neutrality",
                "badge": "§ 16(ia) & Age Neutrality",
                "icon": "warning",
                "t0": audit["q7"]["slides"][3]["t0"],
                "t1": audit["q7"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q7_p4_1",
                        "title": "Section 16(ia) Standard Deduction",
                        "body": "Salaried taxpayers are entitled to ₹ 75,000 standard deduction under Section 16(ia) in default regime.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["₹ 75,000", "Section 16(ia)"]
                    },
                    {
                        "id": "q7_p4_ref",
                        "title": "Age Neutrality in Default Regime",
                        "body": "Statutory rule confirming identical slab thresholds across all ages under Section 115BAC.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "shield",
                        "trap_data": {
                            "mistake": "Applying higher senior citizen basic exemptions (₹ 3L / ₹ 5L) under the default tax regime.",
                            "statutory_rule": "Section 115BAC is completely age-neutral: every individual (normal, senior, super senior) receives the same ₹ 4 Lakh basic exemption and ₹ 12 Lakh rebate threshold."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Gross Salary", "sub": "Salary Income", "icon": "user"},
                    {"label": "Less Sec 16(ia)", "sub": "Standard ₹ 75,000", "icon": "calculator"},
                    {"label": "Apply Sec 87A", "sub": "Age-Neutral Rebate", "icon": "check"}
                ])
            }
        ]
    }

def build_q8():
    # Audio length: 69.00s
    s1_beats = audit["q8"]["slides"][0]["beats"]
    s2_beats = audit["q8"]["slides"][1]["beats"]
    s3_beats = audit["q8"]["slides"][2]["beats"]
    s4_beats = audit["q8"]["slides"][3]["beats"]
    
    return {
        "question_id": "q8",
        "question_title": "Section 87A Proviso Marginal Relief: Income Exceeding ₹ 12 Lakhs",
        "audio_file": "data/audio/q8.mp3",
        "total_duration": audit["q8"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_anomaly",
                "branch_title": "The Anomaly Above ₹ 12 Lakhs Threshold",
                "badge": "§ 87A Proviso",
                "icon": "warning",
                "t0": audit["q8"]["slides"][0]["t0"],
                "t1": audit["q8"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q8_p1_1",
                        "title": "The Cliff-Edge Hardship",
                        "body": "When total income slightly exceeds Section 87A rebate limit, an assessee risks paying more incremental tax than extra income earned.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["Section 87A", "incremental tax"]
                    },
                    {
                        "id": "q8_p1_2",
                        "title": "Marginal Relief Remedy",
                        "body": "To eliminate hardship where additional tax exceeds excess income, Section 87A proviso introduces statutory marginal relief.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["Section 87A proviso", "marginal relief"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Income > ₹ 12L", "sub": "Rebate Boundary Cross", "icon": "warning"},
                    {"label": "Check Tax Spurt", "sub": "Tax > Excess Income?", "icon": "scales"},
                    {"label": "Trigger Relief", "sub": "Sec 87A Proviso", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b2_cliff_edge",
                "branch_title": "Full Rebate Loss vs Proviso Relief",
                "badge": "§ ₹ 12L Default Threshold",
                "icon": "calculator",
                "t0": audit["q8"]["slides"][1]["t0"],
                "t1": audit["q8"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q8_p2_1",
                        "title": "Full Rebate up to ₹ 12 Lakhs",
                        "body": "In the default regime, tax on income up to ₹ 12 Lakhs is completely covered by Section 87A rebate.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "check",
                        "highlights": ["₹ 12 Lakhs", "Section 87A rebate"]
                    },
                    {
                        "id": "q8_p2_2",
                        "title": "Proviso Cap on Incremental Tax",
                        "body": "When income exceeds 12 Lakhs, full rebate ceases, but the proviso ensures tax payable does not exceed income over 12 Lakhs.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["12 Lakhs", "proviso ensures"]
                    },
                    {
                        "id": "q8_p2_ref",
                        "title": "Default Regime Slabs Table (A.Y. 2026-27)",
                        "body": "Applicable progressive rates used for Section 87A marginal relief calculations.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "table_data": {
                            "headers": ["Income Bracket", "Rate", "Tax Amount", "Cumulative Tax"],
                            "rows": [
                                ["Up to ₹ 4,00,000", "Nil", "₹ 0", "₹ 0"],
                                ["₹ 4,00,001 - ₹ 8,00,000", "5%", "₹ 20,000", "₹ 20,000"],
                                ["₹ 8,00,001 - ₹ 12,00,000", "10%", "₹ 40,000", "₹ 60,000"],
                                ["₹ 12,00,001 - ₹ 16,00,000", "15%", "15% on excess", "₹ 60,000 + 15%"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Rebate at ₹ 12L", "sub": "Tax Covered", "icon": "check"},
                    {"label": "Income Crosses", "sub": "Exceeds ₹ 12L", "icon": "calculator"},
                    {"label": "Cap at Excess", "sub": "Tax ≤ (TI - 12L)", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b3_formula",
                "branch_title": "Marginal Relief Statutory Computation Formula",
                "badge": "§ Tax Capped at Excess",
                "icon": "calculator",
                "t0": audit["q8"]["slides"][2]["t0"],
                "t1": audit["q8"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q8_p3_1",
                        "title": "Section 87A Proviso Tax Cap",
                        "body": "Under Section 87A proviso, additional tax payable cannot exceed total income exceeding ₹ 12 Lakhs.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["Section 87A proviso", "₹ 12 Lakhs"]
                    },
                    {
                        "id": "q8_p3_2",
                        "title": "Rebate as Difference Amount",
                        "body": "Difference between slab tax and excess income is granted directly as Section 87A rebate.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["slab tax", "excess income", "rebate"]
                    },
                    {
                        "id": "q8_p3_ref",
                        "title": "Worked Example: Mr. Nitin (₹ 12,50,000)",
                        "body": "Assessment of marginal relief under Section 87A proviso for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 8: Mr. Nitin (Age 35, Resident) Total Income ₹ 12,50,000",
                            "inputs": "Gross Total Income = ₹ 12,50,000 under default tax regime u/s 115BAC.",
                            "steps": [
                                "Step 1: Excess income exceeding ₹ 12,00,000 = ₹ 12,50,000 - ₹ 12,00,000 = ₹ 50,000 (A).",
                                "Step 2: Normal slab tax on ₹ 12,50,000 = ₹ 60,000 (up to 12L) + 15% of ₹ 50,000 (₹ 7,500) = ₹ 67,500 (B).",
                                "Step 3: Since Tax (B) > Excess (A), Rebate u/s 87A proviso = B - A = ₹ 67,500 - ₹ 50,000 = ₹ 17,500.",
                                "Step 4: Tax payable after rebate = ₹ 67,500 - ₹ 17,500 = ₹ 50,000 (exactly equal to excess income).",
                                "Step 5: Add Health & Education Cess @ 4% on ₹ 50,000 = ₹ 2,000.",
                                "Final Tax Liability = ₹ 52,000"
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Excess Income (A)", "sub": "₹ 50,000", "icon": "calculator"},
                    {"label": "Slab Tax (B)", "sub": "₹ 67,500", "icon": "percent"},
                    {"label": "Rebate (B - A)", "sub": "₹ 17,500 Relief", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps: Cess Ordering & Resident Status",
                "badge": "§ Relief Before Cess",
                "icon": "warning",
                "t0": audit["q8"]["slides"][3]["t0"],
                "t1": audit["q8"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q8_p4_1",
                        "title": "Relief Calculated Before Cess",
                        "body": "Marginal relief is deducted before adding 4% Health & Education Cess.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["Marginal Relief", "before adding 4% Cess"]
                    },
                    {
                        "id": "q8_p4_2",
                        "title": "Resident Individual Restriction",
                        "body": "Section 87A marginal relief is exclusively available to Resident Individuals.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["Resident Individuals"]
                    },
                    {
                        "id": "q8_p4_ref",
                        "title": "Exam Trap: Non-Resident & Cess Sequencing",
                        "body": "Common mistake vs statutory rule regarding 87A proviso marginal relief.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Adding 4% cess to slab tax before computing marginal relief or granting proviso relief to non-residents.",
                            "statutory_rule": "Section 87A proviso relief reduces income-tax before cess. Cess @ 4% is added strictly onto net reduced tax. Non-residents get zero relief."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Deduct Relief First", "sub": "Before 4% Cess", "icon": "calculator"},
                    {"label": "Check Residency", "sub": "Resident Only", "icon": "shield"},
                    {"label": "Add 4% Cess", "sub": "On Capped ₹ 50,000", "icon": "check"}
                ])
            }
        ]
    }

def build_q9():
    # Audio length: 74.71s
    s1_beats = audit["q9"]["slides"][0]["beats"]
    s2_beats = audit["q9"]["slides"][1]["beats"]
    s3_beats = audit["q9"]["slides"][2]["beats"]
    s4_beats = audit["q9"]["slides"][3]["beats"]
    
    return {
        "question_id": "q9",
        "question_title": "Domestic Company Marginal Relief: ₹ 1 Crore Threshold (7% Surcharge)",
        "audio_file": "data/audio/q9.mp3",
        "total_duration": audit["q9"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_framework",
                "branch_title": "Domestic Company Tax & Surcharge Framework",
                "badge": "§ Finance Act Rates",
                "icon": "building",
                "t0": audit["q9"]["slides"][0]["t0"],
                "t1": audit["q9"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q9_p1_1",
                        "title": "Surcharge on Exceeding ₹ 1 Crore",
                        "body": "When a domestic company's total income exceeds ₹ 1 Crore, statutory surcharge becomes chargeable.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["domestic company", "₹ 1 Crore", "surcharge"]
                    },
                    {
                        "id": "q9_p1_2",
                        "title": "Turnover-Based Base Tax Rates",
                        "body": "Base income-tax rate depends on the company's previous year turnover (P.Y. 2023-24).",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "scales",
                        "highlights": ["turnover", "P.Y. 2023-24", "base tax rate"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Check P.Y. Turnover", "sub": "P.Y. 2023-24", "icon": "building"},
                    {"label": "Income > ₹ 1 Cr", "sub": "Triggers 7% SC", "icon": "percent"},
                    {"label": "Need Relief Check", "sub": "Prevent Hardship", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b2_rates",
                "branch_title": "Base Rates & Surcharge Tier Structure",
                "badge": "§ Surcharge Tiers",
                "icon": "percent",
                "t0": audit["q9"]["slides"][1]["t0"],
                "t1": audit["q9"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q9_p2_1",
                        "title": "Turnover Threshold & Base Rates",
                        "body": "If turnover in P.Y. 2023-24 is up to ₹ 400 Crores, base tax is 25%; otherwise standard rate is 30%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "percent",
                        "highlights": ["P.Y. 2023-24", "₹ 400 Crores", "25%", "30%"]
                    },
                    {
                        "id": "q9_p2_2",
                        "title": "No Surcharge up to ₹ 1 Crore",
                        "body": "For Total Income up to ₹ 1 Crore, surcharge is Nil.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["₹ 1 Crore", "surcharge is Nil"]
                    },
                    {
                        "id": "q9_p2_3",
                        "title": "7% and 12% Surcharge Tiers",
                        "body": "Surcharge is 7% for income between ₹ 1 Crore and ₹ 10 Crores, and 12% above ₹ 10 Crores.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[2]["t0"],
                        "t1": s2_beats[2]["t1"],
                        "voice_sync_text": s2_beats[2]["text"],
                        "icon": "percent",
                        "highlights": ["7%", "₹ 1 Crore and ₹ 10 Crores", "12%"]
                    },
                    {
                        "id": "q9_p2_ref",
                        "title": "Company Tax & Surcharge Matrix",
                        "body": "Statutory rates for domestic vs foreign companies across income tiers.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "building",
                        "table_data": {
                            "headers": ["Entity Type", "Income Tier", "Surcharge Rate", "Effective Base Rate (30%)"],
                            "rows": [
                                ["Domestic Company", "Up to ₹ 1 Crore", "Nil", "30.0%"],
                                ["Domestic Company", "₹ 1 Crore to ₹ 10 Crores", "7%", "32.1% (30% + 7% SC)"],
                                ["Domestic Company", "Exceeding ₹ 10 Crores", "12%", "33.6% (30% + 12% SC)"],
                                ["Foreign Company", "₹ 1 Crore to ₹ 10 Crores", "2%", "40.8% (40% + 2% SC)"],
                                ["Foreign Company", "Exceeding ₹ 10 Crores", "5%", "42.0% (40% + 5% SC)"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Turnover Criterion", "sub": "≤ ₹ 400Cr: 25% | > 30%", "icon": "building"},
                    {"label": "Income > ₹ 1 Cr", "sub": "7% Surcharge", "icon": "percent"},
                    {"label": "Total Rate", "sub": "32.1% Before Cess", "icon": "rupee"}
                ])
            },
            {
                "branch_id": "b3_ceiling",
                "branch_title": "Marginal Relief Ceiling Formula (₹ 1 Crore)",
                "badge": "§ Ceiling at ₹ 1 Cr",
                "icon": "calculator",
                "t0": audit["q9"]["slides"][2]["t0"],
                "t1": audit["q9"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q9_p3_1",
                        "title": "Relief on Marginal Spurt",
                        "body": "When total income slightly exceeds 1 Crore, marginal relief restricts excess tax over income increase.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "shield",
                        "highlights": ["marginal relief", "excess tax"]
                    },
                    {
                        "id": "q9_p3_2",
                        "title": "Statutory Tax Ceiling Formula",
                        "body": "Tax cannot exceed tax payable on ₹ 1 Crore plus 100% of income exceeding ₹ 1 Crore.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["tax payable on ₹ 1 Crore", "income exceeding ₹ 1 Crore"]
                    },
                    {
                        "id": "q9_p3_ref",
                        "title": "Worked Example: X Ltd. (₹ 1,01,00,000)",
                        "body": "Computation of marginal relief at ₹ 1 Crore threshold for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 9: X Ltd. (Domestic Company) Total Income ₹ 1,01,00,000",
                            "inputs": "Gross Total Income = ₹ 1,01,00,000 (No capital gains). Base rate = 30%. Surcharge = 7%.",
                            "steps": [
                                "Step 1: Normal tax + 7% SC @ 32.1% = ₹ 1,01,00,000 × 32.1% = ₹ 32,42,100.",
                                "Step 2: Ceiling = Tax on ₹ 1 Crore @ 30% (₹ 30,00,000) + Excess income (₹ 1,00,000) = ₹ 31,00,000.",
                                "Step 3: Marginal Relief = Normal Tax (₹ 32,42,100) - Ceiling (₹ 31,00,000) = ₹ 1,42,100.",
                                "Step 4: Tax payable after marginal relief = ₹ 31,00,000.",
                                "Step 5: Add 4% Cess on ₹ 31,00,000 = ₹ 1,24,000. Final Tax Liability = ₹ 32,24,000."
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Tax on ₹ 1 Cr", "sub": "₹ 30,00,000", "icon": "calculator"},
                    {"label": "Add Excess", "sub": "+ ₹ 1,00,000 = ₹ 31L", "icon": "rupee"},
                    {"label": "Marginal Relief", "sub": "₹ 1,42,100 Deducted", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps: Surcharge Stage & Cess Sequence",
                "badge": "§ Sequencing Traps",
                "icon": "warning",
                "t0": audit["q9"]["slides"][3]["t0"],
                "t1": audit["q9"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q9_p4_1",
                        "title": "Relief Applied at Surcharge Stage",
                        "body": "Marginal relief is calculated and applied at the surcharge stage before adding cess.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "warning",
                        "highlights": ["surcharge stage", "before adding cess"]
                    },
                    {
                        "id": "q9_p4_2",
                        "title": "4% Cess Added on Reduced Tax",
                        "body": "4% Health and Education Cess is calculated strictly on the tax amount remaining after deducting marginal relief.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "percent",
                        "highlights": ["4% Cess", "after deducting marginal relief"]
                    },
                    {
                        "id": "q9_p4_ref",
                        "title": "Exam Trap: Turnover Benchmark & Cess Order",
                        "body": "Common mistake vs statutory rule regarding company turnover and relief sequence.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Applying 4% cess before computing company marginal relief, or checking P.Y. 2024-25 instead of P.Y. 2023-24 for turnover.",
                            "statutory_rule": "Base rate 25% applies if turnover in P.Y. 2023-24 ≤ ₹ 400 Cr. Marginal relief is deducted at the surcharge stage. 4% cess is charged on the capped ₹ 31,00,000."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Turnover P.Y. 23-24", "sub": "Benchmark Year", "icon": "building"},
                    {"label": "Deduct Relief", "sub": "At Surcharge Stage", "icon": "shield"},
                    {"label": "Add 4% Cess", "sub": "On Capped Amount", "icon": "check"}
                ])
            }
        ]
    }

def build_q10():
    # Audio length: 61.88s
    s1_beats = audit["q10"]["slides"][0]["beats"]
    s2_beats = audit["q10"]["slides"][1]["beats"]
    s3_beats = audit["q10"]["slides"][2]["beats"]
    s4_beats = audit["q10"]["slides"][3]["beats"]
    
    return {
        "question_id": "q10",
        "question_title": "Domestic Company Marginal Relief: ₹ 10 Crore Threshold (12% Surcharge)",
        "audio_file": "data/audio/q10.mp3",
        "total_duration": audit["q10"]["total_audio_length"],
        "branches": [
            {
                "branch_id": "b1_framework",
                "branch_title": "12% Surcharge Jump at ₹ 10 Crore Threshold",
                "badge": "§ 12% Surcharge Tier",
                "icon": "building",
                "t0": audit["q10"]["slides"][0]["t0"],
                "t1": audit["q10"]["slides"][0]["t1"],
                "points": [
                    {
                        "id": "q10_p1_1",
                        "title": "Surcharge Jump from 7% to 12%",
                        "body": "When a domestic company's total income exceeds ₹ 10 Crores, surcharge jumps from 7% to 12%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[0]["t0"],
                        "t1": s1_beats[0]["t1"],
                        "voice_sync_text": s1_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["₹ 10 Crores", "7% to 12%"]
                    },
                    {
                        "id": "q10_p1_2",
                        "title": "Marginal Relief Protection",
                        "body": "Marginal relief prevents excessive burden caused by this abrupt five-percentage-point surcharge spike.",
                        "spoken": True,
                        "reference": False,
                        "t0": s1_beats[1]["t0"],
                        "t1": s1_beats[1]["t1"],
                        "voice_sync_text": s1_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["Marginal relief", "five-percentage-point surcharge spike"]
                    }
                ],
                "flow_summary": compute_flow_steps(s1_beats[-1]["t0"], s1_beats[-1]["t1"], [
                    {"label": "Income > ₹ 10 Cr", "sub": "7% Jumps to 12%", "icon": "building"},
                    {"label": "Spike in Tax", "sub": "Higher Rate on All TI", "icon": "percent"},
                    {"label": "Trigger Sec Relief", "sub": "Protect Income", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b2_burden",
                "branch_title": "Surcharge Disparity & Tax Burden Analysis",
                "badge": "§ 5% Rate Disparity",
                "icon": "percent",
                "t0": audit["q10"]["slides"][1]["t0"],
                "t1": audit["q10"]["slides"][1]["t1"],
                "points": [
                    {
                        "id": "q10_p2_1",
                        "title": "Abrupt Tax Surge on Entire Income",
                        "body": "Whereas 7% surcharge applied up to 10 Crores, the entire total income suddenly becomes subject to 12% surcharge.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[0]["t0"],
                        "t1": s2_beats[0]["t1"],
                        "voice_sync_text": s2_beats[0]["text"],
                        "icon": "percent",
                        "highlights": ["7% surcharge", "10 Crores", "12% surcharge"]
                    },
                    {
                        "id": "q10_p2_2",
                        "title": "Substantial Corporate Tax Surge",
                        "body": "This surcharge jump significantly multiplies the company's tax burden on marginal income.",
                        "spoken": True,
                        "reference": False,
                        "t0": s2_beats[1]["t0"],
                        "t1": s2_beats[1]["t1"],
                        "voice_sync_text": s2_beats[1]["text"],
                        "icon": "calculator",
                        "highlights": ["significantly multiplies", "marginal income"]
                    },
                    {
                        "id": "q10_p2_ref",
                        "title": "Company Surcharge Comparison Table",
                        "body": "Statutory surcharge tiers across domestic and foreign companies at ₹ 10 Crore mark.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "building",
                        "table_data": {
                            "headers": ["Entity Category", "Up to ₹ 1 Crore", "₹ 1 Cr to ₹ 10 Cr", "Exceeding ₹ 10 Cr"],
                            "rows": [
                                ["Domestic Company", "Nil", "7%", "12%"],
                                ["Foreign Company", "Nil", "2%", "5%"]
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s2_beats[-1]["t0"], s2_beats[-1]["t1"], [
                    {"label": "Up to ₹ 10 Cr", "sub": "7% Surcharge (32.1%)", "icon": "percent"},
                    {"label": "Above ₹ 10 Cr", "sub": "12% Surcharge (33.6%)", "icon": "percent"},
                    {"label": "Burden Spike", "sub": "Marginal Relief Active", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b3_formula",
                "branch_title": "Marginal Relief Ceiling Formula (₹ 10 Crore)",
                "badge": "§ Ceiling at ₹ 10 Cr",
                "icon": "calculator",
                "t0": audit["q10"]["slides"][2]["t0"],
                "t1": audit["q10"]["slides"][2]["t1"],
                "points": [
                    {
                        "id": "q10_p3_1",
                        "title": "Statutory Ceiling Formula",
                        "body": "Tax cannot exceed tax payable on ₹ 10 Crores with 7% surcharge plus income exceeding ₹ 10 Crores.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[0]["t0"],
                        "t1": s3_beats[0]["t1"],
                        "voice_sync_text": s3_beats[0]["text"],
                        "icon": "calculator",
                        "highlights": ["tax payable on ₹ 10 Crores", "7% surcharge", "income exceeding ₹ 10 Crores"]
                    },
                    {
                        "id": "q10_p3_2",
                        "title": "Excess Amount Granted as Relief",
                        "body": "The amount exceeding this statutory ceiling is deducted as marginal relief.",
                        "spoken": True,
                        "reference": False,
                        "t0": s3_beats[1]["t0"],
                        "t1": s3_beats[1]["t1"],
                        "voice_sync_text": s3_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["marginal relief"]
                    },
                    {
                        "id": "q10_p3_ref",
                        "title": "Worked Example: Y Ltd. (₹ 10,01,00,000)",
                        "body": "Computation of marginal relief at ₹ 10 Crore threshold for A.Y. 2026-27.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "calculator",
                        "example_calc": {
                            "title": "Question 10: Y Ltd. (Domestic Company) Total Income ₹ 10,01,00,000",
                            "inputs": "Gross Total Income = ₹ 10,01,00,000. P.Y. 2023-24 turnover = ₹ 410 Crores (> ₹ 400 Cr -> Base 30%).",
                            "steps": [
                                "Step 1: Normal tax + 12% SC @ 33.6% = ₹ 10,01,00,000 × 33.6% = ₹ 3,36,33,600.",
                                "Step 2: Ceiling = Tax on ₹ 10 Crores @ 32.1% (30% + 7% SC = ₹ 3,21,00,000) + Excess income (₹ 1,00,000) = ₹ 3,22,00,000.",
                                "Step 3: Marginal Relief = Normal Tax (₹ 3,36,33,600) - Ceiling (₹ 3,22,00,000) = ₹ 14,33,600.",
                                "Step 4: Tax payable after marginal relief = ₹ 3,22,00,000.",
                                "Step 5: Add 4% Cess on ₹ 3,22,00,000 = ₹ 12,88,000. Final Tax Liability = ₹ 3,34,88,000."
                            ]
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s3_beats[-1]["t0"], s3_beats[-1]["t1"], [
                    {"label": "Tax on ₹ 10 Cr (7%)", "sub": "₹ 3,21,00,000", "icon": "calculator"},
                    {"label": "Add Excess", "sub": "+ ₹ 1,00,000 = ₹ 3.22 Cr", "icon": "rupee"},
                    {"label": "Marginal Relief", "sub": "₹ 14,33,600 Deducted", "icon": "shield"}
                ])
            },
            {
                "branch_id": "b4_traps",
                "branch_title": "Crucial Exam Traps: Foreign Company Rates & Cess Addition",
                "badge": "§ Foreign Company Rates",
                "icon": "warning",
                "t0": audit["q10"]["slides"][3]["t0"],
                "t1": audit["q10"]["slides"][3]["t1"],
                "points": [
                    {
                        "id": "q10_p4_1",
                        "title": "Foreign Company 2% & 5% Surcharge",
                        "body": "Surcharge rates for foreign companies are 2% (above ₹ 1 Crore) and 5% (above ₹ 10 Crores).",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[0]["t0"],
                        "t1": s4_beats[0]["t1"],
                        "voice_sync_text": s4_beats[0]["text"],
                        "icon": "building",
                        "highlights": ["foreign companies", "2%", "5%"]
                    },
                    {
                        "id": "q10_p4_2",
                        "title": "Domestic Company 7% & 12% Surcharge",
                        "body": "In contrast, surcharge rates for domestic companies are 7% and 12%.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[1]["t0"],
                        "t1": s4_beats[1]["t1"],
                        "voice_sync_text": s4_beats[1]["text"],
                        "icon": "shield",
                        "highlights": ["domestic companies", "7%", "12%"]
                    },
                    {
                        "id": "q10_p4_3",
                        "title": "Mandatory 4% Cess Addition",
                        "body": "Finally, remember to add 4% Health and Education Cess to complete tax computation.",
                        "spoken": True,
                        "reference": False,
                        "t0": s4_beats[2]["t0"],
                        "t1": s4_beats[2]["t1"],
                        "voice_sync_text": s4_beats[2]["text"],
                        "icon": "percent",
                        "highlights": ["4% Cess"]
                    },
                    {
                        "id": "q10_p4_ref",
                        "title": "Exam Trap: Foreign Rate Confusion & Cess Order",
                        "body": "Common mistake vs statutory rule regarding company surcharge and marginal relief.",
                        "spoken": False,
                        "reference": True,
                        "t0": None,
                        "t1": None,
                        "voice_sync_text": None,
                        "icon": "warning",
                        "trap_data": {
                            "mistake": "Applying 7% or 12% surcharge to a foreign company, or adding 4% cess before computing marginal relief.",
                            "statutory_rule": "Foreign companies pay 2% surcharge (1-10 Cr) and 5% surcharge (>10 Cr). Base tax is 40%. Marginal relief is deducted before adding 4% cess."
                        }
                    }
                ],
                "flow_summary": compute_flow_steps(s4_beats[-1]["t0"], s4_beats[-1]["t1"], [
                    {"label": "Domestic (7% / 12%)", "sub": "Foreign (2% / 5%)", "icon": "building"},
                    {"label": "Deduct Relief", "sub": "Capped at ₹ 3.22 Cr", "icon": "shield"},
                    {"label": "Add 4% Cess", "sub": "Final Tax Liability", "icon": "check"}
                ])
            }
        ]
    }

def main():
    q1 = build_q1()
    q2 = build_q2()
    q3 = build_q3()
    q4 = build_q4()
    q5 = build_q5()
    q6 = build_q6()
    q7 = build_q7()
    q8 = build_q8()
    q9 = build_q9()
    q10 = build_q10()
    
    mindmaps = {
        "question_to_mindmap": {
            "1": "q1",
            "2": "q2",
            "3": "q3",
            "4": "q4",
            "5": "q5",
            "6": "q6",
            "7": "q7",
            "8": "q8",
            "9": "q9",
            "10": "q10"
        },
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10
    }
    
    with open(MINDMAPS_PATH, "w", encoding="utf-8") as f:
        json.dump(mindmaps, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Successfully built and saved updated mindmaps.json to {MINDMAPS_PATH}")
    print(f"Total topics: {len(mindmaps) - 1} topics (q1..q10)")

if __name__ == "__main__":
    main()
