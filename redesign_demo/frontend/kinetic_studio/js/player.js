// -*- coding: utf-8 -*-
// static/js/player.js
// Statutory Kinetic Studio - Broadcast-Quality Master Clock & Presentation Player
// HiDPI with devicePixelRatio & ResizeObserver, deterministic renderFrame(slideIdx, timeMs),
// WebM export, PNG snapshot, and keyboard accessibility.

(function() {
  const LOGICAL_WIDTH = 1280;
  const LOGICAL_HEIGHT = 720;
  const DEFAULT_LINE_DURATION_MS = 5400;
  const SLIDE_CROSSFADE_MS = 400;

  class PresentationPlayer {
    constructor() {
      this.canvas = null;
      this.ctx = null;
      this.data = null;
      this.currentSlideIdx = 0;
      this.currentTimeMs = 0;
      this.isPlaying = false;
      this.playbackSpeed = 1.0;
      this.lastTimestamp = performance.now();
      this.animationFrameId = null;
      this.sceneGraph = new window.KeyedActorSceneGraph();
      this.lastRenderedSlideIdx = null;
      this.resizeObserver = null;
      this.isExporting = false;

      // Scrubber & voice gating tracking
      this.isScrubbing = false;
      this.isWaitingForVoice = false;
      this.settleHoldRemainingMs = 0;
      this.spokenActorVoices = new Set();

      // Bound methods
      this.loop = this.loop.bind(this);
      this.handleResize = this.handleResize.bind(this);
    }

    init(canvasId = "stage_canvas") {
      this.canvas = document.getElementById(canvasId);
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext("2d");

      // Setup HiDPI & ResizeObserver
      this.setupHiDPI();
      this.setupKeyboard();
      this.setupScrubber();

      // Ensure fonts are loaded before first frame
      if (window.THEME) {
        window.THEME.ensureFontsLoaded().then(() => {
          this.render();
        });
      }
    }

    /**
     * Requirement 4: HiDPI backing store scaling via devicePixelRatio & ResizeObserver
     */
    setupHiDPI() {
      if (!this.canvas) return;

      const resize = () => {
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        const displayWidth = rect.width || 1080;
        const displayHeight = rect.height || (displayWidth * 9 / 16);

        // Scale backing store
        this.canvas.width = Math.round(displayWidth * dpr);
        this.canvas.height = Math.round(displayHeight * dpr);

        // Reset transform and scale to logical 1280x720 space
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        this.ctx.scale(
          (this.canvas.width / LOGICAL_WIDTH),
          (this.canvas.height / LOGICAL_HEIGHT)
        );

        // Re-render current frame
        this.render();
      };

      if (window.ResizeObserver) {
        this.resizeObserver = new ResizeObserver(() => resize());
        this.resizeObserver.observe(this.canvas);
      } else {
        window.addEventListener("resize", resize);
      }

      resize();
    }

    handleResize() {
      this.setupHiDPI();
    }

    setupKeyboard() {
      window.addEventListener("keydown", (e) => {
        if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")) return;

        if (e.code === "Space") {
          e.preventDefault();
          this.togglePlay();
        } else if (e.code === "ArrowRight") {
          e.preventDefault();
          this.nextSlide();
        } else if (e.code === "ArrowLeft") {
          e.preventDefault();
          this.prevSlide();
        } else if (e.code === "KeyR") {
          e.preventDefault();
          this.seekTo(0);
        } else if (e.code === "KeyM") {
          e.preventDefault();
          this.toggleVoice();
        }
      });
    }

    setupScrubber() {
      const slider = document.getElementById("anim_timeline_slider");
      if (!slider) return;

      slider.addEventListener("mousedown", () => { this.isScrubbing = true; });
      slider.addEventListener("touchstart", () => { this.isScrubbing = true; });
      slider.addEventListener("mouseup", () => { this.isScrubbing = false; });
      slider.addEventListener("touchend", () => { this.isScrubbing = false; });
      slider.addEventListener("input", (e) => {
        this.seekTo(parseFloat(e.target.value));
      });
    }

    loadPresentation(data) {
      this.data = data;
      this.currentSlideIdx = 0;
      this.currentTimeMs = 0;
      this.isPlaying = true;
      this.isWaitingForVoice = false;
      this.settleHoldRemainingMs = 0;
      this.lastTimestamp = performance.now();
      this.sceneGraph.reset();

      this.renderTabs();
      this.updatePlayBtnState();
      this.updateSlideTimeline();

      // Trigger Gemini Expressive Voice for the first scene (if not using sequential actor voices)
      if (window.AUDIO_MANAGER) {
        const slide = this.getCurrentSlide();
        const payload = slide?.lines && slide.lines[0]?.action_payload;
        const voiceCues = payload?.voiceCues || [];
        const actors = payload?.actors || [];
        const hasPerActorDialogue = voiceCues.length > 0 || actors.some(a => a.dialogue);
        if (!hasPerActorDialogue) {
          window.AUDIO_MANAGER.playSceneVoice(slide, 0);
        }
      }

      if (!this.animationFrameId) {
        this.lastTimestamp = performance.now();
        this.animationFrameId = requestAnimationFrame(this.loop);
      }
    }

    loop(timestamp) {
      if (!this.lastTimestamp) this.lastTimestamp = timestamp;
      const deltaMs = (timestamp - this.lastTimestamp) * this.playbackSpeed;
      this.lastTimestamp = timestamp;

      if (this.isPlaying && !this.isScrubbing && this.data) {
        const slide = this.getCurrentSlide();
        const maxMs = this.getSlideDurationMs(slide);
        const voiceActive = window.AUDIO_MANAGER ? window.AUDIO_MANAGER.isVoiceActive() : false;
        const payload = slide?.lines && slide.lines[0]?.action_payload;
        const actors = payload?.actors || [];
        const voiceCues = payload?.voiceCues || [];
        const hasPerActorDialogue = voiceCues.length > 0 || actors.some(a => a.dialogue);

        if (this.currentTimeMs < maxMs) {
          // Voice gating between sequential shapes & sub-elements in this slide:
          // Find next unspawned cue or actor whose startMs > currentTimeMs
          let nextSpawnMs = null;
          if (voiceCues.length > 0) {
            const nextCue = voiceCues.find(c => (c.startMs !== undefined && c.startMs > this.currentTimeMs));
            if (nextCue) nextSpawnMs = nextCue.startMs;
          } else {
            const nextActor = actors.find(a => (a.startMs !== undefined && a.startMs > this.currentTimeMs));
            if (nextActor) nextSpawnMs = nextActor.startMs;
          }

          if (voiceActive && nextSpawnMs !== null && this.currentTimeMs >= Math.max(0, nextSpawnMs - 40)) {
            // Previous shape/element's voice is STILL SPEAKING!
            // Hold currentTimeMs right before nextSpawnMs so next element NEVER appears until previous voice finishes!
            this.currentTimeMs = Math.max(0, nextSpawnMs - 40);
            this.isWaitingForVoice = true;
          } else {
            const outroHoldThreshold = Math.max(0, maxMs - 500);
            if (voiceActive && this.currentTimeMs >= outroHoldThreshold) {
              this.currentTimeMs = outroHoldThreshold;
              this.isWaitingForVoice = true;
            } else {
              this.currentTimeMs += deltaMs;
              if (this.currentTimeMs >= maxMs) {
                this.currentTimeMs = maxMs;
                if (voiceActive) {
                  this.isWaitingForVoice = true;
                  this.currentTimeMs = outroHoldThreshold;
                } else {
                  this.settleHoldRemainingMs = 400;
                }
              }
            }
          }

          // Trigger sequential voice for any voice cue or actor that has reached its startMs
          if (hasPerActorDialogue && !this.isScrubbing) {
            if (voiceCues.length > 0) {
              voiceCues.forEach(cue => {
                if (cue.dialogue && this.currentTimeMs >= (cue.startMs || 0)) {
                  const key = `${this.currentSlideIdx}_${cue.id}`;
                  if (!this.spokenActorVoices.has(key)) {
                    this.spokenActorVoices.add(key);
                    if (window.AUDIO_MANAGER) {
                      window.AUDIO_MANAGER.speakSentence(cue.dialogue);
                    }
                  }
                }
              });
            } else {
              actors.forEach((a, aIdx) => {
                if (a.dialogue && this.currentTimeMs >= (a.startMs || 0)) {
                  const key = `${this.currentSlideIdx}_${aIdx}`;
                  if (!this.spokenActorVoices.has(key)) {
                    this.spokenActorVoices.add(key);
                    if (window.AUDIO_MANAGER) {
                      window.AUDIO_MANAGER.speakSentence(a.dialogue);
                    }
                  }
                }
              });
            }
          }
        } else {
          // At or past nominal maxMs
          if (voiceActive) {
            this.isWaitingForVoice = true;
            this.currentTimeMs = Math.max(0, maxMs - 500);
          } else {
            // Voice has completed!
            if (this.isWaitingForVoice) {
              this.isWaitingForVoice = false;
              this.settleHoldRemainingMs = 400;
            }

            if (this.settleHoldRemainingMs > 0) {
              this.settleHoldRemainingMs -= deltaMs;
            } else {
              // Settle hold complete -> advance to next slide
              this.isWaitingForVoice = false;
              this.settleHoldRemainingMs = 0;
              if (this.currentSlideIdx < this.data.scenes.length - 1) {
                this.switchSlide(this.currentSlideIdx + 1);
              } else {
                this.currentTimeMs = maxMs;
                this.isPlaying = false;
                this.updatePlayBtnState();
              }
            }
          }
        }

        this.updateScrubberUI();
        this.render();
      }

      this.animationFrameId = requestAnimationFrame(this.loop);
    }

    getCurrentSlide() {
      if (!this.data || !this.data.scenes) return null;
      return this.data.scenes[this.currentSlideIdx] || null;
    }

    getEffectiveLineDuration(line) {
      if (line && line.action_type === "custom_script_engine" && line.duration_ms) {
        return line.duration_ms;
      }
      // Requirement 1: Nominal line duration strictly accounts for speech length and explicit duration.
      // Speech must conclude by 65% of the line, leaving a >= 1.5s real-time hold in SETTLE (35%).
      const baseDur = line?.duration_ms || DEFAULT_LINE_DURATION_MS;
      const sentence = line?.sentence || "";
      const words = sentence.trim() ? sentence.trim().split(/\s+/).length : 0;
      const speechNeeded = words > 0 ? Math.ceil((words * 360) / 0.65) : DEFAULT_LINE_DURATION_MS;
      return Math.max(baseDur, DEFAULT_LINE_DURATION_MS, speechNeeded);
    }

    getSlideDurationMs(slide) {
      if (!slide) return 10000;
      const isCustomScript = (slide.hide_chrome) ||
        (slide.lines && slide.lines.some(l => l.action_type === "custom_script_engine"));
      if (isCustomScript && slide.duration_ms) {
        return slide.duration_ms;
      }
      let nominalMs = 10000;
      if (slide.lines && slide.lines.length > 0) {
        nominalMs = slide.lines.reduce((acc, l) => acc + this.getEffectiveLineDuration(l), 0);
      } else {
        nominalMs = slide.duration_ms || 10000;
      }
      if (slide.duration_ms && slide.duration_ms > 0) {
        // Guarantee nominal duration comfortably covers audio + 1000ms settle hold
        return Math.max(nominalMs, slide.duration_ms + 1000);
      }
      return nominalMs;
    }

    /**
     * Requirement 5: Deterministic renderFrame(slideIdx, timeMs)
     * Pure function of (slideIdx, timeMs) -> produces identical canvas pixel state.
     */
    renderFrame(slideIdx, timeMs, overrideCtx = null) {
      const ctx = overrideCtx || this.ctx;
      if (!ctx || !this.data || !this.data.scenes) return;

      const slide = this.data.scenes[slideIdx];
      if (!slide) return;

      if (this.lastRenderedSlideIdx !== slideIdx) {
        this.lastRenderedSlideIdx = slideIdx;
        this.sceneGraph.reset();
      }

      const themeColors = window.THEME.getThemeColors();
      const lines = slide.lines || [];
      const totalLines = Math.max(1, lines.length);

      // Determine active line and lineProgress based on timeMs
      let lineAccumMs = 0;
      let activeLineIdx = 0;
      let lineStartMs = 0;
      let activeLineDuration = DEFAULT_LINE_DURATION_MS;

      for (let i = 0; i < lines.length; i++) {
        const dur = this.getEffectiveLineDuration(lines[i]);
        if (timeMs >= lineAccumMs && timeMs < lineAccumMs + dur) {
          activeLineIdx = i;
          lineStartMs = lineAccumMs;
          activeLineDuration = dur;
          break;
        }
        lineAccumMs += dur;
        if (i === lines.length - 1) {
          // Clamped at end
          activeLineIdx = i;
          lineStartMs = lineAccumMs - dur;
          activeLineDuration = dur;
        }
      }

      const lineProgress = window.TWEEN.clamp(
        (timeMs - lineStartMs) / activeLineDuration,
        0,
        1
      );

      const activeLine = lines[activeLineIdx] || {};
      const phaseState = window.TWEEN.getLinePhase(lineProgress);

      // Update DOM UI metadata if on main canvas
      if (ctx === this.ctx) {
        const narrEl = document.getElementById("anim_narration_text");
        if (narrEl && activeLine.sentence) narrEl.textContent = activeLine.sentence;
        const tagEl = document.getElementById("anim_tag_label");
        if (tagEl) tagEl.textContent = `SCENE ${slideIdx + 1} • LINE ${activeLineIdx + 1}`;
        const phaseBadge = document.getElementById("anim_phase_badge");
        if (phaseBadge) {
          const isP1 = slide.screenplay_phase && slide.screenplay_phase.includes("PHASE 1");
          phaseBadge.textContent = isP1 ? "📖 PHASE 1: REAL-LIFE SITUATION EXAMPLE" : "⚖️ PHASE 2: STATUTORY BREAKDOWN & LEGAL ARCHITECTURE";
          phaseBadge.style.background = isP1 ? "#D97706" : "#059669";
        }
        const tagIllustrative = document.getElementById("tag_illustrative_figures");
        if (tagIllustrative) {
          tagIllustrative.style.display = (this.data.is_illustrative !== false) ? "inline-block" : "none";
        }
        const tagVerify = document.getElementById("tag_needs_verification");
        if (tagVerify) {
          tagVerify.style.display = this.data.needs_verification ? "inline-block" : "none";
        }
      }

      // Slide crossfade transition at slide start (0 to 400ms)
      const slideTransition = window.TWEEN.getSlideTransition(timeMs, SLIDE_CROSSFADE_MS);

      // 1. Clear background
      window.SCAFFOLD.drawBackground(ctx, themeColors);

      ctx.save();
      ctx.globalAlpha = slideTransition.opacity;
      ctx.translate(0, slideTransition.offsetY);

      const isCustomScript = (this.data && (this.data.hide_chrome || this.data.act_name === "Custom Prompt-to-Animation Script Studio" || this.data.section_code === "Script Studio")) ||
                             (slide && slide.hide_chrome) ||
                             (activeLine && activeLine.action_type === "custom_script_engine");

      // 2. Render Header Region (x: 48, y: 32, w: 1184, h: 48)
      if (!isCustomScript) {
        window.SCAFFOLD.drawHeader(
          ctx,
          {
            act_name: this.data.act_name,
            section_code: this.data.section_code,
            tab_title: slide.tab_title,
            core_doctrine: this.data.core_doctrine
          },
          themeColors,
          activeLineIdx,
          totalLines
        );
      }

      // 3. Render Data-Driven Layout Frame into mainStageRegion (x: 48, y: 96, w: 1184, h: 480)
      const mainStageRect = isCustomScript
        ? { x: 32, y: 24, w: 1216, h: 672 }
        : window.SCAFFOLD.REGIONS.mainStage;

      const archetype = slide.layout_archetype || "layout_hero_stage";
      const layoutPayload = slide.layout_payload || {};

      let actionBounds = mainStageRect;
      if (!isCustomScript) {
        actionBounds = window.LAYOUT_FRAMES.render(
          ctx,
          archetype,
          layoutPayload,
          mainStageRect,
          phaseState.enterT,
          themeColors,
          activeLineIdx
        );
      }

      // 4. Render Kinetic Action Engine into designated actionBounds
      const actionType = activeLine.action_type || "neutral_action";
      const actionPayload = activeLine.action_payload || {};

      let engineFn = (window.ACTION_ENGINES && window.ACTION_ENGINES[actionType]) ||
                     (window.PILOT_ENGINES && window.PILOT_ENGINES[actionType]);

      if (!engineFn) {
        console.warn(`[PLAYER] Unknown action_type "${actionType}". Rendering key_points fallback.`);
        if (window.ACTION_ENGINES && window.ACTION_ENGINES.key_points) {
          engineFn = window.ACTION_ENGINES.key_points;
        } else {
          engineFn = function renderNeutralFallback(c, pld, bnds, pState, tColors) {
            const cardW = Math.min(560, bnds.w * 0.75);
            const cardH = Math.min(220, bnds.h * 0.70);
            const cardX = bnds.x + (bnds.w - cardW) / 2;
            const cardY = bnds.y + (bnds.h - cardH) / 2;

            c.save();
            window.SHARED_DRAW.card(c, cardX, cardY, cardW, cardH, {
              fill: tColors.bgCard,
              stroke: tColors.borderStrong,
              radius: window.THEME.radii.lg
            });
            c.font = window.THEME.typography.monoBadge;
            c.fillStyle = tColors.textPrimary;
            c.fillText((pld.title || actionType.replace(/_/g, " ")).toUpperCase(), cardX + 24, cardY + 30);
            c.restore();
          };
        }
      }

      engineFn(
        ctx,
        actionPayload,
        actionBounds || mainStageRect,
        phaseState,
        themeColors,
        this.sceneGraph,
        activeLineIdx
      );

      // 5. Render Caption Region (x: 48, y: 592, w: 1184, h: 96)
      if (!isCustomScript) {
        window.SCAFFOLD.drawCaption(
          ctx,
          activeLine.sentence || slide.dialogue,
          activeLine.line_title || `Step ${activeLineIdx + 1}`,
          themeColors
        );
      }

      ctx.restore();

      // Trigger Web Speech synthesis fallback ONLY if Gemini neural audio is not actively playing
      if (!overrideCtx && this.isPlaying && !this.isScrubbing) {
        const sentenceKey = `${slideIdx}_${activeLineIdx}`;
        if (this.lastSpokenKey !== sentenceKey) {
          this.lastSpokenKey = sentenceKey;
          if (window.AUDIO_MANAGER && !window.AUDIO_MANAGER.isPlayingAudio && !window.AUDIO_MANAGER.currentAudioUrl) {
            window.AUDIO_MANAGER.speakSentence(activeLine.sentence);
          }
        }
      }
    }

    render() {
      this.renderFrame(this.currentSlideIdx, this.currentTimeMs);
    }

    seekTo(timeMs) {
      const slide = this.getCurrentSlide();
      const maxMs = this.getSlideDurationMs(slide);
      this.currentTimeMs = window.TWEEN.clamp(parseFloat(timeMs), 0, maxMs);
      this.isWaitingForVoice = false;
      this.settleHoldRemainingMs = 0;
      if (this.spokenActorVoices) {
        this.spokenActorVoices.clear();
      }
      if (window.AUDIO_MANAGER) {
        window.AUDIO_MANAGER.stop();
        window.AUDIO_MANAGER.seekVoice(this.currentTimeMs);
      }
      this.render();
      this.updateScrubberUI();
    }

    togglePlay() {
      this.isPlaying = !this.isPlaying;
      this.lastTimestamp = performance.now();
      this.updatePlayBtnState();
      if (window.AUDIO_MANAGER) {
        if (!this.isPlaying) {
          window.AUDIO_MANAGER.pause();
        } else {
          if (window.AUDIO_MANAGER.isPlayingAudio) {
            window.AUDIO_MANAGER.resume();
          } else {
            const slide = this.getCurrentSlide();
            const payload = slide?.lines && slide.lines[0]?.action_payload;
            const voiceCues = payload?.voiceCues || [];
            const actors = payload?.actors || [];
            const hasPerActorDialogue = voiceCues.length > 0 || actors.some(a => a.dialogue);
            if (!hasPerActorDialogue) {
              window.AUDIO_MANAGER.playSceneVoice(slide, this.currentSlideIdx);
            }
          }
        }
      }
    }

    play() {
      if (!this.isPlaying) this.togglePlay();
    }

    pause() {
      if (this.isPlaying) this.togglePlay();
    }

    nextSlide() {
      if (!this.data || !this.data.scenes) return;
      if (this.currentSlideIdx < this.data.scenes.length - 1) {
        this.switchSlide(this.currentSlideIdx + 1);
      }
    }

    prevSlide() {
      if (!this.data || !this.data.scenes) return;
      if (this.currentSlideIdx > 0) {
        this.switchSlide(this.currentSlideIdx - 1);
      }
    }

    switchSlide(idx) {
      if (!this.data || !this.data.scenes) return;
      if (idx < 0 || idx >= this.data.scenes.length) return;

      this.currentSlideIdx = idx;
      this.currentTimeMs = 0;
      this.isWaitingForVoice = false;
      this.settleHoldRemainingMs = 0;
      this.lastSpokenKey = null;
      if (this.spokenActorVoices) {
        this.spokenActorVoices.clear();
      }
      this.sceneGraph.reset();

      // Trigger Gemini Expressive Voice for new slide if player is active and no per-actor dialogue
      if (this.isPlaying && window.AUDIO_MANAGER) {
        const slide = this.getCurrentSlide();
        const payload = slide?.lines && slide.lines[0]?.action_payload;
        const voiceCues = payload?.voiceCues || [];
        const actors = payload?.actors || [];
        const hasPerActorDialogue = voiceCues.length > 0 || actors.some(a => a.dialogue);
        if (!hasPerActorDialogue) {
          window.AUDIO_MANAGER.playSceneVoice(slide, idx);
        }
      }

      this.updateSlideTabsUI();
      this.updateSlideTimeline();
      this.render();
    }

    nextSlide() {
      if (this.currentSlideIdx < (this.data?.scenes?.length || 1) - 1) {
        this.switchSlide(this.currentSlideIdx + 1);
      }
    }

    prevSlide() {
      if (this.currentSlideIdx > 0) {
        this.switchSlide(this.currentSlideIdx - 1);
      }
    }

    setSpeed(speed) {
      this.playbackSpeed = parseFloat(speed) || 1.0;
      if (window.AUDIO_MANAGER) {
        window.AUDIO_MANAGER.setPlaybackRate(this.playbackSpeed);
      }
      document.querySelectorAll(".speed-btn").forEach(btn => {
        btn.classList.toggle("active", parseFloat(btn.dataset.speed) === this.playbackSpeed);
      });
      this.updateSlideTimeline();
    }

    toggleVoice() {
      if (window.AUDIO_MANAGER) {
        const isMuted = window.AUDIO_MANAGER.toggleMute();
        const btn = document.getElementById("btn_voice_toggle");
        if (btn) {
          btn.textContent = isMuted ? "🔇 Voice: OFF" : "🔊 Voice: ON";
          btn.style.color = isMuted ? "#DC2626" : "#059669";
          btn.style.borderColor = isMuted ? "#FECACA" : "#10B981";
        }
      }
    }

    updatePlayBtnState() {
      const btn = document.getElementById("btn_anim_play_pause");
      if (btn) {
        btn.textContent = this.isPlaying ? "⏸ Pause" : "▶ Play";
      }
    }

    updateSlideTimeline() {
      const slide = this.getCurrentSlide();
      const maxMs = this.getSlideDurationMs(slide);
      const slider = document.getElementById("anim_timeline_slider");
      if (slider) {
        slider.max = maxMs;
        slider.value = this.currentTimeMs;
      }
      this.updateScrubberUI();
    }

    updateScrubberUI() {
      const slider = document.getElementById("anim_timeline_slider");
      const display = document.getElementById("anim_time_display");
      const slide = this.getCurrentSlide();
      const maxMs = this.getSlideDurationMs(slide);

      if (slider && !this.isScrubbing) {
        slider.value = this.currentTimeMs;
      }
      if (display) {
        const curSec = (this.currentTimeMs / 1000).toFixed(1);
        const totalSec = (maxMs / 1000).toFixed(1);
        display.textContent = `${curSec}s / ${totalSec}s`;
      }
    }

    renderTabs() {
      const bar = document.getElementById("anim_scene_tabs");
      if (!bar || !this.data || !this.data.scenes) return;

      bar.innerHTML = "";
      this.data.scenes.forEach((sc, idx) => {
        const btn = document.createElement("button");
        btn.className = `scene-tab-btn ${idx === this.currentSlideIdx ? 'active' : ''}`;
        btn.textContent = sc.tab_title || `Scene ${idx + 1}`;
        btn.onclick = () => this.switchSlide(idx);
        bar.appendChild(btn);
      });
    }

    updateSlideTabsUI() {
      const bar = document.getElementById("anim_scene_tabs");
      if (!bar) return;
      const btns = bar.querySelectorAll(".scene-tab-btn");
      btns.forEach((b, idx) => {
        b.classList.toggle("active", idx === this.currentSlideIdx);
      });
    }

    /**
     * Requirement 4: Export to WebM (Visuals only via MediaRecorder)
     */
    async exportWebM() {
      if (!this.canvas) return;
      if (this.isExporting) return;

      const stream = this.canvas.captureStream(30);
      const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });
      const chunks = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `statutory_kinetic_slide_${this.currentSlideIdx + 1}.webm`;
        a.click();
        URL.revokeObjectURL(url);
        this.isExporting = false;
        alert("WebM video exported successfully! (Visual animation stream captured)");
      };

      this.isExporting = true;
      this.seekTo(0);
      this.isPlaying = true;
      recorder.start();

      const slide = this.getCurrentSlide();
      const maxMs = this.getSlideDurationMs(slide);
      setTimeout(() => {
        recorder.stop();
        this.isPlaying = false;
      }, maxMs + 500);
    }

    /**
     * Requirement 4: Export PNG Snapshot of current frame at 2x resolution
     */
    exportSnapshot() {
      if (!this.canvas) return;
      const offCanvas = document.createElement("canvas");
      offCanvas.width = LOGICAL_WIDTH * 2;
      offCanvas.height = LOGICAL_HEIGHT * 2;
      const offCtx = offCanvas.getContext("2d");
      offCtx.scale(2, 2);

      this.renderFrame(this.currentSlideIdx, this.currentTimeMs, offCtx);

      const url = offCanvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = url;
      a.download = `slide_${this.currentSlideIdx + 1}_snapshot.png`;
      a.click();
    }
  }

  // Singleton instance
  window.PRESENTATION_PLAYER = new PresentationPlayer();
})();
