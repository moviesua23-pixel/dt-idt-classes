import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.cloud_client import cloud_client

sys.stdout.reconfigure(encoding='utf-8')

PROVISIONS_PATH = os.path.join(PROJECT_ROOT, "data", "provisions.json")
MINDMAPS_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")
QNA_PATH = os.path.join(PROJECT_ROOT, "data", "extracted_qna.json")

def main():
    print("=== SYNCING ALL TOPICS (Q1 - Q10) TO GOOGLE SHEETS ===")
    with open(PROVISIONS_PATH, "r", encoding="utf-8") as f:
        provisions = json.load(f)
    with open(MINDMAPS_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
    with open(QNA_PATH, "r", encoding="utf-8") as f:
        qna = json.load(f)

    cloud_client.init_google_sheet("Sheet1")

    for p in provisions:
        q_num = p.get("question_number")
        q_key = f"q{q_num}"
        mm = mindmaps.get(q_key, {})
        q_obj = next((q for q in qna if q.get("question_number") == q_num), {})

        # Multi-format provision Markdown
        pres_md = p.get("provision_presentation_markdown", "")
        stat_sec = p.get("statutory_sections", "")
        core_princ = p.get("core_principle", "")

        multi_provision = f"### {stat_sec}: {core_princ}\n\n{pres_md}"

        # Provision Summary JSON
        prov_summary_json = json.dumps(mm, ensure_ascii=False)

        # Spoken narration list
        narration_list = []
        if "root" in mm:
            narration_list.append({
                "clip": "V1.mp3",
                "title": mm["root"].get("title", ""),
                "t0": mm["root"].get("t0", 0),
                "t1": mm["root"].get("t1", 13.25),
                "narration": f"നമസ്കാരം! ഇന്ന് നമ്മൾ {stat_sec} പ്രകാരമുള്ള {core_princ} വിശദമായി പഠിക്കാം."
            })

        clip_counter = 2
        for bi, b in enumerate(mm.get("branches", [])):
            for pi, pt in enumerate(b.get("points", [])):
                narration_list.append({
                    "clip": f"V{clip_counter}.mp3",
                    "branch": b.get("branch_title", ""),
                    "title": pt.get("title", ""),
                    "t0": pt.get("t0"),
                    "t1": pt.get("t1"),
                    "narration": pt.get("voice_sync_text", "")
                })
                clip_counter += 1

        row_data = {
            "Subject": "DT",
            "Chapter No": "Chapter 1: Basic Concepts",
            "Question No": f"Q{q_num}",
            "Question": q_obj.get("question_text", f"Direct Tax Question {q_num}"),
            "Answer": q_obj.get("icai_answer_text", f"ICAI Solution for Question {q_num}"),
            "Provisions": multi_provision,
            "Provision Summary": prov_summary_json,
            "Malayalam Narration & Timings": json.dumps(narration_list, ensure_ascii=False)
        }

        cloud_client.append_or_update_question_row(row_data, "Sheet1")

    print("\nALL QUESTIONS Q1 - Q10 SUCCESSFULLY SYNCED TO GOOGLE SHEET!")

if __name__ == "__main__":
    main()
