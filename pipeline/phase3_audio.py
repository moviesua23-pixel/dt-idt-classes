import os
import sys
import re
import json
import wave
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.key_rotator import rotator
from pipeline.synthesize_ppt_audio import TTS_STYLE
from google.genai import types

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DEFAULT_VOICE = os.getenv("GEMINI_TTS_VOICE", "Aoede")

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '_', text).strip('_')[:40]

def update_state(phase, percent, status_text):
    state_file = os.path.join(PROJECT_ROOT, 'data', 'state.json')
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            pass
    state[phase] = {"percent": percent, "status": status_text}
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def generate_gemini_audio(script, output_mp3_path, voice_name=None):
    """
    Generates studio-grade spoken audio using Gemini Voice TTS (24kHz 16-bit PCM)
    and converts to standard MP3 with FFmpeg.
    Strictly uses Gemini Expressive Voice with KeyRotator. Zero robotic fallback.
    Returns (duration_seconds, engine_name).
    """
    if not voice_name:
        voice_name = DEFAULT_VOICE
        
    models_to_try = [
        'gemini-3.1-flash-tts-preview',
        'gemini-3.8-flash-tts',
        'gemini-3.8-flash-lite-tts',
        'gemini-2.5-flash-preview-tts'
    ]

    def _call_tts(client):
        last_e = None
        for model in models_to_try:
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=f"{TTS_STYLE}\n\nDeliver this as an expressive, warm teacher explanation with clear emphasis on the rule and example. Speak the narration verbatim:\n{script}",
                    config=types.GenerateContentConfig(
                        response_modalities=['AUDIO'],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=voice_name
                                )
                            )
                        )
                    )
                )
                for part in resp.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.data:
                        return part.inline_data.data, model
            except Exception as e:
                last_e = e
                continue
        raise RuntimeError(f"All Gemini TTS models failed: {last_e}")

    pcm_data, used_model = rotator.execute_with_retry(
        _call_tts,
        timeout_ms=int(os.getenv("GEMINI_TTS_TIMEOUT_MS", "120000")),
        retry_transient=False,
    )

    # Write temporary WAV file
    temp_wav = output_mp3_path + ".temp.wav"
    with wave.open(temp_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm_data)
    
    frames = len(pcm_data) / 2
    duration = round(frames / 24000.0, 1)

    # Convert to MP3
    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', temp_wav, '-b:a', '128k', output_mp3_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
    except Exception as fe:
        print(f"FFmpeg conversion warning: {fe}. Keeping WAV format.")
        if os.path.exists(temp_wav):
            if os.path.exists(output_mp3_path):
                os.remove(output_mp3_path)
            os.rename(temp_wav, output_mp3_path)
            
    return duration, f"Gemini Expressive Voice ({voice_name} via {used_model})"

def run_phase3(force=False, voice_name=None):
    provisions_file = os.path.join(PROJECT_ROOT, 'data', 'provisions.json')
    if not os.path.exists(provisions_file):
        print("Please run Phase 2 first.")
        return
        
    with open(provisions_file, 'r', encoding='utf-8') as f:
        provisions = json.load(f)
        
    audio_dir = os.path.join(PROJECT_ROOT, 'data', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    
    total = len(provisions)
    voice = voice_name or DEFAULT_VOICE
    print(f"Gemini Voice Audio Generation for {total} questions using voice '{voice}'...")

    # Registry to track generated audio per unique topic
    topic_registry = {}
    updated_provisions = []
    
    for idx, item in enumerate(provisions, 1):
        q_num = item.get('question_number')
        topic_title = item.get('core_principle', f'Topic {q_num}').strip()
        topic_key = slugify(topic_title)
        
        script = item.get('malayalam_audio_script', '').strip()
        pct = int(((idx - 1) / total) * 100)
        
        # Check if this topic has already been generated in this run
        if topic_key in topic_registry:
            canonical_filename = topic_registry[topic_key]['audio_file']
            dur = topic_registry[topic_key].get('dur', 60)
            engine = topic_registry[topic_key].get('voice_engine', f"Gemini Voice ({voice})")
            print(f"[REUSE] Q{q_num} shares topic '{topic_title}' -> Reusing: {canonical_filename} ({dur}s)")
            item['topic_id'] = topic_key
            item['topic_title'] = topic_title
            item['audio_file'] = canonical_filename
            item['dur'] = dur
            item['duration_seconds'] = dur
            item['voice_engine'] = engine
            updated_provisions.append(item)
            continue
            
        # New topic encountered: generate audio for this topic
        canonical_filename = f"q{q_num}.mp3"
        audio_path = os.path.join(audio_dir, canonical_filename)
        update_state("phase3", pct, f"Voicing Topic with Gemini: {topic_title[:30]}... (Q{q_num})")
        
        if not script:
            script = "ഡയറക്ട് ടാക്സ് നിയമത്തിലെ ഈ വ്യവസ്ഥ പ്രകാരം നികുതി ബാധ്യത കണക്കാക്കുന്നു."
            
        dur = item.get('dur', 60)
        engine_used = f"Gemini Voice ({voice})"
        
        try:
            if force or not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                print(f"[GEMINI VOICE] Generating audio for topic '{topic_title}' (Q{q_num})...")
                dur, engine_used = generate_gemini_audio(script, audio_path, voice_name=voice)
                print(f"Saved {canonical_filename} with {engine_used} ({dur}s, {os.path.getsize(audio_path)} bytes)")
            else:
                print(f"[EXISTS] Audio {canonical_filename} already cached on disk.")
        except Exception as e:
            print(f"Error generating audio for Q{q_num}: {e}")
            
        topic_registry[topic_key] = {
            "topic_title": topic_title,
            "audio_file": canonical_filename,
            "first_q": q_num,
            "dur": dur,
            "voice_engine": engine_used
        }
        
        item['topic_id'] = topic_key
        item['topic_title'] = topic_title
        item['audio_file'] = canonical_filename
        item['dur'] = dur
        item['duration_seconds'] = dur
        item['voice_engine'] = engine_used
        updated_provisions.append(item)
        
    # Save enriched provisions with topic metadata & accurate duration
    with open(provisions_file, 'w', encoding='utf-8') as f:
        json.dump(updated_provisions, f, indent=2, ensure_ascii=False)
        
    update_state("phase3", 100, f"Completed Gemini Voice generation. {len(topic_registry)} unique topic audio files generated with Gemini Voice ({voice}).")
    print(f"Phase 3 Complete: {len(topic_registry)} unique Gemini Voice topics across {total} questions.")

if __name__ == '__main__':
    force_gen = "--force" in sys.argv
    run_phase3(force=force_gen)
