import os
import sys
import json
import re
import subprocess

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
STORYBOARDS_PATH = os.path.join(DATA_DIR, "ppt_storyboards.json")
OUTPUT_PATH = os.path.join(DATA_DIR, "mindmap_timing_audit.json")

def split_sentences(text):
    if not text:
        return []
    protected = text
    abbrevs = [
        'Sec.', 'u/s.', 'P.Y.', 'A.Y.', 'Ltd.', 'Co.', 'Dr.', 'Mr.', 'Mrs.', 'No.',
        'viz.', 'i.e.', 'e.g.', 'vs.', 'v.', 'Rs.', '₹'
    ]
    for idx, ab in enumerate(abbrevs):
        protected = protected.replace(ab, f"___ABB{idx}___")
    # Protect decimal numbers like 2.5, 12.5, 50.0, 87A etc.
    protected = re.sub(r'(\d+)\.(\d+)', r'\1___DOT___\2', protected)
    
    parts = re.split(r'(?<=[.?!।॥])\s+', protected.strip())
    
    res = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        for idx, ab in enumerate(abbrevs):
            p = p.replace(f"___ABB{idx}___", ab)
        p = p.replace("___DOT___", ".")
        res.append(p)
    return res

def get_silences(audio_path, noise_db=-30, min_duration=0.2):
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "-"
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    output = p.stderr
    
    silences = []
    start_matches = list(re.finditer(r'silence_start:\s*([0-9.]+)', output))
    end_matches = list(re.finditer(r'silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)', output))
    
    for s_m, e_m in zip(start_matches, end_matches):
        s_start = float(s_m.group(1))
        s_end = float(e_m.group(1))
        s_dur = float(e_m.group(2))
        silences.append({
            "start": s_start,
            "end": s_end,
            "duration": s_dur,
            "mid": round((s_start + s_end) / 2.0, 3)
        })
    return silences

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(p.stdout.strip())

def main():
    sb = json.load(open(STORYBOARDS_PATH, encoding='utf-8'))
    topics = ['q1', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
    
    audit_results = {}
    
    print("=========================================================================================")
    print("MIND MAP TIMING AUDIT: SENTENCE SPLITTING & SILENCE DETECTION")
    print("=========================================================================================")
    
    for topic in topics:
        audio_file = os.path.join(AUDIO_DIR, f"{topic}.mp3")
        total_audio_len = get_audio_duration(audio_file)
        silences = get_silences(audio_file, noise_db=-30, min_duration=0.2)
        if len(silences) < 5:
            silences = get_silences(audio_file, noise_db=-28, min_duration=0.15)
            
        topic_slides = sb[topic]["slides"]
        audit_results[topic] = {
            "audio_file": audio_file,
            "total_audio_length": round(total_audio_len, 3),
            "slides": []
        }
        
        print(f"\n--- TOPIC: {topic} (Total Audio: {total_audio_len:.2f}s) ---")
        
        for s_idx, slide in enumerate(topic_slides):
            s_num = slide["slide_number"]
            st0 = float(slide["t0"])
            st1 = float(slide["t1"])
            if s_idx == len(topic_slides) - 1:
                st1 = round(total_audio_len, 2)
                
            narr = slide.get("malayalam_narration", "")
            sentences = split_sentences(narr)
            n_sents = len(sentences)
            
            cand_silences = [
                s for s in silences
                if s["mid"] >= (st0 + 0.6) and s["mid"] <= (st1 - 0.6)
            ]
            
            beats = []
            if n_sents == 1:
                beats.append({
                    "sentence_idx": 1,
                    "text": sentences[0],
                    "t0": round(st0, 2),
                    "t1": round(st1, 2),
                    "method": "single_sentence"
                })
            else:
                sent_lens = [len(s) for s in sentences]
                total_len = sum(sent_lens)
                cum = 0
                expected_fractions = []
                for slen in sent_lens[:-1]:
                    cum += slen
                    expected_fractions.append(cum / total_len)
                
                expected_times = [st0 + (st1 - st0) * f for f in expected_fractions]
                
                chosen_boundaries = []
                used_silence_indices = set()
                
                for exp_t in expected_times:
                    close_cands = [
                        (idx, s) for idx, s in enumerate(cand_silences)
                        if idx not in used_silence_indices and abs(s["mid"] - exp_t) <= 3.5
                    ]
                    if close_cands:
                        close_cands.sort(key=lambda x: (x[1]["duration"], -abs(x[1]["mid"] - exp_t)), reverse=True)
                        best_idx, best_sil = close_cands[0]
                        chosen_boundaries.append(best_sil["mid"])
                        used_silence_indices.add(best_idx)
                    else:
                        min_bound = chosen_boundaries[-1] + 1.0 if chosen_boundaries else st0 + 1.0
                        avail = [
                            (idx, s) for idx, s in enumerate(cand_silences)
                            if idx not in used_silence_indices and s["mid"] > min_bound
                        ]
                        if avail:
                            avail.sort(key=lambda x: abs(x[1]["mid"] - exp_t))
                            best_idx, best_sil = avail[0]
                            chosen_boundaries.append(best_sil["mid"])
                            used_silence_indices.add(best_idx)
                        else:
                            chosen_boundaries.append(round(exp_t, 2))
                
                chosen_boundaries.sort()
                
                b_starts = [st0] + chosen_boundaries
                b_ends = chosen_boundaries + [st1]
                for b_i in range(n_sents):
                    beats.append({
                        "sentence_idx": b_i + 1,
                        "text": sentences[b_i],
                        "t0": round(b_starts[b_i], 2),
                        "t1": round(b_ends[b_i], 2),
                        "method": "silence_detect"
                    })
            
            print(f"Slide {s_num}: [{st0:.2f}s - {st1:.2f}s] ({n_sents} sentences)")
            for b in beats:
                txt_preview = b['text'][:60] + ('...' if len(b['text']) > 60 else '')
                dur = round(b['t1'] - b['t0'], 2)
                print(f"  Beat {b['sentence_idx']}: [{b['t0']:>5.2f}s - {b['t1']:>5.2f}s] ({dur:>4.1f}s) | {txt_preview}")
            
            audit_results[topic]["slides"].append({
                "slide_number": s_num,
                "t0": st0,
                "t1": st1,
                "sentence_count": n_sents,
                "beats": beats
            })
            
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Successfully wrote audit table to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
