// -*- coding: utf-8 -*-
// static/js/script_studio.js
// Statutory Kinetic Studio - Prompt-to-Animation Script Engine
// Parses natural prompt lines:
//   shape (Type) (Text) (Position) (Intro) (Motion, Start Time, End Position)
// and renders high-fidelity canvas animations with timeline and narration.

(function() {
  // Standard 9-slot logical coordinate grid on 1280x720 canvas
  const GRID_POSITIONS = {
    "left top":      { x: 230, y: 150 },
    "top left":      { x: 230, y: 150 },
    "left center":   { x: 230, y: 360 },
    "center left":   { x: 230, y: 360 },
    "left":          { x: 230, y: 360 },
    "left bottom":   { x: 230, y: 570 },
    "bottom left":   { x: 230, y: 570 },

    "center top":    { x: 640, y: 150 },
    "top center":    { x: 640, y: 150 },
    "top":           { x: 640, y: 150 },
    "center":        { x: 640, y: 360 },
    "middle":        { x: 640, y: 360 },
    "center bottom": { x: 640, y: 570 },
    "bottom center": { x: 640, y: 570 },
    "bottom":        { x: 640, y: 570 },

    "right top":     { x: 1050, y: 150 },
    "top right":     { x: 1050, y: 150 },
    "right center":  { x: 1050, y: 360 },
    "center right":  { x: 1050, y: 360 },
    "right":         { x: 1050, y: 360 },
    "right bottom":  { x: 1050, y: 570 },
    "bottom right":  { x: 1050, y: 570 }
  };

  const SORTED_GRID_KEYS = Object.keys(GRID_POSITIONS).sort((a, b) => b.length - a.length);

  const SHAPE_PALETTES = {
    // Characters & Persons
    man:       { icon: "user",        accent: "indigo", label: "MAN / ACTOR",          category: "man" },
    person:    { icon: "user",        accent: "indigo", label: "PERSON / ACTOR",        category: "man" },
    human:     { icon: "user",        accent: "indigo", label: "PERSON / ACTOR",        category: "man" },
    boy:       { icon: "user",        accent: "indigo", label: "MAN / ACTOR",          category: "man" },
    male:      { icon: "user",        accent: "indigo", label: "MAN / ACTOR",          category: "man" },
    woman:     { icon: "user",        accent: "purple", label: "WOMAN / ACTOR",        category: "woman" },
    women:     { icon: "user",        accent: "purple", label: "WOMAN / ACTOR",        category: "woman" },
    girl:      { icon: "user",        accent: "purple", label: "WOMAN / ACTOR",        category: "woman" },
    female:    { icon: "user",        accent: "purple", label: "WOMAN / ACTOR",        category: "woman" },
    lady:      { icon: "user",        accent: "purple", label: "WOMAN / ACTOR",        category: "woman" },
    bailor:    { icon: "user",        accent: "indigo", label: "BAILOR / OWNER",       category: "man" },
    bailee:    { icon: "user",        accent: "emerald",label: "BAILEE / CUSTODIAN",   category: "woman" },
    lawyer:    { icon: "user",        accent: "indigo", label: "ADVOCATE / COUNSEL",   category: "man" },
    judge:     { icon: "gavel",       accent: "amber",  label: "JUDICIAL AUTHORITY",   category: "man" },
    taxpayer:  { icon: "user",        accent: "indigo", label: "ASSESSEE / TAXPAYER",  category: "man" },
    officer:   { icon: "shield",      accent: "emerald",label: "ASSESSING OFFICER",    category: "woman" },

    // Vehicles
    car:       { icon: "truck",       accent: "sky",    label: "CAR / MOTOR VEHICLE",  category: "car" },
    automobile:{ icon: "truck",       accent: "sky",    label: "AUTOMOBILE",           category: "car" },
    auto:      { icon: "truck",       accent: "sky",    label: "VEHICLE / AUTO",       category: "car" },
    vehicle:   { icon: "truck",       accent: "sky",    label: "MOTOR VEHICLE",        category: "car" },
    truck:     { icon: "truck",       accent: "sky",    label: "HEAVY TRUCK / TRANSIT", category: "truck" },
    lorry:     { icon: "truck",       accent: "sky",    label: "CARGO LORRY",          category: "truck" },
    van:       { icon: "truck",       accent: "sky",    label: "DELIVERY VAN",         category: "car" },
    ship:      { icon: "ship",        accent: "sky",    label: "CARGO VESSEL",         category: "ship" },
    boat:      { icon: "ship",        accent: "sky",    label: "VESSEL / BOAT",        category: "ship" },

    // Clothes, Garments & Textiles
    clothes:   { icon: "package",     accent: "emerald",label: "TAILORED CLOTHES",     category: "clothes" },
    cloth:     { icon: "package",     accent: "amber",  label: "TEXTILE / FABRIC",     category: "cloth" },
    coat:      { icon: "award",       accent: "emerald",label: "TAILORED COAT / SUIT",  category: "clothes" },
    suit:      { icon: "award",       accent: "indigo", label: "BUSINESS SUIT",        category: "clothes" },
    shirt:     { icon: "package",     accent: "emerald",label: "GARMENT / SHIRT",      category: "clothes" },
    dress:     { icon: "package",     accent: "purple", label: "DRESS / APPAREL",      category: "clothes" },
    fabric:    { icon: "package",     accent: "amber",  label: "WOVEN FABRIC / BOLT",  category: "cloth" },
    textile:   { icon: "package",     accent: "amber",  label: "TEXTILE MATERIAL",     category: "cloth" },
    garment:   { icon: "package",     accent: "emerald",label: "GARMENT APPAREL",      category: "clothes" },

    // Cargo, Boxes & Goods
    box:       { icon: "package",     accent: "amber",  label: "CARGO CRATE / BOX",    category: "box" },
    package:   { icon: "package",     accent: "amber",  label: "POSTAL PACKAGE",       category: "box" },
    parcel:    { icon: "package",     accent: "amber",  label: "SEALED PARCEL",        category: "box" },
    cargo:     { icon: "package",     accent: "amber",  label: "FREIGHT CARGO",        category: "box" },
    goods:     { icon: "package",     accent: "amber",  label: "MOVABLE PROPERTY",     category: "box" },
    jewel:     { icon: "jewel",       accent: "amber",  label: "JEWEL / BULLION",      category: "jewel" },
    gold:      { icon: "jewel",       accent: "amber",  label: "GOLD / VALUABLE ASSET",category: "jewel" },

    // Buildings & Facilities
    building:  { icon: "building",    accent: "indigo", label: "PREMISES / DEPOT",     category: "building" },
    factory:   { icon: "factory",     accent: "indigo", label: "INDUSTRIAL FACTORY",   category: "factory" },
    store:     { icon: "store",       accent: "emerald",label: "COMMERCIAL STORE",     category: "store" },
    shop:      { icon: "store",       accent: "emerald",label: "REPAIR SHOP / STORE",  category: "store" },
    court:     { icon: "scale",       accent: "amber",  label: "COURT OF LAW",         category: "court" },
    courthouse:{ icon: "scale",       accent: "amber",  label: "JUDICIAL COURTHOUSE",  category: "court" },
    bank:      { icon: "bank",        accent: "emerald",label: "ESCROW BANK",          category: "bank" },

    // Legal & Financial Symbols
    money:     { icon: "currency",    accent: "emerald",label: "CONSIDERATION / SUM",  category: "money" },
    cash:      { icon: "currency",    accent: "emerald",label: "LIQUID CASH",          category: "money" },
    currency:  { icon: "currency",    accent: "emerald",label: "CURRENCY / SUM",       category: "money" },
    document:  { icon: "fileText",    accent: "amber",  label: "CONTRACT / DEED",      category: "document" },
    contract:  { icon: "fileText",    accent: "amber",  label: "CONTRACT DEED",        category: "document" },
    deed:      { icon: "fileText",    accent: "amber",  label: "STATUTORY DEED",       category: "document" },
    scale:     { icon: "scale",       accent: "indigo", label: "LEGAL BALANCE",        category: "scale" },
    scales:    { icon: "scale",       accent: "indigo", label: "LEGAL BALANCE",        category: "scale" },
    gavel:     { icon: "gavel",       accent: "amber",  label: "JUDICIAL DECREE",      category: "gavel" },
    pill:      { icon: "checkCircle", accent: "emerald",label: "STATUTORY VERDICT",    category: "pill" },
    badge:     { icon: "checkCircle", accent: "indigo", label: "STATUTORY COVENANT",   category: "pill" },
    shield:    { icon: "shield",      accent: "indigo", label: "STATUTORY IMMUNITY",   category: "shield" },
    heading:   { icon: "bookmark",    accent: "indigo", label: "HEADING / TITLE",      category: "heading" },
    title:     { icon: "bookmark",    accent: "indigo", label: "HEADING / TITLE",      category: "heading" },
    headline:  { icon: "bookmark",    accent: "indigo", label: "HEADING / TITLE",      category: "heading" }
  };

  /**
   * Resolves shape metadata with smart fuzzy classification
   */
  function resolveShapeMeta(shapeType) {
    if (!shapeType) return { icon: "package", accent: "indigo", label: "SHAPE", category: "goods", overlay: null, custom: null };

    // 1. Delegate to Universal 19-Category Shape Catalog
    if (window.SHAPE_CATALOG && window.SHAPE_CATALOG.lookup) {
      const entry = window.SHAPE_CATALOG.lookup(shapeType);
      if (entry) {
        return {
          icon: entry.icon || "package",
          accent: entry.accent || "indigo",
          label: entry.badgeLabel || entry.categoryTitle || shapeType.toUpperCase(),
          category: entry.category || "goods",
          overlay: entry.overlay || null,
          custom: entry.custom || null
        };
      }
    }

    const clean = shapeType.trim().toLowerCase();

    // 1. Direct exact match
    if (SHAPE_PALETTES[clean]) {
      return { ...SHAPE_PALETTES[clean] };
    }

    // 2. Keyword heuristic classification
    if (clean.includes("woman") || clean.includes("women") || clean.includes("girl") || clean.includes("female") || clean.includes("lady") || clean.includes("mrs") || clean.includes("ms")) {
      return { icon: "user", accent: "purple", label: "WOMAN / ACTOR", category: "woman" };
    }
    if (clean.includes("man") || clean.includes("person") || clean.includes("human") || clean.includes("male") || clean.includes("boy") || clean.includes("mr") || clean.includes("actor") || clean.includes("bailor") || clean.includes("taxpayer") || clean.includes("client")) {
      return { icon: "user", accent: "indigo", label: "MAN / ACTOR", category: "man" };
    }
    if (clean.includes("truck") || clean.includes("lorry")) {
      return { icon: "truck", accent: "sky", label: "TRUCK / TRANSIT", category: "truck" };
    }
    if (clean.includes("car") || clean.includes("auto") || clean.includes("vehicle") || clean.includes("motor") || clean.includes("van") || clean.includes("bus")) {
      return { icon: "truck", accent: "sky", label: "CAR / VEHICLE", category: "car" };
    }
    if (clean.includes("cloth") || clean.includes("fabric") || clean.includes("textile") || clean.includes("silk") || clean.includes("cotton") || clean.includes("wool") || clean.includes("linen")) {
      return { icon: "package", accent: "amber", label: "CLOTH / FABRIC", category: "cloth" };
    }
    if (clean.includes("clothes") || clean.includes("coat") || clean.includes("suit") || clean.includes("shirt") || clean.includes("dress") || clean.includes("jacket") || clean.includes("garment") || clean.includes("apparel")) {
      return { icon: "award", accent: "emerald", label: "CLOTHES / GARMENT", category: "clothes" };
    }
    if (clean.includes("factory") || clean.includes("workshop") || clean.includes("plant") || clean.includes("mill")) {
      return { icon: "factory", accent: "indigo", label: "FACTORY / WORKSHOP", category: "factory" };
    }
    if (clean.includes("court") || clean.includes("tribunal") || clean.includes("bench")) {
      return { icon: "scale", accent: "amber", label: "COURT OF LAW", category: "court" };
    }
    if (clean.includes("store") || clean.includes("shop") || clean.includes("market") || clean.includes("retail")) {
      return { icon: "store", accent: "emerald", label: "COMMERCIAL STORE", category: "store" };
    }
    if (clean.includes("bank") || clean.includes("treasury") || clean.includes("vault")) {
      return { icon: "bank", accent: "emerald", label: "FINANCIAL BANK", category: "bank" };
    }
    if (clean.includes("build") || clean.includes("office") || clean.includes("depot") || clean.includes("tower")) {
      return { icon: "building", accent: "indigo", label: "PREMISES / OFFICE", category: "building" };
    }
    if (clean.includes("box") || clean.includes("crate") || clean.includes("package") || clean.includes("parcel") || clean.includes("cargo") || clean.includes("goods") || clean.includes("shipment")) {
      return { icon: "package", accent: "amber", label: "CARGO / GOODS", category: "box" };
    }
    if (clean.includes("jewel") || clean.includes("gold") || clean.includes("bullion") || clean.includes("diamond")) {
      return { icon: "jewel", accent: "amber", label: "PRECIOUS JEWEL", category: "jewel" };
    }
    if (clean.includes("money") || clean.includes("cash") || clean.includes("rupee") || clean.includes("dollar") || clean.includes("fund") || clean.includes("price") || clean.includes("fee") || clean.includes("compensation")) {
      return { icon: "currency", accent: "emerald", label: "CONSIDERATION / SUM", category: "money" };
    }
    if (clean.includes("doc") || clean.includes("contract") || clean.includes("deed") || clean.includes("paper") || clean.includes("card") || clean.includes("agreement") || clean.includes("notice") || clean.includes("letter")) {
      return { icon: "fileText", accent: "amber", label: "CONTRACT / DEED", category: "document" };
    }
    if (clean.includes("scale") || clean.includes("justice") || clean.includes("balance")) {
      return { icon: "scale", accent: "indigo", label: "LEGAL BALANCE", category: "scale" };
    }
    if (clean.includes("gavel") || clean.includes("decree") || clean.includes("order") || clean.includes("verdict")) {
      return { icon: "gavel", accent: "amber", label: "JUDICIAL GAVEL", category: "gavel" };
    }
    if (clean.includes("pill") || clean.includes("badge") || clean.includes("tag") || clean.includes("stamp") || clean.includes("status")) {
      return { icon: "checkCircle", accent: "emerald", label: "STATUTORY VERDICT", category: "pill" };
    }
    if (clean.includes("ship") || clean.includes("boat") || clean.includes("vessel")) {
      return { icon: "ship", accent: "sky", label: "MARINE VESSEL", category: "ship" };
    }

    return {
      icon: "package",
      accent: "indigo",
      label: shapeType.toUpperCase(),
      category: "generic"
    };
  }

  /**
   * Resolves text position like "left top" or percentage "(20%, 40%)" to {x, y}
   */
  function resolvePosition(posStr, defaultPos = { x: 640, y: 340 }) {
    if (!posStr) return defaultPos;
    const clean = posStr.trim().toLowerCase();

    // Check pre-defined 9 grid positions
    if (GRID_POSITIONS[clean]) {
      return { ...GRID_POSITIONS[clean] };
    }

    // Check partial matches with sorted keys (longest first)
    for (let key of SORTED_GRID_KEYS) {
      if (clean.includes(key)) {
        return { ...GRID_POSITIONS[key] };
      }
    }

    // Check percentage coordinate e.g. "30%, 40%"
    const pctMatch = clean.match(/(\d+)\s*%\s*,\s*(\d+)\s*%/);
    if (pctMatch) {
      return {
        x: Math.round((parseInt(pctMatch[1], 10) / 100) * 1280),
        y: Math.round((parseInt(pctMatch[2], 10) / 100) * 720)
      };
    }

    return defaultPos;
  }

  /**
   * Parses the motion command string:
   * e.g. "Movement to Right, after 1 second, Right top"
   * e.g. "Movement to Left, after 2 seconds, left center"
   * e.g. "stay"
   */
  function parseMotion(motionStr, startPos) {
    if (!motionStr) return { hasMotion: false };
    const clean = motionStr.trim().toLowerCase();

    if (clean === "stay" || clean === "none" || clean === "hold" || clean === "anchor") {
      return { hasMotion: false };
    }

    // Extract start delay (seconds -> ms)
    let delayMs = 1000;
    const delayMatch = clean.match(/after\s*(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)?/);
    if (delayMatch) {
      delayMs = Math.round(parseFloat(delayMatch[1]) * 1000);
    }

    // Extract motion duration (seconds -> ms)
    let durationMs = 1500;
    const durMatch = clean.match(/(?:in|over|duration|for|takes?)\s*(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)?/);
    if (durMatch) {
      durationMs = Math.round(parseFloat(durMatch[1]) * 1000);
    }

    // Extract target position (longest position matches first)
    let targetPos = null;
    for (let key of SORTED_GRID_KEYS) {
      if (clean.includes(key)) {
        targetPos = { ...GRID_POSITIONS[key] };
        break;
      }
    }

    // If no explicit position name found, infer from direction keyword
    if (!targetPos) {
      if (clean.includes("to right") || clean.includes("towards right")) {
        targetPos = { x: Math.min(1050, startPos.x + 400), y: startPos.y };
      } else if (clean.includes("to left") || clean.includes("towards left")) {
        targetPos = { x: Math.max(230, startPos.x - 400), y: startPos.y };
      } else if (clean.includes("to bottom") || clean.includes("downwards")) {
        targetPos = { x: startPos.x, y: Math.min(500, startPos.y + 160) };
      } else if (clean.includes("to top") || clean.includes("upwards")) {
        targetPos = { x: startPos.x, y: Math.max(170, startPos.y - 160) };
      } else {
        targetPos = { ...startPos };
      }
    }

    return {
      hasMotion: true,
      rawDelayMs: delayMs,
      durationMs: durationMs,
      startMs: delayMs,
      endMs: delayMs + durationMs,
      from: { ...startPos },
      to: targetPos
    };
  }

  /**
   * Main Prompt Parser:
   * Converts raw text lines into structured presentation slides
   */
  /**
   * Balanced Parentheses Tokenizer:
   * Extracts top-level parenthesized chunks even when nested, e.g.:
   *   shape (calculation (multiple)) (+) (Full Value of Consideration) (10,00,000) (center)
   *   -> ["calculation (multiple)", "+", "Full Value of Consideration", "10,00,000", "center"]
   */
  function extractBalancedParentheses(str) {
    const tokens = [];
    let depth = 0;
    let startIdx = -1;

    for (let i = 0; i < str.length; i++) {
      const ch = str[i];
      if (ch === '(') {
        if (depth === 0) {
          startIdx = i + 1;
        }
        depth++;
      } else if (ch === ')') {
        depth--;
        if (depth === 0 && startIdx !== -1) {
          tokens.push(str.substring(startIdx, i).trim());
          startIdx = -1;
        }
      }
    }
    return tokens;
  }

  function parseAmountValue(raw) {
    if (raw === null || raw === undefined) return { num: null, raw: "", currency: "" };
    const str = String(raw).trim();
    let currency = "";
    if (str.includes("$")) currency = "$";
    else if (str.includes("€")) currency = "€";
    else if (str.includes("£")) currency = "£";
    else if (str.includes("₹") || /INR/i.test(str) || /Rs/i.test(str)) currency = "₹";

    // Clean out non-numeric characters except . and -
    const cleanNumStr = str.replace(/[₹$€£INRrs\s,]/gi, "").trim();
    const num = parseFloat(cleanNumStr);

    // If no currency specified and num is large (>= 1000) with no units, default to ₹ for financial figures
    if (!currency && num !== null && !isNaN(num) && num >= 1000 && !/\b(?:years?|months?|days?|times?|ratio|%)\b/i.test(str)) {
      currency = "₹";
    }

    return {
      num: isNaN(num) ? null : num,
      raw: str,
      currency: currency
    };
  }

  function resolveSignType(signStr) {
    const s = (signStr || "+").trim().toLowerCase();
    if (s === "+" || s === "plus" || s === "add") return { sign: "+", type: "add" };
    if (s === "−" || s === "-" || s === "minus" || s === "deduct" || s === "less") return { sign: "−", type: "deduct" };
    if (s === "=" || s === "total" || s === "subtotal" || s === "equal" || s === "net") return { sign: "=", type: "total" };
    if (s === "×" || s === "*" || s === "x" || s === "multiply") return { sign: "×", type: "multiply" };
    if (s === "÷" || s === "/" || s === "divide") return { sign: "÷", type: "divide" };
    return { sign: signStr, type: "add" };
  }

  function parseCalculationLine(line, tokens) {
    if (!tokens || tokens.length === 0) return null;

    // Extract dialogue if present
    let dialogueText = "";
    const cleanTokens = [];
    for (let i = 0; i < tokens.length; i++) {
      const tok = tokens[i].trim();
      const dMatch = tok.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
      if (dMatch) {
        dialogueText = dMatch[1].trim();
        continue;
      }
      if (/^(?:dialogue|narration|speech)$/i.test(tok.toLowerCase()) && i + 1 < tokens.length) {
        dialogueText = tokens[i + 1].trim().replace(/^["']|["']$/g, "");
        i++;
        continue;
      }
      cleanTokens.push(tok);
    }

    if (cleanTokens.length === 0) return null;

    const t0 = (cleanTokens[0] || "").toLowerCase().trim();
    const t1 = (cleanTokens[1] || "").toLowerCase().trim();

    // Check if line starts with calculation shape keyword
    const isCalcToken = t0.includes("calculation") || t0.includes("calc_multiple") || t0 === "calc";

    if (isCalcToken) {
      let offset = 1;
      if (t0 === "calculation" && t1 === "multiple") {
        offset = 2;
      }

      const rem = cleanTokens.slice(offset);
      if (rem.length === 0) {
        return { isHeaderOnly: true, pos: "center", dialogue: dialogueText };
      }
      if (rem.length === 1 && (GRID_POSITIONS[rem[0].toLowerCase()] || rem[0].includes("%"))) {
        return { isHeaderOnly: true, pos: rem[0], dialogue: dialogueText };
      }

      let pos = "center";
      let signIdx = 0;
      if (GRID_POSITIONS[rem[0].toLowerCase()] || rem[0].includes("%")) {
        pos = rem[0];
        signIdx = 1;
      }

      const sign = rem[signIdx] || "+";
      const text = rem[signIdx + 1] || "Item";
      const amt = rem[signIdx + 2] || "0";
      const trailingPos = rem[signIdx + 3];
      if (trailingPos && (GRID_POSITIONS[trailingPos.toLowerCase()] || trailingPos.includes("%"))) {
        pos = trailingPos;
      }

      return {
        isHeaderOnly: false,
        pos: pos,
        sign: sign,
        text: text,
        rawAmount: amt,
        dialogue: dialogueText
      };
    }

    // Check shorthand line starting with sign e.g. "(+) (Text) (Amount)"
    const cleanT0 = t0.replace(/\s+/g, "");
    if (cleanT0 === "+" || cleanT0 === "-" || cleanT0 === "−" || cleanT0 === "=" || cleanT0 === "plus" || cleanT0 === "minus" || cleanT0 === "total" || cleanT0 === "less" || cleanT0 === "add" || cleanT0 === "*" || cleanT0 === "/" || cleanT0 === "x") {
      if (cleanTokens.length >= 2) {
        return {
          isHeaderOnly: false,
          pos: "center",
          sign: cleanTokens[0],
          text: cleanTokens[1],
          rawAmount: cleanTokens[2] || "0",
          dialogue: dialogueText
        };
      }
    }

    return null;
  }

  /**
   * Helper to resolve checklist item status:
   * Condition item: { type: "check", isOk: true/false, label: "SATISFIED"/"NOT MET" }
   * Gate unlock item: { type: "gate", isUnlock: true/false, label: "UNLOCKED"/"NOT UNLOCKED" }
   */
  function resolveChecklistStatus(raw) {
    if (!raw) return { type: "check", isOk: true, val: "ok", label: "SATISFIED", raw: "" };
    const s = String(raw).trim().toLowerCase();

    // 1. Gate Unlock / Lock (At last of the list)
    if (s.includes("not unlock") || s.includes("not_unlock") || s.includes("no unlock") ||
        s === "lock" || s === "locked" || s.includes("ineligible") || s.includes("denied") || s.includes("gate locked")) {
      return { type: "gate", isUnlock: false, val: "locked", label: "NOT UNLOCKED", raw: raw };
    }
    if (s.includes("unlock") || s.includes("unlocked") || s === "open" || s.includes("eligible") || s.includes("granted") || s.includes("gate unlocked")) {
      return { type: "gate", isUnlock: true, val: "unlock", label: "UNLOCKED", raw: raw };
    }

    // 2. Condition Not OK / Fail
    if (s === "not" || s === "not ok" || s === "not_ok" || s === "check not" || s === "fail" ||
        s === "failed" || s === "false" || s === "no" || s === "-" || s === "✕" || s === "x" || s === "cross" || s.includes("unmet")) {
      return { type: "check", isOk: false, val: "not", label: "NOT MET", raw: raw };
    }

    // 3. Condition OK / Pass (Default)
    return { type: "check", isOk: true, val: "ok", label: "SATISFIED", raw: raw };
  }

  /**
   * Parses time delay expressions into milliseconds:
   * e.g. "1 second", "1.5 seconds", "0.5s", "after 1s", "500ms"
   */
  function parseItemDelay(str) {
    if (!str) return null;
    const s = String(str).trim().toLowerCase();

    // Match e.g. "500ms", "1000 ms"
    const msMatch = s.match(/^(?:after\s*)?(\d+)\s*ms$/);
    if (msMatch) {
      return parseInt(msMatch[1], 10);
    }

    // Match e.g. "1 second", "1.5 seconds", "1s", "after 2s", "0.5 sec"
    const secMatch = s.match(/^(?:after\s*)?(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)$/);
    if (secMatch) {
      return Math.round(parseFloat(secMatch[1]) * 1000);
    }

    return null;
  }

  /**
   * Helper to identify if a token is explicitly a checklist status keyword
   */
  function isChecklistStatusKeyword(raw) {
    if (!raw) return false;
    const s = String(raw).trim().toLowerCase();
    if (s === "ok" || s === "check ok" || s === "check_ok" || s === "pass" || s === "met" || s === "satisfied" || s === "true" || s === "yes" || s === "+" || s === "✓") return true;
    if (s === "not" || s === "not ok" || s === "not_ok" || s === "check not" || s === "fail" || s === "failed" || s === "false" || s === "no" || s === "-" || s === "✕" || s === "x" || s === "cross" || s === "unmet" || s === "not met") return true;
    if (s.includes("not unlock") || s.includes("not_unlock") || s.includes("no unlock") || s === "lock" || s === "locked" || s.includes("ineligible") || s.includes("denied") || s.includes("gate locked")) return true;
    if (s.includes("unlock") || s.includes("unlocked") || s === "open" || s.includes("eligible") || s.includes("granted") || s.includes("gate unlocked")) return true;
    return false;
  }

  /**
   * Flexibly extracts item fields from tokens:
   * Recognizes text, status, time delay, and grid position in ANY order.
   */
  function extractChecklistItemFromTokens(tokens, isExplicitShapeDecl) {
    let pos = null;
    let delayMs = null;
    let statusRaw = null;
    let dialogueText = "";
    const textCandidates = [];

    for (let idx = 0; idx < tokens.length; idx++) {
      if (isExplicitShapeDecl && idx === 0) continue; // skip shape keyword "check list" / "checklist"
      const tok = tokens[idx];
      const tClean = tok.trim();
      const tLow = tClean.toLowerCase();

      // 0. Dialogue / narration
      const dMatch = tClean.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
      if (dMatch) {
        dialogueText = dMatch[1].trim();
        continue;
      }
      if (/^(?:dialogue|narration|speech)$/i.test(tLow) && idx + 1 < tokens.length) {
        dialogueText = tokens[idx + 1].trim().replace(/^["']|["']$/g, "");
        idx++;
        continue;
      }

      // 1. Grid Position
      if (GRID_POSITIONS[tLow] || /^\s*\d+\s*%\s*,\s*\d+\s*%\s*$/.test(tLow)) {
        pos = tClean;
        continue;
      }

      // 2. Time delay (e.g. "1 second", "0.5s", "after 1s")
      const parsedDelay = parseItemDelay(tClean);
      if (parsedDelay !== null && delayMs === null) {
        delayMs = parsedDelay;
        continue;
      }

      // 3. Status keyword (e.g. "check ok", "unlock", "not ok", "not unlock")
      if (isChecklistStatusKeyword(tClean) && statusRaw === null) {
        statusRaw = tClean;
        continue;
      }

      // 4. Otherwise, text candidate
      textCandidates.push(tClean);
    }

    if (statusRaw === null && textCandidates.length >= 2) {
      statusRaw = textCandidates.pop();
    }

    const text = textCandidates.join(" ").trim();
    const status = resolveChecklistStatus(statusRaw || "ok");

    return {
      text: text,
      status: status,
      delayMs: delayMs,
      dialogue: dialogueText,
      pos: pos
    };
  }

  /**
   * Computes the cumulative timeline for checklist items and the statutory gate.
   * "each time is from the previous list item not from the beginning"
   * Next element only appears after previous item's dialogue is completed!
   */
  function computeChecklistTimeline(actor) {
    if (!actor || !actor.isChecklist) return;

    const items = actor.items || [];
    const gateItem = actor.gateItem || null;

    // Card intro completes at base offset
    const baseOffsetMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 350;
    let runningTimeMs = baseOffsetMs + (actor.startMs !== undefined ? 150 : 350);

    items.forEach((item, idx) => {
      item.startMs = runningTimeMs;
      const words = item.dialogue ? item.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const delay = (item.delayMs !== null && item.delayMs !== undefined) ? item.delayMs : (idx === 0 ? 500 : 600);
      const activeSpan = Math.max(speechMs, delay, 1200);
      item.endMs = item.startMs + activeSpan;
      runningTimeMs = item.endMs + 350; // next item enters after previous voice completes!
    });

    if (gateItem) {
      gateItem.startMs = runningTimeMs;
      const words = gateItem.dialogue ? gateItem.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const gateDelay = (gateItem.delayMs !== null && gateItem.delayMs !== undefined) ? gateItem.delayMs : 600;
      const activeSpan = Math.max(speechMs, gateDelay, 1400);
      gateItem.endMs = gateItem.startMs + activeSpan;
      runningTimeMs = gateItem.endMs + 400;
    }

    actor.totalTimelineMs = runningTimeMs;
  }

  /**
   * Computes cumulative timeline for List items:
   * Next item enters after previous item's active delay or dialogue voice completes.
   */
  function computeListTimeline(actor) {
    if (!actor || !actor.isList) return;
    const items = actor.items || [];
    if (items.length > 0 && items[0].startMs !== undefined && actor.totalTimelineMs) {
      return;
    }
    const baseOffsetMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 350;
    let runningTimeMs = baseOffsetMs + 400; // card intro

    items.forEach((item, idx) => {
      item.startMs = runningTimeMs;
      const words = item.dialogue ? item.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const delay = (item.delayMs !== null && item.delayMs !== undefined) ? item.delayMs : (idx === 0 ? 500 : 700);
      const activeSpan = Math.max(speechMs, delay, 1100);
      item.endMs = item.startMs + activeSpan;
      runningTimeMs = item.endMs + 300;
    });

    actor.totalTimelineMs = runningTimeMs;
  }

  /**
   * Computes sequential relative timeline for calculation (multiple) rows:
   * Next row and odometer roll only starts after previous row's dialogue voice completes!
   */
  function computeCalculationMultipleTimeline(actor) {
    if (!actor || !actor.isCalculation || !actor.items) return;
    const items = actor.items;
    if (items.length === 0) return;

    const baseOffsetMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 350;
    let runningTimeMs = baseOffsetMs + 400; // card header intro

    items.forEach((it, idx) => {
      it.startMs = runningTimeMs;
      const words = it.dialogue ? it.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const activeSpan = Math.max(speechMs, 1100);
      it.endMs = it.startMs + activeSpan;
      runningTimeMs = it.endMs + 350; // next row enters after previous row's dialogue finishes!
    });

    actor.totalTimelineMs = runningTimeMs;
  }

  /**
   * Detection & Extraction for Heading shape lines:
   * Supports:
   *   shape (Heading) (text) (subtitle (if any)) (Text)
   *   shape (Heading) (Title Text) (subtitle) (Subtitle Text)
   *   shape (Heading) (Title Text) (Subtitle Text)
   *   shape (Heading) (Title Text)
   *   shape (Heading) (Title Text) (center) (1 second)
   *   shape type (heading) (Title Text) (subtitle) (Subtitle Text)
   */
  function parseHeadingLine(line, tokens) {
    if (!line) return null;
    const lower = line.toLowerCase().trim();
    const hasShape = lower.startsWith("shape") || /^\s*\(?\s*(?:heading|title|headline|head)\b/i.test(lower);
    if (!hasShape) return null;

    tokens = tokens || extractBalancedParentheses(line);
    if (tokens.length === 0) return null;

    const firstTok = tokens[0].toLowerCase().trim();
    const isHeadingType = /^(?:heading|title|headline|head)$/i.test(firstTok);
    if (!isHeadingType) return null;

    let titleText = "";
    let subtitleText = "";
    let dialogueText = "";
    let pos = "center";
    let delayMs = 0;
    let subtitleDelayMs = 450;
    let slideDurationMs = null;
    let expectSubtitle = false;
    let hasIntroFade = true;
    let hasOutroFade = true;
    let introDurationMs = 600;
    let outroDurationMs = 450;

    for (let i = 1; i < tokens.length; i++) {
      const rawTok = tokens[i].trim();
      const tokLower = rawTok.toLowerCase();

      // 0. Dialogue / Narration check
      const dMatch = rawTok.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
      if (dMatch) {
        dialogueText = dMatch[1].trim();
        continue;
      }
      if (/^(?:dialogue|narration|speech)$/i.test(tokLower) && i + 1 < tokens.length) {
        dialogueText = tokens[i + 1].trim().replace(/^["']|["']$/g, "");
        i++;
        continue;
      }

      // 1. Position check
      let isPos = false;
      for (let k of SORTED_GRID_KEYS) {
        if (tokLower === k) {
          pos = k;
          isPos = true;
          break;
        }
      }
      if (isPos) continue;

      // 2. Time / Delay check
      const delay = parseItemDelay(rawTok);
      if (delay !== null) {
        if (expectSubtitle || subtitleText) {
          subtitleDelayMs = delay;
        } else if (titleText) {
          slideDurationMs = delay;
        } else {
          delayMs = delay;
        }
        continue;
      }

      // 3. Subtitle marker keyword e.g. "subtitle", "subtitle (if any)", "sub_title"
      if (/^sub[-_ ]?title(?:\s*\(.*?\))?$/i.test(tokLower)) {
        expectSubtitle = true;
        continue;
      }

      // 4. Subtitle prefixed e.g. "subtitle: Section 45"
      const subMatch = rawTok.match(/^sub[-_ ]?title\s*:\s*(.+)$/i);
      if (subMatch) {
        subtitleText = subMatch[1].trim();
        continue;
      }

      // 5. Animation / Fade keywords
      if (/^no\s+fade$/i.test(tokLower)) {
        hasIntroFade = false;
        hasOutroFade = false;
        continue;
      }
      if (/^no\s+intro\s+fade$/i.test(tokLower)) {
        hasIntroFade = false;
        continue;
      }
      if (/^no\s+outro\s+fade$/i.test(tokLower)) {
        hasOutroFade = false;
        continue;
      }
      if (/^(?:intro\s+fade|outro\s+fade|fade\s*in|fade\s*out|fade|dissolve|into and outro aniatatoin fade|intro and outro animation fade|fade in and out)$/i.test(tokLower)) {
        hasIntroFade = true;
        hasOutroFade = true;
        continue;
      }

      // 6. Normal text token
      let cleanText = rawTok.replace(/^text\s*:\s*/i, "").trim();

      if (expectSubtitle) {
        subtitleText = cleanText;
        expectSubtitle = false;
      } else if (!titleText) {
        titleText = cleanText;
      } else if (!subtitleText) {
        subtitleText = cleanText;
      }
    }

    if (!titleText && tokens.length > 1) {
      titleText = tokens[1];
    }

    return {
      isHeading: true,
      titleText: titleText || "Statutory Lecture Topic",
      subtitleText: subtitleText || "",
      dialogueText: dialogueText || "",
      pos: pos,
      delayMs: delayMs,
      subtitleDelayMs: subtitleDelayMs,
      slideDurationMs: slideDurationMs || null,
      hasIntroFade: hasIntroFade,
      hasOutroFade: hasOutroFade,
      introDurationMs: introDurationMs,
      outroDurationMs: outroDurationMs
    };
  }

  /**
   * Detection & Extraction for Checklist shape lines:
   * Supports:
   *   shape (check list) (Holding Period > 24 Months) (check ok) (1 second) (center)
   *   shape (check list) (Purchase New Residential House in India) (1 second) (check ok)
   *   shape (check list) (Section 54 Statutory Exemption Gate) (1 second) (unlock)
   *   shape (check list) [ (Condition 1)(check ok)(1s) (Condition 2)(not ok)(1s) (Gate)(1s)(unlock) ] (center)
   */
  function parseChecklistLine(line, tokens, activeChecklistActor) {
    if (!line) return null;
    const lower = line.toLowerCase().trim();

    const isChecklistDecl = lower.includes("check list") ||
                            lower.includes("checklist") ||
                            lower.includes("check_list") ||
                            lower.includes("conditions_list") ||
                            lower.startsWith("shape (gate)") ||
                            lower.startsWith("shape (checklist)");

    const isExplicitShape = lower.startsWith("shape") && isChecklistDecl;

    // Check bracket syntax e.g. shape (check list) [ (Item 1)(check ok)(1s) (Item 2)(1s)(unlock) ] (center)
    const bracketMatch = line.match(/\[([\s\S]+)\]/);
    if (isChecklistDecl && bracketMatch) {
      let pos = "center";
      const outside = line.replace(bracketMatch[0], "");
      for (let k of SORTED_GRID_KEYS) {
        if (outside.toLowerCase().includes(k)) {
          pos = k;
          break;
        }
      }

      const inner = bracketMatch[1];
      const innerTokens = extractBalancedParentheses(inner);
      const items = [];
      let gateItem = null;

      // Group into item chunks
      let currentGroup = [];
      const itemGroups = [];
      innerTokens.forEach(tok => {
        const isDelay = parseItemDelay(tok) !== null;
        const isStatus = isChecklistStatusKeyword(tok);
        if (!isDelay && !isStatus && currentGroup.length > 0 && 
            (currentGroup.some(t => isChecklistStatusKeyword(t)) || currentGroup.some(t => parseItemDelay(t) !== null))) {
          itemGroups.push(currentGroup);
          currentGroup = [tok];
        } else {
          currentGroup.push(tok);
        }
      });
      if (currentGroup.length > 0) itemGroups.push(currentGroup);

      itemGroups.forEach(grp => {
        const parsed = extractChecklistItemFromTokens(grp, false);
        if (parsed.status.type === "gate") {
          gateItem = parsed;
        } else {
          items.push(parsed);
        }
      });

      return {
        isDeclaration: true,
        isCompleteInline: true,
        pos: pos,
        title: "STATUTORY COMPLIANCE CHECKLIST",
        items: items,
        gateItem: gateItem
      };
    }

    if (isExplicitShape) {
      if (!tokens || tokens.length === 0) return null;
      const parsed = extractChecklistItemFromTokens(tokens, true);

      let title = "STATUTORY COMPLIANCE CHECKLIST";
      let item = null;

      if (parsed.text) {
        item = parsed;
      }

      return {
        isDeclaration: true,
        isCompleteInline: false,
        pos: parsed.pos || "center",
        title: title,
        item: item
      };
    }

    // 2. Shorthand item lines when activeChecklistActor exists in current scene
    if (activeChecklistActor && tokens && tokens.length > 0) {
      const parsed = extractChecklistItemFromTokens(tokens, false);
      if (parsed.text || parsed.status.type === "gate") {
        return {
          isDeclaration: false,
          item: parsed
        };
      }
    }

    return null;
  }

  /**
   * Helper to extract a list item from parenthesized tokens:
   * Recognizes title, description, time delay (e.g. "1s"), dialogue, and grid position.
   */
  function extractListItemFromTokens(tokens, isExplicitShapeDecl) {
    let pos = null;
    let delayMs = null;
    let dialogueText = "";
    const textCandidates = [];

    for (let idx = 0; idx < tokens.length; idx++) {
      if (isExplicitShapeDecl && idx === 0) continue; // skip shape keyword "list"
      const tok = tokens[idx];
      const tClean = tok.trim();
      const tLow = tClean.toLowerCase();

      // Dialogue / narration
      const dMatch = tClean.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
      if (dMatch) {
        dialogueText = dMatch[1].trim();
        continue;
      }
      if (/^(?:dialogue|narration|speech)$/i.test(tLow) && idx + 1 < tokens.length) {
        dialogueText = tokens[idx + 1].trim().replace(/^["']|["']$/g, "");
        idx++;
        continue;
      }

      // Grid position
      if (GRID_POSITIONS[tLow] || /^\s*\d+\s*%\s*,\s*\d+\s*%\s*$/.test(tLow)) {
        pos = tClean;
        continue;
      }

      // Time delay (e.g. "1 second", "0.5s", "after 1s")
      const parsedDelay = parseItemDelay(tClean);
      if (parsedDelay !== null && delayMs === null) {
        delayMs = parsedDelay;
        continue;
      }

      // Skip design tags if encountered inside item tokens
      if (/^(?:design|style)\s*[:=]?\s*\d+$/i.test(tClean) || /^(?:cards|timeline|clause|pills|obsidian|stepped|process|statutory)$/i.test(tLow)) {
        continue;
      }

      textCandidates.push(tClean);
    }

    let title = "";
    let desc = "";

    if (textCandidates.length === 1) {
      const fullText = textCandidates[0];
      if (fullText.includes(":") && !fullText.startsWith("http")) {
        const parts = fullText.split(":");
        title = parts[0].trim();
        desc = parts.slice(1).join(":").trim();
      } else {
        title = fullText;
      }
    } else if (textCandidates.length >= 2) {
      title = textCandidates[0];
      desc = textCandidates.slice(1).join(" ").trim();
    }

    return {
      title: title,
      desc: desc,
      text: desc ? `${title}: ${desc}` : title,
      delayMs: delayMs,
      dialogue: dialogueText,
      pos: pos
    };
  }

  /**
   * Helper to resolve the list design variant (1 to 5):
   * 1: "cards" / elevated floating glass cards (default)
   * 2: "timeline" / stepped process flow spine
   * 3: "clause" / formal statutory clauses & digest
   * 4: "pills" / two-tone rounded capsules
   * 5: "obsidian" / dark deck with neon horizon glow
   */
  function resolveListDesign(rawStr) {
    if (!rawStr) return 1;
    const s = String(rawStr).toLowerCase();
    if (s.includes("timeline") || s.includes("process") || s.includes("flow") || s.includes("step") || s.includes("design 2") || s.includes("style 2") || s.endsWith(" 2") || s.endsWith(", 2") || s.endsWith(": 2") || s.endsWith(":2")) return 2;
    if (s.includes("clause") || s.includes("statutory") || s.includes("digest") || s.includes("legal") || s.includes("parchment") || s.includes("section") || s.includes("design 3") || s.includes("style 3") || s.endsWith(" 3") || s.endsWith(", 3") || s.endsWith(": 3") || s.endsWith(":3")) return 3;
    if (s.includes("pill") || s.includes("capsule") || s.includes("chip") || s.includes("minimal") || s.includes("design 4") || s.includes("style 4") || s.endsWith(" 4") || s.endsWith(", 4") || s.endsWith(": 4") || s.endsWith(":4")) return 4;
    if (s.includes("obsidian") || s.includes("dark") || s.includes("neon") || s.includes("cyber") || s.includes("horizon") || s.includes("design 5") || s.includes("style 5") || s.endsWith(" 5") || s.endsWith(", 5") || s.endsWith(": 5") || s.endsWith(":5")) return 5;
    return 1; // Default: cards / elevated
  }

  /**
   * Detection & Extraction for List shape lines:
   *   shape (list) (Title) [ (Item 1) (Item 2) ] (center)
   *   shape (list, cards) [ (Item 1) (Item 2) ]
   *   shape (list, timeline) [ (Step 1) (Step 2) ]
   *   shape (list, clause) [ (Clause a) (Clause b) ]
   *   shape (list, pills) [ (Item 1) (Item 2) ]
   *   shape (list, obsidian) [ (Item 1) (Item 2) ]
   */
  function parseListLine(line, tokens, activeListActor) {
    if (!line) return null;
    const lower = line.toLowerCase().trim();

    // Must NOT match "checklist" or "check list"
    if (lower.includes("checklist") || lower.includes("check list") || lower.includes("check_list")) {
      return null;
    }

    const isListDecl = lower.includes("shape (list") ||
                       lower.startsWith("shape (list") ||
                       /shape\s*\(\s*list[\s,\)]/i.test(line) ||
                       lower.startsWith("list (") ||
                       lower.startsWith("list [");

    const isExplicitShape = isListDecl;

    // 1. Bracket syntax e.g. shape (list, cards) (Title) [ (Item 1)(1s) (Item 2)(2s) ] (center)
    const bracketMatch = line.match(/\[([\s\S]+)\]/);
    if (isListDecl && bracketMatch) {
      let pos = "center";
      const outside = line.replace(bracketMatch[0], "");
      for (let k of SORTED_GRID_KEYS) {
        if (outside.toLowerCase().includes(k)) {
          pos = k;
          break;
        }
      }

      // Extract design
      let design = 1;
      const outsideTokens = extractBalancedParentheses(outside);
      let title = "STATUTORY PROVISIONS & EXPLANATION";

      for (let tok of outsideTokens) {
        const cleanTok = tok.trim();
        const lowTok = cleanTok.toLowerCase();
        if (lowTok.startsWith("shape") || lowTok === "list" || lowTok.includes("list") || GRID_POSITIONS[lowTok]) {
          if (lowTok.includes("list")) {
            const d = resolveListDesign(cleanTok);
            if (d !== 1) design = d;
          }
          continue;
        }
        if (/^(?:design|style)\s*[:=]?\s*(\w+)$/i.test(cleanTok)) {
          design = resolveListDesign(cleanTok);
          continue;
        }
        if (/^(?:cards|timeline|clause|pills|obsidian|stepped|process|statutory)$/i.test(lowTok)) {
          design = resolveListDesign(lowTok);
          continue;
        }
        // First substantive token outside brackets becomes title
        if (!title || title === "STATUTORY PROVISIONS & EXPLANATION") {
          title = cleanTok;
        }
      }

      const inner = bracketMatch[1];
      const innerTokens = extractBalancedParentheses(inner);
      const items = [];
      let currentItem = null;

      innerTokens.forEach(tok => {
        const cleanTok = tok.trim();
        const lowTok = cleanTok.toLowerCase();
        const delay = parseItemDelay(cleanTok);
        const dMatch = cleanTok.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);

        if (delay !== null) {
          if (currentItem) currentItem.delayMs = delay;
        } else if (dMatch) {
          if (currentItem) currentItem.dialogue = dMatch[1].trim();
        } else if (/^(?:dialogue|narration|speech)$/i.test(lowTok)) {
          // next token will be dialogue
        } else {
          if (currentItem) items.push(currentItem);
          let itTitle = cleanTok;
          let itDesc = "";
          if (cleanTok.includes(":") && !cleanTok.startsWith("http")) {
            const parts = cleanTok.split(":");
            itTitle = parts[0].trim();
            itDesc = parts.slice(1).join(":").trim();
          }
          currentItem = {
            title: itTitle,
            desc: itDesc,
            text: itDesc ? `${itTitle}: ${itDesc}` : itTitle,
            delayMs: null,
            dialogue: "",
            pos: null
          };
        }
      });
      if (currentItem) items.push(currentItem);

      return {
        isDeclaration: true,
        isCompleteInline: true,
        pos: pos,
        title: title,
        design: design,
        items: items
      };
    }

    if (isExplicitShape) {
      if (!tokens || tokens.length === 0) return null;
      let design = 1;
      let pos = "center";
      let title = "STATUTORY PROVISIONS & EXPLANATION";

      for (let tok of tokens) {
        const low = tok.toLowerCase().trim();
        if (GRID_POSITIONS[low]) {
          pos = low;
        } else if (/^(?:design|style)\s*[:=]?\s*(\w+)$/i.test(tok) || /^(?:cards|timeline|clause|pills|obsidian|stepped|process|statutory)$/i.test(low)) {
          design = resolveListDesign(tok);
        } else if (low.includes("list")) {
          const d = resolveListDesign(low);
          if (d !== 1) design = d;
        } else if (!title || title === "STATUTORY PROVISIONS & EXPLANATION") {
          title = tok.trim();
        }
      }

      return {
        isDeclaration: true,
        isCompleteInline: false,
        pos: pos,
        title: title,
        design: design,
        item: null
      };
    }

    // Shorthand item lines when activeListActor exists in current scene
    if (activeListActor && tokens && tokens.length > 0) {
      const parsed = extractListItemFromTokens(tokens, false);
      if (parsed.text) {
        return {
          isDeclaration: false,
          item: parsed
        };
      }
    }

    return null;
  }

  /**
   * Helper to parse a mind map dot-notation hierarchical code:
   * e.g. "1", "1.1", "1.2", "1.2.1", "2.3.4"
   */
  function parseMindMapNodeCode(str) {
    if (!str) return null;
    const clean = str.trim().replace(/^[\(\[\{]/, "").replace(/[\)\]\}]$/, "").trim();
    if (!/^\d+(?:\.\d+)*$/.test(clean)) return null;
    const parts = clean.split(".").map(p => parseInt(p, 10));
    const level = parts.length;
    const parentCode = level > 1 ? parts.slice(0, -1).join(".") : null;
    const branchIndex = level >= 2 ? (parts[1] - 1) : 0;
    return {
      code: clean,
      parts: parts,
      level: level,
      parentCode: parentCode,
      branchIndex: Math.max(0, branchIndex)
    };
  }

  /**
   * Normalizes mind map line text by wrapping bare codes outside parens in (code)
   * e.g. "1.1 (Text) (time)" -> "(1.1) (Text) (time)"
   * e.g. "shape type (mind) (1) (Text) (time) 1.1 (Text) (time)" -> "(1) (Text) (time) (1.1) (Text) (time)"
   */
  function normalizeMindMapInput(line) {
    if (!line) return "";
    let s = line.trim();
    // Strip shape declaration prefix if present
    s = s.replace(/^shape\s+(?:type\s+)?(?:\(?mind(?:map|_map|\s+map)?\)?)\s*/i, "");

    let result = "";
    let inParen = 0;
    let inBracket = 0;
    let buffer = "";

    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch === '(') inParen++;
      else if (ch === ')') inParen = Math.max(0, inParen - 1);
      else if (ch === '[') inBracket++;
      else if (ch === ']') inBracket = Math.max(0, inBracket - 1);

      if (inParen === 0 && inBracket === 0) {
        buffer += ch;
      } else {
        if (buffer.length > 0) {
          result += buffer.replace(/\b(\d+(?:\.\d+)*)\b/g, "($1)");
          buffer = "";
        }
        result += ch;
      }
    }
    if (buffer.length > 0) {
      result += buffer.replace(/\b(\d+(?:\.\d+)*)\b/g, "($1)");
    }
    return result;
  }

  /**
   * Extracts an array of node objects from tokens for a mind map
   */
  function parseMindMapNodesFromTokens(tokens) {
    const nodes = [];
    let currentNode = null;

    for (let i = 0; i < tokens.length; i++) {
      const tok = tokens[i].trim();
      const nodeInfo = parseMindMapNodeCode(tok);
      if (nodeInfo) {
        if (currentNode) nodes.push(currentNode);
        currentNode = {
          code: nodeInfo.code,
          parts: nodeInfo.parts,
          level: nodeInfo.level,
          parentCode: nodeInfo.parentCode,
          branchIndex: nodeInfo.branchIndex,
          text: "",
          delayMs: null,
          dialogue: "",
          pos: null
        };
        continue;
      }

      if (!currentNode) continue;

      // Check dialogue / narration
      const dMatch = tok.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
      if (dMatch) {
        currentNode.dialogue = dMatch[1].trim();
        continue;
      }
      if (/^(?:dialogue|narration|speech)$/i.test(tok.toLowerCase()) && i + 1 < tokens.length) {
        currentNode.dialogue = tokens[i + 1].trim().replace(/^["']|["']$/g, "");
        i++;
        continue;
      }

      // Check position keyword
      const tLow = tok.toLowerCase();
      if (GRID_POSITIONS[tLow] || tLow.includes("%")) {
        currentNode.pos = tok;
        continue;
      }

      // Check delay keyword or literal "time"
      if (tLow === "time" && currentNode.delayMs === null) {
        currentNode.delayMs = 1000;
        continue;
      }
      const delay = parseItemDelay(tok);
      if (delay !== null && currentNode.delayMs === null) {
        currentNode.delayMs = delay;
        continue;
      }

      // Otherwise text label
      if (!currentNode.text) {
        currentNode.text = tok;
      } else {
        currentNode.text += " " + tok;
      }
    }
    if (currentNode) nodes.push(currentNode);
    return nodes;
  }

  /**
   * Main detection & parser for Mind Map lines:
   * Supports:
   *   shape (mind) (1) (Capital Asset) (1s) (center)
   *   shape (mind) (1.1) (Movable) (1s)
   *   shape type (mind) (1) (Text) (time) 1.1 (Text) (time) 1.2 (Text) (time)
   *   (1.1) (Movable) (1s)
   *   1.1 (Movable) (1s)
   *   shape (mind) [ (1)(Root)(center) (1.1)(Branch)(1s) ... ]
   */
  function parseMindMapLine(line, tokens, activeMindMapActor) {
    if (!line) return null;
    const lower = line.toLowerCase().trim();

    const isExplicitDecl = lower.includes("shape (mind") ||
                           lower.includes("shape type (mind") ||
                           lower.includes("shape (mindmap") ||
                           lower.includes("shape (mind_map") ||
                           lower.startsWith("shape (mind map)") ||
                           lower.startsWith("mindmap") ||
                           lower.startsWith("mind map");

    // 1. Bracket syntax: shape (mind) [ ... ]
    const bracketMatch = line.match(/\[([\s\S]+)\]/);
    if ((isExplicitDecl || activeMindMapActor) && bracketMatch) {
      let pos = "center";
      const outside = line.replace(bracketMatch[0], "");
      for (let k of SORTED_GRID_KEYS) {
        if (outside.toLowerCase().includes(k)) {
          pos = k;
          break;
        }
      }
      const inner = bracketMatch[1];
      const normInner = normalizeMindMapInput(inner);
      const innerTokens = extractBalancedParentheses(normInner);
      const nodes = parseMindMapNodesFromTokens(innerTokens);
      return {
        isDeclaration: true,
        isCompleteInline: true,
        pos: pos,
        nodes: nodes
      };
    }

    // 2. Explicit shape declaration line
    if (isExplicitDecl) {
      const norm = normalizeMindMapInput(line);
      const normTokens = extractBalancedParentheses(norm);
      const nodes = parseMindMapNodesFromTokens(normTokens);

      let pos = "center";
      for (let k of SORTED_GRID_KEYS) {
        if (lower.includes(k)) {
          pos = k;
          break;
        }
      }

      return {
        isDeclaration: true,
        isCompleteInline: nodes.length > 1,
        pos: pos,
        nodes: nodes
      };
    }

    // 3. Shorthand or bare line if activeMindMapActor exists in scene
    if (activeMindMapActor) {
      const norm = normalizeMindMapInput(line);
      const normTokens = extractBalancedParentheses(norm);
      if (normTokens.length > 0) {
        const nodes = parseMindMapNodesFromTokens(normTokens);
        if (nodes.length > 0) {
          return {
            isDeclaration: false,
            nodes: nodes
          };
        }
      }
    }

    return null;
  }

  /**
   * Computes sequential relative timeline for mind map nodes:
   * "each time is from the previous list item not from the beginning"
   * Next node only appears after previous node's voice dialogue completes!
   */
  function computeMindMapTimeline(actor) {
    if (!actor || !actor.isMindMap) return;
    const nodes = actor.nodes || [];
    if (nodes.length === 0) {
      actor.totalTimelineMs = 2000;
      return;
    }

    const baseOffsetMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 350;
    let runningTimeMs = baseOffsetMs + (actor.startMs !== undefined ? 150 : 350);

    nodes.forEach((node, idx) => {
      node.startMs = runningTimeMs;
      const words = node.dialogue ? node.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const delay = (node.delayMs !== null && node.delayMs !== undefined) ? node.delayMs : (idx === 0 ? 500 : 600);
      const activeSpan = Math.max(speechMs, delay, 1200);
      node.endMs = node.startMs + activeSpan;
      runningTimeMs = node.endMs + 350; // next branch enters only after previous branch's voice completes!
    });

    actor.totalTimelineMs = runningTimeMs;
  }

  /**
   * Pixel-accurate word wrapping for text lines within mind map cards
   */
  function wrapMindMapText(ctx, text, maxW, font) {
    if (!text) return [""];
    if (ctx && font) {
      ctx.save();
      ctx.font = font;
    }
    const words = String(text).trim().split(/\s+/);
    const lines = [];
    let curLine = "";

    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      const test = curLine ? (curLine + " " + w) : w;
      const testW = (ctx && ctx.measureText) ? ctx.measureText(test).width : (test.length * 7.5);
      if (testW <= maxW) {
        curLine = test;
      } else {
        if (curLine) {
          lines.push(curLine);
          curLine = w;
        } else {
          lines.push(w);
          curLine = "";
        }
      }
    }
    if (curLine) lines.push(curLine);
    if (ctx && font) ctx.restore();
    return lines.length > 0 ? lines : [text];
  }

  /**
   * Collision-free hierarchical tree layout algorithm:
   * Computes (x, y) coordinates for all nodes using recursive subtree bounding heights.
   * Root cards and branch cards are dynamically auto-sized to fit long multi-line statutory text.
   */
  function layoutMindMapNodes(actor, canvasW, canvasH, ctx) {
    canvasW = canvasW || 1280;
    canvasH = canvasH || 720;
    const nodes = actor.nodes || [];
    if (nodes.length === 0) return;

    const nodeMap = {};
    nodes.forEach(n => {
      nodeMap[n.code] = n;
      n.children = [];
    });

    const roots = [];
    nodes.forEach(n => {
      if (n.parentCode && nodeMap[n.parentCode]) {
        nodeMap[n.parentCode].children.push(n);
      } else {
        roots.push(n);
      }
    });

    let maxLevel = 1;
    nodes.forEach(n => {
      if (n.level > maxLevel) maxLevel = n.level;
    });

    const colSpacing = maxLevel <= 1 ? 0 : Math.min(380, Math.floor((canvasW - 280) / (maxLevel - 1)));
    const totalTreeW = (maxLevel - 1) * colSpacing;
    const startX = Math.round((canvasW - totalTreeW) / 2);

    // Compute node dimensions with multi-line text wrapping & boosted font sizes
    const baseW = maxLevel <= 2 ? 300 : (maxLevel === 3 ? 275 : 242);

    nodes.forEach(n => {
      n.w = n.level === 1 ? (baseW + 20) : (n.level === 2 ? baseW : (baseW - 10));
      const font = n.level === 1 ? "700 17.5px 'Inter', -apple-system, sans-serif" :
                   (n.level === 2 ? "600 15px 'Inter', -apple-system, sans-serif" :
                                    "600 13.5px 'Inter', -apple-system, sans-serif");
      const maxTextW = n.w - 26;

      // Wrap text into multiple lines
      n.lines = wrapMindMapText(ctx, n.text, maxTextW, font);
      const lineCount = Math.max(1, n.lines.length);
      const lineHeight = n.level === 1 ? 22 : (n.level === 2 ? 19.5 : 17.5);
      const baseH = n.level === 1 ? 54 : (n.level === 2 ? 48 : 42);

      // Expand card height dynamically to fit all text lines without truncation
      n.h = baseH + (lineCount - 1) * lineHeight;
    });

    const rowGap = 14;
    function computeSubtreeHeight(node) {
      if (!node.children || node.children.length === 0) {
        node.subtreeH = node.h + rowGap;
        return node.subtreeH;
      }
      let total = 0;
      node.children.forEach(c => {
        total += computeSubtreeHeight(c);
      });
      node.subtreeH = Math.max(node.h + rowGap, total);
      return node.subtreeH;
    }

    let totalForestH = 0;
    roots.forEach(r => {
      totalForestH += computeSubtreeHeight(r);
    });

    // Vertical scaling if forest exceeds canvas bounds
    const maxUsableH = canvasH - 120;
    const scaleY = totalForestH > maxUsableH ? (maxUsableH / totalForestH) : 1.0;

    const startY = (canvasH - (totalForestH * scaleY)) / 2;
    let curForestY = startY;

    function positionSubtree(node, bandTop, bandH) {
      node.x = startX + (node.level - 1) * colSpacing;
      if (!node.children || node.children.length === 0) {
        node.y = bandTop + bandH / 2;
        return;
      }
      let cCursor = bandTop;
      node.children.forEach(c => {
        const scaledH = c.subtreeH * scaleY;
        positionSubtree(c, cCursor, scaledH);
        cCursor += scaledH;
      });
      const firstC = node.children[0];
      const lastC = node.children[node.children.length - 1];
      node.y = (firstC.y + lastC.y) / 2;
    }

    roots.forEach(r => {
      const scaledRootH = r.subtreeH * scaleY;
      positionSubtree(r, curForestY, scaledRootH);
      curForestY += scaledRootH;
    });
  }

  /**
   * Detection & Extraction for Calculation (single) / Formula lines:
   * e.g. shape (calculation (single)) [ ( (Asset)(10,00,000) / (Liability)(5,00,000) ) ^ (Time)(2) = (Solvency Ratio)(4) ] (center)
   * e.g. calculation (single) [ ( (Asset) / (Liability) ) ^ (Time) ]
   */
  function parseCalculationSingleLine(line) {
    if (!line) return null;
    const lower = line.toLowerCase().trim();

    const isSingleCalc = lower.includes("calculation (single)") ||
                         lower.includes("calculation_single") ||
                         lower.includes("calc_single") ||
                         lower.includes("calc (single)") ||
                         lower.includes("shape (formula)") ||
                         lower.includes("shape (equation)") ||
                         lower.startsWith("formula") ||
                         lower.startsWith("equation");

    if (!isSingleCalc) return null;

    let formulaExpr = "";
    let pos = "center";

    // 1. Match bracket expression [ ... ]
    const bracketMatch = line.match(/\[([\s\S]+)\]/);
    if (bracketMatch) {
      formulaExpr = bracketMatch[1].trim();
      const outside = line.replace(bracketMatch[0], "");
      for (let k of SORTED_GRID_KEYS) {
        if (outside.toLowerCase().includes(k)) {
          pos = k;
          break;
        }
      }
    } else {
      // 2. Match parenthesis expression following keyword
      const idx = lower.indexOf("single");
      const startSearch = idx !== -1 ? (idx + 6) : 0;
      const rest = line.substring(startSearch);
      const openParen = rest.indexOf("(");
      if (openParen !== -1) {
        let depth = 0;
        let start = -1;
        let end = -1;
        for (let j = openParen; j < rest.length; j++) {
          if (rest[j] === '(') {
            if (depth === 0) start = j + 1;
            depth++;
          } else if (rest[j] === ')') {
            depth--;
            if (depth === 0) {
              end = j;
              break;
            }
          }
        }
        if (start !== -1 && end !== -1) {
          formulaExpr = rest.substring(start, end).trim();
          const outside = rest.substring(end + 1);
          for (let k of SORTED_GRID_KEYS) {
            if (outside.toLowerCase().includes(k)) {
              pos = k;
              break;
            }
          }
        }
      }
    }

    if (!formulaExpr) return null;
    return { formulaExpr, pos };
  }

  /**
   * Tokenizer for Formula Expressions:
   * Extracts terms (text)(amount)(time) and math operators /, ^, *, +, -, =, (, )
   */
  function tokenizeFormula(expr) {
    let s = expr.trim();
    if (s.startsWith("[") && s.endsWith("]")) {
      s = s.slice(1, -1).trim();
    }

    const tokens = [];
    let i = 0;
    const n = s.length;

    while (i < n) {
      const ch = s[i];

      if (/\s/.test(ch)) {
        i++;
        continue;
      }

      if (ch === '/' || ch === '^' || ch === '*' || ch === '×' || ch === '+' || ch === '-' || ch === '−' || ch === '=') {
        tokens.push({ type: 'op', value: ch === '×' ? '*' : (ch === '−' ? '-' : ch) });
        i++;
        continue;
      }

      if (ch === '[' || ch === ']' || ch === '{' || ch === '}') {
        tokens.push({ type: 'paren', value: (ch === '[' || ch === '{') ? '(' : ')' });
        i++;
        continue;
      }

      if (ch === '(') {
        let depth = 1;
        let j = i + 1;
        while (j < n && depth > 0) {
          if (s[j] === '(') depth++;
          else if (s[j] === ')') depth--;
          j++;
        }
        const inside = s.substring(i + 1, j - 1).trim();

        // If inside contains nested parentheses, it is a subexpression grouping! e.g. ( (A) / (B) )
        if (inside.includes('(')) {
          tokens.push({ type: 'paren', value: '(' });
          i++;
          continue;
        }

        // Otherwise it is an atomic term: (text) optional (amount) optional (dialogue) optional (time)
        let termText = inside;
        let termAmount = null;
        let introTimeMs = null;
        let termDialogue = "";

        const timeInlineMatch = inside.match(/(?:,\s*after\s*|\s+after\s+|\s*,\s*)(\d+(?:\.\d+)?)\s*(?:s|sec|seconds)\b/i);
        if (timeInlineMatch) {
          introTimeMs = Math.round(parseFloat(timeInlineMatch[1]) * 1000);
          termText = inside.replace(timeInlineMatch[0], "").trim();
        }

        i = j;

        // Loop over any adjacent parenthesized chunks for this term: (amount), (dialogue: "..."), (time)
        while (i < n && /\s/.test(s[i])) i++;
        while (i < n && s[i] === '(') {
          let j2 = i + 1;
          let depth2 = 1;
          while (j2 < n && depth2 > 0) {
            if (s[j2] === '(') depth2++;
            else if (s[j2] === ')') depth2--;
            j2++;
          }
          const inside2 = s.substring(i + 1, j2 - 1).trim();
          if (inside2.includes('(')) break; // Nested paren grouping (subexpression), stop

          // Check if dialogue
          const dMatch = inside2.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
          if (dMatch) {
            termDialogue = dMatch[1].trim();
            i = j2;
            while (i < n && /\s/.test(s[i])) i++;
            continue;
          }
          if (/^(?:dialogue|narration|speech)$/i.test(inside2)) {
            let k = j2;
            while (k < n && /\s/.test(s[k])) k++;
            if (k < n && s[k] === '(') {
              let k2 = k + 1, kd = 1;
              while (k2 < n && kd > 0) {
                if (s[k2] === '(') kd++;
                else if (s[k2] === ')') kd--;
                k2++;
              }
              termDialogue = s.substring(k + 1, k2 - 1).trim().replace(/^["']|["']$/g, "");
              i = k2;
              while (i < n && /\s/.test(s[i])) i++;
              continue;
            }
          }

          // Check if time delay e.g. "after 1.5s", "1s", "1000ms"
          const parsedDelay = parseItemDelay(inside2);
          if (parsedDelay !== null) {
            introTimeMs = parsedDelay;
            i = j2;
            while (i < n && /\s/.test(s[i])) i++;
            continue;
          }

          // Otherwise check if amount chunk e.g. "10,00,000" or "1000000, after 1.5s"
          if (!termAmount) {
            const timeInAmtMatch = inside2.match(/(?:,\s*after\s*|\s+after\s+|\s*,\s*)(\d+(?:\.\d+)?)\s*(?:s|sec|seconds)\b/i);
            if (timeInAmtMatch) {
              introTimeMs = Math.round(parseFloat(timeInAmtMatch[1]) * 1000);
              termAmount = inside2.replace(timeInAmtMatch[0], "").trim();
            } else {
              termAmount = inside2;
            }
            i = j2;
            while (i < n && /\s/.test(s[i])) i++;
            continue;
          }

          // If not recognized, stop loop so we don't swallow other terms
          break;
        }

        const amtData = parseAmountValue(termAmount);
        tokens.push({
          type: 'term',
          text: termText,
          amount: amtData.raw,
          num: amtData.num,
          currency: amtData.currency,
          dialogue: termDialogue,
          introTimeMs: introTimeMs
        });
        continue;
      }

      if (ch === ')') {
        tokens.push({ type: 'paren', value: ')' });
        i++;
        continue;
      }

      // Bare word
      let j = i;
      while (j < n && !/[\s\(\)\[\]\/\^\*\+\=\-]/.test(s[j])) {
        j++;
      }
      const bare = s.substring(i, j).trim();
      if (bare) {
        tokens.push({
          type: 'term',
          text: bare,
          amount: "",
          num: null,
          currency: "₹",
          introTimeMs: null
        });
      }
      i = j;
    }

    return tokens;
  }

  /**
   * AST Parser for Mathematical Formulas using recursive descent
   * Assigns 0.5s sequential pop-up stagger when custom times are omitted.
   */
  function parseFormulaExpression(rawExpr) {
    if (!rawExpr || !rawExpr.trim()) return null;
    const tokens = tokenizeFormula(rawExpr);
    if (!tokens || tokens.length === 0) return null;

    let pos = 0;
    let termCounter = 0;
    let maxIntroMs = 0;

    function peek() {
      return tokens[pos] || null;
    }

    function consume(expectedValue) {
      const tok = tokens[pos];
      if (!tok) return null;
      if (expectedValue && tok.value !== expectedValue) return null;
      pos++;
      return tok;
    }

    function parseEquality() {
      let left = parseAdditive();
      while (peek() && peek().type === 'op' && peek().value === '=') {
        const op = consume().value;
        const right = parseAdditive();
        left = { type: 'binary', op: '=', left, right };
      }
      return left;
    }

    function parseAdditive() {
      let left = parseMultiplicative();
      while (peek() && peek().type === 'op' && (peek().value === '+' || peek().value === '-')) {
        const op = consume().value;
        const right = parseMultiplicative();
        left = { type: 'binary', op: op === '-' ? '−' : op, left, right };
      }
      return left;
    }

    function parseMultiplicative() {
      let left = parsePower();
      while (peek() && peek().type === 'op' && (peek().value === '*' || peek().value === '/')) {
        const op = consume().value;
        const right = parsePower();
        if (op === '/') {
          left = { type: 'fraction', numerator: left, denominator: right };
        } else {
          left = { type: 'binary', op: '×', left, right };
        }
      }
      return left;
    }

    function parsePower() {
      let base = parsePrimary();
      if (peek() && peek().type === 'op' && peek().value === '^') {
        consume();
        const exponent = parsePower();
        return { type: 'power', base, exponent };
      }
      return base;
    }

    function parsePrimary() {
      const tok = peek();
      if (!tok) return null;

      if (tok.type === 'paren' && tok.value === '(') {
        consume();
        const inner = parseEquality();
        if (peek() && peek().type === 'paren' && peek().value === ')') {
          consume();
        }
        return { type: 'bracket', inner };
      }

      if (tok.type === 'term') {
        consume();
        const termId = termCounter++;
        const termNode = {
          type: 'term',
          id: termId,
          text: tok.text,
          amount: tok.amount,
          num: tok.num,
          currency: tok.currency,
          dialogue: tok.dialogue || "",
          introTimeMs: tok.introTimeMs
        };
        terms.push(termNode);
        return termNode;
      }

      consume();
      return null;
    }

    const terms = [];
    const root = parseEquality();

    // Compute sequential timeline for formula terms based on speech length
    let runningTermMs = 400;
    terms.forEach((term, idx) => {
      const words = term.dialogue ? term.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const introMs = (term.introTimeMs !== null && term.introTimeMs !== undefined) ? term.introTimeMs : runningTermMs;
      term.introTimeMs = introMs;
      const activeSpan = Math.max(speechMs, 800);
      term.endMs = term.introTimeMs + activeSpan;
      runningTermMs = term.endMs + 350; // next term enters after previous term's voice finishes!
      if (term.endMs > maxIntroMs) maxIntroMs = term.endMs;
    });

    return {
      ast: root,
      terms: terms,
      totalTerms: termCounter,
      maxIntroMs: maxIntroMs
    };
  }

  /**
   * Computes sequential relative timeline for calculation (single) formula terms:
   * Next term and math roll only starts after previous term's dialogue voice completes!
   */
  function computeCalculationSingleTimeline(actor) {
    if (!actor || !actor.isCalculationSingle || !actor.formulaData || !actor.formulaData.terms) return;
    const baseOffsetMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 350;
    let runningTermMs = baseOffsetMs + 400;
    let maxMs = runningTermMs;

    actor.formulaData.terms.forEach((term, idx) => {
      term.introTimeMs = runningTermMs;
      const words = term.dialogue ? term.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
      const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : 0;
      const activeSpan = Math.max(speechMs, 800);
      term.endMs = term.introTimeMs + activeSpan;
      runningTermMs = term.endMs + 350;
      if (term.endMs > maxMs) maxMs = term.endMs;
    });

    actor.formulaData.maxIntroMs = maxMs;
    actor.totalTimelineMs = runningTermMs;
  }

  /**
   * Main Prompt Parser:
   * Converts raw text lines into structured presentation slides
   */
  function parseScriptPrompt(rawText) {
    if (!rawText || !rawText.trim()) return null;

    const lines = rawText.split(/\r?\n/);
    const scenes = [];
    let currentScene = {
      id: 1,
      tab_title: "1. Kinetic Animation Scene",
      dialogue: "",
      shapeDialogues: [],
      actors: [],
      hasHeading: false
    };

    const shapeRegex = /shape\s*\(([^)]+)\)\s*\(([^)]+)\)\s*\(([^)]+)\)\s*\(([^)]+)\)\s*(?:\(([^)]+)\))?/i;

    for (let rawLine of lines) {
      let line = rawLine.trim();
      if (!line || line.startsWith("//") || line.startsWith("#")) continue;

      // Slide or Scene boundary
      const slideMatch = line.match(/^(?:SLIDE|SCENE)\s*(\d+)?\s*:?\s*(.*)$/i);
      if (slideMatch) {
        const slideNum = slideMatch[1] ? parseInt(slideMatch[1], 10) : (scenes.length + 1);
        const slideTitle = slideMatch[2] ? slideMatch[2].trim() : `Scene ${slideNum}`;
        if (!currentScene.dialogue && currentScene.shapeDialogues && currentScene.shapeDialogues.length > 0) {
          currentScene.dialogue = currentScene.shapeDialogues.join(" ");
        }
        if (currentScene.actors.length > 0 || currentScene.dialogue) {
          scenes.push(currentScene);
          currentScene = {
            id: scenes.length + 1,
            tab_title: `${scenes.length + 1}. ${slideTitle}`,
            dialogue: "",
            shapeDialogues: [],
            actors: [],
            hasHeading: false
          };
        } else {
          currentScene.tab_title = `${slideNum}. ${slideTitle}`;
          currentScene.hasHeading = false;
        }
        continue;
      }

      // Title line
      const titleMatch = line.match(/^TITLE\s*:\s*["']?(.*?)["']?$/i);
      if (titleMatch) {
        currentScene.tab_title = titleMatch[1];
        continue;
      }

      // Narration / Speech line
      const narrMatch = line.match(/^(?:NARRATION|SPEECH|DIALOGUE|TEACHER)\s*:\s*["']?(.*?)["']?$/i);
      if (narrMatch) {
        currentScene.dialogue = narrMatch[1];
        continue;
      }

      // Pop Up Choreography Directive:
      // Supported syntaxes:
      // - (pop up, id: 1, right)
      // - (popup, id: 1, right)
      // - (pop up, id: 1, left)
      // - (pop up, id: 1, top)
      // - (pop up, id: 1, bottom)
      let linePopupData = null;
      const popupMatch = line.match(/\(\s*(?:pop\s*up|popup|emerge)\s*[,:]?\s*(?:from\s*)?(?:id\s*:\s*)?(\w+)(?:\s*[,:]?\s*(\w+))?\s*\)/i);
      if (popupMatch) {
        const rawAnchorId = popupMatch[1].trim();
        const anchorId = isNaN(rawAnchorId) ? rawAnchorId : parseInt(rawAnchorId, 10);
        const direction = (popupMatch[2] || "right").toLowerCase().trim();
        linePopupData = { anchorId, direction };
        line = line.replace(popupMatch[0], "").replace(/\s{2,}/g, " ").trim();
      }

      // Shape Identification Number Detection (e.g. 1, 2, 3):
      // Supported syntaxes:
      // - Line prefix: "1. shape ...", "1) shape ...", "(1) shape ...", "#1 shape ..."
      // - Shape number: "shape 1 (...) ...", "shape #1 (...) ..."
      // - Parenthesized ID token: "shape (1) (...) ...", "shape (id: 1) (...) ...", "shape (#1) (...) ..."
      // The identification number is purely internal metadata for sequence choreography.
      // It is strictly NEVER displayed on screen (0% canvas clutter).
      let lineShapeId = null;

      // 1. Line prefix e.g. "1. shape", "(1) shape", "1) shape", "#1 shape"
      const leadIdMatch = line.match(/^(\(?\d+\)?|\d+[\.\)]|#\d+)\s+(shape|check\s*list|mind\s*map|calculation|heading)/i);
      if (leadIdMatch) {
        lineShapeId = parseInt(leadIdMatch[1].replace(/[^\d]/g, ""), 10);
        line = line.replace(/^(\(?\d+\)?|\d+[\.\)]|#\d+)\s+/i, "");
      }

      // 2. Shape with space number e.g. "shape 1 (", "shape #1 ("
      const shapeNumMatch = line.match(/^shape\s+(?:#)?(\d+)\s*\(/i);
      if (shapeNumMatch) {
        if (lineShapeId === null) lineShapeId = parseInt(shapeNumMatch[1], 10);
        line = line.replace(/^shape\s+(?:#)?\d+\s*\(/i, "shape (");
      }

      // 3. Option C explicit ID attribute e.g. "(id: 1)", "(id: 2)", "(id: shape1)" anywhere in the line
      const anyIdMatch = line.match(/\(\s*id\s*:\s*(\w+)\s*\)/i);
      if (anyIdMatch) {
        if (lineShapeId === null) {
          lineShapeId = isNaN(anyIdMatch[1]) ? anyIdMatch[1] : parseInt(anyIdMatch[1], 10);
        }
        line = line.replace(/\(\s*id\s*:\s*\w+\s*\)/i, "").replace(/\s{2,}/g, " ");
      }

      // 4. Shape with immediate parenthesized numeric ID e.g. "shape (1) (", "shape (#1) ("
      const shapeParenIdMatch = line.match(/^shape\s*\(\s*(?:#)?(\d+)\s*\)\s*\(/i);
      if (shapeParenIdMatch) {
        if (lineShapeId === null) lineShapeId = parseInt(shapeParenIdMatch[1], 10);
        line = line.replace(/^shape\s*\(\s*(?:#)?\d+\s*\)\s*\(/i, "shape (");
      }

      // 0. Check for Heading shape: shape (Heading) (text) (subtitle (if any)) (Text)
      // EXCLUSIVITY RULE: If a heading shape is in this slide, it MUST be the only shape.
      const tokens = extractBalancedParentheses(line);
      const parsedHeading = parseHeadingLine(line, tokens);
      if (parsedHeading) {
        const startPos = resolvePosition(parsedHeading.pos || "center");
        const headingActor = {
          shapeId: lineShapeId,
          shapeType: "heading",
          shapeCategory: "corporate",
          isHeading: true,
          textLabel: parsedHeading.titleText,
          titleText: parsedHeading.titleText,
          subtitleText: parsedHeading.subtitleText,
          icon: "bookmark",
          accent: "indigo",
          startPos: startPos,
          intro: "fade",
          outro: "fade",
          hasIntroFade: parsedHeading.hasIntroFade !== false,
          hasOutroFade: parsedHeading.hasOutroFade !== false,
          introDurationMs: parsedHeading.introDurationMs || 600,
          outroDurationMs: parsedHeading.outroDurationMs || 450,
          slideDurationMs: parsedHeading.slideDurationMs || null,
          motion: { hasMotion: false },
          startMs: parsedHeading.delayMs || 0,
          subtitleDelayMs: parsedHeading.subtitleDelayMs || 450
        };

        // Wipe any previous actors on this slide and lock out future ones
        currentScene.actors = [headingActor];
        currentScene.hasHeading = true;
        if (parsedHeading.dialogueText && !currentScene.dialogue) {
          currentScene.dialogue = parsedHeading.dialogueText;
        }

        if (!currentScene.tab_title || currentScene.tab_title.includes("Scene ")) {
          const slidePrefix = currentScene.id || scenes.length + 1;
          currentScene.tab_title = `${slidePrefix}. ${parsedHeading.titleText}`;
        }
        continue;
      }

      // If slide already has a heading shape, enforce exclusivity by skipping all other shapes
      if (currentScene.hasHeading) {
        continue;
      }

      // 1A. Check for single calculation / formula: shape (calculation (single)) [ ... ]
      const parsedSingle = parseCalculationSingleLine(line);
      if (parsedSingle) {
        const formulaData = parseFormulaExpression(parsedSingle.formulaExpr);
        if (formulaData && formulaData.ast) {
          const startPos = resolvePosition(parsedSingle.pos || "center");
          currentScene.actors.push({
            shapeId: lineShapeId,
            shapeType: "calculation_single",
            shapeCategory: "calculation",
            isCalculationSingle: true,
            textLabel: "Statutory Formula",
            icon: "calculator",
            accent: "indigo",
            startPos: startPos,
            intro: "fade",
            motion: { hasMotion: false },
            formulaData: formulaData
          });
          continue;
        }
      }

      // 1B. Check for multi-line calculation shape: shape (calculation (multiple)) (sign) (text) (amount)
      const parsedCalc = parseCalculationLine(line, tokens);
      if (parsedCalc) {
        let calcActor = null;
        if (currentScene.actors.length > 0) {
          const last = currentScene.actors[currentScene.actors.length - 1];
          if (last && last.isCalculation) {
            calcActor = last;
          }
        }

        if (!calcActor) {
          const startPos = resolvePosition(parsedCalc.pos || "center");
          calcActor = {
            shapeId: lineShapeId,
            shapeType: "calculation_multiple",
            shapeCategory: "calculation",
            isCalculation: true,
            textLabel: "Statutory Computation",
            icon: "calculator",
            accent: "indigo",
            startPos: startPos,
            intro: "fade",
            motion: { hasMotion: false },
            items: []
          };
          currentScene.actors.push(calcActor);
        } else if (parsedCalc.pos && parsedCalc.pos !== "center") {
          calcActor.startPos = resolvePosition(parsedCalc.pos);
        }

        if (!parsedCalc.isHeaderOnly) {
          const amtData = parseAmountValue(parsedCalc.rawAmount);
          const signData = resolveSignType(parsedCalc.sign);
          calcActor.items.push({
            sign: signData.sign,
            signType: signData.type,
            text: parsedCalc.text,
            num: amtData.num,
            rawAmount: amtData.raw,
            currency: amtData.currency,
            dialogue: parsedCalc.dialogue || ""
          });
        }
        continue;
      }

      // 1C. Check for checklist shape: shape (check list) (text) (check ok / not) ... (unlock / not unlock)
      let activeChecklist = null;
      if (currentScene.actors.length > 0) {
        const last = currentScene.actors[currentScene.actors.length - 1];
        if (last && last.isChecklist) {
          activeChecklist = last;
        }
      }

      const parsedChecklist = parseChecklistLine(line, tokens, activeChecklist);
      if (parsedChecklist) {
        if (!activeChecklist || parsedChecklist.isCompleteInline) {
          const startPos = resolvePosition(parsedChecklist.pos || "center");
          const checklistActor = {
            shapeId: lineShapeId,
            shapeType: "checklist",
            shapeCategory: "checklist",
            isChecklist: true,
            textLabel: "Compliance Checklist",
            icon: "checkCircle",
            accent: "emerald",
            startPos: startPos,
            intro: "fade",
            motion: { hasMotion: false },
            title: parsedChecklist.title || "STATUTORY COMPLIANCE CHECKLIST",
            items: parsedChecklist.items || [],
            gateItem: parsedChecklist.gateItem || null
          };

          if (parsedChecklist.item) {
            if (parsedChecklist.item.status.type === "gate") {
              checklistActor.gateItem = parsedChecklist.item;
            } else {
              checklistActor.items.push(parsedChecklist.item);
            }
          }

          currentScene.actors.push(checklistActor);
          continue;
        } else {
          // Append to existing activeChecklist
          if (parsedChecklist.pos && parsedChecklist.pos !== "center") {
            activeChecklist.startPos = resolvePosition(parsedChecklist.pos);
          }
          if (parsedChecklist.item) {
            if (parsedChecklist.item.status.type === "gate") {
              activeChecklist.gateItem = parsedChecklist.item;
            } else {
              activeChecklist.items.push(parsedChecklist.item);
            }
          }
          continue;
        }
      }

      // 1D. Check for list shape: shape (list) (Title) [ (Item 1) (Item 2) ] (center)
      let activeList = null;
      if (currentScene.actors.length > 0) {
        const last = currentScene.actors[currentScene.actors.length - 1];
        if (last && last.isList) {
          activeList = last;
        }
      }

      const parsedList = parseListLine(line, tokens, activeList);
      if (parsedList) {
        if (!activeList || parsedList.isCompleteInline) {
          const startPos = resolvePosition(parsedList.pos || "center");
          const listActor = {
            shapeId: lineShapeId,
            shapeType: "list",
            shapeCategory: "list",
            isList: true,
            textLabel: "Explanatory List",
            icon: "list",
            accent: parsedList.design === 3 ? "amber" : (parsedList.design === 5 ? "emerald" : (parsedList.design === 2 ? "sky" : "indigo")),
            design: parsedList.design || 1,
            startPos: startPos,
            intro: "fade",
            motion: { hasMotion: false },
            title: parsedList.title || "STATUTORY PROVISIONS & EXPLANATION",
            items: parsedList.items || []
          };

          if (parsedList.item) {
            listActor.items.push(parsedList.item);
          }

          currentScene.actors.push(listActor);
          continue;
        } else {
          // Append to existing activeList
          if (parsedList.pos && parsedList.pos !== "center") {
            activeList.startPos = resolvePosition(parsedList.pos);
          }
          if (parsedList.item) {
            activeList.items.push(parsedList.item);
          }
          continue;
        }
      }

      // 1E. Check for mind map shape: shape (mind) (1) (Text) (time) 1.1 (Text) (time) ...
      let activeMindMap = null;
      if (currentScene.actors.length > 0) {
        const last = currentScene.actors[currentScene.actors.length - 1];
        if (last && last.isMindMap) {
          activeMindMap = last;
        }
      }

      const parsedMindMap = parseMindMapLine(line, tokens, activeMindMap);
      if (parsedMindMap) {
        if (!activeMindMap) {
          const startPos = resolvePosition(parsedMindMap.pos || "center");
          const mindMapActor = {
            shapeId: lineShapeId,
            shapeType: "mind",
            shapeCategory: "corporate",
            isMindMap: true,
            textLabel: "Mind Map",
            icon: "network",
            accent: "indigo",
            startPos: startPos,
            intro: "fade",
            motion: { hasMotion: false },
            title: "STATUTORY MIND MAP",
            nodes: parsedMindMap.nodes ? [...parsedMindMap.nodes] : []
          };
          currentScene.actors.push(mindMapActor);
          continue;
        } else {
          // Append nodes to activeMindMap
          if (parsedMindMap.nodes && parsedMindMap.nodes.length > 0) {
            activeMindMap.nodes.push(...parsedMindMap.nodes);
          }
          continue;
        }
      }

      // 2. Standard Shape instruction line using balanced tokens
      if (tokens.length >= 2 && line.toLowerCase().startsWith("shape")) {
        let shapeDialogue = "";
        const cleanTokens = [];

        for (let ti = 0; ti < tokens.length; ti++) {
          const tRaw = tokens[ti].trim();
          const tLow = tRaw.toLowerCase();
          const dMatch = tRaw.match(/^(?:dialogue|narration|speech)\s*:\s*["']?([\s\S]+?)["']?$/i);
          if (dMatch) {
            shapeDialogue = dMatch[1].trim();
            continue;
          }
          if (/^(?:dialogue|narration|speech)$/i.test(tLow) && ti + 1 < tokens.length) {
            shapeDialogue = tokens[ti + 1].trim().replace(/^["']|["']$/g, "");
            ti++;
            continue;
          }
          const idMatch = tRaw.match(/^id\s*:\s*(\w+)$/i);
          if (idMatch) {
            if (lineShapeId === null) lineShapeId = isNaN(idMatch[1]) ? idMatch[1] : parseInt(idMatch[1], 10);
            continue;
          }
          const hashMatch = tRaw.match(/^#(\d+)$/);
          if (hashMatch) {
            if (lineShapeId === null) lineShapeId = parseInt(hashMatch[1], 10);
            continue;
          }
          cleanTokens.push(tRaw);
        }

        // Check if second token is an identification number e.g. shape (man) (1) (Transferor: Rajesh)
        if (lineShapeId === null && cleanTokens.length >= 3 && /^\d+$/.test(cleanTokens[1].trim())) {
          lineShapeId = parseInt(cleanTokens[1].trim(), 10);
          cleanTokens.splice(1, 1);
        }

        const shapeType = (cleanTokens[0] || "").trim();
        const textLabel = (cleanTokens[1] || "").trim();
        const posStr = (cleanTokens[2] || "center").trim();
        let introStr = (cleanTokens[3] || "fade").trim();
        let motionStr = (cleanTokens[4] || "stay").trim();
        if (cleanTokens.length === 4 && (introStr.toLowerCase().startsWith("movement") || introStr.toLowerCase().startsWith("move") || introStr.toLowerCase().includes("after") || introStr.toLowerCase().includes("to "))) {
          motionStr = introStr;
          introStr = "fade";
        }

        const startPos = resolvePosition(posStr);
        const motionData = parseMotion(motionStr, startPos);
        const meta = resolveShapeMeta(shapeType);

        const actor = {
          shapeId: lineShapeId,
          popup: linePopupData,
          shapeType,
          shapeCategory: meta.category,
          textLabel,
          icon: meta.icon,
          accent: meta.accent,
          category: meta.label,
          overlay: meta.overlay,
          customRenderer: meta.custom,
          startPos,
          intro: introStr.toLowerCase(),
          motion: motionData,
          dialogue: shapeDialogue
        };

        currentScene.actors.push(actor);
        if (shapeDialogue) {
          if (!currentScene.shapeDialogues) currentScene.shapeDialogues = [];
          currentScene.shapeDialogues.push(shapeDialogue);
        }
        continue;
      }

      // 3. Fallback Regex for single-line shapes
      const m = line.match(shapeRegex);
      if (m) {
        const shapeType = m[1].trim();
        const textLabel = m[2].trim();
        const posStr = m[3].trim();
        const introStr = m[4].trim();
        const motionStr = (m[5] || "stay").trim();

        const startPos = resolvePosition(posStr);
        const motionData = parseMotion(motionStr, startPos);
        const meta = resolveShapeMeta(shapeType);

        currentScene.actors.push({
          shapeId: lineShapeId,
          popup: linePopupData,
          shapeType,
          shapeCategory: meta.category,
          textLabel,
          icon: meta.icon,
          accent: meta.accent,
          category: meta.label,
          overlay: meta.overlay,
          customRenderer: meta.custom,
          startPos,
          intro: introStr.toLowerCase(),
          motion: motionData
        });
      }
    }

    if (!currentScene.dialogue && currentScene.shapeDialogues && currentScene.shapeDialogues.length > 0) {
      currentScene.dialogue = currentScene.shapeDialogues.join(" ");
    }
    if (currentScene.actors.length > 0 || currentScene.dialogue) {
      scenes.push(currentScene);
    }

    if (scenes.length === 0) return null;

    // Convert scenes into player presentation payload
    return {
      act_name: "Custom Prompt-to-Animation Script Studio",
      section_code: "Script Studio",
      core_doctrine: "Dynamic Shape & Motion Choreography",
      story_summary: "Live choreographed animation generated from custom natural text prompts.",
      hide_chrome: true,
      scenes: scenes.map((sc, sIdx) => {
        // Enforce slide exclusivity: if a heading exists on this scene, keep ONLY the heading actor
        const isHeadingScene = sc.hasHeading || sc.actors.some(a => a.isHeading);
        if (isHeadingScene) {
          sc.actors = sc.actors.filter(a => a.isHeading).slice(0, 1);
        } else {
          // Sort actors on this slide by explicit numeric shapeId if any are present
          if (sc.actors.some(a => a.shapeId !== undefined && a.shapeId !== null)) {
            sc.actors.sort((a, b) => {
              const idA = (a.shapeId !== undefined && a.shapeId !== null && !isNaN(a.shapeId)) ? Number(a.shapeId) : 9999;
              const idB = (b.shapeId !== undefined && b.shapeId !== null && !isNaN(b.shapeId)) ? Number(b.shapeId) : 9999;
              return idA - idB;
            });
          }

          // Resolve Pop-Up Origin coordinates based on anchor shape
          sc.actors.forEach(actor => {
            if (actor.popup && actor.popup.anchorId !== undefined && actor.popup.anchorId !== null) {
              const anchorActor = sc.actors.find(a => String(a.shapeId) === String(actor.popup.anchorId) && a !== actor);
              if (anchorActor && anchorActor.startPos) {
                const anchorX = anchorActor.startPos.x;
                const anchorY = anchorActor.startPos.y;
                const dir = (actor.popup.direction || "right").toLowerCase();
                let fromX = anchorX + 90;
                let fromY = anchorY;

                if (dir === "left") {
                  fromX = anchorX - 90;
                  fromY = anchorY;
                } else if (dir === "top" || dir === "above" || dir === "up") {
                  fromX = anchorX;
                  fromY = anchorY - 80;
                } else if (dir === "bottom" || dir === "below" || dir === "down") {
                  fromX = anchorX;
                  fromY = anchorY + 80;
                } else {
                  // "right"
                  fromX = anchorX + 90;
                  fromY = anchorY;
                }

                actor.popup.from = { x: fromX, y: fromY };
                actor.popup.to = { ...(actor.startPos || { x: 640, y: 360 }) };
                actor.popup.durationMs = 950;
                actor.popup.active = true;
              }
            }
          });
        }

        let durationMs;
        let voiceCues = [];
        if (isHeadingScene) {
          const headingActor = sc.actors[0];
          const words = sc.dialogue ? sc.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
          const speechNeededMs = words > 0 ? (Math.ceil((words * 360) / 0.70) + 1200) : 0;
          const defaultHeadingDur = Math.max(6500, speechNeededMs);
          durationMs = (headingActor && headingActor.slideDurationMs) ? headingActor.slideDurationMs : defaultHeadingDur;
          if (headingActor && headingActor.dialogue) {
            voiceCues.push({
              id: `s${sIdx}_heading`,
              startMs: headingActor.startMs || 0,
              dialogue: headingActor.dialogue,
              label: headingActor.titleText || "Heading"
            });
          }
        } else {
          // Compute sequential actor timeline:
          // In a slide, don't show every shape at once!
          // Next shape only appears after the dialogue voice of previous shape is complete.
          let runningMs = 250;
          sc.actors.forEach((actor, aIdx) => {
            actor.startMs = runningMs;

            if (actor.isChecklist) {
              computeChecklistTimeline(actor);
              actor.endMs = actor.totalTimelineMs || (actor.startMs + 3500);
              runningMs = actor.endMs + 350;
              return;
            }

            if (actor.isList) {
              computeListTimeline(actor);
              actor.endMs = actor.totalTimelineMs || (actor.startMs + 3500);
              runningMs = actor.endMs + 350;
              return;
            }

            if (actor.isMindMap) {
              computeMindMapTimeline(actor);
              actor.endMs = actor.totalTimelineMs || (actor.startMs + 3500);
              runningMs = actor.endMs + 350;
              return;
            }

            if (actor.isCalculation) {
              computeCalculationMultipleTimeline(actor);
              actor.endMs = actor.totalTimelineMs || (actor.startMs + 3500);
              runningMs = actor.endMs + 350;
              return;
            }

            if (actor.isCalculationSingle) {
              computeCalculationSingleTimeline(actor);
              actor.endMs = (actor.formulaData && actor.formulaData.maxIntroMs ? actor.formulaData.maxIntroMs + 1200 : actor.startMs + 3500);
              runningMs = actor.endMs + 350;
              return;
            }

            // Regular shape / actor
            const words = actor.dialogue ? actor.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
            const speechMs = words > 0 ? Math.max(2600, Math.ceil(words * 400) + 800) : (sc.dialogue ? 2400 : 1800);

            // Motion span relative to this actor's startMs
            let motionSpanMs = 0;
            if (actor.motion && actor.motion.hasMotion) {
              const motionDelay = (actor.motion.rawDelayMs !== undefined) ? actor.motion.rawDelayMs : 1000;
              const motionDur = (actor.motion.durationMs !== undefined) ? actor.motion.durationMs : 1500;
              actor.motion.startMs = actor.startMs + motionDelay;
              actor.motion.endMs = actor.motion.startMs + motionDur;
              motionSpanMs = motionDelay + motionDur + 400;
            }

            const activeSpan = Math.max(speechMs, motionSpanMs, 2200);
            actor.endMs = actor.startMs + activeSpan;
            runningMs = actor.endMs + 350; // brief breathing gap before next shape appears
          });

          // Build unified chronological voice cues list for this scene
          sc.actors.forEach((actor, aIdx) => {
            if (actor.isList) {
              if (actor.items) {
                actor.items.forEach((it, iIdx) => {
                  if (it.dialogue) {
                    voiceCues.push({
                      id: `s${sIdx}_a${aIdx}_list_item_${iIdx}`,
                      startMs: it.startMs,
                      dialogue: it.dialogue,
                      label: it.text
                    });
                  }
                });
              }
            } else if (actor.isChecklist) {
              if (actor.items) {
                actor.items.forEach((it, iIdx) => {
                  if (it.dialogue) {
                    voiceCues.push({
                      id: `s${sIdx}_a${aIdx}_item_${iIdx}`,
                      startMs: it.startMs,
                      dialogue: it.dialogue,
                      label: it.text
                    });
                  }
                });
              }
              if (actor.gateItem && actor.gateItem.dialogue) {
                voiceCues.push({
                  id: `s${sIdx}_a${aIdx}_gate`,
                  startMs: actor.gateItem.startMs,
                  dialogue: actor.gateItem.dialogue,
                  label: actor.gateItem.text
                });
              }
            } else if (actor.isMindMap) {
              if (actor.nodes) {
                actor.nodes.forEach((node, nIdx) => {
                  if (node.dialogue) {
                    voiceCues.push({
                      id: `s${sIdx}_a${aIdx}_node_${node.code || nIdx}`,
                      startMs: node.startMs,
                      dialogue: node.dialogue,
                      label: node.text
                    });
                  }
                });
              }
            } else if (actor.isCalculation) {
              if (actor.items) {
                actor.items.forEach((it, iIdx) => {
                  if (it.dialogue) {
                    voiceCues.push({
                      id: `s${sIdx}_a${aIdx}_row_${iIdx}`,
                      startMs: it.startMs,
                      dialogue: it.dialogue,
                      label: it.text
                    });
                  }
                });
              }
            } else if (actor.isCalculationSingle) {
              if (actor.formulaData && actor.formulaData.terms) {
                actor.formulaData.terms.forEach((term, tIdx) => {
                  if (term.dialogue) {
                    voiceCues.push({
                      id: `s${sIdx}_a${aIdx}_term_${term.id !== undefined ? term.id : tIdx}`,
                      startMs: term.introTimeMs,
                      dialogue: term.dialogue,
                      label: term.text
                    });
                  }
                });
              }
            } else {
              if (actor.dialogue) {
                voiceCues.push({
                  id: `s${sIdx}_a${aIdx}`,
                  startMs: actor.startMs || 0,
                  dialogue: actor.dialogue,
                  label: actor.textLabel || actor.titleText || `Actor ${aIdx}`
                });
              }
            }
          });

          // Sort voice cues chronologically
          voiceCues.sort((a, b) => a.startMs - b.startMs);

          const maxActorEndMs = sc.actors.reduce((acc, a) => {
            const end = a.endMs || (a.motion && a.motion.hasMotion ? a.motion.endMs : 3000);
            return Math.max(acc, end);
          }, 3000);

          const words = sc.dialogue ? sc.dialogue.trim().split(/\s+/).filter(Boolean).length : 0;
          const speechNeededMs = words > 0 ? (Math.ceil((words * 360) / 0.65) + 1200) : 0;

          // Accommodate calculation staggered timing, actor motion, speech needed, and settle hold
          const requiredActiveMs = Math.max(maxActorEndMs + 800, runningMs, 3200);
          durationMs = Math.max(5000, Math.ceil(requiredActiveMs / 0.65), speechNeededMs);
        }

        return {
          id: sIdx + 1,
          tab_title: sc.tab_title || `Scene ${sIdx + 1}`,
          hide_chrome: true,
          layout_archetype: "layout_full_canvas",
          layout_payload: {},
          dialogue: sc.dialogue || "",
          duration_ms: durationMs,
          lines: [
            {
              line_num: 1,
              sentence: sc.dialogue || "",
              line_title: "",
              duration_ms: durationMs,
              action_type: "custom_script_engine",
              action_payload: {
                actors: sc.actors,
                voiceCues: voiceCues,
                duration_ms: durationMs
              }
            }
          ]
        };
      })
    };
  }

  /* ==========================================================================
     PICTORIAL VECTOR SILHOUETTE & CHARACTER AVATAR RENDERERS
     Pure Canvas 2D Vector Silhouettes (Man, Woman, Car, Clothes, Buildings, etc.)
     ========================================================================== */

  /**
   * Floating label chip underneath the pictorial silhouette
   */
  function drawFloatingLabelChip(ctx, text, category, accentTheme, themeColors) {
    if (!text) return;
    ctx.save();
    ctx.translate(0, 36);

    ctx.font = "700 12px 'Plus Jakarta Sans', sans-serif";
    const rawW = ctx.measureText(text).width;

    // Check if it fits on a single line comfortably (up to 240px wide)
    const maxSingleLineW = 230;
    let lines = [];

    if (rawW <= maxSingleLineW) {
      lines = [text];
    } else {
      // Split into 2 lines cleanly using word wrap
      const words = text.trim().split(/\s+/);
      let cur = "";
      for (let i = 0; i < words.length; i++) {
        const test = cur ? `${cur} ${words[i]}` : words[i];
        if (ctx.measureText(test).width <= maxSingleLineW) {
          cur = test;
        } else {
          if (cur) lines.push(cur);
          cur = words[i];
          if (lines.length === 1) {
            const remaining = words.slice(i).join(" ");
            lines.push(remaining);
            cur = "";
            break;
          }
        }
      }
      if (cur && lines.length < 2) {
        lines.push(cur);
      }
    }

    // Determine actual measured width of the lines
    let maxLineWidth = 0;
    lines.forEach(l => {
      const w = ctx.measureText(l).width;
      if (w > maxLineWidth) maxLineWidth = w;
    });

    const isMultiLine = lines.length > 1;
    const padH = 24;
    const chipW = Math.max(110, Math.min(300, maxLineWidth + padH));
    const lineHeight = 15;
    const chipH = isMultiLine ? 44 : 30;
    const chipX = -chipW / 2;
    const chipY = 0;

    // Drop shadow
    ctx.shadowColor = "rgba(15, 23, 42, 0.08)";
    ctx.shadowBlur = 8;
    ctx.shadowOffsetY = 3;

    // Container
    ctx.fillStyle = themeColors.bgCard || "#FFFFFF";
    ctx.strokeStyle = accentTheme.border || "#CBD5E1";
    ctx.lineWidth = 1.25;
    ctx.beginPath();
    ctx.roundRect(chipX, chipY, chipW, chipH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.shadowColor = "transparent";

    // Category / Role Tag on top of chip
    if (category) {
      const catText = category.toUpperCase();
      ctx.font = "800 8.5px 'JetBrains Mono', monospace";
      const catW = ctx.measureText(catText).width + 12;
      const catH = 14;
      const catX = -catW / 2;
      const catY = -7;

      ctx.fillStyle = accentTheme.light || "#EEF2FF";
      ctx.strokeStyle = accentTheme.border || "#C7D2FE";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(catX, catY, catW, catH, 7);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = accentTheme.main || "#4F46E5";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(catText, 0, 0);
    }

    // Main Text Label - Vertically and Horizontally Centered
    ctx.font = "700 12px 'Plus Jakarta Sans', sans-serif";
    ctx.fillStyle = themeColors.textPrimary || "#0F172A";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    if (isMultiLine) {
      const startY = chipY + (chipH / 2) - (lineHeight / 2) + 1;
      ctx.fillText(lines[0], 0, startY);
      ctx.fillText(lines[1], 0, startY + lineHeight);
    } else {
      ctx.fillText(lines[0], 0, chipY + chipH / 2 + 1);
    }

    ctx.restore();
  }

  /**
   * Character Silhouette: Man / Professional Male Avatar
   */
  function drawManShape(ctx, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    const r = 30;
    // Glow / shadow
    ctx.shadowColor = "rgba(15, 23, 42, 0.12)";
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 4;

    const bgGrad = ctx.createLinearGradient(0, -r, 0, r);
    bgGrad.addColorStop(0, accentTheme.light || "#EEF2FF");
    bgGrad.addColorStop(1, "#FFFFFF");
    ctx.fillStyle = bgGrad;
    ctx.strokeStyle = accentTheme.main || "#4F46E5";
    ctx.lineWidth = 2.5;

    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.shadowColor = "transparent";

    // Clip to circle boundary
    ctx.save();
    ctx.beginPath();
    ctx.arc(0, 0, r - 1.5, 0, Math.PI * 2);
    ctx.clip();

    // 1. Torso / Shoulders (Dark Navy Suit)
    ctx.fillStyle = accentTheme.dark || "#1E293B";
    ctx.beginPath();
    ctx.moveTo(-24, 30);
    ctx.quadraticCurveTo(-22, 10, -9, 8);
    ctx.lineTo(9, 8);
    ctx.quadraticCurveTo(22, 10, 24, 30);
    ctx.closePath();
    ctx.fill();

    // 2. Collar & Tie
    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.moveTo(-7, 8);
    ctx.lineTo(0, 18);
    ctx.lineTo(7, 8);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = accentTheme.main || "#4F46E5";
    ctx.beginPath();
    ctx.moveTo(-3, 11);
    ctx.lineTo(3, 11);
    ctx.lineTo(4, 23);
    ctx.lineTo(0, 27);
    ctx.lineTo(-4, 23);
    ctx.closePath();
    ctx.fill();

    // Suit Lapel outlines
    ctx.strokeStyle = accentTheme.border || "#94A3B8";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(-9, 8); ctx.lineTo(-3, 21);
    ctx.moveTo(9, 8); ctx.lineTo(3, 21);
    ctx.stroke();

    // 3. Neck
    ctx.fillStyle = "#FBD5BD";
    ctx.fillRect(-4, 1, 8, 8);

    // 4. Head Oval
    ctx.beginPath();
    ctx.ellipse(0, -5, 9, 11, 0, 0, Math.PI * 2);
    ctx.fill();

    // 5. Stylized Male Hair Profile
    ctx.fillStyle = "#334155";
    ctx.beginPath();
    ctx.moveTo(-10, -5);
    ctx.quadraticCurveTo(-10, -17, 0, -17);
    ctx.quadraticCurveTo(10, -17, 10, -4);
    ctx.quadraticCurveTo(8, -12, 3, -13);
    ctx.quadraticCurveTo(-5, -14, -10, -5);
    ctx.closePath();
    ctx.fill();

    ctx.restore(); // restore clip
    ctx.restore();
  }

  /**
   * Character Silhouette: Woman / Professional Female Avatar
   */
  function drawWomanShape(ctx, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    const r = 30;
    ctx.shadowColor = "rgba(15, 23, 42, 0.12)";
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 4;

    const bgGrad = ctx.createLinearGradient(0, -r, 0, r);
    bgGrad.addColorStop(0, accentTheme.light || "#F5F3FF");
    bgGrad.addColorStop(1, "#FFFFFF");
    ctx.fillStyle = bgGrad;
    ctx.strokeStyle = accentTheme.main || "#7C3AED";
    ctx.lineWidth = 2.5;

    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.shadowColor = "transparent";

    // Clip to circle boundary
    ctx.save();
    ctx.beginPath();
    ctx.arc(0, 0, r - 1.5, 0, Math.PI * 2);
    ctx.clip();

    // 1. Hair Background Silhouette
    ctx.fillStyle = "#451A03";
    ctx.beginPath();
    ctx.arc(0, -6, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(-12, -6, 24, 22);

    // 2. Torso / Professional Blazer
    ctx.fillStyle = accentTheme.dark || "#581C87";
    ctx.beginPath();
    ctx.moveTo(-22, 30);
    ctx.quadraticCurveTo(-20, 11, -8, 9);
    ctx.lineTo(8, 9);
    ctx.quadraticCurveTo(20, 11, 22, 30);
    ctx.closePath();
    ctx.fill();

    // Blouse Neckline
    ctx.fillStyle = accentTheme.light || "#EDE9FE";
    ctx.beginPath();
    ctx.moveTo(-6, 9);
    ctx.quadraticCurveTo(0, 19, 6, 9);
    ctx.closePath();
    ctx.fill();

    // Gold Pendant Necklace
    ctx.strokeStyle = "#F59E0B";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 9, 5, 0.2, Math.PI - 0.2);
    ctx.stroke();
    ctx.fillStyle = "#F59E0B";
    ctx.beginPath();
    ctx.arc(0, 14, 1.5, 0, Math.PI * 2);
    ctx.fill();

    // 3. Neck
    ctx.fillStyle = "#FDE2D2";
    ctx.fillRect(-3.5, 2, 7, 8);

    // 4. Head Oval
    ctx.beginPath();
    ctx.ellipse(0, -5, 8.5, 10.5, 0, 0, Math.PI * 2);
    ctx.fill();

    // 5. Stylized Front Hair with side locks
    ctx.fillStyle = "#451A03";
    ctx.beginPath();
    ctx.moveTo(-9, -5);
    ctx.quadraticCurveTo(-9, -16, 0, -16);
    ctx.quadraticCurveTo(9, -16, 9, -5);
    ctx.quadraticCurveTo(6, -12, 2, -13);
    ctx.quadraticCurveTo(-4, -14, -9, -5);
    ctx.closePath();
    ctx.fill();

    // Side hair curls falling down
    ctx.beginPath();
    ctx.moveTo(-9, -5);
    ctx.quadraticCurveTo(-11, 4, -7, 10);
    ctx.lineTo(-6, 10);
    ctx.quadraticCurveTo(-9, 3, -7, -5);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(9, -5);
    ctx.quadraticCurveTo(11, 4, 7, 10);
    ctx.lineTo(6, 10);
    ctx.quadraticCurveTo(9, 3, 7, -5);
    ctx.closePath();
    ctx.fill();

    ctx.restore(); // restore clip
    ctx.restore();
  }

  /**
   * Vehicle Silhouette: Sleek Passenger Car
   */
  function drawCarShape(ctx, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -10);

    // Ground Contact Shadow
    ctx.fillStyle = "rgba(15, 23, 42, 0.15)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 42, 4.5, 0, 0, Math.PI * 2);
    ctx.fill();

    const carColor = accentTheme.main || "#0284C7";
    const carDark = accentTheme.dark || "#0369A1";

    // 1. Car Body Contour
    ctx.beginPath();
    ctx.moveTo(-38, 10);
    ctx.lineTo(-39, 4);
    ctx.quadraticCurveTo(-37, -1, -26, -2);
    ctx.quadraticCurveTo(-14, -4, -8, -17);
    ctx.lineTo(14, -17);
    ctx.quadraticCurveTo(24, -16, 32, -2);
    ctx.lineTo(39, 0);
    ctx.quadraticCurveTo(42, 3, 41, 10);
    ctx.lineTo(31, 10);
    ctx.arc(22, 10, 9, 0, Math.PI, true);
    ctx.lineTo(-13, 10);
    ctx.arc(-22, 10, 9, 0, Math.PI, true);
    ctx.lineTo(-38, 10);
    ctx.closePath();

    const bodyGrad = ctx.createLinearGradient(0, -17, 0, 10);
    bodyGrad.addColorStop(0, carColor);
    bodyGrad.addColorStop(1, carDark);
    ctx.fillStyle = bodyGrad;
    ctx.fill();
    ctx.strokeStyle = carDark;
    ctx.lineWidth = 1.8;
    ctx.stroke();

    // 2. Windows with light reflection
    ctx.fillStyle = "#E0F2FE";
    ctx.strokeStyle = "#94A3B8";
    ctx.lineWidth = 1;

    // Front Window
    ctx.beginPath();
    ctx.moveTo(-6, -15);
    ctx.lineTo(-16, -4);
    ctx.lineTo(-2, -4);
    ctx.lineTo(-2, -15);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Rear Window
    ctx.beginPath();
    ctx.moveTo(1, -15);
    ctx.lineTo(1, -4);
    ctx.lineTo(26, -4);
    ctx.lineTo(13, -15);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // B-Pillar
    ctx.fillStyle = carDark;
    ctx.fillRect(-2, -15, 3, 11);

    // 3. Headlight & Taillight
    ctx.fillStyle = "#FDE047";
    ctx.fillRect(-38, 3, 4, 3);

    ctx.fillStyle = "#EF4444";
    ctx.fillRect(38, 2, 3, 4);

    // Door crease line & handles
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(-16, 2);
    ctx.lineTo(26, 2);
    ctx.stroke();

    ctx.fillStyle = "#CBD5E1";
    ctx.fillRect(-6, 0, 4, 1.5);
    ctx.fillRect(10, 0, 4, 1.5);

    // 4. Wheels
    function drawCarWheel(wx, wy) {
      ctx.fillStyle = "#1E293B";
      ctx.beginPath();
      ctx.arc(wx, wy, 8, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#E2E8F0";
      ctx.strokeStyle = "#64748B";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(wx, wy, 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#334155";
      ctx.beginPath();
      ctx.arc(wx, wy, 1.5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawCarWheel(-22, 10);
    drawCarWheel(22, 10);

    ctx.restore();
  }

  /**
   * Heavy Freight Truck Silhouette
   */
  function drawTruckShape(ctx, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -10);

    // Ground Shadow
    ctx.fillStyle = "rgba(15, 23, 42, 0.15)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 48, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Cargo Container Body
    const cargoGrad = ctx.createLinearGradient(0, -18, 0, 10);
    cargoGrad.addColorStop(0, accentTheme.light || "#EEF2FF");
    cargoGrad.addColorStop(1, accentTheme.border || "#C7D2FE");
    ctx.fillStyle = cargoGrad;
    ctx.strokeStyle = accentTheme.main || "#4F46E5";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.roundRect(-44, -18, 54, 28, [4, 4, 0, 0]);
    ctx.fill();
    ctx.stroke();

    // Vertical ribbed container lines
    ctx.strokeStyle = "rgba(79, 70, 229, 0.25)";
    ctx.lineWidth = 1.2;
    for (let x = -36; x < 6; x += 10) {
      ctx.beginPath();
      ctx.moveTo(x, -16);
      ctx.lineTo(x, 8);
      ctx.stroke();
    }

    // Cab (Cabin)
    ctx.fillStyle = accentTheme.main || "#4F46E5";
    ctx.strokeStyle = accentTheme.dark || "#3730A3";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(10, 10);
    ctx.lineTo(10, -10);
    ctx.lineTo(26, -10);
    ctx.lineTo(38, -2);
    ctx.lineTo(42, 3);
    ctx.lineTo(42, 10);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Cab Windshield
    ctx.fillStyle = "#E0F2FE";
    ctx.beginPath();
    ctx.moveTo(25, -8);
    ctx.lineTo(35, -2);
    ctx.lineTo(25, -2);
    ctx.closePath();
    ctx.fill();

    // Headlight
    ctx.fillStyle = "#FDE047";
    ctx.fillRect(40, 4, 3, 4);

    // Wheels
    function drawTruckWheel(wx, wy) {
      ctx.fillStyle = "#1E293B";
      ctx.beginPath();
      ctx.arc(wx, wy, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#CBD5E1";
      ctx.beginPath();
      ctx.arc(wx, wy, 3.5, 0, Math.PI * 2);
      ctx.fill();
    }

    drawTruckWheel(-32, 11);
    drawTruckWheel(-18, 11);
    drawTruckWheel(28, 11);

    ctx.restore();
  }

  /**
   * Clothes & Textiles Silhouette: Tailored Suit Blazer or Folded Fabric Drape
   */
  function drawClothesShape(ctx, subType, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    const isFabric = subType.includes("cloth") || subType.includes("fabric") || subType.includes("textile");

    if (isFabric) {
      // Folded Textile Bolt Roll with hanging cloth drape
      const mainCol = accentTheme.main || "#D97706";
      const lightCol = accentTheme.light || "#FEF3C7";
      const darkCol = accentTheme.dark || "#92400E";

      // 1. Spool / Roll of Cloth at top
      ctx.fillStyle = lightCol;
      ctx.strokeStyle = mainCol;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.ellipse(0, -16, 26, 8, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = darkCol;
      ctx.beginPath();
      ctx.ellipse(-14, -16, 4, 6, 0, 0, Math.PI * 2);
      ctx.fill();

      // 2. Cascading Fabric Drape
      const drapeGrad = ctx.createLinearGradient(0, -16, 0, 20);
      drapeGrad.addColorStop(0, mainCol);
      drapeGrad.addColorStop(1, darkCol);
      ctx.fillStyle = drapeGrad;
      ctx.strokeStyle = darkCol;
      ctx.beginPath();
      ctx.moveTo(-26, -16);
      ctx.quadraticCurveTo(-28, 6, -22, 20);
      ctx.quadraticCurveTo(-10, 24, 0, 18);
      ctx.quadraticCurveTo(10, 22, 22, 20);
      ctx.quadraticCurveTo(28, 4, 26, -16);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Woven Texture Lines
      ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
      ctx.lineWidth = 1;
      ctx.setLineDash([3, 3]);
      for (let y = -8; y <= 12; y += 6) {
        ctx.beginPath();
        ctx.moveTo(-22, y);
        ctx.lineTo(22, y);
        ctx.stroke();
      }
      ctx.setLineDash([]);

      // Selvedge golden border
      ctx.strokeStyle = "#F59E0B";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(-22, 20);
      ctx.quadraticCurveTo(-10, 24, 0, 18);
      ctx.quadraticCurveTo(10, 22, 22, 20);
      ctx.stroke();

    } else {
      // Tailored Suit Coat / Garment
      const mainCol = accentTheme.main || "#059669";
      const darkCol = accentTheme.dark || "#065F46";

      // Hanger hook
      ctx.strokeStyle = "#94A3B8";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, -22, 4, Math.PI * 0.8, Math.PI * 2.2);
      ctx.lineTo(0, -16);
      ctx.stroke();

      // Coat Silhouette
      ctx.fillStyle = mainCol;
      ctx.strokeStyle = darkCol;
      ctx.lineWidth = 1.8;

      ctx.beginPath();
      ctx.moveTo(-24, -14);
      ctx.lineTo(-28, 12);
      ctx.lineTo(-20, 12);
      ctx.lineTo(-16, 2);
      ctx.lineTo(-18, 20);
      ctx.lineTo(18, 20);
      ctx.lineTo(16, 2);
      ctx.lineTo(20, 12);
      ctx.lineTo(28, 12);
      ctx.lineTo(24, -14);
      ctx.lineTo(10, -16);
      ctx.lineTo(0, -10);
      ctx.lineTo(-10, -16);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Lapels
      ctx.fillStyle = darkCol;
      ctx.beginPath();
      ctx.moveTo(-10, -16); ctx.lineTo(-2, 4); ctx.lineTo(0, 4); ctx.lineTo(0, -10); ctx.closePath(); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(10, -16); ctx.lineTo(2, 4); ctx.lineTo(0, 4); ctx.lineTo(0, -10); ctx.closePath(); ctx.fill();

      // Shirt / Tie peek
      ctx.fillStyle = "#FFFFFF";
      ctx.beginPath();
      ctx.moveTo(-4, -12); ctx.lineTo(4, -12); ctx.lineTo(0, -2); ctx.closePath(); ctx.fill();

      // Gold Buttons
      ctx.fillStyle = "#F59E0B";
      ctx.beginPath();
      ctx.arc(0, 8, 1.8, 0, Math.PI * 2);
      ctx.arc(0, 14, 1.8, 0, Math.PI * 2);
      ctx.fill();

      // Pocket welt
      ctx.strokeStyle = darkCol;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(7, 6); ctx.lineTo(13, 6); ctx.stroke();
    }

    ctx.restore();
  }

  /**
   * Building Silhouette: Factory, Court, Store, or Office Tower
   */
  function drawBuildingShape(ctx, subType, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    const isFactory = subType.includes("factory") || subType.includes("repair") || subType.includes("auto");
    const isCourt = subType.includes("court");
    const isStore = subType.includes("store") || subType.includes("shop");

    if (isFactory) {
      // Sawtooth Industrial Factory with Chimney
      const mainCol = accentTheme.main || "#4F46E5";
      const lightCol = accentTheme.light || "#EEF2FF";

      // Chimney with Smoke
      ctx.fillStyle = "#64748B";
      ctx.fillRect(16, -26, 8, 16);
      ctx.fillStyle = "rgba(203, 213, 225, 0.7)";
      ctx.beginPath();
      ctx.arc(18, -30, 4, 0, Math.PI * 2);
      ctx.arc(23, -33, 5, 0, Math.PI * 2);
      ctx.arc(28, -36, 6, 0, Math.PI * 2);
      ctx.fill();

      // Factory Body with Sawtooth Roof
      ctx.fillStyle = lightCol;
      ctx.strokeStyle = mainCol;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(-28, 18);
      ctx.lineTo(-28, -4);
      ctx.lineTo(-14, -16);
      ctx.lineTo(-14, -4);
      ctx.lineTo(0, -16);
      ctx.lineTo(0, -4);
      ctx.lineTo(14, -16);
      ctx.lineTo(14, -4);
      ctx.lineTo(28, -4);
      ctx.lineTo(28, 18);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Shutter Door
      ctx.fillStyle = mainCol;
      ctx.fillRect(-10, 2, 20, 16);
      ctx.strokeStyle = lightCol;
      ctx.lineWidth = 1;
      for (let y = 6; y < 18; y += 4) {
        ctx.beginPath(); ctx.moveTo(-10, y); ctx.lineTo(10, y); ctx.stroke();
      }

      // Windows
      ctx.fillStyle = "#38BDF8";
      ctx.fillRect(-22, 2, 8, 8);
      ctx.fillRect(14, 2, 8, 8);

    } else if (isCourt) {
      // Classical Courthouse Pediment & Pillars
      const colColor = accentTheme.main || "#D97706";
      ctx.fillStyle = accentTheme.light || "#FEF3C7";
      ctx.strokeStyle = colColor;
      ctx.lineWidth = 1.8;

      ctx.beginPath();
      ctx.moveTo(-28, -8); ctx.lineTo(0, -22); ctx.lineTo(28, -8); ctx.closePath();
      ctx.fill(); ctx.stroke();

      if (window.ICONS) {
        window.ICONS.draw(ctx, "scale", 0, -13, 10, colColor, 1);
      }

      ctx.fillStyle = colColor;
      ctx.fillRect(-22, -6, 5, 18);
      ctx.fillRect(-9, -6, 5, 18);
      ctx.fillRect(4, -6, 5, 18);
      ctx.fillRect(17, -6, 5, 18);

      ctx.fillStyle = accentTheme.border || "#FDE68A";
      ctx.strokeStyle = colColor;
      ctx.lineWidth = 1.5;
      ctx.fillRect(-26, 12, 52, 4); ctx.strokeRect(-26, 12, 52, 4);
      ctx.fillRect(-30, 16, 60, 4); ctx.strokeRect(-30, 16, 60, 4);

    } else if (isStore) {
      // Commercial Store with Striped Awning
      const storeCol = accentTheme.main || "#059669";
      ctx.fillStyle = "#FFFFFF";
      ctx.strokeStyle = storeCol;
      ctx.lineWidth = 1.8;
      ctx.strokeRect(-24, -6, 48, 24);
      ctx.fillRect(-24, -6, 48, 24);

      // Striped Awning
      const stripeW = 9;
      for (let i = 0; i < 6; i++) {
        ctx.fillStyle = i % 2 === 0 ? storeCol : "#FFFFFF";
        ctx.fillRect(-27 + i * stripeW, -18, stripeW, 12);
        ctx.strokeStyle = storeCol;
        ctx.lineWidth = 1;
        ctx.strokeRect(-27 + i * stripeW, -18, stripeW, 12);
      }

      ctx.fillStyle = "#E0F2FE";
      ctx.fillRect(-20, 0, 16, 14);
      ctx.strokeStyle = "#94A3B8";
      ctx.strokeRect(-20, 0, 16, 14);

      ctx.fillStyle = storeCol;
      ctx.fillRect(4, 0, 14, 18);

    } else {
      // Modern Corporate Office Tower
      const mainCol = accentTheme.main || "#4F46E5";
      ctx.fillStyle = accentTheme.light || "#EEF2FF";
      ctx.strokeStyle = mainCol;
      ctx.lineWidth = 1.8;
      ctx.fillRect(-20, -22, 40, 40);
      ctx.strokeRect(-20, -22, 40, 40);

      // Antenna
      ctx.beginPath(); ctx.moveTo(0, -22); ctx.lineTo(0, -30); ctx.stroke();

      // Window Matrix
      ctx.fillStyle = mainCol;
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 3; c++) {
          ctx.fillRect(-15 + c * 11, -16 + r * 7, 7, 4);
        }
      }

      ctx.fillStyle = "#0F172A";
      ctx.fillRect(-6, 10, 12, 8);
    }

    ctx.restore();
  }

  /**
   * Goods / Cargo Box Silhouette
   */
  function drawGoodsBoxShape(ctx, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -12);

    const topCol = "#FDE68A";
    const frontCol = "#F59E0B";
    const sideCol = "#D97706";

    // 1. Top Face
    ctx.fillStyle = topCol;
    ctx.strokeStyle = sideCol;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(24, -8); ctx.lineTo(0, 2); ctx.lineTo(-24, -8); ctx.closePath();
    ctx.fill(); ctx.stroke();

    // 2. Left Front Face
    ctx.fillStyle = frontCol;
    ctx.beginPath();
    ctx.moveTo(-24, -8); ctx.lineTo(0, 2); ctx.lineTo(0, 24); ctx.lineTo(-24, 14); ctx.closePath();
    ctx.fill(); ctx.stroke();

    // 3. Right Front Face
    ctx.fillStyle = sideCol;
    ctx.beginPath();
    ctx.moveTo(0, 2); ctx.lineTo(24, -8); ctx.lineTo(24, 14); ctx.lineTo(0, 24); ctx.closePath();
    ctx.fill(); ctx.stroke();

    // Shipping Tape
    ctx.fillStyle = "rgba(180, 83, 9, 0.45)";
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(0, 2); ctx.lineTo(0, 24); ctx.stroke();

    // Fragile Stamp
    ctx.fillStyle = "#78350F";
    ctx.fillRect(-16, 2, 8, 5);

    ctx.restore();
  }

  /**
   * Legal & Financial Symbol Silhouette: Scale, Gavel, Deed, Money
   */
  function drawLegalSymbolShape(ctx, subType, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    if (subType.includes("gavel")) {
      const woodCol = accentTheme.main || "#B45309";
      const brassCol = "#FDE047";

      // Sound Block Base
      ctx.fillStyle = "#78350F";
      ctx.beginPath();
      ctx.ellipse(0, 16, 26, 7, 0, 0, Math.PI * 2);
      ctx.fill(); ctx.stroke();

      ctx.strokeStyle = "rgba(245, 158, 11, 0.4)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.ellipse(0, 16, 32, 9, 0, 0, Math.PI * 2);
      ctx.stroke();

      ctx.save();
      ctx.rotate(-0.35);

      ctx.fillStyle = woodCol;
      ctx.beginPath();
      ctx.roundRect(-16, -8, 32, 16, 3);
      ctx.fill(); ctx.stroke();

      ctx.fillStyle = brassCol;
      ctx.fillRect(-14, -8, 3, 16);
      ctx.fillRect(11, -8, 3, 16);

      ctx.fillStyle = woodCol;
      ctx.beginPath();
      ctx.roundRect(-3, 8, 6, 26, 3);
      ctx.fill(); ctx.stroke();

      ctx.restore();

    } else if (subType.includes("document") || subType.includes("contract") || subType.includes("deed")) {
      const bgCol = "#FFFFFF";
      const borderCol = accentTheme.border || "#CBD5E1";

      ctx.shadowColor = "rgba(15, 23, 42, 0.08)";
      ctx.shadowBlur = 8;
      ctx.shadowOffsetY = 3;

      ctx.fillStyle = bgCol;
      ctx.strokeStyle = borderCol;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.moveTo(-20, -22); ctx.lineTo(12, -22); ctx.lineTo(20, -14); ctx.lineTo(20, 20); ctx.lineTo(-20, 20); ctx.closePath();
      ctx.fill(); ctx.stroke();

      ctx.shadowColor = "transparent";

      ctx.fillStyle = "#E2E8F0";
      ctx.beginPath();
      ctx.moveTo(12, -22); ctx.lineTo(12, -14); ctx.lineTo(20, -14); ctx.closePath();
      ctx.fill(); ctx.stroke();

      ctx.strokeStyle = "#94A3B8";
      ctx.lineWidth = 1.5;
      for (let y = -10; y <= 8; y += 5) {
        ctx.beginPath(); ctx.moveTo(-14, y); ctx.lineTo(14, y); ctx.stroke();
      }

      ctx.fillStyle = "#DC2626";
      ctx.beginPath();
      ctx.arc(8, 14, 5, 0, Math.PI * 2);
      ctx.fill();

    } else if (subType.includes("money") || subType.includes("cash") || subType.includes("currency")) {
      const coinGrad = ctx.createRadialGradient(0, 0, 4, 0, 0, 24);
      coinGrad.addColorStop(0, "#FEF08A");
      coinGrad.addColorStop(1, "#EAB308");

      ctx.shadowColor = "rgba(234, 179, 8, 0.3)";
      ctx.shadowBlur = 10;

      ctx.fillStyle = coinGrad;
      ctx.strokeStyle = "#CA8A04";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(0, 0, 24, 0, Math.PI * 2);
      ctx.fill(); ctx.stroke();

      ctx.shadowColor = "transparent";

      ctx.strokeStyle = "#FEF9C3";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(0, 0, 20, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = "#713F12";
      ctx.font = "800 20px 'Plus Jakarta Sans', sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("₹", 0, 1);

    } else {
      const brassCol = accentTheme.main || "#4F46E5";
      ctx.strokeStyle = brassCol;
      ctx.lineWidth = 2;

      ctx.beginPath();
      ctx.moveTo(-16, 20); ctx.lineTo(16, 20);
      ctx.moveTo(0, 20); ctx.lineTo(0, -18);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-22, -14); ctx.lineTo(22, -14);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-22, -14); ctx.lineTo(-26, -2);
      ctx.moveTo(-22, -14); ctx.lineTo(-18, -2);
      ctx.stroke();
      ctx.beginPath(); ctx.arc(-22, -2, 6, 0, Math.PI); ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(22, -14); ctx.lineTo(18, -2);
      ctx.moveTo(22, -14); ctx.lineTo(26, -2);
      ctx.stroke();
      ctx.beginPath(); ctx.arc(22, -2, 6, 0, Math.PI); ctx.stroke();
    }

    ctx.restore();
  }

  /**
   * Generic Styled Badge with Icon
   */
  function drawGenericBadgeShape(ctx, iconName, accentTheme, themeColors) {
    ctx.save();
    ctx.translate(0, -14);

    const r = 28;
    ctx.shadowColor = "rgba(15, 23, 42, 0.1)";
    ctx.shadowBlur = 8;
    ctx.shadowOffsetY = 3;

    ctx.fillStyle = accentTheme.light || "#EEF2FF";
    ctx.strokeStyle = accentTheme.main || "#4F46E5";
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.shadowColor = "transparent";

    if (window.ICONS) {
      window.ICONS.draw(ctx, iconName || "package", 0, 0, 26, accentTheme.main, 1.8);
    }

    ctx.restore();
  }

  /**
   * Vector Sign Badge Renderer (+, -, =, ×, ÷) with vivid 3D gradient theme colors and drop shadow
   */
  function drawSignBadge(ctx, signStr, signType, cx, cy, r, scale = 1.0) {
    ctx.save();
    ctx.translate(cx, cy);
    if (scale !== 1.0) {
      ctx.scale(scale, scale);
    }

    let gradTop = "#6366F1";
    let gradBot = "#4338CA";
    let shadowCol = "rgba(79, 70, 229, 0.4)";
    let signChar = signStr || "+";

    if (signChar === "+" || signType === "add") {
      gradTop = "#34D399";
      gradBot = "#059669";
      shadowCol = "rgba(16, 185, 129, 0.45)";
      signChar = "+";
    } else if (signChar === "−" || signChar === "-" || signType === "deduct") {
      gradTop = "#F87171";
      gradBot = "#DC2626";
      shadowCol = "rgba(239, 68, 68, 0.45)";
      signChar = "−";
    } else if (signChar === "=" || signType === "total") {
      gradTop = "#818CF8";
      gradBot = "#4F46E5";
      shadowCol = "rgba(99, 102, 241, 0.5)";
      signChar = "=";
    } else if (signChar === "×" || signChar === "*" || signChar === "x" || signType === "multiply") {
      gradTop = "#FBBF24";
      gradBot = "#D97706";
      shadowCol = "rgba(245, 158, 11, 0.45)";
      signChar = "×";
    } else if (signChar === "÷" || signChar === "/" || signType === "divide") {
      gradTop = "#A78BFA";
      gradBot = "#7C3AED";
      shadowCol = "rgba(139, 92, 246, 0.45)";
      signChar = "÷";
    }

    // Outer subtle shadow for 3D depth
    ctx.shadowColor = shadowCol;
    ctx.shadowBlur = 6;
    ctx.shadowOffsetY = 2;

    const grad = ctx.createLinearGradient(0, -r, 0, r);
    grad.addColorStop(0, gradTop);
    grad.addColorStop(1, gradBot);

    // Outer circle
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();

    // Subtle inner highlight ring
    ctx.shadowColor = "transparent";
    ctx.strokeStyle = "rgba(255, 255, 255, 0.45)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, r - 0.75, 0, Math.PI * 2);
    ctx.stroke();

    // White glyph with crisp clarity
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "800 14px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const textOffsetY = (signChar === "−" || signChar === "=") ? -0.5 : 0.5;
    ctx.fillText(signChar, 0, textOffsetY);

    ctx.restore();
  }

  /**
   * Renders the Calculation Multiple Shape:
   * Executive multi-layer fintech card with vibrant top gradient ribbon,
   * color-coded row containers (+ emerald, - crimson, = executive midnight indigo),
   * live counting odometer roll, and pixel-perfect statutory double underline.
   */
  function drawCalculationMultipleShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    if (!actor.totalTimelineMs) {
      computeCalculationMultipleTimeline(actor);
    }
    const items = actor.items || [];
    const n = items.length;
    if (n === 0) return;

    const rowH = 50;
    const rowGap = 7;
    const headH = 50;
    const padTop = 12;
    const padB = 14;
    const cardH = headH + padTop + (n * rowH) + ((n - 1) * rowGap) + padB;

    // Measure maximum text width for dynamic card sizing
    ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
    let maxTextW = 180;
    items.forEach(it => {
      const w = ctx.measureText(it.text || "").width;
      if (w > maxTextW) maxTextW = w;
    });

    const cardW = Math.max(510, Math.min(640, maxTextW + 280));

    // Clamp coordinates to stay completely within the 1280x720 canvas with 36px margin
    const STAGE_W = 1280;
    const STAGE_H = 720;
    const margin = 36;

    let cx = actor.startPos.x;
    let cy = actor.startPos.y;

    if (cx - cardW / 2 < margin) {
      cx = margin + cardW / 2;
    } else if (cx + cardW / 2 > STAGE_W - margin) {
      cx = STAGE_W - margin - cardW / 2;
    }

    if (cy - cardH / 2 < margin) {
      cy = margin + cardH / 2;
    } else if (cy + cardH / 2 > STAGE_H - margin) {
      cy = STAGE_H - margin - cardH / 2;
    }

    ctx.save();
    ctx.translate(cx, cy);

    const cardX = -cardW / 2;
    const cardY = -cardH / 2;
    const cardRadius = 18;

    // 1. Outer Card Container (with soft luxury shadow)
    ctx.save();
    ctx.shadowColor = "rgba(15, 23, 42, 0.09)";
    ctx.shadowBlur = 24;
    ctx.shadowOffsetY = 8;

    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, cardRadius);
    ctx.fill();
    ctx.restore();

    // Crisp Card Border
    ctx.strokeStyle = "#E2E8F0";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, cardRadius);
    ctx.stroke();

    // 2. Top Vibrant Gradient Accent Ribbon
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, 5, [cardRadius, cardRadius, 0, 0]);
    ctx.clip();
    const topRibbon = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topRibbon.addColorStop(0, "#4F46E5");   // Royal Indigo
    topRibbon.addColorStop(0.35, "#06B6D4"); // Electric Cyan
    topRibbon.addColorStop(0.70, "#10B981"); // Vivid Emerald
    topRibbon.addColorStop(1.00, "#F59E0B"); // Warm Amber
    ctx.fillStyle = topRibbon;
    ctx.fillRect(cardX, cardY, cardW, 5);
    ctx.restore();

    // 3. Card Header Banner
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY + 5, cardW, headH - 5, [0, 0, 0, 0]);
    ctx.clip();

    const headGrad = ctx.createLinearGradient(cardX, cardY + 5, cardX, cardY + headH);
    headGrad.addColorStop(0, "#FAFBFD");
    headGrad.addColorStop(1, "#F1F5F9");
    ctx.fillStyle = headGrad;
    ctx.fillRect(cardX, cardY + 5, cardW, headH - 5);
    ctx.restore();

    // Bottom hairline separator under header
    ctx.strokeStyle = "#E2E8F0";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cardX, cardY + headH);
    ctx.lineTo(cardX + cardW, cardY + headH);
    ctx.stroke();

    // Header Icon (Calculator in colorful squircle badge)
    const iconBadgeX = cardX + 16;
    const iconBadgeY = cardY + 11;
    const iconBadgeW = 28;
    const iconBadgeH = 28;
    const iconGrad = ctx.createLinearGradient(iconBadgeX, iconBadgeY, iconBadgeX + iconBadgeW, iconBadgeY + iconBadgeH);
    iconGrad.addColorStop(0, "#6366F1");
    iconGrad.addColorStop(1, "#4338CA");
    ctx.fillStyle = iconGrad;
    ctx.beginPath();
    ctx.roundRect(iconBadgeX, iconBadgeY, iconBadgeW, iconBadgeH, 8);
    ctx.fill();

    if (window.ICONS) {
      window.ICONS.draw(ctx, "calculator", iconBadgeX + iconBadgeW / 2, iconBadgeY + iconBadgeH / 2, 16, "#FFFFFF");
    }

    // Header Title & Statutory Subtitle
    ctx.font = "800 13px 'Plus Jakarta Sans', sans-serif";
    ctx.fillStyle = "#0F172A";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText("STATUTORY COMPUTATION", cardX + 54, cardY + 20);

    ctx.font = "700 9.5px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#64748B";
    ctx.fillText("STATUTORY AUDIT SCHEDULE", cardX + 54, cardY + 35);

    // Live Items badge on right with active emerald dot
    const badgeText = `${n} LINE ${n === 1 ? 'ITEM' : 'ITEMS'}`;
    ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    const bW = ctx.measureText(badgeText).width + 26;
    const bX = cardX + cardW - bW - 16;
    const bY = cardY + 14;
    const bH = 22;

    ctx.fillStyle = "#EEF2FF";
    ctx.strokeStyle = "#C7D2FE";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(bX, bY, bW, bH, 11);
    ctx.fill();
    ctx.stroke();

    // Emerald status dot
    ctx.fillStyle = "#10B981";
    ctx.beginPath();
    ctx.arc(bX + 11, bY + bH / 2, 3.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#4338CA";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(badgeText, bX + 20, bY + bH / 2);

    // 4. Render Each Calculation Row Container
    const staggerStepMs = 1100;
    const itemDurMs = 900;

    items.forEach((it, i) => {
      const itemStartMs = (it.startMs !== undefined && it.startMs !== null) ? it.startMs : (400 + (i * staggerStepMs));
      
      let tRow = 1.0;
      if (!isSettle) {
        if (timeMs < itemStartMs) {
          // Has not entered yet
          return;
        }
        tRow = Math.min(1.0, Math.max(0.0, (timeMs - itemStartMs) / itemDurMs));
      }

      // Entrance animation: Fade + Pop for Sign and Text
      const popT = isSettle ? 1.0 : Math.min(1.0, tRow / 0.55);
      const rowAlpha = isSettle ? 1.0 : popT;
      const rowScale = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(popT);
      const rowOffsetY = isSettle ? 0 : (1.0 - popT) * 6;

      // Counting animation for Amount
      const countT = isSettle ? 1.0 : window.TWEEN.ease.easeOutCubic(tRow);

      const rowX = cardX + 12;
      const rowW = cardW - 24;
      const ry = cardY + headH + padTop + (i * (rowH + rowGap));
      const rowMidY = ry + rowH / 2;

      const isTotal = it.sign === "=" || it.signType === "total" || it.sign === "total";
      const isAdd = it.sign === "+" || it.signType === "add";
      const isDeduct = it.sign === "−" || it.sign === "-" || it.signType === "deduct";
      const isMultiply = it.sign === "×" || it.sign === "*" || it.sign === "x" || it.signType === "multiply";

      ctx.save();
      ctx.globalAlpha = rowAlpha;

      // 4A. Distinct Row Background Pill & Accent Border
      if (isTotal) {
        // Executive Royal Indigo/Midnight Gradient Card for Total Result
        ctx.save();
        ctx.shadowColor = "rgba(49, 46, 129, 0.25)";
        ctx.shadowBlur = 8;
        ctx.shadowOffsetY = 3;

        const totalGrad = ctx.createLinearGradient(rowX, ry, rowX + rowW, ry + rowH);
        totalGrad.addColorStop(0, "#1E1B4B");
        totalGrad.addColorStop(1, "#312E81");
        ctx.fillStyle = totalGrad;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.fill();
        ctx.restore();

        // Glowing border
        ctx.strokeStyle = "rgba(129, 140, 248, 0.45)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.stroke();

        // Left vertical glowing accent bar
        const leftAccGrad = ctx.createLinearGradient(rowX, ry + 6, rowX, ry + rowH - 6);
        leftAccGrad.addColorStop(0, "#818CF8");
        leftAccGrad.addColorStop(1, "#38BDF8");
        ctx.fillStyle = leftAccGrad;
        ctx.beginPath();
        ctx.roundRect(rowX + 2.5, ry + 6, 4, rowH - 12, 2);
        ctx.fill();
      } else if (isAdd) {
        // Soft Emerald Tint Card
        const addGrad = ctx.createLinearGradient(rowX, ry, rowX + rowW, ry);
        addGrad.addColorStop(0, "rgba(16, 185, 129, 0.10)");
        addGrad.addColorStop(1, "rgba(16, 185, 129, 0.02)");
        ctx.fillStyle = addGrad;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.fill();

        ctx.strokeStyle = "rgba(16, 185, 129, 0.25)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.stroke();

        // Left vertical emerald bar
        ctx.fillStyle = "#10B981";
        ctx.beginPath();
        ctx.roundRect(rowX + 2.5, ry + 6, 4, rowH - 12, 2);
        ctx.fill();
      } else if (isDeduct) {
        // Soft Crimson/Rose Tint Card
        const deductGrad = ctx.createLinearGradient(rowX, ry, rowX + rowW, ry);
        deductGrad.addColorStop(0, "rgba(239, 68, 68, 0.08)");
        deductGrad.addColorStop(1, "rgba(239, 68, 68, 0.015)");
        ctx.fillStyle = deductGrad;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.fill();

        ctx.strokeStyle = "rgba(239, 68, 68, 0.22)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.stroke();

        // Left vertical crimson bar
        ctx.fillStyle = "#EF4444";
        ctx.beginPath();
        ctx.roundRect(rowX + 2.5, ry + 6, 4, rowH - 12, 2);
        ctx.fill();
      } else if (isMultiply) {
        // Soft Amber Tint Card
        const multGrad = ctx.createLinearGradient(rowX, ry, rowX + rowW, ry);
        multGrad.addColorStop(0, "rgba(245, 158, 11, 0.08)");
        multGrad.addColorStop(1, "rgba(245, 158, 11, 0.015)");
        ctx.fillStyle = multGrad;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.fill();

        ctx.strokeStyle = "rgba(245, 158, 11, 0.22)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.stroke();

        // Left vertical amber bar
        ctx.fillStyle = "#F59E0B";
        ctx.beginPath();
        ctx.roundRect(rowX + 2.5, ry + 6, 4, rowH - 12, 2);
        ctx.fill();
      } else {
        // Neutral Slate Card
        ctx.fillStyle = "rgba(248, 250, 252, 0.85)";
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.fill();

        ctx.strokeStyle = "#E2E8F0";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(rowX, ry, rowW, rowH, 10);
        ctx.stroke();

        ctx.fillStyle = "#94A3B8";
        ctx.beginPath();
        ctx.roundRect(rowX + 2.5, ry + 6, 4, rowH - 12, 2);
        ctx.fill();
      }

      // 4B. Row Content Container with Pop scale & offset
      ctx.save();
      ctx.translate(0, rowOffsetY);

      // Left Sign Badge
      const glyphRadius = 13;
      const glyphX = rowX + 24;
      drawSignBadge(ctx, it.sign, it.signType, glyphX, rowMidY, glyphRadius, rowScale);

      // Middle Text Label (Fade & Pop)
      ctx.font = isTotal ? "800 14px 'Plus Jakarta Sans', sans-serif" : "600 13.5px 'Plus Jakarta Sans', sans-serif";
      ctx.fillStyle = isTotal ? "#F8FAFC" : "#0F172A";
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(it.text || "", rowX + 48, rowMidY);

      // 4C. Right Amount Container & Display with Counting Animation
      let displayedAmtStr = "";
      if (it.num !== null && !isNaN(it.num)) {
        const currentCount = Math.round(it.num * countT);
        displayedAmtStr = `${it.currency || "₹"} ${currentCount.toLocaleString("en-IN")}`;
      } else {
        displayedAmtStr = it.rawAmount || "";
      }

      // Amount font & chip container
      ctx.font = isTotal ? "800 15.5px 'JetBrains Mono', monospace" : "800 14.5px 'JetBrains Mono', monospace";
      const amtTextW = ctx.measureText(displayedAmtStr).width;
      const chipPadH = 14;
      const chipW = amtTextW + (chipPadH * 2);
      const chipH = 32;
      const chipX = rowX + rowW - chipW - 10;
      const chipY = rowMidY - chipH / 2;

      // Amount chip pill
      if (isTotal) {
        ctx.fillStyle = "rgba(15, 23, 42, 0.65)";
        ctx.strokeStyle = "rgba(129, 140, 248, 0.4)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(chipX, chipY, chipW, chipH, 8);
        ctx.fill();
        ctx.stroke();
      } else {
        ctx.fillStyle = "rgba(255, 255, 255, 0.95)";
        ctx.strokeStyle = isAdd ? "rgba(16, 185, 129, 0.28)" : (isDeduct ? "rgba(239, 68, 68, 0.28)" : "rgba(226, 232, 240, 0.8)");
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(chipX, chipY, chipW, chipH, 8);
        ctx.fill();
        ctx.stroke();
      }

      // Amount Text Color
      if (!isSettle && tRow < 1.0) {
        ctx.fillStyle = isTotal ? "#38BDF8" : "#2563EB"; // Active neon cyan / royal blue during live roll
      } else {
        if (isTotal) {
          ctx.fillStyle = "#34D399";      // Radiant mint green for settled final result
          ctx.shadowColor = "rgba(52, 211, 153, 0.35)";
          ctx.shadowBlur = 6;
        } else if (isAdd) {
          ctx.fillStyle = "#047857";  // Deep Emerald
        } else if (isDeduct) {
          ctx.fillStyle = "#B91C1C"; // Deep Crimson
        } else if (isMultiply) {
          ctx.fillStyle = "#B45309"; // Deep Amber
        } else {
          ctx.fillStyle = "#0F172A";
        }
      }

      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(displayedAmtStr, chipX + chipW / 2, rowMidY);
      ctx.shadowColor = "transparent";
      ctx.shadowBlur = 0;

      // 4D. Classical Statutory Double Underline for Total Row (=)
      // Placed precisely beneath the amount figures for authentic audited perfection
      if (isTotal) {
        ctx.strokeStyle = "#38BDF8"; // Radiant electric cyan
        ctx.lineWidth = 1.35;
        const lineY1 = chipY + chipH + 2;
        const lineY2 = chipY + chipH + 5;
        const ruleLeft = chipX + chipPadH - 4;
        const ruleRight = chipX + chipW - chipPadH + 4;
        ctx.beginPath();
        ctx.moveTo(ruleLeft, lineY1);
        ctx.lineTo(ruleRight, lineY1);
        ctx.moveTo(ruleLeft, lineY2);
        ctx.lineTo(ruleRight, lineY2);
        ctx.stroke();
      }

      ctx.restore(); // end rowOffsetY
      ctx.restore(); // end rowAlpha
    });

    ctx.restore(); // end main card
  }

  /**
   * Measurement pass for Mathematical AST
   */
  function measureFormulaNode(node, ctx, scale = 1.0) {
    if (!node) return { w: 0, h: 0, ascent: 0, descent: 0 };

    if (node.type === "term") {
      ctx.save();
      ctx.font = "700 " + Math.round(13 * scale) + "px 'Plus Jakarta Sans', sans-serif";
      const textW = ctx.measureText(node.text || "").width;
      let amtW = 0;
      if (node.amount) {
        ctx.font = "800 " + Math.round(13.5 * scale) + "px 'JetBrains Mono', monospace";
        const currPrefix = node.currency ? (node.currency + " ") : "";
        const estAmtStr = (node.num !== null && !isNaN(node.num)) ? `${currPrefix}${node.num.toLocaleString("en-IN")}` : node.amount;
        amtW = ctx.measureText(estAmtStr).width + (14 * scale);
      }
      ctx.restore();

      const hasAmt = Boolean(node.amount);
      const contentW = Math.max(textW, amtW);
      const w = Math.max(76 * scale, contentW + (26 * scale));
      const h = hasAmt ? (54 * scale) : (38 * scale);
      const ascent = h / 2;
      const descent = h / 2;

      node.layout = { w, h, ascent, descent, textW, amtW, hasAmt, scale };
      return node.layout;
    }

    if (node.type === "fraction") {
      const numL = measureFormulaNode(node.numerator, ctx, scale);
      const denL = measureFormulaNode(node.denominator, ctx, scale);
      const gap = 8 * scale;
      const barThickness = Math.max(2, 2.2 * scale);
      const w = Math.max(numL.w, denL.w) + (24 * scale);
      const ascent = numL.h + gap;
      const descent = denL.h + gap + barThickness;
      const h = ascent + descent;

      node.layout = { w, h, ascent, descent, numL, denL, gap, barThickness, scale };
      return node.layout;
    }

    if (node.type === "bracket") {
      const innerL = measureFormulaNode(node.inner, ctx, scale);
      const bracketW = 12 * scale;
      const w = innerL.w + (bracketW * 2) + (8 * scale);
      const padV = 6 * scale;
      const ascent = innerL.ascent + padV;
      const descent = innerL.descent + padV;
      const h = ascent + descent;

      node.layout = { w, h, ascent, descent, innerL, bracketW, scale };
      return node.layout;
    }

    if (node.type === "power") {
      const baseL = measureFormulaNode(node.base, ctx, scale);
      const expScale = scale * 0.78;
      const expL = measureFormulaNode(node.exponent, ctx, expScale);
      const w = baseL.w + (4 * scale) + expL.w;
      const expShiftY = baseL.ascent * 0.7;
      const ascent = Math.max(baseL.ascent, expShiftY + expL.ascent);
      const descent = baseL.descent;
      const h = ascent + descent;

      node.layout = { w, h, ascent, descent, baseL, expL, expShiftY, expScale, scale };
      return node.layout;
    }

    if (node.type === "binary") {
      const leftL = measureFormulaNode(node.left, ctx, scale);
      const rightL = measureFormulaNode(node.right, ctx, scale);
      const isEquals = node.op === "=";
      const opW = isEquals ? (40 * scale) : (32 * scale);
      const w = leftL.w + opW + rightL.w;
      const ascent = Math.max(leftL.ascent, rightL.ascent, 16 * scale);
      const descent = Math.max(leftL.descent, rightL.descent, 16 * scale);
      const h = ascent + descent;

      node.layout = { w, h, ascent, descent, leftL, rightL, opW, isEquals, scale };
      return node.layout;
    }

    return { w: 0, h: 0, ascent: 0, descent: 0 };
  }

  function getSubtreeStartMs(node) {
    if (!node) return 0;
    if (node.type === "term") return node.introTimeMs || 0;
    if (node.type === "fraction") return Math.min(getSubtreeStartMs(node.numerator), getSubtreeStartMs(node.denominator));
    if (node.type === "bracket") return getSubtreeStartMs(node.inner);
    if (node.type === "power") return Math.min(getSubtreeStartMs(node.base), getSubtreeStartMs(node.exponent));
    if (node.type === "binary") return Math.min(getSubtreeStartMs(node.left), getSubtreeStartMs(node.right));
    return 0;
  }

  /**
   * Recursive renderer for Mathematical AST
   */
  function renderFormulaNode(ctx, node, x, baselineY, timeMs, isSettle, isRhs = false) {
    if (!node || !node.layout) return;

    if (node.type === "term") {
      const itemStartMs = node.introTimeMs || 400;
      const itemDurMs = 750;

      if (!isSettle && timeMs < itemStartMs) {
        return; // Has not popped in yet
      }

      const t = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - itemStartMs) / itemDurMs));
      const popT = isSettle ? 1.0 : Math.min(1.0, t / 0.55);
      const alpha = isSettle ? 1.0 : popT;
      const scaleFactor = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(popT);
      const countT = isSettle ? 1.0 : window.TWEEN.ease.easeOutCubic(t);

      const sc = node.layout.scale || 1.0;
      const w = node.layout.w;
      const h = node.layout.h;
      const cx = x + w / 2;
      const cy = baselineY;

      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(cx, cy);
      if (scaleFactor !== 1.0) {
        ctx.scale(scaleFactor, scaleFactor);
      }

      const rx = -w / 2;
      const ry = -h / 2;
      const hasAmt = node.layout.hasAmt;
      const isResult = isRhs;
      const cornerR = Math.max(6, 10 * sc);

      if (isResult) {
        // Executive Midnight Indigo Card for Result Term
        ctx.save();
        ctx.shadowColor = "rgba(49, 46, 129, 0.3)";
        ctx.shadowBlur = 10 * sc;
        ctx.shadowOffsetY = 3 * sc;

        const resGrad = ctx.createLinearGradient(rx, ry, rx + w, ry + h);
        resGrad.addColorStop(0, "#1E1B4B");
        resGrad.addColorStop(1, "#312E81");
        ctx.fillStyle = resGrad;
        ctx.beginPath();
        ctx.roundRect(rx, ry, w, h, cornerR);
        ctx.fill();
        ctx.restore();

        ctx.strokeStyle = "rgba(129, 140, 248, 0.5)";
        ctx.lineWidth = Math.max(1, 1.5 * sc);
        ctx.beginPath();
        ctx.roundRect(rx, ry, w, h, cornerR);
        ctx.stroke();

        // Left glowing accent
        ctx.fillStyle = "#818CF8";
        ctx.beginPath();
        ctx.roundRect(rx + 2.5 * sc, ry + 5 * sc, 3.5 * sc, h - 10 * sc, 2 * sc);
        ctx.fill();
      } else {
        // Input variable card (Crisp white with soft indigo/emerald tint)
        ctx.save();
        ctx.shadowColor = "rgba(15, 23, 42, 0.07)";
        ctx.shadowBlur = 8 * sc;
        ctx.shadowOffsetY = 2 * sc;

        const bgGrad = ctx.createLinearGradient(rx, ry, rx + w, ry + h);
        bgGrad.addColorStop(0, "#FFFFFF");
        bgGrad.addColorStop(1, "#F8FAFC");
        ctx.fillStyle = bgGrad;
        ctx.beginPath();
        ctx.roundRect(rx, ry, w, h, cornerR);
        ctx.fill();
        ctx.restore();

        ctx.strokeStyle = "#CBD5E1";
        ctx.lineWidth = Math.max(1, 1.25 * sc);
        ctx.beginPath();
        ctx.roundRect(rx, ry, w, h, cornerR);
        ctx.stroke();

        // Left indicator
        ctx.fillStyle = "#4F46E5";
        ctx.beginPath();
        ctx.roundRect(rx + 2.5 * sc, ry + 5 * sc, 3.5 * sc, h - 10 * sc, 2 * sc);
        ctx.fill();
      }

      // Variable Label
      const labelY = hasAmt ? (ry + (15 * sc)) : 0;
      ctx.font = "700 " + Math.round(12.5 * sc) + "px 'Plus Jakarta Sans', sans-serif";
      ctx.fillStyle = isResult ? "#F8FAFC" : "#0F172A";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.text || "", 0, labelY);

      // Amount with Counting Odometer
      if (hasAmt) {
        let displayedAmtStr = "";
        if (node.num !== null && !isNaN(node.num)) {
          const currentCount = Math.round(node.num * countT);
          const currPrefix = node.currency ? (node.currency + " ") : "";
          displayedAmtStr = `${currPrefix}${currentCount.toLocaleString("en-IN")}`;
        } else {
          displayedAmtStr = node.amount || "";
        }

        const amtY = ry + h - (15 * sc);
        ctx.font = "800 " + Math.round(13.5 * sc) + "px 'JetBrains Mono', monospace";
        const amtW = ctx.measureText(displayedAmtStr).width;

        // Amount Chip Pill
        const chipW = amtW + (16 * sc);
        const chipH = Math.round(22 * sc);
        const chipX = -chipW / 2;
        const chipY = amtY - chipH / 2;

        if (isResult) {
          ctx.fillStyle = "rgba(15, 23, 42, 0.65)";
          ctx.strokeStyle = "rgba(129, 140, 248, 0.4)";
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(chipX, chipY, chipW, chipH, Math.max(4, 6 * sc));
          ctx.fill();
          ctx.stroke();
        } else {
          ctx.fillStyle = "#F1F5F9";
          ctx.strokeStyle = "#E2E8F0";
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(chipX, chipY, chipW, chipH, Math.max(4, 6 * sc));
          ctx.fill();
          ctx.stroke();
        }

        // Amount Color
        if (!isSettle && t < 1.0) {
          ctx.fillStyle = isResult ? "#38BDF8" : "#2563EB"; // Glowing blue while counting
        } else {
          ctx.fillStyle = isResult ? "#34D399" : "#047857"; // Mint or Emerald when settled
        }

        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(displayedAmtStr, 0, amtY);

        // Classical Double Underline for Result Term
        if (isResult) {
          ctx.strokeStyle = "#38BDF8";
          ctx.lineWidth = 1.35 * sc;
          const lineY1 = chipY + chipH + (1.5 * sc);
          const lineY2 = chipY + chipH + (4.5 * sc);
          ctx.beginPath();
          ctx.moveTo(chipX + 2 * sc, lineY1);
          ctx.lineTo(chipX + chipW - 2 * sc, lineY1);
          ctx.moveTo(chipX + 2 * sc, lineY2);
          ctx.lineTo(chipX + chipW - 2 * sc, lineY2);
          ctx.stroke();
        }
      }

      ctx.restore();
      return;
    }

    if (node.type === "fraction") {
      const hasStarted = isSettle || timeMs >= getSubtreeStartMs(node);
      if (!hasStarted) return;

      const vinculumY = baselineY - (2 * node.layout.scale);

      // 1. Draw Vinculum Horizontal Fraction Bar
      ctx.save();
      ctx.strokeStyle = "#4338CA";
      ctx.lineWidth = node.layout.barThickness;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(x + 2, vinculumY);
      ctx.lineTo(x + node.layout.w - 2, vinculumY);
      ctx.stroke();
      ctx.restore();

      // 2. Render Numerator above
      const numX = x + (node.layout.w - node.layout.numL.w) / 2;
      const numBaselineY = vinculumY - node.layout.gap - node.layout.numL.descent;
      renderFormulaNode(ctx, node.numerator, numX, numBaselineY, timeMs, isSettle, isRhs);

      // 3. Render Denominator below
      const denX = x + (node.layout.w - node.layout.denL.w) / 2;
      const denBaselineY = vinculumY + node.layout.barThickness + node.layout.gap + node.layout.denL.ascent;
      renderFormulaNode(ctx, node.denominator, denX, denBaselineY, timeMs, isSettle, isRhs);
      return;
    }

    if (node.type === "bracket") {
      const hasStarted = isSettle || timeMs >= getSubtreeStartMs(node);
      if (!hasStarted) return;

      const innerX = x + node.layout.bracketW + (4 * node.layout.scale);
      renderFormulaNode(ctx, node.inner, innerX, baselineY, timeMs, isSettle, isRhs);

      // Draw smooth expanding parentheses
      const topY = baselineY - node.layout.ascent;
      const botY = baselineY + node.layout.descent;
      const midY = (topY + botY) / 2;

      ctx.save();
      ctx.strokeStyle = "#4F46E5";
      ctx.lineWidth = Math.max(2, 2.2 * node.layout.scale);
      ctx.lineCap = "round";

      // Left bracket '('
      const leftX = x + 8;
      ctx.beginPath();
      ctx.moveTo(leftX + 4, topY);
      ctx.quadraticCurveTo(leftX - 4, midY, leftX + 4, botY);
      ctx.stroke();

      // Right bracket ')'
      const rightX = x + node.layout.w - 8;
      ctx.beginPath();
      ctx.moveTo(rightX - 4, topY);
      ctx.quadraticCurveTo(rightX + 4, midY, rightX - 4, botY);
      ctx.stroke();

      ctx.restore();
      return;
    }

    if (node.type === "power") {
      renderFormulaNode(ctx, node.base, x, baselineY, timeMs, isSettle, isRhs);

      const expX = x + node.layout.baseL.w + (4 * node.layout.scale);
      const expBaselineY = baselineY - node.layout.expShiftY;
      renderFormulaNode(ctx, node.exponent, expX, expBaselineY, timeMs, isSettle, isRhs);
      return;
    }

    if (node.type === "binary") {
      const hasStarted = isSettle || timeMs >= getSubtreeStartMs(node.left) || timeMs >= getSubtreeStartMs(node.right);
      if (!hasStarted) return;

      renderFormulaNode(ctx, node.left, x, baselineY, timeMs, isSettle, isRhs);

      const opCenterX = x + node.layout.leftL.w + (node.layout.opW / 2);
      const opCenterY = baselineY;

      // Draw mathematical operator
      ctx.save();
      if (node.op === "=") {
        ctx.strokeStyle = "#4F46E5";
        ctx.lineWidth = 2.5;
        ctx.lineCap = "round";
        const barW = 16;
        ctx.beginPath();
        ctx.moveTo(opCenterX - barW / 2, opCenterY - 4);
        ctx.lineTo(opCenterX + barW / 2, opCenterY - 4);
        ctx.moveTo(opCenterX - barW / 2, opCenterY + 4);
        ctx.lineTo(opCenterX + barW / 2, opCenterY + 4);
        ctx.stroke();
      } else if (node.op === "×") {
        ctx.strokeStyle = "#D97706";
        ctx.lineWidth = 2.2;
        ctx.lineCap = "round";
        const r = 6;
        ctx.beginPath();
        ctx.moveTo(opCenterX - r, opCenterY - r);
        ctx.lineTo(opCenterX + r, opCenterY + r);
        ctx.moveTo(opCenterX + r, opCenterY - r);
        ctx.lineTo(opCenterX - r, opCenterY + r);
        ctx.stroke();
      } else if (node.op === "+") {
        ctx.strokeStyle = "#059669";
        ctx.lineWidth = 2.2;
        ctx.lineCap = "round";
        const r = 7;
        ctx.beginPath();
        ctx.moveTo(opCenterX - r, opCenterY);
        ctx.lineTo(opCenterX + r, opCenterY);
        ctx.moveTo(opCenterX, opCenterY - r);
        ctx.lineTo(opCenterX, opCenterY + r);
        ctx.stroke();
      } else if (node.op === "−" || node.op === "-") {
        ctx.strokeStyle = "#DC2626";
        ctx.lineWidth = 2.2;
        ctx.lineCap = "round";
        const r = 7;
        ctx.beginPath();
        ctx.moveTo(opCenterX - r, opCenterY);
        ctx.lineTo(opCenterX + r, opCenterY);
        ctx.stroke();
      }
      ctx.restore();

      const nextRhs = isRhs || (node.op === "=");
      const rightX = x + node.layout.leftL.w + node.layout.opW;
      renderFormulaNode(ctx, node.right, rightX, baselineY, timeMs, isSettle, nextRhs);
    }
  }

  /**
   * Renders the Calculation Single (Complex Formula) Shape:
   * Executive card, mathematical fractions, brackets, superscripts,
   * 0.5s sequential pop-up per element, and live counting amounts.
   */
  function drawCalculationSingleShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    if (!actor || !actor.formulaData || !actor.formulaData.ast) return;
    if (!actor.totalTimelineMs) {
      computeCalculationSingleTimeline(actor);
    }

    // 1. Measure Mathematical AST
    const layout = measureFormulaNode(actor.formulaData.ast, ctx, 1.0);
    const formulaW = layout.w;
    const formulaH = layout.h;

    const headH = 50;
    const padTop = 28;
    const padB = 28;
    const cardW = Math.max(540, Math.min(1100, formulaW + 90));
    const cardH = headH + padTop + formulaH + padB;

    // Clamp coordinates to stage canvas with 36px margin
    const STAGE_W = 1280;
    const STAGE_H = 720;
    const margin = 36;

    let cx = actor.startPos.x;
    let cy = actor.startPos.y;

    if (cx - cardW / 2 < margin) cx = margin + cardW / 2;
    else if (cx + cardW / 2 > STAGE_W - margin) cx = STAGE_W - margin - cardW / 2;

    if (cy - cardH / 2 < margin) cy = margin + cardH / 2;
    else if (cy + cardH / 2 > STAGE_H - margin) cy = STAGE_H - margin - cardH / 2;

    ctx.save();
    ctx.translate(cx, cy);

    const cardX = -cardW / 2;
    const cardY = -cardH / 2;
    const cardRadius = 18;

    // Outer Card Container (with soft luxury shadow)
    ctx.save();
    ctx.shadowColor = "rgba(15, 23, 42, 0.09)";
    ctx.shadowBlur = 24;
    ctx.shadowOffsetY = 8;

    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, cardRadius);
    ctx.fill();
    ctx.restore();

    // Crisp Card Border
    ctx.strokeStyle = "#E2E8F0";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, cardRadius);
    ctx.stroke();

    // Top Vibrant Gradient Accent Ribbon
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, 5, [cardRadius, cardRadius, 0, 0]);
    ctx.clip();
    const topRibbon = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topRibbon.addColorStop(0, "#4F46E5");
    topRibbon.addColorStop(0.35, "#06B6D4");
    topRibbon.addColorStop(0.70, "#10B981");
    topRibbon.addColorStop(1.00, "#F59E0B");
    ctx.fillStyle = topRibbon;
    ctx.fillRect(cardX, cardY, cardW, 5);
    ctx.restore();

    // Card Header Banner
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY + 5, cardW, headH - 5, [0, 0, 0, 0]);
    ctx.clip();
    const headGrad = ctx.createLinearGradient(cardX, cardY + 5, cardX, cardY + headH);
    headGrad.addColorStop(0, "#FAFBFD");
    headGrad.addColorStop(1, "#F1F5F9");
    ctx.fillStyle = headGrad;
    ctx.fillRect(cardX, cardY + 5, cardW, headH - 5);
    ctx.restore();

    ctx.strokeStyle = "#E2E8F0";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cardX, cardY + headH);
    ctx.lineTo(cardX + cardW, cardY + headH);
    ctx.stroke();

    // Header Icon (Calculator in squircle badge)
    const iconBadgeX = cardX + 16;
    const iconBadgeY = cardY + 11;
    const iconBadgeW = 28;
    const iconBadgeH = 28;
    const iconGrad = ctx.createLinearGradient(iconBadgeX, iconBadgeY, iconBadgeX + iconBadgeW, iconBadgeY + iconBadgeH);
    iconGrad.addColorStop(0, "#6366F1");
    iconGrad.addColorStop(1, "#4338CA");
    ctx.fillStyle = iconGrad;
    ctx.beginPath();
    ctx.roundRect(iconBadgeX, iconBadgeY, iconBadgeW, iconBadgeH, 8);
    ctx.fill();

    if (window.ICONS) {
      window.ICONS.draw(ctx, "calculator", iconBadgeX + iconBadgeW / 2, iconBadgeY + iconBadgeH / 2, 16, "#FFFFFF");
    }

    // Title & Subtitle
    ctx.font = "800 13px 'Plus Jakarta Sans', sans-serif";
    ctx.fillStyle = "#0F172A";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText("STATUTORY FORMULA COMPUTATION", cardX + 54, cardY + 20);

    ctx.font = "700 9.5px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#64748B";
    ctx.fillText("MATHEMATICAL EQUATION ENGINE", cardX + 54, cardY + 35);

    // Right Badge
    const termCount = actor.formulaData.totalTerms || 1;
    const badgeText = `${termCount} ${termCount === 1 ? 'TERM' : 'TERMS'}`;
    ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    const bW = ctx.measureText(badgeText).width + 26;
    const bX = cardX + cardW - bW - 16;
    const bY = cardY + 14;
    const bH = 22;

    ctx.fillStyle = "#EEF2FF";
    ctx.strokeStyle = "#C7D2FE";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(bX, bY, bW, bH, 11);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#10B981";
    ctx.beginPath();
    ctx.arc(bX + 11, bY + bH / 2, 3.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#4338CA";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(badgeText, bX + 20, bY + bH / 2);

    // 2. Render Mathematical Expression along computed baseline
    const baselineY = cardY + headH + padTop + layout.ascent;
    const startX = cardX + (cardW - formulaW) / 2;

    renderFormulaNode(ctx, actor.formulaData.ast, startX, baselineY, timeMs, isSettle, false);

    ctx.restore();
  }

  /**
   * Renders the Checklist Shape with Interlocking Chain & Padlock Unlock Animation:
   * Supports condition rows with check/cross badges, and a statutory gate at the end
   * with physical metallic chains and spring padlock that unlocks or remains locked.
   */
  function drawChecklistShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    if (!actor.totalTimelineMs) {
      computeChecklistTimeline(actor);
    }
    const items = actor.items || [];
    const gateItem = actor.gateItem || null;
    const hasGate = !!gateItem;
    const N = items.length;

    // 1. Overall Card Dimensions & Layout
    const cardW = 680;
    const headH = 56;
    const rowH = 46;
    const rowGap = 8;
    const gateH = hasGate ? 72 : 0;
    const gateGap = hasGate ? 14 : 0;
    const padBottom = 16;
    const cardH = headH + (N * (rowH + rowGap)) + (hasGate ? (gateGap + gateH) : 0) + padBottom;

    // Placement
    let cardX = (actor.startPos ? actor.startPos.x : 960) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 540) - cardH / 2;
    // Bounds clamping
    cardX = Math.max(40, Math.min(1920 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(1080 - cardH - 40, cardY));

    // Overall intro animation (0.0s to 0.4s)
    const cardIntroT = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, timeMs / 400));
    const cardScale = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(cardIntroT);
    const cardAlpha = isSettle ? 1.0 : Math.min(1.0, cardIntroT * 1.5);

    if (cardAlpha <= 0) return;

    ctx.save();
    ctx.globalAlpha = cardAlpha;

    // Apply scale pivot around center
    if (!isSettle && cardScale !== 1.0) {
      const cx = cardX + cardW / 2;
      const cy = cardY + cardH / 2;
      ctx.translate(cx, cy);
      ctx.scale(cardScale, cardScale);
      ctx.translate(-cx, -cy);
    }

    // Outer Glow / Shadow
    ctx.shadowColor = "rgba(0, 0, 0, 0.45)";
    ctx.shadowBlur = 24;
    ctx.shadowOffsetY = 10;

    // Container Background - Slate/Obsidian Gradient
    const bgGrad = ctx.createLinearGradient(cardX, cardY, cardX, cardY + cardH);
    bgGrad.addColorStop(0, "rgba(15, 23, 42, 0.96)");
    bgGrad.addColorStop(1, "rgba(30, 41, 59, 0.94)");
    ctx.fillStyle = bgGrad;
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, 16);
    ctx.fill();

    // Reset shadow for inner strokes
    ctx.shadowColor = "transparent";
    ctx.shadowBlur = 0;
    ctx.shadowOffsetY = 0;

    // Card Border
    ctx.strokeStyle = "rgba(148, 163, 184, 0.22)";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Top Statutory Highlight Accent Bar
    const topGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topGrad.addColorStop(0, "#10B981");
    topGrad.addColorStop(0.5, "#06B6D4");
    topGrad.addColorStop(1, "#3B82F6");
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, 16, [16, 16, 0, 0]);
    ctx.clip();
    ctx.fillStyle = topGrad;
    ctx.fillRect(cardX, cardY, cardW, 3.5);
    ctx.restore();

    // 2. Card Header
    // Icon badge
    ctx.fillStyle = "rgba(16, 185, 129, 0.20)";
    ctx.beginPath();
    ctx.arc(cardX + 32, cardY + 28, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#34D399";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Small checkmark inside icon badge
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(cardX + 27, cardY + 28);
    ctx.lineTo(cardX + 30.5, cardY + 31.5);
    ctx.lineTo(cardX + 37, cardY + 24.5);
    ctx.stroke();

    // Title
    ctx.fillStyle = "#F8FAFC";
    ctx.font = "700 13px 'Inter', -apple-system, sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.letterSpacing = "0.5px";
    const headerTitle = actor.title || "STATUTORY COMPLIANCE CHECKLIST";
    ctx.fillText(headerTitle.toUpperCase(), cardX + 54, cardY + 28);

    // Right-side Summary Pill: e.g. "3/3 MET"
    const visibleItems = isSettle ? items : items.filter((it, idx) => {
      const itStart = (it.startMs !== undefined && it.startMs !== null) ? it.startMs : (350 + idx * 500);
      return timeMs >= itStart;
    });
    const metCount = visibleItems.filter(it => it.status && (it.status.val === "ok" || it.status.isOk === true)).length;
    const summaryText = `${metCount}/${N} MET`;
    ctx.font = "600 11px 'Inter', -apple-system, sans-serif";
    const sumW = ctx.measureText(summaryText).width + 20;
    const sumH = 22;
    const sumX = cardX + cardW - 20 - sumW;
    const sumY = cardY + 17;
    ctx.fillStyle = metCount === N ? "rgba(16, 185, 129, 0.20)" : "rgba(245, 158, 11, 0.20)";
    ctx.strokeStyle = metCount === N ? "rgba(52, 211, 153, 0.50)" : "rgba(251, 191, 36, 0.50)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(sumX, sumY, sumW, sumH, 11);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = metCount === N ? "#34D399" : "#FBBF24";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(summaryText, sumX + sumW / 2, sumY + sumH / 2);

    // Header Divider Line
    ctx.strokeStyle = "rgba(148, 163, 184, 0.14)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cardX + 16, cardY + headH);
    ctx.lineTo(cardX + cardW - 16, cardY + headH);
    ctx.stroke();

    // 3. Render Condition Rows
    const itemsStartY = cardY + headH + 10;
    const rowW = cardW - 32;

    items.forEach((item, idx) => {
      const rowX = cardX + 16;
      const rowY = itemsStartY + idx * (rowH + rowGap);

      // Staggered Intro Timing: custom cumulative startMs or fallback
      const itemStartMs = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      const itemIntroT = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - itemStartMs) / 380));
      if (itemIntroT <= 0) return;

      const easedItem = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(itemIntroT);
      const slideX = isSettle ? 0 : (1 - Math.min(1.0, easedItem)) * -24;
      const itemAlpha = isSettle ? 1.0 : Math.min(1.0, itemIntroT * 1.5);

      ctx.save();
      ctx.globalAlpha = cardAlpha * itemAlpha;
      ctx.translate(slideX, 0);

      const isOk = item.status && (item.status.val === "ok" || item.status.isOk === true);

      // Row Container Background
      ctx.fillStyle = isOk ? "rgba(16, 185, 129, 0.08)" : "rgba(239, 68, 68, 0.08)";
      ctx.strokeStyle = isOk ? "rgba(16, 185, 129, 0.28)" : "rgba(239, 68, 68, 0.28)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(rowX, rowY, rowW, rowH, 8);
      ctx.fill();
      ctx.stroke();

      // Left Status Indicator Circle (x: rowX + 22, y: rowY + rowH/2)
      const circleX = rowX + 22;
      const circleY = rowY + rowH / 2;
      const circleR = 12;

      ctx.fillStyle = isOk ? "#059669" : "#DC2626";
      ctx.beginPath();
      ctx.arc(circleX, circleY, circleR, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = isOk ? "#34D399" : "#F87171";
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Icon inside circle (Checkmark vs Cross)
      ctx.strokeStyle = "#FFFFFF";
      ctx.lineWidth = 2;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.beginPath();
      if (isOk) {
        ctx.moveTo(circleX - 4.5, circleY);
        ctx.lineTo(circleX - 1, circleY + 3.5);
        ctx.lineTo(circleX + 5, circleY - 3.5);
      } else {
        ctx.moveTo(circleX - 3.5, circleY - 3.5);
        ctx.lineTo(circleX + 3.5, circleY + 3.5);
        ctx.moveTo(circleX + 3.5, circleY - 3.5);
        ctx.lineTo(circleX - 3.5, circleY + 3.5);
      }
      ctx.stroke();

      // Item Text Label
      ctx.fillStyle = "#F1F5F9";
      ctx.font = "600 13.5px 'Inter', -apple-system, sans-serif";
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.letterSpacing = "0.2px";

      // Truncate if too wide for the badge
      const maxTextW = rowW - 145;
      let text = item.text || `Statutory Condition ${idx + 1}`;
      if (ctx.measureText(text).width > maxTextW) {
        while (text.length > 3 && ctx.measureText(text + "...").width > maxTextW) {
          text = text.slice(0, -1);
        }
        text += "...";
      }
      ctx.fillText(text, rowX + 44, rowY + rowH / 2);

      // Right-side Status Pill Badge
      const badgeW = 96;
      const badgeH = 26;
      const badgeX = rowX + rowW - badgeW - 12;
      const badgeY = rowY + (rowH - badgeH) / 2;

      ctx.fillStyle = isOk ? "rgba(16, 185, 129, 0.18)" : "rgba(239, 68, 68, 0.18)";
      ctx.strokeStyle = isOk ? "rgba(52, 211, 153, 0.55)" : "rgba(248, 113, 113, 0.55)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 13);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = isOk ? "#6EE7B7" : "#FCA5A5";
      ctx.font = "700 10.5px 'Inter', -apple-system, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.letterSpacing = "0.4px";
      ctx.fillText(isOk ? "CHECK OK" : "CHECK NOT OK", badgeX + badgeW / 2, badgeY + badgeH / 2);

      ctx.restore();
    });

    // 4. Render Statutory Gate & Chain Unlock Animation
    if (hasGate) {
      const gateY = itemsStartY + N * (rowH + rowGap) + 6;
      const gateX = cardX + 16;
      const gateW = rowW;

      // Gate Intro Timing: custom cumulative startMs or fallback
      const gateStartMs = (gateItem && gateItem.startMs !== undefined && gateItem.startMs !== null) ? gateItem.startMs : (350 + N * 500 + 200);
      const gateIntroT = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - gateStartMs) / 450));

      if (gateIntroT > 0) {
        const easedGate = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(gateIntroT);
        const gateAlpha = isSettle ? 1.0 : Math.min(1.0, gateIntroT * 1.5);

        ctx.save();
        ctx.globalAlpha = cardAlpha * gateAlpha;

        // Gate evaluation & unlock progress
        const isUnlocked = gateItem.status && (gateItem.status.val === "unlock" || gateItem.status.isUnlock === true);
        const unlockStartMs = gateStartMs + 250;
        const unlockP = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - unlockStartMs) / 700));

        // Subtle divider bridge with small chain link accents
        ctx.strokeStyle = "rgba(148, 163, 184, 0.20)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(gateX + 20, gateY - 5);
        ctx.lineTo(gateX + gateW - 20, gateY - 5);
        ctx.stroke();

        // Jitter rattle for locked state if actively animating
        let rattleX = 0;
        if (!isUnlocked && !isSettle && timeMs > unlockStartMs) {
          const rattleT = Math.min(1.0, (timeMs - unlockStartMs) / 800);
          rattleX = Math.sin(timeMs * 0.06) * (1 - rattleT) * 3;
        }

        ctx.translate(rattleX, 0);

        // Gate Card Background & Border
        ctx.save();
        if (isUnlocked) {
          // Executive Emerald Glow
          const bgEmerald = ctx.createLinearGradient(gateX, gateY, gateX + gateW, gateY + gateH);
          bgEmerald.addColorStop(0, "rgba(6, 78, 59, 0.85)");
          bgEmerald.addColorStop(1, "rgba(4, 120, 87, 0.75)");
          ctx.fillStyle = bgEmerald;
          ctx.strokeStyle = "rgba(52, 211, 153, 0.85)";
          ctx.lineWidth = 1.5;

          if (unlockP > 0.1) {
            ctx.shadowColor = "rgba(16, 185, 129, 0.55)";
            ctx.shadowBlur = 16 * unlockP;
          }
        } else {
          // Locked Crimson/Obsidian Glow
          const bgCrimson = ctx.createLinearGradient(gateX, gateY, gateX + gateW, gateY + gateH);
          bgCrimson.addColorStop(0, "rgba(69, 10, 10, 0.85)");
          bgCrimson.addColorStop(1, "rgba(45, 15, 20, 0.80)");
          ctx.fillStyle = bgCrimson;
          ctx.strokeStyle = "rgba(239, 68, 68, 0.65)";
          ctx.lineWidth = 1.5;

          ctx.shadowColor = "rgba(239, 68, 68, 0.40)";
          ctx.shadowBlur = 10;
        }

        ctx.beginPath();
        ctx.roundRect(gateX, gateY, gateW, gateH, 10);
        ctx.fill();
        ctx.stroke();
        ctx.restore();

        // 5. Physical Metallic Chains & Padlock Animation
        const padCX = gateX + 46;
        const padCY = gateY + gateH / 2;

        // Draw Interlocking Metallic Chains
        // Chains slide outward and fade if unlocked; stay tight and locked if not unlocked
        const chainSlide = isUnlocked ? unlockP * 50 : 0;
        const chainAlpha = isUnlocked ? Math.max(0.0, 1.0 - unlockP * 1.3) : 1.0;

        if (chainAlpha > 0.02) {
          ctx.save();
          ctx.globalAlpha = gateAlpha * chainAlpha;

          // Helper to draw realistic metallic oval link
          const drawMetallicLink = (x, y, angle, w = 14, h = 8) => {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);
            ctx.strokeStyle = "#94A3B8";
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.roundRect(-w / 2, -h / 2, w, h, h / 2);
            ctx.stroke();
            // Highlight
            ctx.strokeStyle = "rgba(255, 255, 255, 0.55)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(-w / 4, 0, 1.5, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
          };

          // Left chain links sliding left
          drawMetallicLink(padCX - 36 - chainSlide, padCY, -0.15);
          drawMetallicLink(padCX - 24 - chainSlide * 0.7, padCY, 0.2);
          drawMetallicLink(padCX - 12 - chainSlide * 0.4, padCY, -0.1);

          // Right chain links sliding right
          drawMetallicLink(padCX + 12 + chainSlide * 0.4, padCY, 0.1);
          drawMetallicLink(padCX + 24 + chainSlide * 0.7, padCY, -0.2);
          drawMetallicLink(padCX + 36 + chainSlide, padCY, 0.15);

          ctx.restore();
        }

        // Draw Vector Padlock
        ctx.save();
        ctx.translate(padCX, padCY);

        const bodyW = 28;
        const bodyH = 22;
        const shackleR = 7.5;

        // Shackle (Springs UP and pivots open on unlock)
        const shackleLift = isUnlocked ? unlockP * 8 : 0;
        const shackleAngle = isUnlocked ? unlockP * 0.55 : 0; // ~32 deg open

        ctx.save();
        ctx.translate(-shackleR, -bodyH / 2 - shackleLift);
        ctx.rotate(shackleAngle);

        ctx.strokeStyle = isUnlocked ? "#6EE7B7" : "#CBD5E1";
        ctx.lineWidth = 3.5;
        ctx.lineCap = "round";
        ctx.beginPath();
        // Left leg anchored into body hole
        ctx.moveTo(0, 4);
        ctx.lineTo(0, -shackleR);
        // Arch shape
        ctx.arc(shackleR, -shackleR, shackleR, Math.PI, 0, false);
        // Right leg entering body hole (or clearing hole when unlocking)
        ctx.lineTo(shackleR * 2, isUnlocked ? -shackleR * 0.2 : 4);
        ctx.stroke();
        ctx.restore();

        // Padlock Body
        const padGrad = ctx.createLinearGradient(-bodyW / 2, -bodyH / 2, bodyW / 2, bodyH / 2);
        if (isUnlocked) {
          padGrad.addColorStop(0, "#10B981");
          padGrad.addColorStop(1, "#047857");
        } else {
          padGrad.addColorStop(0, "#F59E0B"); // Brass golden padlock
          padGrad.addColorStop(1, "#B45309");
        }
        ctx.fillStyle = padGrad;
        ctx.strokeStyle = isUnlocked ? "#A7F3D0" : "#FDE68A";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(-bodyW / 2, -bodyH / 2, bodyW, bodyH, 4);
        ctx.fill();
        ctx.stroke();

        // Keyhole
        ctx.fillStyle = "#0F172A";
        ctx.beginPath();
        ctx.arc(0, -2, 2.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(-1.5, -2);
        ctx.lineTo(1.5, -2);
        ctx.lineTo(2, 4);
        ctx.lineTo(-2, 4);
        ctx.closePath();
        ctx.fill();

        // Radiant Spark Burst on Unlock
        if (isUnlocked && unlockP > 0.25 && unlockP < 0.98 && !isSettle) {
          const sparkT = (unlockP - 0.25) / 0.73;
          const sparkAlpha = Math.sin(sparkT * Math.PI);
          ctx.strokeStyle = `rgba(52, 211, 153, ${sparkAlpha})`;
          ctx.lineWidth = 1.5;
          const r1 = 16 + sparkT * 8;
          const r2 = r1 + 6;
          for (let a = 0; a < 8; a++) {
            const ang = (a * Math.PI) / 4;
            ctx.beginPath();
            ctx.moveTo(Math.cos(ang) * r1, Math.sin(ang) * r1);
            ctx.lineTo(Math.cos(ang) * r2, Math.sin(ang) * r2);
            ctx.stroke();
          }
        }
        ctx.restore(); // end padlock

        // Gate Text Labels
        const textStartX = gateX + 96;
        const gateTitle = gateItem.text || "Statutory Exemption Gate";

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "700 15px 'Inter', -apple-system, sans-serif";
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.letterSpacing = "0.3px";
        ctx.fillText(gateTitle, textStartX, gateY + 24);

        // Subtitle note
        ctx.font = "600 11px 'Inter', -apple-system, sans-serif";
        if (isUnlocked) {
          ctx.fillStyle = "#6EE7B7";
          ctx.fillText("ALL STATUTORY CONDITIONS MET • EXEMPTION UNLOCKED", textStartX, gateY + 46);
        } else {
          ctx.fillStyle = "#FCA5A5";
          ctx.fillText("MANDATORY CONDITIONS NOT MET • EXEMPTION LOCKED", textStartX, gateY + 46);
        }

        // Right-Side Status Pill
        const statusPillW = 128;
        const statusPillH = 32;
        const statusPillX = gateX + gateW - statusPillW - 14;
        const statusPillY = gateY + (gateH - statusPillH) / 2;

        if (isUnlocked) {
          const pillGrad = ctx.createLinearGradient(statusPillX, statusPillY, statusPillX, statusPillY + statusPillH);
          pillGrad.addColorStop(0, "#059669");
          pillGrad.addColorStop(1, "#047857");
          ctx.fillStyle = pillGrad;
          ctx.strokeStyle = "#34D399";
          ctx.lineWidth = 1.5;
        } else {
          const pillGrad = ctx.createLinearGradient(statusPillX, statusPillY, statusPillX, statusPillY + statusPillH);
          pillGrad.addColorStop(0, "#991B1B");
          pillGrad.addColorStop(1, "#7F1D1D");
          ctx.fillStyle = pillGrad;
          ctx.strokeStyle = "#F87171";
          ctx.lineWidth = 1.5;
        }

        ctx.beginPath();
        ctx.roundRect(statusPillX, statusPillY, statusPillW, statusPillH, 16);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "800 11.5px 'Inter', -apple-system, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.letterSpacing = "0.6px";
        ctx.fillText(isUnlocked ? "🔓 UNLOCKED" : "🔒 LOCKED", statusPillX + statusPillW / 2, statusPillY + statusPillH / 2);

        ctx.restore(); // end gate
      }
    }

    ctx.restore(); // end overall card
  }

  /* ==========================================================================
     SHAPE (LIST) - 5 DISTINCT BROADCAST-QUALITY EDUCATIONAL DESIGNS
     ========================================================================== */

  /**
   * Master renderer for the List Shape:
   * Dispatches to 5 distinct visual designs so teachers aren't restricted to one repetitive look.
   * Design 1: Modern Floating Elevated Cards ("cards", default)
   * Design 2: Stepped Timeline Spine ("timeline" / "process")
   * Design 3: Statutory Clauses & Parchment ("clause" / "statutory")
   * Design 4: Minimal Two-Tone Pill Capsules ("pills" / "capsules")
   * Design 5: Obsidian Dark Deck with Neon Horizon Sheen ("obsidian" / "dark")
   */
  function drawListShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    if (!actor.totalTimelineMs) {
      computeListTimeline(actor);
    }
    const items = actor.items || [];
    const N = Math.max(1, items.length);
    const design = actor.design || 1;
    const listStartMs = (actor.startMs !== undefined && actor.startMs !== null) ? actor.startMs : 0;
    if (timeMs < listStartMs) return;

    // Card Intro animation relative to listStartMs
    const timeSinceListStart = Math.max(0, timeMs - listStartMs);
    const cardIntroT = Math.min(1.0, Math.max(0.0, timeSinceListStart / 400));
    const cardScale = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(cardIntroT);
    const cardAlpha = Math.min(1.0, cardIntroT * 1.5);
    if (cardAlpha <= 0) return;

    ctx.save();
    ctx.globalAlpha = cardAlpha;

    switch (design) {
      case 2:
        drawListTimelineDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale);
        break;
      case 3:
        drawListClauseDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale);
        break;
      case 4:
        drawListPillsDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale);
        break;
      case 5:
        drawListObsidianDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale);
        break;
      case 1:
      default:
        drawListCardsDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale);
        break;
    }

    ctx.restore();
  }

  // Helper for applying card center scale pivot
  function applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale) {
    if (cardScale !== 1.0) {
      const cx = cardX + cardW / 2;
      const cy = cardY + cardH / 2;
      ctx.translate(cx, cy);
      ctx.scale(cardScale, cardScale);
      ctx.translate(-cx, -cy);
    }
  }

  /* --------------------------------------------------------------------------
     DESIGN 1: MODERN FLOATING ELEVATED CARDS ("cards" / "elevated")
     -------------------------------------------------------------------------- */
  function drawListCardsDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale) {
    const cardW = 760;
    const headH = 58;
    const rowH = 54;
    const rowGap = 10;
    const padBottom = 16;
    const cardH = headH + (N * (rowH + rowGap)) + padBottom;

    let cardX = (actor.startPos ? actor.startPos.x : 640) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 360) - cardH / 2;
    cardX = Math.max(40, Math.min(1280 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(720 - cardH - 40, cardY));

    applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale);

    // Shell shadow
    ctx.shadowColor = "rgba(15, 23, 42, 0.08)";
    ctx.shadowBlur = 18;
    ctx.shadowOffsetY = 8;

    // Shell Background
    const bgGrad = ctx.createLinearGradient(cardX, cardY, cardX, cardY + cardH);
    bgGrad.addColorStop(0, "#FFFFFF");
    bgGrad.addColorStop(1, "#F8FAFC");
    ctx.fillStyle = bgGrad;
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, cardH, 16);
    ctx.fill();

    ctx.shadowColor = "transparent"; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
    ctx.strokeStyle = "rgba(203, 213, 225, 0.85)";
    ctx.lineWidth = 1.3;
    ctx.stroke();

    // Top Horizon Accent Bar
    const topBar = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topBar.addColorStop(0, "#4F46E5");
    topBar.addColorStop(0.5, "#6366F1");
    topBar.addColorStop(1, "#818CF8");
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(cardX, cardY, cardW, 16, [16, 16, 0, 0]);
    ctx.clip();
    ctx.fillStyle = topBar;
    ctx.fillRect(cardX, cardY, cardW, 3.5);
    ctx.restore();

    // Header
    // Icon badge
    ctx.fillStyle = "#EEF2FF";
    ctx.beginPath();
    ctx.arc(cardX + 34, cardY + 30, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#818CF8";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Star icon inside
    ctx.fillStyle = "#4F46E5";
    ctx.font = "800 13px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("✦", cardX + 34, cardY + 30.5);

    // Title
    ctx.fillStyle = "#0F172A";
    ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.letterSpacing = "0.5px";
    ctx.fillText((actor.title || "STATUTORY PROVISIONS").toUpperCase(), cardX + 58, cardY + 30);

    // Right Summary Pill
    const pillW = 90; const pillH = 24;
    const pillX = cardX + cardW - pillW - 20; const pillY = cardY + 18;
    ctx.fillStyle = "#F1F5F9";
    ctx.strokeStyle = "#CBD5E1";
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.roundRect(pillX, pillY, pillW, pillH, 12); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#475569";
    ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${N} PRINCIPLES`, pillX + pillW / 2, pillY + pillH / 2);

    // Items
    items.forEach((item, idx) => {
      const itStart = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      if (timeMs < itStart) return;

      const itT = isSettle ? 1.0 : Math.min(1.0, (timeMs - itStart) / 350);
      const easeX = isSettle ? 0 : (1.0 - window.TWEEN.ease.easeOutCubic(itT)) * -22;
      const alpha = isSettle ? 1.0 : itT;

      const rx = cardX + 20 + easeX;
      const ry = cardY + headH + idx * (rowH + rowGap);
      const rw = cardW - 40;
      const rh = rowH;

      ctx.save();
      ctx.globalAlpha = ctx.globalAlpha * alpha;

      // Card row shell
      ctx.shadowColor = "rgba(15, 23, 42, 0.04)";
      ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
      ctx.fillStyle = "#FFFFFF";
      ctx.beginPath(); ctx.roundRect(rx, ry, rw, rh, 10); ctx.fill();
      ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
      ctx.strokeStyle = "rgba(226, 232, 240, 0.95)";
      ctx.lineWidth = 1.2; ctx.stroke();

      // Number badge pill
      const bW = 34; const bH = 32;
      const bx = rx + 12; const by = ry + (rh - bH) / 2;
      const bGrad = ctx.createLinearGradient(bx, by, bx + bW, by + bH);
      bGrad.addColorStop(0, "#4F46E5");
      bGrad.addColorStop(1, "#6366F1");
      ctx.fillStyle = bGrad;
      ctx.beginPath(); ctx.roundRect(bx, by, bW, bH, 8); ctx.fill();

      ctx.fillStyle = "#FFFFFF";
      ctx.font = "800 12.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      const numStr = (idx + 1) < 10 ? `0${idx + 1}` : `${idx + 1}`;
      ctx.fillText(numStr, bx + bW / 2, by + bH / 2);

      // Title & Text
      const textX = bx + bW + 16;
      ctx.textAlign = "left"; ctx.textBaseline = "middle";

      if (item.desc) {
        ctx.fillStyle = "#0F172A";
        ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title, textX, ry + 18);

        ctx.fillStyle = "#64748B";
        ctx.font = "500 12px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.desc, textX, ry + 36);
      } else {
        ctx.fillStyle = "#0F172A";
        ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title || item.text, textX, ry + rh / 2);
      }

      ctx.restore();
    });
  }

  /* --------------------------------------------------------------------------
     DESIGN 2: STEPPED TIMELINE SPINE ("timeline" / "process")
     -------------------------------------------------------------------------- */
  function drawListTimelineDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale) {
    const cardW = 760;
    const headH = 58;
    const rowH = 62;
    const rowGap = 12;
    const padBottom = 18;
    const cardH = headH + (N * (rowH + rowGap)) + padBottom;

    let cardX = (actor.startPos ? actor.startPos.x : 640) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 360) - cardH / 2;
    cardX = Math.max(40, Math.min(1280 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(720 - cardH - 40, cardY));

    applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale);

    // Shell
    ctx.shadowColor = "rgba(15, 23, 42, 0.08)";
    ctx.shadowBlur = 18; ctx.shadowOffsetY = 8;
    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, cardH, 16); ctx.fill();
    ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
    ctx.strokeStyle = "rgba(203, 213, 225, 0.85)"; ctx.lineWidth = 1.3; ctx.stroke();

    // Top Sky Horizon Bar
    const topBar = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topBar.addColorStop(0, "#0284C7"); topBar.addColorStop(0.5, "#38BDF8"); topBar.addColorStop(1, "#0EA5E9");
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, 16, [16, 16, 0, 0]); ctx.clip();
    ctx.fillStyle = topBar; ctx.fillRect(cardX, cardY, cardW, 3.5);
    ctx.restore();

    // Header
    ctx.fillStyle = "#E0F2FE";
    ctx.beginPath(); ctx.arc(cardX + 34, cardY + 30, 14, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#38BDF8"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = "#0284C7"; ctx.font = "800 13px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("⏱", cardX + 34, cardY + 30);

    ctx.fillStyle = "#0F172A";
    ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.fillText((actor.title || "STATUTORY PROCEDURE FLOW").toUpperCase(), cardX + 58, cardY + 30);

    // Right Step Counter Pill
    const pillW = 86; const pillH = 24;
    const pillX = cardX + cardW - pillW - 20; const pillY = cardY + 18;
    ctx.fillStyle = "#F0F9FF"; ctx.strokeStyle = "#BAE6FD"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.roundRect(pillX, pillY, pillW, pillH, 12); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#0369A1"; ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${N} STAGES`, pillX + pillW / 2, pillY + pillH / 2);

    // Spine Vertical Conduit
    const spineX = cardX + 46;
    const spineStartY = cardY + headH + 16;
    const spineEndY = cardY + cardH - padBottom - 10;

    ctx.strokeStyle = "rgba(226, 232, 240, 0.85)"; ctx.lineWidth = 3; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(spineX, spineStartY); ctx.lineTo(spineX, spineEndY); ctx.stroke();

    // Items
    items.forEach((item, idx) => {
      const itStart = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      if (timeMs < itStart) return;

      const itT = isSettle ? 1.0 : Math.min(1.0, (timeMs - itStart) / 350);
      const easeX = isSettle ? 0 : (1.0 - window.TWEEN.ease.easeOutCubic(itT)) * -20;
      const alpha = isSettle ? 1.0 : itT;

      const nodeY = cardY + headH + 16 + idx * (rowH + rowGap) + rowH / 2 - 8;
      const rx = cardX + 80 + easeX;
      const ry = cardY + headH + 12 + idx * (rowH + rowGap);
      const rw = cardW - 100;
      const rh = rowH;

      ctx.save();
      ctx.globalAlpha = ctx.globalAlpha * alpha;

      // Active Spine Segment to this node
      ctx.strokeStyle = "#0284C7"; ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(spineX, idx === 0 ? spineStartY : nodeY - (rowH + rowGap));
      ctx.lineTo(spineX, nodeY);
      ctx.stroke();

      // Timeline Node Ring
      ctx.fillStyle = "#F0F9FF"; ctx.beginPath(); ctx.arc(spineX, nodeY, 14, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = "#0284C7"; ctx.lineWidth = 2; ctx.stroke();

      ctx.fillStyle = "#0284C7"; ctx.beginPath(); ctx.arc(spineX, nodeY, 9.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#FFFFFF"; ctx.font = "800 11px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(`${idx + 1}`, spineX, nodeY);

      // Milestone Card
      ctx.shadowColor = "rgba(15, 23, 42, 0.04)"; ctx.shadowBlur = 6; ctx.shadowOffsetY = 2;
      ctx.fillStyle = "#F8FAFC"; ctx.beginPath(); ctx.roundRect(rx, ry, rw, rh, 10); ctx.fill();
      ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
      ctx.strokeStyle = "rgba(203, 213, 225, 0.85)"; ctx.lineWidth = 1.2; ctx.stroke();

      // Pointer triangle to node
      ctx.fillStyle = "#F8FAFC";
      ctx.beginPath();
      ctx.moveTo(rx, nodeY - 5); ctx.lineTo(rx - 6, nodeY); ctx.lineTo(rx, nodeY + 5); ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = "rgba(203, 213, 225, 0.85)"; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(rx, nodeY - 5); ctx.lineTo(rx - 6, nodeY); ctx.lineTo(rx, nodeY + 5); ctx.stroke();

      // Step Tag Pill
      const tagW = 54; const tagH = 18; const tagX = rx + 14; const tagY = ry + (rh - tagH) / 2;
      ctx.fillStyle = "#E0F2FE"; ctx.beginPath(); ctx.roundRect(tagX, tagY, tagW, tagH, 6); ctx.fill();
      ctx.fillStyle = "#0284C7"; ctx.font = "800 9.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(`STAGE ${idx + 1}`, tagX + tagW / 2, tagY + tagH / 2);

      // Content
      const textX = tagX + tagW + 14;
      ctx.textAlign = "left"; ctx.textBaseline = "middle";

      if (item.desc) {
        ctx.fillStyle = "#0F172A"; ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title, textX, ry + 20);

        ctx.fillStyle = "#64748B"; ctx.font = "500 11.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.desc, textX, ry + 40);
      } else {
        ctx.fillStyle = "#0F172A"; ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title || item.text, textX, ry + rh / 2);
      }

      ctx.restore();
    });
  }

  /* --------------------------------------------------------------------------
     DESIGN 3: STATUTORY CLAUSES & FORMAL PARCHMENT ("clause" / "statutory")
     -------------------------------------------------------------------------- */
  function drawListClauseDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale) {
    const cardW = 760;
    const headH = 62;
    const rowH = 56;
    const rowGap = 8;
    const padBottom = 18;
    const cardH = headH + (N * (rowH + rowGap)) + padBottom;

    let cardX = (actor.startPos ? actor.startPos.x : 640) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 360) - cardH / 2;
    cardX = Math.max(40, Math.min(1280 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(720 - cardH - 40, cardY));

    applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale);

    // Formal parchment tone
    ctx.shadowColor = "rgba(69, 26, 3, 0.08)"; ctx.shadowBlur = 20; ctx.shadowOffsetY = 8;
    ctx.fillStyle = "#FEFDFB";
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, cardH, 14); ctx.fill();
    ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
    ctx.strokeStyle = "rgba(180, 83, 9, 0.35)"; ctx.lineWidth = 1.5; ctx.stroke();

    // Antique Gold Top Rule
    const topBar = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topBar.addColorStop(0, "#B45309"); topBar.addColorStop(0.5, "#D97706"); topBar.addColorStop(1, "#F59E0B");
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, 14, [14, 14, 0, 0]); ctx.clip();
    ctx.fillStyle = topBar; ctx.fillRect(cardX, cardY, cardW, 4);
    ctx.restore();

    // Header Emblem
    ctx.fillStyle = "#FEF3C7"; ctx.beginPath(); ctx.arc(cardX + 34, cardY + 32, 14, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#D97706"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = "#B45309"; ctx.font = "800 13px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("⚖", cardX + 34, cardY + 32);

    ctx.fillStyle = "#78350F";
    ctx.font = "800 13.5px 'Plus Jakarta Sans', serif";
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.letterSpacing = "0.8px";
    ctx.fillText((actor.title || "STATUTORY PROVISIONS").toUpperCase(), cardX + 58, cardY + 32);

    // Right Legal Digest Badge
    const pillW = 96; const pillH = 24;
    const pillX = cardX + cardW - pillW - 20; const pillY = cardY + 20;
    ctx.fillStyle = "#FFFBEB"; ctx.strokeStyle = "#FDE68A"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.roundRect(pillX, pillY, pillW, pillH, 6); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#92400E"; ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${N} CLAUSES`, pillX + pillW / 2, pillY + pillH / 2);

    // Antique Gold Margin Rule separating clause column from text
    const marginX = cardX + 68;
    ctx.strokeStyle = "rgba(217, 119, 6, 0.25)"; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(marginX, cardY + headH); ctx.lineTo(marginX, cardY + cardH - padBottom); ctx.stroke();

    const clauseLetters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)"];

    // Items
    items.forEach((item, idx) => {
      const itStart = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      if (timeMs < itStart) return;

      const itT = isSettle ? 1.0 : Math.min(1.0, (timeMs - itStart) / 350);
      const easeX = isSettle ? 0 : (1.0 - window.TWEEN.ease.easeOutCubic(itT)) * -18;
      const alpha = isSettle ? 1.0 : itT;

      const ry = cardY + headH + idx * (rowH + rowGap);
      const rh = rowH;

      ctx.save();
      ctx.globalAlpha = ctx.globalAlpha * alpha;

      // Clause Marker
      ctx.fillStyle = "#B45309";
      ctx.font = "800 13.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      const marker = clauseLetters[idx % clauseLetters.length];
      ctx.fillText(marker, cardX + 42 + easeX, ry + rh / 2);

      // Row background highlight
      const rx = marginX + 10 + easeX;
      const rw = cardW - (marginX - cardX) - 26;
      ctx.fillStyle = "rgba(254, 243, 199, 0.20)";
      ctx.beginPath(); ctx.roundRect(rx, ry + 2, rw, rh - 4, 8); ctx.fill();

      // Content
      ctx.textAlign = "left"; ctx.textBaseline = "middle";
      if (item.desc) {
        ctx.fillStyle = "#451A03"; ctx.font = "700 13px 'Plus Jakarta Sans', serif";
        ctx.fillText(item.title, rx + 14, ry + 18);

        ctx.fillStyle = "#78350F"; ctx.font = "500 11.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.desc, rx + 14, ry + 36);
      } else {
        ctx.fillStyle = "#451A03"; ctx.font = "700 13.5px 'Plus Jakarta Sans', serif";
        ctx.fillText(item.title || item.text, rx + 14, ry + rh / 2);
      }

      ctx.restore();
    });
  }

  /* --------------------------------------------------------------------------
     DESIGN 4: MINIMAL TWO-TONE PILL CAPSULES ("pills" / "capsules")
     -------------------------------------------------------------------------- */
  function drawListPillsDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale) {
    const cardW = 760;
    const headH = 54;
    const rowH = 48;
    const rowGap = 12;
    const padBottom = 16;
    const cardH = headH + (N * (rowH + rowGap)) + padBottom;

    let cardX = (actor.startPos ? actor.startPos.x : 640) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 360) - cardH / 2;
    cardX = Math.max(40, Math.min(1280 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(720 - cardH - 40, cardY));

    applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale);

    // Clean Container
    ctx.shadowColor = "rgba(15, 23, 42, 0.06)"; ctx.shadowBlur = 16; ctx.shadowOffsetY = 6;
    ctx.fillStyle = "#F8FAFC";
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, cardH, 20); ctx.fill();
    ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
    ctx.strokeStyle = "rgba(226, 232, 240, 0.9)"; ctx.lineWidth = 1.3; ctx.stroke();

    // Header Bar
    ctx.fillStyle = "#0F172A";
    ctx.font = "800 13.5px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.fillText((actor.title || "KEY STATUTORY ELEMENTS").toUpperCase(), cardX + 28, cardY + 28);

    // Right Pill Badge
    const pillW = 80; const pillH = 22;
    const pillX = cardX + cardW - pillW - 24; const pillY = cardY + 17;
    ctx.fillStyle = "#E2E8F0"; ctx.beginPath(); ctx.roundRect(pillX, pillY, pillW, pillH, 11); ctx.fill();
    ctx.fillStyle = "#334155"; ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${N} ITEMS`, pillX + pillW / 2, pillY + pillH / 2);

    // Capsule Rows
    items.forEach((item, idx) => {
      const itStart = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      if (timeMs < itStart) return;

      const itT = isSettle ? 1.0 : Math.min(1.0, (timeMs - itStart) / 350);
      const easeX = isSettle ? 0 : (1.0 - window.TWEEN.ease.easeOutCubic(itT)) * -20;
      const alpha = isSettle ? 1.0 : itT;

      const rx = cardX + 24 + easeX;
      const ry = cardY + headH + idx * (rowH + rowGap);
      const rw = cardW - 48;
      const rh = rowH;
      const radius = rh / 2;

      ctx.save();
      ctx.globalAlpha = ctx.globalAlpha * alpha;

      // Full Capsule Body
      ctx.shadowColor = "rgba(15, 23, 42, 0.04)"; ctx.shadowBlur = 5; ctx.shadowOffsetY = 2;
      ctx.fillStyle = "#FFFFFF";
      ctx.beginPath(); ctx.roundRect(rx, ry, rw, rh, radius); ctx.fill();
      ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
      ctx.strokeStyle = "rgba(203, 213, 225, 0.85)"; ctx.lineWidth = 1.2; ctx.stroke();

      // Left Two-Tone Accent Cap
      const capW = 46;
      ctx.save();
      ctx.beginPath(); ctx.roundRect(rx, ry, rw, rh, radius); ctx.clip();
      const capGrad = ctx.createLinearGradient(rx, ry, rx + capW, ry + rh);
      capGrad.addColorStop(0, "#059669"); capGrad.addColorStop(1, "#10B981");
      ctx.fillStyle = capGrad;
      ctx.fillRect(rx, ry, capW, rh);
      ctx.restore();

      // Cap Number
      ctx.fillStyle = "#FFFFFF";
      ctx.font = "800 12.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(`${idx + 1}`, rx + capW / 2 - 1, ry + rh / 2);

      // Body Text
      const textX = rx + capW + 16;
      ctx.textAlign = "left"; ctx.textBaseline = "middle";

      if (item.desc) {
        ctx.fillStyle = "#0F172A"; ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title, textX, ry + 16);
        ctx.fillStyle = "#64748B"; ctx.font = "500 11.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.desc, textX, ry + 32);
      } else {
        ctx.fillStyle = "#0F172A"; ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title || item.text, textX, ry + rh / 2);
      }

      ctx.restore();
    });
  }

  /* --------------------------------------------------------------------------
     DESIGN 5: OBSIDIAN DARK DECK WITH NEON HORIZON SHEEN ("obsidian" / "dark")
     -------------------------------------------------------------------------- */
  function drawListObsidianDesign(ctx, actor, items, N, timeMs, durationMs, themeColors, isSettle, cardScale) {
    const cardW = 760;
    const headH = 60;
    const rowH = 56;
    const rowGap = 12;
    const padBottom = 18;
    const cardH = headH + (N * (rowH + rowGap)) + padBottom;

    let cardX = (actor.startPos ? actor.startPos.x : 640) - cardW / 2;
    let cardY = (actor.startPos ? actor.startPos.y : 360) - cardH / 2;
    cardX = Math.max(40, Math.min(1280 - cardW - 40, cardX));
    cardY = Math.max(40, Math.min(720 - cardH - 40, cardY));

    applyListScale(ctx, cardX, cardY, cardW, cardH, cardScale);

    // Deep Obsidian Body
    ctx.shadowColor = "rgba(0, 0, 0, 0.45)"; ctx.shadowBlur = 24; ctx.shadowOffsetY = 10;
    const bgGrad = ctx.createLinearGradient(cardX, cardY, cardX, cardY + cardH);
    bgGrad.addColorStop(0, "rgba(15, 23, 42, 0.96)");
    bgGrad.addColorStop(1, "rgba(30, 41, 59, 0.94)");
    ctx.fillStyle = bgGrad;
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, cardH, 16); ctx.fill();
    ctx.shadowColor = "transparent"; ctx.shadowBlur = 0;
    ctx.strokeStyle = "rgba(148, 163, 184, 0.22)"; ctx.lineWidth = 1.5; ctx.stroke();

    // Top Glowing Neon Laser Bar
    const topBar = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    topBar.addColorStop(0, "#10B981"); topBar.addColorStop(0.5, "#06B6D4"); topBar.addColorStop(1, "#3B82F6");
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cardX, cardY, cardW, 16, [16, 16, 0, 0]); ctx.clip();
    ctx.fillStyle = topBar; ctx.fillRect(cardX, cardY, cardW, 3.5);
    ctx.restore();

    // Header
    ctx.fillStyle = "rgba(6, 182, 212, 0.20)";
    ctx.beginPath(); ctx.arc(cardX + 34, cardY + 31, 14, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#06B6D4"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = "#06B6D4"; ctx.font = "800 13px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("◆", cardX + 34, cardY + 31);

    ctx.fillStyle = "#F8FAFC";
    ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.letterSpacing = "0.5px";
    ctx.fillText((actor.title || "STATUTORY DIRECTIVES").toUpperCase(), cardX + 58, cardY + 31);

    // Right Neon Badge
    const pillW = 96; const pillH = 24;
    const pillX = cardX + cardW - pillW - 20; const pillY = cardY + 19;
    ctx.fillStyle = "rgba(15, 23, 42, 0.8)"; ctx.strokeStyle = "#06B6D4"; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.roundRect(pillX, pillY, pillW, pillH, 12); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#38BDF8"; ctx.font = "700 10.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${N} DIRECTIVES`, pillX + pillW / 2, pillY + pillH / 2);

    // Rows
    items.forEach((item, idx) => {
      const itStart = (item.startMs !== undefined && item.startMs !== null) ? item.startMs : (350 + idx * 500);
      if (timeMs < itStart) return;

      const itT = isSettle ? 1.0 : Math.min(1.0, (timeMs - itStart) / 350);
      const easeX = isSettle ? 0 : (1.0 - window.TWEEN.ease.easeOutCubic(itT)) * -22;
      const alpha = isSettle ? 1.0 : itT;

      const rx = cardX + 20 + easeX;
      const ry = cardY + headH + idx * (rowH + rowGap);
      const rw = cardW - 40;
      const rh = rowH;

      ctx.save();
      ctx.globalAlpha = ctx.globalAlpha * alpha;

      // Card Row in deep slate
      ctx.fillStyle = "rgba(30, 41, 59, 0.85)";
      ctx.beginPath(); ctx.roundRect(rx, ry, rw, rh, 10); ctx.fill();
      ctx.strokeStyle = "rgba(148, 163, 184, 0.20)"; ctx.lineWidth = 1.2; ctx.stroke();

      // Glowing Neon Top Accent Edge on each row
      ctx.save();
      ctx.beginPath(); ctx.roundRect(rx, ry, rw, 10, [10, 10, 0, 0]); ctx.clip();
      const rowBar = ctx.createLinearGradient(rx, ry, rx + rw, ry);
      rowBar.addColorStop(0, "#06B6D4"); rowBar.addColorStop(1, "rgba(59, 130, 246, 0.1)");
      ctx.fillStyle = rowBar; ctx.fillRect(rx, ry, rw, 2);
      ctx.restore();

      // Glowing Neon Index Badge
      const bW = 34; const bH = 32;
      const bx = rx + 12; const by = ry + (rh - bH) / 2;
      ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
      ctx.beginPath(); ctx.roundRect(bx, by, bW, bH, 8); ctx.fill();
      ctx.strokeStyle = "#06B6D4"; ctx.lineWidth = 1.3; ctx.stroke();

      ctx.fillStyle = "#38BDF8";
      ctx.font = "800 12.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      const numStr = (idx + 1) < 10 ? `0${idx + 1}` : `${idx + 1}`;
      ctx.fillText(numStr, bx + bW / 2, by + bH / 2);

      // Text
      const textX = bx + bW + 16;
      ctx.textAlign = "left"; ctx.textBaseline = "middle";

      if (item.desc) {
        ctx.fillStyle = "#F8FAFC"; ctx.font = "700 13px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title, textX, ry + 18);

        ctx.fillStyle = "#94A3B8"; ctx.font = "500 11.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.desc, textX, ry + 36);
      } else {
        ctx.fillStyle = "#F8FAFC"; ctx.font = "700 13.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillText(item.title || item.text, textX, ry + rh / 2);
      }

      ctx.restore();
    });
  }

  const MIND_MAP_ROOT_PALETTE = {
    primary: "#6366f1",
    light: "#818cf8",
    glow: "rgba(99, 102, 241, 0.5)",
    bgStart: "rgba(15, 23, 42, 0.95)",
    bgEnd: "rgba(30, 27, 75, 0.90)",
    border: "rgba(129, 140, 248, 0.6)",
    text: "#ffffff",
    badgeBg: "#4338ca",
    badgeText: "#ffffff"
  };

  const MIND_MAP_BRANCH_PALETTES = [
    {
      name: "emerald",
      primary: "#10b981",
      light: "#34d399",
      glow: "rgba(16, 185, 129, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(6, 78, 59, 0.35)",
      border: "rgba(52, 211, 153, 0.5)",
      text: "#ecfdf5",
      badgeBg: "#059669",
      badgeText: "#ffffff"
    },
    {
      name: "sky",
      primary: "#0ea5e9",
      light: "#38bdf8",
      glow: "rgba(14, 165, 233, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(12, 74, 110, 0.35)",
      border: "rgba(56, 189, 248, 0.5)",
      text: "#f0f9ff",
      badgeBg: "#0284c7",
      badgeText: "#ffffff"
    },
    {
      name: "purple",
      primary: "#8b5cf6",
      light: "#a78bfa",
      glow: "rgba(139, 92, 246, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(76, 29, 149, 0.35)",
      border: "rgba(167, 139, 250, 0.5)",
      text: "#f5f3ff",
      badgeBg: "#7c3aed",
      badgeText: "#ffffff"
    },
    {
      name: "amber",
      primary: "#f59e0b",
      light: "#fbbf24",
      glow: "rgba(245, 158, 11, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(120, 53, 15, 0.35)",
      border: "rgba(251, 191, 36, 0.5)",
      text: "#fffbeb",
      badgeBg: "#d97706",
      badgeText: "#ffffff"
    },
    {
      name: "rose",
      primary: "#f43f5e",
      light: "#fb7185",
      glow: "rgba(244, 63, 94, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(136, 19, 55, 0.35)",
      border: "rgba(251, 113, 133, 0.5)",
      text: "#fff1f2",
      badgeBg: "#e11d48",
      badgeText: "#ffffff"
    },
    {
      name: "cyan",
      primary: "#06b6d4",
      light: "#22d3ee",
      glow: "rgba(6, 182, 212, 0.45)",
      bgStart: "rgba(15, 23, 42, 0.94)",
      bgEnd: "rgba(22, 78, 99, 0.35)",
      border: "rgba(34, 211, 238, 0.5)",
      text: "#ecfeff",
      badgeBg: "#0891b2",
      badgeText: "#ffffff"
    }
  ];

  /**
   * Evaluates cubic Bezier curve sub-segment from 0 to u using de Casteljau's algorithm
   */
  function evalBezierSub(p0, p1, p2, p3, u) {
    if (u >= 0.999) return { p0, p1, p2, p3, tip: p3 };
    const lerp = (a, b, t) => ({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t });
    const p01 = lerp(p0, p1, u);
    const p12 = lerp(p1, p2, u);
    const p23 = lerp(p2, p3, u);
    const p012 = lerp(p01, p12, u);
    const p123 = lerp(p12, p23, u);
    const p0123 = lerp(p012, p123, u);
    return {
      p0: p0,
      p1: p01,
      p2: p012,
      p3: p0123,
      tip: p0123
    };
  }

  /**
   * Action Engine & Primitive: Heading Shape
   * Features:
   * - Exclusive slide hero marquee / title card
   * - Masterclass typography: 32px bold Title and 18.5px Subtitle
   * - Unlimited multi-line text wrapping without character or word limits
   * - Top floating decorative category badge ("✦ STATUTORY TOPIC ✦")
   * - Animated glowing horizon separator rule with centered diamond pip
   * - High-end obsidian-sapphire glassmorphism with specular border
   * - Kinetic spring pop-in with staggered subtitle reveal and living sheen
   * - Rock-solid settle hold at p >= 0.65
   */
  function drawHeadingShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    const curX = (actor.startPos && actor.startPos.x !== undefined) ? actor.startPos.x : 640;
    const curY = (actor.startPos && actor.startPos.y !== undefined) ? actor.startPos.y : 360;

    const titleText = (actor.titleText || actor.textLabel || "Statutory Topic").trim();
    const subtitleText = (actor.subtitleText || "").trim();
    const hasSubtitle = subtitleText.length > 0;

    // Relative slide progress p in [0.0, 1.0]
    const p = durationMs > 0 ? Math.min(1.0, Math.max(0.0, timeMs / durationMs)) : 0.0;

    // Intro & Outro Fade Parameters
    const introStart = actor.startMs || 0;
    const introDurationMs = actor.introDurationMs || 600;
    const outroDurationMs = actor.outroDurationMs || 450;

    // Progress boundaries: keep card rock-solid for >= 90% of slide
    const introEndP = Math.min(0.18, (introStart + introDurationMs) / durationMs);
    const outroStartP = Math.max(0.90, 1.0 - (outroDurationMs / durationMs));

    // 1. Calculate Intro Fade
    let introFade = 1.0;
    let introScale = 1.0;
    let introOffsetY = 0.0;

    if (actor.hasIntroFade !== false) {
      if (timeMs < introStart) {
        return; // Not spawned yet
      } else if (p < introEndP) {
        const introProgress = introEndP > 0 ? Math.min(1.0, Math.max(0.0, p / introEndP)) : 1.0;
        const easedIntro = window.TWEEN.ease.easeOutCubic(introProgress);
        introFade = easedIntro;
        introScale = 0.94 + 0.06 * easedIntro;
        introOffsetY = (1.0 - easedIntro) * 14;
      }
    }

    // 2. Calculate Outro Fade
    let outroFade = 1.0;
    let outroScale = 1.0;
    let outroOffsetY = 0.0;

    if (actor.hasOutroFade !== false) {
      if (p >= outroStartP) {
        const outroDurP = Math.max(0.02, 1.0 - outroStartP);
        const outroProgress = Math.min(1.0, Math.max(0.0, (p - outroStartP) / outroDurP));
        const easedOutro = window.TWEEN.ease.easeInOutCubic(outroProgress);
        outroFade = Math.max(0.0, 1.0 - easedOutro);
        outroScale = 1.0 - 0.04 * easedOutro;
        outroOffsetY = easedOutro * 12;
      }
    }

    // 3. Combined Total Alpha & Transform
    const totalAlpha = Math.max(0.0, Math.min(1.0, introFade * outroFade));
    if (totalAlpha <= 0.001) return; // Completely invisible / dissolved

    const totalScale = introScale * outroScale;
    const totalOffsetY = introOffsetY + outroOffsetY;

    // Subtitle Staggered Intro Fade
    const subDelay = actor.subtitleDelayMs || 450;
    const subIntroStart = introStart + subDelay;
    const subIntroDur = 450;
    let subIntroFade = 1.0;
    if (timeMs < subIntroStart) {
      subIntroFade = 0.0;
    } else if (timeMs < subIntroStart + subIntroDur) {
      subIntroFade = window.TWEEN.ease.easeOutCubic((timeMs - subIntroStart) / subIntroDur);
    }

    // Dynamic sizing and word wrapping
    const maxTextW = 860;
    const titleFont = "800 32px 'Inter', -apple-system, sans-serif";
    const subFont = "600 18.5px 'Inter', -apple-system, sans-serif";

    const titleLines = wrapMindMapText(ctx, titleText, maxTextW, titleFont);
    const subLines = hasSubtitle ? wrapMindMapText(ctx, subtitleText, maxTextW, subFont) : [];

    const titleLineH = 40;
    const subLineH = 26;
    const titleBlockH = titleLines.length * titleLineH;
    const subBlockH = subLines.length * subLineH;

    // Measure maximum line width to size the card proportionally
    let maxMeasuredW = 0;
    if (ctx && ctx.measureText) {
      ctx.save();
      ctx.font = titleFont;
      titleLines.forEach(l => {
        const mw = ctx.measureText(l).width;
        if (mw > maxMeasuredW) maxMeasuredW = mw;
      });
      if (hasSubtitle) {
        ctx.font = subFont;
        subLines.forEach(l => {
          const mw = ctx.measureText(l).width;
          if (mw > maxMeasuredW) maxMeasuredW = mw;
        });
      }
      ctx.restore();
    } else {
      maxMeasuredW = 500;
    }

    const cardW = Math.max(720, Math.min(1040, Math.round(maxMeasuredW + 150)));
    const pillH = 26;
    const pillTopMargin = 28;
    const pillBottomGap = 20;

    let cardH;
    if (hasSubtitle) {
      cardH = pillTopMargin + pillH + pillBottomGap + titleBlockH + 20 + 2 + 20 + subBlockH + 34;
    } else {
      cardH = pillTopMargin + pillH + pillBottomGap + titleBlockH + 38;
    }
    cardH = Math.max(hasSubtitle ? 250 : 200, cardH);

    ctx.save();
    ctx.globalAlpha = totalAlpha;
    ctx.translate(curX, curY + totalOffsetY);

    if (totalScale !== 1.0) {
      ctx.scale(totalScale, totalScale);
    }

    const rx = -cardW / 2;
    const ry = -cardH / 2;
    const radius = 20;

    // 1. Ambient outer glow & shadow
    ctx.shadowColor = "rgba(0, 0, 0, 0.58)";
    ctx.shadowBlur = 28;
    ctx.shadowOffsetY = 12;

    // 2. Glassmorphism Gradient Background (Obsidian-Sapphire)
    const bgGrad = ctx.createLinearGradient(rx, ry, rx + cardW * 0.4, ry + cardH);
    bgGrad.addColorStop(0.0, "rgba(15, 23, 42, 0.98)");
    bgGrad.addColorStop(0.5, "rgba(24, 30, 72, 0.95)");
    bgGrad.addColorStop(1.0, "rgba(15, 23, 42, 0.98)");
    ctx.fillStyle = bgGrad;
    ctx.beginPath();
    ctx.roundRect(rx, ry, cardW, cardH, radius);
    ctx.fill();

    // 3. Specular Border with Top Highlight
    ctx.shadowColor = "transparent";
    const borderGrad = ctx.createLinearGradient(rx, ry, rx, ry + cardH);
    borderGrad.addColorStop(0.0, "rgba(165, 180, 252, 0.85)");
    borderGrad.addColorStop(0.4, "rgba(129, 140, 248, 0.40)");
    borderGrad.addColorStop(1.0, "rgba(99, 102, 241, 0.20)");
    ctx.strokeStyle = borderGrad;
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.roundRect(rx, ry, cardW, cardH, radius);
    ctx.stroke();

    // 4. Subtle Top Illumination Glow Line
    ctx.save();
    ctx.strokeStyle = "rgba(165, 180, 252, 0.9)";
    ctx.lineWidth = 2.5;
    ctx.shadowColor = "rgba(129, 140, 248, 0.8)";
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.moveTo(rx + 40, ry);
    ctx.lineTo(rx + cardW - 40, ry);
    ctx.stroke();
    ctx.restore();

    // 5. Four Decorative Corner Notches
    ctx.save();
    ctx.strokeStyle = "rgba(129, 140, 248, 0.6)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(rx + 10, ry + 24);
    ctx.lineTo(rx + 10, ry + 10);
    ctx.lineTo(rx + 24, ry + 10);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(rx + cardW - 10, ry + 24);
    ctx.lineTo(rx + cardW - 10, ry + 10);
    ctx.lineTo(rx + cardW - 24, ry + 10);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(rx + 10, ry + cardH - 24);
    ctx.lineTo(rx + 10, ry + cardH - 10);
    ctx.lineTo(rx + 24, ry + cardH - 10);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(rx + cardW - 10, ry + cardH - 24);
    ctx.lineTo(rx + cardW - 10, ry + cardH - 10);
    ctx.lineTo(rx + cardW - 24, ry + cardH - 10);
    ctx.stroke();
    ctx.restore();

    // 6. Top Floating Decorative Category Pill ("✦ STATUTORY TOPIC ✦")
    const pillW = 210;
    const pillY = ry + pillTopMargin;
    const pillX = -pillW / 2;

    ctx.save();
    const pillGrad = ctx.createLinearGradient(pillX, pillY, pillX, pillY + pillH);
    pillGrad.addColorStop(0, "rgba(99, 102, 241, 0.32)");
    pillGrad.addColorStop(1, "rgba(67, 56, 202, 0.20)");
    ctx.fillStyle = pillGrad;
    ctx.strokeStyle = "rgba(129, 140, 248, 0.55)";
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.roundRect(pillX, pillY, pillW, pillH, pillH / 2);
    ctx.fill();
    ctx.stroke();

    // Glowing micro spark icon
    ctx.fillStyle = "#38BDF8";
    ctx.shadowColor = "#38BDF8";
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.arc(pillX + 18, pillY + pillH / 2, 3, 0, Math.PI * 2);
    ctx.fill();

    // Pill label text
    ctx.shadowColor = "transparent";
    ctx.fillStyle = "#C7D2FE";
    ctx.font = "700 11px 'Inter', -apple-system, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.letterSpacing = "1.5px";
    ctx.fillText("✦ STATUTORY TOPIC ✦", 6, pillY + pillH / 2);
    ctx.restore();

    // 7. Render Main Title Lines
    const titleStartY = pillY + pillH + pillBottomGap + (titleLineH / 2);

    ctx.save();
    ctx.font = titleFont;
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.shadowColor = "rgba(0, 0, 0, 0.65)";
    ctx.shadowBlur = 8;
    ctx.shadowOffsetY = 3;

    titleLines.forEach((tLine, idx) => {
      const lineY = titleStartY + idx * titleLineH;
      ctx.fillText(tLine, 0, lineY);
    });
    ctx.restore();

    // 8. Render Separator Rule & Subtitle (if subtitle exists)
    if (hasSubtitle && subIntroFade > 0.001) {
      const sepY = titleStartY + (titleLines.length - 1) * titleLineH + titleLineH / 2 + 20;

      ctx.save();
      ctx.globalAlpha = totalAlpha * subIntroFade;

      // Separator rule width animation
      const maxSepW = Math.min(520, cardW - 140);
      const curSepW = subIntroFade * maxSepW;
      const sepX1 = -curSepW / 2;
      const sepX2 = curSepW / 2;

      // Gradient rule fading at both ends
      const ruleGrad = ctx.createLinearGradient(sepX1, sepY, sepX2, sepY);
      ruleGrad.addColorStop(0.0, "rgba(129, 140, 248, 0.0)");
      ruleGrad.addColorStop(0.15, "rgba(129, 140, 248, 0.45)");
      ruleGrad.addColorStop(0.5, "rgba(165, 180, 252, 0.90)");
      ruleGrad.addColorStop(0.85, "rgba(129, 140, 248, 0.45)");
      ruleGrad.addColorStop(1.0, "rgba(129, 140, 248, 0.0)");

      ctx.strokeStyle = ruleGrad;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(sepX1, sepY);
      ctx.lineTo(sepX2, sepY);
      ctx.stroke();

      // Center glowing jewel / diamond pip
      ctx.fillStyle = "#818CF8";
      ctx.shadowColor = "rgba(129, 140, 248, 0.9)";
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.arc(0, sepY, 3, 0, Math.PI * 2);
      ctx.fill();

      // Living sheen pulse gliding along separator rule
      const sheenPhase = ((timeMs % 3200) / 3200);
      if (sheenPhase > 0.05 && sheenPhase < 0.95) {
        const sheenX = sepX1 + (sepX2 - sepX1) * sheenPhase;
        ctx.fillStyle = "#FFFFFF";
        ctx.shadowColor = "#38BDF8";
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(sheenX, sepY, 2, 0, Math.PI * 2);
        ctx.fill();
      }

      // Subtitle lines
      const subStartY = sepY + 22 + (subLineH / 2);
      const subOffsetY = (1.0 - subIntroFade) * 10;

      ctx.shadowColor = "transparent";
      ctx.font = subFont;
      ctx.fillStyle = "#94A3B8";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.letterSpacing = "0.2px";

      subLines.forEach((sLine, sIdx) => {
        const lineY = subStartY + sIdx * subLineH - subOffsetY;
        ctx.fillText(sLine, 0, lineY);
      });

      ctx.restore();
    }

    ctx.restore();
  }

  /**
   * Renders the Mind Map Shape:
   * Features:
   * - Hierarchical dot-notation tree layout (Root Level 1, Main Branches Level 2, Sub-branches Level 3+)
   * - Sequential relative timing accumulation from previous item
   * - Organic animated curved Bezier conduits with growing lines and energy pulse particles
   * - Glassmorphism cards with level-specific styling, numbering badges, and spring pop-in
   */
  function drawMindMapShape(ctx, actor, timeMs, durationMs, themeColors, isSettle) {
    if (!actor.totalTimelineMs) {
      computeMindMapTimeline(actor);
    }
    if (!actor._laidOut) {
      layoutMindMapNodes(actor, 1280, 720, ctx);
      actor._laidOut = true;
    }

    const nodes = actor.nodes || [];
    if (nodes.length === 0) return;

    const nodeMap = {};
    nodes.forEach(n => {
      nodeMap[n.code] = n;
    });

    // 1. Draw connecting curved Bezier conduits first (beneath cards)
    nodes.forEach(C => {
      if (!C.parentCode || !nodeMap[C.parentCode]) return;
      const P = nodeMap[C.parentCode];

      // Growth starts 350ms before child node enters
      const lineIntroStart = Math.max(0, C.startMs - 350);
      const lineT = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - lineIntroStart) / 350));
      if (lineT <= 0.001) return;

      const palette = C.level === 1 ? MIND_MAP_ROOT_PALETTE : MIND_MAP_BRANCH_PALETTES[C.branchIndex % MIND_MAP_BRANCH_PALETTES.length];

      const p0 = { x: P.x + P.w / 2, y: P.y };
      const p3 = { x: C.x - C.w / 2, y: C.y };
      const dx = p3.x - p0.x;
      const p1 = { x: p0.x + dx * 0.5, y: p0.y };
      const p2 = { x: p3.x - dx * 0.5, y: p3.y };

      const sub = evalBezierSub(p0, p1, p2, p3, lineT);

      ctx.save();
      ctx.strokeStyle = palette.light;
      ctx.lineWidth = C.level === 2 ? 2.8 : 2.0;
      ctx.shadowColor = palette.glow;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.moveTo(sub.p0.x, sub.p0.y);
      ctx.bezierCurveTo(sub.p1.x, sub.p1.y, sub.p2.x, sub.p2.y, sub.p3.x, sub.p3.y);
      ctx.stroke();

      // Glowing tip while branch is growing
      if (!isSettle && lineT < 1.0 && lineT > 0.05) {
        ctx.fillStyle = "#ffffff";
        ctx.shadowColor = palette.light;
        ctx.shadowBlur = 14;
        ctx.beginPath();
        ctx.arc(sub.tip.x, sub.tip.y, 4, 0, Math.PI * 2);
        ctx.fill();
      }

      // Living energy pulse traveling along settled branches
      if (lineT >= 0.999) {
        const pulseCycle = 2600;
        const pulsePhase = ((timeMs + (C.branchIndex || 0) * 450) % pulseCycle) / pulseCycle;
        if (pulsePhase > 0.02 && pulsePhase < 0.98) {
          const pt = evalBezierSub(p0, p1, p2, p3, pulsePhase).tip;
          ctx.fillStyle = "#ffffff";
          ctx.shadowColor = palette.light;
          ctx.shadowBlur = 8;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      ctx.restore();
    });

    // 2. Draw node cards
    nodes.forEach(N => {
      const cardIntroStart = N.startMs || 0;
      const cardT = isSettle ? 1.0 : Math.min(1.0, Math.max(0.0, (timeMs - cardIntroStart) / 380));
      if (cardT <= 0.001) return;

      const scale = isSettle ? 1.0 : window.TWEEN.ease.easeOutBack(cardT);
      const alpha = isSettle ? 1.0 : Math.min(1.0, cardT * 1.5);
      const palette = N.level === 1 ? MIND_MAP_ROOT_PALETTE : MIND_MAP_BRANCH_PALETTES[N.branchIndex % MIND_MAP_BRANCH_PALETTES.length];

      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(N.x, N.y);
      if (!isSettle && scale !== 1.0) {
        ctx.scale(scale, scale);
      }

      const rx = -N.w / 2;
      const ry = -N.h / 2;
      const radius = N.level === 1 ? 12 : (N.level === 2 ? 10 : 8);

      // Card drop shadow
      ctx.shadowColor = "rgba(0, 0, 0, 0.42)";
      ctx.shadowBlur = N.level === 1 ? 20 : 12;
      ctx.shadowOffsetY = 6;

      // Glassmorphism background gradient
      const bgGrad = ctx.createLinearGradient(rx, ry, rx, ry + N.h);
      bgGrad.addColorStop(0, palette.bgStart);
      bgGrad.addColorStop(1, palette.bgEnd);
      ctx.fillStyle = bgGrad;
      ctx.beginPath();
      ctx.roundRect(rx, ry, N.w, N.h, radius);
      ctx.fill();

      // Card border
      ctx.shadowColor = "transparent";
      ctx.strokeStyle = palette.border;
      ctx.lineWidth = N.level === 1 ? 2.0 : 1.5;
      ctx.beginPath();
      ctx.roundRect(rx, ry, N.w, N.h, radius);
      ctx.stroke();

      // Accent highlights: Top glow stripe for Root, Left bar for Branches
      if (N.level === 1) {
        ctx.save();
        ctx.strokeStyle = palette.light;
        ctx.lineWidth = 2.5;
        ctx.shadowColor = palette.glow;
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.moveTo(rx + 16, ry);
        ctx.lineTo(rx + N.w - 16, ry);
        ctx.stroke();
        ctx.restore();
      } else {
        ctx.save();
        ctx.fillStyle = palette.primary;
        ctx.shadowColor = palette.glow;
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.roundRect(rx, ry, 4, N.h, [radius, 0, 0, radius]);
        ctx.fill();
        ctx.restore();
      }

      // Node text label: multi-line rendering with centered vertical alignment (no text limit)
      const lines = N.lines || [N.text || ""];
      const lineCount = lines.length;
      const lineHeight = N.level === 1 ? 22 : (N.level === 2 ? 19.5 : 17.5);
      const totalBlockH = (lineCount - 1) * lineHeight;
      const startTextY = -totalBlockH / 2;

      ctx.font = N.level === 1 ? "700 17.5px 'Inter', -apple-system, sans-serif" :
                (N.level === 2 ? "600 15px 'Inter', -apple-system, sans-serif" :
                                 "600 13.5px 'Inter', -apple-system, sans-serif");
      ctx.fillStyle = "#ffffff";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      const textOffsetX = N.level > 1 ? 2 : 0;
      lines.forEach((lineStr, lineIdx) => {
        const lineY = startTextY + lineIdx * lineHeight;
        ctx.fillText(lineStr, textOffsetX, lineY);
      });

      // Connector port dots
      if (N.children && N.children.length > 0) {
        ctx.fillStyle = palette.light;
        ctx.shadowColor = palette.glow;
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(N.w / 2, 0, 3.5, 0, Math.PI * 2);
        ctx.fill();
      }
      if (N.parentCode) {
        ctx.fillStyle = palette.light;
        ctx.shadowColor = palette.glow;
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(-N.w / 2, 0, 3.5, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    });
  }

  /**
   * Action Engine: custom_script_engine
   * Renders the parsed actors, handling intro easing, motion translation,
   * dashed transit conduits, and distinct pictorial vector silhouettes.
   */
  function renderCustomScriptEngine(ctx, payload = {}, bounds, phaseState, themeColors) {
    const actors = payload.actors || [];
    const p = phaseState.progress;
    const isSettle = p >= 0.98;
    const effectiveP = isSettle ? 1.0 : window.TWEEN.remap(p, 0.10, 0.98, 0, 1);
    const durationMs = payload.duration_ms || 5400;
    const timeMs = p * durationMs;

    ctx.save();

    // EXCLUSIVITY: If this slide contains a Heading shape, render ONLY the Heading shape!
    // No other shapes, motion conduits, or avatars are permitted on this slide.
    const headingActor = actors.find(a => a.isHeading || a.shapeType === "heading" || a.shapeType === "title");
    if (headingActor) {
      drawHeadingShape(ctx, headingActor, timeMs, durationMs, themeColors, isSettle);
      ctx.restore();
      return;
    }

    // 1. Draw motion conduit trails for all moving or popping actors
    actors.forEach(actor => {
      // Pop-up animated curved conduit while popping out from parent anchor
      if (actor.popup && actor.popup.active && timeMs >= (actor.startMs || 0)) {
        const { from, to } = actor.popup;
        const timeSinceSpawn = timeMs - (actor.startMs || 0);
        const popupDur = actor.popup.durationMs || 950;
        const trailDuration = popupDur + 500;
        if (timeSinceSpawn < trailDuration) {
          const fadeProgress = Math.min(1.0, timeSinceSpawn / trailDuration);
          const trailAlpha = Math.max(0.0, 1.0 - fadeProgress) * 0.7;

          ctx.save();
          ctx.strokeStyle = `rgba(99, 102, 241, ${trailAlpha})`;
          ctx.lineWidth = 2.5;
          ctx.setLineDash([5, 5]);
          ctx.beginPath();
          ctx.moveTo(from.x, from.y);
          const cpX = (from.x + to.x) / 2;
          const cpY = Math.min(from.y, to.y) - 35;
          ctx.quadraticCurveTo(cpX, cpY, to.x, to.y);
          ctx.stroke();
          ctx.setLineDash([]);

          // Glowing energy particle traveling along the conduit
          const dotT = Math.min(1.0, timeSinceSpawn / popupDur);
          const invT = 1 - dotT;
          const dotX = invT * invT * from.x + 2 * invT * dotT * cpX + dotT * dotT * to.x;
          const dotY = invT * invT * from.y + 2 * invT * dotT * cpY + dotT * dotT * to.y;
          ctx.fillStyle = `rgba(56, 189, 248, ${trailAlpha})`;
          ctx.shadowColor = "#38BDF8";
          ctx.shadowBlur = 10;
          ctx.beginPath();
          ctx.arc(dotX, dotY, 4.5, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();
        }
      }

      if (actor.motion && actor.motion.hasMotion && timeMs >= (actor.startMs || 0)) {
        const { from, to } = actor.motion;
        ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 6]);
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.stroke();
        ctx.setLineDash([]);

        // Small transit directional arrow in the middle
        const midX = (from.x + to.x) / 2;
        const midY = (from.y + to.y) / 2;
        const angle = Math.atan2(to.y - from.y, to.x - from.x);
        ctx.save();
        ctx.translate(midX, midY);
        ctx.rotate(angle);
        ctx.fillStyle = "#94A3B8";
        ctx.beginPath();
        ctx.moveTo(8, 0);
        ctx.lineTo(-6, -5);
        ctx.lineTo(-6, 5);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      }
    });

    // 2. Render each actor card / token
    actors.forEach((actor, aIdx) => {
      if (actor.isMindMap || actor.shapeType === "mind" || actor.shapeType === "mindmap") {
        drawMindMapShape(ctx, actor, timeMs, durationMs, themeColors, isSettle);
        return;
      }
      if (actor.isChecklist || actor.shapeType === "checklist") {
        drawChecklistShape(ctx, actor, timeMs, durationMs, themeColors, isSettle);
        return;
      }
      if (actor.isList || actor.shapeType === "list") {
        drawListShape(ctx, actor, timeMs, durationMs, themeColors, isSettle);
        return;
      }
      if (actor.isCalculationSingle || actor.shapeType === "calculation_single") {
        drawCalculationSingleShape(ctx, actor, timeMs, durationMs, themeColors, isSettle);
        return;
      }
      if (actor.isCalculation || actor.shapeType === "calculation_multiple") {
        drawCalculationMultipleShape(ctx, actor, timeMs, durationMs, themeColors, isSettle);
        return;
      }

      const { shapeType, textLabel, icon, accent, startPos, intro, motion, popup } = actor;

      // Current position interpolation
      let curX = startPos.x;
      let curY = startPos.y;

      // Actor Appearance Gate:
      // In a slide, don't show every shape at once!
      // Next shape only appears after the dialogue voice of the previous shape is complete.
      const actorStartMs = actor.startMs !== undefined ? actor.startMs : (aIdx * 150);
      if (timeMs < actorStartMs) {
        return; // NOT SPAWNED YET! Remain completely hidden until its turn.
      }

      const introDurationMs = 500;
      let introT = 1.0;
      let introScale = 1.0;
      let introAlpha = 1.0;
      let introOffsetY = 0;

      const timeSinceSpawn = timeMs - actorStartMs;

      // A. Pop-Up Motion & Elastic Entrance
      if (popup && popup.active) {
        const popupDur = popup.durationMs || 950;
        if (timeSinceSpawn < popupDur) {
          const t = Math.min(1.0, Math.max(0.0, timeSinceSpawn / popupDur));
          const easedPos = window.TWEEN.ease.easeOutCubic(t);
          curX = window.TWEEN.lerp(popup.from.x, popup.to.x, easedPos);
          curY = window.TWEEN.lerp(popup.from.y, popup.to.y, easedPos);

          const scaleT = Math.min(1.0, t * 1.25);
          introScale = 0.25 + 0.75 * window.TWEEN.ease.easeOutBack(scaleT);
          introAlpha = Math.min(1.0, t * 2.5);
        } else {
          curX = popup.to.x;
          curY = popup.to.y;
          introScale = 1.0;
          introAlpha = 1.0;
        }
      } else if (motion && motion.hasMotion) {
        if (timeMs >= motion.endMs) {
          curX = motion.to.x;
          curY = motion.to.y;
        } else if (timeMs >= motion.startMs) {
          const t = (timeMs - motion.startMs) / (motion.endMs - motion.startMs);
          const easedT = window.TWEEN.ease.easeInOutCubic(Math.min(1.0, Math.max(0.0, t)));
          curX = window.TWEEN.lerp(motion.from.x, motion.to.x, easedT);
          curY = window.TWEEN.lerp(motion.from.y, motion.to.y, easedT);
        } else {
          curX = motion.from.x;
          curY = motion.from.y;
        }
      }

      if (!popup || !popup.active) {
        if (timeSinceSpawn < introDurationMs) {
          introT = Math.min(1.0, Math.max(0.0, timeSinceSpawn / introDurationMs));
          if (intro.includes("fade")) {
            introAlpha = introT;
          } else if (intro.includes("pop") || intro.includes("scale")) {
            introAlpha = Math.min(1.0, introT * 1.5);
            introScale = window.TWEEN.ease.easeOutBack(introT);
          } else if (intro.includes("drop") || intro.includes("fall")) {
            introAlpha = Math.min(1.0, introT * 1.5);
            introOffsetY = (1.0 - window.TWEEN.ease.easeOutBack(introT)) * -40;
          } else if (intro.includes("slide")) {
            introAlpha = introT;
            introOffsetY = (1.0 - window.TWEEN.ease.easeOutCubic(introT)) * 25;
          }
        }
      }

      ctx.save();
      ctx.globalAlpha = introAlpha;
      ctx.translate(curX, curY + introOffsetY);
      
      // Professional scale boost (1.45x) so shapes boldly fill the enlarged canvas area
      const shapeScale = 1.45;
      const combinedScale = introScale * shapeScale;
      ctx.scale(combinedScale, combinedScale);

      const accentTheme = (window.THEME && window.THEME.colors.accent[accent]) ||
                          (window.THEME ? window.THEME.colors.accent.indigo : { main: "#4F46E5", light: "#EEF2FF", border: "#C7D2FE", dark: "#3730A3" });

      const isPill = shapeType.toLowerCase() === "pill" || shapeType.toLowerCase() === "badge";

      if (isPill) {
        // Render as clean, prominent Pill / Stamp Chip
        const pillText = textLabel.toUpperCase();
        ctx.font = window.THEME ? window.THEME.typography.monoBadge : "700 11.5px monospace";
        const textW = ctx.measureText(pillText).width;
        const pillW = Math.max(160, Math.min(textW + 48, 380));
        const pillH = 38;

        ctx.fillStyle = accentTheme.light;
        ctx.strokeStyle = accentTheme.border;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(-pillW / 2, -pillH / 2, pillW, pillH, 19);
        ctx.fill();
        ctx.stroke();

        if (window.ICONS) {
          window.ICONS.draw(ctx, icon || "checkCircle", -pillW / 2 + 18, 0, 16, accentTheme.main);
        }

        ctx.fillStyle = accentTheme.dark || accentTheme.main;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(pillText, 6, 0);

      } else {
        // Dispatch to custom colorful silhouette, handcrafted figure, or 2,098-icon colorful badge
        const custom = actor.customRenderer;
        const cat = (actor.shapeCategory || actor.shapeType || "").toLowerCase();
        const typeStr = (actor.shapeType || "").toLowerCase();

        // Universal dynamic dispatch via SHAPE_CATALOG
        let rendered = false;

        if (window.SHAPE_CATALOG) {
          if (custom && typeof window.SHAPE_CATALOG.drawShape === "function") {
            rendered = window.SHAPE_CATALOG.drawShape(ctx, custom, accentTheme);
          }
          if (!rendered && (typeStr || cat) && typeof window.SHAPE_CATALOG.drawShape === "function") {
            rendered = window.SHAPE_CATALOG.drawShape(ctx, typeStr || cat, accentTheme);
          }
        }

        // Secondary fallback to legacy handcrafted shapes if not rendered
        if (!rendered) {
          if (custom === "cheque" && window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawChequeShape) {
            window.SHAPE_CATALOG.drawChequeShape(ctx, accentTheme, false);
            rendered = true;
          } else if (custom === "cheque_crossed" && window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawChequeShape) {
            window.SHAPE_CATALOG.drawChequeShape(ctx, accentTheme, true);
            rendered = true;
          } else if ((custom === "building" || typeStr.includes("building") || typeStr.includes("office") || typeStr.includes("tower") || typeStr.includes("complex") || cat.includes("factory") || cat.includes("building") || cat.includes("court") || cat.includes("store") || cat.includes("shop") || cat.includes("bank") || cat.includes("office") || cat.includes("depot")) && window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawBuildingShape) {
            window.SHAPE_CATALOG.drawBuildingShape(ctx, typeStr || cat, accentTheme);
            rendered = true;
          } else if (cat.includes("cloth") || cat.includes("fabric") || cat.includes("textile") || cat.includes("clothes") || cat.includes("coat") || cat.includes("shirt") || cat.includes("dress") || cat.includes("suit") || cat.includes("garment") || cat.includes("apparel")) {
            (window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawClothesShape ? window.SHAPE_CATALOG.drawClothesShape(ctx, cat, accentTheme) : drawClothesShape(ctx, cat, accentTheme, themeColors));
            rendered = true;
          } else if (cat.includes("box") || cat.includes("package") || cat.includes("cargo") || cat.includes("parcel") || cat.includes("goods") || cat.includes("crate")) {
            (window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawGoodsBoxShape ? window.SHAPE_CATALOG.drawGoodsBoxShape(ctx, accentTheme) : drawGoodsBoxShape(ctx, accentTheme, themeColors));
            rendered = true;
          } else if (cat.includes("scale") || cat.includes("gavel") || cat.includes("document") || cat.includes("contract") || cat.includes("money") || cat.includes("cash") || cat.includes("deed") || cat.includes("jewel") || cat.includes("gold")) {
            (window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawLegalSymbolShape ? window.SHAPE_CATALOG.drawLegalSymbolShape(ctx, cat, accentTheme) : drawLegalSymbolShape(ctx, cat, accentTheme, themeColors));
            rendered = true;
          }
        }

        // Final fallback: Colorful Lucide squircle icon or generic badge
        if (!rendered) {
          if (window.drawColorfulBadgeShape && actor.icon && window.COLORFUL_SHAPES_DATA && window.COLORFUL_SHAPES_DATA[actor.icon]) {
            window.drawColorfulBadgeShape(ctx, actor.icon, 0, -14, 28, actor.accent || "indigo", "squircle");
          } else {
            drawGenericBadgeShape(ctx, actor.icon || "package", accentTheme, themeColors);
          }
        }

        // Draw Status Overlay if present (e.g. [damaged], [locked], [stamped], [crossed], [warning])
        if (actor.overlay && window.SHAPE_CATALOG && window.SHAPE_CATALOG.drawOverlay) {
          window.SHAPE_CATALOG.drawOverlay(ctx, actor.overlay);
        }

        // Floating Label Chip underneath with category badge and cleanly wrapped name
        drawFloatingLabelChip(ctx, textLabel, actor.category, accentTheme, themeColors);
      }

      ctx.restore();
    });

    ctx.restore();
  }

  // Register engine with studio
  window.ACTION_ENGINES = window.ACTION_ENGINES || {};
  window.ACTION_ENGINES.custom_script_engine = renderCustomScriptEngine;

  // Sample Bailment script for 1-click loading
  const SAMPLE_SCRIPT = `NARRATION: "Mr. Arjun delivers his car to Apex Auto Repairs for servicing, creating a statutory contract of bailment under Section 148."

shape (Man) (Arjun - Bailor) (left top) (fade) (stay)
shape (Factory) (Apex Auto Repairs - Bailee) (right top) (fade) (stay)
shape (Car) (Honda City KA-01) (left center) (pop) (Movement to Right, after 1 second, right center)
shape (Document) (Bailment Job Card) (center top) (drop, after 1.5 seconds) (stay)
shape (Pill) (Section 148: Temporary Possession Delivered) (center bottom) (drop, after 2.5 seconds) (stay)`;

  // Script Studio UI Controller
  const SCRIPT_STUDIO = {
    parse: parseScriptPrompt,

    loadSample() {
      const textarea = document.getElementById("script_prompt_input");
      if (textarea) {
        textarea.value = SAMPLE_SCRIPT;
      }
    },

    clear() {
      const textarea = document.getElementById("script_prompt_input");
      if (textarea) textarea.value = "";
    },

    runPresentation() {
      const textarea = document.getElementById("script_prompt_input");
      if (!textarea) return;

      const raw = textarea.value.trim();
      if (!raw) {
        alert("Please paste or type your shape prompt lines first!");
        return;
      }

      const presentationData = parseScriptPrompt(raw);
      if (!presentationData || !presentationData.scenes || presentationData.scenes.length === 0) {
        alert("No valid shape lines detected! Make sure lines start with: shape (...) (...) (...) (...) (...)");
        return;
      }

      // Show stage and initialize player
      const animSection = document.getElementById("animation_section");
      if (animSection) {
        animSection.style.display = "flex";
      }

      if (window.PRESENTATION_PLAYER) {
        window.PRESENTATION_PLAYER.init("stage_canvas");
        window.PRESENTATION_PLAYER.loadPresentation(presentationData);
        window.PRESENTATION_PLAYER.isPlaying = true;
      }

      animSection.scrollIntoView({ behavior: "smooth" });
    },

    switchMode(mode) {
      const btnLaw = document.getElementById("tab_btn_law");
      const btnScript = document.getElementById("tab_btn_script");
      const lawSection = document.getElementById("input_section");
      const storyReview = document.getElementById("output_section");
      const scriptSection = document.getElementById("prompt_studio_section");
      const animSection = document.getElementById("animation_section");

      if (mode === "script") {
        if (btnLaw) btnLaw.classList.remove("active");
        if (btnScript) btnScript.classList.add("active");
        if (lawSection) lawSection.style.display = "none";
        if (storyReview) storyReview.style.display = "none";
        if (scriptSection) scriptSection.style.display = "flex";
      } else {
        if (btnScript) btnScript.classList.remove("active");
        if (btnLaw) btnLaw.classList.add("active");
        if (scriptSection) scriptSection.style.display = "none";
        if (lawSection) lawSection.style.display = "flex";
      }
    },

    toggleShapeCatalog() {
      const drawer = document.getElementById("shape_catalog_drawer");
      if (!drawer) return;
      const isActive = drawer.classList.toggle("active");
      if (isActive) {
        this.initCatalogUI();
      }
    },

    insertShape(shapeName) {
      const textarea = document.getElementById("script_prompt_input");
      if (!textarea) return;

      const isOverlay = shapeName.startsWith("[");
      let insertText = "";
      if (isOverlay) {
        insertText = ` ${shapeName}`;
      } else if (shapeName.toLowerCase().includes("calculation")) {
        insertText = `shape (calculation (multiple)) (+) (Full Value of Consideration) (10,00,000) (center)\nshape (calculation (multiple)) (-) (Cost of Acquisition) (4,00,000)\nshape (calculation (multiple)) (-) (Exemption under Section 54) (3,00,000)\nshape (calculation (multiple)) (=) (Taxable Long Term Capital Gains) (3,00,000)\n`;
      } else {
        const readableLabel = shapeName.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
        insertText = `shape (${shapeName}) (${readableLabel}) (center) (drop) (stay)\n`;
      }

      const start = textarea.selectionStart || 0;
      const end = textarea.selectionEnd || 0;
      const val = textarea.value;

      textarea.value = val.substring(0, start) + insertText + val.substring(end);
      textarea.focus();
      const newPos = start + insertText.length;
      textarea.setSelectionRange(newPos, newPos);
    },

    initCatalogUI() {
      const grid = document.getElementById("shape_catalog_grid");
      if (!grid || grid.children.length > 0) return; // already initialized

      if (!window.SHAPE_CATALOG) return;

      const { CATEGORIES, REGISTRY, OVERLAYS } = window.SHAPE_CATALOG;

      // Group registry items by category
      const byCat = {};
      Object.keys(CATEGORIES).forEach(c => { byCat[c] = new Set(); });

      Object.values(REGISTRY).forEach(entry => {
        if (byCat[entry.category]) {
          byCat[entry.category].add(entry.key);
        }
      });

      // Render cards for each category
      Object.keys(CATEGORIES).forEach(catId => {
        const catInfo = CATEGORIES[catId];
        const shapes = Array.from(byCat[catId] || []);
        if (shapes.length === 0 && catId !== "overlays") return;

        const card = document.createElement("div");
        card.className = "shape-cat-card";

        if (catId === "overlays") {
          const overlayKeys = Object.keys(OVERLAYS || {});
          card.innerHTML = `
            <div class="shape-cat-header">
              <span class="shape-cat-title" style="color:#DC2626;">✨ Status Overlays</span>
              <span style="font-size:10.5px; font-weight:700; color:var(--text-muted);">${overlayKeys.length} overlays</span>
            </div>
            <div style="font-size:10.5px; color:var(--text-muted); margin-bottom:6px;">Append to any shape: <code>Shape [overlay]</code></div>
            <div class="shape-pill-list">
              ${overlayKeys.map(ov => `<button type="button" class="shape-chip-btn" style="border-color:#FECACA; background:#FEF2F2; color:#DC2626;" onclick="SCRIPT_STUDIO.insertShape('[${ov}]')">[${ov}]</button>`).join("")}
            </div>
          `;
        } else {
          card.innerHTML = `
            <div class="shape-cat-header">
              <span class="shape-cat-title">${catInfo.title}</span>
              <span style="font-size:10.5px; font-weight:700; color:var(--text-muted);">${shapes.length} shapes</span>
            </div>
            <div class="shape-pill-list">
              ${shapes.map(s => `<button type="button" class="shape-chip-btn" onclick="SCRIPT_STUDIO.insertShape('${s}')">${s}</button>`).join("")}
            </div>
          `;
        }

        grid.appendChild(card);
      });
    },

    parseScriptPrompt: parseScriptPrompt
  };

  // Auto-init catalog UI on page load if container exists
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => SCRIPT_STUDIO.initCatalogUI());
    } else {
      setTimeout(() => SCRIPT_STUDIO.initCatalogUI(), 100);
    }
  }

  window.SCRIPT_STUDIO = SCRIPT_STUDIO;
})();
