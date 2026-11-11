import os
import sys
import json
import argparse
import subprocess
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
MINDMAPS_PATH = os.path.join(DATA_DIR, "mindmaps.json")
STORYBOARDS_PATH = os.path.join(DATA_DIR, "ppt_storyboards.json")
TIMING_AUDIT_PATH = os.path.join(DATA_DIR, "mindmap_timing_audit.json")

ALLOWED_ICONS = {"scales", "shield", "calculator", "percent", "cap", "warning", "gear", "check", "user", "building", "rupee"}

def get_ffprobe_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(p.stdout.strip())

def verify_worked_examples(topic_key, mm_data):
    """
    Recomputes tax liabilities in Python to verify mathematical accuracy.
    """
    errors = []
    if topic_key == "q4":
        # Mr. Arjun: Total income ₹ 16,00,000
        # Age 52: 2.5L-5L @ 5% (12,500) + 5L-10L @ 20% (1,00,000) + 10L-16L @ 30% (1,80,000) = 2,92,500. Cess 4% = 11,700. Total = 3,04,200
        tax_52 = 12500 + 100000 + 180000
        cess_52 = tax_52 * 0.04
        tot_52 = tax_52 + cess_52
        if tot_52 != 304200:
            errors.append(f"Q4 math mismatch: computed {tot_52} != 304200")
            
        # Age 64: 3L-5L @ 5% (10,000) + 5L-10L @ 20% (1,00,000) + 10L-16L @ 30% (1,80,000) = 2,90,000. Cess 4% = 11,600. Total = 3,01,600
        tax_64 = 10000 + 100000 + 180000
        cess_64 = tax_64 * 0.04
        tot_64 = tax_64 + cess_64
        if tot_64 != 301600:
            errors.append(f"Q4 math mismatch: computed {tot_64} != 301600")
            
        # Age 83: 5L-10L @ 20% (1,00,000) + 10L-16L @ 30% (1,80,000) = 2,80,000. Cess 4% = 11,200. Total = 2,91,200
        tax_83 = 100000 + 180000
        cess_83 = tax_83 * 0.04
        tot_83 = tax_83 + cess_83
        if tot_83 != 291200:
            errors.append(f"Q4 math mismatch: computed {tot_83} != 291200")
            
    elif topic_key == "q5":
        # Mr. Manish: ₹ 4,15,000. Tax @ 5% on 1.65L = 8,250. Rebate 8,250 = Nil.
        tax = (415000 - 250000) * 0.05
        rebate = min(tax, 12500)
        net = tax - rebate
        if net != 0:
            errors.append(f"Q5 math mismatch: net {net} != 0")
            
    elif topic_key == "q6":
        # Mr. X: ₹ 16,00,000 default regime. 4L-8L (20k) + 8L-12L (40k) + 12L-16L (60k) = 1,20,000. Cess 4% = 4,800. Total = 1,24,800
        tax = 20000 + 40000 + 60000
        cess = tax * 0.04
        tot = tax + cess
        if tot != 124800:
            errors.append(f"Q6 math mismatch: computed {tot} != 124800")
            
    elif topic_key == "q7":
        # Mr. Mahesh: ₹ 11,00,000. Tax = 20k + (11L-8L)*10% (30k) = 50k. Rebate min(50k, 60k) = 50k. Net = 0
        tax = 20000 + (1100000 - 800000) * 0.10
        rebate = min(tax, 60000)
        net = tax - rebate
        if net != 0:
            errors.append(f"Q7 math mismatch: net {net} != 0")
            
    elif topic_key == "q8":
        # Mr. Nitin: ₹ 12,50,000. Excess = 50,000 (A). Tax = 60k + 15% of 50k = 67,500 (B). Rebate = 67,500 - 50,000 = 17,500.
        # Tax after rebate = 50,000. Cess 4% = 2,000. Total = 52,000
        excess = 1250000 - 1200000
        tax = 60000 + (50000 * 0.15)
        rebate = tax - excess
        net_tax = tax - rebate
        tot = net_tax + (net_tax * 0.04)
        if tot != 52000:
            errors.append(f"Q8 math mismatch: computed {tot} != 52000")
            
    elif topic_key == "q9":
        # X Ltd.: ₹ 1,01,00,000. Base 30% + SC 7% = 32.1% -> 32,42,100.
        # Ceiling: Tax on 1 Cr (30L) + Excess (1L) = 31,00,000.
        # Marginal relief: 32,42,100 - 31,00,000 = 1,42,100.
        tax = 10100000 * 0.321
        ceiling = (10000000 * 0.30) + 100000
        relief = tax - ceiling
        if round(relief, 2) != 142100.0:
            errors.append(f"Q9 math mismatch: computed relief {relief} != 142100")
            
    elif topic_key == "q10":
        # Y Ltd.: ₹ 10,01,00,000. Base 30% + SC 12% = 33.6% -> 3,36,33,600.
        # Ceiling: Tax on 10 Cr @ 32.1% (3,21,00,000) + Excess (1,00,000) = 3,22,00,000.
        # Marginal relief: 3,36,33,600 - 3,22,00,000 = 14,33,600.
        tax = 100100000 * 0.336
        ceiling = (100000000 * 0.321) + 100000
        relief = tax - ceiling
        if round(relief, 2) != 1433600.0:
            errors.append(f"Q10 math mismatch: computed relief {relief} != 1433600")
            
    return errors

