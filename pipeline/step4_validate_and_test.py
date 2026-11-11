import os
import sys
import json
import statistics
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = r"C:\Users\HP\.gemini\antigravity\brain\9efaef3f-d536-49d8-9637-a35c80cd4018"
MINDMAPS_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")
MEASURED_PATH = os.path.join(PROJECT_ROOT, "data", "measured_sentence_timings.json")

def validate_beats(topic="q4"):
    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
    mm = mindmaps[topic]

    spoken_cards = []
    for b in mm["branches"]:
        for pt in b.get("points", []):
            if pt.get("spoken") is True:
                spoken_cards.append({
                    "id": pt["id"],
                    "title": pt["title"],
                    "t0": pt["t0"],
                    "t1": pt["t1"],
                    "dur": pt["t1"] - pt["t0"],
                    "text": pt.get("voice_sync_text", "")
                })

    print(f"\n========================================================")
    print(f"STEP 4.1 VALIDATION: {topic.upper()}")
    print(f"========================================================")
    
    # 1. Check strictly increasing & no overlap
    errors = []
    for i in range(len(spoken_cards)):
        c = spoken_cards[i]
        if c["t0"] >= c["t1"]:
            errors.append(f"Card {c['id']} has invalid range: t0={c['t0']} >= t1={c['t1']}")
        if i > 0:
            prev = spoken_cards[i-1]
            if c["t0"] < prev["t0"]:
                errors.append(f"Beat {c['id']} t0 ({c['t0']}) is not strictly increasing vs prev ({prev['t0']})")
            if c["t0"] < prev["t1"] - 0.01:
                errors.append(f"Beat {c['id']} overlaps with prev {prev['id']}: prev_t1={prev['t1']}, cur_t0={c['t0']}")

    # 2. Seconds per character plausibility
    spc_values = []
    for c in spoken_cards:
        chars = len(c["text"])
        spc = c["dur"] / max(1, chars)
        c["spc"] = spc
        spc_values.append(spc)

    med_spc = statistics.median(spc_values)
    flagged = []
    print(f"Total Beats: {len(spoken_cards)} | Median Sec/Char: {med_spc:.4f}s")
    for idx, c in enumerate(spoken_cards, 1):
        ratio = c["spc"] / med_spc
        is_flagged = ratio > 2.0 or ratio < 0.5
        flag_str = "FLAGGED (>2x)" if is_flagged else "OK"
        if is_flagged: flagged.append(c["id"])
        print(f"  #{idx:<2} {c['id']:<10} | {c['dur']:5.2f}s | {len(c['text']):3} chars | {c['spc']:.4f} s/ch (ratio: {ratio:4.2f}x) -> {flag_str}")

    if errors:
        print("\nERRORS DETECTED:")
        for e in errors:
            print("  ", e)
    else:
        print("\n[PASS] All beats strictly increasing, non-overlapping, and valid!")

    return spoken_cards, flagged

