import os
import sys
import json
import wave
import subprocess
import time
import base64
import io
import hashlib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import rotator

DEFAULT_VOICE = os.getenv("GEMINI_TTS_VOICE", "Kore")
TTS_STYLE = (
    "A calm, confident Indian tax teacher explaining a provision naturally. "
    "Speak Malayalam passages in Malayalam. Speak English legal keywords, "
    "statutory section references, acronyms, amounts, percentages, numerals, "
    "and years clearly in English. Keep a steady conversational pace and read "
    "the supplied transcript verbatim."
)
TTS_MODEL = os.getenv("GEMINI_TTS_MODEL", "gemini-3.8-flash-lite-tts")
AUDIO_DIR = os.path.join(PROJECT_ROOT, 'data', 'audio')
TEMP_DIR = os.path.join(PROJECT_ROOT, 'data', 'audio_temp')
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def generate_slide_audio_pcm(script_text, voice_name=None):
    """
    Calls Gemini Voice TTS and converts its WAV response to 24kHz 16-bit mono PCM.
    No alternate TTS provider is used, so the configured Gemini voice stays consistent.
    """
    if not voice_name:
        voice_name = DEFAULT_VOICE
    
    max_attempts = len(rotator.keys)
    if not max_attempts:
        raise RuntimeError("No Gemini API key configured for voice generation")

    for attempt in range(max_attempts):
        client = rotator.get_client(timeout_ms=30000)
        try:
            if TTS_MODEL.startswith("gemini-3.8-"):
                tts_input = [{
                    "type": "user_input",
                    "content": [{
                        "type": "text",
                        "text": script_text,
                        "annotations": [{
                            "type": "speech_metadata",
                            "style": TTS_STYLE,
                        }],
                    }],
                }]
            else:
                tts_input = script_text
            resp = client.interactions.create(
                model=TTS_MODEL,
                input=tts_input,
                response_format={"type": "audio"},
                generation_config={"speech_config": [{"voice": voice_name}]},
            )
            audio = getattr(resp, "output_audio", None)
            encoded = getattr(audio, "data", None) if audio else None
            if not encoded:
                raise RuntimeError("Gemini returned no audio data")
            wav_data = base64.b64decode(encoded)
            mime_type = str(getattr(audio, "mime_type", "") or "")
            if wav_data[:4] != b"RIFF" and "audio/l16" in mime_type:
                return wav_data
            with wave.open(io.BytesIO(wav_data), "rb") as source:
                pcm_data = source.readframes(source.getnframes())
                input_rate = source.getframerate()
                input_channels = source.getnchannels()
                input_width = source.getsampwidth()
            if input_rate == 24000 and input_channels == 1 and input_width == 2:
                return pcm_data
            converted = subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "wav", "-i", "pipe:0", "-ar", "24000", "-ac", "1", "-f", "s16le", "pipe:1"],
                input=wav_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            return converted.stdout
        except Exception as e:
            err = str(e).replace("\n", " ")[:180]
            print(f"Gemini TTS {TTS_MODEL} attempt {attempt+1}/{max_attempts}: {err}", flush=True)
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                time.sleep(4)
            elif "connection" in str(e).lower() or "10065" in str(e) or "11001" in str(e):
                time.sleep(5)
            else:
                time.sleep(2)
    raise RuntimeError(f"Gemini TTS failed after {max_attempts} API-key attempt(s)")