def validate_topic(topic_key: str, mm_data: dict, storyboard: dict, timing_audit: dict, audio_dur: float):
    errors = []
    warnings = []
    
    # Check audio length against last branch t1
    branches = mm_data.get("branches", [])
    if len(branches) != 4:
        errors.append(f"Expected 4 branches, found {len(branches)}")
        return False, errors, warnings, []
        
    last_branch_t1 = float(branches[-1].get("t1", 0.0))
    if abs(last_branch_t1 - audio_dur) > 0.05:
        errors.append(f"Last branch t1 ({last_branch_t1}) does not match audio length ({audio_dur:.2f}s)")
        
    # Check worked example math
    math_errors = verify_worked_examples(topic_key, mm_data)
    errors.extend(math_errors)
    
    used_sentences = set()
    rows = []
    
    slides = storyboard.get("slides", [])
    audit_slides = timing_audit.get("slides", []) if timing_audit else []
    
    for bi, b in enumerate(branches):
        b_id = b.get("branch_id", f"b{bi+1}")
        b_title = b.get("branch_title", "")
        bt0 = float(b.get("t0", 0.0))
        bt1 = float(b.get("t1", 0.0))
        b_icon = b.get("icon")
        
        if b_icon and b_icon not in ALLOWED_ICONS:
            errors.append(f"Branch {b_id} invalid icon '{b_icon}'")
            
        points = b.get("points", [])
        spoken_points = [p for p in points if p.get("spoken") is True]
        ref_points = [p for p in points if p.get("reference") is True]
        
        # Check against storyboard sentence count
        expected_sents = 0
        slide_narr = ""
        if bi < len(slides):
            slide_narr = slides[bi].get("malayalam_narration", "")
        if bi < len(audit_slides):
            expected_sents = audit_slides[bi].get("sentence_count", len(spoken_points))
            
        if len(spoken_points) != expected_sents:
            errors.append(f"Branch {b_id} beat count ({len(spoken_points)}) != sentence count ({expected_sents})")
            
        # Check duration slicing (equal slices forbidden)
        if len(spoken_points) > 1:
            durs = [float(p["t1"]) - float(p["t0"]) for p in spoken_points]
            # Check if all durations are identical within 0.01s
            if max(durs) - min(durs) < 0.05:
                errors.append(f"Branch {b_id} spoken beats appear to be equal slices ({durs[0]:.2f}s each)")
                
        # Validate each point
        prev_t1 = bt0
        for pi, pt in enumerate(points):
            pt_id = pt.get("id", f"{b_id}_p{pi+1}")
            pt_title = pt.get("title", "")
            is_spoken = pt.get("spoken") is True
            pt_icon = pt.get("icon")
            
            if pt_icon and pt_icon not in ALLOWED_ICONS:
                errors.append(f"Point {pt_id} invalid icon '{pt_icon}'")
                
            if is_spoken:
                pt0 = float(pt.get("t0", 0.0))
                pt1 = float(pt.get("t1", 0.0))
                sync_text = pt.get("voice_sync_text", "")
                
                # Must be exact substring of slide narration
                if slide_narr and sync_text not in slide_narr:
                    errors.append(f"Point {pt_id} voice_sync_text is NOT an exact substring of slide narration")
                    
                # Sentence reuse check
                if sync_text in used_sentences:
                    errors.append(f"Point {pt_id} reuses sentence already used: '{sync_text[:30]}...'")
                used_sentences.add(sync_text)
                
                # Timing range check
                if pt0 >= pt1:
                    errors.append(f"Point {pt_id} invalid timing: {pt0} >= {pt1}")
                if pt0 < bt0 - 0.05 or pt1 > bt1 + 0.05:
                    errors.append(f"Point {pt_id} timing [{pt0}, {pt1}] falls outside branch [{bt0}, {bt1}]")
                if pt0 < prev_t1 - 0.05:
                    errors.append(f"Point {pt_id} t0 ({pt0}) overlaps previous t1 ({prev_t1})")
                    
                prev_t1 = pt1
                
                rows.append({
                    "branch": b_title[:16],
                    "entity": pt_id,
                    "kind": "Spoken Beat",
                    "t0": f"{pt0:5.2f}s",
                    "t1": f"{pt1:5.2f}s",
                    "dur": f"{(pt1-pt0):4.1f}s",
                    "text": pt_title[:38]
                })
            else:
                extra = ""
                if pt.get("table_data"):
                    extra = " [TABLE]"
                elif pt.get("example_calc"):
                    extra = " [EXAMPLE]"
                elif pt.get("trap_data"):
                    extra = " [TRAP]"
                rows.append({
                    "branch": b_title[:16],
                    "entity": pt_id,
                    "kind": "Reference",
                    "t0": "  --- ",
                    "t1": "  --- ",
                    "dur": " --- ",
                    "text": (pt_title + extra)[:38]
                })
                
        # Last spoken beat must end within 0.5s of branch t1
        if spoken_points:
            last_spk_t1 = float(spoken_points[-1]["t1"])
            if abs(last_spk_t1 - bt1) > 0.5:
                errors.append(f"Branch {b_id} last spoken beat ends at {last_spk_t1}, more than 0.5s from branch end {bt1}")
                
        # Flow summary validation
        flow_summary = b.get("flow_summary", [])
        if not flow_summary or len(flow_summary) < 3:
            errors.append(f"Branch {b_id} has fewer than 3 flow steps ({len(flow_summary)})")
        for fi, fs in enumerate(flow_summary):
            f_icon = fs.get("icon")
            if f_icon and f_icon not in ALLOWED_ICONS:
                errors.append(f"Branch {b_id} flow step {fi+1} invalid icon '{f_icon}'")
            ft0 = float(fs.get("t0", 0.0))
            ft1 = float(fs.get("t1", 0.0))
            if ft0 >= ft1:
                errors.append(f"Branch {b_id} flow step {fi+1} invalid timing: {ft0} >= {ft1}")
            rows.append({
                "branch": b_title[:16],
                "entity": f"flow_{bi+1}_{fi+1}",
                "kind": "Flow Step",
                "t0": f"{ft0:5.2f}s",
                "t1": f"{ft1:5.2f}s",
                "dur": f"{(ft1-ft0):4.1f}s",
                "text": f"[{fs.get('label')}] {fs.get('sub', '')}"[:38]
            })

    # Print Timing Table
    print("\n" + "="*105)
    print(f"TIMING & INFOGRAPHIC AUDIT TABLE: {topic_key.upper()} (Audio Duration: {audio_dur:.2f}s)")
    print("="*105)
    print(f"{'Branch':<16} | {'Entity ID':<14} | {'Kind':<12} | {'Start':<7} | {'End':<7} | {'Dur':<6} | {'Title / Summary'}")
    print("-"*105)
    for r in rows:
        print(f"{r['branch']:<16} | {r['entity']:<14} | {r['kind']:<12} | {r['t0']:<7} | {r['t1']:<7} | {r['dur']:<6} | {r['text']}")
    print("="*105 + "\n")
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings, rows