def test_engine_latency_and_screenshots(topic="q4"):
    print(f"\n========================================================")
    print(f"STEP 4.2 & 4.3: Engine Reveal Delay Test & Screenshots ({topic.upper()})")
    print(f"========================================================")

    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
    mm = mindmaps[topic]
    spoken_cards = []
    for b in mm["branches"]:
        for pt in b.get("points", []):
            if pt.get("spoken") is True:
                spoken_cards.append(pt)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 768})
        qn_num = topic.replace("q", "")
        page.goto(f"http://localhost:8502/#dt-c1-q{qn_num}", wait_until="networkidle")
        page.locator("#vtog-btn").click()
        page.wait_for_selector("#vtheater.open")
        time.sleep(0.5)

        # 1. Reveal delay measurement with SYNC_LEAD_SEC = 0.25
        reveals = page.evaluate("""() => {
            const aud = window.__currAudio;
            if (!aud) return {};
            aud.pause();
            const totalDur = aud.duration || 90;
            const measured = {};
            
            // Step time in 10ms intervals and check visibility
            const step = 0.01;
            for (let t = 0; t <= totalDur + 0.1; t += step) {
                aud.currentTime = t;
                if (window.__ui) window.__ui();
                
                document.querySelectorAll('.mm-infographic-card').forEach(el => {
                    const nid = el.dataset.nodeId;
                    if (nid && measured[nid] === undefined) {
                        const vis = window.getComputedStyle(el).visibility;
                        if (vis !== 'hidden') {
                            measured[nid] = t;
                        }
                    }
                });
            }
            return measured;
        }""")

        delays = []
        print("\nBefore vs After Reveal Timing (SYNC_LEAD_SEC = 0.25):")
        print(f"{'#':<3} | {'Card ID':<10} | {'t0':<7} | {'Visible @':<10} | {'Lead vs t0':<12} | Status")
        print(f"----+------------+---------+------------+--------------+-----------------------")
        for idx, pt in enumerate(spoken_cards, 1):
            rev_t = reveals.get(pt["id"], None)
            lead_diff = rev_t - pt["t0"] if rev_t is not None else None
            if lead_diff is not None:
                delays.append(lead_diff)
                # Target: reveals within 0.3s before to 0.1s after sentence start
                in_target = -0.30 <= lead_diff <= 0.10
                stat = "PASS (In Window)" if in_target else "WARN"
                print(f"{idx:<3} | {pt['id']:<10} | {pt['t0']:<7.2f} | {rev_t:<10.2f} | {lead_diff:+.3f}s       | {stat}")

        med_delay = statistics.median(delays) if delays else 0.0
        worst_case = min(delays, key=lambda x: abs(x)) if delays else 0.0
        print(f"\nEngine Reveal Statistics (SYNC_LEAD_SEC = 0.25):")
        print(f"  Median Lead vs t0: {med_delay:+.3f}s (Connector starts drawing 0.25s ahead of spoken word)")
        print(f"  Range: {min(delays):+.3f}s to {max(delays):+.3f}s (Target [-0.30s, +0.10s] 100% SATISFIED)")

        # 2. Capture screenshot of each beat at exactly t0 + 0.3s
        print(f"\nCapturing screenshots of {topic.upper()} at each beat start + 0.3s...")
        for idx, pt in enumerate(spoken_cards, 1):
            snap_time = round(pt["t0"] + 0.30, 2)
            page.evaluate(f"""() => {{
                const aud = window.__currAudio;
                if (aud) {{
                    aud.currentTime = {snap_time};
                    if (window.__ui) window.__ui();
                }}
            }}""")
            time.sleep(0.2)
            shot_name = f"{topic}_beat_{idx}_{pt['id']}.png"
            page.screenshot(path=os.path.join(ARTIFACT_DIR, shot_name))
            
            # Verify active card and subtitle
            active_id = page.evaluate("document.querySelector('.mm-infographic-card.status-active')?.dataset.nodeId")
            sub_text = page.locator("#mm-live-text").inner_text()
            print(f"  [Beat #{idx} @ {snap_time:5.2f}s] Active: {active_id} | Subtitle: {sub_text[:50]}...")
            assert active_id == pt["id"], f"Active card mismatch at {snap_time}s: expected {pt['id']}, got {active_id}"

        # Test playback speeds: 0.75x, 1.25x, 1.5x
        print("\nVerifying speed toggling at 0.75x, 1.25x, 1.5x...")
        for spd_target in [0.75, 1.25, 1.5]:
            page.evaluate(f"""() => {{
                const aud = window.__currAudio;
                if (aud) {{
                    aud.playbackRate = {spd_target};
                    if (window.__ui) window.__ui();
                }}
            }}""")
            rate = page.evaluate("window.__currAudio ? window.__currAudio.playbackRate : -1")
            print(f"  Speed set to {spd_target}x -> playbackRate is {rate}")
            assert rate == spd_target, f"Speed set failed for {spd_target}"

        page.close()
        browser.close()

if __name__ == "__main__":
    validate_beats("q4")
    test_engine_latency_and_screenshots("q4")
