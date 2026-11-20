// ============================================================================
// CA STUDY BOARD ANIMATION LIBRARY - GENERIC DETERMINISTIC SVG RENDERER
// Pure Vanilla JS · Zero Dependencies · Pure Function of Time t
// ============================================================================

(function(global) {
  "use strict";

  // Safe Math & Logic Expression Evaluator (Zero eval / Function)
  function evaluateExpr(expr, scope) {
    if (!expr || typeof expr !== "string") return false;
    try {
      return parseExpression(tokenize(expr), scope);
    } catch (e) {
      console.warn("Expr eval error:", expr, e);
      return false;
    }
  }

  function tokenize(str) {
    const tokens = [];
    let i = 0;
    while (i < str.length) {
      const ch = str[i];
      if (/\s/.test(ch)) { i++; continue; }
      if (/[0-9]/.test(ch)) {
        let num = "";
        while (i < str.length && /[0-9.]/.test(str[i])) { num += str[i]; i++; }
        tokens.push({ type: "num", val: parseFloat(num) });
        continue;
      }
      if (ch === "'" || ch === '"') {
        const quote = ch;
        i++;
        let s = "";
        while (i < str.length && str[i] !== quote) { s += str[i]; i++; }
        i++;
        tokens.push({ type: "str", val: s });
        continue;
      }
      // Operators
      const op2 = str.substr(i, 2);
      if (["==", "!=", "<=", ">=", "&&", "||"].includes(op2)) {
        tokens.push({ type: "op", val: op2 });
        i += 2;
        continue;
      }
      if (["+", "-", "*", "/", "%", "<", ">", "!", "?", ":", "(", ")"].includes(ch)) {
        tokens.push({ type: "op", val: ch });
        i++;
        continue;
      }
      // Identifiers / keywords
      if (/[a-zA-Z_]/.test(ch)) {
        let id = "";
        while (i < str.length && /[a-zA-Z0-9_]/.test(str[i])) { id += str[i]; i++; }
        if (id === "true") tokens.push({ type: "bool", val: true });
        else if (id === "false") tokens.push({ type: "bool", val: false });
        else if (id === "null") tokens.push({ type: "null", val: null });
        else tokens.push({ type: "id", val: id });
        continue;
      }
      i++;
    }
    return tokens;
  }

  function parseExpression(tokens, scope) {
    let pos = 0;
    function peek() { return tokens[pos]; }
    function consume() { return tokens[pos++]; }

    function parseTernary() {
      let cond = parseLogicalOr();
      if (peek() && peek().val === "?") {
        consume(); // '?'
        let ifTrue = parseTernary();
        if (peek() && peek().val === ":") {
          consume(); // ':'
          let ifFalse = parseTernary();
          return cond ? ifTrue : ifFalse;
        }
      }
      return cond;
    }

    function parseLogicalOr() {
      let left = parseLogicalAnd();
      while (peek() && peek().val === "||") {
        consume();
        let right = parseLogicalAnd();
        left = Boolean(left || right);
      }
      return left;
    }

    function parseLogicalAnd() {
      let left = parseEquality();
      while (peek() && peek().val === "&&") {
        consume();
        let right = parseEquality();
        left = Boolean(left && right);
      }
      return left;
    }

    function parseEquality() {
      let left = parseRelational();
      while (peek() && (peek().val === "==" || peek().val === "!=")) {
        let op = consume().val;
        let right = parseRelational();
        left = (op === "==") ? (left == right) : (left != right);
      }
      return left;
    }

    function parseRelational() {
      let left = parseAdditive();
      while (peek() && ["<", ">", "<=", ">="].includes(peek().val)) {
        let op = consume().val;
        let right = parseAdditive();
        if (op === "<") left = (left < right);
        else if (op === ">") left = (left > right);
        else if (op === "<=") left = (left <= right);
        else if (op === ">=") left = (left >= right);
      }
      return left;
    }

    function parseAdditive() {
      let left = parseMultiplicative();
      while (peek() && (peek().val === "+" || peek().val === "-")) {
        let op = consume().val;
        let right = parseMultiplicative();
        left = (op === "+") ? (left + right) : (left - right);
      }
      return left;
    }

    function parseMultiplicative() {
      let left = parseUnary();
      while (peek() && ["*", "/", "%"].includes(peek().val)) {
        let op = consume().val;
        let right = parseUnary();
        if (op === "*") left = left * right;
        else if (op === "/") left = right === 0 ? 0 : left / right;
        else if (op === "%") left = left % right;
      }
      return left;
    }

    function parseUnary() {
      if (peek() && peek().val === "!") {
        consume();
        return !parseUnary();
      }
      if (peek() && peek().val === "-") {
        consume();
        return -parseUnary();
      }
      return parsePrimary();
    }

    function parsePrimary() {
      let t = consume();
      if (!t) return null;
      if (t.type === "num" || t.type === "str" || t.type === "bool" || t.type === "null") {
        return t.val;
      }
      if (t.type === "id") {
        return scope[t.val] !== undefined ? scope[t.val] : 0;
      }
      if (t.val === "(") {
        let res = parseTernary();
        if (peek() && peek().val === ")") consume();
        return res;
      }
      return null;
    }

    return parseTernary();
  }

  // Indian Number Formatter
  function formatIndianNumberOnly(num) {
    if (num === null || num === undefined) return "0";
    const n = Math.round(Number(num));
    if (isNaN(n)) return "0";
    const isNeg = n < 0;
    const absStr = String(Math.abs(n));
    if (absStr.length <= 3) {
      return (isNeg ? "-" : "") + absStr;
    }
    const lastThree = absStr.substring(absStr.length - 3);
    const otherNumbers = absStr.substring(0, absStr.length - 3);
    const formatted = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + lastThree;
    return (isNeg ? "-" : "") + formatted;
  }

  function formatIndianRupee(num) {
    const isNeg = Number(num) < 0;
    const formatted = formatIndianNumberOnly(num);
    return (isNeg ? "-₹ " : "₹ ") + formatted.replace(/^-/, "");
  }

  function formatValue(val, fmt) {
    if (fmt === "inr") return formatIndianRupee(val);
    if (fmt === "percent") return `${val}%`;
    return String(val);
  }

  // Pure SVG Helpers
  const SVG_NS = "http://www.w3.org/2000/svg";
  function svgEl(name, attrs = {}, children = []) {
    const el = document.createElementNS(SVG_NS, name);
    for (const [k, v] of Object.entries(attrs)) {
      if (v !== undefined && v !== null) el.setAttribute(k, v);
    }
    for (const c of children) {
      if (typeof c === "string") el.textContent = c;
      else if (c) el.appendChild(c);
    }
    return el;
  }

  // Easing Functions
  const Ease = {
    linear: t => t,
    easeOut: t => 1 - Math.pow(1 - t, 3),
    easeInOut: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    backOut: t => {
      const c = 1.15;
      return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2);
    },
    bounceOut: t => {
      const n1 = 7.5625, d1 = 2.75;
      if (t < 1 / d1) return n1 * t * t;
      if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
      if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
      return n1 * (t -= 2.625 / d1) * t + 0.984375;
    }
  };

  // ----------------------------------------------------------------------------
  // Vector Primitive Renderers
  // ----------------------------------------------------------------------------
  const PRIMITIVE_RENDERERS = {
    // 1. ACTORS
    person: (props, scope) => {
      const g = svgEl("g", { class: "prim-person" });
      const role = props.role || "Owner";
      const name = props.name || "Party";
      const cx = (props.w || 100) / 2;
      // Avatar circle
      g.appendChild(svgEl("circle", { cx, cy: 38, r: 26, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      // Face / silhouette
      g.appendChild(svgEl("circle", { cx, cy: 32, r: 11, fill: "var(--accent)" }));
      g.appendChild(svgEl("path", { d: `M ${cx - 18} 54 C ${cx - 18} 44 ${cx - 10} 44 ${cx} 44 C ${cx + 10} 44 ${cx + 18} 44 ${cx + 18} 54 Z`, fill: "var(--accent)" }));
      // Label Card dynamically sized to text
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(90, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 72, width: labelW, height: 42, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 88, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 104, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    group_huf: (props) => {
      const g = svgEl("g", { class: "prim-group-huf" });
      const cx = (props.w || 120) / 2;
      // Multiple silhouettes
      g.appendChild(svgEl("circle", { cx: cx - 20, cy: 35, r: 18, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: cx + 20, cy: 35, r: 18, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: cx, cy: 30, r: 22, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      const name = props.name || "Family Group";
      const role = props.role || "Joint Entity";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 72, width: labelW, height: 42, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 88, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 104, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    company: (props) => {
      const g = svgEl("g", { class: "prim-company" });
      const cx = (props.w || 110) / 2;
      g.appendChild(svgEl("rect", { x: cx - 30, y: 15, width: 60, height: 55, rx: 4, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      // Windows grid
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          g.appendChild(svgEl("rect", { x: cx - 22 + c * 16, y: 23 + r * 14, width: 10, height: 9, rx: 2, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1 }));
        }
      }
      const name = props.name || "Company";
      const role = props.role || "Corporate";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 74, width: labelW, height: 40, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 90, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 105, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    firm: (props) => {
      const g = svgEl("g", { class: "prim-firm" });
      const cx = (props.w || 110) / 2;
      g.appendChild(svgEl("rect", { x: cx - 35, y: 18, width: 70, height: 50, rx: 8, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      g.appendChild(svgEl("path", { d: `M ${cx - 20} 45 L ${cx - 7} 35 L ${cx + 7} 48 L ${cx + 20} 38`, fill: "none", stroke: "var(--accent)", "stroke-width": 4, "stroke-linecap": "round" }));
      const name = props.name || "Party";
      const role = props.role || "Unit";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 74, width: labelW, height: 40, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 90, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 105, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    bank: (props) => {
      const g = svgEl("g", { class: "prim-bank" });
      const cx = (props.w || 110) / 2;
      g.appendChild(svgEl("path", { d: `M ${cx - 40} 30 L ${cx} 10 L ${cx + 40} 30 Z`, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      g.appendChild(svgEl("rect", { x: cx - 33, y: 30, width: 10, height: 36, fill: "var(--accent)" }));
      g.appendChild(svgEl("rect", { x: cx - 5, y: 30, width: 10, height: 36, fill: "var(--accent)" }));
      g.appendChild(svgEl("rect", { x: cx + 23, y: 30, width: 10, height: 36, fill: "var(--accent)" }));
      g.appendChild(svgEl("rect", { x: cx - 43, y: 66, width: 86, height: 8, rx: 2, fill: "var(--accent)" }));
      const name = props.name || "Office";
      const role = props.role || "Unit";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 76, width: labelW, height: 40, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 92, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 107, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    govt_dept: (props) => {
      const g = svgEl("g", { class: "prim-govt" });
      const cx = (props.w || 110) / 2;
      g.appendChild(svgEl("circle", { cx, cy: 38, r: 26, fill: "var(--surface)", stroke: "var(--gold)", "stroke-width": 3 }));
      g.appendChild(svgEl("path", { d: `M ${cx - 10} 38 L ${cx} 24 L ${cx + 10} 38 L ${cx} 52 Z`, fill: "var(--gold)" }));
      const name = props.name || "Office";
      const role = props.role || "Unit";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 74, width: labelW, height: 40, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 90, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 105, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    tax_office: (props) => {
      const g = svgEl("g", { class: "prim-tax-office" });
      const cx = (props.w || 110) / 2;
      g.appendChild(svgEl("rect", { x: cx - 35, y: 15, width: 70, height: 55, rx: 6, fill: "var(--surface)", stroke: "var(--warn)", "stroke-width": 3 }));
      g.appendChild(svgEl("text", { x: cx, y: 48, "text-anchor": "middle", "font-size": 24, "font-weight": "900", fill: "var(--warn)" }, ["₹"]));
      const name = props.name || "Office";
      const role = props.role || "Unit";
      const maxTextLen = Math.max(name.length, role.length);
      const labelW = Math.max(100, Math.min(220, Math.round(maxTextLen * 9.5) + 24));
      const rxLeft = cx - labelW / 2;
      g.appendChild(svgEl("rect", { x: rxLeft, y: 74, width: labelW, height: 40, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: cx, y: 90, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [name]));
      g.appendChild(svgEl("text", { x: cx, y: 105, "text-anchor": "middle", "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [role]));
      return g;
    },

    // 2. ASSETS
    house: (props) => {
      const g = svgEl("g", { class: "prim-house" });
      // Roof
      g.appendChild(svgEl("path", { d: "M 15 45 L 55 15 L 95 45 Z", fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 3, "stroke-linejoin": "round" }));
      // Walls
      g.appendChild(svgEl("rect", { x: 24, y: 44, width: 62, height: 46, rx: 4, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      // Door & Window
      g.appendChild(svgEl("rect", { x: 45, y: 60, width: 20, height: 30, rx: 2, fill: "var(--accent)" }));
      g.appendChild(svgEl("rect", { x: 30, y: 52, width: 12, height: 12, rx: 2, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("rect", { x: 68, y: 52, width: 12, height: 12, rx: 2, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1.5 }));
      return g;
    },

    land: (props) => {
      const g = svgEl("g", { class: "prim-land" });
      g.appendChild(svgEl("polygon", { points: "15,65 55,25 95,45 80,80 30,80", fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 3 }));
      g.appendChild(svgEl("circle", { cx: 55, cy: 25, r: 4, fill: "var(--warn)" }));
      g.appendChild(svgEl("circle", { cx: 95, cy: 45, r: 4, fill: "var(--warn)" }));
      g.appendChild(svgEl("text", { x: 55, y: 62, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ok)" }, ["LAND"]));
      return g;
    },

    shares: (props) => {
      const g = svgEl("g", { class: "prim-shares" });
      g.appendChild(svgEl("rect", { x: 18, y: 22, width: 54, height: 50, rx: 4, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 2 }));
      g.appendChild(svgEl("rect", { x: 24, y: 16, width: 54, height: 50, rx: 4, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("path", { d: "M 32 45 L 42 35 L 52 42 L 68 26", fill: "none", stroke: "var(--ok)", "stroke-width": 3, "stroke-linecap": "round" }));
      return g;
    },

    gold: (props) => {
      const g = svgEl("g", { class: "prim-gold" });
      g.appendChild(svgEl("polygon", { points: "20,55 35,25 75,25 90,55", fill: "var(--gold-soft)", stroke: "var(--gold)", "stroke-width": 3 }));
      g.appendChild(svgEl("polygon", { points: "20,55 90,55 85,75 25,75", fill: "var(--gold)", stroke: "var(--gold)", "stroke-width": 2 }));
      g.appendChild(svgEl("text", { x: 55, y: 46, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: "var(--gold)" }, ["GOLD"]));
      return g;
    },

    // 3. INSTRUMENTS
    money_bag: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-money-bag" });
      const amt = props.amount !== undefined ? formatIndianRupee(props.amount) : "₹ Cash";
      g.appendChild(svgEl("path", { d: "M 45 22 C 38 10 62 10 55 22 Z", fill: "var(--gold)" }));
      g.appendChild(svgEl("path", { d: "M 25 35 C 15 70 30 85 50 85 C 70 85 85 70 75 35 Z", fill: "var(--gold-soft)", stroke: "var(--gold)", "stroke-width": 3.5 }));
      g.appendChild(svgEl("text", { x: 50, y: 62, "text-anchor": "middle", "font-size": 22, "font-weight": "900", fill: "var(--gold)" }, ["₹"]));
      if (props.show_label !== false) {
        g.appendChild(svgEl("rect", { x: 5, y: 88, width: 90, height: 26, rx: 6, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
        g.appendChild(svgEl("text", { x: 50, y: 105, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [amt]));
      }
      return g;
    },

    document: (props) => {
      const g = svgEl("g", { class: "prim-document" });
      g.appendChild(svgEl("path", { d: "M 15 10 L 55 10 L 70 25 L 70 85 L 15 85 Z", fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("polygon", { points: "55,10 55,25 70,25", fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("line", { x1: 25, y1: 35, x2: 60, y2: 35, stroke: "var(--line)", "stroke-width": 3, "stroke-linecap": "round" }));
      g.appendChild(svgEl("line", { x1: 25, y1: 48, x2: 60, y2: 48, stroke: "var(--line)", "stroke-width": 3, "stroke-linecap": "round" }));
      g.appendChild(svgEl("line", { x1: 25, y1: 61, x2: 48, y2: 61, stroke: "var(--line)", "stroke-width": 3, "stroke-linecap": "round" }));
      return g;
    },

    // 4. INDICATORS & METAPHORS
    gate: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-gate" });
      const isOpen = Boolean(props.open);
      const angle = isOpen ? (p !== undefined ? p * 75 : 75) : 0;
      // Posts
      g.appendChild(svgEl("rect", { x: 10, y: 10, width: 14, height: 80, rx: 4, fill: "var(--ink)", stroke: "var(--line)", "stroke-width": 2 }));
      g.appendChild(svgEl("rect", { x: 116, y: 10, width: 14, height: 80, rx: 4, fill: "var(--ink)", stroke: "var(--line)", "stroke-width": 2 }));
      // Left Door
      const leftDoor = svgEl("g", { transform: `translate(24, 20) rotate(${-angle})` });
      leftDoor.appendChild(svgEl("rect", { x: 0, y: 0, width: 44, height: 60, rx: 4, fill: isOpen ? "var(--ok-soft)" : "var(--warn-soft)", stroke: isOpen ? "var(--ok)" : "var(--warn)", "stroke-width": 3 }));
      leftDoor.appendChild(svgEl("line", { x1: 0, y1: 0, x2: 44, y2: 60, stroke: isOpen ? "var(--ok)" : "var(--warn)", "stroke-width": 2 }));
      g.appendChild(leftDoor);
      // Right Door
      const rightDoor = svgEl("g", { transform: `translate(116, 20) rotate(${angle})` });
      rightDoor.appendChild(svgEl("rect", { x: -44, y: 0, width: 44, height: 60, rx: 4, fill: isOpen ? "var(--ok-soft)" : "var(--warn-soft)", stroke: isOpen ? "var(--ok)" : "var(--warn)", "stroke-width": 3 }));
      rightDoor.appendChild(svgEl("line", { x1: 0, y1: 0, x2: -44, y2: 60, stroke: isOpen ? "var(--ok)" : "var(--warn)", "stroke-width": 2 }));
      g.appendChild(rightDoor);
      return g;
    },

    padlock: (props) => {
      const g = svgEl("g", { class: "prim-padlock" });
      const isLocked = props.locked !== false;
      const shackleOffset = isLocked ? 0 : -10;
      g.appendChild(svgEl("path", {
        d: `M 22 ${32 + shackleOffset} C 22 14 48 14 48 ${32 + shackleOffset}`,
        fill: "none", stroke: isLocked ? "var(--warn)" : "var(--ok)", "stroke-width": 6, "stroke-linecap": "round"
      }));
      g.appendChild(svgEl("rect", { x: 12, y: 30, width: 46, height: 38, rx: 8, fill: isLocked ? "var(--warn-soft)" : "var(--ok-soft)", stroke: isLocked ? "var(--warn)" : "var(--ok)", "stroke-width": 3 }));
      g.appendChild(svgEl("circle", { cx: 35, cy: 46, r: 4, fill: isLocked ? "var(--warn)" : "var(--ok)" }));
      return g;
    },

    tick: (props) => {
      const g = svgEl("g", { class: "prim-tick" });
      g.appendChild(svgEl("circle", { cx: 20, cy: 20, r: 18, fill: "var(--ok-soft)", stroke: "var(--ok)", "stroke-width": 3 }));
      g.appendChild(svgEl("path", { d: "M 11 20 L 17 26 L 29 14", fill: "none", stroke: "var(--ok)", "stroke-width": 3.5, "stroke-linecap": "round", "stroke-linejoin": "round" }));
      return g;
    },

    cross: (props) => {
      const g = svgEl("g", { class: "prim-cross" });
      g.appendChild(svgEl("circle", { cx: 20, cy: 20, r: 18, fill: "var(--warn-soft)", stroke: "var(--warn)", "stroke-width": 3 }));
      g.appendChild(svgEl("path", { d: "M 13 13 L 27 27 M 27 13 L 13 27", fill: "none", stroke: "var(--warn)", "stroke-width": 3.5, "stroke-linecap": "round" }));
      return g;
    },

    arrow: (props) => {
      const g = svgEl("g", { class: "prim-arrow" });
      const w = props.w || 100;
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      g.appendChild(svgEl("line", { x1: 5, y1: 10, x2: w - 12, y2: 10, stroke: tone, "stroke-width": 4, "stroke-linecap": "round" }));
      g.appendChild(svgEl("polygon", { points: `${w},10 ${w - 14},4 ${w - 14},16`, fill: tone }));
      if (props.label) {
        g.appendChild(svgEl("text", { x: w / 2, y: -4, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: tone }, [props.label]));
      }
      return g;
    },

    line: (props) => {
      const g = svgEl("g", { class: "prim-line" });
      const w = props.w || 200;
      const tone = props.tone ? `var(--${props.tone})` : "var(--line)";
      const dashed = props.dashed ? "6 6" : "none";
      g.appendChild(svgEl("line", { x1: 0, y1: 2, x2: w, y2: 2, stroke: tone, "stroke-width": props.stroke_width || 3, "stroke-dasharray": dashed }));
      if (props.label) {
        g.appendChild(svgEl("text", { x: w / 2, y: -8, "text-anchor": "middle", "font-size": 16, "font-weight": "700", fill: tone }, [props.label]));
      }
      return g;
    },

    strike: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-strike" });
      const w = props.w || 140;
      const progress = p !== undefined ? p : 1.0;
      const curX = w * progress;
      g.appendChild(svgEl("line", {
        x1: 0, y1: 12, x2: curX, y2: 12,
        stroke: "var(--warn)", "stroke-width": props.stroke_width || 4.5, "stroke-linecap": "round"
      }));
      return g;
    },

    gavel: (props) => {
      const g = svgEl("g", { class: "prim-gavel" });
      const w = props.w || 70, h = props.h || 70;
      g.appendChild(svgEl("rect", { x: 10, y: 52, width: 50, height: 12, rx: 3, fill: "var(--ink-muted)", stroke: "var(--ink)", "stroke-width": 1.5 }));
      const mallet = svgEl("g", { transform: "translate(35, 25) rotate(-30)" });
      mallet.appendChild(svgEl("rect", { x: -16, y: -10, width: 32, height: 20, rx: 4, fill: "var(--gold)", stroke: "var(--ink)", "stroke-width": 2 }));
      mallet.appendChild(svgEl("rect", { x: -4, y: 10, width: 8, height: 35, rx: 3, fill: "var(--line)", stroke: "var(--ink)", "stroke-width": 1.5 }));
      g.appendChild(mallet);
      return g;
    },

    clock: (props) => {
      const g = svgEl("g", { class: "prim-clock" });
      const w = props.w || 50, h = props.h || 50;
      const r = Math.min(w, h) / 2 - 4;
      g.appendChild(svgEl("circle", { cx: w/2, cy: h/2, r, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 3 }));
      g.appendChild(svgEl("circle", { cx: w/2, cy: h/2, r: 3, fill: "var(--accent)" }));
      g.appendChild(svgEl("line", { x1: w/2, y1: h/2, x2: w/2, y2: h/2 - r*0.65, stroke: "var(--ink)", "stroke-width": 2.5, "stroke-linecap": "round" }));
      g.appendChild(svgEl("line", { x1: w/2, y1: h/2, x2: w/2 + r*0.5, y2: h/2, stroke: "var(--ink)", "stroke-width": 2, "stroke-linecap": "round" }));
      return g;
    },

    calendar: (props) => {
      const g = svgEl("g", { class: "prim-calendar" });
      const w = props.w || 60, h = props.h || 60;
      g.appendChild(svgEl("rect", { x: 4, y: 8, width: w - 8, height: h - 12, rx: 8, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("rect", { x: 4, y: 8, width: w - 8, height: 16, rx: 4, fill: "var(--accent)" }));
      g.appendChild(svgEl("rect", { x: 14, y: 2, width: 4, height: 10, rx: 2, fill: "var(--ink)" }));
      g.appendChild(svgEl("rect", { x: w - 18, y: 2, width: 4, height: 10, rx: 2, fill: "var(--ink)" }));
      const dateText = props.date || "31";
      g.appendChild(svgEl("text", { x: w / 2, y: h / 2 + 14, "text-anchor": "middle", "font-size": 18, "font-weight": "900", fill: "var(--ink)" }, [dateText]));
      return g;
    },

    coin: (props) => {
      const g = svgEl("g", { class: "prim-coin" });
      const w = props.w || 50, h = props.h || 50;
      const r = Math.min(w, h) / 2 - 3;
      g.appendChild(svgEl("circle", { cx: w/2, cy: h/2, r, fill: "var(--gold-soft)", stroke: "var(--gold)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: w/2, cy: h/2, r: r - 5, fill: "none", stroke: "var(--gold)", "stroke-width": 1.5, "stroke-dasharray": "3 2" }));
      g.appendChild(svgEl("text", { x: w/2, y: h/2 + 6, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: "var(--gold)" }, ["₹"]));
      return g;
    },

    split: (props) => {
      const g = svgEl("g", { class: "prim-split" });
      const w = props.w || 280, h = props.h || 60;
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      g.appendChild(svgEl("path", {
        d: `M 10 ${h/2} L ${w*0.35} ${h/2} C ${w*0.5} ${h/2} ${w*0.5} 12 ${w*0.7} 12 L ${w - 12} 12`,
        fill: "none", stroke: "var(--gold)", "stroke-width": 3, "stroke-dasharray": "4 3"
      }));
      g.appendChild(svgEl("polygon", { points: `${w},12 ${w - 10},7 ${w - 10},17`, fill: "var(--gold)" }));
      g.appendChild(svgEl("path", {
        d: `M 10 ${h/2} L ${w*0.35} ${h/2} C ${w*0.5} ${h/2} ${w*0.5} ${h - 12} ${w*0.7} ${h - 12} L ${w - 12} ${h - 12}`,
        fill: "none", stroke: tone, "stroke-width": 3
      }));
      g.appendChild(svgEl("polygon", { points: `${w},${h - 12} ${w - 10},${h - 17} ${w - 10},${h - 7}`, fill: tone }));
      return g;
    },

    merge: (props) => {
      const g = svgEl("g", { class: "prim-merge" });
      const w = props.w || 280, h = props.h || 60;
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      g.appendChild(svgEl("path", {
        d: `M 12 12 L ${w*0.3} 12 C ${w*0.5} 12 ${w*0.5} ${h/2} ${w*0.65} ${h/2} L ${w - 12} ${h/2}`,
        fill: "none", stroke: "var(--gold)", "stroke-width": 3, "stroke-dasharray": "4 3"
      }));
      g.appendChild(svgEl("path", {
        d: `M 12 ${h - 12} L ${w*0.3} ${h - 12} C ${w*0.5} ${h - 12} ${w*0.5} ${h/2} ${w*0.65} ${h/2} L ${w - 12} ${h/2}`,
        fill: "none", stroke: tone, "stroke-width": 3
      }));
      g.appendChild(svgEl("polygon", { points: `${w},${h/2} ${w - 10},${h/2 - 6} ${w - 10},${h/2 + 6}`, fill: tone }));
      return g;
    },

    machinery: (props) => {
      const g = svgEl("g", { class: "prim-machinery" });
      const w = props.w || 80, h = props.h || 80;
      g.appendChild(svgEl("rect", { x: 10, y: 35, width: 60, height: 35, rx: 6, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: 40, cy: 30, r: 16, fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("circle", { cx: 40, cy: 30, r: 6, fill: "var(--accent)" }));
      for (let a = 0; a < 8; a++) {
        const rad = (a * 45 * Math.PI) / 180;
        const x1 = 40 + 16 * Math.cos(rad);
        const y1 = 30 + 16 * Math.sin(rad);
        const x2 = 40 + 20 * Math.cos(rad);
        const y2 = 30 + 20 * Math.sin(rad);
        g.appendChild(svgEl("line", { x1, y1, x2, y2, stroke: "var(--accent)", "stroke-width": 3, "stroke-linecap": "round" }));
      }
      return g;
    },

    stack: (props) => {
      const g = svgEl("g", { class: "prim-stack" });
      const w = props.w || 200, h = props.h || 60;
      const tone = props.tone || "surface";
      const bg = tone === "ok" ? "var(--ok-soft)" : (tone === "warn" ? "var(--warn-soft)" : "var(--surface)");
      const border = tone === "ok" ? "var(--ok)" : (tone === "warn" ? "var(--warn)" : "var(--line)");
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: 8, fill: bg, stroke: border, "stroke-width": 2 }));
      if (props.label) {
        g.appendChild(svgEl("text", { x: 16, y: h / 2 + 6, "font-size": 17, "font-weight": "800", fill: "var(--ink)" }, [props.label]));
      }
      return g;
    },

    business: (props) => {
      const g = svgEl("g", { class: "prim-business" });
      const w = props.w || 80, h = props.h || 80;
      g.appendChild(svgEl("rect", { x: 10, y: 25, width: 60, height: 50, rx: 6, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
      g.appendChild(svgEl("path", { d: "M 6 25 L 14 10 L 74 10 L 66 25 Z", fill: "var(--accent-soft)", stroke: "var(--accent)", "stroke-width": 2 }));
      g.appendChild(svgEl("rect", { x: 30, y: 45, width: 20, height: 30, rx: 3, fill: "var(--accent)" }));
      return g;
    },

    bonds: (props) => {
      const g = svgEl("g", { class: "prim-bonds" });
      const w = props.w || 70, h = props.h || 70;
      g.appendChild(svgEl("rect", { x: 10, y: 15, width: 50, height: 42, rx: 5, fill: "var(--gold-soft)", stroke: "var(--gold)", "stroke-width": 2 }));
      g.appendChild(svgEl("circle", { cx: 35, cy: 36, r: 10, fill: "none", stroke: "var(--gold)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: 35, y: 40, "text-anchor": "middle", "font-size": 10, "font-weight": "900", fill: "var(--gold)" }, ["BOND"]));
      return g;
    },

    scale: (props) => {
      const g = svgEl("g", { class: "prim-scale" });
      const w = props.w || 80, h = props.h || 80;
      g.appendChild(svgEl("line", { x1: 40, y1: 15, x2: 40, y2: 65, stroke: "var(--ink)", "stroke-width": 3 }));
      g.appendChild(svgEl("polygon", { points: "30,70 50,70 40,65", fill: "var(--ink)" }));
      g.appendChild(svgEl("line", { x1: 15, y1: 22, x2: 65, y2: 22, stroke: "var(--accent)", "stroke-width": 3, "stroke-linecap": "round" }));
      g.appendChild(svgEl("path", { d: "M 15 22 L 10 40 Q 20 45 30 40 Z", fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("path", { d: "M 65 22 L 60 40 Q 70 45 80 40 Z", fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 1.5 }));
      return g;
    },

    curved_arrow: (props) => {
      const g = svgEl("g", { class: "prim-curved-arrow" });
      const w = props.w || 100, h = props.h || 60;
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      g.appendChild(svgEl("path", {
        d: `M 10 ${h - 10} C 10 15 ${w - 20} 15 ${w - 12} ${h - 15}`,
        fill: "none", stroke: tone, "stroke-width": 3, "stroke-linecap": "round"
      }));
      g.appendChild(svgEl("polygon", { points: `${w - 6},${h - 8} ${w - 18},${h - 18} ${w - 4},${h - 22}`, fill: tone }));
      return g;
    },

    // 5. CONTAINERS & DATA VISUALS
    card: (props) => {
      const g = svgEl("g", { class: "prim-card" });
      const w = props.w || 240, h = props.h || 160, rx = props.rx || 14;
      const tone = props.tone || "surface";
      const borderTone = props.border_tone ? `var(--${props.border_tone})` : "var(--line)";
      const bg = tone === "accent" ? "var(--accent-soft)" : (tone === "ok" ? "var(--ok-soft)" : (tone === "warn" ? "var(--warn-soft)" : "var(--surface-card)"));
      // Drop shadow simulation
      g.appendChild(svgEl("rect", { x: 2, y: 4, width: w, height: h, rx, fill: "var(--shadow)" }));
      // Base rect
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx, fill: bg, stroke: borderTone, "stroke-width": 2 }));
      // Top accent bar if requested
      if (props.top_bar) {
        g.appendChild(svgEl("path", { d: `M 0 ${rx} Q 0 0 ${rx} 0 L ${w - rx} 0 Q ${w} 0 ${w} ${rx} L ${w} 8 L 0 8 Z`, fill: `var(--${props.top_bar})` }));
      }
      // Content slots
      if (props.title) {
        g.appendChild(svgEl("text", { x: 20, y: 32, "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [props.title]));
      }
      if (props.subtitle) {
        g.appendChild(svgEl("text", { x: 20, y: 52, "font-size": 16, "font-weight": "600", fill: "var(--ink-muted)" }, [props.subtitle]));
      }
      return g;
    },

    pill: (props) => {
      const g = svgEl("g", { class: "prim-pill" });
      const w = props.w || 110, h = props.h || 32;
      const tone = props.tone || "accent";
      const bg = `var(--${tone}-soft)`;
      const fg = `var(--${tone})`;
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: h / 2, fill: bg, stroke: fg, "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: w / 2, y: h / 2 + 5, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: fg }, [props.text || "Status"]));
      return g;
    },

    text: (props) => {
      const g = svgEl("g", { class: "prim-text" });
      const align = props.align || "left";
      const anchor = align === "center" ? "middle" : (align === "right" ? "end" : "start");
      let size = Math.max(16, props.font_size || 20);
      const weight = props.weight || "700";
      const fill = props.tone ? `var(--${props.tone})` : "var(--ink)";
      const maxW = props.w || 200;
      const x = align === "center" ? maxW / 2 : (align === "right" ? maxW : 0);
      
      const rawText = String(props.text || "");
      let charWidth = size * 0.58;
      let maxCharsPerLine = Math.max(12, Math.floor(maxW / charWidth));

      // Title auto-fit: auto-shrink font size if text would exceed 2 lines
      if (props.is_title) {
        while (size > 18 && rawText.length > maxCharsPerLine * 2) {
          size -= 2;
          charWidth = size * 0.58;
          maxCharsPerLine = Math.max(12, Math.floor(maxW / charWidth));
        }
      }

      const textEl = svgEl("text", {
        x, y: size, "text-anchor": anchor,
        "font-size": size, "font-weight": weight, fill
      });

      if (rawText.length > maxCharsPerLine && !rawText.includes("\n")) {
        const words = rawText.split(/\s+/);
        let curLine = "";
        let lineIdx = 0;
        words.forEach(w => {
          if ((curLine + " " + w).trim().length <= maxCharsPerLine) {
            curLine = (curLine + " " + w).trim();
          } else {
            if (curLine) {
              const tspan = svgEl("tspan", { x, dy: lineIdx === 0 ? 0 : size * 1.25 }, [curLine]);
              textEl.appendChild(tspan);
              lineIdx++;
            }
            curLine = w;
          }
        });
        if (curLine) {
          const tspan = svgEl("tspan", { x, dy: lineIdx === 0 ? 0 : size * 1.25 }, [curLine]);
          textEl.appendChild(tspan);
        }
      } else {
        textEl.textContent = rawText;
      }
      g.appendChild(textEl);
      return g;
    },

    counter: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-counter" });
      const targetVal = props.value !== undefined ? props.value : 0;
      const curVal = p !== undefined ? Math.round(targetVal * p) : targetVal;
      const fmt = props.format || "inr";
      const displayStr = formatValue(curVal, fmt);
      const size = props.font_size || 38;
      const tone = props.tone ? `var(--${props.tone})` : "var(--ink)";
      g.appendChild(svgEl("text", {
        x: (props.w || 200) / 2, y: size,
        "text-anchor": "middle", "font-size": size, "font-weight": "900", fill: tone
      }, [displayStr]));
      if (props.label) {
        g.appendChild(svgEl("text", {
          x: (props.w || 200) / 2, y: size + 20,
          "text-anchor": "middle", "font-size": 16, "font-weight": "700", fill: "var(--ink-muted)"
        }, [props.label]));
      }
      return g;
    },

    ledger_row: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-ledger-row" });
      const w = props.w || 640, h = props.h || 46;
      const isTotal = Boolean(props.is_total);
      const sign = props.sign || "+";
      const label = props.label || "Particulars";
      const rawVal = props.value !== undefined ? props.value : 0;
      const valStr = formatIndianRupee(rawVal);
      const signTone = sign === "-" ? "var(--warn)" : (isTotal ? "var(--ok)" : "var(--accent)");

      // Row background
      g.appendChild(svgEl("rect", {
        x: 0, y: 0, width: w, height: h, rx: 8,
        fill: isTotal ? "var(--ok-soft)" : "var(--surface)",
        stroke: isTotal ? "var(--ok)" : "var(--line)",
        "stroke-width": isTotal ? 2 : 1
      }));

      // Sign pill
      g.appendChild(svgEl("circle", { cx: 24, cy: h / 2, r: 12, fill: "var(--surface)", stroke: signTone, "stroke-width": 2 }));
      g.appendChild(svgEl("text", { x: 24, y: h / 2 + 5, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: signTone }, [sign]));

      // Particulars
      g.appendChild(svgEl("text", { x: 50, y: h / 2 + 5, "font-size": isTotal ? 20 : 18, "font-weight": isTotal ? "800" : "600", fill: "var(--ink)" }, [label]));

      // Value
      g.appendChild(svgEl("text", { x: w - 24, y: h / 2 + 6, "text-anchor": "end", "font-size": isTotal ? 19 : 16, "font-weight": "900", fill: isTotal ? "var(--ok)" : "var(--ink)" }, [valStr]));
      return g;
    },

    bar: (props, scope, p) => {
      const g = svgEl("g", { class: "prim-bar" });
      const w = props.w || 320, h = props.h || 36;
      const maxVal = props.max || 100;
      const targetVal = props.value || 0;
      const curVal = p !== undefined ? targetVal * p : targetVal;
      const ratio = Math.max(0, Math.min(1.0, curVal / Math.max(1, maxVal)));
      const fillW = Math.max(4, w * ratio);
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";

      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: fillW, height: h, rx: 8, fill: tone }));
      if (props.label) {
        g.appendChild(svgEl("text", { x: 12, y: h / 2 + 5, "font-size": 16, "font-weight": "800", fill: ratio > 0.4 ? "#fff" : "var(--ink)" }, [props.label]));
      }
      const valStr = formatIndianRupee(curVal);
      g.appendChild(svgEl("text", { x: w - 12, y: h / 2 + 5, "text-anchor": "end", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [valStr]));
      return g;
    },

    slab_step: (props) => {
      const g = svgEl("g", { class: "prim-slab-step" });
      const w = props.w || 300, h = props.h || 46;
      const rate = props.rate || "10%";
      const range = props.range || props.label || "Up to Slab";
      let taxStr = "₹ 0";
      if (props.tax !== undefined && props.tax !== null) {
        taxStr = typeof props.tax === "number" ? formatIndianRupee(props.tax) : String(props.tax);
      }
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      const toneSoft = props.tone ? `var(--${props.tone}-soft)` : "var(--accent-soft)";
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: 8, fill: "var(--surface)", stroke: "var(--line)", "stroke-width": 1.5 }));
      const rateBadgeW = Math.max(70, Math.min(95, Math.round(w * 0.28)));
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: rateBadgeW, height: h, rx: 8, fill: toneSoft, stroke: tone, "stroke-width": 1.5 }));
      g.appendChild(svgEl("text", { x: Math.round(rateBadgeW / 2), y: Math.round(h / 2) + 5, "text-anchor": "middle", "font-size": 16, "font-weight": "900", fill: tone }, [rate]));
      g.appendChild(svgEl("text", { x: rateBadgeW + 12, y: Math.round(h / 2) + 5, "font-size": 16, "font-weight": "700", fill: "var(--ink)" }, [range]));
      g.appendChild(svgEl("text", { x: w - 16, y: Math.round(h / 2) + 5, "text-anchor": "end", "font-size": 16, "font-weight": "800", fill: "var(--ok)" }, [taxStr]));
      return g;
    },

    timeline_axis: (props) => {
      const g = svgEl("g", { class: "prim-timeline-axis" });
      const w = props.w || 700;
      g.appendChild(svgEl("line", { x1: 20, y1: 25, x2: w - 20, y2: 25, stroke: "var(--line)", "stroke-width": 4, "stroke-linecap": "round" }));
      if (props.ticks && Array.isArray(props.ticks)) {
        props.ticks.forEach(t => {
          const tx = 20 + (t.pos || 0) * (w - 40);
          g.appendChild(svgEl("line", { x1: tx, y1: 15, x2: tx, y2: 35, stroke: "var(--accent)", "stroke-width": 3 }));
          g.appendChild(svgEl("circle", { cx: tx, cy: 25, r: 6, fill: "var(--surface)", stroke: "var(--accent)", "stroke-width": 2.5 }));
          g.appendChild(svgEl("text", { x: tx, y: 50, "text-anchor": "middle", "font-size": 16, "font-weight": "700", fill: "var(--ink)" }, [t.label || ""]));
        });
      }
      return g;
    },

    window_bar: (props) => {
      const g = svgEl("g", { class: "prim-window-bar" });
      const w = props.w || 260, h = props.h || 36;
      const isValid = props.valid !== false;
      const tone = isValid ? "ok" : "warn";
      g.appendChild(svgEl("rect", { x: 0, y: 0, width: w, height: h, rx: 8, fill: `var(--${tone}-soft)`, stroke: `var(--${tone})`, "stroke-width": 2, "stroke-dasharray": "6 4" }));
      g.appendChild(svgEl("text", { x: w / 2, y: h / 2 + 5, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: `var(--${tone})` }, [props.label || "Relief Window"]));
      return g;
    },

    marker: (props) => {
      const g = svgEl("g", { class: "prim-marker" });
      const tone = props.tone ? `var(--${props.tone})` : "var(--accent)";
      g.appendChild(svgEl("path", { d: "M 20 5 C 10 5 10 22 20 38 C 30 22 30 5 20 5 Z", fill: tone }));
      g.appendChild(svgEl("circle", { cx: 20, cy: 16, r: 5, fill: "#fff" }));
      if (props.label) {
        g.appendChild(svgEl("text", { x: 20, y: 54, "text-anchor": "middle", "font-size": 16, "font-weight": "800", fill: "var(--ink)" }, [props.label]));
      }
      return g;
    }
  };

  // ----------------------------------------------------------------------------
  // Animation Instance (Pure Function of Time t)
  // ----------------------------------------------------------------------------
  class AnimationInstance {
    constructor(container, def, slots = {}, options = {}) {
      this.container = container;
      this.def = def;
      this.initialSlots = slots;
      this.timingMap = options.timingMap || {};
      this.theme = options.theme || "light";
      this.speed = 1.0;
      this.currentTime = 0.0;
      this.isPlaying = false;
      this.rafId = null;
      this.lastTimestamp = null;
      this.reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      this.initStage();
      this.updateSlots(slots);
      this.setTime(0.0);
    }

    initStage() {
      this.container.innerHTML = "";
      this.container.setAttribute("data-theme", this.theme);
      this.renderedElements = new Map();

      // Create Root SVG Canvas
      this.svg = svgEl("svg", {
        viewBox: "0 0 1000 562",
        class: "ca-anim-stage",
        "shape-rendering": "geometricPrecision",
        "text-rendering": "geometricPrecision",
        style: "width:100%;height:100%;display:block;background:var(--bg);user-select:none;contain:paint layout;"
      });

      // Background rect for clean capture
      this.svg.appendChild(svgEl("rect", { width: 1000, height: 562, fill: "var(--bg)" }));

      // Root content group
      this.stageGroup = svgEl("g", { class: "anim-stage-group" });
      this.svg.appendChild(this.stageGroup);
      this.container.appendChild(this.svg);
    }

    updateSlots(newSlots) {
      // 1. Merge default slots with user provided slots
      this.currentSlots = {};
      (this.def.slots || []).forEach(s => {
        this.currentSlots[s.key] = s.default;
      });
      Object.assign(this.currentSlots, newSlots);
      this.currentSlots["anim_title"] = this.def.title;

      // 2. Compute derived values safely
      (this.def.derived || []).forEach(d => {
        this.currentSlots[d.key] = evaluateExpr(d.expr, this.currentSlots);
      });

      // 3. Compute effective cue timecodes (supporting timingMap override)
      this.effectiveCues = {};
      (this.def.cues || []).forEach(c => {
        this.effectiveCues[c.id] = (this.timingMap[c.id] !== undefined)
          ? Number(this.timingMap[c.id])
          : Number(c.default_t);
      });

      this.duration = Number(this.def.duration || 14.0);
      if (this.renderedElements) {
        this.renderedElements.clear();
      }
      if (this.stageGroup) {
        this.stageGroup.innerHTML = "";
      }
      this.renderCurrentState();
    }

    renderCurrentState() {
      const t = this.currentTime;
      const currentActiveIds = new Set();

      // Resolve each scene element deterministically
      (this.def.scene || []).forEach(elem => {
        // Evaluate "when" condition
        if (elem.when && !evaluateExpr(elem.when, this.currentSlots)) {
          return; // element conditioned out
        }

        // Suppress badged element if its parent container is conditioned out or inactive
        if (elem.badge_on && !currentActiveIds.has(elem.badge_on)) {
          return; // parent container not rendered
        }

        // Determine appearance timestamp
        let tEnter = 0.0;
        if (elem.cue && this.effectiveCues[elem.cue] !== undefined) {
          tEnter = this.effectiveCues[elem.cue];
        }
        if (elem.offset_t) tEnter += elem.offset_t;

        // If time t is before appearance, element is not rendered
        if (t < tEnter) return;

        currentActiveIds.add(elem.id);

        const enterDur = elem.enter_dur || 0.6;
        const pEnter = Math.min(1.0, Math.max(0.0, (t - tEnter) / enterDur));
        const easedEnter = Ease.easeOut(pEnter);

        // Calculate motion if specified
        let pMotion = 0.0;
        let motionX = 0, motionY = 0, motionScale = 1.0;
        if (elem.motion) {
          const tMotion = tEnter + (elem.motion.delay || 0.0);
          const mDur = elem.motion.duration || 1.0;
          if (t >= tMotion) {
            pMotion = Math.min(1.0, Math.max(0.0, (t - tMotion) / mDur));
            const easedM = Ease.easeInOut(pMotion);
            if (elem.motion.type === "move_to") {
              motionX = (elem.motion.to_x - elem.x) * easedM;
              motionY = (elem.motion.to_y - elem.y) * easedM;
            } else if (elem.motion.type === "scale_to") {
              motionScale = 1.0 + (elem.motion.to_scale - 1.0) * easedM;
            }
          }
        }

        // Element coordinate calculation
        let curX = elem.x + motionX;
        let curY = elem.y + motionY;
        let curScale = motionScale;
        let curOpacity = 1.0;

        // Enter presets: clean smooth easing without jitter or bouncing
        const enterPreset = elem.enter || "fade";
        if (enterPreset === "fade") {
          curOpacity = easedEnter;
        } else if (enterPreset === "pop") {
          curOpacity = easedEnter;
          curScale *= (0.92 + 0.08 * Ease.easeOut(pEnter));
        } else if (enterPreset === "slide_up") {
          curOpacity = easedEnter;
          curY += (1.0 - easedEnter) * 16;
        } else if (enterPreset === "slide_down") {
          curOpacity = easedEnter;
          curY -= (1.0 - easedEnter) * 16;
        } else if (enterPreset === "slide_left") {
          curOpacity = easedEnter;
          curX += (1.0 - easedEnter) * 20;
        } else if (enterPreset === "slide_right") {
          curOpacity = easedEnter;
          curX -= (1.0 - easedEnter) * 20;
        } else if (enterPreset === "grow") {
          curOpacity = easedEnter;
          curScale *= easedEnter;
        } else if (enterPreset === "stamp") {
          curOpacity = easedEnter;
          curScale *= (1.2 - 0.2 * Ease.easeOut(pEnter));
        }

        // Resolve element props and bindings with slot data
        const resolvedProps = Object.assign({}, elem.props || {});
        if (elem.bind) {
          for (const [propKey, slotExpr] of Object.entries(elem.bind)) {
            let resolvedVal = slotExpr;
            if (typeof slotExpr === "string") {
              const exactMatch = slotExpr.match(/^\{\{([a-zA-Z0-9_]+)\}\}$/);
              if (exactMatch) {
                const k = exactMatch[1];
                const rawVal = this.currentSlots[k];
                if (propKey === "value" || propKey === "p" || propKey === "tax") {
                  resolvedVal = (typeof rawVal === "number") ? rawVal : (rawVal !== undefined && !isNaN(Number(rawVal)) ? Number(rawVal) : 0);
                } else if (typeof rawVal === "number") {
                  const slotDef = (this.def.slots || []).find(s => s.key === k);
                  const isCurrency = slotDef && slotDef.format === "inr";
                  resolvedVal = isCurrency ? formatIndianRupee(rawVal) : (rawVal >= 1000 ? formatIndianNumberOnly(rawVal) : String(rawVal));
                } else {
                  resolvedVal = rawVal !== undefined && rawVal !== null ? String(rawVal) : "";
                }
              } else {
                // 1. If prefixed by ₹: format with ₹
                resolvedVal = resolvedVal.replace(/₹\s*\{\{([a-zA-Z0-9_]+)\}\}/g, (_, k) => {
                  const rawVal = this.currentSlots[k];
                  if (rawVal === undefined || rawVal === null) return "";
                  if (typeof rawVal === "number") return formatIndianRupee(rawVal);
                  return `₹ ${rawVal}`;
                });
                // 2. Standard {{slot_name}} replacement
                resolvedVal = resolvedVal.replace(/\{\{([a-zA-Z0-9_]+)\}\}/g, (_, k) => {
                  const rawVal = this.currentSlots[k];
                  if (rawVal === undefined || rawVal === null) return "";
                  const slotDef = (this.def.slots || []).find(s => s.key === k);
                  const isCurrency = slotDef && slotDef.format === "inr";
                  if (typeof rawVal === "number") {
                    if (isCurrency) return formatIndianRupee(rawVal);
                    if (rawVal >= 1000) return formatIndianNumberOnly(rawVal);
                  }
                  return String(rawVal);
                });
                // Check if numeric prop like value or p or tax
                if ((propKey === "value" || propKey === "p" || propKey === "tax") && !isNaN(resolvedVal) && typeof resolvedVal === "string" && resolvedVal.trim() !== "") {
                  resolvedVal = Number(resolvedVal);
                }
              }
            }
            resolvedProps[propKey] = resolvedVal;
          }
        }
        resolvedProps.w = elem.w;
        resolvedProps.h = elem.h;

        // Compute center-anchored transform to prevent diagonal shaking
        const elemW = elem.w !== undefined ? elem.w : 100;
        const elemH = elem.h !== undefined ? elem.h : 60;
        const cx = elemW / 2;
        const cy = elemH / 2;
        const targetX = Math.round((curX + cx * (1 - curScale)) * 100) / 100;
        const targetY = Math.round((curY + cy * (1 - curScale)) * 100) / 100;
        const scaleVal = Math.round(curScale * 1000) / 1000;
        const transformStr = (Math.abs(scaleVal - 1.0) < 0.0005)
          ? `translate(${targetX}, ${targetY})`
          : `translate(${targetX}, ${targetY}) scale(${scaleVal})`;

        const opacityVal = Math.round(curOpacity * 100) / 100;

        // Check if element is already rendered in stageGroup
        if (this.renderedElements && this.renderedElements.has(elem.id)) {
          const entry = this.renderedElements.get(elem.id);
          entry.elGroup.setAttribute("transform", transformStr);
          entry.elGroup.setAttribute("opacity", opacityVal);

          // Update dynamic primitives that animate with progress
          const isDynamic = (elem.type === "counter" || elem.type === "strike" || elem.type === "money_bag" || elem.type === "gate" || elem.type === "ledger_row" || elem.type === "bar" || elem.type === "slab_step");
          if (isDynamic) {
            const renderer = PRIMITIVE_RENDERERS[elem.type];
            if (renderer) {
              const updatedNode = renderer(resolvedProps, this.currentSlots, pMotion || pEnter);
              entry.elGroup.replaceChildren(updatedNode);
            }
          }
        } else {
          // Create container node for this element
          const elGroup = svgEl("g", {
            id: `elem_${elem.id}`,
            class: `anim-element anim-type-${elem.type}${elem.is_container ? " is-container" : ""}${elem.badge_on ? " is-badge" : ""}`,
            "data-elem-id": elem.id,
            "data-badge-on": elem.badge_on || "",
            "data-is-container": elem.is_container ? "true" : "false",
            transform: transformStr,
            opacity: opacityVal
          });

          // Delegate to primitive renderer
          const renderer = PRIMITIVE_RENDERERS[elem.type] || PRIMITIVE_RENDERERS.card;
          const renderedNode = renderer(resolvedProps, this.currentSlots, pMotion || pEnter);
          elGroup.appendChild(renderedNode);

          // Insert into stageGroup preserving scene z-order
          const myIdx = (this.def.scene || []).indexOf(elem);
          let nextSiblingEl = null;
          if (this.def.scene) {
            for (let j = myIdx + 1; j < this.def.scene.length; j++) {
              const nextElem = this.def.scene[j];
              if (this.renderedElements && this.renderedElements.has(nextElem.id)) {
                nextSiblingEl = this.renderedElements.get(nextElem.id).elGroup;
                break;
              }
            }
          }
          if (nextSiblingEl && nextSiblingEl.parentNode === this.stageGroup) {
            this.stageGroup.insertBefore(elGroup, nextSiblingEl);
          } else {
            this.stageGroup.appendChild(elGroup);
          }

          if (!this.renderedElements) this.renderedElements = new Map();
          this.renderedElements.set(elem.id, { elGroup });
        }
      });

      // Remove elements that are no longer active (conditioned out or scrubbed backward)
      if (this.renderedElements) {
        for (const [id, entry] of this.renderedElements.entries()) {
          if (!currentActiveIds.has(id)) {
            if (entry.elGroup && entry.elGroup.parentNode === this.stageGroup) {
              this.stageGroup.removeChild(entry.elGroup);
            }
            this.renderedElements.delete(id);
          }
        }
      }
    }

    setTime(t) {
      this.currentTime = Math.max(0, Math.min(this.duration, Number(t)));
      this.renderCurrentState();
      if (typeof this.onTimeUpdate === "function") {
        this.onTimeUpdate(this.currentTime, this.duration);
      }
    }

    seek(t) {
      this.setTime(t);
    }

    play() {
      if (this.isPlaying) return;
      if (this.currentTime >= this.duration) this.currentTime = 0.0;
      this.isPlaying = true;
      this.lastTimestamp = null;
      this.loop = (now) => {
        if (!this.isPlaying) return;
        if (!this.lastTimestamp) this.lastTimestamp = now;
        const deltaSec = (now - this.lastTimestamp) / 1000.0;
        this.lastTimestamp = now;

        const nextT = this.currentTime + deltaSec * this.speed;
        if (nextT >= this.duration) {
          this.setTime(this.duration);
          this.pause();
        } else {
          this.setTime(nextT);
          this.rafId = requestAnimationFrame(this.loop);
        }
      };
      this.rafId = requestAnimationFrame(this.loop);
    }

    pause() {
      this.isPlaying = false;
      if (this.rafId) {
        cancelAnimationFrame(this.rafId);
        this.rafId = null;
      }
      if (typeof this.onPause === "function") {
        this.onPause();
      }
    }

    setSpeed(s) {
      this.speed = Math.max(0.1, Math.min(5.0, Number(s)));
    }

    setTheme(th) {
      this.theme = th;
      this.container.setAttribute("data-theme", th);
    }

    setSlots(obj) {
      this.updateSlots(obj);
    }

    setTimingMap(obj) {
      this.timingMap = Object.assign({}, obj);
      this.updateSlots(this.currentSlots);
    }

    getCues() {
      return (this.def.cues || []).map(c => ({
        id: c.id,
        label: c.label,
        default_t: c.default_t,
        current_t: this.effectiveCues[c.id] !== undefined ? this.effectiveCues[c.id] : c.default_t
      }));
    }

    destroy() {
      this.pause();
      if (this.renderedElements) {
        this.renderedElements.clear();
        this.renderedElements = null;
      }
      this.container.innerHTML = "";
      this.svg = null;
      this.stageGroup = null;
      this.currentSlots = null;
    }
  }

  // Global Factory API
  global.Anim = {
    create: (container, def, slots, options) => {
      return new AnimationInstance(container, def, slots, options);
    },
    formatINR: formatIndianRupee,
    evaluateExpr: evaluateExpr
  };

})(typeof window !== "undefined" ? window : global);
