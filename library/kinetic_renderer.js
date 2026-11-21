/**
 * Kinetic SVG Animation Engine v1.0
 * Complete 15-Archetype Kinetic Library (10 Specific Actions + 5 General Fallbacks)
 * Pure function of time t in [0, duration].
 *
 * Rules:
 * - Canvas 1000 x 562, Safe Area [35 <= x <= 965, 25 <= y <= 535]
 * - Dual Light & Dark theme support
 * - Zero hardcoded tax words (pure semantic decoupling)
 * - Physical kinetic displacement (>= 100px motion deltas across frames)
 */

(function (global) {
  "use strict";

  // Easing Library
  const Easing = {
    linear: p => p,
    easeIn: p => p * p * p,
    easeOut: p => 1 - Math.pow(1 - p, 3),
    easeInOut: p => p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
    backOut: p => {
      const c1 = 1.70158;
      const c3 = c1 + 1;
      return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
    },
    bounceOut: p => {
      const n1 = 7.5625, d1 = 2.75;
      if (p < 1 / d1) return n1 * p * p;
      if (p < 2 / d1) return n1 * (p -= 1.5 / d1) * p + 0.75;
      if (p < 2.5 / d1) return n1 * (p -= 2.25 / d1) * p + 0.9375;
      return n1 * (p -= 2.625 / d1) * p + 0.984375;
    }
  };

  function clamp01(v) {
    return Math.max(0, Math.min(1, v));
  }

  function formatIndianRupee(num) {
    if (num === null || num === undefined || isNaN(num)) return "₹ 0";
    const n = Math.round(num);
    const isNeg = n < 0;
    const s = Math.abs(n).toString();
    if (s.length <= 3) return (isNeg ? "-₹ " : "₹ ") + s;
    const lastThree = s.substring(s.length - 3);
    const rest = s.substring(0, s.length - 3);
    const formattedRest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return (isNeg ? "-₹ " : "₹ ") + formattedRest + "," + lastThree;
  }

  function formatNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return "0";
    const n = Math.round(num);
    const s = Math.abs(n).toString();
    if (s.length <= 3) return (n < 0 ? "-" : "") + s;
    const lastThree = s.substring(s.length - 3);
    const rest = s.substring(0, s.length - 3);
    const formattedRest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return (n < 0 ? "-" : "") + formattedRest + "," + lastThree;
  }

  function parseAmount(v, defaultVal = 0) {
    if (v === null || v === undefined) return defaultVal;
    if (typeof v === "number") return isNaN(v) ? defaultVal : v;
    const s = String(v).toLowerCase().replace(/,/g, '').replace(/₹/g, '').trim();
    if (!s) return defaultVal;
    if (s.includes('crore') || s.includes('cr')) {
      const m = s.match(/[\d.]+/);
      if (m) return Math.round(parseFloat(m[0]) * 10000000);
    }
    if (s.includes('lakh') || s.includes('lac') || s.includes('l')) {
      const m = s.match(/[\d.]+/);
      if (m) return Math.round(parseFloat(m[0]) * 100000);
    }
    const m = s.match(/[\d.]+/);
    if (m) return Math.round(parseFloat(m[0]));
    return defaultVal;
  }

  function svgEl(tag, attrs = {}, children = []) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v !== null && v !== undefined) el.setAttribute(k, v);
    }
    for (const c of children) {
      if (typeof c === "string") {
        el.appendChild(document.createTextNode(c));
      } else if (c instanceof Node) {
        el.appendChild(c);
      }
    }
    return el;
  }

  function fitText(str, maxW, avgCharW = 9) {
    if (!str) return "";
    const s = String(str);
    const charLimit = Math.floor(maxW / avgCharW);
    if (s.length <= charLimit) return s;
    return s.substring(0, Math.max(3, charLimit - 2)) + "…";
  }

  function svgFittedText(attrs, text, maxW, initialFontSize = 18, isBold = true) {
    let fs = initialFontSize;
    let avgCharW = fs * (isBold ? 0.60 : 0.52);
    let s = String(text !== null && text !== undefined ? text : "");
    if (s.length * avgCharW > maxW && fs > 13) {
      fs = Math.max(12, Math.round(initialFontSize * 0.82));
      avgCharW = fs * (isBold ? 0.60 : 0.52);
    }
    const finalStr = fitText(s, maxW, avgCharW);
    const finalAttrs = Object.assign({}, attrs, { "font-size": fs });
    return svgEl("text", finalAttrs, [finalStr]);
  }


  // -------------------------------------------------------------------------
  // Icon and Token Renderers
  // -------------------------------------------------------------------------
  const ICON_RENDERERS = {
    house: (size, tone) => {
      const g = svgEl("g", { class: "icon-house" });
      const fill = `var(--${tone || "accent"})`;
      g.appendChild(svgEl("path", { d: `M ${size/2} 4 L 4 ${size*0.45} L ${size*0.2} ${size*0.45} L ${size*0.2} ${size - 4} L ${size*0.8} ${size - 4} L ${size*0.8} ${size*0.45} L ${size - 4} ${size*0.45} Z`, fill, stroke: "var(--ink)", "stroke-width": 2 }));
      g.appendChild(svgEl("rect", { x: size*0.4, y: size*0.6, width: size*0.2, height: size*0.36, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 1.5 }));
      return g;
    },
    shares: (size, tone) => {
      const g = svgEl("g", { class: "icon-shares" });
      const fill = `var(--${tone || "ok"})`;
      g.appendChild(svgEl("rect", { x: 4, y: 6, width: size - 8, height: size - 12, rx: 6, fill: "var(--surface)", stroke: fill, "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: size/2, cy: size/2, r: size*0.25, fill: `var(--${tone || "ok"}-soft)` }));
      g.appendChild(svgEl("path", { d: `M ${size*0.25} ${size*0.65} L ${size*0.45} ${size*0.45} L ${size*0.6} ${size*0.55} L ${size*0.75} ${size*0.35}`, fill: "none", stroke: fill, "stroke-width": 2.5, "stroke-linecap": "round" }));
      return g;
    },
    goods: (size, tone) => {
      const g = svgEl("g", { class: "icon-goods" });
      const fill = `var(--${tone || "gold"})`;
      g.appendChild(svgEl("path", { d: `M ${size/2} 4 L ${size - 6} ${size*0.25} L ${size - 6} ${size*0.75} L ${size/2} ${size - 4} L 6 ${size*0.75} L 6 ${size*0.25} Z`, fill: "var(--surface)", stroke: fill, "stroke-width": 2.5 }));
      g.appendChild(svgEl("line", { x1: size/2, y1: 4, x2: size/2, y2: size - 4, stroke: fill, "stroke-width": 2 }));
      g.appendChild(svgEl("line", { x1: 6, y1: size*0.25, x2: size - 6, y2: size*0.25, stroke: fill, "stroke-width": 2 }));
      return g;
    },
    money_bag: (size, tone) => {
      const g = svgEl("g", { class: "icon-money-bag" });
      const fill = `var(--${tone || "gold"})`;
      g.appendChild(svgEl("path", { d: `M ${size*0.3} ${size*0.2} L ${size*0.45} 4 L ${size*0.55} 4 L ${size*0.7} ${size*0.2} C ${size*0.95} ${size*0.45} ${size*0.85} ${size - 4} ${size/2} ${size - 4} C ${size*0.15} ${size - 4} ${size*0.05} ${size*0.45} ${size*0.3} ${size*0.2} Z`, fill: `var(--gold-soft)`, stroke: fill, "stroke-width": 2.5 }));
      g.appendChild(svgEl("text", { x: size/2, y: size*0.68, "text-anchor": "middle", "font-size": Math.round(size*0.42), "font-weight": "900", fill: fill }, ["₹"]));
      return g;
    },
    scale: (size, tone) => {
      const g = svgEl("g", { class: "icon-scale" });
      const fill = `var(--${tone || "accent"})`;
      g.appendChild(svgEl("line", { x1: size/2, y1: 6, x2: size/2, y2: size - 6, stroke: "var(--ink)", "stroke-width": 3 }));
      g.appendChild(svgEl("line", { x1: 6, y1: 16, x2: size - 6, y2: 16, stroke: fill, "stroke-width": 3, "stroke-linecap": "round" }));
      return g;
    },
    clock: (size, tone) => {
      const g = svgEl("g", { class: "icon-clock" });
      const fill = `var(--${tone || "accent"})`;
      g.appendChild(svgEl("circle", { cx: size/2, cy: size/2, r: size/2 - 4, fill: "var(--surface)", stroke: fill, "stroke-width": 2.5 }));
      g.appendChild(svgEl("polyline", { points: `${size/2},${size*0.25} ${size/2},${size/2} ${size*0.7},${size/2}`, fill: "none", stroke: fill, "stroke-width": 2.5, "stroke-linecap": "round" }));
      return g;
    },
    check: (size, tone) => {
      const g = svgEl("g", { class: "icon-check" });
      const fill = `var(--${tone || "ok"})`;
      g.appendChild(svgEl("circle", { cx: size/2, cy: size/2, r: size/2 - 4, fill: `var(--${tone || "ok"}-soft)`, stroke: fill, "stroke-width": 2.5 }));
      g.appendChild(svgEl("path", { d: `M ${size*0.28} ${size*0.52} L ${size*0.44} ${size*0.68} L ${size*0.72} ${size*0.34}`, fill: "none", stroke: fill, "stroke-width": 3, "stroke-linecap": "round", "stroke-linejoin": "round" }));
      return g;
    },
    lock: (size, tone) => {
      const g = svgEl("g", { class: "icon-lock" });
      const fill = `var(--${tone || "warn"})`;
      g.appendChild(svgEl("path", { d: `M ${size*0.3} ${size*0.45} L ${size*0.3} ${size*0.3} C ${size*0.3} ${size*0.14} ${size*0.7} ${size*0.14} ${size*0.7} ${size*0.3} L ${size*0.7} ${size*0.45}`, fill: "none", stroke: fill, "stroke-width": 3 }));
      g.appendChild(svgEl("rect", { x: size*0.2, y: size*0.45, width: size*0.6, height: size*0.48, rx: 6, fill: fill, stroke: "var(--ink)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("circle", { cx: size/2, cy: size*0.65, r: size*0.08, fill: "#ffffff" }));
      return g;
    }
  };

  // Helper: Header Banner
  function renderHeaderBanner(title, tone = "accent") {
    const headerCard = svgEl("g", { transform: "translate(60, 35)" });
    headerCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 55, rx: 12, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": 1.5 }));
    headerCard.appendChild(svgFittedText({ x: 24, y: 35, "font-weight": "900", fill: `var(--${tone})` }, title || "Interactive Scenario", 830, 22, true));
    return headerCard;
  }

  // Helper: Actor Card
  function renderActorCard(x, y, w, h, name, role, tone) {
    const g = svgEl("g", { transform: `translate(${x}, ${y})` });
    g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: 16, fill: "var(--surface)", stroke: `var(--${tone || "accent"})`, "stroke-width": 2 }));
    const avatarR = 26, avatarX = 40, avatarY = h / 2;
    g.appendChild(svgEl("circle", { cx: avatarX, cy: avatarY, r: avatarR, fill: `var(--${tone || "accent"}-soft)`, stroke: `var(--${tone || "accent"})`, "stroke-width": 2 }));
    g.appendChild(svgEl("circle", { cx: avatarX, cy: avatarY - 8, r: 10, fill: `var(--${tone || "accent"})` }));
    g.appendChild(svgEl("path", { d: `M ${avatarX - 16} ${avatarY + 20} Q ${avatarX} ${avatarY + 6} ${avatarX + 16} ${avatarY + 20} Z`, fill: `var(--${tone || "accent"})` }));
    const textX = avatarX + avatarR + 18;
    const maxTextW = w - textX - 16;
    g.appendChild(svgFittedText({ x: textX, y: avatarY - 4, "font-weight": "800", fill: "var(--ink)" }, name || "Party", maxTextW, 19, true));
    g.appendChild(svgFittedText({ x: textX, y: avatarY + 20, "font-weight": "600", fill: "var(--ink-muted)" }, role || "Entity", maxTextW, 14, false));
    return g;
  }

  // Helper: Traveling Item on Parabolic Arc
  function renderTravelingItem(startX, startY, endX, endY, p, arcHeight, label, value, iconType, tone = "accent") {
    const curX = startX + (endX - startX) * p;
    const curY = startY + (endY - startY) * p - (4 * arcHeight * p * (1 - p));
    const tokenW = 190, tokenH = 76;
    const g = svgEl("g", { transform: `translate(${curX - tokenW/2}, ${curY - tokenH/2})` });
    g.appendChild(svgEl("rect", { x: 2, y: 4, width: tokenW, height: tokenH, rx: 14, fill: "var(--shadow)" }));
    g.appendChild(svgEl("rect", { x: 0, y: 0, width: tokenW, height: tokenH, rx: 14, fill: "var(--surface)", stroke: `var(--${tone})`, "stroke-width": 2.5 }));
    const iconFn = ICON_RENDERERS[iconType] || ICON_RENDERERS.goods;
    const iconG = svgEl("g", { transform: "translate(12, 14)" });
    iconG.appendChild(iconFn(48, tone));
    g.appendChild(iconG);
    g.appendChild(svgFittedText({ x: 68, y: 32, "font-weight": "800", fill: "var(--ink)" }, label || "Item", 120, 15, true));
    const valStr = typeof value === "number" ? formatIndianRupee(value) : String(value || "");
    g.appendChild(svgEl("text", { x: 68, y: 56, "font-size": 17, "font-weight": "900", fill: `var(--${tone})` }, [valStr]));
    return g;
  }

  // Helper: Trajectory Guide Line
  function renderTrajectoryGuide(startX, startY, endX, endY, arcHeight, tone = "accent") {
    const midX = (startX + endX) / 2;
    const midY = (startY + endY) / 2 - arcHeight;
    return svgEl("path", {
      d: `M ${startX} ${startY} Q ${midX} ${midY} ${endX} ${endY}`,
      fill: "none",
      stroke: `var(--${tone}-soft)`,
      "stroke-width": 3,
      "stroke-dasharray": "6 5",
      "stroke-linecap": "round"
    });
  }

  // -------------------------------------------------------------------------
  // THE 15 KINETIC ANIMATION BUILDERS
  // -------------------------------------------------------------------------
  const ANIMATIONS = {

    // =========================================================================
    // 1. give_and_receive
    // =========================================================================
    give_and_receive: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueActors = cues.cue_actors || 0.2;
      const cueItem = cues.cue_item || 3.0;
      const cueReturn = cues.cue_payment || 7.5;

      stage.appendChild(renderHeaderBanner(slots.title || "Asset Handover & Settlement", "accent"));

      const pActors = clamp01((t - cueActors) / 1.0);
      const easeActors = Easing.backOut(pActors);
      const giverX = 60, giverY = 150, actorW = 280, actorH = 120;
      const receiverX = 660, receiverY = 150;

      if (pActors > 0) {
        const gGiver = renderActorCard(giverX, giverY, actorW, actorH, slots.giver || "Giver", "Transferor", "accent");
        gGiver.setAttribute("transform", `translate(${giverX}, ${giverY}) scale(${easeActors})`);
        gGiver.style.transformOrigin = `${giverX + actorW/2}px ${giverY + actorH/2}px`;
        stage.appendChild(gGiver);

        const gReceiver = renderActorCard(receiverX, receiverY, actorW, actorH, slots.receiver || "Receiver", "Transferee", "ok");
        gReceiver.setAttribute("transform", `translate(${receiverX}, ${receiverY}) scale(${easeActors})`);
        gReceiver.style.transformOrigin = `${receiverX + actorW/2}px ${receiverY + actorH/2}px`;
        stage.appendChild(gReceiver);
      }

      const itemStartX = giverX + actorW, itemStartY = giverY + actorH / 2;
      const itemEndX = receiverX, itemEndY = receiverY + actorH / 2;
      stage.appendChild(renderTrajectoryGuide(itemStartX, itemStartY, itemEndX, itemEndY, 70, "accent"));

      const payStartX = receiverX, payStartY = receiverY + actorH / 2 + 20;
      const payEndX = giverX + actorW, payEndY = giverY + actorH / 2 + 20;
      stage.appendChild(renderTrajectoryGuide(payStartX, payStartY, payEndX, payEndY, -70, "gold"));

      if (t >= cueItem) {
        const pItem = clamp01((t - cueItem) / 1.5);
        const easeItem = Easing.easeInOut(pItem);
        const targetVal = parseAmount(slots.item_value ?? slots.val ?? slots.amount, 0);
        const curVal = Math.round(targetVal * easeItem);
        stage.appendChild(renderTravelingItem(
          itemStartX, itemStartY, itemEndX, itemEndY,
          easeItem, 70,
          slots.item_label || "Capital Asset",
          curVal,
          slots.item_icon || "house",
          "accent"
        ));
      }

      if (t >= cueReturn) {
        const pReturn = clamp01((t - cueReturn) / 1.5);
        const easeReturn = Easing.easeInOut(pReturn);
        const paymentAmt = parseAmount(slots.payment_amount ?? slots.payment_val ?? slots.payment, 0);

        if (paymentAmt > 0) {
          const curPayVal = Math.round(paymentAmt * easeReturn);
          stage.appendChild(renderTravelingItem(
            payStartX, payStartY, payEndX, payEndY,
            easeReturn, -70,
            "Payment Settlement",
            curPayVal,
            "money_bag",
            "gold"
          ));
        } else {
          const stampP = clamp01((t - cueReturn) / 0.6);
          const stampScale = Easing.backOut(stampP);
          const gStamp = svgEl("g", { transform: `translate(420, 290) scale(${stampScale})` });
          gStamp.style.transformOrigin = "500px 310px";
          gStamp.appendChild(svgEl("rect", { x: -80, y: -20, width: 160, height: 40, rx: 10, fill: "var(--warn-soft)", stroke: "var(--warn)", "stroke-width": 2 }));
          gStamp.appendChild(svgEl("text", { x: 0, y: 6, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--warn)" }, ["No Payment Returned"]));
          stage.appendChild(gStamp);
        }

        if (t >= cueReturn + 0.8) {
          const pNote = clamp01((t - (cueReturn + 0.8)) / 0.6);
          const noteY = 410 + (1 - Easing.easeOut(pNote)) * 40;
          const noteCard = svgEl("g", { transform: `translate(60, ${noteY})`, opacity: pNote });
          const isSettled = paymentAmt > 0;
          const tone = isSettled ? "ok" : "accent";
          noteCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 80, rx: 14, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": 2 }));
          noteCard.appendChild(svgFittedText({ x: 30, y: 35, "font-weight": "800", fill: "var(--ink)" }, slots.tag_text || (isSettled ? "Commercial Settlement Transfer Complete" : "Unilateral Transfer / Gift Handover Complete"), 690, 18, true));
          noteCard.appendChild(svgFittedText({ x: 30, y: 62, "font-weight": "600", fill: "var(--ink-muted)" }, slots.note || (isSettled ? "Payment received fulfills agreement terms." : "Asset transferred without monetary return."), 690, 15, false));

          const checkPill = svgEl("g", { transform: "translate(740, 22)" });
          checkPill.appendChild(svgEl("rect", { x: 0, y: 0, width: 110, height: 36, rx: 18, fill: `var(--${tone})` }));
          checkPill.appendChild(svgEl("text", { x: 55, y: 24, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "#ffffff" }, ["Settled"]));
          noteCard.appendChild(checkPill);
          stage.appendChild(noteCard);
        }
      }

      return stage;
    },

    // =========================================================================
    // 2. swap (Dual crossing arcs with value compare)
    // =========================================================================
    swap: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueParties = cues.cue_parties || 0.2;
      const cueCrossing = cues.cue_crossing || 3.0;
      const cueCompare = cues.cue_compare || 8.0;

      stage.appendChild(renderHeaderBanner(slots.title || "Bilateral Asset Exchange", "accent"));

      const pParties = clamp01((t - cueParties) / 0.9);
      const easeParties = Easing.backOut(pParties);
      const partyAX = 60, partyAY = 140, partyW = 270, partyH = 115;
      const partyBX = 670, partyBY = 140;

      if (pParties > 0) {
        const gA = renderActorCard(partyAX, partyAY, partyW, partyH, slots.party_a || "Party Alpha", "Initiator", "accent");
        gA.setAttribute("transform", `translate(${partyAX}, ${partyAY}) scale(${easeParties})`);
        gA.style.transformOrigin = `${partyAX + partyW/2}px ${partyAY + partyH/2}px`;
        stage.appendChild(gA);

        const gB = renderActorCard(partyBX, partyBY, partyW, partyH, slots.party_b || "Party Beta", "Counterparty", "ok");
        gB.setAttribute("transform", `translate(${partyBX}, ${partyBY}) scale(${easeParties})`);
        gB.style.transformOrigin = `${partyBX + partyW/2}px ${partyBY + partyH/2}px`;
        stage.appendChild(gB);
      }

      const aStartX = partyAX + partyW, aStartY = partyAY + 40;
      const aEndX = partyBX, aEndY = partyBY + 40;
      stage.appendChild(renderTrajectoryGuide(aStartX, aStartY, aEndX, aEndY, 75, "accent"));

      const bStartX = partyBX, bStartY = partyBY + 75;
      const bEndX = partyAX + partyW, bEndY = partyAY + 75;
      stage.appendChild(renderTrajectoryGuide(bStartX, bStartY, bEndX, bEndY, -75, "ok"));

      const valA = parseAmount(slots.item_a_val ?? (slots.item_a ? (slots.item_a.val ?? slots.item_a.amount) : null), 3200000);
      const valB = parseAmount(slots.item_b_val ?? (slots.item_b ? (slots.item_b.val ?? slots.item_b.amount) : null), 2700000);

      if (t >= cueCrossing) {
        const pCross = clamp01((t - cueCrossing) / 1.8);
        const easeCross = Easing.easeInOut(pCross);

        const curValA = Math.round(valA * easeCross);
        const itemANode = renderTravelingItem(
          aStartX, aStartY, aEndX, aEndY,
          easeCross, 75,
          slots.item_a_label || (slots.item_a ? slots.item_a.label : null) || "Asset Alpha",
          curValA,
          slots.item_a_icon || (slots.item_a ? slots.item_a.icon : null) || "goods",
          "accent"
        );
        stage.appendChild(itemANode);

        const curValB = Math.round(valB * easeCross);
        const itemBNode = renderTravelingItem(
          bStartX, bStartY, bEndX, bEndY,
          easeCross, -75,
          slots.item_b_label || (slots.item_b ? slots.item_b.label : null) || "Asset Beta",
          curValB,
          slots.item_b_icon || (slots.item_b ? slots.item_b.icon : null) || "shares",
          "ok"
        );
        stage.appendChild(itemBNode);
      }

      if (t >= cueCompare) {
        const pComp = clamp01((t - cueCompare) / 0.8);
        const easeComp = Easing.backOut(pComp);
        const isEqual = valA === valB;
        const diff = Math.abs(valA - valB);
        const compTone = isEqual ? "ok" : "gold";

        const compG = svgEl("g", { transform: `translate(280, ${340 + (1 - easeComp)*25}) scale(${easeComp})` });
        compG.style.transformOrigin = "440px 390px";
        compG.appendChild(svgEl("rect", { x: 0, y: 0, width: 440, height: 95, rx: 16, fill: `var(--${compTone}-soft)`, stroke: `var(--${compTone})`, "stroke-width": 2 }));

        const badgeText = isEqual ? "Balanced 1:1 Value Match" : `Differential Balance: ${formatIndianRupee(diff)}`;
        compG.appendChild(svgEl("text", { x: 220, y: 38, "text-anchor": "middle", "font-size": 20, "font-weight": "900", fill: `var(--${compTone})` }, [badgeText]));
        const subText = isEqual ? "Both exchange assets possess equivalent monetary valuation." : "Monetary settlement required to balance unequal exchange values.";
        compG.appendChild(svgEl("text", { x: 220, y: 68, "text-anchor": "middle", "font-size": 15, "font-weight": "600", fill: "var(--ink-muted)" }, [subText]));
        stage.appendChild(compG);

        const footCard = svgEl("g", { transform: "translate(60, 460)", opacity: pComp });
        footCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 60, rx: 12, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
        footCard.appendChild(svgEl("text", { x: 24, y: 36, "font-size": 16, "font-weight": "700", fill: "var(--ink)" }, ["Exchange Settlement Verification: Mutual asset transfer concluded with verified valuation base."]));
        stage.appendChild(footCard);
      }

      return stage;
    },

    // =========================================================================
    // 3. split_into_parts (Block cracks and divides into N cards)
    // =========================================================================
    split_into_parts: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueWhole = cues.cue_whole || 0.5;
      const cueCrack = cues.cue_crack || 3.5;
      const cueParts = cues.cue_parts || 6.5;
      const cueVerify = cues.cue_verify || 10.5;

      stage.appendChild(renderHeaderBanner(slots.title || "Entity Partition & Allocation", "accent"));

      const rawParts = slots.parts || slots.chunks || slots.branches || [];
      const parts = rawParts.length > 0 ? rawParts.map(p => ({
        label: p.label || p.title || p.text || "Allocation Branch",
        amount: parseAmount(p.amount ?? p.val ?? p.value, 0)
      })) : [
        { label: "Allocation Branch One", amount: 2500000 },
        { label: "Allocation Branch Two", amount: 2000000 },
        { label: "Residual Allocation", amount: 1500000 }
      ];
      const wholeAmt = parseAmount(slots.whole_amount ?? slots.whole_val, 6000000);
      const numParts = Math.max(2, Math.min(5, parts.length));

      // Upper Whole Block
      const wholeX = 260, wholeY = 110, wholeW = 480, wholeH = 105;
      const pWhole = clamp01((t - cueWhole) / 0.8);
      const easeWhole = Easing.backOut(pWhole);

      let crackShake = 0;
      if (t >= cueCrack && t < cueParts) {
        crackShake = Math.sin((t - cueCrack) * 25) * 4;
      }

      const wholeCard = svgEl("g", { transform: `translate(${wholeX + crackShake}, ${wholeY}) scale(${easeWhole})` });
      wholeCard.style.transformOrigin = `${wholeX + wholeW/2}px ${wholeY + wholeH/2}px`;
      wholeCard.appendChild(svgEl("rect", { x: 0, y: 0, width: wholeW, height: wholeH, rx: 16, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      wholeCard.appendChild(svgEl("text", { x: wholeW/2, y: 40, "text-anchor": "middle", "font-size": 20, "font-weight": "800", fill: "var(--ink)" }, [slots.whole_label || "Unified Total Base"]));
      const curWhole = Math.round(wholeAmt * pWhole);
      wholeCard.appendChild(svgEl("text", { x: wholeW/2, y: 78, "text-anchor": "middle", "font-size": 26, "font-weight": "900", fill: "var(--accent)" }, [formatIndianRupee(curWhole)]));

      // Crack fracture line
      if (t >= cueCrack) {
        const pCrack = clamp01((t - cueCrack) / 1.0);
        const crackD = "M 240 10 L 230 40 L 255 65 L 235 95 L 245 105";
        const crackPath = svgEl("path", {
          d: crackD, fill: "none", stroke: "var(--warn)", "stroke-width": 4, "stroke-linecap": "round",
          "stroke-dasharray": "120", "stroke-dashoffset": `${(1 - pCrack) * 120}`
        });
        wholeCard.appendChild(crackPath);
      }
      stage.appendChild(wholeCard);

      // Parts sliding down
      if (t >= cueParts) {
        const pParts = clamp01((t - cueParts) / 1.6);
        const easeParts = Easing.bounceOut(pParts);

        const totalW = 880;
        const gap = 16;
        const cardW = Math.floor((totalW - (numParts - 1) * gap) / numParts);
        const targetY = 250;

        parts.slice(0, numParts).forEach((part, idx) => {
          const targetX = 60 + idx * (cardW + gap);
          // Travel from whole block center downwards
          const startX = wholeX + wholeW / 2 - cardW / 2;
          const startY = wholeY + wholeH;
          const curX = startX + (targetX - startX) * easeParts;
          const curY = startY + (targetY - startY) * easeParts;

          const partG = svgEl("g", { transform: `translate(${curX}, ${curY})` });
          partG.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW, height: 160, rx: 14, fill: "var(--surface)", stroke: "var(--ok)", "stroke-width": 2 }));

          // Percent badge
          const pct = Math.round(((part.amount || 0) / wholeAmt) * 100);
          partG.appendChild(svgEl("rect", { x: 14, y: 14, width: 62, height: 28, rx: 14, fill: "var(--ok-soft)" }));
          partG.appendChild(svgEl("text", { x: 45, y: 33, "text-anchor": "middle", "font-size": 15, "font-weight": "900", fill: "var(--ok)" }, [`${pct}%`]));

          // Label
          partG.appendChild(svgEl("text", { x: 14, y: 72, "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [part.label || `Branch ${idx+1}`]));

          // Count-up amount
          const curPartAmt = Math.round((part.amount || 0) * pParts);
          partG.appendChild(svgEl("text", { x: 14, y: 110, "font-size": 20, "font-weight": "900", fill: "var(--ok)" }, [formatIndianRupee(curPartAmt)]));

          // Share indicator bar
          partG.appendChild(svgEl("rect", { x: 14, y: 130, width: cardW - 28, height: 8, rx: 4, fill: "var(--line)" }));
          partG.appendChild(svgEl("rect", { x: 14, y: 130, width: (cardW - 28) * (pct / 100) * pParts, height: 8, rx: 4, fill: "var(--ok)" }));

          stage.appendChild(partG);
        });
      }

      // Reconciliation verification banner
      if (t >= cueVerify) {
        const pVer = clamp01((t - cueVerify) / 0.8);
        const easeVer = Easing.backOut(pVer);
        const verCard = svgEl("g", { transform: `translate(60, ${440 + (1 - easeVer)*25}) scale(${easeVer})` });
        verCard.style.transformOrigin = "500px 470px";
        verCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 65, rx: 14, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 2 }));
        verCard.appendChild(svgEl("text", { x: 30, y: 40, "font-size": 18, "font-weight": "900", fill: "var(--ok)" }, ["Allocation Verification: 100% of Unified Total Base Reconciles Perfectly across Allocated Branches"]));
        stage.appendChild(verCard);
      }

      return stage;
    },

    // =========================================================================
    // 4. merge_into_one (Cards slide inward to center and fuse with shockwave)
    // =========================================================================
    merge_into_one: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueInputs = cues.cue_inputs || 0.5;
      const cueSlide = cues.cue_slide || 4.0;
      const cueFuse = cues.cue_fuse || 7.5;
      const cueTotal = cues.cue_total || 10.0;

      stage.appendChild(renderHeaderBanner(slots.title || "Stream Convergence & Fusion", "accent"));

      const rawInputs = slots.inputs || slots.streams || slots.items || [];
      const inputs = rawInputs.length > 0 ? rawInputs.map(i => ({
        label: i.label || i.title || i.text || "Input Entity",
        amount: parseAmount(i.amount ?? i.val ?? i.value, 0)
      })) : [
        { label: "Input Entity Alpha", amount: 2800000 },
        { label: "Input Entity Beta", amount: 3200000 }
      ];
      const numInputs = Math.max(2, Math.min(5, inputs.length));
      const totalSum = inputs.reduce((acc, it) => acc + (it.amount || 0), 0);

      const fusionPoint = { x: 500, y: 220 };
      const gap = 20, totalW = 880;
      const cardW = Math.floor((totalW - (numInputs - 1) * gap) / numInputs);
      const initialY = 130;

      // Inputs sliding to center
      if (t < cueFuse) {
        const pSlide = t >= cueSlide ? clamp01((t - cueSlide) / 3.0) : 0;
        const easeSlide = Easing.easeInOut(pSlide);

        inputs.slice(0, numInputs).forEach((inp, idx) => {
          const initX = 60 + idx * (cardW + gap);
          const curX = initX + (fusionPoint.x - (initX + cardW/2)) * easeSlide;
          const curY = initialY + (fusionPoint.y - (initialY + 60)) * easeSlide;
          const curScale = 1.0 - 0.5 * easeSlide;

          const card = svgEl("g", { transform: `translate(${curX}, ${curY}) scale(${curScale})` });
          card.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW, height: 120, rx: 14, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2 }));
          card.appendChild(svgEl("text", { x: cardW/2, y: 45, "text-anchor": "middle", "font-size": 17, "font-weight": "800", fill: "var(--ink)" }, [inp.label || `Entity ${idx+1}`]));
          card.appendChild(svgEl("text", { x: cardW/2, y: 85, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--accent)" }, [formatIndianRupee(inp.amount || 0)]));
          stage.appendChild(card);
        });
      }

      // Fusion shockwave
      if (t >= cueFuse && t < cueFuse + 1.2) {
        const pWave = clamp01((t - cueFuse) / 1.0);
        const waveR = 20 + pWave * 160;
        const waveOpacity = 1 - pWave;
        stage.appendChild(svgEl("circle", { cx: fusionPoint.x, cy: fusionPoint.y, r: waveR, fill: "none", stroke: "var(--gold)", "stroke-width": 4, opacity: waveOpacity }));
        stage.appendChild(svgEl("circle", { cx: fusionPoint.x, cy: fusionPoint.y, r: waveR * 0.7, fill: "none", stroke: "var(--accent)", "stroke-width": 3, opacity: waveOpacity }));
      }

      // Emerged unified whole card
      if (t >= cueFuse) {
        const pEmerg = clamp01((t - cueFuse) / 1.2);
        const easeEmerg = Easing.backOut(pEmerg);
        const mergedW = 600, mergedH = 175;
        const mergedX = 500 - mergedW / 2;
        const mergedY = 170;

        const mergedCard = svgEl("g", { transform: `translate(${mergedX}, ${mergedY}) scale(${easeEmerg})` });
        mergedCard.style.transformOrigin = `${mergedX + mergedW/2}px ${mergedY + mergedH/2}px`;
        mergedCard.appendChild(svgEl("rect", { x: 0, y: 0, width: mergedW, height: mergedH, rx: 20, fill: "var(--surface)", stroke: "var(--ok)", "stroke-width": 3.5 }));

        // Glow ring
        mergedCard.appendChild(svgEl("rect", { x: -4, y: -4, width: mergedW + 8, height: mergedH + 8, rx: 24, fill: "none", stroke: "var(--ok-soft)", "stroke-width": 4, opacity: 0.6 }));

        // Content
        mergedCard.appendChild(svgEl("text", { x: mergedW/2, y: 48, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--ink)" }, [slots.result_label || slots.merged_label || "Combined Unified Whole"]));

        const pCount = t >= cueTotal ? 1.0 : clamp01((t - cueFuse) / (cueTotal - cueFuse));
        const curMergedVal = Math.round(totalSum * pCount);
        mergedCard.appendChild(svgEl("text", { x: mergedW/2, y: 105, "text-anchor": "middle", "font-size": 36, "font-weight": "900", fill: "var(--ok)" }, [formatIndianRupee(curMergedVal)]));

        mergedCard.appendChild(svgEl("rect", { x: mergedW/2 - 120, y: 125, width: 240, height: 32, rx: 16, fill: "var(--ok-soft)" }));
        mergedCard.appendChild(svgEl("text", { x: mergedW/2, y: 147, "text-anchor": "middle", "font-size": 15, "font-weight": "900", fill: "var(--ok)" }, ["Fusion & Convergence Complete"]));

        stage.appendChild(mergedCard);

        // Bottom summary note
        const footCard = svgEl("g", { transform: "translate(60, 435)", opacity: pEmerg });
        footCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 65, rx: 14, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1.5 }));
        footCard.appendChild(svgEl("text", { x: 30, y: 40, "font-size": 17, "font-weight": "800", fill: "var(--accent)" }, ["Composite Settlement: All contributing input streams have fused into a single unified whole."]));
        stage.appendChild(footCard);
      }

      return stage;
    },

    // =========================================================================
    // 5. add_up (Dropping rows with continuous running total meter)
    // =========================================================================
    add_up: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const rawItems = slots.items || slots.rows || slots.steps || [];
      const items = rawItems.length > 0 ? rawItems.map(it => ({
        label: it.label || it.title || it.text || "Component",
        amount: parseAmount(it.amount ?? it.val ?? it.value, 0)
      })) : [
        { label: "Base Component One", amount: 1200000 },
        { label: "Secondary Component Two", amount: 450000 },
        { label: "Supplemental Addition", amount: 250000 }
      ];

      stage.appendChild(renderHeaderBanner(slots.title || "Summation & Aggregation Ladder", "accent"));

      const stackX = 60, stackY = 110, stackW = 540;
      const numItems = Math.min(7, items.length);
      const rowH = Math.min(54, Math.floor(340 / numItems));
      const rowGap = 8;

      let runningTotal = 0;
      const dropDuration = (duration - 3.5) / numItems;

      items.slice(0, numItems).forEach((item, idx) => {
        const itemCue = (cues[`cue_row_${idx+1}`] !== undefined) ? cues[`cue_row_${idx+1}`] : (1.0 + idx * dropDuration);
        const pDrop = clamp01((t - itemCue) / 0.8);
        if (pDrop <= 0) return;

        const easeDrop = Easing.bounceOut(pDrop);
        const targetY = stackY + idx * (rowH + rowGap);
        const curY = targetY - (1 - easeDrop) * 80;

        const rowG = svgEl("g", { transform: `translate(${stackX}, ${curY})` });
        rowG.appendChild(svgEl("rect", { x: 0, y: 0, width: stackW, height: rowH, rx: 10, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 2 }));
        rowG.appendChild(svgEl("circle", { cx: 28, cy: rowH/2, r: 14, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 1.5 }));
        rowG.appendChild(svgEl("text", { x: 28, y: rowH/2 + 5, "text-anchor": "middle", "font-size": 18, "font-weight": "900", fill: "var(--ok)" }, ["+"]));
        rowG.appendChild(svgEl("text", { x: 56, y: rowH/2 + 6, "font-size": 17, "font-weight": "800", fill: "var(--ink)" }, [item.label || `Item ${idx+1}`]));

        const rowAmt = item.amount || 0;
        const curRowAmt = Math.round(rowAmt * pDrop);
        rowG.appendChild(svgEl("text", { x: stackW - 20, y: rowH/2 + 6, "text-anchor": "end", "font-size": 17, "font-weight": "900", fill: "var(--ink)" }, [formatIndianRupee(curRowAmt)]));

        stage.appendChild(rowG);
        runningTotal += curRowAmt;
      });

      const meterX = 620, meterY = 110, meterW = 320, meterH = 360;
      const meterCard = svgEl("g", { transform: `translate(${meterX}, ${meterY})` });
      meterCard.appendChild(svgEl("rect", { x: 0, y: 0, width: meterW, height: meterH, rx: 18, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      meterCard.appendChild(svgEl("rect", { x: 0, y: 0, width: meterW, height: 60, rx: 18, fill: "var(--accent)" }));
      meterCard.appendChild(svgEl("text", { x: meterW/2, y: 38, "text-anchor": "middle", "font-size": 19, "font-weight": "900", fill: "#ffffff" }, [slots.total_label || "Aggregated Total Result"]));
      meterCard.appendChild(svgEl("circle", { cx: meterW/2, cy: 175, r: 75, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 2 }));
      meterCard.appendChild(svgEl("text", { x: meterW/2, y: 184, "text-anchor": "middle", "font-size": 28, "font-weight": "900", fill: "var(--accent)" }, [formatIndianRupee(runningTotal)]));

      const cueFinal = cues.cue_final || (duration - 2.0);
      if (t >= cueFinal) {
        const pFinal = clamp01((t - cueFinal) / 0.8);
        const easeFinal = Easing.backOut(pFinal);
        const badgeG = svgEl("g", { transform: `translate(${meterW/2}, 300) scale(${easeFinal})` });
        badgeG.style.transformOrigin = `${meterW/2}px 300px`;
        badgeG.appendChild(svgEl("rect", { x: -110, y: -22, width: 220, height: 44, rx: 22, fill: "var(--ok)", stroke: "var(--ink)", "stroke-width": 1.5 }));
        badgeG.appendChild(svgEl("text", { x: 0, y: 6, "text-anchor": "middle", "font-size": 17, "font-weight": "900", fill: "#ffffff" }, ["Total Complete"]));
        meterCard.appendChild(badgeG);
      }

      stage.appendChild(meterCard);
      return stage;
    },

    // =========================================================================
    // 6. take_away (Tall bar with slicing reduction chunks and net remainder)
    // =========================================================================
    take_away: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueStart = cues.cue_start || 0.5;
      const cueResult = cues.cue_result || 10.5;

      stage.appendChild(renderHeaderBanner(slots.title || "Sequential Subtraction & Remainder", "accent"));

      const startAmt = parseAmount(slots.start_amount ?? slots.whole_val ?? slots.whole_amount ?? slots.start_val, 5000000);
      const rawSteps = slots.steps || slots.chunks || slots.deductions || slots.slices || [];
      const steps = rawSteps.length > 0 ? rawSteps.map(s => ({
        label: s.label || s.title || s.text || "Outflow Step",
        amount: parseAmount(s.amount ?? s.val ?? s.value, 0)
      })) : [
        { label: "Primary Outflow Step", amount: 1200000 },
        { label: "Secondary Outflow Step", amount: 1500000 }
      ];

      const pStart = clamp01((t - cueStart) / 1.5);
      const easeStart = Easing.easeOut(pStart);

      // Left column: Tall Vertical Bar
      const colX = 70, colY = 110, colW = 260, colH = 390;
      const leftCol = svgEl("g", { transform: `translate(${colX}, ${colY})` });
      leftCol.appendChild(svgEl("rect", { x: 0, y: 0, width: colW, height: colH, rx: 16, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2 }));
      leftCol.appendChild(svgEl("text", { x: colW/2, y: 35, "text-anchor": "middle", "font-size": 18, "font-weight": "800", fill: "var(--ink)" }, [slots.start_label || slots.whole_label || "Initial Gross Value"]));
      const curGross = Math.round(startAmt * easeStart);
      leftCol.appendChild(svgEl("text", { x: colW/2, y: 65, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--accent)" }, [formatIndianRupee(curGross)]));

      // Bar container & fill
      const barX = 40, barBaseY = 360, barW = colW - 80, maxBarH = 260;
      leftCol.appendChild(svgEl("rect", { x: barX, y: barBaseY - maxBarH, width: barW, height: maxBarH, rx: 8, fill: "var(--surface-card)", stroke: "var(--line)", "stroke-width": 1.5 }));

      // Slicing reductions
      let remainingAmt = startAmt;
      let totalReductionsSoFar = 0;
      const rightColX = 360;

      steps.forEach((step, idx) => {
        const cueSlice = cues[`cue_slice_${idx+1}`] || (3.5 + idx * 3.5);
        const pSlice = clamp01((t - cueSlice) / 1.5);
        const easeSlice = Easing.easeInOut(pSlice);

        const sliceAmt = step.amount || 0;
        const curSliceAmt = Math.round(sliceAmt * easeSlice);
        totalReductionsSoFar += curSliceAmt;

        // Reduction card on the right
        if (pSlice > 0) {
          const targetY = 110 + idx * 95;
          const startSlideX = colX + colW;
          const curSlideX = startSlideX + (rightColX - startSlideX) * easeSlice;

          const sliceCard = svgEl("g", { transform: `translate(${curSlideX}, ${targetY})` });
          sliceCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 570, height: 75, rx: 14, fill: "var(--surface)", stroke: "var(--warn)", "stroke-width": 2 }));

          // Minus badge
          sliceCard.appendChild(svgEl("circle", { cx: 35, cy: 37, r: 18, fill: "var(--warn-soft)", stroke: "var(--warn)", "stroke-width": 1.5 }));
          sliceCard.appendChild(svgEl("text", { x: 35, y: 44, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--warn)" }, ["−"]));

          sliceCard.appendChild(svgEl("text", { x: 70, y: 44, "font-size": 18, "font-weight": "800", fill: "var(--ink)" }, [step.label || `Reduction ${idx+1}`]));
          sliceCard.appendChild(svgEl("text", { x: 540, y: 44, "text-anchor": "end", "font-size": 20, "font-weight": "900", fill: "var(--warn)" }, [formatIndianRupee(curSliceAmt)]));

          stage.appendChild(sliceCard);
        }
      });

      // Height of remaining bar shrinks as reductions take effect
      const effectiveRemaining = Math.max(0, startAmt * easeStart - totalReductionsSoFar);
      const curBarH = (effectiveRemaining / startAmt) * maxBarH;
      const barTone = effectiveRemaining > 0 ? "ok" : "warn";
      leftCol.appendChild(svgEl("rect", { x: barX, y: barBaseY - curBarH, width: barW, height: curBarH, rx: 8, fill: `var(--${barTone})`, opacity: 0.85 }));

      stage.appendChild(leftCol);

      // Result Card at Bottom Right
      if (t >= cueResult) {
        const pRes = clamp01((t - cueResult) / 0.8);
        const easeRes = Easing.backOut(pRes);
        const netY = 110 + steps.length * 95 + 15;
        const resCard = svgEl("g", { transform: `translate(${rightColX}, ${netY}) scale(${easeRes})` });
        resCard.style.transformOrigin = `${rightColX + 285}px ${netY + 45}px`;
        resCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 570, height: 85, rx: 16, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 2.5 }));
        resCard.appendChild(svgEl("text", { x: 30, y: 36, "font-size": 18, "font-weight": "900", fill: "var(--ok)" }, [slots.result_label || "Net Remainder Result"]));
        const finalNet = startAmt - steps.reduce((a, b) => a + (b.amount || 0), 0);
        resCard.appendChild(svgEl("text", { x: 30, y: 68, "font-size": 24, "font-weight": "900", fill: "var(--ink)" }, [formatIndianRupee(finalNet)]));

        const okPill = svgEl("g", { transform: "translate(440, 24)" });
        okPill.appendChild(svgEl("rect", { x: 0, y: 0, width: 100, height: 36, rx: 18, fill: "var(--ok)" }));
        okPill.appendChild(svgEl("text", { x: 50, y: 24, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: "#ffffff" }, ["Net Balance"]));
        resCard.appendChild(okPill);

        stage.appendChild(resCard);
      }

      return stage;
    },

    // =========================================================================
    // 7. compare_two
    // =========================================================================
    compare_two: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueBars = cues.cue_bars || 0.5;
      const cueScale = cues.cue_scale || 4.5;
      const cueWinner = cues.cue_winner || 8.5;

      const valA = parseAmount(slots.val_a ?? slots.val_1 ?? slots.amount_a, 1800000);
      const valB = parseAmount(slots.val_b ?? slots.val_2 ?? slots.amount_b, 2500000);
      const mode = (slots.mode || "higher").toLowerCase();
      const capVal = slots.cap_amount ? parseAmount(slots.cap_amount) : null;

      let winnerIsA = mode === "higher" ? (valA > valB) : (valA < valB);
      const isTie = valA === valB;

      const modeLabel = mode === "higher" ? "Higher of Two Values Decision" : "Lower of Two Values Decision";
      stage.appendChild(renderHeaderBanner(slots.title || modeLabel, "accent"));

      const pGrow = clamp01((t - cueBars) / 3.0);
      const easeGrow = Easing.easeOut(pGrow);

      const maxVal = Math.max(valA, valB, capVal || 0) * 1.25;
      const maxBarH = 180;
      const hA = Math.max(20, (valA / maxVal) * maxBarH * easeGrow);
      const hB = Math.max(20, (valB / maxVal) * maxBarH * easeGrow);

      const curValA = Math.round(valA * easeGrow);
      const curValB = Math.round(valB * easeGrow);

      const isPostWinner = t >= cueWinner;
      const pWinLift = isPostWinner ? clamp01((t - cueWinner) / 0.8) : 0;
      const easeLift = Easing.backOut(pWinLift);
      const liftA = winnerIsA ? -24 * easeLift : 12 * easeLift;
      const liftB = !winnerIsA && !isTie ? -24 * easeLift : 12 * easeLift;
      const toneA = isPostWinner ? (winnerIsA ? "ok" : "surface") : "accent";
      const toneB = isPostWinner ? (!winnerIsA && !isTie ? "ok" : "surface") : "gold";

      const colAX = 140, colW = 180;
      const cardA = svgEl("g", { transform: `translate(${colAX}, ${115 + liftA})` });
      cardA.appendChild(svgFittedText({ x: colW/2, y: 35, "text-anchor": "middle", "font-weight": "800", fill: "var(--ink)" }, slots.label_a || "Benchmark A", colW - 20, 17, true));
      cardA.appendChild(svgEl("text", { x: colW/2, y: 70, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: `var(--${toneA})` }, [formatIndianRupee(curValA)]));
      cardA.appendChild(svgEl("rect", { x: 30, y: 260 - hA, width: colW - 60, height: hA, rx: 8, fill: `var(--${toneA}-soft)`, stroke: `var(--${toneA})`, "stroke-width": 2 }));
      stage.appendChild(cardA);

      const colBX = 680, colBW = 180;
      const cardB = svgEl("g", { transform: `translate(${colBX}, ${115 + liftB})` });
      cardB.appendChild(svgEl("rect", { x: 0, y: 0, width: colBW, height: 285, rx: 14, fill: "var(--surface)", stroke: `var(--${toneB})`, "stroke-width": (!winnerIsA && !isTie && isPostWinner) ? 3.5 : 2 }));
      cardB.appendChild(svgFittedText({ x: colBW/2, y: 35, "text-anchor": "middle", "font-weight": "800", fill: "var(--ink)" }, slots.label_b || "Benchmark B", colBW - 20, 17, true));
      cardB.appendChild(svgEl("text", { x: colBW/2, y: 70, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: `var(--${toneB})` }, [formatIndianRupee(curValB)]));
      cardB.appendChild(svgEl("rect", { x: 30, y: 260 - hB, width: colBW - 60, height: hB, rx: 8, fill: `var(--${toneB}-soft)`, stroke: `var(--${toneB})`, "stroke-width": 2 }));
      stage.appendChild(cardB);

      const scalePivotX = 500, scalePivotY = 220;
      let tiltAngle = 0;
      if (t >= cueScale) {
        const pTilt = clamp01((t - cueScale) / 1.5);
        const easeTilt = Easing.easeInOut(pTilt);
        const targetAngle = isTie ? 0 : (winnerIsA ? -18 : 18);
        tiltAngle = targetAngle * easeTilt;
      }

      const scaleG = svgEl("g", { transform: `translate(${scalePivotX}, ${scalePivotY})` });
      scaleG.appendChild(svgEl("line", { x1: 0, y1: 0, x2: 0, y2: 120, stroke: "var(--ink)", "stroke-width": 4 }));
      scaleG.appendChild(svgEl("polygon", { points: "-35,125 35,125 0,110", fill: "var(--ink)" }));

      const beamG = svgEl("g", { transform: `rotate(${tiltAngle})` });
      beamG.appendChild(svgEl("line", { x1: -110, y1: 0, x2: 110, y2: 0, stroke: "var(--accent)", "stroke-width": 5, "stroke-linecap": "round" }));
      beamG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 7, fill: "var(--ink)" }));
      beamG.appendChild(svgEl("line", { x1: -110, y1: 0, x2: -110, y2: 40, stroke: "var(--line)", "stroke-width": 2 }));
      beamG.appendChild(svgEl("path", { d: "M -140 40 Q -110 52 -80 40 Z", fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2 }));
      beamG.appendChild(svgEl("line", { x1: 110, y1: 0, x2: 110, y2: 40, stroke: "var(--line)", "stroke-width": 2 }));
      beamG.appendChild(svgEl("path", { d: "M 80 40 Q 110 52 140 40 Z", fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2 }));
      scaleG.appendChild(beamG);
      stage.appendChild(scaleG);

      if (capVal && capVal > 0) {
        const capY = 375 - ((capVal / maxVal) * maxBarH);
        const capG = svgEl("g");
        capG.appendChild(svgEl("line", { x1: 100, y1: capY, x2: 900, y2: capY, stroke: "var(--warn)", "stroke-width": 2.5, "stroke-dasharray": "6 4" }));
        capG.appendChild(svgEl("rect", { x: 420, y: capY - 14, width: 160, height: 28, rx: 6, fill: "var(--warn-soft)", stroke: "var(--warn)", "stroke-width": 1.5 }));
        capG.appendChild(svgEl("text", { x: 500, y: capY + 5, "text-anchor": "middle", "font-size": 15, "font-weight": "800", fill: "var(--warn)" }, [`Limit Cap: ${formatIndianRupee(capVal)}`]));
        stage.appendChild(capG);
      }

      if (t >= cueWinner) {
        const pWin = clamp01((t - cueWinner) / 0.8);
        const winY = 420 + (1 - Easing.easeOut(pWin)) * 30;
        const winCard = svgEl("g", { transform: `translate(60, ${winY})`, opacity: pWin });
        winCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 75, rx: 14, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 2 }));

        const winningVal = winnerIsA ? valA : valB;
        const effectiveVal = (capVal && winningVal > capVal) ? capVal : winningVal;
        const winnerName = winnerIsA ? (slots.label_a || "Benchmark A") : (slots.label_b || "Benchmark B");

        winCard.appendChild(svgEl("text", { x: 30, y: 34, "font-size": 18, "font-weight": "800", fill: "var(--ink)" }, [`Decision Result: ${winnerName} Selected`]));
        winCard.appendChild(svgEl("text", { x: 30, y: 58, "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [`Adopted Amount: ${formatIndianRupee(effectiveVal)} · Rule Criteria Verified`]));

        const winPill = svgEl("g", { transform: "translate(740, 20)" });
        winPill.appendChild(svgEl("rect", { x: 0, y: 0, width: 110, height: 36, rx: 18, fill: "var(--ok)" }));
        winPill.appendChild(svgEl("text", { x: 55, y: 24, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "#ffffff" }, ["Accepted"]));
        winCard.appendChild(winPill);

        stage.appendChild(winCard);
      }

      return stage;
    },

    // =========================================================================
    // 8. time_range (Horizontal ruler axis with span window and dropping event pin)
    // =========================================================================
    time_range: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueAxis = cues.cue_axis || 0.5;
      const cueWindow = cues.cue_window || 4.0;
      const cueEvent = cues.cue_event || 7.5;
      const cueOutcome = cues.cue_outcome || 10.5;

      stage.appendChild(renderHeaderBanner(slots.title || "Prescribed Window & Event Timing", "accent"));

      const spanLen = parseAmount(slots.span_length, 24);
      const spanUnit = slots.span_unit || "Months";
      const eventOffset = slots.event_offset !== undefined ? parseAmount(slots.event_offset, 16) : 16;
      const isInside = slots.is_inside !== undefined ? Boolean(slots.is_inside) : (eventOffset <= spanLen);

      // Timeline axis baseline (x: 100 to 900, y: 240)
      const axisStartX = 100, axisEndX = 900, axisY = 240;
      const pAxis = clamp01((t - cueAxis) / 1.5);
      const curAxisX = axisStartX + (axisEndX - axisStartX) * Easing.easeOut(pAxis);

      const axisG = svgEl("g");
      axisG.appendChild(svgEl("line", { x1: axisStartX, y1: axisY, x2: curAxisX, y2: axisY, stroke: "var(--ink)", "stroke-width": 4, "stroke-linecap": "round" }));

      // Ticks & month milestones
      const totalUnits = 36;
      const pxPerUnit = (axisEndX - axisStartX - 60) / totalUnits;
      const startPinX = axisStartX + 40;

      for (let u = 0; u <= totalUnits; u += 6) {
        const tickX = startPinX + u * pxPerUnit;
        if (tickX <= curAxisX) {
          axisG.appendChild(svgEl("line", { x1: tickX, y1: axisY - 8, x2: tickX, y2: axisY + 8, stroke: "var(--ink-muted)", "stroke-width": 2 }));
          axisG.appendChild(svgEl("text", { x: tickX, y: axisY + 28, "text-anchor": "middle", "font-size": 14, "font-weight": "700", fill: "var(--ink-muted)" }, [`${u}M`]));
        }
      }
      stage.appendChild(axisG);

      // Cue 2: Span window expansion
      const endPinX = startPinX + spanLen * pxPerUnit;
      if (t >= cueWindow) {
        const pWin = clamp01((t - cueWindow) / 1.5);
        const easeWin = Easing.easeOut(pWin);
        const curWinW = (endPinX - startPinX) * easeWin;

        // Translucent highlight rect
        stage.appendChild(svgEl("rect", { x: startPinX, y: axisY - 50, width: curWinW, height: 50, fill: "var(--accent-soft)", opacity: 0.5, rx: 6 }));
        stage.appendChild(svgEl("line", { x1: startPinX, y1: axisY - 50, x2: startPinX + curWinW, y2: axisY - 50, stroke: "var(--accent)", "stroke-width": 3 }));

        // Start pin
        const startPin = svgEl("g", { transform: `translate(${startPinX}, ${axisY})` });
        startPin.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 8, fill: "var(--accent)" }));
        startPin.appendChild(svgEl("text", { x: 0, y: -65, "text-anchor": "middle", "font-size": 15, "font-weight": "800", fill: "var(--accent)" }, [slots.start_label || "Start Baseline"]));
        stage.appendChild(startPin);

        // End limit pin
        if (pWin >= 0.9) {
          const endPin = svgEl("g", { transform: `translate(${endPinX}, ${axisY})` });
          endPin.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 8, fill: "var(--gold)" }));
          endPin.appendChild(svgEl("line", { x1: 0, y1: -70, x2: 0, y2: 0, stroke: "var(--gold)", "stroke-width": 2, "stroke-dasharray": "4 3" }));
          endPin.appendChild(svgEl("text", { x: 0, y: -78, "text-anchor": "middle", "font-size": 15, "font-weight": "800", fill: "var(--gold)" }, [`${spanLen} ${spanUnit} Limit`]));
          stage.appendChild(endPin);
        }
      }

      // Cue 3: Event Flag drops from top
      const eventTargetX = startPinX + eventOffset * pxPerUnit;
      if (t >= cueEvent) {
        const pEvent = clamp01((t - cueEvent) / 1.0);
        const easeDrop = Easing.bounceOut(pEvent);
        const curEventY = (axisY - 140) + easeDrop * 140;
        const tone = isInside ? "ok" : "warn";

        const flagG = svgEl("g", { transform: `translate(${eventTargetX}, ${curEventY})` });
        flagG.appendChild(svgEl("line", { x1: 0, y1: 0, x2: 0, y2: -45, stroke: `var(--${tone})`, "stroke-width": 3 }));
        flagG.appendChild(svgEl("path", { d: "M 0 -45 L 35 -32 L 0 -18 Z", fill: `var(--${tone})` }));
        flagG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 7, fill: `var(--${tone})` }));

        flagG.appendChild(svgEl("rect", { x: -80, y: -78, width: 160, height: 28, rx: 6, fill: "var(--surface)", stroke: `var(--${tone})`, "stroke-width": 1.5 }));
        flagG.appendChild(svgEl("text", { x: 0, y: -59, "text-anchor": "middle", "font-size": 14, "font-weight": "800", fill: `var(--${tone})` }, [slots.event_label || "Action Event"]));

        stage.appendChild(flagG);
      }

      // Cue 4: Outcome banner at bottom
      if (t >= cueOutcome) {
        const pOut = clamp01((t - cueOutcome) / 0.8);
        const easeOut = Easing.backOut(pOut);
        const tone = isInside ? "ok" : "warn";
        const resCard = svgEl("g", { transform: `translate(60, ${410 + (1 - easeOut)*25}) scale(${easeOut})` });
        resCard.style.transformOrigin = "500px 450px";
        resCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 85, rx: 16, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": 2 }));

        const titleText = isInside ? "Timing Criteria Fulfilled · Event Within Permitted Window" : "Prescribed Limit Exceeded · Action Overdue";
        resCard.appendChild(svgEl("text", { x: 30, y: 36, "font-size": 19, "font-weight": "900", fill: `var(--${tone})` }, [titleText]));
        const detailText = isInside ? `Completed at Month ${eventOffset} (before ${spanLen} ${spanUnit} ceiling) · Full Relief Applies.` : `Occurred at Month ${eventOffset} (${eventOffset - spanLen} ${spanUnit} past deadline) · Relief Disallowed.`;
        resCard.appendChild(svgEl("text", { x: 30, y: 64, "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [detailText]));

        const badgePill = svgEl("g", { transform: "translate(740, 24)" });
        badgePill.appendChild(svgEl("rect", { x: 0, y: 0, width: 110, height: 36, rx: 18, fill: `var(--${tone})` }));
        badgePill.appendChild(svgEl("text", { x: 55, y: 24, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: "#ffffff" }, [isInside ? "In Time" : "Overdue"]));
        resCard.appendChild(badgePill);

        stage.appendChild(resCard);
      }

      return stage;
    },

    // =========================================================================
    // 9. conditions_gate (Condition cards + mechanical gate swing or padlock)
    // =========================================================================
    conditions_gate: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueCards = cues.cue_cards || 0.5;
      const cueEval = cues.cue_eval || 4.0;
      const cueGate = cues.cue_gate || 9.0;

      stage.appendChild(renderHeaderBanner(slots.title || "Prescribed Gatekeeper Checklist", "accent"));

      const rawConds = slots.conditions || slots.checklist || slots.criteria || [];
      const conditions = rawConds.length > 0 ? rawConds.map((cond, idx) => ({
        label: cond.label || cond.text || cond.title || cond.criterion || cond.name || `Criterion ${idx+1}`,
        passed: cond.passed !== undefined ? Boolean(cond.passed) : (cond.met !== undefined ? Boolean(cond.met) : (cond.is_met !== undefined ? Boolean(cond.is_met) : true))
      })) : [
        { label: "Initial Eligibility Condition", passed: true },
        { label: "Secondary Compliance Standard", passed: true },
        { label: "Eligibility Window Fulfillment", passed: true }
      ];
      const allPassed = conditions.every(c => c.passed);

      // Left Column: Condition Cards sliding in
      const cardW = 440, cardH = 68, cardGap = 12;
      const startLeftY = 120;

      conditions.forEach((cond, idx) => {
        const itemCue = cueCards + idx * 0.7;
        const pSlide = clamp01((t - itemCue) / 0.8);
        if (pSlide <= 0) return;

        const easeSlide = Easing.backOut(pSlide);
        const curX = 60 - (1 - easeSlide) * 200;
        const curY = startLeftY + idx * (cardH + cardGap);

        const cardG = svgEl("g", { transform: `translate(${curX}, ${curY})` });
        cardG.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW, height: cardH, rx: 12, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 2 }));
        cardG.appendChild(svgFittedText({ x: 24, y: 40, "font-weight": "800", fill: "var(--ink)" }, cond.label || `Criterion ${idx+1}`, 330, 16, true));

        // Stamp evaluation
        const evalCue = cueEval + idx * 0.9;
        if (t >= evalCue) {
          const pStamp = clamp01((t - evalCue) / 0.5);
          const easeStamp = Easing.bounceOut(pStamp);
          const tone = cond.passed ? "ok" : "warn";

          const stampG = svgEl("g", { transform: `translate(385, 34) scale(${easeStamp})` });
          stampG.style.transformOrigin = "385px 34px";
          stampG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 18, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": 2 }));
          const sym = cond.passed ? "✓" : "✗";
          stampG.appendChild(svgEl("text", { x: 0, y: 6, "text-anchor": "middle", "font-size": 20, "font-weight": "900", fill: `var(--${tone})` }, [sym]));
          cardG.appendChild(stampG);
        }

        stage.appendChild(cardG);
      });

      // Right Column: Mechanical Gate Portal
      const gateX = 540, gateY = 120, gateW = 370, gateH = 360;
      const gateChamber = svgEl("g", { transform: `translate(${gateX}, ${gateY})` });

      // Clip Path strictly containing doors within portal arch
      const defs = svgEl("defs");
      const clip = svgEl("clipPath", { id: "gate_portal_clip" });
      clip.appendChild(svgEl("rect", { x: 25, y: 25, width: gateW - 50, height: gateH - 50, rx: 10 }));
      defs.appendChild(clip);
      gateChamber.appendChild(defs);

      // Outer Portal Arch Frame
      gateChamber.appendChild(svgEl("rect", { x: 0, y: 0, width: gateW, height: gateH, rx: 20, fill: "var(--surface-card)", stroke: "var(--ink)", "stroke-width": 3 }));
      // Inner doorway background
      gateChamber.appendChild(svgEl("rect", { x: 25, y: 25, width: gateW - 50, height: gateH - 50, rx: 10, fill: allPassed ? "var(--ok-soft)" : "var(--warn-soft)" }));

      const doorContainer = svgEl("g");
      const doorW = (gateW - 50) / 2;

      // Cue 3: Gate action
      if (t >= cueGate) {
        const pGate = clamp01((t - cueGate) / 1.5);

        if (allPassed) {
          const easeOpen = Easing.easeInOut(pGate);
          // Hinge rotation: projected door width foreshortens from doorW to 25px
          const curDoorW = Math.max(25, doorW * (1 - easeOpen * 0.85));

          // Left door hinged at x=25
          doorContainer.appendChild(svgEl("rect", { x: 25, y: 25, width: curDoorW, height: gateH - 50, rx: 4, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 2.5 }));
          // Right door hinged at x=25 + doorW*2 = 25 + 320 = 345
          doorContainer.appendChild(svgEl("rect", { x: 25 + doorW * 2 - curDoorW, y: 25, width: curDoorW, height: gateH - 50, rx: 4, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 2.5 }));
          gateChamber.appendChild(doorContainer);

          gateChamber.appendChild(svgEl("text", { x: gateW/2, y: gateH/2 - 10, "text-anchor": "middle", "font-size": 24, "font-weight": "900", fill: "var(--ok)" }, ["GATE UNLOCKED"]));
          gateChamber.appendChild(svgEl("text", { x: gateW/2, y: gateH/2 + 25, "text-anchor": "middle", "font-size": 15, "font-weight": "800", fill: "var(--ink)" }, [slots.open_caption || "All Conditions Met · Access Granted"]));
        } else {
          const shake = Math.sin((t - cueGate) * 30) * Math.max(0, 1 - (t - cueGate) / 1.5) * 6;
          doorContainer.appendChild(svgEl("rect", { x: 25 + shake, y: 25, width: gateW - 50, height: gateH - 50, rx: 4, fill: "var(--surface)", stroke: "var(--warn)", "stroke-width": 3 }));
          gateChamber.appendChild(doorContainer);

          const easeLock = Easing.bounceOut(pGate);
          const lockY = 20 + easeLock * 90;
          const lockG = svgEl("g", { transform: `translate(${gateW/2 - 35}, ${lockY})` });
          lockG.appendChild(ICON_RENDERERS.lock(70, "warn"));
          gateChamber.appendChild(lockG);

          gateChamber.appendChild(svgEl("text", { x: gateW/2, y: gateH - 60, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--warn)" }, ["GATE LOCKED"]));
          gateChamber.appendChild(svgEl("text", { x: gateW/2, y: gateH - 35, "text-anchor": "middle", "font-size": 15, "font-weight": "800", fill: "var(--ink-muted)" }, [slots.closed_caption || "Condition Failed · Access Locked"]));
        }
      } else {
        doorContainer.appendChild(svgEl("rect", { x: 25, y: 25, width: doorW, height: gateH - 50, rx: 4, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 2 }));
        doorContainer.appendChild(svgEl("rect", { x: 25 + doorW, y: 25, width: doorW, height: gateH - 50, rx: 4, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 2 }));
        gateChamber.appendChild(doorContainer);
        gateChamber.appendChild(svgEl("text", { x: gateW/2, y: gateH/2, "text-anchor": "middle", "font-size": 18, "font-weight": "800", fill: "var(--ink-muted)" }, ["Evaluating Checklist..."]));
      }

      stage.appendChild(gateChamber);
      return stage;
    },

    // =========================================================================
    // 10. chain_passing (Conveyor nodes, multi-hop parabolic arcs, carried cost tag)
    // =========================================================================
    chain_passing: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueOwners = cues.cue_owners || 0.5;
      const cueHop1 = cues.cue_hop_1 || 4.0;
      const cueHop2 = cues.cue_hop_2 || 8.0;
      const cueCarried = cues.cue_carried || 11.0;

      stage.appendChild(renderHeaderBanner(slots.title || "Succession Cost Base Carryover", "accent"));

      const rawOwners = slots.owners || [];
      const owners = rawOwners.length > 0 ? rawOwners.map((ow, idx) => ({
        name: ow.name || `Owner ${idx+1}`,
        year: String(ow.year || "")
      })) : [
        { name: "Predecessor One", year: "Year One" },
        { name: "Intermediary Owner", year: "Year Five" },
        { name: "Current Beneficiary", year: "Year Ten" }
      ];
      const numOwners = Math.max(3, Math.min(5, owners.length));
      const totalW = 660;
      const nodeSpacing = totalW / (numOwners - 1);
      const startX = 140, trackY = 270;

      // Connecting conveyor line
      stage.appendChild(svgEl("line", { x1: startX, y1: trackY, x2: startX + totalW, y2: trackY, stroke: "var(--line)", "stroke-width": 4, "stroke-linecap": "round" }));

      // Owner Pedestals
      const nodeCoords = [];
      owners.slice(0, numOwners).forEach((ow, idx) => {
        const nx = startX + idx * nodeSpacing;
        nodeCoords.push(nx);

        const pNode = clamp01((t - cueOwners) / 0.8);
        const easeNode = Easing.backOut(pNode);

        const nodeG = svgEl("g", { transform: `translate(${nx}, ${trackY}) scale(${easeNode})` });
        nodeG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: 34, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
        nodeG.appendChild(svgEl("circle", { cx: 0, cy: -8, r: 11, fill: "var(--accent)" }));
        nodeG.appendChild(svgEl("path", { d: "M -14 16 Q 0 4 14 16 Z", fill: "var(--accent)" }));

        nodeG.appendChild(svgFittedText({ x: 0, y: 52, "text-anchor": "middle", "font-weight": "800", fill: "var(--ink)" }, ow.name || `Owner ${idx+1}`, 115, 14, true));
        nodeG.appendChild(svgEl("text", { x: 0, y: 72, "text-anchor": "middle", "font-size": 13, "font-weight": "700", fill: "var(--ink-muted)" }, [ow.year || ""]));
        stage.appendChild(nodeG);
      });

      // Item token positions across time
      let curItemX = nodeCoords[0];
      let curItemY = trackY - 45;

      if (t < cueHop1) {
        // Resting at Owner 1
        const itemNode = renderTravelingItem(nodeCoords[0], curItemY, nodeCoords[0], curItemY, 0, 0, slots.item_label || "Capital Asset", parseAmount(slots.tag_value ?? slots.item_value ?? slots.val, 1800000), "house", "accent");
        stage.appendChild(itemNode);
      } else if (t >= cueHop1 && t < cueHop2) {
        const pHop = clamp01((t - cueHop1) / 1.8);
        const easeHop = Easing.easeInOut(pHop);
        const itemNode = renderTravelingItem(
          nodeCoords[0], curItemY, nodeCoords[1], curItemY,
          easeHop, 80,
          slots.item_label || "Capital Asset",
          parseAmount(slots.tag_value ?? slots.item_value ?? slots.val, 1800000),
          "house",
          "accent"
        );
        stage.appendChild(itemNode);
      } else {
        const pHop2 = clamp01((t - cueHop2) / 1.8);
        const easeHop2 = Easing.easeInOut(pHop2);
        const itemNode = renderTravelingItem(
          nodeCoords[1], curItemY, nodeCoords[2], curItemY,
          easeHop2, 80,
          slots.item_label || "Capital Asset",
          parseAmount(slots.tag_value ?? slots.item_value ?? slots.val, 1800000),
          "house",
          "accent"
        );
        stage.appendChild(itemNode);
      }

      // Cue Carried: Direct umbilical dashed tag from Owner 1 to Final Owner
      if (t >= cueCarried) {
        const pCar = clamp01((t - cueCarried) / 1.2);
        const easeCar = Easing.easeInOut(pCar);

        const endNodeX = nodeCoords[nodeCoords.length - 1];
        const tagX = nodeCoords[0] + (endNodeX - nodeCoords[0]) * easeCar;
        const tagY = trackY + 80;

        stage.appendChild(renderTrajectoryGuide(nodeCoords[0], trackY + 80, endNodeX, trackY + 80, -35, "gold"));

        const tagW = 190;
        const carriedTag = svgEl("g", { transform: `translate(${tagX - tagW/2}, ${tagY})` });
        carriedTag.appendChild(svgEl("rect", { x: 0, y: 0, width: tagW, height: 44, rx: 22, fill: "var(--gold)", stroke: "var(--ink)", "stroke-width": 2 }));
        carriedTag.appendChild(svgEl("text", { x: tagW/2, y: 20, "text-anchor": "middle", "font-size": 13, "font-weight": "800", fill: "#ffffff" }, [slots.tag_label || "Original Base Cost"]));
        carriedTag.appendChild(svgEl("text", { x: tagW/2, y: 37, "text-anchor": "middle", "font-size": 15, "font-weight": "900", fill: "#ffffff" }, [formatIndianRupee(parseAmount(slots.tag_value ?? slots.item_value ?? slots.val, 1800000))]));
        stage.appendChild(carriedTag);

        const noteCard = svgEl("g", { transform: "translate(60, 440)", opacity: pCar });
        noteCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 850, height: 60, rx: 12, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 2 }));
        noteCard.appendChild(svgEl("text", { x: 25, y: 36, "font-size": 16, "font-weight": "900", fill: "var(--ok)" }, ["Historical Cost Basis Maintained: Current beneficiary adopts original predecessor acquisition value."]));
        stage.appendChild(noteCard);
      }

      return stage;
    },

    // =========================================================================
    // 11. key_statement (G1: Word-by-word reveal + marker highlight sweep)
    // =========================================================================
    key_statement: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      const cueReveal = cues.cue_statement || 0.5;
      const cueHighlight = cues.cue_highlight || 4.5;
      const cueSupport = cues.cue_support || 8.5;

      const pEnter = clamp01(t / 0.8);
      const easeEnter = Easing.backOut(pEnter);
      const cardX = 80, cardY = 80 + (1 - easeEnter) * 30, cardW = 840, cardH = 380;
      const card = svgEl("g", { transform: `translate(${cardX}, ${cardY})` });
      card.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW, height: cardH, rx: 20, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));

      const iconSize = 70;
      const iconFn = ICON_RENDERERS[slots.icon_type] || ICON_RENDERERS.scale;
      const iconP = clamp01((t - cueReveal) / 1.0);
      const iconScale = Easing.backOut(iconP);
      const iconG = svgEl("g", { transform: `translate(${cardW/2 - iconSize/2}, 35) scale(${iconScale})` });
      iconG.style.transformOrigin = `${iconSize/2}px ${iconSize/2}px`;
      iconG.appendChild(iconFn(iconSize, "accent"));
      card.appendChild(iconG);

      const statement = slots.statement || "Legal standards require standard benchmark value adoption when agreed price falls below prescribed limits.";
      const rawWords = statement.split(/\s+/);
      const lines = [];
      let curLine = "";
      for (const w of rawWords) {
        const testLine = curLine ? (curLine + " " + w) : w;
        if (testLine.length * 15 > 720 && curLine) {
          lines.push(curLine);
          curLine = w;
        } else {
          curLine = testLine;
        }
      }
      if (curLine) lines.push(curLine);
      const fs = lines.length > 2 ? 21 : 25;
      const lineH = lines.length > 2 ? 34 : 40;
      const startY = 150 - (lines.length - 2) * 10;
      lines.slice(0, 3).forEach((line, i) => {
        card.appendChild(svgFittedText({ x: cardW/2, y: startY + i * lineH, "text-anchor": "middle", "font-weight": "900", fill: "var(--ink)" }, line, 760, fs, true));
      });

      if (t >= cueHighlight) {
        const pSweep = clamp01((t - cueHighlight) / 1.5);
        const easeSweep = Easing.easeOut(pSweep);
        const sweepW = 480 * easeSweep;
        const marker = svgEl("rect", {
          x: cardW/2 - 240,
          y: startY + (lines.length > 1 ? lineH - 18 : 6),
          width: sweepW,
          height: 18,
          rx: 4,
          fill: "var(--gold-soft)",
          opacity: 0.65
        });
        card.insertBefore(marker, card.firstChild.nextSibling);
      }

      if (t >= cueSupport) {
        const pSup = clamp01((t - cueSupport) / 0.8);
        const easeSup = Easing.backOut(pSup);
        const supG = svgEl("g", { transform: `translate(40, ${270 + (1 - easeSup) * 35})`, opacity: pSup });
        supG.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW - 80, height: 65, rx: 12, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1.5 }));
        supG.appendChild(svgFittedText({ x: 25, y: 38, "font-weight": "800", fill: "var(--accent)" }, slots.support_line || "Core principle applies across asset exchanges and value reviews.", cardW - 130, 17, true));
        card.appendChild(supG);
      }

      stage.appendChild(card);
      return stage;
    },

    // =========================================================================
    // 12. step_sequence (G2: Moving pulse orb along roadmap milestones)
    // =========================================================================
    step_sequence: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      stage.appendChild(renderHeaderBanner(slots.title || "Linear Procedural Progression", "accent"));

      const steps = slots.steps || [
        { num: "1", title: "Initial Evaluation Step", desc: "Establish baseline data and eligibility" },
        { num: "2", title: "Analytical Evaluation", desc: "Apply relevant benchmarks and adjustments" },
        { num: "3", title: "Final Settlement Determination", desc: "Verify compliance and conclude result" }
      ];
      const numSteps = Math.max(2, Math.min(5, steps.length));
      const totalW = 800;
      const stepGap = totalW / (numSteps - 1);
      const startX = 100, pathY = 160;

      // Roadmap track line
      stage.appendChild(svgEl("line", { x1: startX, y1: pathY, x2: startX + totalW, y2: pathY, stroke: "var(--line)", "stroke-width": 5, "stroke-linecap": "round" }));

      // Milestones
      const stepXCoords = [];
      steps.slice(0, numSteps).forEach((st, idx) => {
        const sx = startX + idx * stepGap;
        stepXCoords.push(sx);

        stage.appendChild(svgEl("circle", { cx: sx, cy: pathY, r: 24, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
        stage.appendChild(svgEl("text", { x: sx, y: pathY + 7, "text-anchor": "middle", "font-size": 17, "font-weight": "900", fill: "var(--accent)" }, [st.num || `${idx+1}`]));
      });

      // Traveling pulse orb
      const cue1 = cues.cue_step_1 || 0.5;
      const cue2 = cues.cue_step_2 || 4.5;
      const cue3 = cues.cue_step_3 || 8.5;

      let orbX = stepXCoords[0];
      let activeIdx = 0;

      if (t < cue2) {
        orbX = stepXCoords[0];
        activeIdx = 0;
      } else if (t >= cue2 && t < cue3) {
        const pMove = clamp01((t - cue2) / 1.5);
        orbX = stepXCoords[0] + (stepXCoords[1] - stepXCoords[0]) * Easing.easeInOut(pMove);
        activeIdx = 1;
      } else {
        const pMove2 = clamp01((t - cue3) / 1.5);
        orbX = stepXCoords[1] + (stepXCoords[2] - stepXCoords[1]) * Easing.easeInOut(pMove2);
        activeIdx = 2;
      }

      // Draw active traveling orb
      stage.appendChild(svgEl("circle", { cx: orbX, cy: pathY, r: 16, fill: "var(--gold)", stroke: "#ffffff", "stroke-width": 3 }));
      stage.appendChild(svgEl("circle", { cx: orbX, cy: pathY, r: 24, fill: "none", stroke: "var(--gold)", "stroke-width": 2, opacity: 0.6 }));

      // Step cards below
      const totalCardSpan = 800;
      const cardGap = 16;
      const cardW = Math.floor((totalCardSpan - (numSteps - 1) * cardGap) / numSteps);
      const cardY = 230;

      steps.slice(0, numSteps).forEach((st, idx) => {
        const cx = 80 + idx * (cardW + cardGap);
        const isActive = idx === activeIdx;
        const tone = isActive ? "accent" : "surface";

        const card = svgEl("g", { transform: `translate(${cx}, ${cardY})` });
        card.appendChild(svgEl("rect", { x: 0, y: 0, width: cardW, height: 180, rx: 14, fill: isActive ? "var(--surface)" : "var(--surface-card)", stroke: `var(--${isActive ? "accent" : "line"})`, "stroke-width": isActive ? 3 : 1.5 }));
        card.appendChild(svgEl("rect", { x: 14, y: 14, width: 32, height: 32, rx: 8, fill: `var(--${isActive ? "accent" : "line"})` }));
        card.appendChild(svgEl("text", { x: 30, y: 36, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: "#ffffff" }, [st.num || `${idx+1}`]));
        const descWords = (st.desc || "").split(/\s+/);
        const descMid = Math.ceil(descWords.length / 2);
        const dLine1 = descWords.slice(0, descMid).join(" ");
        const dLine2 = descWords.slice(descMid).join(" ");
        card.appendChild(svgFittedText({ x: 14, y: 68, "font-weight": "600", fill: "var(--ink-muted)" }, dLine1, cardW - 28, 12, false));
        if (dLine2) {
          card.appendChild(svgFittedText({ x: 14, y: 88, "font-weight": "600", fill: "var(--ink-muted)" }, dLine2, cardW - 28, 12, false));
        }

        if (isActive) {
          card.appendChild(svgEl("rect", { x: 14, y: 135, width: cardW - 28, height: 28, rx: 14, fill: "var(--accent-soft)" }));
          card.appendChild(svgEl("text", { x: cardW/2, y: 154, "text-anchor": "middle", "font-size": 13, "font-weight": "900", fill: "var(--accent)" }, ["ACTIVE STAGE"]));
        }

        stage.appendChild(card);
      });

      // Bottom progress bar
      const progCard = svgEl("g", { transform: "translate(80, 445)" });
      progCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 800, height: 45, rx: 12, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      const pFull = clamp01(t / duration);
      progCard.appendChild(svgEl("rect", { x: 12, y: 15, width: (800 - 24) * pFull, height: 20, rx: 10, fill: "var(--ok)" }));
      progCard.appendChild(svgEl("text", { x: 400, y: 31, "text-anchor": "middle", "font-size": 14, "font-weight": "900", fill: "var(--ink)" }, [`Workflow Progression: ${Math.round(pFull*100)}% Complete`]));
      stage.appendChild(progCard);

      return stage;
    },

    // =========================================================================
    // 13. formula_builder (G3: Mathematical equation chips assembling + arithmetic)
    // =========================================================================
    formula_builder: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      stage.appendChild(renderHeaderBanner(slots.title || "Arithmetic Formula Construction", "accent"));

      const rawChips = slots.chips || slots.items || [];
      const chips = rawChips.length > 0 ? rawChips.map(c => {
        if (c.op) return { op: c.op };
        return {
          label: c.label || c.title || c.name || "",
          val: parseAmount(c.val ?? c.amount ?? 0),
          is_total: Boolean(c.is_total)
        };
      }) : [
        { label: "Primary Base Component", val: 5000000 },
        { op: "−" },
        { label: "Prescribed Outflow Base", val: 1800000 },
        { op: "−" },
        { label: "Permissible Outflow", val: 200000 },
        { op: "=" },
        { label: "Net Final Balance", val: 3000000, is_total: true }
      ];

      const cueOp1 = cues.cue_operand_1 || 0.5;
      const cueOp2 = cues.cue_operand_2 || 4.0;
      const cueOp3 = cues.cue_operand_3 || 7.5;
      const cueRes = cues.cue_result || 10.5;

      const chipY = 170;
      let curX = 55;

      chips.forEach((ch, idx) => {
        let chCue = cueOp1;
        if (idx >= 2 && idx < 4) chCue = cueOp2;
        else if (idx >= 4 && idx < 6) chCue = cueOp3;
        else if (idx >= 6) chCue = cueRes;

        const pCh = clamp01((t - chCue) / 0.8);
        if (pCh <= 0) return;

        const easeCh = Easing.backOut(pCh);

        if (ch.op) {
          const opW = 36;
          const opG = svgEl("g", { transform: `translate(${curX + (1 - easeCh)*15}, ${chipY + 28}) scale(${easeCh})` });
          opG.appendChild(svgEl("circle", { cx: opW/2, cy: 18, r: 18, fill: "var(--surface)", stroke: "var(--ink)", "stroke-width": 2 }));
          opG.appendChild(svgEl("text", { x: opW/2, y: 25, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--ink)" }, [ch.op]));
          stage.appendChild(opG);
          curX += opW + 8;
        } else {
          const isTot = ch.is_total;
          const chipW = isTot ? 180 : 138;
          const tone = isTot ? "ok" : "accent";

          const card = svgEl("g", { transform: `translate(${curX}, ${chipY - (1 - easeCh)*30}) scale(${easeCh})` });
          card.appendChild(svgEl("rect", { x: 0, y: 0, width: chipW, height: 90, rx: 12, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": isTot ? 3 : 2 }));
          card.appendChild(svgFittedText({ x: chipW/2, y: 30, "text-anchor": "middle", "font-weight": "800", fill: "var(--ink)" }, ch.label || "", chipW - 14, 12, true));

          const curVal = Math.round((ch.val || 0) * pCh);
          card.appendChild(svgEl("text", { x: chipW/2, y: 64, "text-anchor": "middle", "font-size": isTot ? 20 : 16, "font-weight": "900", fill: `var(--${tone})` }, [formatIndianRupee(curVal)]));

          stage.appendChild(card);
          curX += chipW + 8;
        }
      });

      // Bottom full equation summary card
      if (t >= cueRes) {
        const pEq = clamp01((t - cueRes) / 0.8);
        const easeEq = Easing.backOut(pEq);
        const eqCard = svgEl("g", { transform: `translate(60, ${350 + (1 - easeEq)*30}) scale(${easeEq})` });
        eqCard.style.transformOrigin = "500px 410px";
        eqCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 110, rx: 16, fill: "var(--surface)", stroke: "var(--ok)", "stroke-width": 2.5 }));
        eqCard.appendChild(svgEl("text", { x: 40, y: 45, "font-size": 20, "font-weight": "900", fill: "var(--ok)" }, ["Formula Arithmetic Verification"]));
        const eqStr = chips.map(c => c.op ? ` ${c.op} ` : (formatIndianRupee(c.val || 0) + (c.is_total ? " Net Total" : ""))).join("");
        eqCard.appendChild(svgFittedText({ x: 40, y: 82, "font-weight": "800", fill: "var(--ink)" }, eqStr, 800, 22, true));
        stage.appendChild(eqCard);
      }

      return stage;
    },

    // =========================================================================
    // 14. table_reveal (G4: Matrix grid with sequential rows and row spotlight)
    // =========================================================================
    table_reveal: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      stage.appendChild(renderHeaderBanner(slots.title || "Comparative Structured Matrix", "accent"));

      const headers = slots.headers || ["Entity Classification", "Baseline Criterion", "Evaluation Metric", "Result Status"];
      const rows = slots.rows || [
        ["Category Alpha", "Criteria Standard One", "₹ 25,00,000", "Approved"],
        ["Category Beta", "Criteria Standard Two", "₹ 38,00,000", "Selected"],
        ["Category Gamma", "Criteria Standard Three", "₹ 12,00,000", "Exempt"]
      ];
      const spotlightIdx = slots.spotlight_row !== undefined ? slots.spotlight_row : 1;

      const cueHdr = cues.cue_header || 0.5;
      const cueRows = cues.cue_rows || 3.5;
      const cueSpot = cues.cue_spotlight || 8.0;

      const tblX = 60, tblY = 110, tblW = 880;
      const colW = tblW / headers.length;
      const rowH = 55;

      // Header row
      const pHdr = clamp01((t - cueHdr) / 0.8);
      const easeHdr = Easing.easeOut(pHdr);
      const hdrG = svgEl("g", { transform: `translate(${tblX}, ${tblY - (1 - easeHdr)*30})`, opacity: pHdr });
      hdrG.appendChild(svgEl("rect", { x: 0, y: 0, width: tblW, height: 48, rx: 10, fill: "var(--ink)" }));
      headers.forEach((h, i) => {
        hdrG.appendChild(svgFittedText({ x: i * colW + 20, y: 31, "font-weight": "800", fill: "#ffffff" }, h, colW - 30, 15, true));
      });
      stage.appendChild(hdrG);

      // Data rows
      rows.forEach((row, rIdx) => {
        const rCue = cueRows + rIdx * 1.0;
        const pR = clamp01((t - rCue) / 0.7);
        if (pR <= 0) return;

        const easeR = Easing.backOut(pR);
        const rY = tblY + 56 + rIdx * (rowH + 6);
        const isSpotlight = (t >= cueSpot && rIdx === spotlightIdx);
        const isDimmed = (t >= cueSpot && rIdx !== spotlightIdx);

        const rowG = svgEl("g", { transform: `translate(${tblX - (1 - easeR)*40}, ${rY})`, opacity: isDimmed ? 0.35 : pR });
        rowG.appendChild(svgEl("rect", { x: 0, y: 0, width: tblW, height: rowH, rx: 10, fill: "var(--surface)", stroke: isSpotlight ? "var(--ok)" : "var(--line)", "stroke-width": isSpotlight ? 3.5 : 1.5 }));

        row.forEach((cell, cIdx) => {
          const cellMaxW = (isSpotlight && cIdx === row.length - 1) ? (colW - 140) : (colW - 30);
          rowG.appendChild(svgFittedText({ x: cIdx * colW + 20, y: 34, "font-weight": isSpotlight ? "900" : "700", fill: isSpotlight ? "var(--ok)" : "var(--ink)" }, cell, cellMaxW, 15, isSpotlight));
        });

        if (isSpotlight) {
          // Spotlight badge
          rowG.appendChild(svgEl("rect", { x: tblW - 130, y: 12, width: 115, height: 32, rx: 16, fill: "var(--ok)" }));
          rowG.appendChild(svgEl("text", { x: tblW - 72, y: 33, "text-anchor": "middle", "font-size": 14, "font-weight": "900", fill: "#ffffff" }, ["TARGET ROW"]));
        }

        stage.appendChild(rowG);
      });

      // Bottom footnote
      const footCard = svgEl("g", { transform: "translate(60, 460)" });
      footCard.appendChild(svgEl("rect", { x: 0, y: 0, width: 880, height: 50, rx: 12, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      footCard.appendChild(svgEl("text", { x: 24, y: 31, "font-size": 15, "font-weight": "700", fill: "var(--ink)" }, ["Matrix Spotlight: Highlights relevant categorization threshold based on criteria matching."]));
      stage.appendChild(footCard);

      return stage;
    },

    // =========================================================================
    // 15. concept_map (G5: Central hub branching to child cards with highlight)
    // =========================================================================
    concept_map: (slots, t, duration, cues) => {
      const stage = svgEl("g");
      stage.appendChild(renderHeaderBanner(slots.title || "Hub & Branch Concept Architecture", "accent"));

      const branches = slots.branches || [
        { label: "Primary Branch Node", desc: "Standard Operation Protocol", highlight: false },
        { label: "Key Selected Branch", desc: "Core Emphasis Criterion", highlight: true },
        { label: "Conditional Branch", desc: "Alternative Secondary Route", highlight: false }
      ];

      const cueHub = cues.cue_hub || 0.5;
      const cueBranches = cues.cue_branches || 4.0;
      const cueEmphasize = cues.cue_emphasize || 8.5;

      const hubX = 170, hubY = 270, hubR = 55;

      // Central Hub
      const pHub = clamp01((t - cueHub) / 1.0);
      const easeHub = Easing.backOut(pHub);

      const hubG = svgEl("g", { transform: `translate(${hubX}, ${hubY}) scale(${easeHub})` });
      hubG.style.transformOrigin = `${hubX}px ${hubY}px`;
      hubG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: hubR, fill: "var(--accent)", stroke: "var(--ink)", "stroke-width": 3 }));
      hubG.appendChild(svgEl("circle", { cx: 0, cy: 0, r: hubR + 10, fill: "none", stroke: "var(--accent-soft)", "stroke-width": 3 }));
      const hubWords = (slots.hub_label || "Central Hub").split(" ");
      if (hubWords.length > 1) {
        const mid = Math.ceil(hubWords.length / 2);
        const l1 = hubWords.slice(0, mid).join(" ");
        const l2 = hubWords.slice(mid).join(" ");
        hubG.appendChild(svgFittedText({ x: 0, y: -4, "text-anchor": "middle", "font-weight": "900", fill: "#ffffff" }, l1, 95, 14, true));
        hubG.appendChild(svgFittedText({ x: 0, y: 16, "text-anchor": "middle", "font-weight": "900", fill: "#ffffff" }, l2, 95, 14, true));
      } else {
        hubG.appendChild(svgFittedText({ x: 0, y: 6, "text-anchor": "middle", "font-weight": "900", fill: "#ffffff" }, slots.hub_label || "Central Hub", 95, 15, true));
      }
      stage.appendChild(hubG);

      // Target Branch destinations on right
      const branchTargetX = 490, branchW = 390, branchH = 80;
      const branchStartY = 130, branchGap = 20;
      const startBX = hubX + hubR;

      branches.forEach((br, idx) => {
        const bCue = cueBranches + idx * 0.9;
        const pBr = clamp01((t - bCue) / 1.5);
        const easeBr = Easing.easeOut(pBr);
        const targetBY = branchStartY + idx * (branchH + branchGap);

        // Physical travel: card slides from hub out to targetX
        const curBX = startBX + (branchTargetX - startBX) * easeBr;
        const curBY = hubY + (targetBY - hubY) * easeBr;

        // Dynamic Bezier connector path growing along with card
        const curveMidX = (startBX + curBX) / 2;
        const pathD = `M ${startBX} ${hubY} C ${curveMidX} ${hubY}, ${curveMidX} ${curBY + branchH/2}, ${curBX} ${curBY + branchH/2}`;

        stage.appendChild(svgEl("path", {
          d: pathD,
          fill: "none",
          stroke: br.highlight ? "var(--ok)" : "var(--line)",
          "stroke-width": br.highlight ? 4 : 2.5,
          "stroke-linecap": "round",
          opacity: Math.max(0.01, pBr)
        }));

        const isEmp = (t >= cueEmphasize && br.highlight);
        const isDim = (t >= cueEmphasize && !br.highlight);
        const tone = isEmp ? "ok" : "accent";

        const card = svgEl("g", { transform: `translate(${curBX}, ${curBY}) scale(${isEmp ? 1.05 : 1.0})`, opacity: isDim ? 0.35 : Math.max(0.01, pBr) });
        card.style.transformOrigin = `${curBX}px ${curBY + branchH/2}px`;
        card.appendChild(svgEl("rect", { x: 0, y: 0, width: branchW, height: branchH, rx: 14, fill: "var(--surface)", stroke: `var(--${tone})`, "stroke-width": isEmp ? 3.5 : 2 }));

        const maxLabelW = isEmp ? (branchW - 135) : (branchW - 40);
        card.appendChild(svgFittedText({ x: 20, y: 34, "font-weight": "900", fill: "var(--ink)" }, br.label || `Branch ${idx+1}`, maxLabelW, 17, true));
        card.appendChild(svgFittedText({ x: 20, y: 58, "font-weight": "600", fill: "var(--ink-muted)" }, br.desc || "", maxLabelW, 14, false));

        if (isEmp) {
          card.appendChild(svgEl("rect", { x: branchW - 110, y: 22, width: 95, height: 34, rx: 17, fill: "var(--ok)" }));
          card.appendChild(svgEl("text", { x: branchW - 62, y: 44, "text-anchor": "middle", "font-size": 14, "font-weight": "900", fill: "#ffffff" }, ["SELECTED"]));
        }

        stage.appendChild(card);
      });

      return stage;
    }
  };

  // -------------------------------------------------------------------------
  // KineticAnimationInstance Class (Pure Function of Time t)
  // -------------------------------------------------------------------------
  function normalizeSlots(archId, rawSlots) {
    if (!rawSlots) return {};
    const slots = Object.assign({}, rawSlots);

    if (archId === "take_away") {
      if (slots.start_amount === undefined) {
        if (slots.whole_val !== undefined) slots.start_amount = parseAmount(slots.whole_val);
        else if (slots.whole_amount !== undefined) slots.start_amount = parseAmount(slots.whole_amount);
        else if (slots.start_val !== undefined) slots.start_amount = parseAmount(slots.start_val);
      } else {
        slots.start_amount = parseAmount(slots.start_amount);
      }
      if (slots.start_label === undefined && slots.whole_label !== undefined) {
        slots.start_label = slots.whole_label;
      }
      const rawSteps = slots.steps || slots.chunks || slots.deductions || slots.slices;
      if (rawSteps && Array.isArray(rawSteps)) {
        slots.steps = rawSteps.map((s, idx) => ({
          label: s.label || s.title || s.text || `Outflow Step ${idx+1}`,
          amount: parseAmount(s.amount !== undefined ? s.amount : s.val)
        }));
      }
    } else if (archId === "conditions_gate") {
      const rawConds = slots.conditions || slots.checklist || slots.criteria;
      if (rawConds && Array.isArray(rawConds)) {
        slots.conditions = rawConds.map((c, idx) => ({
          label: c.label || c.text || c.title || c.criterion || c.name || `Criterion ${idx+1}`,
          passed: c.passed !== undefined ? Boolean(c.passed) : (c.met !== undefined ? Boolean(c.met) : (c.is_met !== undefined ? Boolean(c.is_met) : true))
        }));
      }
    } else if (archId === "split_into_parts") {
      if (slots.whole_amount === undefined && slots.whole_val !== undefined) {
        slots.whole_amount = parseAmount(slots.whole_val);
      } else if (slots.whole_amount !== undefined) {
        slots.whole_amount = parseAmount(slots.whole_amount);
      }
      const rawParts = slots.parts || slots.chunks || slots.branches;
      if (rawParts && Array.isArray(rawParts)) {
        slots.parts = rawParts.map(p => ({
          label: p.label || p.title || p.text || "Allocation Branch",
          amount: parseAmount(p.amount !== undefined ? p.amount : p.val)
        }));
      }
    } else if (archId === "merge_into_one") {
      const rawInputs = slots.inputs || slots.streams || slots.items;
      if (rawInputs && Array.isArray(rawInputs)) {
        slots.inputs = rawInputs.map(i => ({
          label: i.label || i.title || i.text || "Input Stream",
          amount: parseAmount(i.amount !== undefined ? i.amount : i.val)
        }));
      }
      if (slots.result_label === undefined && slots.merged_label !== undefined) {
        slots.result_label = slots.merged_label;
      }
    } else if (archId === "add_up") {
      const rawItems = slots.items || slots.rows || slots.steps;
      if (rawItems && Array.isArray(rawItems)) {
        slots.items = rawItems.map(it => ({
          label: it.label || it.title || it.text || "Component",
          amount: parseAmount(it.amount !== undefined ? it.amount : it.val)
        }));
      }
    } else if (archId === "compare_two") {
      if (slots.val_a !== undefined) slots.val_a = parseAmount(slots.val_a);
      else if (slots.val_1 !== undefined) slots.val_a = parseAmount(slots.val_1);
      if (slots.val_b !== undefined) slots.val_b = parseAmount(slots.val_b);
      else if (slots.val_2 !== undefined) slots.val_b = parseAmount(slots.val_2);
      if (slots.cap_amount !== undefined && slots.cap_amount) slots.cap_amount = parseAmount(slots.cap_amount);
    } else if (archId === "swap") {
      if (slots.item_a && typeof slots.item_a === "object") {
        if (slots.item_a_val === undefined) slots.item_a_val = parseAmount(slots.item_a.val || slots.item_a.amount);
        if (slots.item_a_label === undefined) slots.item_a_label = slots.item_a.label;
        if (slots.item_a_icon === undefined) slots.item_a_icon = slots.item_a.icon;
      }
      if (slots.item_b && typeof slots.item_b === "object") {
        if (slots.item_b_val === undefined) slots.item_b_val = parseAmount(slots.item_b.val || slots.item_b.amount);
        if (slots.item_b_label === undefined) slots.item_b_label = slots.item_b.label;
        if (slots.item_b_icon === undefined) slots.item_b_icon = slots.item_b.icon;
      }
    } else if (archId === "give_and_receive") {
      if (slots.item_value !== undefined) slots.item_value = parseAmount(slots.item_value);
      if (slots.payment_amount !== undefined) slots.payment_amount = parseAmount(slots.payment_amount);
    } else if (archId === "chain_passing") {
      if (slots.tag_value !== undefined) slots.tag_value = parseAmount(slots.tag_value);
      else if (slots.item_value !== undefined) slots.tag_value = parseAmount(slots.item_value);
    } else if (archId === "formula_builder") {
      const rawChips = slots.chips || slots.items;
      if (rawChips && Array.isArray(rawChips)) {
        const expandedChips = [];
        rawChips.forEach((c, idx) => {
          const hasVal = (c.val !== undefined || c.amount !== undefined);
          const hasLabel = Boolean(c.label || c.title);
          const op = c.op ? (c.op === "-" ? "−" : c.op) : null;
          
          if (op && !hasVal && !hasLabel) {
            expandedChips.push({ op: op });
          } else if (op && (hasVal || hasLabel)) {
            if (op !== "+" || idx > 0) {
              expandedChips.push({ op: op });
            }
            expandedChips.push({
              label: c.label || c.title || c.name || "",
              val: parseAmount(c.val !== undefined ? c.val : c.amount),
              is_total: Boolean(c.is_total)
            });
          } else {
            expandedChips.push({
              label: c.label || c.title || c.name || "",
              val: parseAmount(c.val !== undefined ? c.val : c.amount),
              is_total: Boolean(c.is_total)
            });
          }
        });
        slots.chips = expandedChips;
      }
    }
    return slots;
  }
  class KineticAnimationInstance {
    constructor(container, def, rawSlots = {}, options = {}) {
      this.container = container;
      this.def = def;
      const normalizedSlots = normalizeSlots(def.id, rawSlots);
      this.slots = Object.assign({}, def.slots_default || {}, normalizedSlots);
      this.cues = Object.assign({}, def.cues_default || {}, options.cues || {});
      this.duration = def.duration || 14.0;
      this.theme = options.theme || "light";
      this.currentTime = 0.0;

      this.initDom();
      this.seek(0.0);
    }

    initDom() {
      this.container.innerHTML = "";
      this.svg = svgEl("svg", {
        viewBox: "0 0 1000 562",
        class: `kinetic-stage theme-${this.theme}`,
        width: "100%",
        height: "100%",
        style: "display: block; width: 100%; height: auto; max-height: 100%;"
      });

      // Defs & CSS Variables for Light / Dark mode
      const defs = svgEl("defs");
      const style = svgEl("style", {}, [`
        .theme-light {
          --surface: #ffffff;
          --surface-card: #f8fafc;
          --ink: #0f172a;
          --ink-muted: #64748b;
          --accent: #2563eb;
          --accent-soft: #dbeafe;
          --ok: #16a34a;
          --ok-soft: #dcfce7;
          --warn: #dc2626;
          --warn-soft: #fee2e2;
          --gold: #d97706;
          --gold-soft: #fef3c7;
          --line: #cbd5e1;
          --shadow: rgba(0, 0, 0, 0.06);
          background-color: #f1f5f9;
        }
        .theme-dark {
          --surface: #1e293b;
          --surface-card: #0f172a;
          --ink: #f8fafc;
          --ink-muted: #94a3b8;
          --accent: #38bdf8;
          --accent-soft: #0369a1;
          --ok: #22c55e;
          --ok-soft: #14532d;
          --warn: #ef4444;
          --warn-soft: #7f1d1d;
          --gold: #f59e0b;
          --gold-soft: #78350f;
          --line: #334155;
          --shadow: rgba(0, 0, 0, 0.35);
          background-color: #0b1120;
        }
        text {
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          user-select: none;
        }
      `]);
      defs.appendChild(style);
      this.svg.appendChild(defs);

      this.sceneGroup = svgEl("g", { id: "scene_group" });
      this.svg.appendChild(this.sceneGroup);
      this.container.appendChild(this.svg);
    }

    setTheme(theme) {
      this.theme = theme;
      this.svg.setAttribute("class", `kinetic-stage theme-${theme}`);
    }

    updateSlots(newSlots) {
      const normalizedNew = normalizeSlots(this.def.id, newSlots);
      this.slots = Object.assign({}, this.slots, normalizedNew);
      this.seek(this.currentTime);
    }

    seek(t) {
      this.currentTime = Math.max(0, Math.min(this.duration, t));
      const builder = ANIMATIONS[this.def.id];
      if (builder) {
        const frame = builder(this.slots, this.currentTime, this.duration, this.cues);
        this.sceneGroup.replaceChildren(frame);
      }
    }
  }

  // Export to global namespace
  global.KineticRenderer = {
    AnimationInstance: KineticAnimationInstance,
    ANIMATIONS,
    normalizeSlots,
    parseAmount,
    formatIndianRupee,
    formatNumber,
    Easing
  };

})(typeof window !== "undefined" ? window : global);
