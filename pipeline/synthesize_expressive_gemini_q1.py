import os
import sys
import json
import wave
import subprocess
import time
from pydub import AudioSegment
from pydub.silence import detect_silence

PROJECT_ROOT = r"C:\Users\HP\OneDrive\Desktop\VISHNU\DT and IDT Classes"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator
from google import genai
from google.genai import types

sys.stdout.reconfigure(encoding='utf-8')

AUDIO_DIR = os.path.join(PROJECT_ROOT, "data", "audio")
MINDMAP_PATH = os.path.join(PROJECT_ROOT, "data", "mindmaps.json")
PROVISIONS_PATH = os.path.join(PROJECT_ROOT, "data", "provisions.json")
INDEX_PATH = os.path.join(PROJECT_ROOT, "frontend", "index.html")
TEMP_DIR = os.path.join(PROJECT_ROOT, "data", "audio_temp", "q1_gemini_expressive")
os.makedirs(TEMP_DIR, exist_ok=True)

MODEL_NAME = 'gemini-2.5-flash-preview-tts'
VOICE_NAME = 'Aoede'
SAMPLE_RATE = 24000
BYTES_PER_SAMPLE = 2

# Expressive, pedagogical Malayalam scripts with phonetic English terms
SCRIPTS = {
    "intro": (
        "നമസ്കാരം! ഇന്ന് നമ്മൾ പഠിക്കുന്നത് ഇൻകം ടാക്സ് ആക്റ്റിലെ സെക്ഷൻ നാല് പ്രകാരമുള്ള, "
        "ഡൈവേർഷൻ ഓഫ് ഇൻകം, ആപ്ലിക്കേഷൻ ഓഫ് ഇൻകം എന്നീ രണ്ട് സുപ്രധാന നിയമ തത്വങ്ങളാണ്. "
        "നമുക്ക് ഓരോന്നായി വിശദമായി മനസ്സിലാക്കാം."
    ),
    "branch1": (
        "ആദ്യമായി കോർ ഡിസ്റ്റിൻക്ഷൻ നോക്കാം. വരുമാനത്തിന്റെ വിനിയോഗത്തിൽ രണ്ട് പ്രധാന നിയമസ്ഥിതികളാണുള്ളത്. "
        "വരുമാനത്തിന്റെ സോഴ്സിൽ തന്നെ, മേലധികാരമുള്ള നിയമബാധ്യത വരുമാനം മാറ്റിയാൽ അത് ഡൈവേർഷൻ ആണ്; "
        "എന്നാൽ വരുമാനം ആദ്യം സ്വന്തമായി ലഭിച്ചതിനു ശേഷം മറ്റൊരാൾക്ക് നൽകിയാൽ അത് ആപ്ലിക്കേഷൻ മാത്രമാണ്. "
        "... ... "
        "ഇവിടെ സമയം വളരെ നിർണ്ണായകമാണ്! ഒബ്ലിഗേഷൻ എപ്പോൾ പ്രവർത്തിക്കുന്നു എന്നതാണ് ഏറ്റവും പ്രധാനപ്പെട്ട ടെസ്റ്റ്. "
        "വരുമാനം അസസ്സീയുടെ സ്വന്തം പോക്കറ്റിൽ ആദ്യം വന്നുചേരുന്നുണ്ടോ എന്ന് നമ്മൾ പരിശോധിക്കണം."
    ),
    "branch2": (
        "രണ്ടാമതായി, ഓവർറൈഡിംഗ് ടൈറ്റിൽ എന്താണെന്ന് മനസ്സിലാക്കാം. വരുമാനം ഉണ്ടാകുന്നതിന് മുൻപ് തന്നെ, "
        "നിയമപരമായി നിർബന്ധിതമായ ബാധ്യത വരുമാനത്തിന്റെ സോഴ്സുമായി ബന്ധിപ്പിച്ചിരിക്കണം. "
        "അങ്ങനെ വരുമ്പോൾ, വരുമാനം അസസ്സീക്ക് ലഭിക്കുന്നതിന് മുൻപേ തന്നെ അത് വഴിതിരിച്ചു വിടപ്പെടുന്നു. "
        "... ... "
        "ശ്രദ്ധിക്കുക! ഒരു പേയ്മെന്റിനെ ചാർജ് എന്ന് വിളിച്ചതുകൊണ്ട് മാത്രം അത് ഡൈവേർഷൻ ആകില്ല. "
        "കരാറിന്റെ സ്വഭാവം, നിയമപരമായ സാധുത, സോഴ്സുമായുള്ള ബന്ധം എന്നിവ കൃത്യമായി പരിശോധിച്ചാൽ മാത്രമേ യഥാർത്ഥ നിയമ സ്വഭാവം മനസ്സിലാകൂ."
    ),
    "branch3": (
        "മൂന്നാമതായി, ആപ്ലിക്കേഷൻ ഓഫ് ഇൻകം എന്താണെന്ന് നോക്കാം. ഇവിടെ വരുമാനം ആദ്യം അസസ്സീക്ക് നിയമപരമായി ലഭ്യമാകുന്നു, "
        "അല്ലെങ്കിൽ അസസ്സീയുടെ പൂർണ്ണ നിയന്ത്രണത്തിൽ എത്തുന്നു. "
        "അതിനുശേഷം ആ വരുമാനത്തിൽ നിന്നും പണം ചെലവഴിക്കുന്നത് വെറും ആപ്ലിക്കേഷൻ മാത്രമാണ്. "
        "... ... "
        "നമ്മൾ ഓർക്കേണ്ട ഒരു പ്രധാന കാര്യമുണ്ട്: വരുമാനം ലഭിച്ച ശേഷം കുടുംബാംഗങ്ങൾക്ക് നൽകുന്ന പണമോ ഗിഫ്റ്റോ വരുമാനത്തെ നികുതിയിൽ നിന്ന് ഒഴിവാക്കില്ല. "
        "നിയമപരമായ പ്രത്യേക ഡിഡക്ഷൻ ഉണ്ടെങ്കിൽ മാത്രമേ ഇതിന് നികുതിയിളവ് ലഭിക്കൂ."
    ),
    "branch4": (
        "നാലാമതായി, ഇവയുടെ നികുതി അനന്തരഫലങ്ങൾ എന്താണെന്ന് പരിശോധിക്കാം. യഥാർത്ഥ ഡൈവേർഷൻ ആണെങ്കിൽ, "
        "ആ വരുമാനം അസസ്സീയുടെ വരുമാനമല്ല, അതിനാൽ അത് നികുതിവിധേയമല്ല. "
        "എന്നാൽ ആപ്ലിക്കേഷൻ ആണെങ്കിൽ, മുഴുവൻ തുകയ്ക്കും അസസ്സീ നികുതി നൽകേണ്ടതുണ്ട്. "
        "... ... "
        "അവസാനമായി പരീക്ഷയ്ക്ക് ഓർക്കാൻ ഒരു ലളിതമായ റൂൾ: അസസ്സീക്ക് ലഭിക്കുന്നതിന് മുൻപ് സോഴ്സിൽ നിന്ന് വരുമാനം വഴിമാറിയോ? "
        "ഇല്ല, ആദ്യം അസസ്സീക്കാണ് ലഭിച്ചതെങ്കിൽ, സംശയമില്ല, അത് ആപ്ലിക്കേഷൻ ഓഫ് ഇൻകം തന്നെയാണ്."
    )
}

