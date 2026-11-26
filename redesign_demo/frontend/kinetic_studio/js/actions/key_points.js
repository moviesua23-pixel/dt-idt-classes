// -*- coding: utf-8 -*-
// static/js/actions/key_points.js
// Statutory Kinetic Studio - Key Points Generic Fallback Engine
// Adapts dynamically to 1 to 6 legal points, rights, definitions, or exceptions.
// Serves as the exclusive neutral fallback when an action_type is unknown or invalid.

(function() {
  const KEY_POINTS = {
    key_points(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME && window.THEME.prefersReducedMotion();

      const title = payload.title || "Statutory Framework & Principles";
      let rawPoints = payload.points;
      if (!Array.isArray(rawPoints) || rawPoints.length === 0) {
        if (payload.detail || payload.description) {
          rawPoints = [{ label: payload.title || "Statutory Principle", detail: payload.detail || payload.description, value: payload.value }];
        } else {
          rawPoints = [{ label: "Statutory Principles", detail: "Statutory provisions and rights applicable to the factual situation." }];
        }
      }

      const points = rawPoints.slice(0, 6).map((pt, idx) => ({
        idx: idx + 1,
        label: String(pt.label || `Point ${idx + 1}`),
        detail: String(pt.detail || pt.description || pt.text || ""),
        value: pt.value ? String(pt.value) : (pt.amount ? window.SHARED_DRAW.formatIndianCurrency(pt.amount) : "")
      }));

      const n = Math.max(1, points.length);

      // Card Dimensions
      const cardW = Math.min(1000, bounds.w * 0.98);
      const cardH = Math.min(450, bounds.h * 0.96);
      const cardX = bounds.x + (bounds.w - cardW) / 2;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      // Layout chosen from N: 1-3 stacked cards; 4-6 two columns
      const isTwoColumn = n >= 4;
      const midPoint = isTwoColumn ? Math.ceil(n / 2) : n;

      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_key_points", { x: cardX, y: cardY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Container Card
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? themeColors.borderStrong : themeColors.border,
        radius: window.THEME.radii.lg
      });

      // Header Ribbon (42px)
      ctx.fillStyle = themeColors.bgSubtle;
      ctx.beginPath();
      ctx.roundRect(cardX, cardY, cardW, 42, [window.THEME.radii.lg, window.THEME.radii.lg, 0, 0]);
      ctx.fill();
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1;
      ctx.stroke();

      window.ICONS.draw(ctx, "fileText", cardX + 22, cardY + 21, 18, window.THEME.colors.accent.indigo.main);

      ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(title.toUpperCase(), cardX + 44, cardY + 21);

      // Total count badge on right
      window.SHARED_DRAW.pill(ctx, `${n} PRINCIPLES`, cardX + cardW - 120, cardY + 10, {
        fill: themeColors.bgCard,
        textFill: themeColors.textSecondary,
        stroke: themeColors.border
      });

      // 2. Render Points
      const listStartY = cardY + 54;
      const availH = cardH - 68;
      const rowsPerCol = isTwoColumn ? midPoint : n;
      const rowH = Math.max(50, Math.floor(availH / rowsPerCol));

      points.forEach((pt, idx) => {
        const isCol2 = isTwoColumn && idx >= midPoint;
        const colIdx = isCol2 ? 1 : 0;
        const rowInCol = isCol2 ? (idx - midPoint) : idx;

        const colW = isTwoColumn ? (cardW - 48) / 2 : (cardW - 32);
        const colX = isTwoColumn ? (cardX + 16 + colIdx * (colW + 16)) : (cardX + 16);
        const ry = listStartY + rowInCol * rowH;

        const subStart = idx / n;
        const subEnd = (idx + 1) / n;
        const itemP = isSettle ? 1.0 : (isReduced ? 1.0 : window.TWEEN.getSubPhase(effectiveP, subStart, subEnd));
        const itemAlpha = isSettle ? 1.0 : (isReduced ? 1.0 : (0.25 + 0.75 * itemP));

        ctx.save();
        ctx.globalAlpha = itemAlpha;

        // Card row background
        const isDark = window.THEME && window.THEME.mode === "dark";
        const rowBg = isDark ? "rgba(30, 41, 59, 0.35)" : themeColors.bgCard;

        ctx.fillStyle = rowBg;
        ctx.strokeStyle = themeColors.border;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(colX, ry + 2, colW, rowH - 6, window.THEME.radii.sm);
        ctx.fill();
        ctx.stroke();

        // Left numeric accent bullet
        ctx.fillStyle = window.THEME.colors.accent.indigo.light;
        ctx.beginPath();
        ctx.arc(colX + 20, ry + rowH / 2 - 1, 11, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = "700 12px 'JetBrains Mono', monospace";
        ctx.fillStyle = window.THEME.colors.accent.indigo.main;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(pt.idx), colX + 20, ry + rowH / 2 - 1);

        // Optional Value Pill on Right
        const hasVal = !!pt.value;
        const valBadgeW = hasVal ? (ctx.measureText(pt.value).width + 28) : 0;
        if (hasVal) {
          window.SHARED_DRAW.pill(ctx, pt.value, colX + colW - valBadgeW - 12, ry + (rowH - 24) / 2 - 1, {
            fill: themeColors.bgSubtle,
            textFill: themeColors.textPrimary,
            stroke: themeColors.border
          });
        }

        // Text Region
        const textStartX = colX + 40;
        const textMaxW = colW - (textStartX - colX) - (hasVal ? valBadgeW + 20 : 16);

        ctx.textAlign = "left";
        ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = themeColors.textPrimary;

        let labelText = pt.label;
        if (ctx.measureText(labelText).width > textMaxW) {
          while (labelText.length > 3 && ctx.measureText(labelText + "…").width > textMaxW) {
            labelText = labelText.slice(0, -1);
          }
          labelText += "…";
        }

        if (pt.detail && rowH >= 46) {
          ctx.textBaseline = "middle";
          ctx.fillText(labelText, textStartX, ry + rowH / 2 - 9);

          ctx.font = "400 13px 'Plus Jakarta Sans', sans-serif";
          ctx.fillStyle = themeColors.textSecondary;
          let detailText = pt.detail;
          if (ctx.measureText(detailText).width > textMaxW) {
            while (detailText.length > 3 && ctx.measureText(detailText + "…").width > textMaxW) {
              detailText = detailText.slice(0, -1);
            }
            detailText += "…";
          }
          ctx.fillText(detailText, textStartX, ry + rowH / 2 + 9);
        } else {
          ctx.textBaseline = "middle";
          ctx.fillText(labelText, textStartX, ry + rowH / 2 - 1);
        }

        ctx.restore();
      });

      ctx.restore();
    }
  };

  window.ACTION_ENGINES = window.ACTION_ENGINES || {};
  window.ACTION_ENGINES.key_points = KEY_POINTS.key_points;
})();
