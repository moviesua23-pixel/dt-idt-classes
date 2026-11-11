import os
import sys
import json
import wave
import subprocess
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator
from google.genai import types

AUDIO_DIR = os.path.join(PROJECT_ROOT, "data", "audio")
MINDMAP_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")
PROVISIONS_PATH = os.path.join(PROJECT_ROOT, "data", "provisions.json")
STORYBOARD_PATH = os.path.join(PROJECT_ROOT, "data", "ppt_storyboards.json")
TEMP_DIR = os.path.join(PROJECT_ROOT, "data", "audio_temp", "q1_expressive")
os.makedirs(TEMP_DIR, exist_ok=True)

VOICE_NAME = "Aoede"
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2  # 16-bit mono

# Deliberate sync pauses
INTER_CARD_PAUSE = 0.750   # 750ms between cards within a block
INTER_BLOCK_PAUSE = 1.400  # 1400ms between branches/blocks so presentation transitions gracefully

def generate_expressive_pcm(text: str) -> bytes:
    """Generates expressive, teacher-toned Malayalam audio PCM bytes."""
    prompt = (
        f"You are a warm, engaging, and passionate Malayalam professor teaching tax law to CA students. "
        f"Speak with lively natural emotion, varied pitch, conversational pauses, and clear pronunciation of English legal terms. "
        f"Do not sound robotic or monotone; sound like a real teacher in a classroom.\n\n"
        f"Text to speak:\n{text}"
    )
    
    max_attempts = len(rotator.keys)
    for attempt in range(max_attempts):
        client = rotator.get_client()
        try:
            resp = client.models.generate_content(
                model='gemini-2.5-flash-preview-tts',
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['AUDIO'],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=VOICE_NAME
                            )
                        )
                    )
                )
            )
            if resp.candidates and resp.candidates[0].content and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.data:
                        return part.inline_data.data
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(2)
    raise RuntimeError(f"Failed to generate audio for text: {text}")