def synthesize_topic_audio(key, topic_data):
    """
    Synthesizes audio for each slide in topic_data, calculates exact timings,
    concatenates into data/audio/{key}.mp3, and updates topic_data with exact t0 and t1 for each slide.
    """
    slides = topic_data.get('slides', [])
    if not slides:
        return None

    print(f"\n=== Synthesizing Fresh Gemini Audio for {key}: {len(slides)} slides ===")
    
    slide_wavs = []
    current_time = 0.0
    pause_duration = 0.4 # 400ms pause between slides
    
    # Generate 0.4s silence PCM (24000 samples/sec * 2 bytes/sample * 0.4 sec = 19200 bytes)
    silence_pcm = b'\x00' * int(24000 * 2 * pause_duration)

    for i, slide in enumerate(slides):
        script = slide.get('malayalam_narration', '').strip()
        if not script:
            script = "അടുത്ത ഭാഗം നമുക്ക് വിശദമായി നോക്കാം."

        slide_wav_path = os.path.join(TEMP_DIR, f"{key}_slide_{i+1}.wav")
        pcm_bytes = generate_slide_audio_pcm(script)
        
        if not pcm_bytes:
            print(f"Error: Failed to synthesize audio for {key} slide {i+1}")
            return None

        # Write WAV file
        with wave.open(slide_wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(pcm_bytes)

        duration = len(pcm_bytes) / (24000 * 2)
        slide['t0'] = round(current_time, 2)
        slide['t1'] = round(current_time + duration, 2)
        slide['duration'] = round(duration, 2)
        
        print(f"  Slide {i+1} [{slide['t0']}s - {slide['t1']}s] ({slide['duration']}s): {slide.get('slide_title')}")
        
        slide_wavs.append(slide_wav_path)
        current_time = slide['t1'] + pause_duration

    # Stitch WAV files together using FFmpeg concat filter or wave module
    final_wav_path = os.path.join(TEMP_DIR, f"{key}_full.wav")
    final_mp3_path = os.path.join(AUDIO_DIR, f"{key}.mp3")
    
    with wave.open(final_wav_path, 'wb') as out_wf:
        out_wf.setnchannels(1)
        out_wf.setsampwidth(2)
        out_wf.setframerate(24000)
        
        for idx, sw in enumerate(slide_wavs):
            with wave.open(sw, 'rb') as in_wf:
                out_wf.writeframes(in_wf.readframes(in_wf.getnframes()))
            if idx < len(slide_wavs) - 1:
                out_wf.writeframes(silence_pcm)

    # Convert to MP3
    subprocess.run([
        'ffmpeg', '-y', '-i', final_wav_path,
        '-b:a', '128k', final_mp3_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    total_duration = round(current_time - pause_duration, 2)
    topic_data['total_duration'] = total_duration
    print(f"-> Successfully created {final_mp3_path} (Total: {total_duration}s)")
    return total_duration

def main():
    force_all = '--force' in sys.argv
    specific_key = next((arg for arg in sys.argv[1:] if not arg.startswith('--')), None)

    sb_file = os.path.join(PROJECT_ROOT, 'data', 'ppt_storyboards.json')
    if not os.path.exists(sb_file):
        print(f"Storyboard file {sb_file} does not exist. Run generate_ppt_storyboards.py first.")
        return

    with open(sb_file, 'r', encoding='utf-8') as f:
        storyboards = json.load(f)

    # Update provisions metadata too
    prov_file = os.path.join(PROJECT_ROOT, 'data', 'provisions.json')
    with open(prov_file, 'r', encoding='utf-8') as f:
        provisions = json.load(f)

    for key, topic_data in storyboards.items():
        if specific_key and key != specific_key:
            continue
        if not specific_key and key in ['q1', 'q4', 'q5']:
            print(f"Skipping {key}: already synthesized with studio voice.", flush=True)
            continue
        mp3_path = os.path.join(AUDIO_DIR, f"{key}.mp3")
        if not force_all and topic_data.get('total_duration') and os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000:
            print(f"Audio for {key} already synthesized ({topic_data['total_duration']}s), skipping.")
            continue

        dur = synthesize_topic_audio(key, topic_data)
        if dur:
            combined_script = "\n\n".join([s.get('malayalam_narration', '') for s in topic_data.get('slides', [])])
            topic_data['combined_script'] = combined_script
            
            qn_str = key.replace('q', '')
            try:
                qn = int(qn_str)
            except Exception:
                qn = None
                
            for p in provisions:
                if p.get('question_number') == qn or (qn == 1 and p.get('question_number') in [1, 2, 3]) or (qn == 9 and p.get('question_number') in [9, 10]):
                    p['dur'] = dur
                    p['duration_seconds'] = dur
                    p['malayalam_audio_script'] = combined_script
                    p['audio_file'] = f"{key}.mp3"
                    p['video_file'] = f"{key}.mp4"
                    p['voice_engine'] = f"Gemini Voice ({DEFAULT_VOICE})"

            with open(sb_file, 'w', encoding='utf-8') as f:
                json.dump(storyboards, f, indent=2, ensure_ascii=False)

            with open(prov_file, 'w', encoding='utf-8') as f:
                json.dump(provisions, f, indent=2, ensure_ascii=False)
    
    print("\nAll audio synthesis and storyboard timing alignment complete!")

if __name__ == '__main__':
    main()
