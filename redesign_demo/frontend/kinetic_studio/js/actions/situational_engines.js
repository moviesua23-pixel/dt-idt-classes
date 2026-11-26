// -*- coding: utf-8 -*-
// static/js/actions/situational_engines.js
// Statutory Kinetic Studio - Situational Action Engines for Real-World Scenarios
// 1. hazard_calamity  2. unauthorized_diversion  3. custody_bailment
// Strictly renders into given bounds {x, y, w, h}. Reaches final state by 65% and holds stable through 100%.

(function() {
  window.ACTION_ENGINES = window.ACTION_ENGINES || {};

  const SITUATIONAL_ENGINES = {
    /**
     * ============================================================
     * 1. HAZARD / CALAMITY ENGINE
     * ============================================================
     * Calamity events: fires, earthquakes, floods, boiler explosions, accidental loss.
     * Central asset/premises card with kinetic impact, seismic fault/heat fracture,
     * and settled alert pill.
     * Zero hardcoded legal conclusions: outcome text is payload-driven;
     * neutral fallbacks: "Event", "Loss".
     * Accessibility: Zero shake under prefers-reduced-motion; pulse stops by 65%.
     */
    hazard_calamity(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      // Payload parameters (strictly payload-driven; neutral fallbacks only)
      const eventTitle = payload.event_title || payload.title || "Event";
      const affectedAsset = payload.affected_asset || payload.asset || "Subject Matter";
      const cause = payload.cause || "";
      const consequence = payload.statutory_consequence || payload.consequence || "Loss";
      const calamityType = (payload.calamity_type || "general").toLowerCase();

      // Card geometry
      const cardW = Math.min(680, bounds.w * 0.88);
      const cardH = Math.min(340, bounds.h * 0.86);
      const baseX = bounds.x + (bounds.w - cardW) / 2;
      const baseY = bounds.y + (bounds.h - cardH) / 2;

      // Accessibility: No shake under prefersReducedMotion; stops at 65%
      let shakeX = 0;
      let shakeY = 0;
      if (!isReduced && !isSettle && p > 0.12 && p < 0.65) {
        const decay = 1.0 - effectiveP;
        shakeX = Math.sin(p * Math.PI * 14) * decay * 7;
        shakeY = Math.cos(p * Math.PI * 12) * decay * 4;
      }

      const cardX = baseX + shakeX;
      const cardY = baseY + shakeY;

      ctx.save();

      // 1. Base card container
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? window.THEME.colors.accent.crimson.border : themeColors.borderStrong,
        radius: window.THEME.radii.lg
      });

      // 2. Calamity Header Bar
      const headerH = 52;
      ctx.fillStyle = themeColors.bgMuted;
      ctx.beginPath();
      ctx.moveTo(cardX + 12, cardY);
      ctx.lineTo(cardX + cardW - 12, cardY);
      ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + 12);
      ctx.lineTo(cardX + cardW, cardY + headerH);
      ctx.lineTo(cardX, cardY + headerH);
      ctx.lineTo(cardX, cardY + 12);
      ctx.quadraticCurveTo(cardX, cardY, cardX + 12, cardY);
      ctx.closePath();
      ctx.fill();

      // Header bottom border
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cardX, cardY + headerH);
      ctx.lineTo(cardX + cardW, cardY + headerH);
      ctx.stroke();

      // Icon selection based on calamityType
      let iconName = "alertTriangle";
      if (calamityType.includes("fire") || calamityType.includes("explosion") || calamityType.includes("heat")) {
        iconName = "flame";
      } else if (calamityType.includes("earthquake") || calamityType.includes("tremor") || calamityType.includes("quake")) {
        iconName = "tremor";
      } else if (calamityType.includes("flood") || calamityType.includes("ship") || calamityType.includes("sea")) {
        iconName = "ship";
      } else if (calamityType.includes("factory") || calamityType.includes("plant") || calamityType.includes("boiler")) {
        iconName = "factory";
      } else if (calamityType.includes("vehicle") || calamityType.includes("car") || calamityType.includes("truck")) {
        iconName = "car";
      }

      // Draw Header Icon
      window.ICONS.draw(
        ctx,
        iconName,
        cardX + 28,
        cardY + headerH / 2,
        22,
        window.THEME.colors.accent.crimson.main,
        1.75
      );

      // Event Title
      ctx.font = window.THEME.typography.monoBadge;
      ctx.fillStyle = window.THEME.colors.accent.crimson.main;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      let titleStr = eventTitle.toUpperCase();
      const maxHeaderTitleW = cardW - 70;
      if (ctx.measureText(titleStr).width > maxHeaderTitleW) {
        while (titleStr.length > 3 && ctx.measureText(titleStr + "…").width > maxHeaderTitleW) {
          titleStr = titleStr.slice(0, -1);
        }
        titleStr += "…";
      }
      ctx.fillText(titleStr, cardX + 48, cardY + headerH / 2);

      // 3. Central Asset Representation Box
      const assetBoxX = cardX + 24;
      const assetBoxY = cardY + headerH + 18;
      const assetBoxW = cardW - 48;
      const assetBoxH = 110;
      const maxAssetLineW = assetBoxW - 75;

      ctx.fillStyle = themeColors.bgMuted;
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1.25;
      ctx.beginPath();
      ctx.roundRect(assetBoxX, assetBoxY, assetBoxW, assetBoxH, 8);
      ctx.fill();
      ctx.stroke();

      // Asset Label & Icon
      window.ICONS.draw(
        ctx,
        "building",
        assetBoxX + 32,
        assetBoxY + 36,
        26,
        themeColors.textSecondary,
        1.5
      );

      ctx.font = window.THEME.typography.titleBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      let dispAsset = affectedAsset;
      if (ctx.measureText(dispAsset).width > maxAssetLineW) {
        while (dispAsset.length > 3 && ctx.measureText(dispAsset + "…").width > maxAssetLineW) {
          dispAsset = dispAsset.slice(0, -1);
        }
        dispAsset += "…";
      }
      ctx.fillText(dispAsset, assetBoxX + 58, assetBoxY + 36);

      // Cause line if provided
      if (cause) {
        ctx.font = window.THEME.typography.body;
        ctx.fillStyle = themeColors.textSecondary;
        let dispCause = cause;
        if (ctx.measureText(dispCause).width > maxAssetLineW) {
          while (dispCause.length > 3 && ctx.measureText(dispCause + "…").width > maxAssetLineW) {
            dispCause = dispCause.slice(0, -1);
          }
          dispCause += "…";
        }
        ctx.fillText(dispCause, assetBoxX + 58, assetBoxY + 66);
      }

      // 4. Kinetic Fracture Line (appears across asset during perform phase)
      if (effectiveP > 0.25) {
        const fractureP = isSettle ? 1.0 : window.TWEEN.remap(effectiveP, 0.25, 0.65, 0, 1);
        ctx.strokeStyle = window.THEME.colors.accent.crimson.main;
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        ctx.beginPath();

        const fStartX = assetBoxX + assetBoxW * 0.45;
        const fStartY = assetBoxY + 12;
        const pts = [
          [fStartX, fStartY],
          [fStartX + 18, fStartY + 25],
          [fStartX - 12, fStartY + 50],
          [fStartX + 22, fStartY + 75],
          [fStartX + 8, fStartY + assetBoxH - 12]
        ];

        ctx.moveTo(pts[0][0], pts[0][1]);
        const maxIdx = Math.min(pts.length - 1, Math.floor(fractureP * (pts.length - 1)) + 1);
        for (let i = 1; i <= maxIdx; i++) {
          const prev = pts[i - 1];
          const curr = pts[i];
          const segProgress = Math.min(1, (fractureP * (pts.length - 1)) - (i - 1));
          if (segProgress > 0) {
            const ix = prev[0] + (curr[0] - prev[0]) * segProgress;
            const iy = prev[1] + (curr[1] - prev[1]) * segProgress;
            ctx.lineTo(ix, iy);
          }
        }
        ctx.stroke();
      }

      // 5. Settled Consequence Badge
      const badgeY = assetBoxY + assetBoxH + 24;

      // Slow non-flashing pulse that halts strictly by 65%
      let pulseAlpha = 0.95;
      if (!isReduced && !isSettle && p > 0.2 && p < 0.65) {
        pulseAlpha = 0.70 + 0.25 * Math.sin(p * Math.PI * 4);
      }

      ctx.save();
      ctx.globalAlpha = isSettle ? 1.0 : pulseAlpha;

      window.SHARED_DRAW.pill(ctx, consequence, cardX + 24, badgeY, {
        fill: window.THEME.colors.accent.crimson.light,
        textFill: window.THEME.colors.accent.crimson.main,
        stroke: window.THEME.colors.accent.crimson.border,
        icon: "alertTriangle",
        paddingX: 16,
        maxW: cardW - 48
      });

      ctx.restore();
      ctx.restore();
    },

    /**
     * ============================================================
     * 2. UNAUTHORIZED DIVERSION / FRAUD ENGINE
     * ============================================================
     * Factual matrix: Fund/asset siphoning, embezzlement, kickbacks, ghost payroll.
     * Shows source entity, authorized destination channel, and diverted stream
     * dropping into unauthorized account.
     * Fully driven by payload: source, intended_recipient, diverted_to, amount, who_acted.
     * Zero hardcoded legal conclusions: outcome text is payload-driven;
     * neutral fallbacks: "Diversion", "Source", "Diverted".
     * Accessibility: Pulse halts by 65%; no rapid flashing.
     */
    unauthorized_diversion(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      // Payload parameters
      const title = payload.title || "Diversion";
      const source = payload.source || payload.from_account || "Source";
      const intended = payload.intended_recipient || payload.intended_purpose || "Intended Destination";
      const divertedTo = payload.diverted_to || payload.unauthorized_recipient || "Diverted Account";
      const amountStr = payload.amount ? (payload.amount.toString().startsWith("₹") ? payload.amount : "₹" + payload.amount) : "";
      const whoActed = payload.who_acted || payload.actor || "";
      const statusText = payload.status || payload.consequence || "Diversion";

      // Card geometry
      const cardW = Math.min(680, bounds.w * 0.88);
      const cardH = Math.min(350, bounds.h * 0.88);
      const cardX = bounds.x + (bounds.w - cardW) / 2;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      ctx.save();

      // 1. Background Card
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? window.THEME.colors.accent.amber.border : themeColors.borderStrong,
        radius: window.THEME.radii.lg
      });

      // 2. Header
      const headerH = 46;
      ctx.fillStyle = themeColors.bgMuted;
      ctx.beginPath();
      ctx.moveTo(cardX + 12, cardY);
      ctx.lineTo(cardX + cardW - 12, cardY);
      ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + 12);
      ctx.lineTo(cardX + cardW, cardY + headerH);
      ctx.lineTo(cardX, cardY + headerH);
      ctx.lineTo(cardX, cardY + 12);
      ctx.quadraticCurveTo(cardX, cardY, cardX + 12, cardY);
      ctx.closePath();
      ctx.fill();

      window.ICONS.draw(ctx, "siphon", cardX + 26, cardY + headerH / 2, 20, window.THEME.colors.accent.amber.main, 1.75);

      ctx.font = window.THEME.typography.monoBadge;
      ctx.fillStyle = window.THEME.colors.accent.amber.main;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, title.toUpperCase(), cardW - 160), cardX + 44, cardY + headerH / 2);

      if (whoActed) {
        ctx.font = window.THEME.typography.caption;
        ctx.fillStyle = themeColors.textSecondary;
        ctx.textAlign = "right";
        ctx.fillText(window.SHARED_DRAW.truncate(ctx, whoActed, 140), cardX + cardW - 24, cardY + headerH / 2);
      }

      // 3. Three Nodes: Source (Top-Left), Intended (Top-Right), Diverted (Bottom-Center)
      const nodeW = 205;
      const nodeH = 68;

      const srcX = cardX + 24;
      const srcY = cardY + headerH + 24;

      const intX = cardX + cardW - nodeW - 24;
      const intY = srcY;

      const divX = cardX + (cardW - nodeW) / 2;
      const divY = cardY + cardH - nodeH - 58;

      // Draw Source Node
      window.SHARED_DRAW.card(ctx, srcX, srcY, nodeW, nodeH, {
        fill: themeColors.bgMuted,
        stroke: themeColors.borderStrong,
        radius: 8
      });
      window.ICONS.draw(ctx, "bank", srcX + 22, srcY + 24, 20, themeColors.textSecondary, 1.5);
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.textAlign = "left";
      ctx.fillText("SOURCE", srcX + 40, srcY + 24);
      ctx.font = window.THEME.typography.bodyBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, source, nodeW - 28), srcX + 14, srcY + 50);

      // Draw Intended Destination Node
      window.SHARED_DRAW.card(ctx, intX, intY, nodeW, nodeH, {
        fill: themeColors.bgMuted,
        stroke: themeColors.border,
        radius: 8
      });
      window.ICONS.draw(ctx, "building", intX + 22, intY + 24, 20, themeColors.textSecondary, 1.5);
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.textAlign = "left";
      ctx.fillText("INTENDED", intX + 40, intY + 24);
      ctx.font = window.THEME.typography.bodyBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, intended, nodeW - 28), intX + 14, intY + 50);

      // Normal Flow Line (Source -> Intended) - Dotted / Weak
      ctx.strokeStyle = themeColors.border;
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(srcX + nodeW, srcY + nodeH / 2);
      ctx.lineTo(intX, intY + nodeH / 2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw Diverted Account Node (Bottom)
      const isDark = window.THEME && window.THEME.mode === "dark";
      const divFill = isDark ? "rgba(220, 38, 38, 0.22)" : window.THEME.colors.accent.crimson.light;
      const divBorderColor = isDark
        ? (isSettle ? "rgba(248, 113, 113, 0.6)" : themeColors.borderStrong)
        : (isSettle ? window.THEME.colors.accent.crimson.border : themeColors.borderStrong);
      const divIconColor = isDark ? "#F87171" : window.THEME.colors.accent.crimson.main;

      window.SHARED_DRAW.card(ctx, divX, divY, nodeW, nodeH, {
        fill: divFill,
        stroke: divBorderColor,
        radius: 8
      });
      window.ICONS.draw(ctx, "cross", divX + 22, divY + 24, 20, divIconColor, 1.5);
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = divIconColor;
      ctx.textAlign = "left";
      ctx.fillText("DIVERTED TO", divX + 40, divY + 24);
      ctx.font = window.THEME.typography.bodyBold;
      ctx.fillStyle = themeColors.textPrimary;
      ctx.fillText(window.SHARED_DRAW.truncate(ctx, divertedTo, nodeW - 28), divX + 14, divY + 50);

      // 4. Kinetic Diverted Stream (Curve from midpoint of source-to-intended down to Diverted Node)
      const midFlowX = srcX + nodeW + 30;
      const midFlowY = srcY + nodeH / 2;
      const targetDivX = divX + nodeW / 2;
      const targetDivY = divY;

      const pathProgress = isSettle ? 1.0 : window.TWEEN.ease.easeInOutQuart(effectiveP);

      ctx.strokeStyle = window.THEME.colors.accent.crimson.main;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(srcX + nodeW, srcY + nodeH / 2);
      ctx.lineTo(midFlowX, midFlowY);

      // Curve down to diverted node
      const currentEndX = midFlowX + (targetDivX - midFlowX) * pathProgress;
      const currentEndY = midFlowY + (targetDivY - midFlowY) * pathProgress;
      ctx.quadraticCurveTo(midFlowX + 20, midFlowY + 30, currentEndX, currentEndY);
      ctx.stroke();

      // Moving Token or Siphoned Amount Pill
      if (amountStr) {
        const pillX = midFlowX + 10;
        const pillY = midFlowY + 20;
        ctx.fillStyle = window.THEME.colors.accent.crimson.main;
        ctx.beginPath();
        ctx.roundRect(pillX, pillY, 110, 26, 13);
        ctx.fill();
        ctx.font = window.THEME.typography.monoBadge;
        ctx.fillStyle = "#FFFFFF";
        ctx.textAlign = "center";
        ctx.fillText(amountStr, pillX + 55, pillY + 13);
      }

      // 5. Settled Alert Pill at Bottom
      const bottomPillY = cardY + cardH - 38;
      let alertAlpha = 1.0;
      if (!isReduced && !isSettle && p > 0.3 && p < 0.65) {
        alertAlpha = 0.75 + 0.25 * Math.sin(p * Math.PI * 4);
      }

      ctx.save();
      ctx.globalAlpha = isSettle ? 1.0 : alertAlpha;
      window.SHARED_DRAW.pill(ctx, statusText, cardX + 24, bottomPillY, {
        fill: window.THEME.colors.accent.crimson.light,
        textFill: window.THEME.colors.accent.crimson.main,
        stroke: window.THEME.colors.accent.crimson.border,
        icon: "alertTriangle",
        maxW: cardW - 48
      });
      ctx.restore();

      ctx.restore();
    },

    /**
     * ============================================================
     * 3. CUSTODY / BAILMENT ENGINE
     * ============================================================
     * Factual matrix: Bailment, custody, pawn/pledge, dry-cleaning, repairs, valet parking.
     * Two primary parties: Bailor (Owner) and Bailee (Custodian).
     * Smooth custodial transfer beam with goods item token, custodial lock/tag,
     * and settled custody status badge.
     * Fully driven by payload: bailor, bailee, goods_item, purpose, custody_status.
     * Zero hardcoded legal conclusions: neutral fallbacks only: "Custody", "Bailor", "Bailee".
     * Accessibility: Slow smooth transitions; stops by 65%.
     */
    custody_bailment(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME.prefersReducedMotion();

      // Payload parameters
      const title = payload.title || "Custody";
      const bailor = payload.bailor || payload.owner || "Bailor";
      const bailee = payload.bailee || payload.custodian || "Bailee";
      const goodsItem = payload.goods_item || payload.item || "Goods";
      const purpose = payload.purpose || payload.terms || "Custody Terms";
      const custodyStatus = payload.custody_status || payload.status || "Custody";
      const itemType = (payload.item_type || "goods").toLowerCase();

      // Card geometry
      const cardW = Math.min(680, bounds.w * 0.88);
      const cardH = Math.min(340, bounds.h * 0.86);
      const cardX = bounds.x + (bounds.w - cardW) / 2;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      ctx.save();

      // 1. Background Card
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? window.THEME.colors.accent.indigo.border : themeColors.borderStrong,
        radius: window.THEME.radii.lg
      });

      // 2. Header
      const headerH = 46;
      ctx.fillStyle = themeColors.bgMuted;
      ctx.beginPath();
      ctx.moveTo(cardX + 12, cardY);
      ctx.lineTo(cardX + cardW - 12, cardY);
      ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + 12);
      ctx.lineTo(cardX + cardW, cardY + headerH);
      ctx.lineTo(cardX, cardY + headerH);
      ctx.lineTo(cardX, cardY + 12);
      ctx.quadraticCurveTo(cardX, cardY, cardX + 12, cardY);
      ctx.closePath();
      ctx.fill();

      // Header icon based on goods
      let goodsIcon = "lock";
      if (itemType.includes("jewel") || itemType.includes("gold") || itemType.includes("diamond")) {
        goodsIcon = "jewel";
      } else if (itemType.includes("car") || itemType.includes("vehicle")) {
        goodsIcon = "car";
      } else if (itemType.includes("repair") || itemType.includes("tool")) {
        goodsIcon = "wrench";
      }

      window.ICONS.draw(ctx, goodsIcon, cardX + 26, cardY + headerH / 2, 20, window.THEME.colors.accent.indigo.main, 1.75);

      // Header Title with truncation
      ctx.font = window.THEME.typography.monoBadge;
      ctx.fillStyle = window.THEME.colors.accent.indigo.main;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      const maxTitleW = Math.max(120, (cardW - 100) * 0.45);
      let dispTitle = title.toUpperCase();
      if (ctx.measureText(dispTitle).width > maxTitleW) {
        while (dispTitle.length > 3 && ctx.measureText(dispTitle + "…").width > maxTitleW) {
          dispTitle = dispTitle.slice(0, -1);
        }
        dispTitle += "…";
      }
      ctx.fillText(dispTitle, cardX + 44, cardY + headerH / 2);

      // Purpose tag on top-right with truncation
      ctx.font = window.THEME.typography.caption;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.textAlign = "right";
      const maxPurposeW = Math.max(120, (cardW - 100) * 0.50);
      let dispPurpose = purpose;
      if (ctx.measureText(dispPurpose).width > maxPurposeW) {
        while (dispPurpose.length > 3 && ctx.measureText(dispPurpose + "…").width > maxPurposeW) {
          dispPurpose = dispPurpose.slice(0, -1);
        }
        dispPurpose += "…";
      }
      ctx.fillText(dispPurpose, cardX + cardW - 24, cardY + headerH / 2);

      // 3. Bilateral Party Containers: Bailor (Left), Bailee (Right)
      // Responsive party width guarantees at least 100px corridor between parties
      const partyW = Math.min(210, Math.max(130, Math.floor((cardW - 140) / 2)));
      const partyH = 115;
      const partyY = cardY + headerH + 28;

      const bailorX = cardX + 24;
      const baileeX = cardX + cardW - partyW - 24;
      const maxPartyTextW = partyW - 32;

      // Bailor Box
      window.SHARED_DRAW.card(ctx, bailorX, partyY, partyW, partyH, {
        fill: themeColors.bgMuted,
        stroke: themeColors.borderStrong,
        radius: 8
      });
      window.ICONS.draw(ctx, "user", bailorX + 24, partyY + 28, 22, themeColors.textSecondary, 1.5);
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.textAlign = "left";
      ctx.fillText("BAILOR (OWNER)", bailorX + 42, partyY + 28);
      ctx.font = window.THEME.typography.bodyBold;
      ctx.fillStyle = themeColors.textPrimary;
      let dispBailor = bailor;
      if (ctx.measureText(dispBailor).width > maxPartyTextW) {
        while (dispBailor.length > 3 && ctx.measureText(dispBailor + "…").width > maxPartyTextW) {
          dispBailor = dispBailor.slice(0, -1);
        }
        dispBailor += "…";
      }
      ctx.fillText(dispBailor, bailorX + 16, partyY + 62);

      // Bailee Box
      window.SHARED_DRAW.card(ctx, baileeX, partyY, partyW, partyH, {
        fill: themeColors.bgMuted,
        stroke: isSettle ? window.THEME.colors.accent.indigo.border : themeColors.borderStrong,
        radius: 8
      });
      window.ICONS.draw(ctx, "building", baileeX + 24, partyY + 28, 22, themeColors.textSecondary, 1.5);
      ctx.font = window.THEME.typography.captionBold;
      ctx.fillStyle = themeColors.textSecondary;
      ctx.textAlign = "left";
      ctx.fillText("BAILEE (CUSTODIAN)", baileeX + 42, partyY + 28);
      ctx.font = window.THEME.typography.bodyBold;
      ctx.fillStyle = themeColors.textPrimary;
      let dispBailee = bailee;
      if (ctx.measureText(dispBailee).width > maxPartyTextW) {
        while (dispBailee.length > 3 && ctx.measureText(dispBailee + "…").width > maxPartyTextW) {
          dispBailee = dispBailee.slice(0, -1);
        }
        dispBailee += "…";
      }
      ctx.fillText(dispBailee, baileeX + 16, partyY + 62);

      // 4. Custodial Transfer Beam (Middle)
      const beamStartX = bailorX + partyW;
      const beamEndX = baileeX;
      const beamY = partyY + partyH / 2;
      const corridorW = beamEndX - beamStartX;
      const corridorMidX = beamStartX + corridorW / 2;

      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(beamStartX, beamY);
      ctx.lineTo(beamEndX, beamY);
      ctx.stroke();
      ctx.setLineDash([]);

      // Goods Item Label permanently centered above the corridor (never collides with Bailee/Bailor box)
      ctx.font = window.THEME.typography.captionBold;
      let dispGoods = goodsItem;
      const maxGoodsW = Math.max(60, corridorW - 16);
      if (ctx.measureText(dispGoods).width > maxGoodsW) {
        while (dispGoods.length > 3 && ctx.measureText(dispGoods + "…").width > maxGoodsW) {
          dispGoods = dispGoods.slice(0, -1);
        }
        dispGoods += "…";
      }
      const goodsMetric = ctx.measureText(dispGoods);
      const pillW = goodsMetric.width + 12;
      ctx.fillStyle = themeColors.bgCard;
      ctx.beginPath();
      ctx.roundRect(corridorMidX - pillW / 2, beamY - 36, pillW, 18, 4);
      ctx.fill();
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(dispGoods, corridorMidX, beamY - 27);

      // Moving Goods Token (travels along beam cleanly underneath the label)
      const tokenP = isSettle ? 1.0 : window.TWEEN.ease.easeInOutQuart(effectiveP);
      const minTokenX = beamStartX + 20;
      const maxTokenX = beamEndX - 20;
      const tokenX = minTokenX + (maxTokenX - minTokenX) * tokenP;
      const tokenY = beamY;

      // Draw Goods Token Circle
      ctx.fillStyle = window.THEME.colors.accent.indigo.main;
      ctx.beginPath();
      ctx.arc(tokenX, tokenY, 18, 0, Math.PI * 2);
      ctx.fill();

      // Icon inside token
      window.ICONS.draw(ctx, goodsIcon, tokenX, tokenY, 16, "#FFFFFF", 1.5);

      // 5. Settled Custody Status Pill at Bottom
      const bottomPillY = cardY + cardH - 42;
      window.SHARED_DRAW.pill(ctx, custodyStatus, cardX + 24, bottomPillY, {
        fill: window.THEME.colors.accent.indigo.light,
        textFill: window.THEME.colors.accent.indigo.main,
        stroke: window.THEME.colors.accent.indigo.border,
        icon: "lock",
        maxW: cardW - 48
      });

      ctx.restore();
    }
  };

  // Register all 3 situational engines into window.ACTION_ENGINES
  Object.assign(window.ACTION_ENGINES, SITUATIONAL_ENGINES);
  window.SITUATIONAL_ENGINES = SITUATIONAL_ENGINES;
})();