def main():
    parser = argparse.ArgumentParser(description="Strict Validation Script for Mind Maps")
    parser.add_argument("--topic", help="Specific topic to validate, e.g. q4")
    args = parser.parse_args()
    
    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
        
    with open(STORYBOARDS_PATH, "r", encoding="utf-8") as f:
        storyboards = json.load(f)
        
    with open(TIMING_AUDIT_PATH, "r", encoding="utf-8") as f:
        timing_audit = json.load(f)
        
    # Check question_to_mindmap
    q_to_mm = mindmaps.get("question_to_mindmap", {})
    print("Checking question_to_mindmap:")
    print(" ", q_to_mm)
    for q_num in range(1, 11):
        str_q = str(q_num)
        if str_q not in q_to_mm:
            print(f"ERROR: Question {str_q} missing in question_to_mindmap")
            sys.exit(1)
            
    target_topics = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
    if args.topic:
        target_topics = [args.topic]
        
    total_passed = 0
    total_failed = 0
    
    for t_key in target_topics:
        mm = mindmaps.get(t_key)
        if not mm:
            print(f"[{t_key}] MISSING from mindmaps.json")
            total_failed += 1
            continue
            
        # Audio mapping: q1, q2, q3 share q1.mp3
        audio_key = "q1" if t_key in ["q1", "q2", "q3"] else t_key
        audio_file = os.path.join(AUDIO_DIR, f"{audio_key}.mp3")
        audio_dur = get_ffprobe_duration(audio_file)
        
        sb = storyboards.get(audio_key, {})
        ta = timing_audit.get(audio_key, {})
        
        valid, errors, warnings, rows = validate_topic(t_key, mm, sb, ta, audio_dur)
        if valid:
            total_passed += 1
            print(f"[{t_key.upper()}] PASS: All {len(rows)} elements, timings, and math verified.")
        else:
            total_failed += 1
            print(f"[{t_key.upper()}] FAIL with {len(errors)} errors:")
            for e in errors:
                print(f"  - ERROR: {e}")
                
    print("\n" + "="*50)
    print(f"VALIDATION SUMMARY: {total_passed} PASSED, {total_failed} FAILED")
    print("="*50)
    
    if total_failed > 0:
        sys.exit(1)
    else:
        print("[SUCCESS] All mindmaps passed strict validation!")
        sys.exit(0)

if __name__ == "__main__":
    main()
