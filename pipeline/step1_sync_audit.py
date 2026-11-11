import os
import sys
import json
import re
import time
import subprocess
import statistics
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "data", "audio")
MINDMAPS_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")

def get_silence_boundaries(audio_path):
    cmd = [
        "ffmpeg", "-y", "-i", audio_path,
        "-af", "silencedetect=noise=-30dB:d=0.20",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    boundaries = []
    for line in res.stderr.splitlines():
        m_start = re.search(r"silence_start:\s*([\d\.]+)", line)
        if m_start:
            boundaries.append(("start", float(m_start.group(1))))
        m_end = re.search(r"silence_end:\s*([\d\.]+)", line)
        if m_end:
            boundaries.append(("end", float(m_end.group(1))))
    return boundaries

def has_silence_near(boundaries, t0, tolerance=0.30):
    for b_type, b_time in boundaries:
        if abs(b_time - t0) <= tolerance:
            return True, b_type, b_time, abs(b_time - t0)
    return False, None, None, None

def run_step1_audit():
    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)

    target_topics = ["q4", "q6", "q8"]
    audit_results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)

        for topic in target_topics:
            print(f"\nAnalyzing {topic.upper()}...", flush=True)
            audio_file = os.path.join(AUDIO_DIR, f"{topic}.mp3")
            silence_bounds = get_silence_boundaries(audio_file)

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
                            "text": pt.get("voice_sync_text", "")
                        })

            # Check silence boundaries within 0.3s of t0
            for card in spoken_cards:
                has_s, s_type, s_time, s_diff = has_silence_near(silence_bounds, card["t0"], 0.30)
                card["has_silence_near"] = has_s
                card["silence_detail"] = f"{s_type}@{s_time:.2f}s (Δ{s_diff:.2f}s)" if has_s else "NO PAUSE"

            # Measure browser reveal timings using high-speed in-browser stepping (10ms steps)
            page = browser.new_page(viewport={"width": 1366, "height": 768})
            qn_num = topic.replace("q", "")
            page.goto(f"http://localhost:8502/#dt-c1-q{qn_num}", wait_until="networkidle")
            page.locator("#vtog-btn").click()
            page.wait_for_selector("#vtheater.open")
            time.sleep(0.5)

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
            page.close()

            delays = []
            for card in spoken_cards:
                cid = card["id"]
                rev_t = reveals.get(cid, None)
                card["reveal_time"] = rev_t
                if rev_t is not None:
                    diff = rev_t - card["t0"]
                    card["delay"] = diff
                    delays.append(diff)
                else:
                    card["delay"] = None

            median_delay = statistics.median(delays) if delays else 0.0
            audit_results[topic] = {
                "cards": spoken_cards,
                "delays": delays,
                "median_delay": median_delay
            }

        browser.close()

    # Print Full Audit Tables
    for topic in target_topics:
        res = audit_results[topic]
        cards = res["cards"]
        print(f"\n==========================================================================================================================================", flush=True)
        print(f"STEP 1 AUDIT RESULTS: {topic.upper()} (Median Delay: {res['median_delay']:+.4f}s)", flush=True)
        print(f"==========================================================================================================================================", flush=True)
        print(f"{'#':<3} | {'t0':<7} | {'t1':<7} | {'Pause within 0.3s?':<22} | {'Visible @':<10} | {'Diff vs t0':<11} | Sentence Substring", flush=True)
        print(f"----+---------+---------+------------------------+------------+-------------+-------------------------------------------------------------", flush=True)
        for idx, c in enumerate(cards, 1):
            rev_str = f"{c['reveal_time']:.2f}s" if c['reveal_time'] is not None else "NEVER"
            diff_str = f"{c['delay']:+.3f}s" if c['delay'] is not None else "N/A"
            text_snip = (c['text'][:65] + '...') if len(c['text']) > 65 else c['text']
            print(f"{idx:<3} | {c['t0']:<7.2f} | {c['t1']:<7.2f} | {c['silence_detail']:<22} | {rev_str:<10} | {diff_str:<11} | {text_snip}", flush=True)

    print("\n==========================================================================================================================================", flush=True)
    print("STEP 1 DELAY SUMMARY ACROSS AUDITED TOPICS", flush=True)
    print("==========================================================================================================================================", flush=True)
    for topic in target_topics:
        d = audit_results[topic]["delays"]
        print(f"{topic.upper()}: Median Delay = {statistics.median(d):+.4f}s | Min = {min(d):+.4f}s | Max = {max(d):+.4f}s | N = {len(d)} cards", flush=True)

if __name__ == "__main__":
    run_step1_audit()