def generate_pcm(client, text, tag):
    print(f"Synthesizing {tag} with Gemini Voice ({VOICE_NAME})...", flush=True)
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
        raise RuntimeError(f"No audio returned for {tag}: {resp}")
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_path = os.path.join(TEMP_DIR, f"{tag}.wav")
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(BYTES_PER_SAMPLE)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    print(f"  -> Generated {tag}: {len(pcm)} bytes PCM -> {wav_path}", flush=True)
    return AudioSegment.from_wav(wav_path)

def split_branch_audio(audio_seg, tag):
    # Detect silence in milliseconds
    silences = detect_silence(audio_seg, min_silence_len=250, silence_thresh=-35)
    print(f"  [{tag}] Detected {len(silences)} silences: {silences}")
    
    mid = len(audio_seg) // 2
    best_split = None
    if silences:
        # find the silence closest to the middle
        best_split = min(silences, key=lambda s: abs((s[0] + s[1]) // 2 - mid))
    
    if best_split:
        p1 = audio_seg[:best_split[0]]
        p2 = audio_seg[best_split[1]:]
    else:
        # Fallback: 50% split
        p1 = audio_seg[:mid]
        p2 = audio_seg[mid:]
        
    return p1, p2

def main():
    print("=== SYNTHESIZING EXPRESSIVE TRANSITION-SYNCED GEMINI VOICE FOR Q1 ===")
    
    # Use Key 3 which has fresh quota
    client = genai.Client(api_key=rotator.keys[2])
    
    # 1. Synthesize all 5 clips
    raw_clips = {}
    for key in ["intro", "branch1", "branch2", "branch3", "branch4"]:
        raw_clips[key] = generate_pcm(client, SCRIPTS[key], key)
        time.sleep(1.5)
        
    # 2. Split branches into Point 1 and Point 2
    points_audio = {}
    points_audio["intro"] = raw_clips["intro"]
    for bi in range(1, 5):
        b_key = f"branch{bi}"
        p1, p2 = split_branch_audio(raw_clips[b_key], b_key)
        points_audio[f"b{bi}_p1"] = p1
        points_audio[f"b{bi}_p2"] = p2
        
    # 3. Assemble with exact deliberate transition silences
    INTER_POINT_SILENCE_MS = 800    # 800ms silence between points
    INTER_BRANCH_SILENCE_MS = 1500  # 1500ms silence between branches for smooth UI transition
    
    assembled = AudioSegment.empty()
    timestamps = {}
    
    # Intro
    intro_start_s = 0.0
    intro_dur_s = round(len(points_audio["intro"]) / 1000.0, 2)
    intro_end_s = round(intro_start_s + intro_dur_s, 2)
    timestamps["intro"] = {"t0": intro_start_s, "t1": intro_end_s}
    
    assembled += points_audio["intro"]
    assembled += AudioSegment.silent(duration=INTER_BRANCH_SILENCE_MS)
    
    current_ms = len(assembled)
    
    for bi in range(1, 5):
        b_start_s = round(current_ms / 1000.0, 2)
        
        # Point 1
        p1_audio = points_audio[f"b{bi}_p1"]
        p1_t0 = round(current_ms / 1000.0, 2)
        p1_dur_s = round(len(p1_audio) / 1000.0, 2)
        p1_t1 = round(p1_t0 + p1_dur_s, 2)
        timestamps[f"b{bi}_p1"] = {"t0": p1_t0, "t1": p1_t1}
        
        assembled += p1_audio
        assembled += AudioSegment.silent(duration=INTER_POINT_SILENCE_MS)
        current_ms = len(assembled)
        
        # Point 2
        p2_audio = points_audio[f"b{bi}_p2"]
        p2_t0 = round(current_ms / 1000.0, 2)
        p2_dur_s = round(len(p2_audio) / 1000.0, 2)
        p2_t1 = round(p2_t0 + p2_dur_s, 2)
        timestamps[f"b{bi}_p2"] = {"t0": p2_t0, "t1": p2_t1}
        
        assembled += p2_audio
        
        b_end_s = p2_t1
        timestamps[f"branch{bi}"] = {"t0": b_start_s, "t1": b_end_s}
        
        if bi < 4:
            assembled += AudioSegment.silent(duration=INTER_BRANCH_SILENCE_MS)
            current_ms = len(assembled)
        else:
            assembled += AudioSegment.silent(duration=1000) # 1s outro
            current_ms = len(assembled)
            
    total_dur_s = round(len(assembled) / 1000.0, 2)
    print(f"\nFinal Assembled Duration: {total_dur_s}s")
    print("Timestamps Map:")
    for k, v in timestamps.items():
        print(f"  {k}: {v['t0']}s - {v['t1']}s")
        
    # 4. Export high quality MP3
    final_mp3_path = os.path.join(AUDIO_DIR, "q1.mp3")
    old_mp3_path = os.path.join(AUDIO_DIR, "q1_gtts_backup.mp3")
    if os.path.exists(final_mp3_path) and not os.path.exists(old_mp3_path):
        import shutil
        shutil.copy2(final_mp3_path, old_mp3_path)
        print(f"Backed up old audio to {old_mp3_path}")
        
    temp_stitched_wav = os.path.join(TEMP_DIR, "q1_final_stitched.wav")
    assembled.export(temp_stitched_wav, format="wav")
    
    subprocess.run([
        "ffmpeg", "-y", "-i", temp_stitched_wav,
        "-b:a", "192k",
        "-ar", "24000",
        final_mp3_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Successfully generated studio MP3: {final_mp3_path}")
    
    # 5. Update mindmaps.json
    with open(MINDMAP_PATH, "r", encoding="utf-8") as f:
        mindmaps = json.load(f)
    q1_mm = mindmaps.get("q1")
    if q1_mm:
        if "root" in q1_mm:
            q1_mm["root"]["t0"] = timestamps["intro"]["t0"]
            q1_mm["root"]["t1"] = timestamps["intro"]["t1"]
            
        for bi, branch in enumerate(q1_mm.get("branches", [])):
            b_key = f"branch{bi+1}"
            if b_key in timestamps:
                branch["t0"] = timestamps[b_key]["t0"]
                branch["t1"] = timestamps[b_key]["t1"]
            points = branch.get("points", [])
            for pi, pt in enumerate(points):
                p_key = f"b{bi+1}_p{pi+1}"
                if p_key in timestamps:
                    pt["t0"] = timestamps[p_key]["t0"]
                    pt["t1"] = timestamps[p_key]["t1"]
                    pt["spoken"] = True
                    
        q1_mm["total_duration"] = total_dur_s
        with open(MINDMAP_PATH, "w", encoding="utf-8") as f:
            json.dump(mindmaps, f, indent=2, ensure_ascii=False)
        print("Updated data/mindmaps.json with sample-accurate transition timestamps!")
        
    # 6. Update provisions.json
    with open(PROVISIONS_PATH, "r", encoding="utf-8") as f:
        provisions = json.load(f)
    for p in provisions:
        if p.get("question_number") == 1:
            p["dur"] = total_dur_s
            p["duration_seconds"] = total_dur_s
            p["voice"] = f"Gemini Voice ({VOICE_NAME})"
            p["voice_engine"] = f"Gemini Voice ({VOICE_NAME})"
            p["audio_file"] = "q1.mp3"
    with open(PROVISIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(provisions, f, indent=2, ensure_ascii=False)
    print("Updated data/provisions.json!")
    
    # 7. Update frontend/index.html embedded snapshot
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    import re
    m = re.search(r'(<script type="application/json" id="pipeline-data">)([\s\S]+?)(</script>)', html)
    if m:
        try:
            pipe_data = json.loads(m.group(2))
            if "mindmaps" in pipe_data and "q1" in pipe_data["mindmaps"]:
                pipe_data["mindmaps"]["q1"] = q1_mm
            if "provisions" in pipe_data:
                for p in pipe_data["provisions"]:
                    if p.get("question_number") == 1:
                        p["dur"] = total_dur_s
                        p["duration_seconds"] = total_dur_s
                        p["voice"] = f"Gemini Voice ({VOICE_NAME})"
                        p["audio_file"] = "q1.mp3"
            new_json = json.dumps(pipe_data, ensure_ascii=False)
            html = html[:m.start(2)] + new_json + html[m.end(2):]
            with open(INDEX_PATH, "w", encoding="utf-8") as f:
                f.write(html)
            print("Updated frontend/index.html embedded snapshot!")
        except Exception as e:
            print("Error updating index.html:", e)

if __name__ == "__main__":
    main()
