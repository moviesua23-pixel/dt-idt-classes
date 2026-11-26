// -*- coding: utf-8 -*-
// static/js/shape_catalog.js  (v2.5: Comprehensive 19-Category Handcrafted Shape Kit)
// Universal 19-Category Domain Shape Catalog + 60+ handcrafted, broadcast-quality vector silhouettes.
// Every shape follows the unified visual language:
//   - Top-left 2-stop directional gradient illumination (grad, vgrad)
//   - Outlines are a darker tone of fill (1.3px, round joins)
//   - Ground contact elliptical shadows under objects; lift shadow under flat documents
//   - Slate neutral foundations paired with the active scene accent

(function() {
  // 19 Universal Statutory Categories with display titles & default themes
  const CATEGORIES = {
    people:       { title: "People & Roles",               accent: "indigo", badge: "PERSON / ROLE" },
    vehicles:     { title: "Vehicles & Transit",            accent: "sky",    badge: "VEHICLE / TRANSIT" },
    property:     { title: "Property & Buildings",          accent: "indigo", badge: "REAL PROPERTY" },
    goods:        { title: "Goods & Commodities",           accent: "amber",  badge: "MOVABLE COMMODITY" },
    documents:    { title: "Documents & Instruments",       accent: "amber",  badge: "LEGAL INSTRUMENT" },
    finance:      { title: "Money & Finance",               accent: "emerald",badge: "MONETARY CORPUS" },
    law:          { title: "Law & Government",              accent: "amber",  badge: "STATUTORY DECREE" },
    corporate:    { title: "Corporate Governance",          accent: "purple", badge: "CORPORATE BODY" },
    hazards:      { title: "Hazards & Force Majeure",       accent: "crimson",badge: "CALAMITY / EVENT" },
    cyber:        { title: "Tech, Cyber & Digital",         accent: "sky",    badge: "CYBER ASSET" },
    time:         { title: "Time, Limitations & Deadlines", accent: "indigo", badge: "STATUTORY PERIOD" },
    tax:          { title: "Direct & Indirect Tax",         accent: "emerald",badge: "TAX / STATUTORY" },
    banking:      { title: "Banking & Negotiable Inst.",    accent: "emerald",badge: "BANKING INSTRUMENT" },
    agency:       { title: "Agency & Partnership",          accent: "indigo", badge: "AGENCY / COVENANT" },
    environment:  { title: "Torts & Environment",           accent: "amber",  badge: "TORT / LIABILITY" },
    tools:        { title: "Tools & Professional Props",    accent: "slate",  badge: "TOOL / OPERATIONAL" },
    agriculture:  { title: "Nature & Agriculture",          accent: "emerald",badge: "AGRICULTURAL ASSET" },
    connectors:   { title: "Connectors & Flow Glyphs",      accent: "slate",  badge: "RELATIONAL LINK" },
    overlays:     { title: "Status Overlays",               accent: "crimson",badge: "STATUS OVERLAY" }
  };

  // Curated registry of recognized shapes across the 19 categories
  const REGISTRY = {};

  function reg(keywords, categoryId, iconName, customRenderer = null) {
    const list = Array.isArray(keywords) ? keywords : [keywords];
    const cat = CATEGORIES[categoryId] || CATEGORIES.goods;
    list.forEach(k => {
      const clean = k.toLowerCase().replace(/[\\s\\-_]+/g, "");
      REGISTRY[clean] = {
        key: k,
        cleanKey: clean,
        category: categoryId,
        categoryTitle: cat.title,
        badgeLabel: cat.badge,
        accent: cat.accent,
        icon: iconName,
        custom: customRenderer
      };
    });
  }

  /* ==========================================================================
     POPULATE 19 CATEGORIES WITH DEDICATED ILLUSTRATED RENDERERS
     ========================================================================== */

  // 1. People & Roles
  reg(["person", "human", "plain_figure", "man", "male", "boy", "gentleman", "bailor", "owner", "taxpayer", "assessee", "customer", "client", "buyer"], "people", "user", "man");
  reg(["woman", "women", "female", "girl", "lady", "bailee", "custodian", "seller", "vendor"], "people", "user", "woman");
  reg(["person_briefcase", "executive", "manager", "director"], "people", "briefcase-business", "executive");
  reg(["person_robe", "judge", "advocate", "counsel", "lawyer"], "people", "gavel", "judge");
  reg(["person_cap", "officer", "inspector", "assessing_officer", "police_badge", "enforcement", "directorate"], "people", "shield", "officer");
  reg(["person_ledger", "accountant", "auditor", "ca", "bookkeeper"], "people", "file-spreadsheet", "accountant");
  reg(["person_hardhat", "engineer", "contractor", "builder"], "people", "hard-hat", "engineer");
  reg(["person_stethoscope", "doctor", "physician", "medical_officer"], "people", "stethoscope", "doctor");
  reg(["person_cane", "elderly", "senior_citizen", "retiree"], "people", "accessibility", "elderly");
  reg(["child", "minor", "infant"], "people", "baby", "child");
  reg(["pair", "partners", "couple", "two_persons", "partner_pair", "firm_partners"], "people", "users", "partners");
  reg(["group3", "team", "shareholders", "citizens", "crowd"], "people", "users", "crowd");
  reg(["board_table", "board_of_directors", "boardroom_members", "boardroom", "board_meeting"], "people", "presentation", "boardroom");
  reg(["pedestrian", "victim", "plaintiff_pedestrian"], "environment", "user", "pedestrian");

  // 2. Vehicles & Transit
  reg(["car", "automobile", "auto_car", "sedan"], "vehicles", "car", "car");
  reg(["truck", "freight_truck", "lorry"], "vehicles", "truck", "truck");
  reg(["van", "delivery_van"], "vehicles", "truck", "van");
  reg(["bus", "coach"], "vehicles", "bus-front", "bus");
  reg(["auto_rickshaw", "autorickshaw", "three_wheeler"], "vehicles", "bike", "auto_rickshaw");
  reg(["two_wheeler", "bike", "motorcycle", "scooter"], "vehicles", "bike", "two_wheeler");
  reg(["ship", "cargo_ship", "vessel", "barge", "boat", "container_ship", "cargo_vessel"], "vehicles", "ship", "ship");
  reg(["aircraft", "plane", "airplane", "flight"], "vehicles", "plane", "aircraft");
  reg(["train", "locomotive", "railway"], "vehicles", "train-front", "train");
  reg(["tanker", "oil_tanker", "fuel_tanker"], "vehicles", "fuel", "tanker");
  reg(["cargo_container", "shipping_container"], "vehicles", "boxes", "cargo_container");

  // 3. Property & Buildings
  reg(["house", "residential_house", "home"], "property", "home", "house");
  reg(["apartment", "flat", "condo"], "property", "building-2", "apartment");
  reg(["shop", "store", "retail_store"], "property", "store", "store");
  reg(["warehouse", "godown", "storage"], "property", "warehouse", "warehouse");
  reg(["factory", "plant", "workshop", "mill"], "property", "factory", "factory");
  reg(["office_tower", "office", "commercial_building", "building", "complex", "commercial_complex"], "property", "building", "building");
  reg(["farmland", "agricultural_land", "field_rows", "farm", "plot", "land", "boundary_plot", "site"], "property", "trees", "farmland");
  reg(["hotel", "resort"], "property", "hotel", "hotel");
  reg(["hospital", "clinic"], "property", "hospital", "hospital");
  reg(["school", "college", "university"], "property", "graduation-cap", "school");
  reg(["silo", "grain_silo"], "property", "cylinder", "silo");
  reg(["bank_building", "bank", "financial_institution"], "property", "landmark", "bank");
  reg(["court", "courthouse", "tribunal_building", "tribunal_bench", "bench", "high_court", "supreme_court"], "property", "scale", "court");
  reg(["customs_house", "port_office"], "property", "anchor", "customs_house");

  // 4. Goods & Commodities
  reg(["crate", "wooden_crate", "box", "package", "parcel", "goods"], "goods", "package", "box");
  reg(["sack", "gunny_bag", "bale", "grain_bale", "wheat", "rice_grain"], "goods", "package", "sack");
  reg(["roll_fabric", "cloth", "fabric", "textile", "silk", "cotton"], "goods", "package", "fabric");
  reg(["garment", "clothes", "coat", "suit", "shirt", "dress"], "goods", "shirt", "clothes");
  reg(["jewellery", "jewelry", "gem", "diamond"], "goods", "gem", "jewel");
  reg(["gold_bar", "gold", "bullion", "ingot"], "goods", "gem", "gold");
  reg(["fish_crate", "fish", "marine_catch"], "goods", "fish", "fish");
  reg(["machinery", "machine", "heavy_equipment", "textile_machine", "loom", "spinning_machine"], "goods", "cog", "machinery");
  reg(["plastic_granules", "chemical_raw_material", "marble_slab", "granite_slab", "stone", "yarn_spool", "thread_spool"], "goods", "boxes", "raw_material");
  reg(["smartphone", "phone", "mobile"], "goods", "smartphone", "smartphone");
  reg(["laptop", "computer", "notebook"], "goods", "laptop", "laptop");
  reg(["camera", "cctv"], "goods", "camera", "camera");
  reg(["watch", "luxury_watch"], "goods", "watch", "watch");

  // 5. Documents & Instruments
  reg(["contract", "deed", "agreement"], "documents", "file-text", "document");
  reg(["cheque", "check", "bank_cheque"], "documents", "credit-card", "cheque");
  reg(["cheque_crossed", "crossed_cheque", "stop_sign_cheque", "dishonoured_cheque", "bounced_cheque"], "documents", "credit-card", "cheque_crossed");
  reg(["promissory_note", "demand_note", "will", "testament"], "documents", "file-text", "promissory_note");
  reg(["bill_of_lading", "shipping_bill", "e_way_bill", "eway_bill"], "documents", "anchor", "bill_of_lading");
  reg(["invoice", "tax_invoice", "bill", "credit_note", "debit_note", "challan", "tax_challan", "receipt", "voucher"], "documents", "receipt", "invoice");
  reg(["letter_of_credit", "loc", "guarantee_shield", "bank_guarantee", "letter_of_guarantee"], "documents", "shield-check", "letter_of_credit");
  reg(["share_certificate", "debenture"], "documents", "award", "share_certificate");
  reg(["passbook", "bank_book"], "documents", "book", "passbook");
  reg(["summons", "warrant", "subpoena", "notice", "demand_notice", "show_cause_notice", "power_of_attorney", "poa", "tender_bid", "tender", "audit_report", "tax_audit", "authority_letter", "power_letter"], "documents", "mail", "summons");

  // 6. Money & Finance
  reg(["coin", "coins", "currency_coin", "notes_stack", "cash", "money", "currency", "rupees", "rupee", "indian_rupee", "inr", "cash_bag", "corpus", "consideration"], "finance", "coins", "cash_bag");
  reg(["wallet", "funds"], "finance", "wallet", "wallet");
  reg(["safe", "vault", "locker"], "finance", "vault", "safe");
  reg(["ledger", "cash_book", "day_book", "itc_ledger", "input_tax_credit", "electronic_credit_ledger"], "finance", "book-open", "ledger");
  reg(["calculator", "computation", "tax_calculator"], "finance", "calculator", "calculator");
  reg(["calculation_multiple", "calculation(multiple)", "calculation", "statutory_computation"], "finance", "calculator", "calculation_multiple");
  reg(["calculation_single", "calculation(single)", "formula", "equation", "statutory_formula"], "finance", "calculator", "calculation_single");
  reg(["checklist", "check_list", "check list", "conditions_list", "statutory_checklist", "gate", "conditions_gate"], "finance", "check-square", "checklist");
  reg(["percent_tag", "percent", "interest_rate"], "finance", "badge-percent", "percent_tag");
  reg(["loan", "borrowing", "advances", "deposit", "fixed_deposit", "fd", "pledge_box", "pledge", "hypothecation"], "finance", "landmark", "loan_deposit");
  reg(["insurance_umbrella", "umbrella", "insurance"], "finance", "shield", "umbrella");
  reg(["bar_chart", "financial_growth", "trend_down", "loss", "capital_loss", "trend_up", "profit", "capital_gain"], "finance", "trending-up", "chart");

  // 7. Law & Government
  reg(["gavel", "courtroom_gavel", "mallet"], "law", "gavel", "gavel");
  reg(["scales", "scale", "justice_balance"], "law", "scale", "scale");
  reg(["statute_book", "bare_act", "income_tax_act", "contract_act"], "law", "book-marked", "statute_book");
  reg(["seal", "official_seal", "embossed_seal", "stamp", "rubber_stamp", "seal_stamp"], "law", "stamp", "official_seal");
  reg(["flag_pole", "flag", "state_emblem"], "law", "flag", "flag");
  reg(["tax_office", "revenue_dept", "it_dept"], "law", "building", "building");
  reg(["handcuffs", "arrest", "penal_action", "lock_warrant", "seizure_order"], "law", "lock", "handcuffs");
  reg(["customs_scanner", "customs"], "law", "scan", "customs_scanner");

  // 8. Corporate Governance
  reg(["mind", "mindmap", "mind_map", "mind map", "concept_map", "tree_map", "hierarchy_map"], "corporate", "network", "mind");
  reg(["heading", "head", "title", "headline", "hero_heading", "section_heading", "chapter_heading", "topic_heading", "banner_heading"], "corporate", "bookmark", "heading");
  reg(["ballot_box", "voting", "postal_ballot"], "corporate", "vote", "ballot_box");
  reg(["org_chart", "hierarchy", "management"], "corporate", "network", "org_chart");
  reg(["share_pie", "shareholding_pattern", "equity_split"], "corporate", "pie-chart", "share_pie");
  reg(["merger_arrows", "amalgamation", "merger", "demerger_split", "demerger", "spinoff"], "corporate", "git-merge", "merger");
  reg(["office_desk", "workstation", "letterhead", "corporate_memo", "registered_office_sign", "roc_sign"], "corporate", "table", "office_desk");

  // 9. Hazards & Force Majeure
  reg(["fire", "flame", "burn", "arson"], "hazards", "flame", "fire");
  reg(["flood", "water_damage", "deluge", "dam", "water_reservoir", "river", "watercourse"], "hazards", "waves", "flood");
  reg(["earthquake_crack", "earthquake", "seismic", "collapse", "structural_failure"], "hazards", "zap", "earthquake");
  reg(["storm", "cyclone", "tempest", "lightning", "zap", "act_of_god"], "hazards", "cloud-lightning", "storm");
  reg(["explosion", "blast", "bomb"], "hazards", "bomb", "explosion");
  reg(["spill", "chemical_leak", "toxic_spill", "toxic_barrel", "hazardous_substance"], "hazards", "biohazard", "toxic_barrel");
  reg(["smoke", "pollution", "chimney_smoke", "factory_emission", "nuisance", "power_off", "blackout", "grid_failure"], "hazards", "cloud", "smoke");

  // 10. Tech, Cyber & Digital
  reg(["server", "data_center", "cloud_server", "database", "db_storage", "sql"], "cyber", "server", "server");
  reg(["phishing_hook", "phishing", "cyber_fraud"], "cyber", "fishing-hook", "phishing");
  reg(["padlock_broken", "breach", "data_leak"], "cyber", "lock-keyhole-open", "breach");
  reg(["ransomware_screen", "malware", "virus"], "cyber", "shield-alert", "ransomware");
  reg(["email_envelope", "email", "electronic_mail"], "cyber", "mail", "email");
  reg(["usb_drive", "pen_drive", "flash_disk"], "cyber", "hard-drive", "usb");
  reg(["crypto_coin", "crypto", "bitcoin", "vda"], "cyber", "bitcoin", "crypto");
  reg(["qr_code", "digital_code", "upi"], "cyber", "qr-code", "qr_code");

  // 11. Time, Limitations & Deadlines
  reg(["clock", "limitation_clock", "time", "stopwatch", "rapid_period", "interest_clock", "penal_interest"], "time", "clock", "clock");
  reg(["calendar", "assessment_year", "financial_year", "year_badge", "3_year_limitation"], "time", "calendar", "calendar");
  reg(["hourglass", "expiry", "time_barred"], "time", "hourglass", "hourglass");
  reg(["deadline_flag", "due_date", "timeline_dot", "milestone", "180_day_badge", "180_days", "half_year"], "time", "flag", "deadline");

  // 12. Direct & Indirect Tax
  reg(["itr_form", "income_tax_return", "itr", "gst_return", "gstr1", "gstr3b", "gstin", "tds_certificate", "form_16", "form_26as"], "tax", "file-text", "tax_doc");
  reg(["pan_card_generic", "pan_card", "pan"], "tax", "credit-card", "pan_card");
  reg(["assessment_stack", "scrutiny_order"], "tax", "layers", "assessment_stack");
  reg(["search_magnifier", "search_and_seizure"], "tax", "search", "search_magnifier");
  reg(["seized_box", "confiscated_assets"], "tax", "package-x", "seized_box");
  reg(["exempt_shield", "statutory_exemption", "deduction"], "tax", "shield-check", "exempt_shield");

  // 13. Banking & Negotiable Inst.
  reg(["teller_counter", "bank_counter"], "banking", "landmark", "teller_counter");
  reg(["atm", "automated_teller"], "banking", "credit-card", "atm");

  // 14. Agency & Partnership
  reg(["handshake", "agreement_consent", "meeting_of_minds"], "agency", "handshake", "handshake");
  reg(["two_keys", "dual_control"], "agency", "key", "two_keys");
  reg(["delegate_arrow", "sub_agency", "delegatus_non_potest_delegare"], "agency", "arrow-right-left", "delegate_arrow");
  reg(["signboard", "firm_signboard"], "agency", "signpost", "signboard");

  // 15. Tools & Professional Props
  reg(["key", "safe_key", "delivery_key"], "tools", "key", "key");
  reg(["wrench", "spanner", "repair_tool"], "tools", "wrench", "wrench");
  reg(["magnifier", "search_glass", "inspection"], "tools", "search", "magnifier");
  reg(["scissors_cut", "scissors", "partition_cut"], "tools", "scissors", "scissors");
  reg(["hanger", "clothes_hanger"], "tools", "hanger", "clothes");
  reg(["scale_weight", "weighing_stone"], "tools", "scale", "scale");
  reg(["stamp_pad", "ink_pad"], "tools", "stamp", "official_seal");
  reg(["pen", "fountain_pen", "signature_pen"], "tools", "pen-tool", "pen");
  reg(["briefcase", "attache_case", "parcel_tag", "cargo_tag"], "tools", "briefcase", "briefcase");

  // 16. Nature & Agriculture
  reg(["tree", "standing_timber", "forest", "orchard", "plantation"], "agriculture", "tree-pine", "tree");
  reg(["crop", "growing_crops", "harvest", "grain", "paddy", "cereals"], "agriculture", "sprout", "crop");
  reg(["tractor", "farm_tractor", "agricultural_machinery"], "agriculture", "truck", "tractor");
  reg(["cow", "cattle", "livestock"], "agriculture", "paw-print", "cow");
  reg(["mine", "mineral_quarry", "coal_mine"], "agriculture", "pickaxe", "mine");

  // 17. Connectors & Flow Glyphs
  reg(["arrow", "arrow_right", "flow_arrow", "double_arrow", "reciprocal_arrow", "dashed_flow", "subordinate_flow", "split_arrow", "divergent_flow", "loop_arrow", "cyclic_restitution", "equals", "equal_sign", "equivalence", "plus", "addition", "aggregate", "minus", "subtraction", "deduction_glyph", "bracket", "grouping", "link", "covenant_link", "broken_link", "severability", "breach_link"], "connectors", "arrow-right", "connector");

  // 18. Status Overlays
  const OVERLAYS = {
    damaged:  { icon: "alert-triangle", color: "#DC2626", bg: "#FEE2E2", label: "DAMAGED" },
    locked:   { icon: "lock",           color: "#D97706", bg: "#FEF3C7", label: "LOCKED" },
    stamped:  { icon: "stamp",          color: "#059669", bg: "#ECFDF5", label: "STAMPED" },
    crossed:  { icon: "x",              color: "#DC2626", bg: "#FEE2E2", label: "VOID" },
    check:    { icon: "check",          color: "#059669", bg: "#ECFDF5", label: "VERIFIED" },
    warning:  { icon: "alert-circle",   color: "#D97706", bg: "#FEF3C7", label: "CAUTION" },
    clock:    { icon: "clock",          color: "#4F46E5", bg: "#EEF2FF", label: "PENDING" },
    rupee:    { icon: "badge-indian-rupee", color: "#CA8A04", bg: "#FEF08A", label: "PAID" },
    percent:  { icon: "percent",        color: "#9333EA", bg: "#FAF5FF", label: "TAXED" },
    missing:  { icon: "help-circle",    color: "#64748B", bg: "#F1F5F9", label: "MISSING" },
    flag:     { icon: "flag",           color: "#DC2626", bg: "#FEE2E2", label: "DISPUTED" },
    question: { icon: "help-circle",    color: "#4F46E5", bg: "#EEF2FF", label: "QUERY" }
  };

  /* ==========================================================================
     LOOKUP & CLASSIFICATION ENGINE
     ========================================================================== */
  function lookup(rawShapeStr) {
    if (!rawShapeStr) return null;
    const str = rawShapeStr.trim();
    let overlayType = null;
    let baseName = str;
    const overlayMatch = str.match(/^(.*?)\\s*\\[(.*?)\\]$/);
    if (overlayMatch) {
      baseName = overlayMatch[1].trim();
      overlayType = overlayMatch[2].trim().toLowerCase();
    }

    const clean = baseName.toLowerCase().replace(/[\\s\\-_]+/g, "");

    // 1. Direct match in registry
    let found = REGISTRY[clean];

    // 2. Fallback fuzzy substring scan
    if (!found) {
      for (let k in REGISTRY) {
        if (clean.includes(k) || k.includes(clean)) {
          found = REGISTRY[k];
          break;
        }
      }
    }

    // 3. Fallback to raw Lucide icon if name exists directly in window.COLORFUL_SHAPES_DATA
    if (!found && window.COLORFUL_SHAPES_DATA) {
      const hyphenKey = baseName.toLowerCase().replace(/[\\s_]+/g, "-");
      if (window.COLORFUL_SHAPES_DATA[hyphenKey]) {
        found = {
          key: baseName,
          category: "goods",
          categoryTitle: "General Asset / Artifact",
          badgeLabel: "STATUTORY OBJECT",
          accent: "indigo",
          icon: hyphenKey,
          custom: null
        };
      }
    }

    // 4. Default generic fallback
    if (!found) {
      found = {
        key: baseName,
        category: "goods",
        categoryTitle: "Statutory Asset",
        badgeLabel: baseName.toUpperCase(),
        accent: "indigo",
        icon: "package",
        custom: null
      };
    }

    return {
      ...found,
      baseName,
      overlay: overlayType && OVERLAYS[overlayType] ? { type: overlayType, ...OVERLAYS[overlayType] } : null
    };
  }

  /* ==========================================================================
     PROFESSIONAL SHAPE KIT ENGINE (v2.5)
     Unified palette, light source, outlines, ground shadows, and lift shadows.
     ========================================================================== */

  const C = {
    ink: "#0F172A", s800: "#1E293B", s700: "#334155", s600: "#475569", s500: "#64748B",
    s400: "#94A3B8", s300: "#CBD5E1", s200: "#E2E8F0", s100: "#F1F5F9", s50: "#F8FAFC",
    white: "#FFFFFF", paper: "#FFFDF7", paperLo: "#F3EEDF",
    glass: "#BAE6FD", glassHi: "#E0F2FE", glassLo: "#7DD3FC",
    gold: "#EAB308", goldHi: "#FDE047", goldLo: "#A16207",
    skin: "#F5CBA7", skinLo: "#E3A878", hair: "#1F2937", hairBrown: "#5B3A29",
    red: "#DC2626", redLo: "#991B1B", green: "#059669", greenHi: "#D1FAE5",
    sky: "#0284C7", skyHi: "#38BDF8", skyLo: "#0369A1",
    emerald: "#10B981", emeraldHi: "#34D399", emeraldLo: "#047857",
    purple: "#7C3AED", purpleHi: "#A78BFA", purpleLo: "#581C87"
  };

  function hex2rgb(h) {
    h = String(h).replace("#", "");
    if (h.length === 3) h = h.split("").map(c => c + c).join("");
    const n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(h, t) {
    if (!/^#?[0-9a-f]{3,6}$/i.test(String(h))) return h;
    const [r, g, b] = hex2rgb(h);
    const target = t >= 0 ? 255 : 0, a = Math.abs(t);
    const m = v => Math.round(v + (target - v) * a).toString(16).padStart(2, "0");
    return "#" + m(r) + m(g) + m(b);
  }
  function T(accent) {
    const a = accent || {};
    const m = a.main || "#4F46E5";
    return { m, hi: mix(m, 0.28), lo: mix(m, -0.18), deep: a.dark || mix(m, -0.42),
             soft: a.light || mix(m, 0.9), line: mix(m, -0.38), ring: a.border || mix(m, 0.7) };
  }
  const edge = f => mix(f, -0.38);

  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
  function paint(ctx, fill, stroke, lw) {
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke !== null) { ctx.strokeStyle = stroke || edge(typeof fill === "string" ? fill : C.s500); ctx.lineWidth = lw || 1.3; ctx.lineJoin = "round"; ctx.lineCap = "round"; ctx.stroke(); }
  }
  function box(ctx, x, y, w, h, r, fill, stroke, lw) { rr(ctx, x, y, w, h, r); paint(ctx, fill, stroke, lw); }
  function poly(ctx, pts, fill, stroke, lw) {
    ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
    ctx.closePath(); paint(ctx, fill, stroke, lw);
  }
  function circ(ctx, x, y, r, fill, stroke, lw) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); paint(ctx, fill, stroke, lw); }
  function line(ctx, x1, y1, x2, y2, col, lw) {
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
    ctx.strokeStyle = col; ctx.lineWidth = lw || 1.2; ctx.lineCap = "round"; ctx.stroke();
  }
  function grad(ctx, x0, y0, x1, y1, c0, c1) {
    const g = ctx.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, c0); g.addColorStop(1, c1); return g;
  }
  function vgrad(ctx, y0, y1, base, lift) { return grad(ctx, 0, y0, 0, y1, mix(base, lift === undefined ? 0.16 : lift), base); }
  function ground(ctx, cx, cy, rx, ry) {
    ctx.save(); ctx.fillStyle = "rgba(15,23,42,0.14)";
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry || rx * 0.12, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  }
  function lift(ctx) { ctx.shadowColor = "rgba(15,23,42,0.16)"; ctx.shadowBlur = 9; ctx.shadowOffsetY = 3; }
  function noShadow(ctx) { ctx.shadowColor = "transparent"; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }
  function sparkle(ctx, x, y, r, col) {
    ctx.fillStyle = col; ctx.beginPath();
    ctx.moveTo(x, y - r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.quadraticCurveTo(x, y, x, y + r);
    ctx.quadraticCurveTo(x, y, x - r, y); ctx.quadraticCurveTo(x, y, x, y - r); ctx.fill();
  }
  function wheel(ctx, x, y, r, rim) {
    circ(ctx, x, y, r, C.ink, null);
    circ(ctx, x, y, r * 0.62, rim || C.s300, C.s500, 1);
    circ(ctx, x, y, r * 0.22, C.s600, null);
    ctx.strokeStyle = C.s500; ctx.lineWidth = 1;
    for (let i = 0; i < 5; i++) {
      const a = (i / 5) * Math.PI * 2 + 0.3;
      ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r * 0.22, y + Math.sin(a) * r * 0.22);
      ctx.lineTo(x + Math.cos(a) * r * 0.6, y + Math.sin(a) * r * 0.6); ctx.stroke();
    }
  }
  function trunc(s, n) { s = String(s || ""); return s.length > n ? s.slice(0, n - 1) + "\\u2026" : s; }

  

  /* ==========================================================================
     CORE V2 HANDCRAFTED SHAPES (31 FOUNDATION ARCHETYPES)
     ========================================================================== */

function drawCarShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 22, 44, 4.5);

    // Body (rear on the left, facing right)
    const body = new Path2D("M-46 12 L-46 3 Q-46 -2 -40 -3.5 L-29 -5.5 L-19 -17 Q-17 -20 -12 -20 L12 -20 Q17 -20 20 -17 L29 -6 L40 -4 Q46 -3 46 3 L46 12 Z");
    ctx.fillStyle = grad(ctx, 0, -20, 0, 12, t.hi, t.lo); ctx.fill(body);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(body);

    // Side sill + shoulder highlight
    ctx.fillStyle = t.deep; ctx.fillRect(-45, 8, 90, 3.5);
    line(ctx, -40, -1.5, 38, -1.5, "rgba(255,255,255,0.35)", 1.2);

    // Windows
    const w1 = [[-24, -5], [-17, -15.5], [-4, -15.5], [-4, -5]];
    const w2 = [[0, -5], [0, -15.5], [11, -15.5], [14.5, -15], [22, -5]];
    [w1, w2].forEach(p => { poly(ctx, p, grad(ctx, 0, -16, 0, -5, C.glassHi, C.glassLo), t.line, 1.1); });
    line(ctx, -14, -13, -9, -13, "rgba(255,255,255,0.8)", 1.4);
    line(ctx, 3, -13, 8, -13, "rgba(255,255,255,0.8)", 1.4);

    // Door seam + handles
    line(ctx, -2, -5, -2, 8, t.line, 1);
    line(ctx, 22, -3, 22, 8, t.line, 1);
    line(ctx, -9, -2.5, -5, -2.5, t.deep, 1.4);
    line(ctx, 5, -2.5, 9, -2.5, t.deep, 1.4);

    // Lights
    box(ctx, 41, -2, 5, 5, 2, "#FEF9C3", "#CA8A04", 1);
    box(ctx, -46, -1, 4, 5, 1.5, C.red, C.redLo, 1);

    // Wheels with arches
    [-27, 27].forEach(x => {
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(x, 12, 11.5, Math.PI, 0); ctx.fill();
      wheel(ctx, x, 13, 9, C.s200);
    });
    ctx.restore();
  }

function drawTruckShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 22, 46, 4.5);

    // Cargo container
    box(ctx, -47, -26, 58, 36, 3, grad(ctx, 0, -26, 0, 10, C.white, C.s200), C.s400, 1.3);
    for (let x = -39; x < 8; x += 7.5) line(ctx, x, -23, x, 7, C.s300, 1);
    ctx.fillStyle = t.m; ctx.fillRect(-46, -8, 56, 5);          // accent livery band
    ctx.fillStyle = t.deep; ctx.fillRect(-46, -3, 56, 1.4);
    box(ctx, -47, 8, 58, 3.5, 1, C.s600, null);                  // chassis

    // Cab
    const cab = new Path2D("M13 10 L13 -18 Q13 -22 17 -22 L32 -22 Q35 -22 37 -19 L46 -4 L46 10 Z");
    ctx.fillStyle = grad(ctx, 0, -22, 0, 10, t.hi, t.lo); ctx.fill(cab);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(cab);
    poly(ctx, [[17, -4], [17, -18], [31, -18], [39, -4]], grad(ctx, 0, -18, 0, -4, C.glassHi, C.glassLo), t.line, 1.1);
    line(ctx, 20, -15, 25, -15, "rgba(255,255,255,0.85)", 1.4);
    line(ctx, 25, 1, 31, 1, t.deep, 1.4);
    box(ctx, 43, 0, 4, 5, 1.5, "#FEF9C3", "#CA8A04", 1);         // headlight
    box(ctx, 44, 8, 4, 4, 1, C.s600, null);                       // bumper

    // Wheels
    [-34, -16, 30].forEach(x => {
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(x, 11, 9.5, Math.PI, 0); ctx.fill();
      wheel(ctx, x, 13, 8, C.s200);
    });
    ctx.restore();
  }

function drawAutoRickshawShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 22, 40, 4);
    const yel = "#FBBF24";

    // Rear body (yellow) + canopy (accent) + windscreen
    const body = new Path2D("M-36 12 L-36 -6 Q-36 -9 -33 -9 L12 -9 L22 4 L34 6 Q38 7 38 11 L38 12 Z");
    ctx.fillStyle = vgrad(ctx, -9, 12, yel, 0.2); ctx.fill(body);
    ctx.strokeStyle = edge(yel); ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(body);
    const canopy = new Path2D("M-37 -9 L-37 -22 Q-37 -27 -31 -27 L10 -27 Q15 -27 17 -22 L21 -9 Z");
    ctx.fillStyle = grad(ctx, 0, -27, 0, -9, t.hi, t.lo); ctx.fill(canopy);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.stroke(canopy);
    poly(ctx, [[-30, -11], [-30, -21], [8, -21], [13, -11]], grad(ctx, 0, -21, 0, -11, C.glassHi, C.glassLo), t.line, 1.1);
    line(ctx, -24, -18, -14, -18, "rgba(255,255,255,0.85)", 1.4);
    // front windscreen + handlebar
    poly(ctx, [[20, -9], [26, 4], [22, 4], [17, -9]], C.glass, t.line, 1);
    line(ctx, 26, 4, 30, -2, C.s600, 2);
    box(ctx, 33, 1, 5, 4, 2, "#FEF9C3", "#CA8A04", 1);            // headlight
    ctx.fillStyle = t.deep; ctx.fillRect(-36, 8, 72, 3);
    // Wheels: rear (with arch) and front
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(-20, 12, 10.5, Math.PI, 0); ctx.fill();
    wheel(ctx, -20, 13, 8.5, C.s200);
    wheel(ctx, 30, 13, 7.5, C.s200);
    ctx.restore();
  }

function drawTwoWheelerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -6);
    ground(ctx, 0, 22, 38, 4);
    // Frame / fairing
    const fair = new Path2D("M-14 6 Q-16 -6 -6 -10 L8 -10 Q14 -10 15 -3 L18 6 Z");
    ctx.fillStyle = grad(ctx, 0, -10, 0, 6, t.hi, t.lo); ctx.fill(fair);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(fair);
    // Seat + rear section
    box(ctx, -32, -12, 26, 6, 3, C.s800, null);
    const rear = new Path2D("M-30 -6 L-8 -6 L-12 8 L-26 8 Z");
    ctx.fillStyle = t.lo; ctx.fill(rear); ctx.strokeStyle = t.line; ctx.lineWidth = 1.2; ctx.stroke(rear);
    // Front fork, handlebar, headlight, windshield
    line(ctx, 18, -6, 28, 13, C.s600, 3);
    line(ctx, 15, -16, 21, -6, C.s700, 2.4);
    line(ctx, 11, -18, 20, -18, C.s800, 3);
    poly(ctx, [[17, -18], [23, -29], [26, -29], [24, -18]], C.glass, C.s500, 1);
    box(ctx, 21, -12, 5, 5, 2.5, "#FEF9C3", "#CA8A04", 1);
    // Floorboard + exhaust
    box(ctx, -8, 6, 24, 3.5, 1.5, t.deep, null);
    box(ctx, -34, 5, 14, 3.5, 1.7, C.s400, C.s600, 1);
    wheel(ctx, -26, 13, 9.5, C.s200);
    wheel(ctx, 28, 13, 9.5, C.s200);
    ctx.restore();
  }

function drawTractorShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 42, 4.5);
    // Hood
    const hood = new Path2D("M-2 6 L-2 -10 Q-2 -14 2 -14 L30 -14 Q34 -14 36 -10 L40 4 L40 8 L-2 8 Z");
    ctx.fillStyle = grad(ctx, 0, -14, 0, 8, t.hi, t.lo); ctx.fill(hood);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(hood);
    for (let i = 0; i < 4; i++) line(ctx, 30 + i * 2.2, -6 + i * 0.5, 30 + i * 2.2, 2, t.deep, 1);   // grille
    // Cabin frame + roof + seat
    box(ctx, -38, -16, 38, 5, 2, t.deep, null);                       // roof
    line(ctx, -34, -11, -34, 6, t.deep, 2.4);
    line(ctx, -4, -11, -4, 4, t.deep, 2.4);
    poly(ctx, [[-33, -10], [-5, -10], [-5, 2], [-33, 2]], "rgba(186,230,253,0.55)", t.line, 1);
    box(ctx, -26, -2, 12, 5, 2, C.s800, null);                         // seat
    box(ctx, -38, 4, 40, 5, 2, t.lo, t.line, 1.2);                     // chassis
    // Exhaust pipe
    box(ctx, 20, -26, 3, 12, 1.2, C.s600, C.s800, 1);
    circ(ctx, 21.5, -29, 2.4, "rgba(148,163,184,0.55)", null);
    // Wheels: big rear, small front
    circ(ctx, -22, 8, 17, C.ink, null);
    circ(ctx, -22, 8, 11, t.m, t.line, 1.2);
    circ(ctx, -22, 8, 3.4, C.s300, C.s600, 1);
    for (let a = 0; a < 6; a++) {
      const r1 = a / 6 * Math.PI * 2;
      line(ctx, -22 + Math.cos(r1) * 3.5, 8 + Math.sin(r1) * 3.5, -22 + Math.cos(r1) * 10, 8 + Math.sin(r1) * 10, t.line, 1);
    }
    circ(ctx, 28, 14, 9, C.ink, null);
    circ(ctx, 28, 14, 5.4, t.m, t.line, 1.1);
    circ(ctx, 28, 14, 1.8, C.s300, null);
    ctx.restore();
  }

function drawChequeShape(ctx, accentTheme = {}, isCrossed = false) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 90, h = 48, x = -w / 2, y = -h / 2;

    lift(ctx); box(ctx, x, y, w, h, 4, grad(ctx, x, y, x + w, y + h, C.paper, C.paperLo), null); noShadow(ctx);
    box(ctx, x, y, w, h, 4, null, mix(t.m, 0.35), 1.4);

    ctx.save(); rr(ctx, x, y, w, h, 4); ctx.clip();
    // Security wave pattern
    ctx.strokeStyle = mix(t.m, 0.82); ctx.lineWidth = 1;
    for (let k = 0; k < 4; k++) {
      ctx.beginPath();
      for (let px = x; px <= x + w; px += 3) { const py = y + 18 + k * 6 + Math.sin(px * 0.28 + k) * 1.6; px === x ? ctx.moveTo(px, py) : ctx.lineTo(px, py); }
      ctx.stroke();
    }
    ctx.fillStyle = t.m; ctx.fillRect(x, y, w, 9);               // header band
    ctx.restore();
    circ(ctx, x + 8, y + 4.5, 2.6, "rgba(255,255,255,0.9)", null);  // bank mark
    line(ctx, x + 14, y + 4.5, x + 36, y + 4.5, "rgba(255,255,255,0.75)", 1.6);
    box(ctx, x + w - 26, y + 2, 22, 5, 1, "rgba(255,255,255,0.22)", "rgba(255,255,255,0.7)", 0.8); // date box

    // Payee / words / amount
    line(ctx, x + 20, y + 17, x + w - 8, y + 17, C.s400, 1);
    line(ctx, x + 6, y + 17, x + 16, y + 17, C.s300, 1.4);
    line(ctx, x + 8, y + 25, x + w - 34, y + 25, C.s400, 1);
    box(ctx, x + w - 29, y + 20, 24, 11, 2, C.white, t.m, 1.1);
    ctx.fillStyle = t.deep; ctx.font = "800 8px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("\u20B9", x + w - 23, y + 26);
    ctx.textBaseline = "alphabetic";

    // Signature
    ctx.strokeStyle = "#1D4ED8"; ctx.lineWidth = 1.2; ctx.beginPath();
    ctx.moveTo(x + w - 36, y + 38); ctx.bezierCurveTo(x + w - 32, y + 31, x + w - 28, y + 42, x + w - 24, y + 35);
    ctx.bezierCurveTo(x + w - 21, y + 31, x + w - 18, y + 40, x + w - 12, y + 36); ctx.stroke();
    line(ctx, x + w - 38, y + 40, x + w - 8, y + 40, C.s400, 0.9);

    // MICR strip
    ctx.fillStyle = C.s700;
    for (let i = 0; i < 18; i++) ctx.fillRect(x + 7 + i * 3.1, y + h - 7, i % 3 === 0 ? 1.8 : 1.1, 3.4);

    if (isCrossed) {
      ctx.save(); ctx.translate(x + 15, y + 22); ctx.rotate(-Math.PI / 4);
      ctx.fillStyle = "rgba(255,255,255,0.9)"; ctx.fillRect(-17, -6.5, 34, 13);
      line(ctx, -17, -6.5, 17, -6.5, C.red, 1.5); line(ctx, -17, 6.5, 17, 6.5, C.red, 1.5);
      ctx.fillStyle = C.red; ctx.font = "800 5px 'JetBrains Mono', monospace"; ctx.textAlign = "center";
      ctx.fillText("A/C PAYEE", 0, -0.5); ctx.fillText("ONLY", 0, 4.6);
      ctx.restore();
    }
    ctx.restore();
  }