def main():
    print("=== Generating Expressive, Transition-Synced Audio for Q1 ===", flush=True)
    
    with open(MINDMAP_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
    with open(PROVISIONS_PATH, "r", encoding="utf-8") as f:
        provisions = json.load(f)
        
    q1_mm = mindmaps.get("q1")
    if not q1_mm:
        print("Error: q1 not found in mindmaps.json")
        return

    # Intro text for Q1
    intro_text = "ഇന്ന് Section 4-ലെ diversion of income, application of income എന്നീ പ്രധാന നിയമസങ്കൽപ്പങ്ങൾ നമുക്ക് വിശദമായി പഠിക്കാം."
    print("-> Synthesizing Intro...", flush=True)
    intro_pcm = generate_expressive_pcm(intro_text)
    intro_dur = len(intro_pcm) / (SAMPLE_RATE * BYTES_PER_SAMPLE)
    
    clips = [(intro_pcm, intro_dur, "intro", None)]
    
    current_time = 0.0
    intro_t0 = 0.0
    intro_t1 = round(intro_dur, 2)
    current_time = intro_t1 + INTER_BLOCK_PAUSE
    
    if "root" in q1_mm:
        q1_mm["root"]["t0"] = intro_t0
        q1_mm["root"]["t1"] = intro_t1
    
    # Iterate through branches and points
    for bi, branch in enumerate(q1_mm.get("branches", [])):
        b_title = branch.get("branch_title", "")
        b_t0 = round(current_time, 2)
        print(f"\n-> Branch {bi+1}: {b_title} (Starts at {b_t0}s)", flush=True)
        
        points = branch.get("points", [])
        for pi, pt in enumerate(points):
            text = pt.get("voice_sync_text") or pt.get("body")
            if isinstance(text, list):
                text = " ".join(text)
            
            p_title = pt.get("title", "")
            print(f"   Point {pi+1}: {p_title}...", flush=True)
            pcm = generate_expressive_pcm(text)
            dur = len(pcm) / (SAMPLE_RATE * BYTES_PER_SAMPLE)
            
            p_t0 = round(current_time, 2)
            p_t1 = round(current_time + dur, 2)
            
            pt["t0"] = p_t0
            pt["t1"] = p_t1
            pt["spoken"] = True
            
            print(f"     => [{p_t0}s - {p_t1}s] ({dur:.2f}s)", flush=True)
            
            # Determine pause after this point
            is_last_in_branch = (pi == len(points) - 1)
            pause_sec = INTER_BLOCK_PAUSE if is_last_in_branch else INTER_CARD_PAUSE
            
            clips.append((pcm, dur, f"b{bi+1}_p{pi+1}", pause_sec))
            current_time = round(p_t1 + pause_sec, 2)
            
        branch["t0"] = b_t0
        branch["t1"] = round(points[-1]["t1"] if points else current_time, 2)
    
    total_audio_dur = round(current_time, 2)
    q1_mm["total_duration"] = total_audio_dur
    print(f"\nTotal calculated duration: {total_audio_dur}s", flush=True)
    
    # Stitch PCM clips with exact silence buffers
    full_wav_path = os.path.join(TEMP_DIR, "q1_stitched.wav")
    final_mp3_path = os.path.join(AUDIO_DIR, "q1.mp3")
    
    # Backup old q1.mp3
    old_mp3_path = os.path.join(AUDIO_DIR, "q1_old.mp3")
    if os.path.exists(final_mp3_path) and not os.path.exists(old_mp3_path):
        import shutil
        shutil.copy2(final_mp3_path, old_mp3_path)
        print(f"Backed up old q1.mp3 to {old_mp3_path}")
        
    with wave.open(full_wav_path, "wb") as out_wf:
        out_wf.setnchannels(1)
        out_wf.setsampwidth(BYTES_PER_SAMPLE)
        out_wf.setframerate(SAMPLE_RATE)
        
        for idx, (pcm, dur, tag, pause_sec) in enumerate(clips):
            out_wf.writeframes(pcm)
            if pause_sec and pause_sec > 0:
                silence_bytes = b'\x00' * int(SAMPLE_RATE * BYTES_PER_SAMPLE * pause_sec)
                out_wf.writeframes(silence_bytes)
                
    # Convert stitched WAV to high quality MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", full_wav_path,
        "-b:a", "192k",
        "-ar", "24000",
        final_mp3_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"Successfully created high-quality expressive audio: {final_mp3_path}")
    
    # Save updated mindmaps.json
    with open(MINDMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(mindmaps, f, indent=2, ensure_ascii=False)
    print("Updated data/mindmaps.json with exact sample-accurate timestamps!")
    
    # Update provisions.json for Q1
    for p in provisions:
        if p.get("question_number") == 1:
            p["dur"] = total_audio_dur
            p["duration_seconds"] = total_audio_dur
            p["voice"] = "Gemini Voice (Aoede - Expressive)"
            p["voice_engine"] = "Gemini Voice (Aoede)"
            p["audio_file"] = "q1.mp3"
            
    with open(PROVISIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(provisions, f, indent=2, ensure_ascii=False)
    print("Updated data/provisions.json!")
    
    # Also update frontend/index.html embedded snapshot
    index_path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    import re
    # Update pipeline-data embedded JSON
    m = re.search(r'(<script type="application/json" id="pipeline-data">)([\s\S]+?)(</script>)', html)
    if m:
        try:
            pipe_data = json.loads(m.group(2))
            if "mindmaps" in pipe_data and "q1" in pipe_data["mindmaps"]:
                pipe_data["mindmaps"]["q1"] = q1_mm
            if "provisions" in pipe_data:
                for p in pipe_data["provisions"]:
                    if p.get("question_number") == 1:
                        p["dur"] = total_audio_dur
                        p["duration_seconds"] = total_audio_dur
                        p["voice"] = "Gemini Voice (Aoede - Expressive)"
                        p["audio_file"] = "q1.mp3"
            new_json = json.dumps(pipe_data, ensure_ascii=False)
            html = html[:m.start(2)] + new_json + html[m.end(2):]
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(html)
            print("Updated frontend/index.html embedded snapshot!")
        except Exception as e:
            print("Error updating index.html:", e)

if __name__ == "__main__":
    main()
