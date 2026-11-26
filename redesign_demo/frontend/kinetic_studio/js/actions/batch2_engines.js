// -*- coding: utf-8 -*-
// static/js/actions/batch2_engines.js
// Statutory Kinetic Studio - Batch 2 Action Engines:
// 1. financial_meter  2. clock_limitation  3. property_transfer  4. condition_checklist
// Strictly renders into given bounds {x, y, w, h}. Reaches final state by 65% and holds stable through 100%.

(function() {
  window.ACTION_ENGINES = window.ACTION_ENGINES || {};

  const BATCH2 = {
    /**
     * ============================================================
     * 1. FINANCIAL METER ENGINE
     * ============================================================
     * Semicircular precision instrument gauge / metric dial with statutory threshold.
     * Tabular count-up with Indian number grouping (en-IN), needle rotation,
     * threshold marker, and settled compliance verdict badge.
     * Missing data handling: draws empty track, no invented arc or %, label only.
     * Loss vs gain distinguishable by color (crimson vs emerald) and icon.
     */
    financial_meter(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      const title = payload.title || "Financial Quantum / Statutory Metric";
      const rawVal = payload.numeric_value ?? payload.current_val;
      const hasData = rawVal !== undefined && rawVal !== null && !isNaN(Number(rawVal));
      const targetVal = hasData ? Number(rawVal) : 0;

      const rawMax = payload.max_value ?? payload.max_val;
      const hasMax = rawMax !== undefined && rawMax !== null && !isNaN(Number(rawMax));
      const maxVal = hasMax ? Number(rawMax) : (hasData ? (targetVal > 0 ? targetVal * 1.5 : 10000000) : 10000000);

      const rawMin = payload.min_value ?? payload.min_val;
      const hasMin = rawMin !== undefined && rawMin !== null && !isNaN(Number(rawMin));
      const minVal = hasMin ? Number(rawMin) : 0;

      const rawThreshold = payload.threshold;
      const hasThreshold = rawThreshold !== undefined && rawThreshold !== null && !isNaN(Number(rawThreshold));
      const thresholdVal = hasThreshold ? Number(rawThreshold) : null;

      const direction = (payload.direction || "").toLowerCase(); // "gain", "loss", "threshold", or ""
      const unit = payload.unit || "₹";

      const cardW = Math.min(620, bounds.w * 0.85);
      const cardH = Math.min(350, bounds.h * 0.90);
      const cardX = bounds.x + (bounds.w - cardW) / 2;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      // Gauge geometry
      const gaugeCenterX = cardX + cardW / 2;
      const gaugeCenterY = cardY + cardH * 0.52;
      const gaugeRadius = Math.min(130, cardH * 0.38);

      const startAngle = Math.PI * 0.80; // 144 deg
      const endAngle = Math.PI * 2.20;   // 396 deg (total span: 252 deg)
      const totalSpan = endAngle - startAngle;

      const normTarget = hasData ? Math.max(0, Math.min(1, (targetVal - minVal) / (maxVal - minVal || 1))) : 0;
      const normThreshold = hasThreshold ? Math.max(0, Math.min(1, (thresholdVal - minVal) / (maxVal - minVal || 1))) : null;

      // Current progress
      const currentNorm = hasData ? (isSettle ? normTarget : (isReduced ? normTarget : normTarget * window.TWEEN.ease.easeOutCubic(effectiveP))) : 0;
      const currentAngle = startAngle + (currentNorm * totalSpan);
      const thresholdAngle = hasThreshold ? startAngle + (normThreshold * totalSpan) : null;

      // Keyed actor persistence
      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_financial_meter", { x: cardX, y: cardY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Instrument Dashboard Card
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: themeColors.borderStrong,
        radius: window.THEME.radii.lg
      });

      // Top Header
      ctx.font = window.THEME.typography.monoBadge;
      ctx.fillStyle = window.THEME.colors.accent.indigo.main;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, title.toUpperCase(), cardW - 60), gaugeCenterX, cardY + 28);

      // 2. Semicircular Gauge Track (Background)
      ctx.lineWidth = 14;
      ctx.lineCap = "round";
      ctx.strokeStyle = themeColors.bgSubtle;
      ctx.beginPath();
      ctx.arc(gaugeCenterX, gaugeCenterY, gaugeRadius, startAngle, endAngle);
      ctx.stroke();

      // Determine accent colors & icons based on direction
      let arcColor = window.THEME.colors.accent.indigo.main;
      let badgeTheme = window.THEME.colors.accent.indigo;
      let badgeIcon = "shield";
      let defaultStatus = "WITHIN STATUTORY THRESHOLD";

      if (direction === "loss") {
        arcColor = window.THEME.colors.accent.crimson.main;
        badgeTheme = window.THEME.colors.accent.crimson;
        badgeIcon = "alertTriangle";
        defaultStatus = "STATUTORY LOSS COMPUTATION";
      } else if (direction === "gain") {
        arcColor = window.THEME.colors.accent.emerald.main;
        badgeTheme = window.THEME.colors.accent.emerald;
        badgeIcon = "trendingUp";
        defaultStatus = "STATUTORY QUANTUM COMPUTATION";
      } else if (hasThreshold) {
        arcColor = window.THEME.colors.accent.indigo.main;
        badgeTheme = window.THEME.colors.accent.indigo;
        badgeIcon = "shield";
        defaultStatus = "STATUTORY THRESHOLD COMPARISON";
      }

      const statusText = payload.status || (hasData ? defaultStatus : "Amount not specified");

      // Active Value Arc - Only drawn when data is present and progress > 0
      if (hasData && currentNorm > 0) {
        ctx.strokeStyle = arcColor;
        ctx.beginPath();
        ctx.arc(gaugeCenterX, gaugeCenterY, gaugeRadius, startAngle, currentAngle);
        ctx.stroke();
      }

      // 3. Threshold Marker Tick & Label (only if threshold provided)
      if (hasThreshold && thresholdAngle !== null) {
        const thX1 = gaugeCenterX + Math.cos(thresholdAngle) * (gaugeRadius - 12);
        const thY1 = gaugeCenterY + Math.sin(thresholdAngle) * (gaugeRadius - 12);
        const thX2 = gaugeCenterX + Math.cos(thresholdAngle) * (gaugeRadius + 12);
        const thY2 = gaugeCenterY + Math.sin(thresholdAngle) * (gaugeRadius + 12);

        ctx.strokeStyle = window.THEME.colors.accent.amber.main;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(thX1, thY1);
        ctx.lineTo(thX2, thY2);
        ctx.stroke();
      }

      // 4. Center Tabular Counter Display (en-IN Indian grouping)
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      if (hasData) {
        const displayVal = Math.round(isSettle ? targetVal : (isReduced ? targetVal : targetVal * window.TWEEN.ease.easeOutCubic(effectiveP)));
        const formattedVal = `${unit} ${displayVal.toLocaleString("en-IN")}`;

        ctx.font = window.THEME.typography.hero;
        ctx.fillStyle = themeColors.textPrimary;
        ctx.fillText(formattedVal, gaugeCenterX, gaugeCenterY - 10);

        ctx.font = window.THEME.typography.caption;
        ctx.fillStyle = themeColors.textSecondary;
        if (hasThreshold) {
          const thFormatted = `${unit} ${thresholdVal.toLocaleString("en-IN")}`;
          ctx.fillText(window.SHARED_DRAW.truncate(ctx, `Statutory Threshold: ${thFormatted}`, cardW - 80), gaugeCenterX, gaugeCenterY + 28);
        } else {
          ctx.fillText(window.SHARED_DRAW.truncate(ctx, payload.subtitle || "Statutory Quantum Assessment", cardW - 80), gaugeCenterX, gaugeCenterY + 28);
        }
      } else {
        // Missing data: draw no fill, no invented percentage, label only
        ctx.font = window.THEME.typography.hero;
        ctx.fillStyle = themeColors.textMuted;
        ctx.fillText("—", gaugeCenterX, gaugeCenterY - 10);

        ctx.font = window.THEME.typography.caption;
        ctx.fillStyle = themeColors.textSecondary;
        ctx.fillText("Amount not specified", gaugeCenterX, gaugeCenterY + 28);
      }

      // Min / Max Labels at track bases
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textMuted;
      const minX = gaugeCenterX + Math.cos(startAngle) * (gaugeRadius + 22);
      const minY = gaugeCenterY + Math.sin(startAngle) * (gaugeRadius + 22);
      ctx.fillText(hasMin || hasData ? `${unit} ${minVal.toLocaleString("en-IN")}` : "—", minX, minY);

      const maxX = gaugeCenterX + Math.cos(endAngle) * (gaugeRadius + 22);
      const maxY = gaugeCenterY + Math.sin(endAngle) * (gaugeRadius + 22);
      ctx.fillText(hasMax || hasData ? `${unit} ${maxVal.toLocaleString("en-IN")}` : "—", maxX, maxY);

      // 5. Settled Compliance / Assessment Badge (Bottom)
      if (isSettle) {
        const finalBadgeTheme = hasData ? badgeTheme : { light: themeColors.bgSubtle, main: themeColors.textSecondary, border: themeColors.border };
        const finalBadgeIcon = hasData ? badgeIcon : "shield";
        const pillMaxW = Math.min(420, cardW - 40);
        window.SHARED_DRAW.pill(ctx, statusText.toUpperCase(), cardX + (cardW - pillMaxW) / 2, cardY + cardH - 46, {
          fill: finalBadgeTheme.light,
          textFill: finalBadgeTheme.main,
          stroke: finalBadgeTheme.border,
          icon: finalBadgeIcon,
          maxW: pillMaxW
        });
      }

      ctx.restore();
    },

    /**
     * ============================================================
     * 2. CLOCK LIMITATION ENGINE
     * ============================================================
     * Precision limitation clock dial with rotating limitation hand,
     * statutory deadline sector sweep, countdown card, and settled time-bar badge.
     * Hand angle and sector derived from payload (elapsed vs. limit).
     * With missing data, dial shows label only (no invented arc or hand angle).
     */
    clock_limitation(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      const actTitle = payload.act_title || "Statutory Limitation Period";
      const deadlineText = payload.deadline || "Prescribed Statutory Limitation";

      const hasElapsed = payload.elapsed !== undefined && payload.elapsed !== null && !isNaN(Number(payload.elapsed));
      const hasLimit = payload.limit !== undefined && payload.limit !== null && !isNaN(Number(payload.limit)) && Number(payload.limit) > 0;
      const hasData = hasElapsed && hasLimit;

      let ratio = 0;
      let isBarred = payload.is_barred === true;
      if (hasData) {
        ratio = Math.max(0, Number(payload.elapsed) / Number(payload.limit));
        if (ratio >= 1.0) isBarred = true;
      }

      const verdict = payload.verdict || (isBarred ? "LIMITATION PERIOD LAPSED" : "LIMITATION PERIOD COMPUTED");

      const clockR = Math.min(100, bounds.h * 0.28);
      const clockX = bounds.x + bounds.w * 0.28;
      const clockY = bounds.y + bounds.h * 0.48;

      // Rotation angles: Hand rotates from -90 deg (12 o'clock) clockwise
      const startHandAngle = -Math.PI / 2;
      const maxSweep = Math.min(Math.PI * 2, ratio * Math.PI * 2);
      const handT = isSettle ? 1.0 : (isReduced ? 1.0 : window.TWEEN.ease.easeInOutQuart(effectiveP));
      const currentHandAngle = startHandAngle + (handT * maxSweep);

      // Keyed actor persistence
      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_clock_dial", { x: clockX, y: clockY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Clock Face Outer Case
      ctx.fillStyle = themeColors.bgCard;
      ctx.strokeStyle = themeColors.borderStrong;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(clockX, clockY, clockR, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Swept Limitation Sector Arc - ONLY drawn when hasData is true and maxSweep > 0
      if (hasData && maxSweep > 0) {
        ctx.fillStyle = isBarred ? "rgba(220, 38, 38, 0.12)" : "rgba(16, 185, 129, 0.12)";
        ctx.beginPath();
        ctx.moveTo(clockX, clockY);
        ctx.arc(clockX, clockY, clockR - 4, startHandAngle, currentHandAngle, false);
        ctx.closePath();
        ctx.fill();
      }

      // 12 Clock Hour Pips
      for (let i = 0; i < 12; i++) {
        const ang = (i * Math.PI) / 6 - Math.PI / 2;
        const isMajor = i % 3 === 0;
        const pLen = isMajor ? 10 : 5;
        const px1 = clockX + Math.cos(ang) * (clockR - 6);
        const py1 = clockY + Math.sin(ang) * (clockR - 6);
        const px2 = clockX + Math.cos(ang) * (clockR - 6 - pLen);
        const py2 = clockY + Math.sin(ang) * (clockR - 6 - pLen);

        ctx.strokeStyle = isMajor ? themeColors.textPrimary : themeColors.textMuted;
        ctx.lineWidth = isMajor ? 2 : 1;
        ctx.beginPath();
        ctx.moveTo(px1, py1);
        ctx.lineTo(px2, py2);
        ctx.stroke();
      }

      // Rotating Limitation Hand - ONLY drawn when hasData is true
      if (hasData) {
        ctx.strokeStyle = isBarred ? window.THEME.colors.accent.crimson.main : window.THEME.colors.accent.indigo.main;
        ctx.lineWidth = 2.5;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(clockX, clockY);
        ctx.lineTo(
          clockX + Math.cos(currentHandAngle) * (clockR - 22),
          clockY + Math.sin(currentHandAngle) * (clockR - 22)
        );
        ctx.stroke();
      }

      // Center Pin
      ctx.fillStyle = hasData ? (isBarred ? window.THEME.colors.accent.crimson.main : window.THEME.colors.accent.indigo.main) : themeColors.textMuted;
      ctx.beginPath();
      ctx.arc(clockX, clockY, 5, 0, Math.PI * 2);
      ctx.fill();

      // 2. Right Side Limitation Dossier Card
      const cardW = Math.min(480, bounds.w * 0.52);
      const cardH = 220;
      const cardX = bounds.x + bounds.w - cardW - 30;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle && isBarred ? window.THEME.colors.accent.crimson.border : themeColors.border,
        radius: window.THEME.radii.lg
      });

      // Top Tag
      ctx.fillStyle = isBarred ? window.THEME.colors.accent.crimson.light : window.THEME.colors.accent.indigo.light;
      ctx.beginPath();
      ctx.roundRect(cardX, cardY, cardW, 46, [window.THEME.radii.lg, window.THEME.radii.lg, 0, 0]);
      ctx.fill();
      ctx.stroke();

      window.ICONS.draw(ctx, "clock", cardX + 24, cardY + 23, 20, isBarred ? window.THEME.colors.accent.crimson.main : window.THEME.colors.accent.indigo.main);

      ctx.font = window.THEME.typography.monoBadge;
      ctx.fillStyle = isBarred ? window.THEME.colors.accent.crimson.dark : window.THEME.colors.accent.indigo.dark;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, actTitle.toUpperCase(), cardW - 70), cardX + 46, cardY + 23);

      // Deadline Detail
      ctx.font = window.THEME.typography.titleBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, deadlineText, cardW - 48), cardX + 24, cardY + 82);

      ctx.font = window.THEME.typography.body;
      ctx.fillStyle = themeColors.textSecondary;
      const detailText = payload.detail || (hasData ? `Elapsed: ${payload.elapsed} of ${payload.limit} ${payload.unit || "Periods"}` : "Prescribed period within which action or appeal must be instituted.");
      window.SHARED_DRAW.wrapText(ctx, detailText, cardX + 24, cardY + 104, cardW - 48, 18, 2, "left");

      // 3. Settled Verdict Badge
      if (isSettle) {
        const badgeTheme = isBarred ? window.THEME.colors.accent.crimson : window.THEME.colors.accent.emerald;
        window.SHARED_DRAW.pill(ctx, verdict.toUpperCase(), cardX + 24, cardY + cardH - 44, {
          fill: badgeTheme.light,
          textFill: badgeTheme.main,
          stroke: badgeTheme.border,
          icon: isBarred ? "alertTriangle" : "checkCircle",
          maxW: cardW - 48
        });
      }

      ctx.restore();
    },

    /**
     * ============================================================
     * 3. PROPERTY TRANSFER ENGINE
     * ============================================================
     * Real estate architecture boundary, Transferor/Transferee bilateral stations,
     * golden title key conveying across trajectory, settled conveyance instrument badge.
     * Universal statutory neutrality: No jurisdiction-specific wording ("VESTED & MUTATED").
     */
    property_transfer(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      const transferor = payload.transferor || "Transferor Entity";
      const transferee = payload.transferee || "Transferee Entity";
      const propertyDesc = payload.property_desc || "Commercial Immovable Asset";
      const deedText = payload.deed_title || payload.instrument || "Registered Instrument";
      const statusText = payload.status || "CONVEYANCE INSTRUMENT EXECUTED";

      const stationW = Math.min(220, bounds.w * 0.26);
      const stationH = 120;
      const stationY = bounds.y + bounds.h * 0.52;

      const leftX = bounds.x + 30;
      const rightX = bounds.x + bounds.w - stationW - 30;

      // Key travel
      const startX = leftX + stationW;
      const startY = stationY + 40;
      const endX = rightX;
      const endY = stationY + 40;
      const keyT = isSettle ? 1.0 : (isReduced ? 1.0 : window.TWEEN.ease.easeInOutQuart(effectiveP));

      // Keyed actor persistence
      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_property_asset", { x: leftX, y: stationY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Central Architectural Building Silhouette
      const bldgCenterX = bounds.x + bounds.w / 2;
      const bldgY = bounds.y + 40;
      const bldgW = 160;
      const bldgH = 130;

      // Building Card
      window.SHARED_DRAW.card(ctx, bldgCenterX - (bldgW / 2), bldgY, bldgW, bldgH, {
        fill: themeColors.bgCard,
        stroke: themeColors.borderStrong,
        radius: window.THEME.radii.md
      });

      // Roof Gable
      ctx.fillStyle = window.THEME.colors.accent.indigo.light;
      ctx.strokeStyle = window.THEME.colors.accent.indigo.border;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(bldgCenterX - (bldgW / 2), bldgY + 36);
      ctx.lineTo(bldgCenterX, bldgY + 6);
      ctx.lineTo(bldgCenterX + (bldgW / 2), bldgY + 36);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Building Icon
      window.ICONS.draw(ctx, "building", bldgCenterX, bldgY + 68, 32, window.THEME.colors.accent.indigo.main);

      // Property Label
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      let dispProp = propertyDesc;
      if (ctx.measureText(dispProp).width > (bldgW - 20)) {
        while (dispProp.length > 3 && ctx.measureText(dispProp + "…").width > (bldgW - 20)) {
          dispProp = dispProp.slice(0, -1);
        }
        dispProp += "…";
      }
      ctx.fillText(dispProp, bldgCenterX, bldgY + 110);

      // 2. Transferor Card (Left)
      window.SHARED_DRAW.card(ctx, leftX, stationY, stationW, stationH, {
        fill: themeColors.bgCard,
        stroke: window.THEME.colors.accent.indigo.border
      });
      window.ICONS.draw(ctx, "user", leftX + 32, stationY + 36, 22, window.THEME.colors.accent.indigo.main);
      ctx.font = window.THEME.typography.titleBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      let dispTransferor = transferor;
      const maxPartyW = stationW - 65;
      if (ctx.measureText(dispTransferor).width > maxPartyW) {
        while (dispTransferor.length > 3 && ctx.measureText(dispTransferor + "…").width > maxPartyW) {
          dispTransferor = dispTransferor.slice(0, -1);
        }
        dispTransferor += "…";
      }
      ctx.fillText(dispTransferor, leftX + 54, stationY + 36);

      ctx.font = window.THEME.typography.caption;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, payload.transferor_role || "Transferor Entity", maxPartyW), leftX + 24, stationY + 74);

      // 3. Transferee Card (Right)
      window.SHARED_DRAW.card(ctx, rightX, stationY, stationW, stationH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? window.THEME.colors.accent.emerald.border : themeColors.border
      });
      window.ICONS.draw(ctx, "user", rightX + 32, stationY + 36, 22, isSettle ? window.THEME.colors.accent.emerald.main : themeColors.textMuted);
      ctx.font = window.THEME.typography.titleBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      let dispTransferee = transferee;
      if (ctx.measureText(dispTransferee).width > maxPartyW) {
        while (dispTransferee.length > 3 && ctx.measureText(dispTransferee + "…").width > maxPartyW) {
          dispTransferee = dispTransferee.slice(0, -1);
        }
        dispTransferee += "…";
      }
      ctx.fillText(dispTransferee, rightX + 54, stationY + 36);

      ctx.font = window.THEME.typography.caption;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, payload.transferee_role || "Transferee Entity", maxPartyW), rightX + 24, stationY + 74);

      // 4. Trajectory Arc & Key Transfer
      const proj = window.SHARED_DRAW.trajectoryArc(ctx, startX, startY, endX, endY, -60, keyT, window.THEME.colors.accent.amber.main);

      // Key Token
      if (!isSettle && p > 0.15) {
        const kx = proj.x;
        const ky = proj.y;
        ctx.save();
        ctx.translate(kx, ky);
        ctx.fillStyle = "#F59E0B";
        ctx.strokeStyle = "#D97706";
        ctx.lineWidth = 1.5;
        // Key head
        ctx.beginPath();
        ctx.arc(0, 0, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        // Inner cutout
        ctx.fillStyle = themeColors.bgCard;
        ctx.beginPath();
        ctx.arc(0, 0, 4, 0, Math.PI * 2);
        ctx.fill();
        // Key shaft & teeth
        ctx.fillStyle = "#F59E0B";
        ctx.fillRect(8, -2, 14, 4);
        ctx.fillRect(16, 2, 3, 5);
        ctx.fillRect(20, 2, 3, 4);
        ctx.restore();
      }

      // 5. Settled Title Conveyance Badge (Bottom)
      if (isSettle) {
        const conveyText = `${statusText.toUpperCase()}: ${deedText.toUpperCase()}`;
        const pillMaxW = Math.min(500, bounds.w - 60);
        window.SHARED_DRAW.pill(ctx, conveyText, bounds.x + (bounds.w - Math.min(460, pillMaxW)) / 2, bounds.y + bounds.h - 48, {
          fill: window.THEME.colors.accent.emerald.light,
          textFill: window.THEME.colors.accent.emerald.main,
          stroke: window.THEME.colors.accent.emerald.border,
          icon: "checkCircle",
          maxW: pillMaxW
        });
      }

      ctx.restore();
    },

    /**
     * ============================================================
     * 4. CONDITION CHECKLIST ENGINE
     * ============================================================
     * Multi-step statutory criteria compliance board.
     * Checkmarks spring into place sequentially across PERFORM phase,
     * concluding in settled emerald all-satisfied banner.
     * Derived dynamically: "ALL N CONDITIONS" derived from actual criteria count.
     */
    condition_checklist(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME && window.THEME.prefersReducedMotion();

      const title = payload.title || "Statutory Condition Evaluation";
      const logic = String(payload.logic || "all_required").toLowerCase();

      // Normalize conditions
      let rawConditions = payload.conditions;
      if (!rawConditions && Array.isArray(payload.criteria)) {
        rawConditions = payload.criteria;
      }
      if (!Array.isArray(rawConditions)) {
        rawConditions = [];
      }

      const conditions = rawConditions.map((c, idx) => {
        if (typeof c === "string") {
          return { idx: idx + 1, rule: c, fact: "", status: "met" };
        }
        let st = String(c.status || "").toLowerCase();
        if (!st) {
          if (c.satisfied === true) st = "met";
          else if (c.satisfied === false) st = "not_met";
          else st = "met";
        }
        if (!["met", "not_met", "not_applicable", "unclear"].includes(st)) {
          st = "unclear";
        }
        return {
          idx: idx + 1,
          rule: String(c.rule || c.text || c.label || `Condition ${idx + 1}`),
          fact: c.fact ? String(c.fact) : "",
          status: st
        };
      });

      if (conditions.length === 0) {
        conditions.push({
          idx: 1,
          rule: "Statutory Condition Evaluation",
          fact: "",
          status: "unclear"
        });
      }

      const n = Math.max(1, conditions.length);

      // Determine overall outcome derived in code
      let outcomeStatus = "met"; // "met" | "not_met" | "unclear" | "weighted"
      let outcomeText = "";

      if (logic === "weighted_or_custom") {
        outcomeStatus = "weighted";
        outcomeText = "Outcome depends on statute-specific weighting";
      } else {
        const applicable = conditions.filter(c => c.status !== "not_applicable");
        const hasUnclear = applicable.some(c => c.status === "unclear");
        const anyMet = applicable.some(c => c.status === "met");
        const allMet = applicable.length > 0 && applicable.every(c => c.status === "met");
        const anyNotMet = applicable.some(c => c.status === "not_met");

        if (logic === "any_one") {
          if (anyMet) {
            outcomeStatus = "met";
            outcomeText = payload.outcome_met_label || "Conditions met";
          } else if (hasUnclear) {
            outcomeStatus = "unclear";
            outcomeText = "Cannot be determined from the facts";
          } else {
            outcomeStatus = "not_met";
            outcomeText = payload.outcome_not_met_label || "Conditions not met";
          }
        } else {
          // default: all_required
          if (anyNotMet) {
            outcomeStatus = "not_met";
            outcomeText = payload.outcome_not_met_label || "Conditions not met";
          } else if (hasUnclear) {
            outcomeStatus = "unclear";
            outcomeText = "Cannot be determined from the facts";
          } else if (allMet) {
            outcomeStatus = "met";
            outcomeText = payload.outcome_met_label || "Conditions met";
          } else {
            outcomeStatus = "unclear";
            outcomeText = "Cannot be determined from the facts";
          }
        }
      }

      // Card Bounds
      const boardW = Math.min(1000, bounds.w * 0.98);
      const boardH = Math.min(450, bounds.h * 0.96);
      const boardX = bounds.x + (bounds.w - boardW) / 2;
      const boardY = bounds.y + (bounds.h - boardH) / 2;

      // Layout chosen from N: 1-4 stacked rows; 5-6 two columns of cards; 7-8 compact rows
      const isTwoColumn = n >= 5;
      const midPoint = isTwoColumn ? Math.ceil(n / 2) : n;

      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_checklist_board", { x: boardX, y: boardY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Container Card
      window.SHARED_DRAW.card(ctx, boardX, boardY, boardW, boardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? themeColors.borderStrong : themeColors.border,
        radius: window.THEME.radii.lg
      });

      // Header Ribbon (42px)
      ctx.fillStyle = themeColors.bgSubtle;
      ctx.beginPath();
      ctx.roundRect(boardX, boardY, boardW, 42, [window.THEME.radii.lg, window.THEME.radii.lg, 0, 0]);
      ctx.fill();
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1;
      ctx.stroke();

      window.ICONS.draw(ctx, "shieldCheck", boardX + 22, boardY + 21, 18, window.THEME.colors.accent.indigo.main);

      ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, title.toUpperCase(), boardW - 220), boardX + 44, boardY + 21);

      // Logic Pill on Right
      const logicBadge = logic === "any_one" ? "ANY ONE REQUIRED" : (logic === "weighted_or_custom" ? "STATUTORY WEIGHTING" : "ALL REQUIRED");
      window.SHARED_DRAW.pill(ctx, logicBadge, boardX + boardW - 160, boardY + 10, {
        fill: themeColors.bgCard,
        textFill: themeColors.textSecondary,
        stroke: themeColors.border,
        maxW: 150
      });

      // 2. Fixed Outcome Banner (Bottom 48px)
      const bannerH = 48;
      const bannerY = boardY + boardH - bannerH - 12;
      const bannerW = boardW - 32;
      const bannerX = boardX + 16;
      const bannerP = isSettle ? 1.0 : window.TWEEN.remap(effectiveP, 0.70, 1.0, 0, 1);
      const showBanner = isSettle || bannerP > 0;

      // Available height for conditions
      const listStartY = boardY + 48;
      const availH = bannerY - listStartY - 8;
      const rowsPerCol = isTwoColumn ? midPoint : n;
      const rowH = Math.max(34, Math.floor(availH / rowsPerCol));

      // 3. Render Conditions
      conditions.forEach((cond, idx) => {
        const isCol2 = isTwoColumn && idx >= midPoint;
        const colIdx = isCol2 ? 1 : 0;
        const rowInCol = isCol2 ? (idx - midPoint) : idx;

        const colW = isTwoColumn ? (boardW - 48) / 2 : (boardW - 32);
        const colX = isTwoColumn ? (boardX + 16 + colIdx * (colW + 16)) : (boardX + 16);
        const ry = listStartY + rowInCol * rowH;

        // Progressive evaluation flip during PERFORM
        const subStart = idx / n;
        const subEnd = (idx + 1) / n;
        const itemP = isSettle ? 1.0 : (isReduced ? 1.0 : window.TWEEN.getSubPhase(effectiveP, subStart, subEnd));
        const isItemEvaluated = itemP >= 0.99;
        const rowAlpha = isSettle ? 1.0 : (isReduced ? 1.0 : (0.25 + 0.75 * itemP));

        ctx.save();
        ctx.globalAlpha = rowAlpha;

        // Row Card Background
        const isDark = window.THEME && window.THEME.mode === "dark";
        let rowBg = isDark ? "rgba(30, 41, 59, 0.35)" : themeColors.bgCard;
        let rowBorder = themeColors.border;

        if (isItemEvaluated) {
          if (cond.status === "met") {
            rowBorder = window.THEME.colors.accent.emerald.border;
          } else if (cond.status === "not_met") {
            rowBorder = window.THEME.colors.accent.crimson.border;
          }
        }

        ctx.fillStyle = rowBg;
        ctx.strokeStyle = rowBorder;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(colX, ry + 2, colW, rowH - 4, window.THEME.radii.sm);
        ctx.fill();
        ctx.stroke();

        // Condition index badge
        ctx.fillStyle = themeColors.bgSubtle;
        ctx.beginPath();
        ctx.arc(colX + 18, ry + rowH / 2, 10, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = "700 12px 'JetBrains Mono', monospace";
        ctx.fillStyle = themeColors.textPrimary;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(cond.idx), colX + 18, ry + rowH / 2);

        // Badge Width and Position
        const badgeW = (cond.status === "not_applicable") ? 130 : ((cond.status === "not_met") ? 86 : 72);
        const textStartX = colX + 36;
        const textMaxW = colW - (textStartX - colX) - badgeW - 16;

        // Text: Rule (Primary) and Fact (Secondary)
        ctx.textAlign = "left";
        ctx.font = "600 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = themeColors.textPrimary;

        let ruleText = cond.rule;
        if (ctx.measureText(ruleText).width > textMaxW) {
          while (ruleText.length > 3 && ctx.measureText(ruleText + "…").width > textMaxW) {
            ruleText = ruleText.slice(0, -1);
          }
          ruleText += "…";
        }

        if (cond.fact && rowH >= 44) {
          ctx.textBaseline = "middle";
          ctx.fillText(ruleText, textStartX, ry + rowH / 2 - 8);

          ctx.font = "400 12px 'Plus Jakarta Sans', sans-serif";
          ctx.fillStyle = themeColors.textSecondary;
          let factText = cond.fact;
          if (ctx.measureText(factText).width > textMaxW) {
            while (factText.length > 3 && ctx.measureText(factText + "…").width > textMaxW) {
              factText = factText.slice(0, -1);
            }
            factText += "…";
          }
          ctx.fillText(factText, textStartX, ry + rowH / 2 + 9);
        } else {
          ctx.textBaseline = "middle";
          ctx.fillText(ruleText, textStartX, ry + rowH / 2);
        }

        // Status Badge (MET / NOT MET / NOT APPLICABLE / UNCLEAR)
        const badgeX = colX + colW - badgeW - 10;
        const badgeY = ry + (rowH - 24) / 2;

        if (isItemEvaluated) {
          let bFill, bText, bStroke, bIcon, bLabel;
          if (cond.status === "met") {
            bFill = isDark ? "rgba(5, 150, 105, 0.22)" : window.THEME.colors.accent.emerald.light;
            bText = isDark ? "#34D399" : window.THEME.colors.accent.emerald.main;
            bStroke = window.THEME.colors.accent.emerald.border;
            bIcon = "checkCircle";
            bLabel = "MET";
          } else if (cond.status === "not_met") {
            bFill = isDark ? "rgba(220, 38, 38, 0.22)" : window.THEME.colors.accent.crimson.light;
            bText = isDark ? "#F87171" : window.THEME.colors.accent.crimson.main;
            bStroke = window.THEME.colors.accent.crimson.border;
            bIcon = "alertCircle";
            bLabel = "NOT MET";
          } else if (cond.status === "not_applicable") {
            bFill = isDark ? "rgba(100, 116, 139, 0.20)" : themeColors.bgSubtle;
            bText = themeColors.textMuted;
            bStroke = themeColors.border;
            bIcon = "info";
            bLabel = "NOT APPLICABLE";
          } else {
            // unclear
            bFill = isDark ? "rgba(217, 119, 6, 0.22)" : window.THEME.colors.accent.amber.light;
            bText = isDark ? "#FBBF24" : window.THEME.colors.accent.amber.main;
            bStroke = window.THEME.colors.accent.amber.border;
            bIcon = "helpCircle";
            bLabel = "UNCLEAR";
          }

          window.SHARED_DRAW.pill(ctx, bLabel, badgeX, badgeY, {
            fill: bFill,
            textFill: bText,
            stroke: bStroke,
            icon: bIcon
          });
        } else {
          // Pending status
          window.SHARED_DRAW.pill(ctx, "EVALUATING", badgeX, badgeY, {
            fill: themeColors.bgSubtle,
            textFill: themeColors.textMuted,
            stroke: themeColors.border
          });
        }

        ctx.restore();
      });

      // 4. Settled Outcome Banner at Bottom
      const bannerAlpha = isSettle ? 1.0 : (isReduced ? 1.0 : (0.25 + 0.75 * bannerP));
      ctx.save();
      ctx.globalAlpha = bannerAlpha;

        const isDark = window.THEME && window.THEME.mode === "dark";
        let bannerBg, bannerBorder, bannerIcon, bannerTextColor;

        if (outcomeStatus === "met") {
          bannerBg = isDark ? "rgba(5, 150, 105, 0.22)" : window.THEME.colors.accent.emerald.light;
          bannerBorder = window.THEME.colors.accent.emerald.border;
          bannerIcon = "shieldCheck";
          bannerTextColor = isDark ? "#34D399" : window.THEME.colors.accent.emerald.main;
        } else if (outcomeStatus === "not_met") {
          bannerBg = isDark ? "rgba(220, 38, 38, 0.22)" : window.THEME.colors.accent.crimson.light;
          bannerBorder = window.THEME.colors.accent.crimson.border;
          bannerIcon = "alertTriangle";
          bannerTextColor = isDark ? "#F87171" : window.THEME.colors.accent.crimson.main;
        } else if (outcomeStatus === "weighted") {
          bannerBg = isDark ? "rgba(99, 102, 241, 0.20)" : window.THEME.colors.accent.indigo.light;
          bannerBorder = window.THEME.colors.accent.indigo.border;
          bannerIcon = "info";
          bannerTextColor = isDark ? "#818CF8" : window.THEME.colors.accent.indigo.main;
        } else {
          // unclear
          bannerBg = isDark ? "rgba(217, 119, 6, 0.20)" : window.THEME.colors.accent.amber.light;
          bannerBorder = window.THEME.colors.accent.amber.border;
          bannerIcon = "helpCircle";
          bannerTextColor = isDark ? "#FBBF24" : window.THEME.colors.accent.amber.main;
        }

        ctx.fillStyle = bannerBg;
        ctx.strokeStyle = bannerBorder;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(bannerX, bannerY, bannerW, bannerH, window.THEME.radii.md);
        ctx.fill();
        ctx.stroke();

        window.ICONS.draw(ctx, bannerIcon, bannerX + 24, bannerY + bannerH / 2, 20, bannerTextColor);

        ctx.font = "700 14px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = bannerTextColor;
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(window.SHARED_DRAW.truncate(ctx, outcomeText.toUpperCase(), bannerW - 80), bannerX + 44, bannerY + bannerH / 2);

        ctx.restore();

      ctx.restore();
    }
  };

  // Register Batch 2 engines onto global ACTION_ENGINES
  Object.assign(window.ACTION_ENGINES, BATCH2);
})();