function drawTaxDocShape(ctx, shapeKey, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 66, h = 56, x = -w / 2, y = -h / 2, f = 12;
    const sheet = new Path2D(`M${x + 4} ${y} L${x + w - f} ${y} L${x + w} ${y + f} L${x + w} ${y + h - 4} Q${x + w} ${y + h} ${x + w - 4} ${y + h} L${x + 4} ${y + h} Q${x} ${y + h} ${x} ${y + h - 4} L${x} ${y + 4} Q${x} ${y} ${x + 4} ${y} Z`);
    lift(ctx); ctx.fillStyle = C.white; ctx.fill(sheet); noShadow(ctx);
    ctx.strokeStyle = C.s300; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(sheet);
    poly(ctx, [[x + w - f, y], [x + w - f, y + f], [x + w, y + f]], C.s100, C.s300, 1.2);   // folded corner

    // Header band with title
    ctx.save(); ctx.clip(sheet);
    ctx.fillStyle = t.m; ctx.fillRect(x, y, w - f, 14);
    ctx.fillRect(x + w - f, y + f - 2, f, 2);
    ctx.restore();
    ctx.fillStyle = C.white; ctx.font = "800 6.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    ctx.fillText(trunc(String(shapeKey || "").toUpperCase().replace(/[_\-]+/g, " "), 11), x + 6, y + 7.5);
    ctx.textBaseline = "alphabetic";

    // Text lines + figure column
    for (let i = 0; i < 4; i++) {
      const ly = y + 22 + i * 6.5;
      line(ctx, x + 7, ly, x + w - 22, ly, C.s300, 1.5);
      line(ctx, x + w - 16, ly, x + w - 7, ly, i === 3 ? t.m : C.s300, 1.5);
    }
    // Verified seal
    circ(ctx, x + w - 15, y + h - 11, 7.5, t.soft, t.m, 1.3);
    ctx.strokeStyle = t.m; ctx.lineWidth = 1.8; ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.beginPath(); ctx.moveTo(x + w - 18.5, y + h - 11); ctx.lineTo(x + w - 15.5, y + h - 8); ctx.lineTo(x + w - 11, y + h - 14); ctx.stroke();
    ctx.restore();
  }

function drawSafeShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 30, 34, 4);
    box(ctx, -32, 22, 8, 6, 2, C.s700, null); box(ctx, 24, 22, 8, 6, 2, C.s700, null);   // feet
    box(ctx, -35, -30, 70, 54, 6, grad(ctx, -35, -30, 35, 24, C.s500, C.s800), C.s400, 1.4);
    box(ctx, -29, -24, 58, 42, 4, grad(ctx, -29, -24, 29, 18, C.s600, C.s700), C.s800, 1.2);
    // Hinges
    box(ctx, -33, -16, 4, 8, 1.5, C.s300, C.s600, 1); box(ctx, -33, 4, 4, 8, 1.5, C.s300, C.s600, 1);
    // Dial
    circ(ctx, -3, -3, 15, C.s300, C.s800, 1.3);
    circ(ctx, -3, -3, 11.5, C.s100, C.s500, 1);
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      line(ctx, -3 + Math.cos(a) * 8, -3 + Math.sin(a) * 8, -3 + Math.cos(a) * 10.5, -3 + Math.sin(a) * 10.5, C.s500, 1);
    }
    circ(ctx, -3, -3, 4.2, t.m, t.line, 1.1);
    line(ctx, -3, -3, 2, -8, t.deep, 2);
    // Handle bar + indicator
    box(ctx, 15, -10, 8, 3.4, 1.5, C.gold, C.goldLo, 1);
    line(ctx, 19, -6, 19, 6, C.gold, 3);
    circ(ctx, 22, -20, 1.8, C.green, null);
    ctx.restore();
  }

function drawCalculatorShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    lift(ctx); box(ctx, -26, -34, 52, 68, 7, grad(ctx, -26, -34, 26, 34, C.s600, C.s800), null); noShadow(ctx);
    box(ctx, -26, -34, 52, 68, 7, null, C.ink, 1.3);
    box(ctx, -20, -28, 40, 16, 3, C.greenHi, "#6EE7B7", 1.1);              // display
    ctx.fillStyle = "#047857";                                              // display segments
    [-14, -7, 0, 7].forEach((dx, i) => ctx.fillRect(dx + 6, -22, 4, 2.4 + (i % 2)));
    const cols = 4, rows = 4, kw = 8.6, kh = 7.2, gx = 2.4, gy = 2.6, sx = -20, sy = -8;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const isOp = c === 3, isTop = r === 0 && c < 3, isEq = r === rows - 1 && c === cols - 1;
      const fill = isEq ? C.green : isOp ? t.m : isTop ? C.s400 : C.s200;
      box(ctx, sx + c * (kw + gx), sy + r * (kh + gy), kw, kh, 2, fill, edge(fill), 0.9);
    }
    ctx.restore();
  }

function drawServerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 32, 3.5);
    for (let i = 0; i < 3; i++) {
      const y = -32 + i * 21;
      box(ctx, -31, y, 62, 18, 4, grad(ctx, 0, y, 0, y + 18, C.s600, C.s800), C.s500, 1.2);
      for (let s = 0; s < 4; s++) line(ctx, -26 + s * 5, y + 6, -26 + s * 5, y + 12, C.s400, 1.2);      // drive slots
      circ(ctx, 18, y + 9, 2.2, i === 1 ? "#F59E0B" : C.green, null);
      circ(ctx, 25, y + 9, 2.2, i === 2 ? t.m : C.s500, null);
    }
    box(ctx, -8, 32, 16, 4, 2, C.s700, null);
    ctx.restore();
  }

function drawHandshakeShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    // Sleeves (left navy, right accent) with white cuffs
    poly(ctx, [[-46, -12], [-26, -16], [-26, 8], [-46, 12]], "#1E3A8A", "#172554", 1.2);
    poly(ctx, [[46, -12], [26, -16], [26, 8], [46, 12]], t.m, t.line, 1.2);
    box(ctx, -30, -16, 5, 24, 1.5, C.white, C.s300, 1);
    box(ctx, 25, -16, 5, 24, 1.5, C.white, C.s300, 1);
    // Left hand
    const lh = new Path2D("M-25 -13 Q-14 -16 -4 -13 L12 -8 Q18 -5 14 0 L6 8 Q0 13 -8 10 L-25 6 Z");
    ctx.fillStyle = grad(ctx, 0, -14, 0, 12, C.skin, C.skinLo); ctx.fill(lh);
    ctx.strokeStyle = edge(C.skinLo); ctx.lineWidth = 1.2; ctx.lineJoin = "round"; ctx.stroke(lh);
    // Right hand (on top) with knuckle fingers
    const rh = new Path2D("M25 -13 Q14 -17 4 -14 L-6 -9 Q-12 -4 -7 0 L2 9 Q8 14 16 10 L25 6 Z");
    ctx.fillStyle = grad(ctx, 0, -17, 0, 14, mix(C.skin, 0.12), C.skin); ctx.fill(rh);
    ctx.strokeStyle = edge(C.skinLo); ctx.stroke(rh);
    for (let i = 0; i < 4; i++) line(ctx, -2 + i * 3.6, 2 - i * 0.2, 0 + i * 3.6, 10 - i * 0.4, C.skinLo, 1.3);   // finger gaps
    // Thumb
    ctx.beginPath(); ctx.ellipse(-8, -12, 9, 3.6, -0.18, 0, Math.PI * 2);
    ctx.fillStyle = C.skin; ctx.fill(); ctx.strokeStyle = edge(C.skinLo); ctx.stroke();
    sparkle(ctx, -2, -26, 3.2, C.gold); sparkle(ctx, 12, -23, 2.2, C.goldHi);
    ctx.restore();
  }

function drawFarmlandShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -6);
    // Isometric plot
    const P = [[0, -26], [46, -2], [0, 22], [-46, -2]];
    ctx.save(); ctx.translate(0, 5); poly(ctx, P, "rgba(15,23,42,0.13)", null); ctx.restore();   // slab shadow
    poly(ctx, [[-46, -2], [0, 22], [0, 30], [-46, 6]], "#8B5E34", "#5A3A1C", 1.2);                  // soil side
    poly(ctx, [[0, 22], [46, -2], [46, 6], [0, 30]], "#6F4A27", "#5A3A1C", 1.2);
    poly(ctx, P, grad(ctx, -46, -26, 46, 22, "#BBF7D0", "#86EFAC"), "#15803D", 1.3);
    // Crop rows (parallel to the left-to-top edge)
    ctx.save(); ctx.beginPath(); ctx.moveTo(P[0][0], P[0][1]); P.slice(1).forEach(p => ctx.lineTo(p[0], p[1])); ctx.closePath(); ctx.clip();
    for (let i = 0; i < 9; i++) {
      const u = (i + 0.5) / 9, sx = -46 + 46 * u, sy = -2 + 24 * u;
      ctx.strokeStyle = i % 2 ? "#16A34A" : "#4ADE80"; ctx.lineWidth = 3.2; ctx.lineCap = "butt";
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + 46, sy - 24); ctx.stroke();
    }
    ctx.restore();
    poly(ctx, P, null, "#15803D", 1.3);
    // Boundary pegs
    P.forEach(p => { box(ctx, p[0] - 1.5, p[1] - 5, 3, 6, 1, C.s100, C.s500, 0.9); });
    // Tree + sun
    line(ctx, 22, -2, 22, -9, "#78350F", 2); circ(ctx, 22, -14, 6.2, "#15803D", "#14532D", 1.1); circ(ctx, 20, -16, 2, "#4ADE80", null);
    circ(ctx, -30, -24, 5, C.goldHi, C.gold, 1.1);
    ctx.restore();
  }

function drawHouseShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 42, 4.5);
    box(ctx, -34, -6, 68, 34, 2, grad(ctx, -34, -6, 34, 28, C.white, C.s100), C.s400, 1.3);          // walls
    // Chimney, roof
    box(ctx, 14, -28, 8, 14, 1.5, t.deep, edge(t.deep), 1.1);
    poly(ctx, [[-40, -4], [0, -30], [40, -4]], grad(ctx, 0, -30, 0, -4, t.hi, t.lo), t.line, 1.3);
    poly(ctx, [[-40, -4], [40, -4], [38, 0], [-38, 0]], t.deep, null);
    line(ctx, -22, -9, -4, -22, "rgba(255,255,255,0.28)", 1.4);
    circ(ctx, 0, -12, 4, t.soft, t.line, 1.1);                                                       // gable window
    // Door
    box(ctx, -7, 8, 14, 20, [7, 7, 0, 0], t.m, t.line, 1.2);
    circ(ctx, 3.5, 19, 1.3, C.goldHi, null); box(ctx, -10, 27, 20, 2.5, 0.8, C.s300, C.s500, 0.9);
    // Windows
    [-26, 14].forEach(x => {
      box(ctx, x, 6, 14, 12, 1.5, grad(ctx, 0, 6, 0, 18, C.glassHi, C.glassLo), C.s500, 1.1);
      line(ctx, x + 7, 6, x + 7, 18, C.s500, 1); line(ctx, x, 12, x + 14, 12, C.s500, 1);
      box(ctx, x - 1.5, 18, 17, 2.4, 0.8, C.s300, C.s500, 0.8);
    });
    ctx.restore();
  }

function drawFactoryShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 46, 4.5);
    // Chimney + smoke
    box(ctx, 26, -26, 9, 32, 1.5, grad(ctx, 26, 0, 35, 0, C.s300, C.s500), C.s600, 1.2);
    ctx.fillStyle = t.m; ctx.fillRect(26, -26, 9, 4);
    [[31, -31, 4.2], [37, -37, 5.2], [31, -43, 6]].forEach(([x, y, r], i) => circ(ctx, x, y, r, `rgba(148,163,184,${0.5 - i * 0.12})`, null));
    // Main hall with sawtooth roof
    box(ctx, -42, -8, 78, 36, 2, grad(ctx, -42, -8, 36, 28, C.s100, C.s200), C.s500, 1.3);
    for (let i = 0; i < 3; i++) {
      const x = -42 + i * 24;
      poly(ctx, [[x, -8], [x, -24], [x + 24, -8]], grad(ctx, x, -24, x + 24, -8, t.hi, t.lo), t.line, 1.2);
      poly(ctx, [[x + 1.5, -9.5], [x + 1.5, -19], [x + 10.5, -9.5]], C.glass, null);
    }
    // Windows + roll door
    for (let i = 0; i < 3; i++) box(ctx, -37 + i * 14, -2, 10, 8, 1.5, grad(ctx, 0, -2, 0, 6, C.glassHi, C.glassLo), C.s500, 1);
    box(ctx, 6, 4, 22, 24, 2, C.s300, C.s600, 1.2);
    for (let y = 8; y < 28; y += 4) line(ctx, 7, y, 27, y, C.s500, 1);
    box(ctx, -42, 24, 78, 4, 1, t.deep, null);
    ctx.restore();
  }

function drawCourtShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 46, 4.5);
    const stone = vgrad(ctx, -30, 24, C.s100, 0.5);
    // Pediment with scale emblem
    poly(ctx, [[-44, -12], [0, -34], [44, -12]], grad(ctx, 0, -34, 0, -12, C.s50, C.s200), C.s500, 1.3);
    poly(ctx, [[-32, -14], [0, -29], [32, -14]], null, C.s300, 1);
    circ(ctx, 0, -19, 5.5, t.m, t.line, 1.1);
    line(ctx, -3.5, -19, 3.5, -19, C.white, 1.3); line(ctx, 0, -22.5, 0, -15.5, C.white, 1.3);
    // Entablature
    box(ctx, -46, -12, 92, 6, 1.5, C.s200, C.s500, 1.2);
    // Columns
    for (let i = 0; i < 4; i++) {
      const x = -36 + i * 24 - 4;
      box(ctx, x - 1.5, -6, 11, 3, 1, C.s200, C.s500, 1);
      box(ctx, x, -3, 8, 26, 1.5, grad(ctx, x, 0, x + 8, 0, C.s50, C.s200), C.s500, 1.1);
      line(ctx, x + 2.7, -2, x + 2.7, 21, C.s300, 0.9); line(ctx, x + 5.3, -2, x + 5.3, 21, C.s300, 0.9);
      box(ctx, x - 1.5, 23, 11, 3, 1, C.s200, C.s500, 1);
    }
    // Steps
    box(ctx, -48, 26, 96, 3.5, 1, C.s200, C.s500, 1.1); box(ctx, -44, 29.5, 88, 3.5, 1, C.s300, C.s500, 1.1);
    ctx.fillStyle = t.m; ctx.fillRect(-4, -6, 8, 0);
    ctx.restore();
  }

function drawBankShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    drawCourtShape(ctx, accentTheme);
    // Replace the scale emblem with a coin mark so a bank reads differently from a court
    ctx.save(); ctx.translate(0, -8);
    circ(ctx, 0, -19, 6.3, C.s100, null);
    circ(ctx, 0, -19, 5.6, C.gold, C.goldLo, 1.1);
    ctx.fillStyle = C.goldLo; ctx.font = "800 7.5px 'Plus Jakarta Sans', sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("\u20B9", 0, -18.5); ctx.textBaseline = "alphabetic";
    ctx.restore();
  }

function drawStoreShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 40, 4.5);
    box(ctx, -36, -10, 72, 38, 2, grad(ctx, -36, -10, 36, 28, C.white, C.s100), C.s400, 1.3);
    // Striped awning
    const n = 8, w = 80 / n;
    for (let i = 0; i < n; i++) {
      const x = -40 + i * w;
      poly(ctx, [[x, -22], [x + w, -22], [x + w + 1.5, -4], [x + 1.5 - 3, -4]], i % 2 ? C.white : t.m, t.line, 0.9);
      ctx.beginPath(); ctx.arc(x + w / 2 - 0.7, -4, w / 2, 0, Math.PI); ctx.fillStyle = i % 2 ? C.white : t.m; ctx.fill(); ctx.strokeStyle = t.line; ctx.lineWidth = 0.9; ctx.stroke();
    }
    box(ctx, -40, -26, 80, 5, 2, t.deep, edge(t.deep), 1.1);
    // Display window + door
    box(ctx, -30, 6, 34, 18, 2, grad(ctx, 0, 6, 0, 24, C.glassHi, C.glassLo), C.s500, 1.2);
    line(ctx, -26, 20, -18, 10, "rgba(255,255,255,0.8)", 1.6);
    box(ctx, 10, 4, 16, 24, [3, 3, 0, 0], t.m, t.line, 1.2); box(ctx, 13, 8, 10, 11, 1.5, C.glassHi, t.line, 0.9); circ(ctx, 23, 19, 1.2, C.goldHi, null);
    ctx.restore();
  }

function drawOfficeShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 32, 4);
    line(ctx, 0, -38, 0, -31, C.s500, 1.6); circ(ctx, 0, -39, 1.8, C.red, null);                       // antenna
    box(ctx, -22, -31, 44, 61, 3, grad(ctx, -22, -34, 22, 30, mix(t.m, 0.1), t.lo), t.line, 1.3);
    box(ctx, 22, -26, 12, 56, 2, grad(ctx, 22, 0, 34, 0, t.lo, t.deep), t.line, 1.2);               // side wing
    for (let r = 0; r < 6; r++) for (let c = 0; c < 4; c++) {
      const lit = (r * 3 + c * 5) % 7 < 3;
      box(ctx, -17 + c * 9.5, -25 + r * 7.2, 6.5, 4.6, 1, lit ? C.goldHi : C.glassHi, null);
    }
    for (let r = 0; r < 6; r++) box(ctx, 25, -21 + r * 7.2, 6, 4.6, 1, C.glassHi, null);
    box(ctx, -6, 20, 12, 10, [2, 2, 0, 0], C.glassHi, t.line, 1);
    ctx.restore();
  }

function drawBuildingShape(ctx, sub, accentTheme = {}) {
    const s = String(sub || "").toLowerCase();
    if (/factory|plant|mill|workshop/.test(s)) return drawFactoryShape(ctx, accentTheme);
    if (/court|tribunal|bench/.test(s)) return drawCourtShape(ctx, accentTheme);
    if (/bank|treasury|vault/.test(s)) return drawBankShape(ctx, accentTheme);
    if (/store|shop|market|retail/.test(s)) return drawStoreShape(ctx, accentTheme);
    return drawOfficeShape(ctx, accentTheme);
  }

function drawGoldBullionShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -6);
    ground(ctx, 0, 26, 40, 4);
    function bar(cx, cy, w, h) {
      const k = 6;                                                         // top-face inset
      poly(ctx, [[cx - w / 2 + k, cy - h], [cx + w / 2 - k, cy - h], [cx + w / 2, cy], [cx - w / 2, cy]], grad(ctx, 0, cy - h, 0, cy, "#FDE68A", "#EAB308"), C.goldLo, 1.2);
      poly(ctx, [[cx - w / 2 + k + 3, cy - h + 3], [cx + w / 2 - k - 3, cy - h + 3], [cx + w / 2 - 6, cy - 3], [cx - w / 2 + 6, cy - 3]], null, "rgba(161,98,7,0.5)", 0.9);
      line(ctx, cx - w / 2 + k + 4, cy - h + 1.6, cx - 2, cy - h + 1.6, "rgba(255,255,255,0.8)", 1.4);
    }
    bar(-22, 24, 40, 15); bar(22, 24, 40, 15); bar(0, 9, 40, 15);
    sparkle(ctx, 26, -14, 5, C.goldHi); sparkle(ctx, -28, -6, 3.2, C.goldHi); sparkle(ctx, 12, -24, 2.6, C.gold);
    ctx.restore();
  }

function bar(cx, cy, w, h) {
      const k = 6;                                                         // top-face inset
      poly(ctx, [[cx - w / 2 + k, cy - h], [cx + w / 2 - k, cy - h], [cx + w / 2, cy], [cx - w / 2, cy]], grad(ctx, 0, cy - h, 0, cy, "#FDE68A", "#EAB308"), C.goldLo, 1.2);
      poly(ctx, [[cx - w / 2 + k + 3, cy - h + 3], [cx + w / 2 - k - 3, cy - h + 3], [cx + w / 2 - 6, cy - 3], [cx - w / 2 + 6, cy - 3]], null, "rgba(161,98,7,0.5)", 0.9);
      line(ctx, cx - w / 2 + k + 4, cy - h + 1.6, cx - 2, cy - h + 1.6, "rgba(255,255,255,0.8)", 1.4);
    }

function drawJewelShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 24, 3.5);
    const g = t.m;
    poly(ctx, [[-22, -8], [-12, -22], [12, -22], [22, -8], [0, 26]], grad(ctx, -22, -22, 22, 26, mix(g, 0.45), g), t.line, 1.3);
    poly(ctx, [[-22, -8], [22, -8], [0, 26]], null, t.line, 1);
    poly(ctx, [[-12, -22], [-6, -8], [0, -22], [6, -8], [12, -22]], null, t.line, 1);
    line(ctx, -6, -8, 0, 26, t.line, 0.9); line(ctx, 6, -8, 0, 26, t.line, 0.9);
    poly(ctx, [[-12, -22], [-6, -8], [-22, -8]], "rgba(255,255,255,0.35)", null);
    poly(ctx, [[0, -22], [6, -8], [-6, -8]], "rgba(255,255,255,0.22)", null);
    sparkle(ctx, 24, -20, 5, C.white); sparkle(ctx, -26, -14, 3, C.white);
    ctx.restore();
  }

function drawCashBagShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 36, 4);
    // Sack
    const bag = new Path2D("M-8 -20 Q-16 -10 -26 4 Q-34 18 -22 26 Q0 32 22 26 Q34 18 26 4 Q16 -10 8 -20 Z");
    ctx.fillStyle = grad(ctx, -26, -20, 26, 28, t.hi, t.lo); ctx.fill(bag);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(bag);
    // Tied neck
    poly(ctx, [[-9, -20], [9, -20], [12, -27], [4, -24], [0, -29], [-4, -24], [-12, -27]], t.lo, t.line, 1.2);
    box(ctx, -10, -21, 20, 4.5, 2, C.gold, C.goldLo, 1.1);
    // Rupee medallion
    circ(ctx, 0, 6, 12.5, C.white, t.line, 1.3);
    circ(ctx, 0, 6, 9.6, t.soft, t.ring, 1);
    ctx.fillStyle = t.deep; ctx.font = "800 15px 'JetBrains Mono', monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("\u20B9", 0, 7); ctx.textBaseline = "alphabetic";
    // Coins at the base
    [[-30, 26], [-22, 29], [30, 27]].forEach(([x, y]) => { ctx.beginPath(); ctx.ellipse(x, y, 6, 2.6, 0, 0, Math.PI * 2); ctx.fillStyle = C.gold; ctx.fill(); ctx.strokeStyle = C.goldLo; ctx.lineWidth = 1; ctx.stroke(); });
    ctx.restore();
  }

function drawGoodsBoxShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 30, 4);
    const top = "#FCD9A0", left = "#E8A94E", right = "#C98A32", ln = "#8A5A1A";
    poly(ctx, [[-26, -8], [0, -20], [26, -8], [0, 4]], top, ln, 1.2);
    poly(ctx, [[-26, -8], [0, 4], [0, 30], [-26, 18]], left, ln, 1.2);
    poly(ctx, [[0, 4], [26, -8], [26, 18], [0, 30]], right, ln, 1.2);
    // Tape + label
    poly(ctx, [[-4, -18], [4, -14], [4, 6], [-4, 2]], "rgba(255,248,230,0.75)", null);
    poly(ctx, [[-4, 2], [4, 6], [4, 26.5], [-4, 28]], "rgba(255,248,230,0.6)", null);
    poly(ctx, [[-21, 4], [-8, 10], [-8, 19], [-21, 13]], C.white, "#B7791F", 0.9);
    line(ctx, -19, 7.5, -11, 11.5, C.s400, 1); line(ctx, -19, 10.5, -11, 14.5, C.s300, 1);
    // Fragile glass mark
    ctx.save(); ctx.translate(14, 10); ctx.transform(1, -0.45, 0, 1, 0, 0);
    ctx.strokeStyle = "#7C2D12"; ctx.lineWidth = 1.2; ctx.beginPath();
    ctx.moveTo(-3.5, -4.5); ctx.lineTo(3.5, -4.5); ctx.lineTo(1, 0); ctx.lineTo(1, 4); ctx.moveTo(-1, 4); ctx.lineTo(3, 4); ctx.moveTo(-1, 0); ctx.lineTo(-3.5, -4.5); ctx.stroke();
    ctx.restore();
    ctx.restore();
  }

function drawClothesShape(ctx, sub, accentTheme = {}) {
    const t = T(accentTheme);
    const s = String(sub || "").toLowerCase();
    ctx.save(); ctx.translate(0, -8);
    if (/cloth\b|fabric|textile|silk|cotton|wool|linen/.test(s) && !/clothes/.test(s)) {
      // Folded fabric bolt
      ground(ctx, 0, 26, 34, 4);
      box(ctx, -32, -12, 64, 34, 5, grad(ctx, 0, -12, 0, 22, "#FCD34D", "#F59E0B"), "#B45309", 1.3);
      for (let i = 0; i < 6; i++) line(ctx, -28, -6 + i * 5, 28, -6 + i * 5 + (i % 2 ? 0.8 : -0.8), "rgba(180,83,9,0.28)", 1.2);
      ctx.beginPath(); ctx.ellipse(-32, 5, 6, 17, 0, 0, Math.PI * 2); ctx.fillStyle = "#F59E0B"; ctx.fill(); ctx.strokeStyle = "#B45309"; ctx.lineWidth = 1.3; ctx.stroke();
      ctx.beginPath(); ctx.ellipse(-32, 5, 2.6, 7, 0, 0, Math.PI * 2); ctx.fillStyle = "#92400E"; ctx.fill();
      ctx.fillStyle = "#FEF3C7"; ctx.fillRect(-26, 16, 52, 3);
    } else {
      // Tailored blazer on a hanger
      ctx.strokeStyle = C.s600; ctx.lineWidth = 1.8; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(0, -24); ctx.bezierCurveTo(0, -29, 5, -30, 5, -33); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-26, -8); ctx.lineTo(0, -24); ctx.lineTo(26, -8); ctx.stroke();
      const col = C.green;
      const jacket = new Path2D("M-24 -8 L-12 -12 L0 -2 L12 -12 L24 -8 L30 22 L16 26 L16 28 L-16 28 L-16 26 L-30 22 Z");
      ctx.fillStyle = grad(ctx, -30, -12, 30, 28, mix(col, 0.2), mix(col, -0.06)); ctx.fill(jacket);
      ctx.strokeStyle = edge(col); ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(jacket);
      poly(ctx, [[-12, -12], [0, -2], [-5, 22], [-16, 8]], mix(col, -0.14), edge(col), 1.1);      // lapels
      poly(ctx, [[12, -12], [0, -2], [5, 22], [16, 8]], mix(col, -0.14), edge(col), 1.1);
      poly(ctx, [[-4, -9], [4, -9], [0, 0]], C.white, null);
      box(ctx, 8, 12, 9, 2.4, 1, mix(col, -0.3), null);                                           // pocket welt
      [2, 11].forEach(y => circ(ctx, 0.2, y, 1.7, C.goldHi, C.goldLo, 0.9));                       // buttons
      line(ctx, -22, 8, -26, 20, "rgba(0,0,0,0.18)", 1);                                           // sleeve seam
    }
    ctx.restore();
  }

function drawScaleShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 24, 3.5);
    const brass = "#D4A017";
    box(ctx, -16, 28, 32, 5, 2, "#A16207", "#713F12", 1.1);
    poly(ctx, [[-10, 28], [-3, -22], [3, -22], [10, 28]], grad(ctx, -10, 0, 10, 0, "#FDE68A", "#CA8A04"), "#854D0E", 1.2);
    circ(ctx, 0, -26, 4.6, C.goldHi, "#854D0E", 1.2);
    // Beam
    ctx.save(); ctx.translate(0, -22); ctx.rotate(-0.06);
    box(ctx, -38, -2, 76, 4.5, 2, grad(ctx, 0, -2, 0, 3, "#FDE68A", "#CA8A04"), "#854D0E", 1.2);
    [-34, 34].forEach(x => {
      line(ctx, x, 1, x - 11, 28, "#A16207", 1.1); line(ctx, x, 1, x + 11, 28, "#A16207", 1.1);
      ctx.beginPath(); ctx.moveTo(x - 14, 27); ctx.quadraticCurveTo(x, 40, x + 14, 27); ctx.closePath();
      ctx.fillStyle = grad(ctx, x - 14, 27, x + 14, 38, "#FDE68A", "#CA8A04"); ctx.fill(); ctx.strokeStyle = "#854D0E"; ctx.lineWidth = 1.2; ctx.stroke();
    });
    ctx.restore();
    ctx.restore();
  }

function drawGavelShape(ctx, accentTheme = {}) {
    const wood = "#8B4A2B";
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 30, 4);
    // Sound block
    ctx.beginPath(); ctx.ellipse(0, 26, 28, 7, 0, 0, Math.PI * 2); ctx.fillStyle = "#5C2E17"; ctx.fill();
    box(ctx, -26, 17, 52, 9, 3, grad(ctx, 0, 17, 0, 26, mix(wood, 0.2), wood), edge(wood), 1.2);
    ctx.beginPath(); ctx.ellipse(0, 17, 26, 5, 0, 0, Math.PI * 2); ctx.fillStyle = mix(wood, 0.28); ctx.fill(); ctx.strokeStyle = edge(wood); ctx.lineWidth = 1.2; ctx.stroke();
    // Mallet (angled)
    ctx.save(); ctx.translate(-4, 6); ctx.rotate(-0.62);
    box(ctx, -3, -2, 6, 40, 3, grad(ctx, -3, 0, 3, 0, mix(wood, 0.25), wood), edge(wood), 1.2);
    box(ctx, -20, -22, 40, 20, 5, grad(ctx, 0, -22, 0, -2, mix(wood, 0.28), wood), edge(wood), 1.3);
    box(ctx, -20, -17, 40, 3, 0, C.gold, C.goldLo, 0.9); box(ctx, -20, -9, 40, 3, 0, C.gold, C.goldLo, 0.9);
    ctx.restore();
    ctx.strokeStyle = C.gold; ctx.lineWidth = 1.4; ctx.lineCap = "round";
    [[-26, 6, -33, 2], [-27, 12, -35, 12], [26, 8, 32, 4]].forEach(a => line(ctx, a[0], a[1], a[2], a[3], C.gold, 1.4));   // impact marks
    ctx.restore();
  }

function drawDocumentShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 58, h = 66, x = -w / 2, y = -h / 2, f = 13;
    const sheet = new Path2D(`M${x + 4} ${y} L${x + w - f} ${y} L${x + w} ${y + f} L${x + w} ${y + h - 4} Q${x + w} ${y + h} ${x + w - 4} ${y + h} L${x + 4} ${y + h} Q${x} ${y + h} ${x} ${y + h - 4} L${x} ${y + 4} Q${x} ${y} ${x + 4} ${y} Z`);
    lift(ctx); ctx.fillStyle = grad(ctx, x, y, x + w, y + h, C.paper, C.paperLo); ctx.fill(sheet); noShadow(ctx);
    ctx.strokeStyle = C.s300; ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(sheet);
    poly(ctx, [[x + w - f, y], [x + w - f, y + f], [x + w, y + f]], C.paperLo, C.s300, 1.1);
    line(ctx, x + 9, y + 12, x + 30, y + 12, t.m, 2.4);                       // title
    for (let i = 0; i < 6; i++) line(ctx, x + 9, y + 21 + i * 6, x + w - 9 - (i === 5 ? 18 : 0), y + 21 + i * 6, C.s300, 1.5);
    // Signature + wax seal
    ctx.strokeStyle = "#1D4ED8"; ctx.lineWidth = 1.2; ctx.beginPath();
    ctx.moveTo(x + 9, y + h - 9); ctx.bezierCurveTo(x + 13, y + h - 17, x + 17, y + h - 4, x + 21, y + h - 11); ctx.bezierCurveTo(x + 24, y + h - 15, x + 26, y + h - 8, x + 30, y + h - 10); ctx.stroke();
    circ(ctx, x + w - 13, y + h - 12, 8, C.red, C.redLo, 1.3);
    circ(ctx, x + w - 13, y + h - 12, 5, null, "rgba(255,255,255,0.55)", 1);
    sparkle(ctx, x + w - 13, y + h - 12, 3, "rgba(255,255,255,0.85)");
    ctx.restore();
  }

function drawMoneyShape(ctx, accentTheme = {}) { return drawCashBagShape(ctx, accentTheme); }

function drawShieldShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 22, 3.5);
    const sh = new Path2D("M0 -32 L26 -23 L26 2 Q26 22 0 34 Q-26 22 -26 2 L-26 -23 Z");
    lift(ctx); ctx.fillStyle = grad(ctx, -26, -32, 26, 34, t.hi, t.lo); ctx.fill(sh); noShadow(ctx);
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.4; ctx.lineJoin = "round"; ctx.stroke(sh);
    const inner = new Path2D("M0 -25 L19 -18.5 L19 1 Q19 16 0 26 Q-19 16 -19 1 L-19 -18.5 Z");
    ctx.strokeStyle = "rgba(255,255,255,0.55)"; ctx.lineWidth = 1.2; ctx.stroke(inner);
    ctx.strokeStyle = C.white; ctx.lineWidth = 4; ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.beginPath(); ctx.moveTo(-9, 0); ctx.lineTo(-2.5, 7); ctx.lineTo(10, -8); ctx.stroke();
    ctx.restore();
  }

function drawLegalSymbolShape(ctx, sub, accentTheme = {}) {
    const s = String(sub || "").toLowerCase();
    if (/gavel|verdict|decree|mallet/.test(s)) return drawGavelShape(ctx, accentTheme);
    if (/scale|justice|balance/.test(s)) return drawScaleShape(ctx, accentTheme);
    if (/money|cash|rupee|currency|fund|fee/.test(s)) return drawCashBagShape(ctx, accentTheme);
    if (/gold|bullion/.test(s)) return drawGoldBullionShape(ctx, accentTheme);
    if (/jewel|diamond|gem/.test(s)) return drawJewelShape(ctx, accentTheme);
    if (/shield|immunity|protection/.test(s)) return drawShieldShape(ctx, accentTheme);
    return drawDocumentShape(ctx, accentTheme);
  }

