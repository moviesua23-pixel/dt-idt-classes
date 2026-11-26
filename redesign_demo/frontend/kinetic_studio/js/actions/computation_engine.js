// -*- coding: utf-8 -*-
// static/js/actions/computation_engine.js
// Statutory Kinetic Studio - Dynamic Content-Driven Statutory Computation Engine
// Supports 2 to 8 calculation items with code-authoritative arithmetic, Indian number grouping (en-IN),
// adaptive single/two-column layout, vector operator glyphs, and backward-compatible adapters.

(function() {
  function drawOperatorGlyph(ctx, type, cx, cy, radius, themeColors) {
    ctx.save();
    let bg, fg;
    if (type === "add") {
      bg = window.THEME.colors.accent.emerald.light;
      fg = window.THEME.colors.accent.emerald.main;
    } else if (type === "deduct") {
      bg = window.THEME.colors.accent.crimson.light;
      fg = window.THEME.colors.accent.crimson.main;
    } else if (type === "subtotal" || type === "total") {
      bg = window.THEME.colors.accent.indigo.light;
      fg = window.THEME.colors.accent.indigo.main;
    } else {
      bg = themeColors.bgSubtle;
      fg = themeColors.textMuted;
    }

    if (window.THEME && window.THEME.mode === "dark") {
      if (type === "add") bg = "rgba(5, 150, 105, 0.24)";
      else if (type === "deduct") bg = "rgba(220, 38, 38, 0.24)";
      else if (type === "subtotal" || type === "total") bg = "rgba(79, 70, 229, 0.24)";
    }

    // Badge circle
    ctx.fillStyle = bg;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = fg;
    ctx.fillStyle = fg;
    ctx.lineWidth = 1.75;
    ctx.lineCap = "round";

    const s = radius * 0.55;
    if (type === "add") {
      // Horizontal and vertical line
      ctx.beginPath();
      ctx.moveTo(cx - s, cy);
      ctx.lineTo(cx + s, cy);
      ctx.moveTo(cx, cy - s);
      ctx.lineTo(cx, cy + s);
      ctx.stroke();
    } else if (type === "deduct") {
      // Single horizontal line
      ctx.beginPath();
      ctx.moveTo(cx - s, cy);
      ctx.lineTo(cx + s, cy);
      ctx.stroke();
    } else if (type === "subtotal" || type === "total") {
      // Two parallel horizontal lines (=)
      ctx.beginPath();
      ctx.moveTo(cx - s, cy - s * 0.4);
      ctx.lineTo(cx + s, cy - s * 0.4);
      ctx.moveTo(cx - s, cy + s * 0.4);
      ctx.lineTo(cx + s, cy + s * 0.4);
      ctx.stroke();
    } else {
      // Info "i" icon
      ctx.beginPath();
      ctx.arc(cx, cy - s * 0.55, 1.25, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(cx, cy - s * 0.1);
      ctx.lineTo(cx, cy + s * 0.6);
      ctx.stroke();
    }
    ctx.restore();
  }

  function parseAmount(val) {
    if (val === null || val === undefined) return null;
    if (typeof val === "number") return isNaN(val) ? null : val;
    if (typeof val === "string") {
      const cleaned = val.replace(/[₹$€£, ]/g, "").trim();
      if (!cleaned) return null;
      const num = Number(cleaned);
      return isNaN(num) ? null : num;
    }
    return null;
  }

  function computeLedgerItems(items, modelResultAmount) {
    let runningBalance = 0;
    let hasAnyAmount = false;
    let allInfo = true;

    const computed = (items || []).map((it, idx) => {
      const type = String(it.type || "add").toLowerCase();
      if (type !== "info") allInfo = false;

      const numVal = parseAmount(it.amount);

      if (numVal !== null) {
        hasAnyAmount = true;
        if (type === "add") {
          runningBalance += numVal;
        } else if (type === "deduct") {
          runningBalance -= numVal;
        } else if (type === "subtotal" || type === "total") {
          // If the subtotal row itself provides an amount that matches runningBalance, keep it;
          // Otherwise, code-authoritative running balance is used.
        }
      }

      return {
        idx: idx + 1,
        label: String(it.label || `Item ${idx + 1}`),
        num: numVal,
        type: type,
        note: it.note ? String(it.note) : (it.source ? String(it.source) : ""),
        balanceAtStep: runningBalance
      };
    });

    if (computed.length === 0) {
      computed.push({
        idx: 1,
        label: "Statutory Balance",
        num: null,
        type: "info",
        note: "Statutory",
        balanceAtStep: 0
      });
      allInfo = true;
    }

    // Check discrepancy with modelResultAmount
    const modelNum = parseAmount(modelResultAmount);
    if (modelNum !== null) {
      if (hasAnyAmount && modelNum !== runningBalance) {
        console.warn(`[STATUTORY_COMPUTATION] Model result_amount (${modelNum}) disagreed with code-computed total (${runningBalance}). Using computed total.`);
      }
    }

    return {
      rows: computed,
      totalAmount: runningBalance,
      hasAmounts: hasAnyAmount,
      isAllInfo: allInfo
    };
  }

  const COMPUTATION_ENGINE = {
    statutory_computation(ctx, payload = {}, bounds, phaseState, themeColors, sceneGraph, lineIdx = 0) {
      const p = phaseState.progress;
      const isSettle = p >= 0.65;
      const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.15, 0.65, 0, 1);
      const isReduced = window.THEME && window.THEME.prefersReducedMotion();

      const title = payload.title || "Statutory Computation Ledger";
      const currency = payload.currency || "INR";
      const currSymbol = currency === "INR" ? "₹" : "$";
      const rawItems = Array.isArray(payload.items) ? payload.items : [];
      const ledger = computeLedgerItems(rawItems, payload.result_amount);
      const rows = ledger.rows;
      const n = Math.max(1, rows.length);

      // Sizing & Outer Card Bounds (snapped to bounds)
      const cardW = Math.min(1000, bounds.w * 0.98);
      const cardH = Math.min(450, bounds.h * 0.96);
      const cardX = bounds.x + (bounds.w - cardW) / 2;
      const cardY = bounds.y + (bounds.h - cardH) / 2;

      // Layout strategy: If N >= 6, use 2-column ledger to maintain >= 12px logical text
      const isTwoColumn = n >= 6;
      const midPoint = isTwoColumn ? Math.ceil(n / 2) : n;

      if (sceneGraph) {
        sceneGraph.setLineIndex(lineIdx);
        sceneGraph.resolveActor("actor_statutory_computation", { x: cardX, y: cardY }, phaseState.enterT);
      }

      ctx.save();

      // 1. Ledger Card Container
      window.SHARED_DRAW.card(ctx, cardX, cardY, cardW, cardH, {
        fill: themeColors.bgCard,
        stroke: isSettle ? themeColors.borderStrong : themeColors.border,
        radius: window.THEME.radii.lg
      });

      // Header Banner (42px)
      ctx.fillStyle = themeColors.bgSubtle;
      ctx.beginPath();
      ctx.roundRect(cardX, cardY, cardW, 42, [window.THEME.radii.lg, window.THEME.radii.lg, 0, 0]);
      ctx.fill();
      ctx.strokeStyle = themeColors.border;
      ctx.lineWidth = 1;
      ctx.stroke();

      window.ICONS.draw(ctx, "calculator", cardX + 22, cardY + 21, 18, window.THEME.colors.accent.indigo.main);

      ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
      ctx.fillStyle = themeColors.textPrimary;
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(title.toUpperCase(), cardX + 44, cardY + 21);

      // Currency indicator on right
      window.SHARED_DRAW.pill(ctx, currency, cardX + cardW - 74, cardY + 10, {
        fill: themeColors.bgCard,
        textFill: themeColors.textSecondary,
        stroke: themeColors.border
      });

      // 2. Fixed Result Box (Bottom 52px)
      const resultBoxH = 50;
      const resultBoxY = cardY + cardH - resultBoxH - 12;
      const resultBoxW = cardW - 32;
      const resultBoxX = cardX + 16;

      const resultLabel = payload.result_label || "Net Statutory Balance";
      const resultP = isSettle ? 1.0 : window.TWEEN.remap(effectiveP, 0.70, 1.0, 0, 1);
      const showResult = isSettle || resultP > 0;

      // Available height for items between header and result box
      const listStartY = cardY + 48;
      const availH = resultBoxY - listStartY - 8;

      // Compute row heights
      const rowsPerCol = isTwoColumn ? midPoint : n;
      const rowH = Math.max(34, Math.floor(availH / rowsPerCol));

      // 3. Render Calculation Rows
      // Two-column reading order: Top-to-bottom in Col 1, then top-to-bottom in Col 2
      rows.forEach((row, idx) => {
        const isCol2 = isTwoColumn && idx >= midPoint;
        const colIdx = isCol2 ? 1 : 0;
        const rowInCol = isCol2 ? (idx - midPoint) : idx;

        const colW = isTwoColumn ? (cardW - 48) / 2 : (cardW - 32);
        const colX = isTwoColumn ? (cardX + 16 + colIdx * (colW + 16)) : (cardX + 16);
        const ry = listStartY + rowInCol * rowH;

        // Progressive reveal during PERFORM (0.15 to 0.65)
        const subStart = idx / n;
        const subEnd = (idx + 1) / n;
        const itemP = isSettle ? 1.0 : (isReduced ? 1.0 : window.TWEEN.getSubPhase(effectiveP, subStart, subEnd));
        const rowAlpha = isSettle ? 1.0 : (isReduced ? 1.0 : (0.25 + 0.75 * itemP));

        ctx.save();
        ctx.globalAlpha = rowAlpha;

        // Row background strip (subtle hover style)
        const isHighlight = isSettle && (row.type === "subtotal" || row.type === "total");
        if (isHighlight) {
          ctx.fillStyle = (window.THEME && window.THEME.mode === "dark") ? "rgba(99, 102, 241, 0.12)" : "rgba(99, 102, 241, 0.06)";
          ctx.beginPath();
          ctx.roundRect(colX, ry + 2, colW, rowH - 4, window.THEME.radii.sm);
          ctx.fill();
        }

        // Left Operator / Line Badge
        const glyphRadius = Math.min(10, Math.floor(rowH * 0.28));
        const glyphX = colX + 14 + glyphRadius;
        const glyphY = ry + rowH / 2;
        drawOperatorGlyph(ctx, row.type, glyphX, glyphY, glyphRadius, themeColors);

        // Line number
        ctx.font = "700 12px 'JetBrains Mono', monospace";
        ctx.fillStyle = themeColors.textMuted;
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(String(row.idx), colX + 4, glyphY);

        // Label (wrapped to max 2 lines with ellipsis, min 13px logical text)
        const textStartX = glyphX + glyphRadius + 12;
        const textMaxW = colW - (textStartX - colX) - (isTwoColumn ? 175 : 210);
        ctx.font = "600 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = isHighlight ? window.THEME.colors.accent.indigo.main : themeColors.textPrimary;
        ctx.textAlign = "left";

        // Word wrapping
        const words = row.label.split(/\s+/);
        let l1 = "", l2 = "";
        for (const w of words) {
          const test1 = l1 ? `${l1} ${w}` : w;
          if (ctx.measureText(test1).width <= textMaxW && !l2) {
            l1 = test1;
          } else {
            const test2 = l2 ? `${l2} ${w}` : w;
            if (ctx.measureText(test2).width <= textMaxW) {
              l2 = test2;
            } else {
              while (l2.length > 3 && ctx.measureText(l2 + "…").width > textMaxW) {
                l2 = l2.slice(0, -1);
              }
              l2 += "…";
              break;
            }
          }
        }

        if (l2 && rowH >= 40) {
          ctx.textBaseline = "middle";
          ctx.fillText(l1, textStartX, glyphY - 7);
          ctx.font = "400 12px 'Plus Jakarta Sans', sans-serif";
          ctx.fillStyle = themeColors.textSecondary;
          ctx.fillText(l2, textStartX, glyphY + 8);
        } else {
          ctx.textBaseline = "middle";
          ctx.fillText(l1 + (l2 ? "…" : ""), textStartX, glyphY);
        }

        // Amount Column (Right aligned, en-IN format)
        ctx.textAlign = "right";
        ctx.textBaseline = "middle";
        const amtX = colX + colW - 14;

        if (row.num !== null) {
          const signPrefix = (row.num < 0) ? "− " : "";
          const absNum = Math.abs(row.num);
          const formattedAmt = `${signPrefix}${currSymbol}${absNum.toLocaleString("en-IN")}`;

          ctx.font = "700 14px 'JetBrains Mono', monospace";
          if (row.type === "deduct") {
            ctx.fillStyle = window.THEME.colors.accent.crimson.main;
          } else if (row.type === "add") {
            ctx.fillStyle = window.THEME.colors.accent.emerald.main;
          } else {
            ctx.fillStyle = themeColors.textPrimary;
          }
          ctx.fillText(formattedAmt, amtX, glyphY);
        } else {
          ctx.font = "500 13px 'Plus Jakarta Sans', sans-serif";
          ctx.fillStyle = themeColors.textMuted;
          ctx.fillText("Amount not specified", amtX, glyphY);
        }

        ctx.restore();
      });

      // 4. Result Box at Bottom
      const resAlpha = isSettle ? 1.0 : (isReduced ? 1.0 : (0.25 + 0.75 * resultP));
      ctx.save();
      ctx.globalAlpha = resAlpha;

        const isDark = window.THEME && window.THEME.mode === "dark";
        const resBoxFill = isDark ? "rgba(15, 23, 42, 0.65)" : themeColors.bgSubtle;
        const resBorder = ledger.hasAmounts ? window.THEME.colors.accent.indigo.border : themeColors.border;

        ctx.fillStyle = resBoxFill;
        ctx.strokeStyle = resBorder;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(resultBoxX, resultBoxY, resultBoxW, resultBoxH, window.THEME.radii.md);
        ctx.fill();
        ctx.stroke();

        // Label on Left
        ctx.font = "700 14px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = themeColors.textPrimary;
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(resultLabel.toUpperCase(), resultBoxX + 20, resultBoxY + resultBoxH / 2);

        // Evaluated Final Total on Right
        ctx.textAlign = "right";
        ctx.textBaseline = "middle";
        const totalX = resultBoxX + resultBoxW - 20;

        if (ledger.hasAmounts && !ledger.isAllInfo) {
          const finalVal = isSettle ? ledger.totalAmount : Math.round(ledger.totalAmount * window.TWEEN.ease.easeOutCubic(effectiveP));
          const finalSign = finalVal < 0 ? "− " : "";
          const absTotal = Math.abs(finalVal);
          const formattedTotal = `${finalSign}${currSymbol}${absTotal.toLocaleString("en-IN")}`;

          ctx.font = "800 20px 'JetBrains Mono', monospace";
          ctx.fillStyle = finalVal < 0 ? window.THEME.colors.accent.crimson.main : window.THEME.colors.accent.emerald.main;
          ctx.fillText(formattedTotal, totalX, resultBoxY + resultBoxH / 2);
        } else {
          ctx.font = "500 13px 'Plus Jakarta Sans', sans-serif";
          ctx.fillStyle = themeColors.textMuted;
          ctx.fillText("Amount not specified", totalX, resultBoxY + resultBoxH / 2);
        }

        ctx.restore();

      ctx.restore();
    }
  };

  // Backward-compatible adapters mapping old engines to statutory_computation
  function adaptPenaltyFine(payload) {
    const items = [];
    if (payload.base_demand) {
      items.push({ label: payload.row1_label || "Base Demand", amount: payload.base_demand, type: "add" });
    }
    if (payload.penalty_amount) {
      items.push({ label: payload.row2_label || "Statutory Penalty", amount: payload.penalty_amount, type: "add" });
    }
    if (payload.interest_amount) {
      items.push({ label: payload.row3_label || "Statutory Interest", amount: payload.interest_amount, type: "add" });
    }
    return {
      title: payload.penalty_title || payload.title || "Statutory Demand Computation",
      items: items.length > 0 ? items : [{ label: "Demand Assessment", amount: payload.total_amount || payload.numeric_value, type: "add" }],
      result_label: payload.total_label || "Total Statutory Demand",
      result_amount: parseAmount(payload.total_amount || payload.numeric_value)
    };
  }

  function adaptWaterfallFlow(payload) {
    const items = [];
    if (payload.realized_corpus) {
      items.push({ label: payload.corpus_label || "Statutory Corpus", amount: payload.realized_corpus, type: "add" });
    }
    const rawTiers = Array.isArray(payload.tiers) ? payload.tiers : [];
    rawTiers.forEach((t, idx) => {
      items.push({
        label: t.label || `Step ${idx + 1}`,
        amount: t.amount,
        type: t.settled !== false ? "deduct" : "info",
        note: t.settled !== false ? "Settled" : "Exhausted"
      });
    });
    if (items.length === 0) {
      items.push({
        label: payload.waterfall_title || payload.title || "Statutory Balance",
        amount: null,
        type: "info",
        note: "Statutory"
      });
    }
    return {
      title: payload.waterfall_title || payload.title || "Statutory Ledger",
      items: items,
      result_label: payload.result_label || "Statutory Balance",
      result_amount: 0
    };
  }

  // Register on window.ACTION_ENGINES
  window.ACTION_ENGINES = window.ACTION_ENGINES || {};
  window.ACTION_ENGINES.statutory_computation = COMPUTATION_ENGINE.statutory_computation;

  // Aliases for legacy payloads
  window.ACTION_ENGINES.penalty_fine = function(ctx, payload, bounds, phaseState, themeColors, sceneGraph, lineIdx) {
    const adapted = adaptPenaltyFine(payload);
    return COMPUTATION_ENGINE.statutory_computation(ctx, adapted, bounds, phaseState, themeColors, sceneGraph, lineIdx);
  };

  window.ACTION_ENGINES.waterfall_flow = function(ctx, payload, bounds, phaseState, themeColors, sceneGraph, lineIdx) {
    const adapted = adaptWaterfallFlow(payload);
    return COMPUTATION_ENGINE.statutory_computation(ctx, adapted, bounds, phaseState, themeColors, sceneGraph, lineIdx);
  };
})();
