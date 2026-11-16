/* ==========================================================================
   PURE AUDIO-DRIVEN KINETIC EXPLAINER ENGINE
   Architecture: render(t) is a pure function of audio.currentTime
   ========================================================================== */

(function(){

const FIXTURES = {
  "dt-c2-q14": {
    "question_id": "dt-c2-q14",
    "audio_url": "data/audio/dt-c2-q14.mp3",
    "duration_sec": 46.2,
    "sync_offset_sec": 0.0,
    "context_pill": "§ 45(2) · Conversion into Stock-in-Trade",
    "beats": [
      {
        "id": "b1",
        "layout": "headline",
        "start": 0.0,
        "end": 6.0,
        "voice_sync_text": "Section 45(2) പ്രകാരം ഒരു Capital Asset, Stock-in-trade ആയി convert ചെയ്യുമ്പോൾ transfer നടക്കുന്നു.",
        "title": { "text": "[[Section 45(2)]]", "at": 0.4 },
        "subtitle": { "text": "Capital asset becomes stock-in-trade, and the tax is [[deferred]] until sale.", "at": 1.6 }
      },
      {
        "id": "b2",
        "layout": "timeline",
        "start": 6.0,
        "end": 16.0,
        "voice_sync_text": "പക്ഷെ tax levy ചെയ്യുന്നത് conversion നടക്കുന്ന വർഷമല്ല, മറിച്ച് ആ stock യഥാർത്ഥത്തിൽ വിൽക്കുന്ന മുൻവർഷത്തിലാണ്.",
        "axis_at": 6.3,
        "arrow_at": 9.4,
        "nodes": [
          {
            "side": "left",
            "at": 6.8,
            "title": "Conversion Year",
            "sub": "(2024-25)",
            "tone": "accent",
            "chips": [
              { "text": "Deemed Transfer", "at": 7.8 },
              { "text": "Tax Parked · ₹ 0 Tax", "at": 8.6 }
            ]
          },
          {
            "side": "right",
            "at": 11.0,
            "title": "Actual Sale Year",
            "sub": "(2025-26)",
            "tone": "ok",
            "chips": [
              { "text": "Stock Sold", "at": 12.0 },
              { "text": "Tax Crystallized!", "at": 13.0, "emphasis": true }
            ]
          }
        ]
      },
      {
        "id": "b3",
        "layout": "scene",
        "start": 16.0,
        "end": 24.0,
        "voice_sync_text": "ഒരു practical example നോക്കാം. Rahul 2010-ൽ ₹ 10 Lakhs-ന് വാങ്ങിയ prime land, P.Y. 2024-25-ൽ convert ചെയ്യുന്നു.",
        "image_url": "data/img/dt-c2-q14-b3.svg",
        "zoom": [1.0, 1.06],
        "tags": [
          { "label": "Cost of land", "value": 1000000, "at": 17.6, "tone": "accent", "pos": "top-left" },
          { "label": "Fair market value on conversion", "value": 4500000, "at": 19.6, "tone": "ok", "pos": "mid-right" }
        ]
      },
      {
        "id": "b4",
        "layout": "split",
        "start": 24.0,
        "end": 32.0,
        "voice_sync_text": "Stock ₹ 65 Lakhs-ന് വിൽക്കുമ്പോൾ dual taxation split വരുന്നു: Capital Gain ₹ 26.5L, Business Profit ₹ 20L.",
        "title": { "text": "Two heads of income, [[one year of sale]]", "at": 24.3 },
        "cards": [
          { "kicker": "Capital gains", "title": "u/s 45(2)", "value": 2650000, "note": "FMV on conversion − indexed cost", "at": 25.6, "tone": "accent" },
          { "kicker": "Business income", "title": "u/s 28", "value": 2000000, "note": "Sale price − FMV on conversion", "at": 27.4, "tone": "ok" }
        ]
      },
      {
        "id": "b5",
        "layout": "trap",
        "start": 32.0,
        "end": 40.0,
        "voice_sync_text": "Section 54EC exemption-ൽ 6 months count ചെയ്യേണ്ടത് conversion മുതലല്ല, stock വിൽക്കുന്ന തീയതി മുതലാണെന്ന് Circular 791 വ്യക്തമാക്കുന്നു.",
        "title": { "text": "Exam trap: gain is [[not taxed]] at conversion", "at": 32.3 },
        "cards": [
          { "tone": "bad", "kicker": "Common mistake", "text": "Taxing the gain in the year of conversion", "at": 34.0 },
          { "tone": "good", "kicker": "Correct rule", "text": "Capital gain is charged in the year the stock is sold", "at": 36.4 }
        ]
      },
      {
        "id": "b6",
        "layout": "takeaway",
        "start": 40.0,
        "end": 46.2,
        "voice_sync_text": "അതുകൊണ്ട് ഓർക്കുക: Section 45(2) പ്രകാരം Tax is deferred, not avoided.",
        "title": { "text": "Tax is [[deferred]], not avoided.", "at": 40.4 }
      }
    ]
  }
};
FIXTURES["ch2_q14"] = FIXTURES["dt-c2-q14"];

function bezier(mX1, mY1, mX2, mY2) {
  function A(aA1, aA2) { return 1.0 - 3.0 * aA2 + 3.0 * aA1; }
  function B(aA1, aA2) { return 3.0 * aA2 - 6.0 * aA1; }
  function C(aA1)      { return 3.0 * aA1; }
  function calcBezier(aT, aA1, aA2) { return ((A(aA1, aA2)*aT + B(aA1, aA2))*aT + C(aA1))*aT; }
  function getSlope(aT, aA1, aA2) { return 3.0*A(aA1, aA2)*aT*aT + 2.0*B(aA1, aA2)*aT + C(aA1); }
  return function(x) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let t = x;
    for (let i = 0; i < 8; ++i) {
      const currentSlope = getSlope(t, mX1, mX2);
      if (currentSlope === 0.0) break;
      const currentX = calcBezier(t, mX1, mX2) - x;
      t -= currentX / currentSlope;
    }
    return calcBezier(t, mY1, mY2);
  };
}

const ease = bezier(0.22, 1, 0.36, 1);
const prog = (t, s, d) => ease(Math.min(1, Math.max(0, (t - s) / Math.max(0.001, d))));
const progLinear = (t, s, d) => Math.min(1, Math.max(0, (t - s) / Math.max(0.001, d)));

const EASE = {
  linear: p => p,
  out:    p => 1 - Math.pow(1 - p, 3),
  back:   p => 1 + 2.7 * Math.pow(p - 1, 3) + 1.7 * Math.pow(p - 1, 2),
  spring: p => (p >= 1 ? 1 : 1 - Math.exp(-6 * p) * Math.cos(14 * p)),
};
if (typeof PRESETS !== "undefined" && PRESETS.EASE_EXTRA) {
  Object.assign(EASE, PRESETS.EASE_EXTRA);
}
const inr  = n => "₹ " + Math.round(n).toLocaleString("en-IN");
const EXIT = 0.4;

const NS = "http://www.w3.org/2000/svg";
const TONE = { accent: "#4F46E5", ok: "#059669", warn: "#DC2626", bad: "#DC2626", good: "#059669" };

const isReducedMotion = () => {
  try {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch(e) {
    return false;
  }
};

const h = (cls, parent, html) => {
  const d = document.createElement("div");
  d.className = cls;
  if (html) d.innerHTML = html;
  parent.appendChild(d);
  return d;
};

const sv = (name, attrs, parent) => {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
};

const fade = (ctx, el, at, dy = 12, dur = 0.55) => ctx.push({ el, kind: "fade", start: at, dur, dy });

function words(ctx, parent, text, at, step = 0.05) {
  let n = 0;
  text.split(/(\[\[.*?\]\])/).filter(Boolean).forEach(part => {
    const marked = /^\[\[.*\]\]$/.test(part), raw = marked ? part.slice(2, -2) : part;
    let holder = parent;
    if (marked) {
      holder = document.createElement("span");
      holder.className = "mk";
      parent.appendChild(holder);
    }
    raw.split(/(\s+)/).filter(Boolean).forEach(tok => {
      if (/^\s+$/.test(tok)) {
        holder.appendChild(document.createTextNode(" "));
        return;
      }
      const s = document.createElement("span");
      s.className = "w";
      s.textContent = tok;
      holder.appendChild(s);
      ctx.push({ el: s, kind: "word", start: at + n++ * step, dur: 0.45 });
    });
    if (marked) {
      ctx.push({ el: holder, kind: "mark", start: at + (n - 1) * step + 0.1, dur: 0.3 });
    }
  });
}

const TEMPLATES = {
  headline(el, b, ctx) {
    words(ctx, h("headline", el), b.title.text, b.title.at);
    if (b.subtitle) words(ctx, h("sub", el), b.subtitle.text, b.subtitle.at);
  },
  takeaway(el, b, ctx) {
    if (b.title) words(ctx, h("headline", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    if (b.subtitle) words(ctx, h("sub", el), b.subtitle.text || b.subtitle, b.subtitle.at || (b.start + 0.8));
    const pointsList = b.points || (b.rules || []).map((r, i) => ({
      num: r.num || (r.step || (i + 1)),
      text: r.text || r.rule || r,
      at: r.at || (b.start + 0.8 + i * 0.5)
    }));

    if (pointsList.length > 0) {
      const wrap = h("takeaway-list", el);
      pointsList.forEach((pt, idx) => {
        const item = h("takeaway-item", wrap);
        item.innerHTML = `
          <div class="takeaway-num">${pt.num || (idx + 1)}</div>
          <div class="takeaway-text">${pt.text}</div>
        `;
        fade(ctx, item, pt.at || (b.start + 0.8 + idx * 0.5), 10, 0.4);
      });
    }
  },

  timeline(el, b, ctx) {
    const svg = sv("svg", { viewBox: "0 0 960 340", width: "100%", height: "100%" }, el);
    const axis = sv("path", { d: "M 150 170 L 810 170", stroke: "#D1D5DB", "stroke-width": 4, fill: "none", "stroke-linecap": "round", pathLength: 1 }, svg);
    ctx.push({ el: axis, kind: "draw", start: b.axis_at || (b.start + 0.2), dur: 1.0 });

    if (b.arrow_at) {
      const arrow = sv("path", { d: "M 210 170 L 740 170", stroke: TONE.accent, "stroke-width": 5, fill: "none", "stroke-linecap": "round", pathLength: 1 }, svg);
      const head  = sv("path", { d: "M 722 150 L 752 170 L 722 190", stroke: TONE.accent, "stroke-width": 5, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round", pathLength: 1 }, svg);
      ctx.push({ el: arrow, kind: "draw", start: b.arrow_at, dur: 1.4 });
      ctx.push({ el: head,  kind: "draw", start: b.arrow_at + 1.2, dur: 0.4 });
    }

    if (b.spans && Array.isArray(b.spans)) {
      b.spans.forEach(spn => {
        const x1 = 150 + (spn.from_x !== undefined ? spn.from_x : 0.1) * 660;
        const x2 = 150 + (spn.to_x !== undefined ? spn.to_x : 0.9) * 660;
        const g = sv("g", { class: "fade" }, svg);
        sv("rect", { x: Math.min(x1, x2), y: 130, width: Math.abs(x2 - x1), height: 80, rx: 8, fill: "rgba(79, 70, 229, 0.08)", stroke: TONE[spn.tone] || TONE.accent, "stroke-width": 1.5, "stroke-dasharray": "4 4" }, g);
        const t = sv("text", { x: (x1 + x2) / 2, y: 175, "text-anchor": "middle", "font-size": 18, "font-weight": 600, fill: TONE[spn.tone] || TONE.accent }, g);
        t.textContent = spn.text;
        fade(ctx, g, spn.at);
      });
    }

    if (b.nodes && Array.isArray(b.nodes)) {
      b.nodes.forEach(n => {
        const x = (n.x !== undefined) ? (150 + n.x * 660) : (n.side === "left" ? 180 : 780);
        const c = TONE[n.tone] || TONE.accent;
        const dot = sv("circle", { cx: x, cy: 170, r: 14, fill: "#fff", stroke: c, "stroke-width": 5, class: "fade" }, svg);
        fade(ctx, dot, n.at, 0, 0.5);
        [[n.title, 100, 30, 800, "#111827", 0.2], [n.sub, 130, 22, 500, "#6B7280", 0.4]].forEach(([txt, y, size, w, fill, d]) => {
          if (!txt) return;
          const t = sv("text", { x, y, "text-anchor": "middle", "font-size": size, "font-weight": w, fill, class: "fade" }, svg);
          t.textContent = txt;
          fade(ctx, t, n.at + d);
        });
        if (n.chips && Array.isArray(n.chips)) {
          n.chips.forEach((chip, i) => {
            const w = 40 + chip.text.length * 12, g = sv("g", { class: "fade" }, svg);
            sv("rect", { x: x - w / 2, y: 210 + i * 60, width: w, height: 46, rx: 23, fill: chip.emphasis ? "#FEF08A" : "#fff", stroke: c, "stroke-width": 1.5 }, g);
            const t = sv("text", { x, y: 240 + i * 60, "text-anchor": "middle", "font-size": 22, "font-weight": 700, fill: c }, g);
            t.textContent = chip.text;
            fade(ctx, g, chip.at);
          });
        }
      });
    }
  },

  scene(el, b, ctx) {
    const POS = {
      "top-left": ["6%", "10%"],
      "top-right": ["62%", "10%"],
      "mid-right": ["62%", "34%"],
      "bottom-left": ["6%", "70%"],
      "bottom-right": ["62%", "70%"]
    };
    const scene = h("scene", el);
    fade(ctx, scene, b.start + 0.1, 16, 0.7);
    const img = document.createElement("img");
    img.className = "art";
    const src = (b.image_url && !b.image_url.startsWith("http") && !b.image_url.startsWith("../") && !b.image_url.startsWith("/")) ? ("../" + b.image_url) : (b.image_url || "");
    img.src = src;
    img.alt = "";
    img.style.cssText = "width:100%;height:100%;display:block;object-fit:cover;transform-origin:50% 60%";
    scene.appendChild(img);
    const zFrom = (b.zoom && b.zoom[0]) ? b.zoom[0] : 1.0;
    const zTo = (b.zoom && b.zoom[1]) ? b.zoom[1] : 1.03;
    ctx.push({ el: img, kind: "zoom", start: b.start, dur: b.end - b.start, from: zFrom, to: zTo });
    if (b.tags && Array.isArray(b.tags)) {
      b.tags.forEach(t => {
        const tag = h("tag " + (t.tone === "ok" ? "ok" : ""), scene, "<small></small><b class='num'>₹ 0</b>");
        [tag.style.left, tag.style.top] = POS[t.pos] || POS["top-left"];
        tag.firstChild.textContent = t.label;
        fade(ctx, tag, t.at, 12, 0.5);
        ctx.push({ el: tag.lastChild, kind: "count", start: t.at, dur: 2.0, target: t.value, fmt: t.fmt || "inr" });
      });
    }
  },

  split(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const row = h("row", el);
    b.cards.forEach(c => {
      const card = h("card " + (c.tone === "ok" ? "b" : "a"), row, "<div class='k'></div><div class='t'></div><div class='v num'>₹ 0</div><div class='e'></div>");
      card.querySelector(".k").textContent = c.kicker || "";
      card.querySelector(".t").textContent = c.title || "";
      card.querySelector(".e").textContent = c.note || "";
      fade(ctx, card, c.at, 16, 0.6);
      ctx.push({ el: card.querySelector(".v"), kind: "count", start: c.at + 0.2, dur: 2.0, target: c.value, fmt: c.fmt || "inr" });
    });
  },

  trap(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const row = h("row", el);
    b.cards.forEach(c => {
      const card = h("card " + c.tone, row, `<div class='icon'>${c.tone === "bad" ? "✕" : "✓"}</div><div class='k'></div><div class='t small'></div>`);
      card.querySelector(".k").textContent = c.kicker || "";
      card.querySelector(".t").textContent = c.text || "";
      fade(ctx, card, c.at, 16, 0.6);
    });
  },

  fork(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const forkWrap = h("fork-wrap", el);

    if (b.story_steps && Array.isArray(b.story_steps)) {
      const stepsRow = h("story-steps-row", forkWrap);
      b.story_steps.forEach(st => {
        const stCard = h("story-step-card", stepsRow);
        stCard.innerHTML = `
          <div class="step-badge">${st.badge}</div>
          <div class="step-title">${st.title}</div>
          <div class="step-sub">${st.sub}</div>
          ${st.val ? `<div class="step-val num">${inr(st.val)}</div>` : ""}
        `;
        fade(ctx, stCard, st.at, 10, 0.4);
      });
    }

    if (b.divider) {
      const divBox = h("fork-divider", forkWrap);
      divBox.textContent = b.divider.text || b.divider || "";
      fade(ctx, divBox, b.divider.at || (b.start + 1.0), 0, 0.4);
    }

    const branchesRow = h("fork-branches", forkWrap);
    (b.branches || []).forEach(br => {
      const col = h("fork-branch " + br.side, branchesRow);
      const branchAt = br.at !== undefined ? br.at : ((b.divider && b.divider.at) ? b.divider.at + 0.1 : (b.start + 1.2));
      fade(ctx, col, branchAt, 8, 0.4);

      const lbl = h("branch-label", col);
      lbl.textContent = br.label;

      (br.facts || []).forEach(f => {
        const factBox = h("branch-fact", col);
        factBox.textContent = f.text;
        const dx = br.side === "left" ? -20 : 20;
        ctx.push({ el: factBox, kind: "slide", start: f.at, dur: 0.5, dx, dy: 0 });
      });

      if (br.outcome) {
        const outBox = h("branch-outcome", col);
        outBox.textContent = br.outcome.text;
        fade(ctx, outBox, br.outcome.at, 10, 0.5);
      }

      if (b.active && b.active.side === br.side) {
        ctx.push({ el: col, kind: "glow", start: b.active.at, dur: 0.6 });
      }
    });

    if (b.example) {
      const exBox = h("beat-example-card", forkWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <path d="M 36 30 Q 42 26 46 32" stroke="#111827" stroke-width="2.5" fill="none"/>
              <path d="M 54 32 Q 58 34 64 31" stroke="#111827" stroke-width="2.5" fill="none"/>
              <path d="M 43 52 Q 47 48 51 52 T 58 50" stroke="#111827" stroke-width="2.5" fill="none"/>
              <circle cx="76" cy="22" r="11" fill="#F59E0B"/>
              <text x="76" y="26" font-family="system-ui" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">₹</text>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Mr. Hari"}</div>
            <div class="ex-role">${b.example.role || "Practical Case"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.title ? b.title.at + 0.5 : b.start), 12, 0.5);
    }
  },

  meter(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const meterWrap = h("meter-wrap", el);

    // Support both b.meter_display and b.limit / b.reading
    const md = b.meter_display || {};
    const limitVal = b.limit ? b.limit.value : (md.threshold || md.max_val || 2500000);
    const limitText = b.limit ? b.limit.text : (md.labels?.threshold_label || "Statutory Ceiling / Threshold");
    const readingValNum = b.reading ? b.reading.value : (md.current_val || 0);
    const readingText = b.reading ? b.reading.text : (md.labels?.current_label || "Eligible Reinvestment");
    const limitAt = b.limit?.at || (b.start + 0.8);
    const readingAt = b.reading?.at || (b.start + 1.4);

    const gaugeBox = h("meter-gauge", meterWrap);
    const track = h("meter-track", gaugeBox);
    const bar = h("meter-bar", track);

    const limitLine = h("meter-limit-line", track);
    const limitLbl = h("meter-limit-label", gaugeBox);
    limitLbl.textContent = limitText + ": " + inr(limitVal);
    fade(ctx, limitLine, limitAt, 0, 0.3);
    fade(ctx, limitLbl, limitAt, 0, 0.3);

    const ratio = Math.min(1.0, Math.max(0.05, readingValNum / Math.max(1, limitVal)));
    ctx.push({ el: bar, kind: "fill", start: readingAt, dur: 1.8, to: ratio });

    const readingBox = h("meter-reading", meterWrap);
    const readingLbl = h("reading-label", readingBox);
    readingLbl.textContent = readingText;
    const readingVal = h("reading-val num", readingBox);
    fade(ctx, readingBox, readingAt, 12, 0.5);
    ctx.push({ el: readingVal, kind: "count", start: readingAt, dur: 1.8, target: readingValNum, fmt: b.reading?.fmt || "inr" });

    if (b.outcome) {
      const outPill = h("meter-outcome " + (b.outcome.tone || "ok"), meterWrap);
      outPill.textContent = b.outcome.text || b.outcome;
      fade(ctx, outPill, b.outcome.at || (readingAt + 1.0), 14, 0.6);
    }

    if (b.padlock) {
      const padBox = h("meter-padlock-box", meterWrap);
      padBox.innerHTML = `
        <div class="padlock-icon unlocked">
          <svg viewBox="0 0 100 100" width="36" height="36">
            <g class="shackle" style="transform-origin: 30px 48px; transform: rotate(-28deg);">
              <path d="M 30 48 V 30 C 30 18 70 18 70 30 V 48" stroke="#059669" stroke-width="7" stroke-linecap="round" fill="none"/>
            </g>
            <rect x="22" y="44" width="56" height="46" rx="10" fill="#10B981" stroke="#065F46" stroke-width="2"/>
            <circle cx="50" cy="62" r="5" fill="#fff"/>
            <path d="M 48 64 L 46 76 L 54 76 L 52 64 Z" fill="#fff"/>
          </svg>
        </div>
        <div class="padlock-label">${b.padlock.text || "Threshold Condition Fulfilled!"}</div>
      `;
      fade(ctx, padBox, b.padlock.at || (b.outcome ? b.outcome.at : readingAt + 1.0), 10, 0.5);
    }

    if (b.breakdown && Array.isArray(b.breakdown)) {
      const bdGrid = h("meter-breakdown-grid", meterWrap);
      bdGrid.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:14px;width:100%;";
      b.breakdown.forEach((it, idx) => {
        const isOk = !it.status?.toLowerCase().includes("ineligible") && !it.status?.toLowerCase().includes("exclude");
        const card = h("meter-bd-card", bdGrid);
        card.style.cssText = `background:var(--matte);border:1px solid ${isOk ? 'var(--ok)' : 'var(--warn)'};border-radius:10px;padding:8px 12px;display:flex;justify-content:space-between;align-items:center;`;
        card.innerHTML = `
          <div>
            <div style="font-size:0.85rem;font-weight:600;color:var(--ink)">${it.label}</div>
            <div style="font-size:0.75rem;color:${isOk ? 'var(--ok)' : 'var(--warn)'};font-weight:700">${it.status || ''}</div>
          </div>
          <div class="num" style="font-size:0.95rem;font-weight:800;color:var(--ink)">${inr(it.val || 0)}</div>
        `;
        fade(ctx, card, b.start + 1.0 + idx * 0.4, 8, 0.4);
      });
    }

    if (b.example) {
      const exBox = h("beat-example-card", meterWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <path d="M 42 49 Q 50 58 58 49" stroke="#059669" stroke-width="3" stroke-linecap="round" fill="none"/>
              <circle cx="76" cy="22" r="11" fill="#059669"/>
              <path d="M 71 22 L 74 25 L 81 18" stroke="#fff" stroke-width="2" fill="none"/>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Assessee"}</div>
            <div class="ex-role">${b.example.role || "Threshold Qualified"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text || b.example}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.outcome ? b.outcome.at + 0.3 : readingAt + 1.5), 12, 0.5);
    }
  },

  ledger(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const ledgerTable = h("ledger-table", el);

    // Support both b.rows and b.ledger_rows
    const rowsList = b.rows || (b.ledger_rows || []).map((r, i) => ({
      sign: r.sign || (r.type === "deduction" ? "minus" : "plus"),
      label: r.label || r.particulars || r.text,
      value: r.value !== undefined ? r.value : (r.amount || 0),
      at: r.at || (b.start + 0.6 + i * 0.4),
      fmt: r.fmt || "inr"
    }));

    rowsList.forEach((r, idx) => {
      const row = h("ledger-row " + (r.sign || "plus"), ledgerTable);
      const signCol = h("ledger-sign", row);
      signCol.textContent = r.sign === "minus" ? "−" : (r.sign === "total" ? "=" : "+");
      const lblCol = h("ledger-lbl", row);
      lblCol.textContent = r.label;
      const valCol = h("ledger-val num", row);
      valCol.textContent = inr(0);

      const rAt = r.at || (b.start + 0.6 + idx * 0.4);
      ctx.push({ el: row, kind: "slide", start: rAt, dur: 0.5, dx: -15, dy: 0 });
      ctx.push({ el: valCol, kind: "count", start: rAt + 0.1, dur: 1.2, target: r.value, fmt: r.fmt || "inr" });
    });

    const totObj = b.total || b.net_total;
    if (totObj) {
      const totValNum = totObj.value !== undefined ? totObj.value : (totObj.amount !== undefined ? totObj.amount : (totObj.taxable_amount || 0));
      const totLblText = totObj.label || totObj.particulars || "Taxable Capital Gain";
      const totAt = totObj.at || (b.start + 0.6 + rowsList.length * 0.4 + 0.5);

      const rule = h("ledger-rule", ledgerTable);
      ctx.push({ el: rule, kind: "strike", start: totAt - 0.2, dur: 0.4 });

      const totRow = h("ledger-row total-row", ledgerTable);
      const totSign = h("ledger-sign", totRow);
      totSign.textContent = "=";
      const totLbl = h("ledger-lbl", totRow);
      totLbl.textContent = totLblText;
      const totVal = h("ledger-val num", totRow);

      ctx.push({ el: totRow, kind: "slide", start: totAt, dur: 0.6, dx: 0, dy: 10 });
      ctx.push({ el: totVal, kind: "count", start: totAt + 0.1, dur: 1.5, target: totValNum, fmt: totObj.fmt || "inr" });
    }

    if (b.callout) {
      const calloutBox = h("ledger-callout-box", el);
      calloutBox.innerHTML = `
        <div class="callout-pill">${b.callout.badge || "Tax Alert"}</div>
        <div class="callout-text">${b.callout.text || b.callout}</div>
      `;
      fade(ctx, calloutBox, b.callout.at || (b.start + 2.5), 12, 0.5);
    }
  },

  case_card(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const card = h("case-card-wrap", el);

    const hdr = h("case-header", card);
    const cName = h("case-name", hdr);
    cName.textContent = b.case.text;
    fade(ctx, cName, b.case.at, 10, 0.4);

    if (b.court) {
      const courtBadge = h("case-court", hdr);
      courtBadge.textContent = b.court.text;
      fade(ctx, courtBadge, b.court.at, 0, 0.4);
    }

    if (b.gap) {
      const gapBox = h("case-gap", card);
      const gapKicker = h("case-kicker", gapBox);
      gapKicker.textContent = "Statutory Ambiguity";
      const gapText = h("case-body", gapBox);
      gapText.textContent = b.gap.text;
      fade(ctx, gapBox, b.gap.at, 12, 0.5);
    }

    if (b.principle) {
      const prinBox = h("case-principle", card);
      const prinKicker = h("case-kicker", prinBox);
      prinKicker.textContent = "Judicial Ruling";
      const prinText = h("case-body principle-text", prinBox);
      words(ctx, prinText, b.principle.text, b.principle.at);
      fade(ctx, prinBox, b.principle.at, 12, 0.5);
    }

    if (b.effect) {
      const effBox = h("case-effect", card);
      const effKicker = h("case-kicker", effBox);
      effKicker.textContent = "Statutory Effect";
      const effText = h("case-body", effBox);
      effText.textContent = b.effect.text;
      fade(ctx, effBox, b.effect.at, 10, 0.5);
    }

    if (b.houses && Array.isArray(b.houses)) {
      const housesGrid = h("case-houses-grid", card);
      b.houses.forEach(hItem => {
        const hCard = h("case-house-card " + (hItem.isTotal ? "total" : ""), housesGrid);
        hCard.innerHTML = `
          <div class="house-loc">${hItem.location}</div>
          <div class="house-status">${hItem.status}</div>
          <div class="house-val num">${inr(hItem.cost)}</div>
        `;
        fade(ctx, hCard, hItem.at, 8, 0.4);
      });
    }
  },

  compare(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const cmpWrap = h("compare-wrap", el);
    (b.columns || []).forEach((colData, ci) => {
      const col = h("compare-col", cmpWrap);
      const colTitle = h("compare-col-title", col);
      colTitle.textContent = colData.title;
      ctx.push({ el: col, kind: "slide", start: colData.at, dur: 0.5, dx: ci === 0 ? -15 : 15, dy: 0 });

      (colData.rows || []).forEach(r => {
        const row = h("compare-row", col);
        const rLbl = h("compare-row-lbl", row);
        rLbl.textContent = r.label;
        const rVal = h("compare-row-val", row);
        rVal.textContent = r.text;
        fade(ctx, row, r.at, 8, 0.4);
      });
    });

    if (b.highlight && Array.isArray(b.highlight)) {
      b.highlight.forEach(hl => {
        const rows = cmpWrap.querySelectorAll(`.compare-row:nth-child(${hl.row + 1})`);
        rows.forEach(r => {
          ctx.push({ el: r, kind: "glow", start: hl.at, dur: 0.5 });
        });
      });
    }
  },

  checklist(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const listWrap = h("checklist-wrap", el);

    (b.items || []).forEach(it => {
      const row = h("checklist-row " + (it.result === "pass" ? "pass" : "fail"), listWrap);
      const ico = h("checklist-icon", row);
      ico.textContent = it.result === "pass" ? "✓" : "✕";
      const txt = h("checklist-text", row);
      txt.textContent = it.text;
      ctx.push({ el: row, kind: "slide", start: it.at, dur: 0.5, dx: -12, dy: 0 });
    });
  },

  statute_quote(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const quoteWrap = h("statute-quote-wrap", el);

    if (b.sale_card) {
      const sc = h("quote-sale-card", quoteWrap);
      sc.innerHTML = `
        <div class="sale-card-grid">
          <div class="sale-item">
            <div class="sale-lbl">${b.sale_card.sale_lbl || "Full Consideration (June 2025)"}</div>
            <div class="sale-val num">${inr(b.sale_card.sale_val || 0)}</div>
          </div>
          <div class="sale-sign">−</div>
          <div class="sale-item">
            <div class="sale-lbl">${b.sale_card.cost_lbl || "Adjusted Cost u/s 51"}</div>
            <div class="sale-val num">${inr(b.sale_card.cost_val || 0)}</div>
          </div>
          <div class="sale-sign">=</div>
          <div class="sale-item gain">
            <div class="sale-lbl">${b.sale_card.gain_lbl || "Gross LTCG"}</div>
            <div class="sale-val num">${inr(b.sale_card.gain_val || 0)}</div>
          </div>
        </div>
      `;
      fade(ctx, sc, b.sale_card.at || (b.start + 0.5), 10, 0.4);
    }

    if (b.context_bubble) {
      const cbBox = h("beat-example-card", quoteWrap);
      cbBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar" style="font-size:1.8rem;line-height:1;display:flex;align-items:center;justify-content:center;">§</div>
          <div>
            <div class="ex-name">${b.context_bubble.speaker || "Statutory Intent"}</div>
            <div class="ex-role">${b.context_bubble.theme || "Core Provision"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.context_bubble.text || b.context_bubble}</div>
      `;
      fade(ctx, cbBox, b.context_bubble.at || (b.start + 0.6), 12, 0.5);
    }

    if (b.example) {
      const exBox = h("beat-example-card", quoteWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <circle cx="76" cy="22" r="11" fill="#F59E0B"/>
              <text x="76" y="26" font-family="system-ui" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">?</text>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Assessee Question"}</div>
            <div class="ex-role">${b.example.role || "Practical Issue"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text || b.example}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.start + 0.8), 12, 0.5);
    }

    if (b.quote) {
      const quoteBox = h("statute-quote-box", quoteWrap);
      const qText = typeof b.quote === "string" ? b.quote : (b.quote.text || "");
      const qAt = (b.quote && b.quote.at) ? b.quote.at : (b.start + 1.0);
      fade(ctx, quoteBox, qAt, 10, 0.4);
      words(ctx, quoteBox, qText, qAt, 0.04);
      if (b.quote.citation) {
        const cit = h("quote-citation", quoteBox);
        cit.style.cssText = "font-size:0.85rem;color:var(--ink-soft);margin-top:8px;font-style:italic;display:block;";
        cit.textContent = "— " + b.quote.citation;
      }
    }
  },

  hub_branches(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const wrap = h("hub-branches-wrap", el);
    const stage = h("hub-branches-stage", wrap);

    const style = b.style || "fade.glow.calm";
    const hero = h("hero", stage);
    const avatarImg = h("hero-avatar", hero);
    avatarImg.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
      <circle cx="50" cy="40" r="28" fill="var(--matte, #F3F4F6)" stroke="var(--ink, #111827)" stroke-width="3"/>
      <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="var(--accent, #4F46E5)" opacity="0.9"/>
      <circle cx="41" cy="38" r="3.5" fill="var(--ink, #111827)"/>
      <circle cx="59" cy="38" r="3.5" fill="var(--ink, #111827)"/>
      <g class="s-a">
        <path d="M 36 30 Q 42 26 46 32" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 54 32 Q 58 34 64 31" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 43 52 Q 47 48 51 52 T 58 50" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <circle cx="76" cy="22" r="12" fill="var(--warn, #DC2626)" opacity="0.95"/>
        <text x="76" y="27" font-family="system-ui, sans-serif" font-weight="900" font-size="14" fill="#FFFFFF" text-anchor="middle">?</text>
      </g>
      <g class="s-b">
        <path d="M 36 29 Q 42 28 46 30" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 54 30 Q 58 28 64 29" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 42 49 Q 50 58 58 49" stroke="var(--ok, #059669)" stroke-width="3" stroke-linecap="round" fill="none"/>
        <circle cx="76" cy="22" r="12" fill="var(--ok, #059669)" opacity="0.95"/>
        <path d="M 70 22 L 74 26 L 82 17" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </g>
    </svg>`;
    const moodA = h("mood s-a", hero);
    moodA.textContent = b.hero.mood_a;
    const moodB = h("mood s-b", hero);
    moodB.textContent = b.hero.mood_b;

    let lock = null;
    if (b.unlock) {
      lock = h("lock", stage);
      const lockIcon = h("lock-icon", lock);
      lockIcon.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
        <g class="shackle" style="transform-origin: 30px 48px;">
          <path d="M 30 48 V 30 C 30 18 70 18 70 30 V 48" stroke="var(--ink, #111827)" stroke-width="7" stroke-linecap="round" fill="none"/>
        </g>
        <rect x="22" y="44" width="56" height="46" rx="10" fill="var(--accent, #4F46E5)" stroke="var(--ink, #111827)" stroke-width="3"/>
        <circle cx="50" cy="62" r="5" fill="#FFFFFF"/>
        <path d="M 48 64 L 46 76 L 54 76 L 52 64 Z" fill="#FFFFFF"/>
      </svg>`;
      const lockText = h("lock-text", lock);
      lockText.textContent = b.unlock.text;
    }

    const branchesGrid = h("branches-grid", wrap);
    const branchEls = (b.branches || []).map(br => {
      const card = h("branch-card" + (br.taxable ? " taxable-remainder" : ""), branchesGrid);
      const icon = h("house-icon", card);
      icon.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
        <path d="M 16 46 L 50 18 L 84 46" stroke="var(--ink, #111827)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="${br.taxable ? 'var(--warn)' : 'var(--accent)'}"/>
        <rect x="68" y="22" width="8" height="16" fill="var(--ink-soft)" stroke="var(--ink)" stroke-width="2"/>
        <rect x="24" y="46" width="52" height="44" rx="4" fill="var(--matte)" stroke="var(--ink)" stroke-width="3"/>
        <rect x="42" y="62" width="16" height="28" rx="2" fill="${br.taxable ? 'var(--warn)' : 'var(--accent)'}" opacity="0.85"/>
      </svg>`;
      const lbl = h("house-label", card);
      lbl.textContent = br.label;
      const tag = h("tag num", card);
      tag.textContent = br.tag;
      return card;
    });

    if (typeof PRESETS !== "undefined" && PRESETS.applyEnter) {
      PRESETS.applyEnter(ctx, hero, b.hero.at, style);
    } else {
      fade(ctx, hero, b.hero.at, 10, 0.5);
    }

    ctx.push({ el: hero, kind: "swap", start: b.hero.mood_at });

    if (lock && b.unlock) {
      const shackle = lock.querySelector(".shackle");
      if (shackle) {
        ctx.push({ el: shackle, kind: "tween", start: b.unlock.at, dur: 0.5, ease: "back", to: { y: -1.2, rot: -35 } });
      }
      fade(ctx, lock, b.unlock.at, 8, 0.4);
    }

    (b.branches || []).forEach((br, i) => {
      if (typeof PRESETS !== "undefined" && PRESETS.applyEnter) {
        PRESETS.applyEnter(ctx, branchEls[i], br.at, style);
      } else {
        fade(ctx, branchEls[i], br.at, 12, 0.5);
      }
    });
  }
};

class Explainer {
  constructor({ stage, focal, audio, caption, bar, pill, scrub, speed, playBtn, timeText }) {
    Object.assign(this, { stage, focal, audio, caption, bar, pill, scrub, speed, playBtn, timeText });
    this.anim = [];
    this.beatEls = [];
    this.raf = 0;
    this.sp = null;
    this.offset = 0;
    this.isDebug = window.location.search.includes("debug=1");

    if (this.isDebug && this.stage) {
      this.initDebugHud();
    }

    audio.addEventListener("play",       () => { this.updatePlayIcon(true); this.loop(); });
    audio.addEventListener("pause",      () => { this.updatePlayIcon(false); cancelAnimationFrame(this.raf); });
    audio.addEventListener("seeked",     () => this.render());
    audio.addEventListener("timeupdate", () => { if (audio.paused) this.render(); });

    if (this.scrub) {
      this.scrub.addEventListener("input", () => {
        if (this.audio.duration) {
          this.audio.currentTime = Number(this.scrub.value);
        }
      });
    }

    if (this.speed) {
      this.speed.addEventListener("change", () => {
        this.audio.playbackRate = Number(this.speed.value);
      });
      this.speed.addEventListener("click", (e) => e.stopPropagation());
    }

    if (this.playBtn) {
      this.playBtn.addEventListener("click", () => this.toggle());
    }

    // Space key to toggle play/pause
    this.keyHandler = (e) => {
      if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "SELECT")) return;
      if (e.code === "Space" || e.key === " ") {
        e.preventDefault();
        this.toggle();
      }
    };
    window.addEventListener("keydown", this.keyHandler);
  }

  initDebugHud() {
    this.debugHud = document.createElement("div");
    this.debugHud.id = "expDebugHud";
    this.debugHud.style.cssText = "position:absolute;top:8px;right:8px;background:rgba(17,24,39,0.85);color:#fff;font-family:monospace;font-size:12px;padding:6px 10px;border-radius:6px;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;";
    this.debugDot = document.createElement("span");
    this.debugDot.style.cssText = "width:8px;height:8px;border-radius:50%;background:#4ADE80;opacity:0.3;";
    this.debugText = document.createElement("span");
    this.debugHud.appendChild(this.debugDot);
    this.debugHud.appendChild(this.debugText);
    this.stage.appendChild(this.debugHud);
  }

  updatePlayIcon(isPlaying) {
    if (!this.playBtn) return;
    const playSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
    const pauseSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
    this.playBtn.innerHTML = isPlaying ? pauseSvg : playSvg;
  }

  toggle() {
    if (this.isPlaying || (this.audio && !this.audio.paused)) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    if (this.audio && this.audio.src) {
      const p = this.audio.play();
      if (p && typeof p.catch === "function") {
        p.then(() => {
          this.isPlaying = true;
          this.updatePlayIcon(true);
          if (typeof this.onPlay === "function") this.onPlay();
          this.loop();
        }).catch(err => {
          console.warn("Audio autoplay blocked by browser, awaiting user gesture:", err);
          this.isPlaying = false;
          this.updatePlayIcon(false);
          if (typeof this.onPause === "function") this.onPause();
        });
        return;
      }
    }
    this.isPlaying = true;
    this.updatePlayIcon(true);
    if (typeof this.onPlay === "function") this.onPlay();
    this.startVirtualClock();
    this.loop();
  }

  pause() {
    this.isPlaying = false;
    this.updatePlayIcon(false);
    if (typeof this.onPause === "function") this.onPause();
    if (this.audio) this.audio.pause();
    this.stopVirtualClock();
    cancelAnimationFrame(this.raf);
  }

  startVirtualClock() {
    this._lastClockTick = performance.now();
    this._virtualClockActive = true;
  }

  stopVirtualClock() {
    this._virtualClockActive = false;
  }

  async load(qid, inlineSp = null) {
    let sp = inlineSp;
    const normKey = qid ? qid.replace(/-/g, "_") : "";
    const chKey = qid ? qid.replace(/^dt-/, "").replace(/-/g, "_") : "";

    if (!sp && typeof FIXTURES !== "undefined") {
      sp = FIXTURES[qid] || FIXTURES[normKey] || FIXTURES[chKey];
    }
    if (!sp && window.EXPLAINER_SCREENPLAYS) {
      sp = window.EXPLAINER_SCREENPLAYS[qid] || window.EXPLAINER_SCREENPLAYS[normKey] || window.EXPLAINER_SCREENPLAYS[chKey];
    }

    if (!sp && window.location.protocol !== "file:") {
      try {
        const resp = await fetch(`/api/screenplay/${qid}`);
        if (resp.ok) sp = await resp.json();
      } catch (e) {}
    }

    if (!sp && window.location.protocol !== "file:") {
      try {
        const localResp = await fetch(`data/screenplays/${qid}.json`);
        if (localResp.ok) sp = await localResp.json();
      } catch (e) {}
    }

    // Check window.D for live screenplay
    if (!sp && window.D && window.D.qna) {
      const qObj = window.D.qna.find(item => item.id === qid || ("dt-c" + item.ch + "-q" + item.n) === qid);
      if (qObj) {
        const prov = window.D.prov?.[qObj.topic];
        if (prov && prov.screenplay) {
          sp = prov.screenplay;
        }
      }
    }

    if (!sp && window.EXPLAINER_SCREENPLAYS) {
      sp = window.EXPLAINER_SCREENPLAYS[qid] || window.EXPLAINER_SCREENPLAYS[normKey] || window.EXPLAINER_SCREENPLAYS["dt-c2-q25"] || window.EXPLAINER_SCREENPLAYS["dt-c2-q14"];
    }

    if (!sp) {
      console.warn("Could not find screenplay for", qid, "generating fallback structure...");
      sp = {
        question_id: qid,
        context_pill: "Statutory Pedagogical Explainer",
        duration_sec: 45.0,
        beats: [
          {
            id: "b1",
            layout: "headline",
            start: 0,
            end: 15,
            voice_sync_text: "Statutory overview and core legal doctrine.",
            title: { text: "Statutory Provision Analysis", at: 0.5 },
            subtitle: { text: "Master the statutory principle before solving the exam case.", at: 2.0 }
          },
          {
            id: "b2",
            layout: "takeaway",
            start: 15,
            end: 45,
            voice_sync_text: "Golden takeaways for CA Final / Inter exams.",
            title: { text: "Key Statutory Takeaways", at: 15.5 },
            points: [
              { num: "1", text: "Verify statutory eligibility conditions under relevant section.", at: 18.0 },
              { num: "2", text: "Compute capital gains and appropriate exemptions accurately.", at: 25.0 }
            ]
          }
        ]
      };
    }

    this.sp = sp;
    this.offset = sp.sync_offset_sec || 0;
    this._virtualTime = 0;
    if (this.pill && sp.context_pill) {
      this.pill.textContent = sp.context_pill;
    }

    if (sp.audio_url) {
      const aSrc = (sp.audio_url && !sp.audio_url.startsWith("http") && !sp.audio_url.startsWith("../") && !sp.audio_url.startsWith("/")) ? ("../" + sp.audio_url) : sp.audio_url;
      this.audio.src = aSrc;
    }

    if (this.scrub) {
      this.scrub.min = 0;
      this.scrub.max = sp.duration_sec || 46.2;
      this.scrub.step = 0.05;
      this.scrub.value = 0;
    }

    this.focal.innerHTML = "";
    this.anim = [];
    this.beatEls = sp.beats.map((b, i) => {
      const el = document.createElement("div");
      el.className = "beat " + b.layout;
      el.id = "beat-" + (b.id || (i + 1));
      el.dataset.layout = b.layout;
      this.focal.appendChild(el);
      if (TEMPLATES[b.layout]) {
        TEMPLATES[b.layout](el, b, { push: a => this.anim.push({ ...a, beat: i, p: 0 }) });
      } else {
        console.warn("Unknown layout:", b.layout);
        TEMPLATES.headline(el, { title: { text: "Beat " + (i + 1), at: b.start } }, { push: a => this.anim.push({ ...a, beat: i, p: 0 }) });
      }
      return el;
    });

    this.render();
  }

  time(t) {
    if (t !== undefined && t !== null) {
      this._mockTime = t;
      this.render();
      return t;
    }
    if (this._mockTime !== undefined && this._mockTime !== null) return this._mockTime;
    if (this.audio && this.audio.src && !this.audio.error && !isNaN(this.audio.currentTime) && this.audio.currentTime > 0) {
      return Math.max(0, this.audio.currentTime - this.offset);
    }
    return Math.max(0, (this._virtualTime || 0) - this.offset);
  }

  loop() {
    if (this._virtualClockActive) {
      const now = performance.now();
      const dt = (now - (this._lastClockTick || now)) / 1000 * (this.audio?.playbackRate || 1.0);
      this._lastClockTick = now;
      this._virtualTime = (this._virtualTime || 0) + dt;
      const maxDur = this.sp?.duration_sec || 46.2;
      if (this.scrub) {
        this.scrub.value = this._virtualTime;
      }
      if (this.timeText) {
        const cur = this._virtualTime, dur = maxDur;
        this.timeText.textContent = Math.floor(cur / 60) + ":" + (Math.floor(cur % 60) < 10 ? "0" : "") + Math.floor(cur % 60) + " / " + Math.floor(dur / 60) + ":" + (Math.floor(dur % 60) < 10 ? "0" : "") + Math.floor(dur % 60);
      }
      if (this._virtualTime >= maxDur) {
        this._virtualTime = maxDur;
        this.render();
        this.pause();
        return;
      }
    }
    this.render();
    if (this.isPlaying || (this.audio && !this.audio.paused)) {
      this.raf = requestAnimationFrame(() => this.loop());
    }
  }

  render() {
    if (!this.sp || !this.sp.beats) return;
    const t = this.time(), beats = this.sp.beats;
    let active = 0;
    beats.forEach((b, i) => { if (t >= b.start) active = i; });
    this.beatEls.forEach((e, i) => e.classList.toggle("active", i === active));
    this.stage.dataset.beat = active + 1;

    // Exit drift: previous text fades and rises 8px before the next beat
    const b = beats[active];
    const x = (active < beats.length - 1 && b.end) ? ease((t - (b.end - EXIT)) / EXIT) : 0;
    const el = this.beatEls[active];
    if (el) {
      el.style.opacity = Math.max(0, 1 - x);
      el.style.transform = isReducedMotion() ? "none" : `translateY(${-8 * x}px)`;
    }

    let debugAnchorTriggered = false;

    // Animation updates
    for (const a of this.anim) {
      if (a.beat !== active) continue;
      const p = prog(t, a.start, a.dur);
      a.p = p; // Hook for test assertions

      if (this.isDebug && Math.abs(t - a.start) < 0.05) {
        debugAnchorTriggered = true;
      }

      switch (a.kind) {
        case "word":
          a.el.style.opacity = p;
          a.el.style.transform = isReducedMotion() ? "none" : `translateY(${12 * (1 - p)}px)`;
          break;
        case "mark":
          a.el.style.backgroundSize = `${p * 100}% 88%`;
          break;
        case "draw":
          a.el.style.strokeDasharray = 1;
          a.el.style.strokeDashoffset = 1 - p;
          a.el.style.opacity = p > 0 ? 1 : 0;
          break;
        case "fade":
          a.el.style.opacity = p;
          if (a.dy && !isReducedMotion()) a.el.style.transform = `translateY(${a.dy * (1 - p)}px)`;
          break;
        case "count": {
          const val = a.target * p;
          if (a.fmt === "pct") {
            a.el.textContent = Math.round(val) + "%";
          } else if (a.fmt === "num") {
            a.el.textContent = Math.round(val).toLocaleString("en-IN");
          } else {
            a.el.textContent = inr(val);
          }
          break;
        }
        case "zoom": {
          if (isReducedMotion()) {
            a.el.style.transform = "scale(1)";
          } else {
            const z = Math.min(1, Math.max(0, (t - a.start) / Math.max(0.001, a.dur)));
            a.el.style.transform = `scale(${a.from + (a.to - a.from) * z})`;
          }
          break;
        }
        case "fill": {
          const fillTo = (a.to !== undefined) ? a.to : 1;
          a.el.style.transform = `scaleX(${fillTo * p})`;
          a.el.style.transformOrigin = "left center";
          break;
        }
        case "slide": {
          const dx = (isReducedMotion() ? 0 : (a.dx || 0)) * (1 - p);
          const dy = (isReducedMotion() ? 0 : (a.dy || 0)) * (1 - p);
          a.el.style.opacity = p;
          a.el.style.transform = `translate(${dx}px, ${dy}px)`;
          break;
        }
        case "strike": {
          a.el.style.width = `${p * 100}%`;
          break;
        }
        case "glow": {
          a.el.style.boxShadow = `0 0 ${p * 24}px rgba(79, 70, 229, ${p * 0.35})`;
          a.el.style.borderColor = `rgba(79, 70, 229, ${0.2 + p * 0.8})`;
          a.el.style.backgroundColor = `rgba(224, 231, 255, ${p * 0.25})`;
          break;
        }
        case "tween": {
          const easeFn = (typeof PRESETS !== "undefined" && PRESETS.EASE_EXTRA && PRESETS.EASE_EXTRA[a.ease])
            ? PRESETS.EASE_EXTRA[a.ease]
            : (EASE[a.ease || "out"] || EASE.out);
          const ep = easeFn(progLinear(t, a.start, a.dur));
          const D = { x: 0, y: 0, rot: 0, s: 1, o: 1, clip: 1 };
          const L = (valA, valB, pos) => valA + (valB - valA) * pos;
          const f = Object.assign({}, D, a.from);
          const g = Object.assign({}, D, a.to);
          const reduce = isReducedMotion();
          const y = reduce ? 0 : L(f.y, g.y, ep);
          const sc = reduce ? 1 : L(f.s, g.s, ep);
          a.el.style.transform = `translate(${L(f.x, g.x, ep)}cqw, ${y}cqw) rotate(${L(f.rot, g.rot, ep)}deg) scale(${sc})`;
          a.el.style.opacity = Math.max(0, Math.min(1, L(f.o, g.o, ep)));
          a.el.style.clipPath = `inset(0 ${(1 - L(f.clip, g.clip, ep)) * 100}% 0 0)`;
          break;
        }
        case "swap":
          a.el.dataset.state = t >= a.start ? "b" : "a";
          break;
      }
    }

    if (this.isDebug && this.debugHud) {
      this.debugText.textContent = `t=${t.toFixed(2)}s | B${active + 1}`;
      this.debugDot.style.opacity = debugAnchorTriggered ? "1.0" : "0.25";
      this.debugDot.style.background = debugAnchorTriggered ? "#FACC15" : "#4ADE80";
    }

    if (this.caption) {
      this.caption.textContent = b.voice_sync_text || "";
    }

    const dur = this.sp.duration_sec || this.audio.duration || 1;
    if (this.bar) {
      this.bar.style.width = Math.min(100, Math.max(0, 100 * t / dur)) + "%";
    }

    if (this.scrub && !this.scrub.matches(":active")) {
      this.scrub.value = t;
    }

    if (this.timeText) {
      const fmt = s => {
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60);
        return m + ":" + (sec < 10 ? "0" : "") + sec;
      };
      this.timeText.textContent = `${fmt(t)} / ${fmt(dur)}`;
    }
  }

  destroy() {
    cancelAnimationFrame(this.raf);
    this.audio.pause();
    window.removeEventListener("keydown", this.keyHandler);
  }
}

window.Explainer = Explainer;
window.TEMPLATES = TEMPLATES;
window.LAYOUTS = Object.keys(TEMPLATES);

window.EXPLAINER_SCREENPLAYS = window.EXPLAINER_SCREENPLAYS || {};
window.EXPLAINER_SCREENPLAYS["dt-c2-q14"] = {
  "question_id": "dt-c2-q14",
  "audio_url": "data/audio/dt-c2-q14.mp3",
  "duration_sec": 46.2,
  "sync_offset_sec": 0.0,
  "context_pill": "§ 45(2) · Conversion into Stock-in-Trade",
  "beats": [
    {
      "id": "b1",
      "layout": "headline",
      "start": 0.0,
      "end": 6.0,
      "voice_sync_text": "Section 45(2) പ്രകാരം ഒരു Capital Asset, Stock-in-trade ആയി convert ചെയ്യുമ്പോൾ transfer നടക്കുന്നു.",
      "title": { "text": "[[Section 45(2)]]", "at": 0.4 },
      "subtitle": { "text": "Capital asset becomes stock-in-trade, and the tax is [[deferred]] until sale.", "at": 1.6 }
    },
    {
      "id": "b2",
      "layout": "timeline",
      "start": 6.0,
      "end": 16.0,
      "voice_sync_text": "പക്ഷെ tax levy ചെയ്യുന്നത് conversion നടക്കുന്ന വർഷമല്ല, മറിച്ച് ആ stock യഥാർത്ഥത്തിൽ വിൽക്കുന്ന മുൻവർഷത്തിലാണ്.",
      "axis_at": 6.3,
      "arrow_at": 9.4,
      "nodes": [
        {
          "side": "left",
          "at": 6.8,
          "title": "Conversion Year",
          "sub": "(2024-25)",
          "tone": "accent",
          "chips": [
            { "text": "Deemed Transfer", "at": 7.8 },
            { "text": "Tax Parked · ₹ 0 Tax", "at": 8.6 }
          ]
        },
        {
          "side": "right",
          "at": 11.0,
          "title": "Actual Sale Year",
          "sub": "(2025-26)",
          "tone": "ok",
          "chips": [
            { "text": "Stock Sold", "at": 12.0 },
            { "text": "Tax Crystallized!", "at": 13.0, "emphasis": true }
          ]
        }
      ]
    },
    {
      "id": "b3",
      "layout": "scene",
      "start": 16.0,
      "end": 24.0,
      "voice_sync_text": "ഒരു practical example നോക്കാം. Rahul 2010-ൽ ₹ 10 Lakhs-ന് വാങ്ങിയ prime land, P.Y. 2024-25-ൽ convert ചെയ്യുന്നു.",
      "image_url": "data/img/dt-c2-q14-b3.svg",
      "zoom": [1.0, 1.06],
      "tags": [
        { "label": "Cost of land", "value": 1000000, "at": 17.6, "tone": "accent", "pos": "top-left" },
        { "label": "Fair market value on conversion", "value": 4500000, "at": 19.6, "tone": "ok", "pos": "mid-right" }
      ]
    },
    {
      "id": "b4",
      "layout": "split",
      "start": 24.0,
      "end": 32.0,
      "voice_sync_text": "Stock ₹ 65 Lakhs-ന് വിൽക്കുമ്പോൾ dual taxation split വരുന്നു: Capital Gain ₹ 26.5L, Business Profit ₹ 20L.",
      "title": { "text": "Two heads of income, [[one year of sale]]", "at": 24.3 },
      "cards": [
        { "kicker": "Capital gains", "title": "u/s 45(2)", "value": 2650000, "note": "FMV on conversion − indexed cost", "at": 25.6, "tone": "accent" },
        { "kicker": "Business income", "title": "u/s 28", "value": 2000000, "note": "Sale price − FMV on conversion", "at": 27.4, "tone": "ok" }
      ]
    },
    {
      "id": "b5",
      "layout": "trap",
      "start": 32.0,
      "end": 40.0,
      "voice_sync_text": "Section 54EC exemption-ൽ 6 months count ചെയ്യേണ്ടത് conversion മുതലല്ല, stock വിൽക്കുന്ന തീയതി മുതലാണെന്ന് Circular 791 വ്യക്തമാക്കുന്നു.",
      "title": { "text": "Exam trap: gain is [[not taxed]] at conversion", "at": 32.3 },
      "cards": [
        { "tone": "bad", "kicker": "Common mistake", "text": "Taxing the gain in the year of conversion", "at": 34.0 },
        { "tone": "good", "kicker": "Correct rule", "text": "Capital gain is charged in the year the stock is sold", "at": 36.4 }
      ]
    },
    {
      "id": "b6",
      "layout": "takeaway",
      "start": 40.0,
      "end": 46.2,
      "voice_sync_text": "അതുകൊണ്ട് ഓർക്കുക: Section 45(2) പ്രകാരം Tax is deferred, not avoided.",
      "title": { "text": "Tax is [[deferred]], not avoided.", "at": 40.4 }
    }
  ]
};

FIXTURES["test_fixture_all_layouts"] = {
  "question_id": "test_fixture_all_layouts",
  "audio_url": "data/audio/dt-c2-q14.mp3",
  "duration_sec": 65.0,
  "sync_offset_sec": 0.0,
  "context_pill": "Test Suite ? All 13 Layouts Parity Fixture",
  "fallback": false,
  "meta": {
    "concept": "Comprehensive test fixture verifying all 13 layout templates",
    "mechanism": {
      "primary": "threshold",
      "secondary": [
        "date_cutoff",
        "computation"
      ]
    }
  },
  "beats": [
    {
      "id": "b1",
      "layout": "headline",
      "start": 0.0,
      "end": 5.0,
      "purpose": "Verify headline layout",
      "serves": [
        "p1"
      ],
      "voice_sync_text": "Headline test beat with title and subtitle.",
      "title": {
        "text": "[[Section 54]] Test Headline",
        "at": 0.5
      },
      "subtitle": {
        "text": "Testing word reveal and marker sweep",
        "at": 1.5
      }
    },
    {
      "id": "b2",
      "layout": "timeline",
      "start": 5.0,
      "end": 10.0,
      "purpose": "Verify timeline layout with spans and x coordinates",
      "serves": [
        "p2"
      ],
      "voice_sync_text": "Timeline test beat with span windows.",
      "axis_at": 5.2,
      "arrow_at": 6.5,
      "spans": [
        {
          "text": "Exemption Window",
          "from_x": 0.2,
          "to_x": 0.8,
          "tone": "accent",
          "at": 5.5
        }
      ],
      "nodes": [
        {
          "x": 0.2,
          "side": "left",
          "tone": "accent",
          "title": "2024",
          "sub": "Purchase",
          "at": 5.6,
          "chips": [
            {
              "text": "Step 1",
              "at": 6.0
            }
          ]
        },
        {
          "x": 0.8,
          "side": "right",
          "tone": "ok",
          "title": "2026",
          "sub": "Sale",
          "at": 7.0,
          "chips": [
            {
              "text": "Step 2",
              "at": 7.4
            }
          ]
        }
      ]
    },
    {
      "id": "b3",
      "layout": "scene",
      "start": 10.0,
      "end": 15.0,
      "purpose": "Verify scene layout with count tag",
      "serves": [
        "p3"
      ],
      "voice_sync_text": "Scene test beat with image zoom.",
      "image_url": "data/img/dt-c2-q14-b3.svg",
      "zoom": [
        1.0,
        1.03
      ],
      "tags": [
        {
          "pos": "bottom-left",
          "label": "Test Property",
          "value": 1500000,
          "at": 10.5,
          "fmt": "inr"
        }
      ]
    },
    {
      "id": "b4",
      "layout": "split",
      "start": 15.0,
      "end": 20.0,
      "purpose": "Verify split layout",
      "serves": [
        "p4"
      ],
      "voice_sync_text": "Split computation dual cards.",
      "title": {
        "text": "Dual Head [[Split]]",
        "at": 15.2
      },
      "cards": [
        {
          "tone": "accent",
          "kicker": "LTCG",
          "title": "Gain",
          "value": 2500000,
          "note": "Section 45",
          "at": 15.6,
          "fmt": "inr"
        },
        {
          "tone": "ok",
          "kicker": "PGBP",
          "title": "Profit",
          "value": 1000000,
          "note": "Section 28",
          "at": 17.0,
          "fmt": "inr"
        }
      ]
    },
    {
      "id": "b5",
      "layout": "trap",
      "start": 20.0,
      "end": 25.0,
      "purpose": "Verify trap layout",
      "serves": [
        "p5"
      ],
      "voice_sync_text": "Exam trap comparison.",
      "title": {
        "text": "Common [[Mistake]]",
        "at": 20.2
      },
      "cards": [
        {
          "tone": "bad",
          "kicker": "Wrong",
          "text": "Tax on conversion date",
          "at": 20.6
        },
        {
          "tone": "good",
          "kicker": "Correct",
          "text": "Tax on sale date",
          "at": 22.0
        }
      ]
    },
    {
      "id": "b6",
      "layout": "fork",
      "start": 25.0,
      "end": 30.0,
      "purpose": "Verify fork layout (date_cutoff)",
      "serves": [
        "p6"
      ],
      "voice_sync_text": "Cut-off date dividing line test.",
      "title": {
        "text": "Cut-off [[1st April 2014]]",
        "at": 25.2
      },
      "divider": {
        "text": "1st April 2014 dividing line",
        "at": 25.4
      },
      "branches": [
        {
          "side": "left",
          "label": "Before 01-04-2014",
          "facts": [
            {
              "text": "Advance forfeited",
              "at": 26.0
            }
          ],
          "outcome": {
            "text": "Deduct from cost",
            "at": 27.0
          }
        },
        {
          "side": "right",
          "label": "On or after 01-04-2014",
          "facts": [
            {
              "text": "Advance forfeited",
              "at": 26.5
            }
          ],
          "outcome": {
            "text": "Taxable u/s 56(2)(ix)",
            "at": 27.5
          }
        }
      ],
      "active": {
        "side": "left",
        "at": 28.0
      }
    },
    {
      "id": "b7",
      "layout": "meter",
      "start": 30.0,
      "end": 35.0,
      "purpose": "Verify meter layout (threshold)",
      "serves": [
        "p7"
      ],
      "voice_sync_text": "Threshold meter test.",
      "title": {
        "text": "Section 54 [[Threshold Meter]]",
        "at": 30.2
      },
      "limit": {
        "text": "Statutory Limit",
        "value": 20000000,
        "at": 30.4
      },
      "reading": {
        "text": "Current Capital Gain",
        "value": 3425000,
        "at": 31.0,
        "fmt": "inr"
      },
      "outcome": {
        "text": "Two houses unlocked",
        "at": 32.5,
        "tone": "ok"
      }
    },
    {
      "id": "b8",
      "layout": "ledger",
      "start": 35.0,
      "end": 40.0,
      "purpose": "Verify ledger layout (computation)",
      "serves": [
        "p8"
      ],
      "voice_sync_text": "Computation ledger calculation rows.",
      "title": {
        "text": "Taxable LTCG [[Ledger]]",
        "at": 35.2
      },
      "rows": [
        {
          "label": "Full Value of Consideration",
          "value": 4300000,
          "sign": "plus",
          "at": 35.5,
          "fmt": "inr"
        },
        {
          "label": "Less: Cost of Acquisition",
          "value": 875000,
          "sign": "minus",
          "at": 36.5,
          "fmt": "inr"
        },
        {
          "label": "Less: Section 54 Exemption",
          "value": 1200000,
          "sign": "minus",
          "at": 37.5,
          "fmt": "inr"
        }
      ],
      "total": {
        "label": "Taxable Long Term Capital Gain",
        "value": 2225000,
        "at": 38.0,
        "fmt": "inr"
      }
    },
    {
      "id": "b9",
      "layout": "case_card",
      "start": 40.0,
      "end": 45.0,
      "purpose": "Verify case_card layout (precedent)",
      "serves": [
        "p9"
      ],
      "voice_sync_text": "Judicial precedent case law card.",
      "title": {
        "text": "Landmark [[Judicial Precedent]]",
        "at": 40.2
      },
      "case": {
        "text": "Balraj v. CIT (2002)",
        "at": 40.5
      },
      "court": {
        "text": "Delhi High Court",
        "at": 41.0
      },
      "gap": {
        "text": "Unregistered agreement with possession",
        "at": 41.5
      },
      "principle": {
        "text": "Legal registered title is [[not mandatory]] if full consideration is paid",
        "at": 42.0
      },
      "effect": {
        "text": "Section 54 deduction fully allowed",
        "at": 43.0
      }
    },
    {
      "id": "b10",
      "layout": "compare",
      "start": 45.0,
      "end": 50.0,
      "purpose": "Verify compare layout (classification)",
      "serves": [
        "p10"
      ],
      "voice_sync_text": "Comparison table columns.",
      "title": {
        "text": "Classification [[Comparison]]",
        "at": 45.2
      },
      "columns": [
        {
          "title": "Old Regime",
          "at": 45.5,
          "rows": [
            {
              "label": "Exemption",
              "text": "? 2.5 Lakhs",
              "at": 46.0
            }
          ]
        },
        {
          "title": "New Regime",
          "at": 46.5,
          "rows": [
            {
              "label": "Exemption",
              "text": "? 3.0 Lakhs",
              "at": 47.0
            }
          ]
        }
      ],
      "highlight": [
        {
          "row": 0,
          "at": 48.0
        }
      ]
    },
    {
      "id": "b11",
      "layout": "checklist",
      "start": 50.0,
      "end": 55.0,
      "purpose": "Verify checklist layout (condition_chain)",
      "serves": [
        "p11"
      ],
      "voice_sync_text": "Condition chain checklist.",
      "title": {
        "text": "Eligibility [[Checklist]]",
        "at": 50.2
      },
      "items": [
        {
          "text": "Individual or HUF assessee",
          "result": "pass",
          "at": 50.8
        },
        {
          "text": "Long term capital asset transferred",
          "result": "pass",
          "at": 51.8
        },
        {
          "text": "New house within statutory period",
          "result": "pass",
          "at": 52.8
        }
      ]
    },
    {
      "id": "b12",
      "layout": "statute_quote",
      "start": 55.0,
      "end": 60.0,
      "purpose": "Verify statute_quote layout",
      "serves": [
        "p12"
      ],
      "voice_sync_text": "Statutory verbatim extract.",
      "title": {
        "text": "Bare Act [[Extract]]",
        "at": 55.2
      },
      "quote": {
        "text": "Where the amount of the capital gain [[does not exceed two crore rupees]], the assessee may, at his option, purchase two residential houses in India.",
        "at": 55.5
      }
    },
    {
      "id": "b13",
      "layout": "takeaway",
      "start": 60.0,
      "end": 65.0,
      "purpose": "Verify takeaway layout",
      "serves": [
        "p13"
      ],
      "voice_sync_text": "Closing takeaway axiom.",
      "title": {
        "text": "Compliance is [[absolute]], not discretionary.",
        "at": 60.5
      }
    }
  ]
};
window.EXPLAINER_SCREENPLAYS["test_fixture_all_layouts"] = FIXTURES["test_fixture_all_layouts"];

window.EXPLAINER_SCREENPLAYS["ch2_q14"] = window.EXPLAINER_SCREENPLAYS["dt-c2-q14"];

FIXTURES["dt-c2-q25"] = {
  "question_id": "dt-c2-q25",
  "audio_url": "data/audio/dt-c2-q25.mp3",
  "duration_sec": 203.28,
  "sync_offset_sec": 0.0,
  "context_pill": "§ 54 · Two Residential Houses & § 51 Advance Forfeiture",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "fork",
      "start": 0.0,
      "end": 40.73,
      "voice_sync_text": "സെക്ഷൻ 51-ന്റെ പ്രൊവിഷൻ മനസ്സിലാക്കാൻ നമുക്ക് ഹരിയുടെ ഒരു സിമ്പിൾ എക്സാമ്പിൾ നോക്കാം. ഹരി 2002-ൽ 9 ലക്ഷം രൂപയ്ക്ക് ഡൽഹിയിൽ ഒരു റെസിഡൻഷ്യൽ ഹൗസ് വാങ്ങി. 2005 മെയ് മാസത്തിൽ പരി എന്ന ബയറുമായി നെഗോഷ്യേഷൻ നടത്തുമ്പോൾ 25,000 രൂപ അഡ്വാൻസ് മണി വാങ്ങി. പക്ഷെ പിന്നീട് ആ ഡീൽ കാൻസലാവുകയും ഹരി ആ അഡ്വാൻസ് ഫോർഫീറ്റ് ചെയ്യുകയും ചെയ്തു. ഇവിടെ ഒരു കട്ട്-ഓഫ് ഡേറ്റ് ഓർക്കുക: ഒന്നാം തീയതി ഏപ്രിൽ 2014-ന് മുൻപാണ് ഫോർഫീച്ചർ എങ്കിൽ, സെക്ഷൻ 51 പ്രകാരം അത് കോസ്റ്റ് ഓഫ് അക്വിസിഷനിൽ നിന്ന് കുറയ്ക്കണം! അതുകൊണ്ട് ഹരിയുടെ അഡ്ജസ്റ്റഡ് കോസ്റ്റ് 9 ലക്ഷത്തിൽ നിന്ന് 25,000 കുറച്ച് 8 ലക്ഷത്തി 75,000 രൂപയായി മാറുന്നു!",
      "title": {
        "text": "Section 51 · Advance Money Forfeiture Cut-off",
        "at": 0.3
      },
      "story_steps": [
        {
          "badge": "Year 2002",
          "title": "Delhi House Acquisition",
          "sub": "Hari purchased residential house in Delhi",
          "val": 900000,
          "at": 4.8
        },
        {
          "badge": "May 2005",
          "title": "Negotiation with Pari",
          "sub": "Agreement to sell & advance money received",
          "val": 25000,
          "at": 10.5
        },
        {
          "badge": "Deal Cancelled",
          "title": "Advance Forfeited by Hari",
          "sub": "Kept advance upon buyer default u/s 51",
          "val": 25000,
          "at": 18.0
        }
      ],
      "divider": {
        "text": "Forfeiture Cut-off Date: 01-04-2014",
        "at": 22.8
      },
      "branches": [
        {
          "side": "left",
          "label": "Before 01-04-2014 (Hari's Case: May 2005)",
          "facts": [
            {
              "text": "Deduct from Cost of Acquisition u/s 51",
              "at": 29.8
            }
          ],
          "outcome": {
            "text": "Reduces Cost of Acquisition",
            "at": 31.5
          }
        },
        {
          "side": "right",
          "label": "On/After 01-04-2014",
          "facts": [
            {
              "text": "Taxable under IFOS u/s 56(2)(ix)",
              "at": 27.0
            }
          ],
          "outcome": {
            "text": "Income from Other Sources (No Cost Reduction)",
            "at": 28.5
          }
        }
      ],
      "active": {
        "side": "left",
        "at": 29.8
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Adjusted Cost Result",
        "text": "Section 51 Computation: Cost ₹ 9,00,000 − Advance Forfeited ₹ 25,000 = Adjusted Cost ₹ 8,75,000!",
        "at": 33.5
      },
      "style": "zoom_in.color_shift.calm",
      "serves": [
        "p1",
        "p2",
        "c1",
        "c2",
        "f2",
        "d1",
        "n3",
        "t1"
      ]
    },
    {
      "id": "b2",
      "layout": "statute_quote",
      "start": 40.98,
      "end": 78.51,
      "voice_sync_text": "ഇനി 2025 ജൂൺ മാസത്തിൽ ഹരി ഈ വീട് 43 ലക്ഷം രൂപയ്ക്ക് വിൽക്കുന്നു. അപ്പോൾ ഹരിയുടെ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ വരുന്നത് 43 ലക്ഷം മൈനസ് 8 ലക്ഷത്തി 75,000, അതായത് 34 ലക്ഷത്തി 25,000 രൂപ! ഇവിടെ ഹരി ചോദിക്കുന്നു: 'എനിക്ക് സെക്ഷൻ 54 പ്രകാരം ഒരു വീടിന് പകരം രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങി എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാൻ പറ്റുമോ?' സെക്ഷൻ 54 സബ് സെക്ഷൻ ഒന്നിന്റെ ഫസ്റ്റ് പ്രൊവൈസോ പറയുന്നത് നോക്കൂ: ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടി രൂപയിൽ കവിയുന്നില്ലെങ്കിൽ, അസ്സസ്സീക്ക് ഇന്ത്യയിൽ രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങാനുള്ള സ്റ്റാറ്റ്യൂട്ടറി ഓപ്ഷൻ ലഭിക്കും!",
      "title": {
        "text": "Section 54(1) · First Proviso: Two Residential Houses",
        "at": 41.2
      },
      "sale_card": {
        "sale_lbl": "Full Value of Consideration (June 2025)",
        "sale_val": 4300000,
        "cost_lbl": "Less: Adjusted Cost u/s 51",
        "cost_val": 875000,
        "gain_lbl": "Gross LTCG Generated",
        "gain_val": 3425000,
        "at": 42.5
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Assessee Question",
        "text": "Can I purchase TWO residential houses in India and claim Section 54 exemption?",
        "at": 58.6
      },
      "quote": {
        "text": "Where Capital Gain ≤ [[₹ 2.00 Crore]], Assessee may purchase or construct [[two residential houses in India]] (Once-in-a-lifetime option).",
        "at": 67.5
      },
      "style": "fade.pulse.snappy",
      "serves": [
        "p3",
        "c3",
        "n6",
        "t3"
      ]
    },
    {
      "id": "b3",
      "layout": "meter",
      "start": 78.76,
      "end": 100.41,
      "voice_sync_text": "ഇവിടെ നമ്മുടെ ത്രെഷോൾഡ് മീറ്റർ നോക്കൂ! സ്റ്റാറ്റ്യൂട്ടറി ലിമിറ്റ് രണ്ട് കോടി രൂപയാണ്. ഹരിയുടെ ക്യാപിറ്റൽ ഗെയിൻ എത്രയാണ്? വെറും 34 ലക്ഷത്തി 25,000 രൂപ മാത്രം! ഇത് രണ്ട് കോടി രൂപയേക്കാൾ വളരെ താഴെയാണ്. അതുകൊണ്ട് ദാ, നമ്മുടെ പാഡ്‌ലോക്ക് ഓപ്പൺ ആയി! ഹരിക്ക് ജീവിതത്തിൽ ഒരിക്കൽ മാത്രം ലഭിക്കുന്ന ടു റെസിഡൻഷ്യൽ ഹൗസസ് ഓപ്ഷൻ ഇവിടെ അൺലോക്ക് ആയിരിക്കുന്നു!",
      "title": {
        "text": "Section 54 Statutory Threshold Gauge",
        "at": 79.0
      },
      "limit": {
        "text": "Statutory Ceiling Limit",
        "value": 20000000,
        "at": 81.0
      },
      "reading": {
        "text": "Hari's Long-Term Capital Gain",
        "value": 3425000,
        "at": 84.5,
        "fmt": "inr"
      },
      "outcome": {
        "text": "₹ 34.25 Lakhs ≤ ₹ 2.00 Crore · THRESHOLD SATISFIED",
        "tone": "ok",
        "at": 90.0
      },
      "padlock": {
        "text": "Capital Gain ₹ 34.25L ≤ ₹ 2.00 Crore: TWO HOUSES OPTION UNLOCKED!",
        "at": 92.5
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Threshold Qualified",
        "text": "Once-in-a-lifetime option unlocked! Entitled to claim exemption for 2 residential houses in India.",
        "at": 95.5
      },
      "style": "slide_down.glow.snappy",
      "serves": [
        "c3",
        "n5",
        "n6"
      ]
    },
    {
      "id": "b4",
      "layout": "case_card",
      "start": 100.66,
      "end": 140.83,
      "voice_sync_text": "ഹരി രണ്ട് വീടുകൾ വാങ്ങി. ഒന്ന് ചെന്നൈയിൽ 5 ലക്ഷം രൂപയ്ക്ക്, മറ്റൊന്ന് ഡൽഹിയിൽ 7 ലക്ഷം രൂപയ്ക്ക്. പക്ഷെ ഇവിടെ ഒരു വലിയ പ്രശ്നം വന്നു! ഡൽഹിയിലെ വീടിന്റെ മുഴുവൻ തുകയും നൽകി ഹരി കൈവശം വെച്ചെങ്കിലും, അതിന്റെ സെയിൽ ഡീഡ് രജിസ്റ്റർ ചെയ്തിട്ടില്ല! അസ്സസ്സിങ് ഓഫീസർ ചോദിക്കുന്നു: 'രജിസ്ട്രേഷൻ ഇല്ലാത്ത വീടിന് എങ്ങനെ സെക്ഷൻ 54 കൊടുക്കും?' ഇവിടെയാണ് ഡൽഹി ഹൈക്കോടതിയുടെ ലാൻഡ്മാർക്ക് കേസായ ബൽരാജ് വേഴ്സസ് സി.ഐ.ടി. വരുന്നത്! കോടതി വ്യക്തമാക്കി: സെക്ഷൻ 53A പ്രകാരം പൊസഷനും മുഴുവൻ പെയ്മെന്റും ഉണ്ടെങ്കിൽ സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ആയി. അതിനാൽ രജിസ്റ്റേർഡ് ഡീഡ് ഇല്ലെങ്കിലും ഡൽഹി വീടിന് സെക്ഷൻ 54 എക്സംപ്ഷൻ പൂർണ്ണമായും ലഭിക്കും!",
      "title": {
        "text": "Judicial Precedent · Section 54 Legal Title",
        "at": 101.0
      },
      "houses": [
        {
          "location": "Chennai House",
          "status": "House 1 · Registered Sale Deed",
          "cost": 500000,
          "at": 102.5
        },
        {
          "location": "Delhi House",
          "status": "House 2 · Possession Taken, Full Payment Paid",
          "cost": 700000,
          "at": 105.0
        },
        {
          "location": "Total Section 54 Exemption",
          "status": "Exemption Allowed for Both Houses",
          "cost": 1200000,
          "isTotal": true,
          "at": 134.0
        }
      ],
      "gap": {
        "text": "AO Objection: Delhi house deed was unregistered on 31-03-2026. Can Section 54 exemption be disallowed?",
        "at": 108.5
      },
      "case": {
        "text": "Balraj v. CIT (2002) 254 ITR 22",
        "at": 118.5
      },
      "court": {
        "text": "Delhi High Court Benchmark",
        "at": 119.5
      },
      "principle": {
        "text": "Section 53A TPA possession and full consideration constitute substantial ownership for Section 54 without registered deed.",
        "at": 122.5
      },
      "effect": {
        "text": "Exemption ALLOWED for Delhi House (₹ 7,00,000) despite lack of registered conveyance.",
        "at": 128.5
      },
      "style": "whip_left.shake.calm",
      "serves": [
        "c4",
        "f4",
        "cl1",
        "cl2",
        "t2"
      ]
    },
    {
      "id": "b5",
      "layout": "ledger",
      "start": 141.08,
      "end": 180.05,
      "voice_sync_text": "ഇനി ഫൈനൽ ക്യാപിറ്റൽ ഗെയിൻസ് ലെഡ്ജർ നോക്കാം. ഫുൾ വാല്യൂ ഓഫ് കൺസിഡറേഷൻ 43 ലക്ഷം രൂപ. ലെസ്സ്: അഡ്ജസ്റ്റഡ് കോസ്റ്റ് ഓഫ് അക്വിസിഷൻ 8 ലക്ഷത്തി 75,000 രൂപ. ഗ്രോസ് ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ 34 ലക്ഷത്തി 25,000 രൂപ. ഇനി ഇതിൽ നിന്ന് രണ്ട് വീടുകളുടെയും എക്സംപ്ഷൻ കുറയ്ക്കാം: ഡൽഹി വീടിന് 7 ലക്ഷം, ചെന്നൈ വീടിന് 5 ലക്ഷം. ആകെ എക്സംപ്ഷൻ 12 ലക്ഷം രൂപ! ബാക്കി വരുന്ന തുക നോക്കൂ: 34 ലക്ഷത്തി 25,000-ൽ നിന്ന് 12 ലക്ഷം കുറച്ചാൽ കൃത്യം 22 ലക്ഷത്തി 25,000 രൂപ! സ്റ്റുഡന്റ്സ് ഓർക്കുക, ഈ 22 ലക്ഷത്തി 25,000 രൂപ ടാക്സബിൾ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ ആണ്!",
      "title": {
        "text": "Statutory Capital Gains Ledger",
        "at": 141.4
      },
      "rows": [
        {
          "sign": "plus",
          "label": "Full Value of Consideration (Sold June 2025)",
          "value": 4300000,
          "at": 144.0,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Adjusted Cost u/s 51 (₹ 9,00,000 − ₹ 25,000)",
          "value": 875000,
          "at": 148.2,
          "fmt": "inr"
        },
        {
          "sign": "plus",
          "label": "Gross Long-Term Capital Gain",
          "value": 3425000,
          "at": 152.2,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Delhi House Exemption (Balraj v. CIT)",
          "value": 700000,
          "at": 158.8,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Chennai House Exemption (Second House)",
          "value": 500000,
          "at": 161.2,
          "fmt": "inr"
        }
      ],
      "total": {
        "label": "Taxable Long-Term Capital Gain",
        "value": 2225000,
        "at": 168.0,
        "fmt": "inr"
      },
      "callout": {
        "badge": "Taxable Remainder",
        "text": "Remaining ₹ 22,25,000 is fully taxable LTCG! Exemption is capped to ₹ 12,00,000 actual investment.",
        "at": 174.8
      },
      "style": "slide_up.shimmer.calm",
      "serves": [
        "c1",
        "c2",
        "c3",
        "c4",
        "f1",
        "f2",
        "f3",
        "f4"
      ]
    },
    {
      "id": "b6",
      "layout": "takeaway",
      "start": 180.3,
      "end": 203.27,
      "voice_sync_text": "അതുകൊണ്ട് എക്സാമിനായി മൂന്ന് ഗോൾഡൻ റൂൾസ് എപ്പോഴും ഓർക്കുക: ഒന്ന്, 2014-ന് മുൻപുള്ള അഡ്വാൻസ് ഫോർഫീച്ചർ കോസ്റ്റ് കുറയ്ക്കുന്നു. രണ്ട്, ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടിയിൽ താഴെയാണെങ്കിൽ രണ്ട് വീടുകൾക്ക് എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാം. മൂന്ന്, രജിസ്ട്രേഷൻ പൂർത്തിയായില്ലെങ്കിലും സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ഉണ്ടെങ്കിൽ സെക്ഷൻ 54 ലഭിക്കും. ബാക്കി വരുന്ന ഗെയിൻ കൃത്യമായി ടാക്സ് ചെയ്യപ്പെടും!",
      "title": {
        "text": "Exam Summary · 3 Golden Takeaways",
        "at": 180.6
      },
      "points": [
        {
          "num": "1",
          "text": "Advance forfeited before 01-04-2014 reduces Cost of Acquisition u/s 51.",
          "at": 184.5
        },
        {
          "num": "2",
          "text": "Capital Gains ≤ ₹ 2 Crore unlocks exemption for TWO residential houses u/s 54.",
          "at": 189.2
        },
        {
          "num": "3",
          "text": "Possession + full payment qualifies u/s 53A TPA without deed registration (Balraj v. CIT).",
          "at": 195.0
        },
        {
          "num": "★",
          "text": "Taxable Remainder: Remaining ₹ 22.25L is fully taxable LTCG.",
          "at": 200.8
        }
      ],
      "style": "zoom_in.none.calm",
      "serves": [
        "f1",
        "f2",
        "f3",
        "f4"
      ]
    }
  ]
};
FIXTURES["dt_c2_q25"] = FIXTURES["dt-c2-q25"];
FIXTURES["ch2_q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["dt-c2-q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["dt_c2_q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["ch2_q25"] = FIXTURES["dt-c2-q25"];

FIXTURES["dt-c2-q32"] = {
  "question_id": "dt-c2-q32",
  "audio_url": "data/audio/dt-c2-q32.mp3",
  "duration_sec": 125.8,
  "sync_offset_sec": 0.0,
  "context_pill": "Section 54G | Shifting of Industrial Undertaking",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "fork",
      "voice_sync_text": "Makkale, Gama Ltd avarude industrial undertaking urban corporation limitsil ninnu non-urban areayilekk shift cheyyukayanu. Shifting processil avaru Land, Building, Plant & Machinery, pinne Furniture vare vilkkukayum puthiyath vangukayum cheythu. Pakshe Section 54G il oru valiya trap undu. Athu manassilakkiyillel examil marks pokum!",
      "title": {
        "text": "Asset Eligibility Filter under Section 54G",
        "at": 0.5
      },
      "story_steps": [
        {
          "badge": "Shift Decision",
          "title": "Urban to Non-Urban Shifting",
          "sub": "Gama Ltd transfers industrial undertaking assets",
          "val": 4500000,
          "at": 2.0
        }
      ],
      "divider": {
        "text": "Scope of Section 54G: Specified Assets Only",
        "at": 5.0
      },
      "branches": [
        {
          "side": "left",
          "label": "Eligible Specified Assets",
          "facts": [
            {
              "text": "Plant & Machinery, Land, or Building",
              "at": 7.0
            },
            {
              "text": "Both transfer & reinvestment qualify u/s 54G",
              "at": 9.5
            }
          ],
          "outcome": {
            "text": "Eligible for Section 54G Exemption",
            "at": 12.0
          }
        },
        {
          "side": "right",
          "label": "Ineligible Non-Specified Assets",
          "facts": [
            {
              "text": "Furniture & Fixtures, Office Appliances",
              "at": 7.0
            },
            {
              "text": "Neither sale nor new purchase qualifies",
              "at": 9.5
            }
          ],
          "outcome": {
            "text": "No Exemption! Full STCG Taxable",
            "at": 12.0
          }
        }
      ],
      "result_card": {
        "badge": "Key Exclusion",
        "title": "Furniture STCG Isolated",
        "val": 100000,
        "at": 15.0
      },
      "start": 0.0,
      "end": 23.4
    },
    {
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Section 54G clear aayi parayunnu: Capital Gain arose from transfer of machinery, plant, building, or land used for the purpose of an industrial undertaking situated in an urban area. Assessee 1 year before or 3 years after the date of transfer eligible assets purchase cheythal, deduction kittum.",
      "title": {
        "text": "Statutory Mandate: Section 54G(1)",
        "at": 0.5
      },
      "quote": {
        "text": "Where the capital gain arises from the transfer of a capital asset, being plant, machinery, land or building or any rights in building or land, used for the purpose of an industrial undertaking situated in an urban area... and the assessee has within a period of one year before or three years after the date on which the transfer took place purchased new machinery or plant or acquired building or land...",
        "citation": "Section 54G(1) of the Income-tax Act, 1961",
        "emphasis": "plant, machinery, land or building... 1 year before or 3 years after"
      },
      "context_bubble": {
        "badge": "Time Horizon",
        "note": "Reinvestment Window: July 2026 acquisition satisfies the 'within 3 years after March 2026' requirement.",
        "at": 6.0
      },
      "start": 23.75,
      "end": 46.91
    },
    {
      "id": "b3",
      "layout": "meter",
      "voice_sync_text": "Nammude total eligible investment pool ethrayanu? Land Rs 4 Lakh, Building Rs 7 Lakh, Plant & Machinery Rs 17 Lakh. Total Rs 28 Lakhs! Note cheyyuka, Furniture-nte Rs 2 Lakh ivide add cheyyan padilla. Ee Rs 28 Lakhs namukk STCG-kkum LTCG-kkum ethirayi set-off cheyyam.",
      "title": {
        "text": "Section 54G Eligible Investment Reinvestment Pool",
        "at": 0.5
      },
      "meter_display": {
        "min_val": 0,
        "max_val": 3000000,
        "current_val": 2800000,
        "unit": "₹",
        "threshold": 2500000,
        "labels": {
          "start": "₹ 0",
          "threshold_label": "STCG Threshold: ₹ 25L",
          "current_label": "Eligible Reinvestment: ₹ 28L"
        }
      },
      "breakdown": [
        {
          "label": "New Land Acquired",
          "val": 400000,
          "status": "Qualifies"
        },
        {
          "label": "New Building Acquired",
          "val": 700000,
          "status": "Qualifies"
        },
        {
          "label": "New Plant & Machinery",
          "val": 1700000,
          "status": "Qualifies"
        },
        {
          "label": "New Furniture Purchased",
          "val": 200000,
          "status": "Ineligible (Excluded)"
        }
      ],
      "start": 47.26,
      "end": 70.3
    },
    {
      "id": "b4",
      "layout": "ledger",
      "voice_sync_text": "Tax optimizationte golden trick ivideyanu! Act-il pro-rata set-off niyamam illa. Assessee-kk beneficial aaya reethiyil exemption exhaust cheyyam. Athukondu higher tax bracket ulla Short-term Capital Gain first wipe out cheyyanam. Building & Plant STCG total Rs 25 Lakhs poornnamayum Section 54G vechu Nil aakki. Balance Rs 3 Lakhs Land-nte Long-term Capital Gain-il ninnu kurachu. So, final taxable amount just Rs 2 Lakhs mathram!",
      "title": {
        "text": "Computation of Taxable Capital Gains for AY 2026-27",
        "at": 0.5
      },
      "ledger_rows": [
        {
          "label": "Building STCG u/s 50 (₹18L - WDV ₹4L)",
          "amount": 1400000,
          "type": "income",
          "note": "Depreciable Asset u/s 50"
        },
        {
          "label": "Plant & Machinery STCG u/s 50 (₹16L - WDV ₹5L)",
          "amount": 1100000,
          "type": "income",
          "note": "Depreciable Asset u/s 50"
        },
        {
          "label": "Total Deemed STCG Eligible for Section 54G",
          "amount": 2500000,
          "type": "subtotal",
          "note": "Taxable at normal corporate tax rates"
        },
        {
          "label": "Less: Section 54G Exemption (Priority 1: Against STCG)",
          "amount": -2500000,
          "type": "deduction",
          "note": "Exhausted against high-tax STCG first"
        },
        {
          "label": "Net STCG on Industrial Assets",
          "amount": 0,
          "type": "subtotal",
          "note": "Fully Exempt"
        },
        {
          "label": "Land LTCG (Sale ₹8L - Cost ₹4L)",
          "amount": 400000,
          "type": "income",
          "note": "Non-depreciable Long-term asset"
        },
        {
          "label": "Less: Balance Section 54G Exemption (₹28L - ₹25L)",
          "amount": -300000,
          "type": "deduction",
          "note": "Remaining balance set off against LTCG"
        },
        {
          "label": "Taxable LTCG on Land (Taxable @ 12.5% u/s 112)",
          "amount": 100000,
          "type": "taxable",
          "note": "Concessional tax rate"
        },
        {
          "label": "Furniture STCG (Sale ₹3L - WDV ₹2L)",
          "amount": 100000,
          "type": "taxable",
          "note": "No 54G Exemption allowed for Furniture"
        }
      ],
      "net_total": {
        "label": "Total Taxable Capital Gains",
        "val": 200000,
        "detail": "₹1,00,000 LTCG @ 12.5% + ₹1,00,000 STCG @ Normal Rates"
      },
      "start": 70.65,
      "end": 99.69
    },
    {
      "id": "b5",
      "layout": "takeaway",
      "voice_sync_text": "Exam hall-il orthu vekkenda 3 Golden Rules: Onnamathathu, Furniture-nu Section 54G il sthanamilla. Randamathathu, Section 50 prakaram ulla STCG-kkum Section 54G exemption valid aanu. Moonnamathathu, tax liability minimize cheyyan Section 54G deduction aadyam STCG-kk ethireyum, balance LTCG-kk ethireyum set-off cheyyam!",
      "title": {
        "text": "3 Golden Rules for Section 54G Mastery",
        "at": 0.5
      },
      "rules": [
        {
          "num": "01",
          "heading": "Strict Asset Basket (Furniture Excluded)",
          "body": "Section 54G applies strictly to Plant, Machinery, Land, and Building. Capital gains on Furniture cannot be exempted, and reinvestment in Furniture does not count towards the eligible investment."
        },
        {
          "num": "02",
          "heading": "Section 50 Deemed STCG is Eligible",
          "body": "Even though Section 50 deems depreciable assets as Short-Term Capital Gains, Section 54G exemption is fully applicable against such deemed STCG (established in landmark jurisprudence and CBDT circulars)."
        },
        {
          "num": "03",
          "heading": "Most Beneficial Set-Off Ordering",
          "body": "The statute does not compel pro-rata apportionment. Always exhaust Section 54G exemption against Short-Term Capital Gains first (normal tax rate) before offsetting Long-Term Capital Gains (concessional 12.5% rate u/s 112)."
        }
      ],
      "start": 100.04,
      "end": 125.8
    }
  ]
};
FIXTURES["dt_c2_q32"] = FIXTURES["dt-c2-q32"];
FIXTURES["ch2_q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["dt-c2-q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["dt_c2_q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["ch2_q32"] = FIXTURES["dt-c2-q32"];



})();