/* ==========================================================================
     CATEGORY 1: PEOPLE & ROLES
     ========================================================================== */

  function drawPersonShape(ctx, role = "man", accentTheme = {}) {
    const t = T(accentTheme);
    const r = String(role || "man").toLowerCase();
    const isCA = /accountant|^ca$|auditor|bookkeeper/.test(r);
    const isDoc = /doctor|physician/.test(r);
    const isJudge = /judge|lawyer|advocate/.test(r);
    const isWoman = /woman|female|lady|girl/.test(r);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 30, 24, 3.5);

    // Torso (rounded shoulders)
    const torso = new Path2D("M-24 30 L-24 12 Q-24 0 -12 -2 L12 -2 Q24 0 24 12 L24 30 Z");
    const coat = isDoc ? C.white : isJudge ? C.ink : isCA ? "#1E3A8A" : isWoman ? t.m : "#1E40AF";
    ctx.fillStyle = grad(ctx, -24, -2, 24, 30, mix(coat, coat === C.white ? 0 : 0.14), coat === C.white ? C.s100 : mix(coat, -0.08));
    ctx.fill(torso); ctx.strokeStyle = coat === C.white ? C.s300 : (coat === C.ink ? C.s600 : edge(coat)); ctx.lineWidth = 1.3; ctx.lineJoin = "round"; ctx.stroke(torso);

    box(ctx, -4.5, -8, 9, 9, 3, C.skinLo, null);

    if (isDoc) {
      poly(ctx, [[-6, -2], [0, 14], [6, -2]], "#0D9488", null);
      ctx.strokeStyle = "#1D4ED8"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(0, 4, 9, 0.35, Math.PI - 0.35); ctx.stroke();
      circ(ctx, 7.5, 11, 3, C.s200, C.s500, 1);
      box(ctx, -17, 15, 8, 6, 1.5, C.white, C.s300, 1);
      line(ctx, -15.5, 17, -10.5, 17, "#0D9488", 1.2);
    } else if (isJudge) {
      poly(ctx, [[-4, -2], [0, 14], [4, -2]], C.white, null);
      box(ctx, -5.5, -2, 4, 16, 1, C.white, C.s300, 0.8); box(ctx, 1.5, -2, 4, 16, 1, C.white, C.s300, 0.8);
      line(ctx, 0, 14, 0, 30, "#334155", 1);
    } else if (isWoman) {
      poly(ctx, [[-9, -2], [0, 12], [9, -2]], "#FEF3C7", edge("#FEF3C7"), 1);
      circ(ctx, 0, 10, 2, C.gold, C.goldLo, 1);
    } else {
      poly(ctx, [[-8, -2], [0, 13], [8, -2]], C.white, C.s300, 1);
      poly(ctx, [[-2.4, 0], [2.4, 0], [3.4, 12], [0, 17], [-3.4, 12]], isCA ? C.red : "#3B82F6", null);
      line(ctx, -14, 4, -14, 22, "rgba(255,255,255,0.2)", 1);
    }

    if (isCA) {
      ctx.save(); ctx.translate(16, 14); ctx.rotate(0.1);
      box(ctx, -7, -9, 15, 20, 2, "#065F46", "#022C22", 1.2);
      ctx.fillStyle = C.gold; ctx.fillRect(-7, -9, 3.2, 20);
      line(ctx, -1, -3, 5, -3, "rgba(255,255,255,0.8)", 1.4); line(ctx, -1, 1, 5, 1, "rgba(255,255,255,0.5)", 1.4);
      ctx.restore();
    } else if (!isDoc && !isJudge && !isWoman) {
      box(ctx, 14, 16, 14, 11, 2, "#7C4A24", "#4A2B12", 1.2);
      ctx.strokeStyle = "#4A2B12"; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.arc(21, 16, 3.2, Math.PI, 0); ctx.stroke();
      line(ctx, 14, 21, 28, 21, "#4A2B12", 0.9); box(ctx, 19.5, 19.5, 3, 3, 0.8, C.gold, null);
    }

    // Head
    ctx.beginPath(); ctx.ellipse(0, -17, 10, 11.5, 0, 0, Math.PI * 2);
    ctx.fillStyle = grad(ctx, -8, -28, 8, -6, mix(C.skin, 0.1), C.skin); ctx.fill();
    ctx.strokeStyle = edge(C.skinLo); ctx.lineWidth = 1.2; ctx.stroke();
    ctx.beginPath(); ctx.ellipse(-10, -16, 1.6, 2.6, 0, 0, Math.PI * 2); ctx.fillStyle = C.skin; ctx.fill();
    ctx.beginPath(); ctx.ellipse(10, -16, 1.6, 2.6, 0, 0, Math.PI * 2); ctx.fill();

    const hairCol = isWoman ? C.hairBrown : C.hair;
    ctx.fillStyle = hairCol;
    if (isWoman) {
      ctx.beginPath(); ctx.moveTo(-11, -14); ctx.quadraticCurveTo(-13, -31, 0, -30); ctx.quadraticCurveTo(13, -31, 11, -14);
      ctx.lineTo(13, 4); ctx.quadraticCurveTo(9, 6, 8, 1); ctx.lineTo(8, -17); ctx.quadraticCurveTo(0, -24, -8, -17); ctx.lineTo(-8, 1);
      ctx.quadraticCurveTo(-9, 6, -13, 4); ctx.closePath(); ctx.fill();
    } else {
      ctx.beginPath(); ctx.moveTo(-10.5, -17); ctx.quadraticCurveTo(-12, -30, 0, -29.5); ctx.quadraticCurveTo(12, -30, 10.5, -17);
      ctx.quadraticCurveTo(9, -23, 3, -23.5); ctx.quadraticCurveTo(-4, -22, -10.5, -17); ctx.closePath(); ctx.fill();
    }
    circ(ctx, -3.8, -16.5, 1.25, C.ink, null); circ(ctx, 3.8, -16.5, 1.25, C.ink, null);
    ctx.strokeStyle = "#9A3412"; ctx.lineWidth = 1.1; ctx.lineCap = "round";
    ctx.beginPath(); ctx.arc(0, -13.4, 3.4, 0.25, Math.PI - 0.25); ctx.stroke();
    if (isCA) {
      ctx.strokeStyle = "#92400E"; ctx.lineWidth = 1.2;
      rr(ctx, -8, -19.5, 6, 5, 1.8); ctx.stroke(); rr(ctx, 2, -19.5, 6, 5, 1.8); ctx.stroke(); line(ctx, -2, -17.5, 2, -17.5, "#92400E", 1.1);
    }
    ctx.restore();
  }

  function drawOfficerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 30, 24, 3.5);
    // Torso khaki / police navy uniform
    const torso = new Path2D("M-24 30 L-24 12 Q-24 0 -12 -2 L12 -2 Q24 0 24 12 L24 30 Z");
    ctx.fillStyle = grad(ctx, -24, -2, 24, 30, "#334155", "#1E293B"); ctx.fill(torso);
    ctx.strokeStyle = C.s800; ctx.lineWidth = 1.3; ctx.stroke(torso);
    // Gold badge & shoulder epaulettes
    box(ctx, -23, 3, 8, 3.5, 1, C.gold, C.goldLo, 1); box(ctx, 15, 3, 8, 3.5, 1, C.gold, C.goldLo, 1);
    poly(ctx, [[-13, 10], [-8, 10], [-6, 17], [-10.5, 21], [-15, 17]], C.gold, C.goldLo, 1);
    box(ctx, -4.5, -8, 9, 9, 3, C.skinLo, null);
    // Head
    circ(ctx, 0, -17, 10.5, C.skin, edge(C.skinLo), 1.2);
    circ(ctx, -3.8, -16.5, 1.25, C.ink, null); circ(ctx, 3.8, -16.5, 1.25, C.ink, null);
    // Peaked Officer Cap
    poly(ctx, [[-15, -22], [-14, -31], [14, -31], [15, -22]], "#1E293B", C.s800, 1.2);
    box(ctx, -16, -23, 32, 4.5, 1, C.gold, C.goldLo, 1);
    poly(ctx, [[-14, -20], [14, -20], [12, -18], [-12, -18]], C.ink, null);
    circ(ctx, 0, -26.5, 2.5, C.goldHi, C.goldLo, 1);
    ctx.restore();
  }

  function drawEngineerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 30, 24, 3.5);
    const torso = new Path2D("M-24 30 L-24 12 Q-24 0 -12 -2 L12 -2 Q24 0 24 12 L24 30 Z");
    ctx.fillStyle = "#F97316"; ctx.fill(torso); ctx.strokeStyle = "#C2410C"; ctx.lineWidth = 1.3; ctx.stroke(torso); // hi-vis orange vest
    // Reflective silver bands
    ctx.fillStyle = C.s100; ctx.fillRect(-22, 12, 44, 4); ctx.fillRect(-22, 22, 44, 4);
    box(ctx, -4.5, -8, 9, 9, 3, C.skinLo, null);
    circ(ctx, 0, -17, 10.5, C.skin, edge(C.skinLo), 1.2);
    circ(ctx, -3.8, -16.5, 1.25, C.ink, null); circ(ctx, 3.8, -16.5, 1.25, C.ink, null);
    // Yellow Safety Hard-hat
    poly(ctx, [[-15, -22], [0, -33], [15, -22]], C.gold, C.goldLo, 1.2);
    box(ctx, -17, -22, 34, 4, 1.5, C.goldHi, C.goldLo, 1);
    line(ctx, 0, -32, 0, -22, C.goldLo, 1.5); // center ridge
    // Rolled blueprint in arm
    ctx.save(); ctx.translate(16, 16); ctx.rotate(-0.4);
    box(ctx, -4, -14, 8, 28, 3, C.glassHi, C.sky, 1.1);
    line(ctx, -4, 0, 4, 0, C.red, 1.4);
    ctx.restore();
    ctx.restore();
  }

  function drawElderlyShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 30, 24, 3.5);
    const torso = new Path2D("M-22 30 L-22 12 Q-22 0 -11 -2 L11 -2 Q22 0 22 12 L22 30 Z");
    ctx.fillStyle = "#475569"; ctx.fill(torso); ctx.strokeStyle = C.s700; ctx.lineWidth = 1.3; ctx.stroke(torso);
    // Warm beige knitted shawl
    poly(ctx, [[-20, 4], [0, 22], [20, 4], [14, 0], [0, 14], [-14, 0]], "#D6D3D1", "#A8A29E", 1.2);
    box(ctx, -4.5, -8, 9, 9, 3, C.skinLo, null);
    circ(ctx, 0, -17, 10.5, C.skin, edge(C.skinLo), 1.2);
    // Silver grey hair
    ctx.beginPath(); ctx.arc(0, -20, 11, Math.PI, 0); ctx.fillStyle = C.s300; ctx.fill(); ctx.strokeStyle = C.s400; ctx.stroke();
    // Round reading spectacles
    ctx.strokeStyle = C.s700; ctx.lineWidth = 1.1;
    circ(ctx, -4.5, -16.5, 3.2, "rgba(255,255,255,0.45)", C.s700, 1);
    circ(ctx, 4.5, -16.5, 3.2, "rgba(255,255,255,0.45)", C.s700, 1);
    line(ctx, -1.3, -16.5, 1.3, -16.5, C.s700, 1);
    // Wooden walking cane
    line(ctx, 22, 10, 22, 30, "#78350F", 2.4);
    ctx.beginPath(); ctx.arc(19, 10, 3, 0, Math.PI, true); ctx.strokeStyle = "#78350F"; ctx.lineWidth = 2.4; ctx.stroke();
    ctx.restore();
  }

  function drawChildShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -4);
    ground(ctx, 0, 26, 18, 3);
    // Small torso with bright colored t-shirt
    const torso = new Path2D("M-17 26 L-17 12 Q-17 2 -8 0 L8 0 Q17 2 17 12 L17 26 Z");
    ctx.fillStyle = t.m; ctx.fill(torso); ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.stroke(torso);
    box(ctx, -3.5, -6, 7, 7, 2, C.skinLo, null);
    // Big expressive head
    circ(ctx, 0, -15, 11.5, C.skin, edge(C.skinLo), 1.2);
    circ(ctx, -4.5, -14.5, 1.6, C.ink, null); circ(ctx, 4.5, -14.5, 1.6, C.ink, null);
    ctx.strokeStyle = "#9A3412"; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(0, -11, 4, 0.2, Math.PI - 0.2); ctx.stroke();
    // Playful tuft hair
    ctx.beginPath(); ctx.arc(0, -18, 12, Math.PI * 0.9, Math.PI * 2.1); ctx.fillStyle = C.hairBrown; ctx.fill();
    ctx.restore();
  }

  function drawPartnersShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 42, 4);
    // Left partner (gentleman)
    ctx.save(); ctx.translate(-18, 0); ctx.scale(0.88, 0.88);
    drawPersonShape(ctx, "man", accentTheme);
    ctx.restore();
    // Right partner (lady)
    ctx.save(); ctx.translate(18, 0); ctx.scale(0.88, 0.88);
    drawPersonShape(ctx, "woman", accentTheme);
    ctx.restore();
    // Intertwined collaboration link symbol in center
    circ(ctx, 0, 16, 5, C.goldHi, C.goldLo, 1.1);
    ctx.fillStyle = C.goldLo; ctx.font = "800 7px 'Plus Jakarta Sans', sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("&", 0, 16);
    ctx.restore();
  }

  function drawCrowdShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 48, 4.5);
    // Back left and back right figures
    ctx.save(); ctx.translate(-24, -4); ctx.scale(0.72, 0.72); ctx.globalAlpha = 0.8;
    drawPersonShape(ctx, "man", accentTheme);
    ctx.restore();
    ctx.save(); ctx.translate(24, -4); ctx.scale(0.72, 0.72); ctx.globalAlpha = 0.8;
    drawPersonShape(ctx, "woman", accentTheme);
    ctx.restore();
    // Front prominent center leader
    ctx.save(); ctx.translate(0, 4); ctx.scale(0.92, 0.92);
    drawPersonShape(ctx, "man", accentTheme);
    ctx.restore();
    ctx.restore();
  }

  function drawBoardroomShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 46, 4.5);
    // Large polished mahogany conference table
    const tab = [[-42, 6], [0, -14], [42, 6], [0, 26]];
    poly(ctx, tab, grad(ctx, 0, -14, 0, 26, "#78350F", "#451A03"), "#291305", 1.4);
    poly(ctx, [[-42, 6], [0, 26], [0, 31], [-42, 11]], "#451A03", null);
    poly(ctx, [[0, 26], [42, 6], [42, 11], [0, 31]], "#291305", null);
    line(ctx, -26, 4, 0, -7, "rgba(255,255,255,0.3)", 1.4);
    // Executive leather chairs placed around table
    [[-32, -6], [-10, -18], [10, -18], [32, -6], [-28, 22], [0, 29], [28, 22]].forEach(([cx, cy]) => {
      circ(ctx, cx, cy, 4.8, C.s800, C.s600, 1.1);
      circ(ctx, cx, cy, 2.4, t.m, null);
    });
    ctx.restore();
  }

  function drawPedestrianShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 22, 3);
    // Walking figure with separated limbs
    line(ctx, -4, 14, -12, 30, C.s800, 3.5); // back leg
    line(ctx, 2, 14, 12, 30, C.s800, 3.5);  // forward leg
    box(ctx, -8, -2, 16, 18, 3, t.m, t.line, 1.3); // jacket
    line(ctx, -6, 2, -14, 14, C.s700, 2.5); // swinging arm
    box(ctx, -2.5, -8, 5, 7, 2, C.skinLo, null);
    circ(ctx, 0, -16, 9, C.skin, edge(C.skinLo), 1.2);
    circ(ctx, 2, -16, 1.2, C.ink, null);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 2: VEHICLES & TRANSIT (Expanded)
     ========================================================================== */

  function drawShipShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 46, 4);
    // Hull
    const hull = new Path2D("M-44 4 L-38 18 Q0 24 38 18 L46 4 L-44 4 Z");
    ctx.fillStyle = grad(ctx, 0, 4, 0, 22, "#1E293B", "#0F172A"); ctx.fill(hull);
    ctx.strokeStyle = C.s800; ctx.lineWidth = 1.3; ctx.stroke(hull);
    // Red statutory waterline
    ctx.fillStyle = C.red; ctx.fillRect(-41, 14, 82, 3);
    // Bridge superstructure & containers
    box(ctx, -34, -8, 48, 12, 2, t.m, t.line, 1.1); // shipping container stack
    box(ctx, -26, -18, 32, 10, 2, C.gold, C.goldLo, 1.1);
    box(ctx, 18, -22, 16, 26, 2, C.white, C.s400, 1.2); // navigation bridge
    for (let i = 0; i < 3; i++) box(ctx, 21 + i * 4.2, -18, 2.8, 3, 0.5, C.glassHi, C.s500, 0.8);
    line(ctx, 26, -22, 26, -30, C.s600, 1.5); circ(ctx, 26, -31, 1.8, C.red, null); // mast
    // Water wake ripples
    ctx.strokeStyle = C.skyHi; ctx.lineWidth = 1.2;
    line(ctx, -48, 20, -32, 20, C.skyHi, 1.2); line(ctx, 32, 20, 48, 20, C.skyHi, 1.2);
    ctx.restore();
  }

  function drawAircraftShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 38, 3.5);
    // Fuselage
    const fuse = new Path2D("M-44 0 Q-46 -6 -32 -6 L34 -6 Q46 -6 46 0 Q46 6 34 6 L-32 6 Q-46 6 -44 0 Z");
    ctx.fillStyle = grad(ctx, 0, -6, 0, 6, C.white, C.s200); ctx.fill(fuse);
    ctx.strokeStyle = C.s400; ctx.lineWidth = 1.3; ctx.stroke(fuse);
    // Cockpit & passenger windows
    poly(ctx, [[36, -3], [42, -2], [42, 1], [36, 1]], C.glassHi, C.s600, 1);
    for (let x = -20; x < 28; x += 6) circ(ctx, x, -1, 1.2, C.glassLo, null);
    // Wing
    poly(ctx, [[-6, 0], [10, 0], [-2, 26], [-12, 26]], grad(ctx, 0, 0, 0, 26, C.s100, C.s300), C.s500, 1.2);
    box(ctx, -4, 14, 5, 8, 2, t.m, t.line, 1); // turbofan engine
    // Tail fin
    poly(ctx, [[-36, -6], [-26, -6], [-38, -26], [-44, -26]], t.m, t.line, 1.2);
    ctx.restore();
  }

  function drawTrainShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 46, 4);
    // Rails
    line(ctx, -48, 20, 48, 20, C.s600, 2); line(ctx, -48, 24, 48, 24, C.s600, 2);
    for (let x = -44; x <= 44; x += 8) line(ctx, x, 18, x, 26, "#78350F", 2.2);
    // Locomotive Body
    box(ctx, -44, -18, 88, 32, 4, grad(ctx, 0, -18, 0, 14, t.hi, t.lo), t.line, 1.3);
    poly(ctx, [[30, -18], [44, -4], [44, 14], [30, 14]], t.deep, null); // aerodynamic nose
    poly(ctx, [[28, -14], [38, -4], [32, 2], [24, 2]], C.glassHi, C.s600, 1.1); // windshield
    for (let x = -36; x < 16; x += 12) box(ctx, x, -8, 8, 8, 1.5, C.glassHi, C.s500, 1);
    box(ctx, 42, 6, 4, 4, 1, "#FEF9C3", C.goldLo, 1); // headlight
    // Under-chassis bogies & wheels
    [-28, -14, 12, 26].forEach(x => wheel(ctx, x, 17, 6.5, C.s200));
    ctx.restore();
  }

  function drawBusShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 44, 4.5);
    box(ctx, -42, -22, 84, 36, 4, grad(ctx, 0, -22, 0, 14, "#F59E0B", "#D97706"), "#B45309", 1.3);
    // Windshield & side windows
    box(ctx, 24, -18, 15, 16, 2, C.glassHi, C.s600, 1.1);
    for (let x = -36; x < 18; x += 11) box(ctx, x, -16, 8, 12, 1.5, C.glassHi, C.s600, 1);
    ctx.fillStyle = t.m; ctx.fillRect(-42, 2, 84, 4); // livery band
    box(ctx, 39, 6, 4, 4, 1, "#FEF9C3", C.goldLo, 1); // headlight
    wheel(ctx, -24, 15, 8.5, C.s200); wheel(ctx, 24, 15, 8.5, C.s200);
    ctx.restore();
  }

  function drawTankerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 46, 4.5);
    // Cylindrical tanker tank
    box(ctx, -46, -20, 56, 30, 12, grad(ctx, 0, -20, 0, 10, C.white, C.s300), C.s500, 1.3);
    box(ctx, -38, -23, 10, 3, 1, C.s600, null); box(ctx, -14, -23, 10, 3, 1, C.s600, null); // manhole caps
    box(ctx, -24, -8, 12, 12, 1, C.red, C.redLo, 1); // hazmat diamond
    // Cab
    poly(ctx, [[13, 10], [13, -16], [28, -16], [38, -2], [42, 10]], t.m, t.line, 1.3);
    poly(ctx, [[18, -4], [18, -13], [27, -13], [34, -4]], C.glassHi, C.s600, 1);
    box(ctx, 40, 3, 3, 4, 1, "#FEF9C3", C.goldLo, 1);
    [-32, -18, 28].forEach(x => wheel(ctx, x, 14, 8, C.s200));
    ctx.restore();
  }

  function drawCargoContainerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 42, 4);
    box(ctx, -42, -22, 84, 44, 3, grad(ctx, -42, -22, 42, 22, t.hi, t.lo), t.line, 1.3);
    for (let x = -34; x <= 34; x += 8.5) line(ctx, x, -20, x, 20, t.deep, 1.2); // corrugated ribs
    // Locking door bar & seal
    line(ctx, 0, -22, 0, 22, C.s800, 2);
    circ(ctx, 0, 0, 4, C.goldHi, C.goldLo, 1.1);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 3: PROPERTY & BUILDINGS (Expanded)
     ========================================================================== */

  function drawWarehouseShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 46, 4.5);
    // Main warehouse gable hall
    poly(ctx, [[-44, 26], [-44, -8], [0, -28], [44, -8], [44, 26]], grad(ctx, 0, -28, 0, 26, C.s100, C.s200), C.s500, 1.3);
    poly(ctx, [[-46, -7], [0, -30], [46, -7]], null, t.m, 2.5); // overhang roof line
    // Two large roller shutter loading doors
    [-24, 10].forEach(x => {
      box(ctx, x, 2, 22, 24, 2, C.s300, C.s600, 1.2);
      for (let y = 6; y < 26; y += 4) line(ctx, x + 1, y, x + 21, y, C.s500, 1);
    });
    circ(ctx, 0, -14, 4, C.glassHi, C.s500, 1); // gable ventilation fan
    ctx.restore();
  }

  function drawHospitalShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 44, 4.5);
    box(ctx, -38, -26, 76, 54, 3, grad(ctx, 0, -26, 0, 28, C.white, C.s100), C.s400, 1.3);
    // Medical Cross Emblem on top marquee
    box(ctx, -14, -36, 28, 12, 2, C.white, C.s400, 1.2);
    ctx.fillStyle = C.red;
    ctx.fillRect(-8, -32, 16, 4); ctx.fillRect(-2, -38, 4, 16);
    // Windows grid
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) {
      box(ctx, -30 + c * 16, -18 + r * 12, 10, 8, 1.5, C.glassHi, C.s500, 1);
    }
    // Emergency entrance
    box(ctx, -10, 14, 20, 14, [2, 2, 0, 0], C.glassHi, C.red, 1.2);
    ctx.restore();
  }

  function drawHotelShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 44, 4.5);
    box(ctx, -36, -30, 72, 58, 3, grad(ctx, 0, -30, 0, 28, "#F5F3FF", "#DDD6FE"), "#7C3AED", 1.3);
    // Grand entrance canopy
    poly(ctx, [[-18, 16], [18, 16], [22, 24], [-22, 24]], C.gold, C.goldLo, 1.1);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) {
      box(ctx, -26 + c * 20, -22 + r * 10, 12, 6, 1, C.glassHi, C.s600, 0.9);
      line(ctx, -26 + c * 20, -16 + r * 10, -14 + c * 20, -16 + r * 10, C.gold, 1.2); // balcony rail
    }
    sparkle(ctx, 0, -35, 4, C.goldHi); // 5-star crown
    ctx.restore();
  }

  function drawSchoolShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 46, 4.5);
    box(ctx, -42, -8, 84, 36, 2, grad(ctx, 0, -8, 0, 28, "#FEF3C7", "#FDE68A"), "#B45309", 1.3);
    // Central clock bell tower
    poly(ctx, [[-16, -8], [0, -32], [16, -8]], "#B45309", "#78350F", 1.3);
    box(ctx, -12, -8, 24, 36, 1, "#FDE68A", "#B45309", 1.2);
    circ(ctx, 0, -18, 5, C.white, C.ink, 1.2); // academic clock
    line(ctx, 0, -18, 0, -15, C.ink, 1.2); line(ctx, 0, -18, 2.5, -18, C.ink, 1.2);
    // Arched library windows
    for (let i = 0; i < 4; i++) {
      const x = i < 2 ? (-38 + i * 14) : (14 + (i - 2) * 14);
      box(ctx, x, 0, 10, 18, [5, 5, 0, 0], C.glassHi, C.s600, 1);
    }
    ctx.restore();
  }

  function drawSiloShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 28, 4);
    box(ctx, -20, -16, 40, 44, 3, grad(ctx, -20, 0, 20, 0, C.white, C.s300), C.s500, 1.3);
    poly(ctx, [[-22, -16], [0, -34], [22, -16]], grad(ctx, -22, -34, 22, -16, C.s100, C.s300), C.s500, 1.3);
    for (let y = -8; y < 24; y += 8) line(ctx, -20, y, 20, y, C.s400, 1.1); // steel ribs
    ctx.restore();
  }

  function drawCustomsHouseShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    drawCourtShape(ctx, accentTheme);
    // Anchor emblem on pediment
    ctx.save(); ctx.translate(0, -8);
    circ(ctx, 0, -19, 6.5, C.s100, null);
    ctx.strokeStyle = t.m; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.arc(0, -20, 2.5, 0, Math.PI * 2); ctx.stroke();
    line(ctx, 0, -17.5, 0, -12, t.m, 1.6);
    ctx.beginPath(); ctx.arc(0, -15, 4.5, 0.2, Math.PI - 0.2); ctx.stroke();
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 4: GOODS & COMMODITIES (Expanded)
     ========================================================================== */

  function drawSackBaleShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 30, 4);
    // Burlap Gunny Sack
    const sack = new Path2D("M-8 -18 Q-18 -8 -22 6 Q-26 20 -16 26 Q0 30 16 26 Q26 20 22 6 Q18 -8 8 -18 Z");
    ctx.fillStyle = grad(ctx, -22, -18, 22, 28, "#EAB308", "#A16207"); ctx.fill(sack);
    ctx.strokeStyle = "#713F12"; ctx.lineWidth = 1.3; ctx.stroke(sack);
    // Stitched wheat ear stencil
    ctx.strokeStyle = "rgba(113, 63, 18, 0.55)"; ctx.lineWidth = 1.5;
    line(ctx, 0, -4, 0, 18, "rgba(113, 63, 18, 0.55)", 1.5);
    for (let i = 0; i < 4; i++) {
      line(ctx, 0, 0 + i * 4, -4, -3 + i * 4, "rgba(113, 63, 18, 0.55)", 1.2);
      line(ctx, 0, 0 + i * 4, 4, -3 + i * 4, "rgba(113, 63, 18, 0.55)", 1.2);
    }
    // Tied rope collar
    box(ctx, -9, -19, 18, 4, 1.5, "#FEF08A", "#854D0E", 1);
    ctx.restore();
  }

  function drawMachineryShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 38, 4);
    box(ctx, -34, -14, 68, 40, 4, grad(ctx, 0, -14, 0, 26, C.s600, C.s800), C.s500, 1.3);
    // Two interlocking brass gears
    function gear(cx, cy, r, teeth) {
      circ(ctx, cx, cy, r, C.gold, C.goldLo, 1.2);
      circ(ctx, cx, cy, r * 0.4, C.s800, null);
      for (let i = 0; i < teeth; i++) {
        const a = (i / teeth) * Math.PI * 2;
        box(ctx, cx + Math.cos(a) * r - 2, cy + Math.sin(a) * r - 2, 4, 4, 1, C.goldHi, null);
      }
    }
    gear(-12, 2, 13, 8);
    gear(14, 8, 9, 6);
    // Emergency STOP button
    circ(ctx, -22, -6, 4, C.red, C.redLo, 1);
    ctx.restore();
  }

  function drawSmartphoneShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 32, 22, 3.5);
    lift(ctx);
    box(ctx, -17, -32, 34, 64, 6, grad(ctx, -17, -32, 17, 32, C.s800, C.ink), null);
    noShadow(ctx);
    box(ctx, -17, -32, 34, 64, 6, null, C.s400, 1.3);
    // Glass display screen
    box(ctx, -14, -28, 28, 56, 4, grad(ctx, 0, -28, 0, 28, "#1E1B4B", "#312E81"), null);
    // Dynamic island / camera punch & home indicator
    circ(ctx, 0, -25, 1.5, C.s800, null);
    line(ctx, -8, 24, 8, 24, C.white, 1.5);
    // Screen gloss reflection
    poly(ctx, [[-14, -28], [10, -28], [-14, 14]], "rgba(255,255,255,0.18)", null);
    ctx.restore();
  }

  function drawLaptopShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 44, 4.5);
    // Screen display open
    poly(ctx, [[-30, -24], [30, -24], [34, 12], [-34, 12]], grad(ctx, 0, -24, 0, 12, C.s800, C.ink), C.s400, 1.3);
    box(ctx, -26, -20, 52, 28, 2, grad(ctx, 0, -20, 0, 8, C.glassHi, C.glassLo), C.s500, 1);
    // Keyboard base deck
    poly(ctx, [[-42, 14], [42, 14], [38, 26], [-38, 26]], grad(ctx, 0, 14, 0, 26, C.s200, C.s300), C.s500, 1.2);
    box(ctx, -10, 20, 20, 4, 1, C.s400, null); // trackpad
    ctx.restore();
  }

  function drawCameraCctvShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 3.5);
    // Mount bracket & arm
    box(ctx, -28, -12, 6, 24, 2, C.s700, null);
    line(ctx, -22, 0, -10, 0, C.s600, 3.5);
    // Camera cylindrical housing angled down
    ctx.save(); ctx.translate(0, 0); ctx.rotate(0.25);
    box(ctx, -14, -10, 36, 20, 4, grad(ctx, 0, -10, 0, 10, C.white, C.s200), C.s500, 1.3);
    box(ctx, 22, -8, 6, 16, 2, C.ink, null); // lens hood
    circ(ctx, 25, 0, 5, C.sky, C.skyLo, 1); // lens optic
    circ(ctx, -10, -5, 1.5, C.red, null); // recording red LED
    ctx.restore();
    ctx.restore();
  }

  function drawWatchShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 20, 3);
    // Stitched leather strap
    box(ctx, -8, -32, 16, 64, 3, "#78350F", "#451A03", 1.2);
    // Round stainless steel bezel
    circ(ctx, 0, 0, 17, grad(ctx, -17, -17, 17, 17, C.white, C.s300), C.s500, 1.4);
    circ(ctx, 0, 0, 13.5, C.ink, C.gold, 1); // sapphire dial
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      line(ctx, Math.cos(a) * 10, Math.sin(a) * 10, Math.cos(a) * 12.5, Math.sin(a) * 12.5, C.goldHi, 1);
    }
    line(ctx, 0, 0, 0, -7, C.goldHi, 1.5); line(ctx, 0, 0, 5, 0, C.goldHi, 1.2); // watch hands
    circ(ctx, 0, 0, 1.5, C.red, null);
    ctx.restore();
  }

  function drawFishCrateShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 36, 4);
    box(ctx, -32, -4, 64, 30, 2, "#93C5FD", "#3B82F6", 1.2);
    // Fish inside crate
    poly(ctx, [[-22, -8], [0, -14], [18, -8], [26, -14], [26, -2], [18, -8]], "#60A5FA", "#1D4ED8", 1.2);
    circ(ctx, -16, -9, 1.4, C.ink, null);
    // Ice chips
    sparkle(ctx, -6, -8, 2.5, C.white); sparkle(ctx, 10, -6, 2, C.white);
    ctx.restore();
  }

  function drawRawMaterialShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 38, 4);
    // Architectural polished granite/marble slab
    poly(ctx, [[-36, 8], [0, -12], [36, 8], [0, 28]], grad(ctx, 0, -12, 0, 28, "#E2E8F0", "#94A3B8"), C.s600, 1.3);
    poly(ctx, [[-36, 8], [0, 28], [0, 32], [-36, 12]], C.s600, null);
    poly(ctx, [[0, 28], [36, 8], [36, 12], [0, 32]], C.s700, null);
    line(ctx, -18, 6, 8, -4, "rgba(255,255,255,0.6)", 1.4); // polish reflection
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 5: DOCUMENTS & TAX FORMS (Expanded)
     ========================================================================== */

  function drawInvoiceBillShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 62, h = 68, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 3, grad(ctx, x, y, x + w, y + h, C.white, C.paper), null); noShadow(ctx);
    box(ctx, x, y, w, h, 3, null, C.s300, 1.3);
    // Tax Invoice Header
    ctx.fillStyle = t.m; ctx.fillRect(x, y, w, 11);
    ctx.fillStyle = C.white; ctx.font = "800 6.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("TAX INVOICE", 0, y + 5.5);
    // Itemized table grid lines
    line(ctx, x + 6, y + 20, x + w - 6, y + 20, C.s400, 1.2);
    for (let i = 0; i < 4; i++) {
      const ly = y + 28 + i * 7;
      line(ctx, x + 6, ly, x + w - 24, ly, C.s300, 1);
      line(ctx, x + w - 18, ly, x + w - 6, ly, C.s400, 1.2);
    }
    // Subtotal & GSTIN box
    box(ctx, x + w - 26, y + h - 14, 20, 8, 1, t.soft, t.m, 1);
    ctx.restore();
  }

  function drawPromissoryNoteShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    const w = 78, h = 46, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 3, grad(ctx, x, y, x + w, y + h, C.paper, C.paperLo), null); noShadow(ctx);
    box(ctx, x, y, w, h, 3, null, "#B45309", 1.3);
    // Intaglio ornamental border
    rr(ctx, x + 3, y + 3, w - 6, h - 6, 2); ctx.strokeStyle = "rgba(180,83,9,0.35)"; ctx.lineWidth = 1; ctx.stroke();
    // Revenue stamp in top-right corner
    box(ctx, x + w - 16, y + 6, 10, 12, 1, C.red, C.redLo, 1);
    // "ON DEMAND I PROMISE TO PAY" text lines
    line(ctx, x + 8, y + 14, x + 34, y + 14, "#92400E", 1.8);
    for (let i = 0; i < 3; i++) line(ctx, x + 8, y + 22 + i * 5, x + w - 22, y + 22 + i * 5, C.s400, 1);
    // Signature
    ctx.strokeStyle = "#1D4ED8"; ctx.lineWidth = 1.2; ctx.beginPath();
    ctx.moveTo(x + w - 30, y + 38); ctx.bezierCurveTo(x + w - 24, y + 30, x + w - 18, y + 42, x + w - 8, y + 36); ctx.stroke();
    ctx.restore();
  }

  function drawBillOfLadingShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 62, h = 68, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 3, C.white, C.s300, 1.3); noShadow(ctx);
    ctx.fillStyle = C.sky; ctx.fillRect(x, y, w, 10);
    ctx.fillStyle = C.white; ctx.font = "800 6.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("BILL OF LADING", 0, y + 5);
    // Anchor maritime glyph
    circ(ctx, x + 10, y + 20, 3.5, null, C.sky, 1.2);
    for (let i = 0; i < 5; i++) line(ctx, x + 18, y + 20 + i * 6.5, x + w - 8, y + 20 + i * 6.5, C.s300, 1.1);
    // Port stamp
    circ(ctx, x + w - 16, y + h - 16, 8, null, C.sky, 1.3);
    ctx.restore();
  }

  function drawLetterOfCreditShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 66, h = 58, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 4, grad(ctx, x, y, x + w, y + h, C.white, C.paper), null); noShadow(ctx);
    box(ctx, x, y, w, h, 4, null, C.emerald, 1.3);
    ctx.fillStyle = C.emerald; ctx.fillRect(x, y, w, 9);
    ctx.fillStyle = C.white; ctx.font = "800 6px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("IRREVOCABLE L/C", 0, y + 4.5);
    for (let i = 0; i < 4; i++) line(ctx, x + 8, y + 18 + i * 6, x + w - 8, y + 18 + i * 6, C.s300, 1.1);
    // Golden Bank Guarantee Seal
    circ(ctx, x + w - 16, y + h - 14, 7.5, C.goldHi, C.goldLo, 1.2);
    ctx.restore();
  }

  function drawShareCertificateShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    const w = 82, h = 52, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 3, grad(ctx, x, y, x + w, y + h, C.white, C.paperLo), null); noShadow(ctx);
    box(ctx, x, y, w, h, 3, null, "#7C3AED", 1.4);
    rr(ctx, x + 3, y + 3, w - 6, h - 6, 2); ctx.strokeStyle = "rgba(124,58,237,0.3)"; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = "#7C3AED"; ctx.font = "800 6.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("SHARE CERTIFICATE", 0, y + 10);
    for (let i = 0; i < 3; i++) line(ctx, x + 10, y + 20 + i * 6, x + w - 10, y + 20 + i * 6, C.s300, 1.1);
    // Gold ribbon seal
    circ(ctx, x + 16, y + h - 12, 6.5, C.goldHi, C.goldLo, 1.2);
    poly(ctx, [[x + 13, y + h - 6], [x + 10, y + h], [x + 16, y + h - 3], [x + 22, y + h], [x + 19, y + h - 6]], C.gold, null);
    ctx.restore();
  }

  function drawPassbookShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    box(ctx, -34, -22, 68, 44, 3, grad(ctx, -34, -22, 34, 22, "#1E3A8A", "#172554"), null);
    noShadow(ctx);
    box(ctx, -34, -22, 68, 44, 3, null, C.s800, 1.3);
    // Golden bank emblem & title
    circ(ctx, 0, -8, 6.5, C.gold, C.goldLo, 1.1);
    ctx.fillStyle = C.goldHi; ctx.font = "800 6px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.fillText("BANK PASSBOOK", 0, 8);
    // Magnetic black data strip on back
    ctx.fillStyle = C.ink; ctx.fillRect(-34, 14, 68, 5);
    ctx.restore();
  }

  function drawSummonsNoticeShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    const w = 62, h = 68, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 3, C.white, C.s300, 1.3); noShadow(ctx);
    // Urgent Notice Header banner
    ctx.fillStyle = C.red; ctx.fillRect(x, y, w, 11);
    ctx.fillStyle = C.white; ctx.font = "800 6px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("STATUTORY SUMMONS", 0, y + 5.5);
    for (let i = 0; i < 5; i++) line(ctx, x + 8, y + 20 + i * 6.5, x + w - 8, y + 20 + i * 6.5, C.s400, 1.1);
    // Red Court Seal
    circ(ctx, x + w - 16, y + h - 14, 7.5, "rgba(220,38,38,0.15)", C.red, 1.3);
    ctx.restore();
  }

  function drawPanCardShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    const w = 84, h = 52, x = -w / 2, y = -h / 2;
    lift(ctx); box(ctx, x, y, w, h, 4, grad(ctx, x, y, x + w, y + h, "#E0F2FE", "#BAE6FD"), null); noShadow(ctx);
    box(ctx, x, y, w, h, 4, null, "#0284C7", 1.4);
    // Header
    ctx.fillStyle = "#0369A1"; ctx.font = "800 5px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "left"; ctx.fillText("INCOME TAX DEPARTMENT", x + 6, y + 8);
    ctx.fillText("GOVT. OF INDIA", x + 6, y + 14);
    // Photo box
    box(ctx, x + 6, y + 18, 18, 22, 1, C.s300, C.s500, 0.8);
    // Alphanumeric PAN Box
    box(ctx, x + 30, y + 26, 48, 8, 1, C.white, C.skyLo, 0.9);
    ctx.fillStyle = C.ink; ctx.font = "800 5.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.fillText("ABCDE1234F", x + 54, y + 31);
    // Hologram strip
    box(ctx, x + w - 14, y + 6, 8, 8, 1, C.goldHi, C.goldLo, 0.8);
    ctx.restore();
  }

  function drawAssessmentStackShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 38, 4);
    // 3 tiered folders with colored tabs
    [[-16, 22, "#3B82F6"], [-8, 11, "#10B981"], [0, 0, t.m]].forEach(([oy, y, col]) => {
      box(ctx, -32, y - 10, 64, 20, 2, C.white, col, 1.3);
      box(ctx, 16, y - 14, 14, 5, [2, 2, 0, 0], col, null);
    });
    ctx.restore();
  }

  function drawSearchMagnifierShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 24, 3.5);
    // Magnifying lens inspecting document
    circ(ctx, -4, -6, 17, "rgba(186,230,253,0.35)", C.gold, 2.5);
    circ(ctx, -4, -6, 13, null, "rgba(255,255,255,0.6)", 1.2);
    line(ctx, 8, 6, 26, 24, "#78350F", 4); // ebony handle
    sparkle(ctx, -8, -12, 3, C.white);
    ctx.restore();
  }

  function drawSeizedBoxShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 34, 4);
    box(ctx, -26, -10, 52, 36, 2, "#D97706", "#92400E", 1.3);
    // Government yellow tape & red wax seal
    line(ctx, -26, 8, 26, 8, C.goldHi, 4);
    circ(ctx, 0, 8, 8, C.red, C.redLo, 1.2);
    ctx.restore();
  }

  function drawExemptShieldShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 24, 3.5);
    const sh = new Path2D("M0 -32 L26 -23 L26 2 Q26 22 0 34 Q-26 22 -26 2 L-26 -23 Z");
    lift(ctx); ctx.fillStyle = grad(ctx, -26, -32, 26, 34, C.emeraldHi, C.emeraldLo); ctx.fill(sh); noShadow(ctx);
    ctx.strokeStyle = "#047857"; ctx.lineWidth = 1.4; ctx.stroke(sh);
    ctx.strokeStyle = C.white; ctx.lineWidth = 3.5; ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.beginPath(); ctx.moveTo(-8, 2); ctx.lineTo(-2, 8); ctx.lineTo(10, -6); ctx.stroke();
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 6: MONEY, FINANCE & BANKING (Expanded)
     ========================================================================== */

  function drawWalletShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 32, 4);
    // Currency notes peeking out
    box(ctx, -20, -16, 40, 12, 1, "#BBF7D0", "#15803D", 1);
    // Bifold Leather Wallet
    box(ctx, -26, -6, 52, 32, 4, grad(ctx, 0, -6, 0, 26, "#78350F", "#451A03"), "#291305", 1.3);
    // Stitched perimeter & brass snap closure
    rr(ctx, -24, -4, 48, 28, 3); ctx.strokeStyle = "rgba(255,255,255,0.25)"; ctx.lineWidth = 1; ctx.setLineDash([2, 2]); ctx.stroke(); ctx.setLineDash([]);
    box(ctx, 16, 6, 8, 8, 2, C.goldHi, C.goldLo, 1);
    ctx.restore();
  }

  function drawLedgerBookShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 36, 4);
    // Hardbound accounting daybook
    box(ctx, -28, -24, 56, 50, 3, grad(ctx, -28, 0, 28, 0, "#065F46", "#022C22"), "#022C22", 1.4);
    box(ctx, -28, -24, 8, 50, [3, 0, 0, 3], C.gold, C.goldLo, 1); // gold gilded spine
    // Ribbon bookmark
    poly(ctx, [[-4, 26], [4, 26], [4, 34], [0, 31], [-4, 34]], C.red, null);
    ctx.restore();
  }

  function drawPercentTagShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    box(ctx, -22, -22, 44, 44, 8, grad(ctx, -22, -22, 22, 22, "#A855F7", "#7C3AED"), null);
    noShadow(ctx);
    box(ctx, -22, -22, 44, 44, 8, null, "#581C87", 1.4);
    circ(ctx, 0, -14, 3, C.white, C.s500, 1); // brass eyelet
    ctx.fillStyle = C.white; ctx.font = "800 18px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("%", 0, 4);
    ctx.restore();
  }

  function drawFinancialChartShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 38, 4);
    // Coordinate axes
    line(ctx, -32, 22, 32, 22, C.s400, 1.5); line(ctx, -32, 22, -32, -22, C.s400, 1.5);
    // Ascending bars
    [[-24, 12, 10], [-8, 20, 10], [8, 30, 10], [24, 40, 10]].forEach(([x, h, w]) => {
      box(ctx, x - w / 2, 22 - h, w, h, [2, 2, 0, 0], grad(ctx, 0, 22 - h, 0, 22, t.hi, t.lo), t.line, 1.1);
    });
    // Upward trend arrow
    ctx.strokeStyle = C.emerald; ctx.lineWidth = 2.5; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(-24, 10); ctx.lineTo(-8, 2); ctx.lineTo(8, -8); ctx.lineTo(24, -18); ctx.stroke();
    poly(ctx, [[24, -22], [28, -14], [20, -16]], C.emerald, null);
    ctx.restore();
  }

  function drawInsuranceUmbrellaShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 28, 3.5);
    // Canopy
    ctx.beginPath(); ctx.arc(0, -6, 28, Math.PI, 0); ctx.closePath();
    ctx.fillStyle = grad(ctx, 0, -34, 0, -6, t.hi, t.lo); ctx.fill();
    ctx.strokeStyle = t.line; ctx.lineWidth = 1.3; ctx.stroke();
    // Metal shaft & curved J-handle
    line(ctx, 0, -6, 0, 22, C.s600, 2.5);
    ctx.beginPath(); ctx.arc(5, 22, 5, Math.PI, 0, true); ctx.strokeStyle = C.s600; ctx.lineWidth = 2.5; ctx.stroke();
    circ(ctx, 0, -34, 2, C.gold, null);
    ctx.restore();
  }

  function drawLoanDepositShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    drawCourtShape(ctx, accentTheme);
    // Currency exchange badge overlay
    circ(ctx, 22, 16, 9, C.goldHi, C.goldLo, 1.2);
    ctx.fillStyle = C.goldLo; ctx.font = "800 10px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("₹", 22, 16.5);
  }

  function drawAtmShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 28, 4);
    box(ctx, -22, -30, 44, 58, 4, grad(ctx, 0, -30, 0, 28, C.s700, C.s900 || C.ink), C.s500, 1.3);
    // Screen & keypad
    box(ctx, -16, -24, 32, 18, 2, C.skyLo, C.sky, 1);
    box(ctx, -14, -2, 28, 10, 1, C.s300, C.s600, 1);
    // Cash dispenser slot with rupee note
    box(ctx, -14, 14, 28, 4, 1, C.ink, null);
    box(ctx, -10, 12, 20, 5, 1, C.greenHi, C.emerald, 0.8);
    ctx.restore();
  }

  function drawTellerCounterShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 44, 4.5);
    // Glass barrier & counter desk
    box(ctx, -38, 2, 76, 26, 2, "#78350F", "#451A03", 1.3);
    box(ctx, -34, -26, 68, 28, 2, "rgba(186,230,253,0.45)", C.s400, 1.2);
    // Speaker grille & pass-through tray
    circ(ctx, 0, -12, 5, C.s200, C.s500, 1);
    box(ctx, -12, 2, 24, 6, 1, C.s100, C.s600, 1);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 7: LAW, GOVERNMENT & CRIMES (Expanded)
     ========================================================================== */

  function drawStatuteBookShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 32, 4);
    box(ctx, -26, -26, 52, 52, 3, grad(ctx, 0, -26, 0, 26, "#881337", "#4C0519"), "#4C0519", 1.4);
    box(ctx, -26, -26, 8, 52, [3, 0, 0, 3], C.gold, C.goldLo, 1);
    // Scales of justice emblem on book cover
    circ(ctx, 2, -2, 7, null, C.goldHi, 1.2);
    line(ctx, -3, -2, 7, -2, C.goldHi, 1.2); line(ctx, 2, -7, 2, 3, C.goldHi, 1.2);
    ctx.restore();
  }

  function drawOfficialSealShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    circ(ctx, 0, 0, 22, C.red, C.redLo, 1.4);
    noShadow(ctx);
    circ(ctx, 0, 0, 17, null, "rgba(255,255,255,0.75)", 1.2);
    // Serrated edge points & star
    sparkle(ctx, 0, 0, 6, C.goldHi);
    ctx.restore();
  }

  function drawFlagPoleShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 24, 3.5);
    // Silver pole & gold finial
    line(ctx, -16, -34, -16, 28, C.s500, 2.5);
    circ(ctx, -16, -35, 2.5, C.goldHi, C.goldLo, 1);
    // Flowing flag
    poly(ctx, [[-16, -32], [22, -26], [18, -12], [-16, -18]], grad(ctx, -16, -32, 22, -12, C.red, C.gold), C.redLo, 1.2);
    ctx.restore();
  }

  function drawHandcuffsShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 34, 3.5);
    // Twin steel handcuffs with connecting chain
    circ(ctx, -16, 0, 13, null, C.s400, 3); circ(ctx, 16, 0, 13, null, C.s400, 3);
    line(ctx, -3, 0, 3, 0, C.s600, 3);
    circ(ctx, -16, -10, 2, C.s600, null); circ(ctx, 16, -10, 2, C.s600, null); // keyhole
    ctx.restore();
  }

  function drawCustomsScannerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 44, 4);
    // X-Ray inspection portal frame
    box(ctx, -34, -28, 68, 54, 4, grad(ctx, 0, -28, 0, 26, C.s700, C.s900 || C.ink), C.s500, 1.4);
    box(ctx, -22, -16, 44, 42, 2, C.s100, null);
    // Conveyor belt & luggage
    box(ctx, -42, 14, 84, 8, 2, C.s800, null);
    box(ctx, -8, 2, 16, 12, 2, "#F59E0B", "#B45309", 1);
    // Laser scanning beam
    line(ctx, -20, -10, 20, -10, C.red, 2);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 8: CORPORATE GOVERNANCE (Expanded)
     ========================================================================== */

  function drawBallotBoxShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 34, 4);
    box(ctx, -24, -14, 48, 40, 3, grad(ctx, 0, -14, 0, 26, t.hi, t.lo), t.line, 1.3);
    // Top slot & entering vote ballot paper
    box(ctx, -12, -15, 24, 3, 1, C.ink, null);
    box(ctx, -8, -26, 16, 16, 1, C.white, C.s400, 1);
    line(ctx, -5, -20, 5, -20, t.m, 1.2);
    ctx.restore();
  }

  function drawOrgChartShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 38, 4);
    // Top executive box
    box(ctx, -14, -24, 28, 12, 2, t.m, t.line, 1.1);
    line(ctx, 0, -12, 0, -2, C.s500, 1.4);
    line(ctx, -24, -2, 24, -2, C.s500, 1.4);
    // Bottom 3 branch boxes
    [-24, 0, 24].forEach(x => {
      line(ctx, x, -2, x, 6, C.s500, 1.4);
      box(ctx, x - 10, 6, 20, 10, 2, C.white, t.line, 1.1);
    });
    ctx.restore();
  }

  function drawSharePieShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 32, 4);
    // 3D Pie Chart slices
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, 22, -0.6, Math.PI * 1.2); ctx.closePath();
    ctx.fillStyle = t.m; ctx.fill(); ctx.strokeStyle = t.line; ctx.stroke();
    // Highlighted separated slice
    ctx.save(); ctx.translate(4, -4);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, 22, Math.PI * 1.2, -0.6); ctx.closePath();
    ctx.fillStyle = C.goldHi; ctx.fill(); ctx.strokeStyle = C.goldLo; ctx.stroke();
    ctx.restore();
    ctx.restore();
  }

  function drawMergerShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 38, 4);
    // Two converging curved arrows merging into one
    ctx.strokeStyle = t.m; ctx.lineWidth = 4; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(-32, -18); ctx.quadraticCurveTo(-10, 0, 18, 0); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-32, 18); ctx.quadraticCurveTo(-10, 0, 18, 0); ctx.stroke();
    poly(ctx, [[18, -6], [28, 0], [18, 6]], t.m, null);
    circ(ctx, -32, -18, 4, C.sky, null); circ(ctx, -32, 18, 4, C.emerald, null);
    ctx.restore();
  }

  function drawOfficeDeskShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 42, 4.5);
    box(ctx, -36, 6, 72, 20, 2, "#64748B", "#334155", 1.2);
    // Computer screen on desk
    box(ctx, -14, -14, 28, 18, 2, C.s800, C.s600, 1.2);
    box(ctx, -12, -12, 24, 14, 1, C.glassHi, null);
    line(ctx, 0, 4, 0, 8, C.s700, 2);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 9: HAZARDS & FORCE MAJEURE (Expanded)
     ========================================================================== */

  function drawFireFlameShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 24, 3.5);
    // Outer flame (crimson red)
    const flame = new Path2D("M0 -34 Q14 -18 18 -2 Q24 16 0 26 Q-24 16 -18 -2 Q-14 -18 0 -34 Z");
    ctx.fillStyle = grad(ctx, 0, -34, 0, 26, "#EF4444", "#DC2626"); ctx.fill(flame);
    // Inner flame (golden yellow core)
    const core = new Path2D("M0 -18 Q8 -8 10 2 Q12 16 0 22 Q-12 16 -10 2 Q-8 -8 0 -18 Z");
    ctx.fillStyle = grad(ctx, 0, -18, 0, 22, "#FEF08A", "#F59E0B"); ctx.fill(core);
    sparkle(ctx, -14, -22, 2.5, C.goldHi); sparkle(ctx, 16, -18, 2, C.goldHi);
    ctx.restore();
  }

  function drawFloodWaterShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 38, 4);
    // Cascading flood water deluge waves
    for (let i = 0; i < 3; i++) {
      const y = -10 + i * 12;
      ctx.beginPath();
      ctx.moveTo(-38, y);
      ctx.bezierCurveTo(-20, y - 10, -10, y + 10, 0, y);
      ctx.bezierCurveTo(10, y - 10, 20, y + 10, 38, y);
      ctx.strokeStyle = i === 1 ? C.skyHi : C.sky; ctx.lineWidth = 3.5; ctx.lineCap = "round"; ctx.stroke();
    }
    ctx.restore();
  }

  function drawEarthquakeShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 42, 4);
    // Shifted tectonic ground fracture
    poly(ctx, [[-40, 10], [-18, 10], [-8, -12], [4, 6], [16, -16], [40, 10], [40, 24], [-40, 24]], "#78350F", "#451A03", 1.3);
    line(ctx, -18, 10, -8, -12, C.red, 2); line(ctx, -8, -12, 4, 6, C.red, 2); line(ctx, 4, 6, 16, -16, C.red, 2);
    ctx.restore();
  }

  function drawStormShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -10);
    ground(ctx, 0, 32, 34, 3.5);
    // Dark cumulus cloud
    circ(ctx, -14, -8, 14, C.s600, C.s800, 1.2); circ(ctx, 10, -6, 16, C.s600, C.s800, 1.2); circ(ctx, 0, -18, 18, C.s500, C.s700, 1.2);
    box(ctx, -18, -4, 36, 14, 0, C.s600, null);
    // Jagged electric gold lightning bolt
    poly(ctx, [[2, 2], [-8, 16], [-1, 16], [-6, 30], [8, 12], [1, 12]], C.goldHi, C.goldLo, 1.1);
    ctx.restore();
  }

  function drawExplosionShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 30, 4);
    // Multi-pointed blast starburst
    ctx.beginPath();
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      const r = i % 2 === 0 ? 28 : 14;
      i === 0 ? ctx.moveTo(Math.cos(a) * r, Math.sin(a) * r) : ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r);
    }
    ctx.closePath();
    ctx.fillStyle = grad(ctx, 0, -28, 0, 28, "#EF4444", "#F59E0B"); ctx.fill();
    ctx.strokeStyle = "#B91C1C"; ctx.lineWidth = 1.3; ctx.stroke();
    circ(ctx, 0, 0, 8, "#FEF08A", null);
    ctx.restore();
  }

  function drawToxicBarrelShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 4);
    // Ribbed chemical drum
    box(ctx, -18, -22, 36, 46, 5, grad(ctx, -18, 0, 18, 0, "#15803D", "#14532D"), "#052E16", 1.3);
    for (let y = -10; y <= 14; y += 12) line(ctx, -18, y, 18, y, C.ink, 1.5);
    // Biohazard / radioactive warning emblem
    circ(ctx, 0, 2, 7, C.goldHi, C.goldLo, 1);
    circ(ctx, 0, 2, 2.5, C.ink, null);
    ctx.restore();
  }

  function drawSmokeShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 34, 4);
    [[ -14, 12, 14 ], [ 10, 8, 16 ], [ -4, -4, 18 ], [ 12, -18, 12 ]].forEach(([cx, cy, r]) => {
      circ(ctx, cx, cy, r, "rgba(100, 116, 139, 0.45)", "rgba(71, 85, 105, 0.6)", 1.1);
    });
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 10: TECH, CYBER & DIGITAL (Expanded)
     ========================================================================== */

  function drawPhishingShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 3.5);
    // Suspended fishing hook snagging an envelope
    line(ctx, 0, -32, 0, -10, C.s400, 1.2);
    ctx.beginPath(); ctx.arc(-6, 2, 12, -0.4, Math.PI * 0.85); ctx.strokeStyle = C.s600; ctx.lineWidth = 2.5; ctx.stroke();
    // Snagged credentials envelope
    ctx.save(); ctx.translate(6, 10); ctx.rotate(0.2);
    box(ctx, -12, -8, 24, 16, 2, C.white, C.red, 1.2);
    line(ctx, -12, -8, 0, 2, C.red, 1); line(ctx, 12, -8, 0, 2, C.red, 1);
    ctx.restore();
    ctx.restore();
  }

  function drawBreachShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 3.5);
    // Broken Padlock
    box(ctx, -16, -2, 32, 24, 4, C.red, C.redLo, 1.3);
    // Severed broken shackle
    ctx.strokeStyle = C.s400; ctx.lineWidth = 3.5; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(-10, -2); ctx.lineTo(-10, -18); ctx.arc(0, -18, 10, Math.PI, -0.2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(10, -2); ctx.lineTo(10, -8); ctx.stroke();
    ctx.restore();
  }

  function drawRansomwareShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 32, 4);
    box(ctx, -26, -20, 52, 36, 3, C.s800, C.s500, 1.3);
    box(ctx, -22, -16, 44, 28, 2, C.redLo, null);
    // Skull / Lock alert glyph
    ctx.fillStyle = C.white; ctx.font = "800 12px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("🔒", 0, -2);
    line(ctx, 0, 16, 0, 24, C.s700, 3); // monitor stand
    box(ctx, -12, 24, 24, 3, 1, C.s600, null);
    ctx.restore();
  }

  function drawEmailShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    box(ctx, -28, -18, 56, 36, 3, grad(ctx, 0, -18, 0, 18, C.white, C.paper), null);
    noShadow(ctx);
    box(ctx, -28, -18, 56, 36, 3, null, t.m, 1.3);
    // Envelope flap folds
    poly(ctx, [[-28, -18], [0, 2], [28, -18]], null, t.m, 1.2);
    line(ctx, -28, 18, -8, 0, C.s300, 1.1); line(ctx, 28, 18, 8, 0, C.s300, 1.1);
    ctx.restore();
  }

  function drawUsbShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 20, 3.5);
    box(ctx, -10, -10, 20, 36, 3, grad(ctx, -10, 0, 10, 0, C.s600, C.s800), C.s500, 1.2);
    // USB-A metal connector plug
    box(ctx, -7, -26, 14, 16, 1, C.s200, C.s400, 1.1);
    box(ctx, -4, -22, 3, 4, 0.5, C.ink, null); box(ctx, 1, -22, 3, 4, 0.5, C.ink, null);
    ctx.restore();
  }

  function drawCryptoShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 26, 4);
    circ(ctx, 0, 0, 22, grad(ctx, -22, -22, 22, 22, "#FDE047", "#CA8A04"), "#854D0E", 1.4);
    circ(ctx, 0, 0, 18, null, "rgba(255,255,255,0.6)", 1);
    ctx.fillStyle = "#713F12"; ctx.font = "800 18px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("₿", 0, 1);
    ctx.restore();
  }

  function drawQrCodeShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    box(ctx, -24, -24, 48, 48, 4, C.white, null); noShadow(ctx);
    box(ctx, -24, -24, 48, 48, 4, null, C.s400, 1.3);
    // 3 corner alignment target boxes
    function qrCorner(cx, cy) {
      box(ctx, cx - 6, cy - 6, 12, 12, 1, C.ink, null);
      box(ctx, cx - 4, cy - 4, 8, 8, 0.5, C.white, null);
      box(ctx, cx - 2, cy - 2, 4, 4, 0.5, C.ink, null);
    }
    qrCorner(-14, -14); qrCorner(14, -14); qrCorner(-14, 14);
    // Random binary data pips
    ctx.fillStyle = C.ink;
    for (let i = 0; i < 5; i++) ctx.fillRect(2 + i * 3, -4 + i * 3, 2.5, 2.5);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 11: TIME, LIMITATIONS & DEADLINES (Expanded)
     ========================================================================== */

  function drawClockShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 4);
    circ(ctx, 0, 0, 22, grad(ctx, -22, -22, 22, 22, C.white, C.s100), t.m, 1.5);
    // Red 180-day countdown limitation sector
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, 19, -Math.PI / 2, Math.PI / 3); ctx.closePath();
    ctx.fillStyle = "rgba(239, 68, 68, 0.22)"; ctx.fill();
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      line(ctx, Math.cos(a) * 16, Math.sin(a) * 16, Math.cos(a) * 19, Math.sin(a) * 19, C.s400, 1.2);
    }
    line(ctx, 0, 0, 0, -12, C.ink, 2); line(ctx, 0, 0, 8, 4, C.red, 1.5); // clock hands
    circ(ctx, 0, 0, 2, C.red, null);
    ctx.restore();
  }

  function drawCalendarShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    lift(ctx);
    box(ctx, -24, -24, 48, 48, 4, C.white, null); noShadow(ctx);
    box(ctx, -24, -24, 48, 48, 4, null, C.s300, 1.3);
    // Red Sunday header bar
    box(ctx, -24, -24, 48, 14, [4, 4, 0, 0], C.red, C.redLo, 1.1);
    ctx.fillStyle = C.white; ctx.font = "800 6.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("AY 2024-25", 0, -17);
    // Date number
    ctx.fillStyle = C.ink; ctx.font = "800 20px 'Plus Jakarta Sans', sans-serif";
    ctx.fillText("31", 0, 7);
    ctx.restore();
  }

  function drawHourglassShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 22, 3.5);
    // Top & bottom brass plates
    box(ctx, -18, -26, 36, 4, 1.5, C.goldHi, C.goldLo, 1.1);
    box(ctx, -18, 22, 36, 4, 1.5, C.goldHi, C.goldLo, 1.1);
    // Glass bulbs with sand waist
    poly(ctx, [[-14, -22], [14, -22], [2, 0], [14, 22], [-14, 22], [-2, 0]], "rgba(186,230,253,0.35)", C.s400, 1.2);
    // Falling golden sand
    poly(ctx, [[-10, 22], [10, 22], [0, 8]], C.gold, null);
    line(ctx, 0, -4, 0, 12, C.goldHi, 1.2);
    ctx.restore();
  }

  function drawDeadlineShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 30, 20, 3);
    // Milestone rock base
    box(ctx, -14, 18, 28, 10, 2, C.s300, C.s500, 1.2);
    line(ctx, 0, -32, 0, 18, C.s600, 2.5);
    // Checkered finish / deadline flag
    poly(ctx, [[0, -30], [24, -22], [0, -14]], C.red, C.redLo, 1.2);
    ctx.restore();
  }

  /* ==========================================================================
     CATEGORY 15, 16, 17: TOOLS, NATURE, CONNECTORS (Expanded)
     ========================================================================== */

  function drawTwoKeysShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 26, 3.5);
    // Dual brass keys on ring
    circ(ctx, 0, -8, 8, null, C.gold, 2.5);
    [[-0.3, -12], [0.3, 8]].forEach(([rot, ox]) => {
      ctx.save(); ctx.rotate(rot);
      line(ctx, 0, -2, 0, 22, C.goldHi, 2.8);
      box(ctx, 0, 14, 6, 3, 0.5, C.goldHi, null); box(ctx, 0, 19, 4, 3, 0.5, C.goldHi, null);
      ctx.restore();
    });
    ctx.restore();
  }

  function drawKeyShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 24, 3.5);
    circ(ctx, -14, 0, 9, null, C.gold, 2.8);
    line(ctx, -5, 0, 24, 0, C.goldHi, 3.5);
    box(ctx, 14, 0, 4, 8, 1, C.goldHi, null); box(ctx, 20, 0, 4, 6, 1, C.goldHi, null);
    ctx.restore();
  }

  function drawWrenchShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 24, 3.5);
    ctx.save(); ctx.rotate(-0.6);
    box(ctx, -4, -14, 8, 38, 2, C.s300, C.s500, 1.2);
    // Open jaws
    circ(ctx, 0, -16, 9, C.s300, C.s500, 1.2);
    box(ctx, -4, -24, 8, 10, 0, C.s50, null);
    ctx.restore();
    ctx.restore();
  }

  function drawMagnifierShape(ctx, accentTheme = {}) {
    drawSearchMagnifierShape(ctx, accentTheme);
  }

  function drawScissorsShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 24, 3.5);
    // Twin blades pivoted
    line(ctx, -18, 18, 16, -16, C.s400, 3);
    line(ctx, 18, 18, -16, -16, C.s400, 3);
    circ(ctx, -16, 18, 5, null, C.red, 2); circ(ctx, 18, 18, 5, null, C.red, 2);
    circ(ctx, 0, 0, 2, C.gold, null);
    ctx.restore();
  }

  function drawPenShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 24, 3.5);
    ctx.save(); ctx.rotate(-0.5);
    box(ctx, -4, -28, 8, 44, 2, "#1E3A8A", "#172554", 1.2);
    poly(ctx, [[-4, 16], [4, 16], [0, 26]], C.goldHi, C.goldLo, 1.1); // gold nib
    line(ctx, -4, -12, 4, -12, C.gold, 1.5); // gold band
    ctx.restore();
    ctx.restore();
  }

  function drawBriefcaseShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 32, 4);
    box(ctx, -26, -10, 52, 34, 4, grad(ctx, 0, -10, 0, 24, "#78350F", "#451A03"), "#291305", 1.3);
    // Handle & brass clasps
    ctx.beginPath(); ctx.arc(0, -10, 7, Math.PI, 0); ctx.strokeStyle = "#451A03"; ctx.lineWidth = 2.5; ctx.stroke();
    box(ctx, -14, -2, 6, 5, 1, C.goldHi, C.goldLo, 1); box(ctx, 8, -2, 6, 5, 1, C.goldHi, C.goldLo, 1);
    ctx.restore();
  }

  function drawTreeShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 30, 4);
    // Trunk
    poly(ctx, [[-5, 26], [-3, -4], [3, -4], [5, 26]], "#78350F", "#451A03", 1.2);
    // Lush tiered pine canopy
    poly(ctx, [[-26, 12], [0, -12], [26, 12]], grad(ctx, 0, -12, 0, 12, "#16A34A", "#15803D"), "#14532D", 1.2);
    poly(ctx, [[-20, -2], [0, -22], [20, -2]], grad(ctx, 0, -22, 0, -2, "#22C55E", "#16A34A"), "#14532D", 1.2);
    poly(ctx, [[-14, -14], [0, -32], [14, -14]], grad(ctx, 0, -32, 0, -14, "#4ADE80", "#22C55E"), "#15803D", 1.2);
    ctx.restore();
  }

  function drawCropShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 26, 3.5);
    // Harvested cereal sheaf tied in bundle
    poly(ctx, [[-14, 26], [-6, 0], [-18, -22], [18, -22], [6, 0], [14, 26]], grad(ctx, 0, -22, 0, 26, "#FDE047", "#D97706"), "#92400E", 1.3);
    box(ctx, -8, -2, 16, 4, 1, C.red, null); // red ribbon knot
    ctx.restore();
  }

  function drawCowShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 26, 38, 4.5);
    // Cattle body & head
    box(ctx, -26, -10, 44, 24, 6, C.white, C.s400, 1.3);
    // Black dairy patches
    circ(ctx, -14, -2, 7, C.ink, null); circ(ctx, 4, 4, 6, C.ink, null);
    // Legs
    [-20, -12, 8, 16].forEach(x => box(ctx, x, 14, 4, 12, 1, C.white, C.s500, 1));
    // Head & horns
    poly(ctx, [[18, -6], [32, -14], [34, 4], [18, 6]], C.white, C.s400, 1.2);
    line(ctx, 24, -12, 28, -20, C.gold, 2); // horn
    circ(ctx, 28, -4, 1.4, C.ink, null);
    ctx.restore();
  }

  function drawMineShape(ctx, accentTheme = {}) {
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 28, 40, 4);
    // Quarry rock cliff
    poly(ctx, [[-38, 26], [-28, -18], [0, -12], [24, -24], [38, 26]], "#64748B", "#334155", 1.3);
    // Crossed pickaxes
    ctx.strokeStyle = C.goldHi; ctx.lineWidth = 2.5;
    line(ctx, -14, 18, 14, -10, C.goldHi, 2.5);
    poly(ctx, [[6, -14], [18, -12], [14, -6]], C.s300, null);
    ctx.restore();
  }

  function drawConnectorShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    ground(ctx, 0, 24, 34, 3.5);
    // Dimensional glossy flow arrow
    ctx.strokeStyle = t.m; ctx.lineWidth = 5; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(-32, 0); ctx.lineTo(16, 0); ctx.stroke();
    poly(ctx, [[16, -10], [32, 0], [16, 10]], t.m, null);
    ctx.restore();
  }

  function drawSignboardShape(ctx, accentTheme = {}) {
    const t = T(accentTheme);
    ctx.save(); ctx.translate(0, -8);
    // Hanging chains
    line(ctx, -20, -32, -20, -14, C.s600, 1.5); line(ctx, 20, -32, 20, -14, C.s600, 1.5);
    // Wooden board
    box(ctx, -32, -14, 64, 28, 3, grad(ctx, 0, -14, 0, 14, "#78350F", "#451A03"), "#291305", 1.3);
    box(ctx, -26, -8, 52, 16, 1, "rgba(255,255,255,0.15)", null);
    ctx.restore();
  }

  /* ==========================================================================
     STATUS OVERLAY BADGE
     ========================================================================== */
  function drawOverlay(ctx, overlay) {
    if (!overlay) return;
    const col = overlay.color || C.red, tint = overlay.bg || "#FEE2E2", kind = overlay.type || "";
    ctx.save(); ctx.translate(24, -34);
    ctx.shadowColor = "rgba(15,23,42,0.22)"; ctx.shadowBlur = 7; ctx.shadowOffsetY = 2;
    circ(ctx, 0, 0, 12.5, C.white, null);
    noShadow(ctx);
    circ(ctx, 0, 0, 12.5, tint, col, 1.8);
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 2.2; ctx.lineCap = "round"; ctx.lineJoin = "round";
    const glyph = {
      check: () => { ctx.beginPath(); ctx.moveTo(-5, 0.5); ctx.lineTo(-1.5, 4); ctx.lineTo(5.5, -3.5); ctx.stroke(); },
      crossed: () => { ctx.beginPath(); ctx.moveTo(-4.5, -4.5); ctx.lineTo(4.5, 4.5); ctx.moveTo(4.5, -4.5); ctx.lineTo(-4.5, 4.5); ctx.stroke(); },
      warning: () => { ctx.beginPath(); ctx.moveTo(0, -5.5); ctx.lineTo(0.2, 1.5); ctx.stroke(); circ(ctx, 0, 5, 1.3, col, null); },
      damaged: () => { ctx.beginPath(); ctx.moveTo(-1, -6); ctx.lineTo(2, -1); ctx.lineTo(-2, 1); ctx.lineTo(1, 6); ctx.stroke(); },
      locked: () => { box(ctx, -4.5, -0.5, 9, 6.5, 1.5, col, null); ctx.beginPath(); ctx.arc(0, -1, 3.3, Math.PI, 0); ctx.stroke(); },
      clock: () => { ctx.beginPath(); ctx.arc(0, 0, 6, 0, Math.PI * 2); ctx.lineWidth = 1.6; ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, -3.2); ctx.lineTo(0, 0); ctx.lineTo(2.6, 1.6); ctx.stroke(); },
      rupee: () => { ctx.font = "800 12px 'JetBrains Mono', monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("\\u20B9", 0, 0.8); ctx.textBaseline = "alphabetic"; },
      percent: () => { circ(ctx, -3.2, -3.2, 1.9, null, col, 1.6); circ(ctx, 3.2, 3.2, 1.9, null, col, 1.6); ctx.beginPath(); ctx.moveTo(4.5, -5); ctx.lineTo(-4.5, 5); ctx.stroke(); },
      missing: () => { ctx.font = "800 13px 'Plus Jakarta Sans', sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("?", 0, 1); ctx.textBaseline = "alphabetic"; },
      question: () => glyph.missing(),
      flag: () => { ctx.beginPath(); ctx.moveTo(-3.5, 6); ctx.lineTo(-3.5, -6); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-3.5, -6); ctx.lineTo(5, -3.5); ctx.lineTo(-3.5, -0.5); ctx.closePath(); ctx.fill(); },
      stamped: () => { circ(ctx, 0, -4.2, 2.6, col, null); box(ctx, -1.3, -2, 2.6, 5, 0.6, col, null); box(ctx, -5.2, 3, 10.4, 2.8, 1, col, null); }
    };
    (glyph[kind] || glyph.warning)();
    ctx.restore();
  }

  


  // Direct Aliases for Category Archetypes
  function drawManShape(ctx, th) { drawPersonShape(ctx, "man", th); }
  function drawWomanShape(ctx, th) { drawPersonShape(ctx, "woman", th); }
  function drawAccountantShape(ctx, th) { drawPersonShape(ctx, "accountant", th); }
  function drawDoctorShape(ctx, th) { drawPersonShape(ctx, "doctor", th); }
  function drawJudgeShape(ctx, th) { drawPersonShape(ctx, "judge", th); }
  function drawExecutiveShape(ctx, th) { drawPersonShape(ctx, "executive", th); }
  function drawGoldShape(ctx, th) { drawGoldBullionShape(ctx, th); }
  function drawBoxShape(ctx, th) { drawGoodsBoxShape(ctx, th); }
  function drawFabricShape(ctx, th) { drawClothesShape(ctx, "fabric", th); }
  function drawCameraShape(ctx, th) { drawCameraCctvShape(ctx, th); }
  function drawChartShape(ctx, th) { drawFinancialChartShape(ctx, th); }
  function drawDelegateArrowShape(ctx, th) { drawConnectorShape(ctx, th); }
  function drawFireShape(ctx, th) { drawFireFlameShape(ctx, th); }
  function drawFishShape(ctx, th) { drawFishCrateShape(ctx, th); }
  function drawFlagShape(ctx, th) { drawFlagPoleShape(ctx, th); }
  function drawFloodShape(ctx, th) { drawFloodWaterShape(ctx, th); }
  function drawInvoiceShape(ctx, th) { drawInvoiceBillShape(ctx, th); }
  function drawLedgerShape(ctx, th) { drawLedgerBookShape(ctx, th); }
  function drawSackShape(ctx, th) { drawSackBaleShape(ctx, th); }
  function drawSummonsShape(ctx, th) { drawSummonsNoticeShape(ctx, th); }
  function drawUmbrellaShape(ctx, th) { drawInsuranceUmbrellaShape(ctx, th); }
  function drawVanShape(ctx, th) { drawCarShape(ctx, th); }
  function drawApartmentShape(ctx, th) { drawBuildingShape(ctx, "apartment", th); }

  /* ==========================================================================
     UNIVERSAL MASTER DISPATCHER: drawShape(ctx, shapeName, accentTheme)
     ========================================================================== */
  function drawShape(ctx, shapeName, accentTheme = {}) {
    if (!shapeName) return false;
    const entry = lookup(shapeName);
    const custom = entry && entry.custom ? entry.custom : String(shapeName).toLowerCase().replace(/[\s\-_]+/g, "");
    if (!custom) return false;

    // Direct role check
    if (custom === "man" || custom === "woman" || custom === "accountant" || custom === "doctor" || custom === "judge" || custom === "executive") {
      drawPersonShape(ctx, custom, accentTheme);
      return true;
    }

    const parts = custom.split("_");
    const camel = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join("");
    const candidates = [
      "draw" + camel + "Shape",
      "draw" + camel,
      "draw" + parts[0].charAt(0).toUpperCase() + parts[0].slice(1) + "Shape"
    ];
    for (const name of candidates) {
      if (window.SHAPE_CATALOG && typeof window.SHAPE_CATALOG[name] === "function") {
        window.SHAPE_CATALOG[name](ctx, accentTheme);
        return true;
      }
    }
    return false;
  }


  // Master Window Exports
  window.SHAPE_CATALOG = {
    CATEGORIES,
    REGISTRY,
    OVERLAYS,
    lookup,
    drawShape,
    drawAccountantShape,
    drawAircraftShape,
    drawApartmentShape,
    drawAssessmentStackShape,
    drawAtmShape,
    drawAutoRickshawShape,
    drawBallotBoxShape,
    drawBankShape,
    drawBillOfLadingShape,
    drawBoardroomShape,
    drawBoxShape,
    drawBreachShape,
    drawBriefcaseShape,
    drawBuildingShape,
    drawBusShape,
    drawCalculatorShape,
    drawCalendarShape,
    drawCameraCctvShape,
    drawCameraShape,
    drawCarShape,
    drawCargoContainerShape,
    drawCashBagShape,
    drawChartShape,
    drawChequeShape,
    drawChildShape,
    drawClockShape,
    drawClothesShape,
    drawConnectorShape,
    drawCourtShape,
    drawCowShape,
    drawCropShape,
    drawCrowdShape,
    drawCryptoShape,
    drawCustomsHouseShape,
    drawCustomsScannerShape,
    drawDeadlineShape,
    drawDelegateArrowShape,
    drawDoctorShape,
    drawDocumentShape,
    drawEarthquakeShape,
    drawElderlyShape,
    drawEmailShape,
    drawEngineerShape,
    drawExecutiveShape,
    drawExemptShieldShape,
    drawExplosionShape,
    drawFabricShape,
    drawFactoryShape,
    drawFarmlandShape,
    drawFinancialChartShape,
    drawFireFlameShape,
    drawFireShape,
    drawFishCrateShape,
    drawFishShape,
    drawFlagPoleShape,
    drawFlagShape,
    drawFloodShape,
    drawFloodWaterShape,
    drawGavelShape,
    drawGoldBullionShape,
    drawGoldShape,
    drawGoodsBoxShape,
    drawHandcuffsShape,
    drawHandshakeShape,
    drawHospitalShape,
    drawHotelShape,
    drawHourglassShape,
    drawHouseShape,
    drawInsuranceUmbrellaShape,
    drawInvoiceBillShape,
    drawInvoiceShape,
    drawJewelShape,
    drawJudgeShape,
    drawKeyShape,
    drawLaptopShape,
    drawLedgerBookShape,
    drawLedgerShape,
    drawLegalSymbolShape,
    drawLetterOfCreditShape,
    drawLoanDepositShape,
    drawMachineryShape,
    drawMagnifierShape,
    drawManShape,
    drawMergerShape,
    drawMineShape,
    drawMoneyShape,
    drawOfficeDeskShape,
    drawOfficeShape,
    drawOfficerShape,
    drawOfficialSealShape,
    drawOrgChartShape,
    drawOverlay,
    drawPanCardShape,
    drawPartnersShape,
    drawPassbookShape,
    drawPedestrianShape,
    drawPenShape,
    drawPercentTagShape,
    drawPersonShape,
    drawPhishingShape,
    drawPromissoryNoteShape,
    drawQrCodeShape,
    drawRansomwareShape,
    drawRawMaterialShape,
    drawSackBaleShape,
    drawSackShape,
    drawSafeShape,
    drawScaleShape,
    drawSchoolShape,
    drawScissorsShape,
    drawSearchMagnifierShape,
    drawSeizedBoxShape,
    drawServerShape,
    drawShape,
    drawShareCertificateShape,
    drawSharePieShape,
    drawShieldShape,
    drawShipShape,
    drawSignboardShape,
    drawSiloShape,
    drawSmartphoneShape,
    drawSmokeShape,
    drawStatuteBookShape,
    drawStoreShape,
    drawStormShape,
    drawSummonsNoticeShape,
    drawSummonsShape,
    drawTankerShape,
    drawTaxDocShape,
    drawTellerCounterShape,
    drawToxicBarrelShape,
    drawTractorShape,
    drawTrainShape,
    drawTreeShape,
    drawTruckShape,
    drawTwoKeysShape,
    drawTwoWheelerShape,
    drawUmbrellaShape,
    drawUsbShape,
    drawVanShape,
    drawWalletShape,
    drawWarehouseShape,
    drawWatchShape,
    drawWomanShape,
    drawWrenchShape
  };

  console.log(`[SHAPE-CATALOG v2.5 MASTER] Initialized universal 19-category catalog with ${Object.keys(REGISTRY).length} registered keywords and 145 handcrafted shape functions.`);
})();
