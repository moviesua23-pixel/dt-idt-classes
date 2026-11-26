// -*- coding: utf-8 -*-
// static/js/audio.js
// Statutory Kinetic Studio - Voice & Speech Narration Engine
// Web Speech synthesis with ml-IN detection, fallback notice, and sentence-level synchronization.

(function() {
  class StudioAudioManager {
    constructor() {
      this.enabled = true;
      this.isMuted = false;
      this.currentUtterance = null;
      this.selectedVoice = null;
      this.hasMalayalamVoice = false;
      this.voicesLoaded = false;
      this.voiceNoticeShown = false;

      // Gemini Expressive Voice state
      this.audioElement = (typeof Audio !== "undefined") ? new Audio() : null;
      this.currentAudioUrl = null;
      this.isPlayingAudio = false;
      this.isSynthesizing = false;
      this.playbackSpeed = 1.0;
      this.activeSceneIdx = null;
      this.synthesisCache = {}; // dialogue text -> { audio_url, duration_ms }
      this.onEndedCallbacks = [];

      this.initAudioElement();
      this.initVoices();
    }

    initAudioElement() {
      if (!this.audioElement) return;
      this.audioElement.preload = "auto";

      this.audioElement.addEventListener("play", () => {
        this.isPlayingAudio = true;
      });

      this.audioElement.addEventListener("playing", () => {
        this.isPlayingAudio = true;
      });

      this.audioElement.addEventListener("ended", () => {
        this.isPlayingAudio = false;
        this.notifyVoiceEnded();
      });

      this.audioElement.addEventListener("pause", () => {
        if (this.audioElement.currentTime >= (this.audioElement.duration || 0) - 0.1) {
          this.isPlayingAudio = false;
        }
      });

      this.audioElement.addEventListener("error", (e) => {
        console.warn("[AUDIO] Gemini audio playback error:", e);
        this.isPlayingAudio = false;
        this.notifyVoiceEnded();
      });
    }

    notifyVoiceEnded() {
      const callbacks = [...this.onEndedCallbacks];
      this.onEndedCallbacks = [];
      callbacks.forEach(cb => {
        try { cb(); } catch (err) { console.error("[AUDIO] onEndedCallback error:", err); }
      });
    }

    onVoiceEnded(callback) {
      if (typeof callback === "function") {
        this.onEndedCallbacks.push(callback);
      }
    }

    isVoiceActive() {
      if (!this.enabled || this.isMuted) return false;
      if (this.isSynthesizing) return true;
      if (this.isPlayingAudio && this.audioElement && !this.audioElement.paused && !this.audioElement.ended) {
        return true;
      }
      if (this.currentUtterance !== null && typeof window !== "undefined" && window.speechSynthesis && window.speechSynthesis.speaking) {
        return true;
      }
      return false;
    }

    initVoices() {
      if (typeof window === "undefined" || !("speechSynthesis" in window)) {
        return;
      }

      const updateVoices = () => {
        const voices = window.speechSynthesis.getVoices();
        if (!voices || voices.length === 0) return;

        this.voicesLoaded = true;
        const mlVoice = voices.find(v => v.lang && (v.lang === "ml-IN" || v.lang.startsWith("ml")));
        const enInVoice = voices.find(v => v.lang && v.lang === "en-IN");
        const enVoice = voices.find(v => v.lang && v.lang.startsWith("en"));

        if (mlVoice) {
          this.selectedVoice = mlVoice;
          this.hasMalayalamVoice = true;
          this.hideVoiceNotice();
        } else {
          this.selectedVoice = enInVoice || enVoice || voices[0];
          this.hasMalayalamVoice = false;
          // Only show notice if not using Gemini Expressive Voice
          if (!this.isPlayingAudio && !this.currentAudioUrl) {
            this.showVoiceNotice();
          }
        }
      };

      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = updateVoices;
      }
      updateVoices();
    }

    showVoiceNotice() {
      if (this.voiceNoticeShown) return;
      this.voiceNoticeShown = true;

      let banner = document.getElementById("voice_notice_banner");
      if (!banner) {
        banner = document.createElement("div");
        banner.id = "voice_notice_banner";
        banner.style.cssText = `
          display: flex;
          align-items: center;
          justify-content: space-between;
          background: #EFF6FF;
          border: 1px solid #BFDBFE;
          border-left: 4px solid #3B82F6;
          border-radius: 6px;
          padding: 8px 14px;
          margin: 8px 0;
          font-family: 'Plus Jakarta Sans', sans-serif;
          font-size: 12px;
          font-weight: 600;
          color: #1E40AF;
        `;
        const canvasWrapper = document.querySelector(".canvas-wrapper");
        if (canvasWrapper && canvasWrapper.parentNode) {
          canvasWrapper.parentNode.insertBefore(banner, canvasWrapper);
        }
      }

      banner.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:14px;">🎙️</span>
          <span><strong>Gemini Expressive Voice (Aoede):</strong> High-fidelity neural voice enabled. (Web Speech en-IN fallback available).</span>
        </div>
        <button onclick="this.parentElement.style.display='none'" style="background:none; border:none; color:#1E40AF; font-size:14px; cursor:pointer; padding:0 4px;" title="Dismiss">✕</button>
      `;
      banner.style.display = "flex";
    }

    hideVoiceNotice() {
      const banner = document.getElementById("voice_notice_banner");
      if (banner) banner.style.display = "none";
    }

    /**
     * Plays Gemini Expressive Neural Audio for a given slide/scene.
     * Fetches on-demand from /api/synthesize_voice if not already generated.
     */
    playSceneVoice(scene, sceneIdx = 0, onEnd = null) {
      if (!this.enabled || this.isMuted) return;
      if (onEnd) this.onVoiceEnded(onEnd);

      this.stop();
      this.activeSceneIdx = sceneIdx;

      if (!scene) return;
      const dialogue = (scene.dialogue || scene.story_narration || (scene.lines && scene.lines.map(l => l.sentence).join(" ")) || "").trim();
      if (!dialogue) return;

      // Check if scene has an explicit audio_url
      if (scene.audio_url) {
        this.playAudioUrl(scene.audio_url);
        return;
      }

      // Check in-memory synthesis cache
      if (this.synthesisCache[dialogue]) {
        const cached = this.synthesisCache[dialogue];
        scene.audio_url = cached.audio_url;
        scene.duration_ms = cached.duration_ms;
        this.playAudioUrl(cached.audio_url);
        return;
      }

      // Request on-demand synthesis from server
      if (window.location.protocol === "file:") {
        this.speakSentence(dialogue, { onEnd: () => this.notifyVoiceEnded() });
        return;
      }
      this.isSynthesizing = true;
      fetch("/api/synthesize_voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dialogue: dialogue,
          voice: "Aoede",
          scene_idx: sceneIdx
        })
      })
      .then(res => res.json())
      .then(data => {
        this.isSynthesizing = false;
        if (data && data.audio_url) {
          this.synthesisCache[dialogue] = data;
          scene.audio_url = data.audio_url;
          if (data.duration_ms) scene.duration_ms = data.duration_ms;

          // Update timeline duration if still on this scene
          if (window.PRESENTATION_PLAYER && window.PRESENTATION_PLAYER.currentSlideIdx === sceneIdx) {
            window.PRESENTATION_PLAYER.updateSlideTimeline();
            if (window.PRESENTATION_PLAYER.isPlaying) {
              this.playAudioUrl(data.audio_url);
            }
          }
        } else {
          this.speakSentence(dialogue, { onEnd: () => this.notifyVoiceEnded() });
        }
      })
      .catch(err => {
        this.isSynthesizing = false;
        console.warn("[AUDIO] Gemini voice synthesis error, using WebSpeech fallback:", err);
        this.speakSentence(dialogue, { onEnd: () => this.notifyVoiceEnded() });
      });
    }

    playAudioUrl(url) {
      if (!this.audioElement || this.isMuted) return;
      try {
        this.currentAudioUrl = url;
        this.audioElement.src = url;
        this.audioElement.playbackRate = this.playbackSpeed;
        this.audioElement.currentTime = 0;
        this.isPlayingAudio = true;
        this.audioElement.play().catch(e => {
          console.warn("[AUDIO] Audio element play error:", e);
        });
      } catch (err) {
        console.error("[AUDIO] playAudioUrl error:", err);
      }
    }

    seekVoice(timeMs) {
      if (this.audioElement && this.currentAudioUrl) {
        try {
          this.audioElement.currentTime = Math.max(0, timeMs / 1000);
        } catch (e) {
          // ignore seek error
        }
      }
    }

    setPlaybackRate(speed) {
      this.playbackSpeed = parseFloat(speed) || 1.0;
      if (this.audioElement) {
        this.audioElement.playbackRate = this.playbackSpeed;
      }
    }

    pause() {
      if (this.audioElement && this.isPlayingAudio) {
        this.audioElement.pause();
      }
      if (typeof window !== "undefined" && window.speechSynthesis) {
        window.speechSynthesis.pause();
      }
    }

    resume() {
      if (this.isMuted) return;
      if (this.audioElement && this.currentAudioUrl && this.isPlayingAudio) {
        this.audioElement.play().catch(() => {});
      }
      if (typeof window !== "undefined" && window.speechSynthesis && window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }
    }

    speakSentence(text, options = {}) {
      if (!this.enabled || this.isMuted) return;
      if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
      if (!text || !text.trim()) return;

      this.stop();

      const utterance = new SpeechSynthesisUtterance(text.trim());
      utterance.voice = this.selectedVoice;
      utterance.lang = this.hasMalayalamVoice ? "ml-IN" : "en-IN";
      utterance.rate = options.rate || this.playbackSpeed;
      utterance.pitch = options.pitch || 1.0;

      utterance.onend = () => {
        this.currentUtterance = null;
        if (options.onEnd) options.onEnd();
        this.notifyVoiceEnded();
      };

      utterance.onerror = (e) => {
        console.warn("[AUDIO] Speech synthesis warning:", e.error);
        this.currentUtterance = null;
        if (options.onEnd) options.onEnd();
        this.notifyVoiceEnded();
      };

      this.currentUtterance = utterance;
      window.speechSynthesis.speak(utterance);
    }

    stop() {
      if (this.audioElement) {
        try {
          this.audioElement.pause();
          this.audioElement.currentTime = 0;
        } catch (e) {}
      }
      this.isPlayingAudio = false;
      this.isSynthesizing = false;

      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      this.currentUtterance = null;
    }

    toggleMute() {
      this.isMuted = !this.isMuted;
      if (this.isMuted) {
        this.stop();
      }
      return this.isMuted;
    }

    setMuted(muted) {
      this.isMuted = !!muted;
      if (this.isMuted) {
        this.stop();
      }
    }
  }

  // Expose singleton to window
  window.AUDIO_MANAGER = new StudioAudioManager();
})();
