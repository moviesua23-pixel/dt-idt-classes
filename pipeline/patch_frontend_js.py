"""
pipeline/patch_frontend_js.py
Updates renderMindMapCanvasHtml, updateConnectorPaths, getState, syncMindMap, handleAutoScroll, and highlightKeywords
in frontend/index.html.
"""

import os
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(PROJECT_ROOT, "frontend", "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update highlightKeywords
old_hl_pattern = re.compile(r'function highlightKeywords\(text,\s*hl\)\s*\{.*?return clean;\s*\}', re.DOTALL)
new_hl = """function highlightKeywords(text, hl){
  if(!text) return "";
  let clean = esc(String(text));

  // 1. Amounts: ₹ 2,50,000, ₹ 1 Crore, etc.
  clean = clean.replace(/(₹\\s*[\\d,]+(?:\\.\\d+)?(?:\\s*(?:Lakhs?|Crores?|L|Cr|lacs?))?)/gi, '<span class="chip-amt">$1</span>');
  
  // 2. Percentages: 5%, 20%, 30%, 32.1%, etc.
  clean = clean.replace(/(\\b\\d+(?:\\.\\d+)?%)/g, '<span class="chip-rate">$1</span>');
  
  // 3. Statutory Sections: Section 115BAC, u/s 87A, § 4, etc.
  clean = clean.replace(/((?:Section|u\\/s|§)\\s*[0-9A-Za-z()]+(?:\\([0-9A-Za-z]+\\))?)/gi, '<span class="chip-sec">$1</span>');

  return clean;
}"""

if old_hl_pattern.search(content):
    content = old_hl_pattern.sub(lambda m: new_hl, content)
    print("[OK] Replaced highlightKeywords")
else:
    print("[WARN] highlightKeywords pattern not matched")

# 2. Update renderMindMapCanvasHtml
old_render_canvas_pattern = re.compile(r'function renderMindMapCanvasHtml\(mm,\s*q,\s*p\)\s*\{.*?return `\s*<div class="mm-scroll-stage".*?`;\s*\}', re.DOTALL)

new_render_canvas = """function renderMindMapCanvasHtml(mm, q, p){
  if (!mm || !mm.branches || mm.branches.length === 0) {
    return `
      <div class="mm-canvas-container" style="display:grid;place-items:center;min-height:360px">
        <div style="text-align:center;color:#64748B">
          <h4 style="color:#0F172A;margin-bottom:6px">Mind Map Not Available for This Topic</h4>
          <p style="font-size:.85rem">Please switch to <b>Slide Detail</b> view to study this provision.</p>
        </div>
      </div>
    `;
  }

  const root = mm.root || { id: "root", title: p.doctrine, badge: "§ LAW" };

  return `
    <div class="mm-scroll-stage" id="mm-scroll-stage">
      <div class="mm-canvas-container" id="mm-canvas-container">
        <svg class="mm-connector-svg" id="mm-connector-svg" aria-hidden="true">
          <defs>
            <marker id="arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#12A150" />
            </marker>
            <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#E8590C" />
            </marker>
            <marker id="arrow-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#7048E8" />
            </marker>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#1C7ED6" />
            </marker>
            <marker id="arrow-teal" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0CA678" />
            </marker>
            <marker id="arrow-trap" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#FA5252" />
            </marker>
          </defs>
        </svg>

        <!-- Minimalist Root Card: Section Code Badge + Doctrine in One Line -->
        <div class="mm-root-card" id="mm-node-root" data-node-id="root" data-t0="0" data-t1="${root.t1 || 5.0}" tabindex="0" role="button" aria-label="Jump to start: ${esc(root.title)}">
          <div class="mm-root-top-row">
            <span class="mm-root-badge">${esc(root.badge || '§ LAW')}</span>
            <span class="mm-root-step-tag">CORE STATUTORY DOCTRINE</span>
          </div>
          <div class="mm-root-title">${esc(root.title)}</div>
        </div>

        <!-- Sequential Infographic Blocks Downward (B1 -> B2 -> B3 -> B4) -->
        ${mm.branches.map((b, bi) => `
          <div class="mm-infographic-block status-hidden" id="mm-block-${b.branch_id}" data-branch-id="${b.branch_id}" data-t0="${b.t0}" data-t1="${b.t1}">
            <!-- 1. Section Title Pill (Dark Navy, White Text, Section Badge) -->
            <div class="mm-block-pill" id="mm-bpill-${b.branch_id}" data-t0="${b.t0}" data-branch-id="${b.branch_id}" tabindex="0" role="button" aria-label="Jump to ${esc(b.branch_title)}">
              <div class="mm-bp-icon-badge">${getIconSvg(b.icon || 'scales', 18, '#60A5FA')}</div>
              <span class="mm-bp-step">BLOCK ${bi + 1}</span>
              <span class="mm-bp-title" title="${esc(b.branch_title)}">${esc(b.branch_title)}</span>
              ${b.badge ? `<span class="mm-bp-badge">${esc(b.badge)}</span>` : ''}
              <div class="mm-bp-underline"></div>
            </div>

            <!-- 2. Point Cards Grid: 3 per row (2 on tablet, 1 on phone) -->
            <div class="mm-cards-row" id="mm-cards-${b.branch_id}">
              ${(b.points || []).map((pt, pi) => {
                const isFull = !!(pt.table_data || pt.example_calc);
                let theme = 'theme-blue';
                if (pt.trap_data) theme = 'theme-trap';
                else if (pt.table_data) theme = 'theme-blue';
                else if (pt.example_calc) theme = 'theme-green';
                else {
                  const palette = ['theme-green', 'theme-orange', 'theme-purple', 'theme-blue', 'theme-teal'];
                  theme = palette[pi % palette.length];
                }
                const isSpk = pt.spoken === true;
                return `
                  <div class="mm-infographic-card ${theme} ${isFull ? 'card-fullwidth' : ''} status-hidden" id="mm-card-${pt.id}" data-point-id="${pt.id}" data-branch-id="${b.branch_id}" data-t0="${pt.t0 != null ? pt.t0 : ''}" data-t1="${pt.t1 != null ? pt.t1 : ''}" data-spoken="${isSpk}" tabindex="0" role="button" aria-label="${esc(pt.title)}">
                    <!-- 56px Circular White Icon Badge overlapping top-left corner -->
                    <div class="mm-card-icon-badge">
                      ${getIconSvg(pt.icon || 'check', 24)}
                    </div>

                    <!-- Separate Status Strip at Top Right -->
                    <span class="mm-card-live-strip" id="tag-pt-${pt.id}"></span>

                    <!-- Coloured Header Pill with Card Title (Wraps to 2 lines, NEVER truncated) -->
                    <div class="mm-card-ribbon">
                      <span class="mm-card-title">${esc(pt.title)}</span>
                    </div>

                    <!-- Card Body: 17-18px dark text (#1B2A41), line-height 1.5 -->
                    <div class="mm-card-body">
                      ${renderCardBodyContent(pt)}
                    </div>
                  </div>
                `;
              }).join('')}
            </div>

            <!-- 3. Converging Connectors SVG -->
            <div class="mm-converge-container" id="mm-conv-wrap-${b.branch_id}">
              <svg class="mm-converge-svg" id="mm-converge-${b.branch_id}" aria-hidden="true"></svg>
            </div>

            <!-- 4. Flow Summary Pill & Flow Steps Row -->
            <div class="mm-flow-pill status-flow-hidden" id="mm-fpill-${b.branch_id}" data-branch-id="${b.branch_id}" tabindex="0" role="button" aria-label="Statutory Flow Summary">
              ${getIconSvg('gear', 16, '#FFFFFF')}
              <span>STATUTORY COMPUTATION FLOW</span>
            </div>

            <div class="mm-flow-steps-row" id="mm-fsteps-${b.branch_id}">
              ${(b.flow_summary || []).map((step, si) => `
                ${si > 0 ? `<div class="mm-fs-arrow">${getIconSvg('arrow_right', 16, '#94A3B8')}</div>` : ''}
                <div class="mm-flow-step-box status-hidden" id="mm-fstep-${b.branch_id}-${si}" data-t0="${step.t0}" data-t1="${step.t1}" data-branch-id="${b.branch_id}" tabindex="0" role="button" aria-label="Step ${si + 1}: ${esc(step.label)}">
                  <div class="mm-fs-top">
                    <span class="mm-fs-icon">${getIconSvg(step.icon || 'check', 14)}</span>
                    <span class="mm-fs-num">Step ${si + 1}</span>
                  </div>
                  <div class="mm-fs-label">${esc(step.label)}</div>
                  ${step.sub ? `<div class="mm-fs-sub">${esc(step.sub)}</div>` : ''}
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Subtitle Bar (Pinned directly above dock, showing exact source sentence) -->
    <div class="mm-live-bar" id="mm-live-bar">
      <span class="mm-live-badge"><span class="pnb-live-dot"></span>EXPLAINING NOW</span>
      <span class="mm-live-text" id="mm-live-text">Tap Play to start animated Malayalam explanation</span>
    </div>
  `;
}"""

if old_render_canvas_pattern.search(content):
    content = old_render_canvas_pattern.sub(lambda m: new_render_canvas, content)
    print("[OK] Replaced renderMindMapCanvasHtml")
else:
    print("[WARN] renderMindMapCanvasHtml pattern not matched")

# 3. Update getState, handleAutoScroll, updateConnectorPaths, syncMindMap
old_engine_pattern = re.compile(r'function getState\(mindmap,\s*cur\)\s*\{.*?function syncMindMap\(cur\)\s*\{.*?\}\s*\}', re.DOTALL)

new_engine = """function getState(mindmap, cur){
  if(!mindmap || !mindmap.branches) return { branchStates: {}, pointStates: {}, flowStates: {}, convergeStates: {}, cardConnectors: {}, activePoint: null, activeFlowStep: null, activeBranch: null, allMastered: false };
  const branchStates = {};
  const pointStates = {};
  const flowStates = {};
  const convergeStates = {};
  const cardConnectors = {};
  let activePoint = null;
  let activeFlowStep = null;
  let activeBranch = null;
  const tot = mindmap.total_duration || total();
  const allMastered = cur >= tot;

  mindmap.branches.forEach((b) => {
    let status = "hidden";
    let progress = 0;
    const t0 = parseFloat(b.t0 || 0);
    const t1 = parseFloat(b.t1 || 999);

    if(cur >= t1){
      status = "mastered";
      progress = 1;
    } else if(cur >= t0){
      activeBranch = b;
      const elapsed = cur - t0;
      const DRAW_TIME = 0.8;
      if(elapsed < DRAW_TIME){
        status = "drawing";
        progress = Math.min(1, Math.max(0, elapsed / DRAW_TIME));
      } else {
        status = "active";
        progress = 1;
      }
    } else {
      status = "hidden";
      progress = 0;
    }
    branchStates[b.branch_id] = { status, progress, t0, t1 };

    // Find last spoken beat t1 for reference cards
    const spkPts = (b.points || []).filter(p => p.spoken === true);
    const lastSpkT1 = spkPts.length > 0 ? parseFloat(spkPts[spkPts.length - 1].t1 || b.t1) : b.t1;

    // Points / Cards
    (b.points || []).forEach(pt => {
      if(pt.spoken === true){
        const pt0 = parseFloat(pt.t0 != null ? pt.t0 : t0);
        const pt1 = parseFloat(pt.t1 != null ? pt.t1 : t1);
        let pStatus = "hidden";
        let connProg = 0;
        const ptDur = pt1 - pt0;
        const connDur = Math.min(0.8, Math.max(0.25, ptDur * 0.25));

        if(cur >= pt1){
          pStatus = "done";
          connProg = 1;
        } else if(cur >= pt0){
          pStatus = "active";
          activePoint = pt;
          activeBranch = b;
          connProg = Math.min(1, Math.max(0, (cur - pt0) / connDur));
        } else {
          pStatus = "hidden";
          connProg = 0;
        }
        pointStates[pt.id] = pStatus;
        cardConnectors[pt.id] = { status: pStatus, progress: connProg };
      } else {
        // Reference cards reveal immediately after last spoken beat of that branch
        if(cur >= lastSpkT1){
          pointStates[pt.id] = "reference";
          cardConnectors[pt.id] = { status: "reference", progress: 1 };
        } else {
          pointStates[pt.id] = "hidden";
          cardConnectors[pt.id] = { status: "hidden", progress: 0 };
        }
      }
    });

    // Flow Summary steps
    let anyFlowActive = false;
    let allFlowDone = (b.flow_summary && b.flow_summary.length > 0);
    (b.flow_summary || []).forEach((step, si) => {
      const st0 = parseFloat(step.t0 || 0);
      const st1 = parseFloat(step.t1 || 999);
      let fStatus = "hidden";
      if(cur >= st1){
        fStatus = "done";
      } else if(cur >= st0){
        fStatus = "active";
        anyFlowActive = true;
        activeFlowStep = { branch_id: b.branch_id, step, index: si, t0: st0 };
        activeBranch = b;
        allFlowDone = false;
      } else {
        fStatus = "hidden";
        allFlowDone = false;
      }
      flowStates[b.branch_id + '_' + si] = fStatus;
    });

    // Converging connectors state
    if(allFlowDone || status === "mastered"){
      convergeStates[b.branch_id] = "done";
    } else if(anyFlowActive || (b.flow_summary && b.flow_summary.length > 0 && cur >= parseFloat(b.flow_summary[0].t0 || 0))){
      convergeStates[b.branch_id] = "active";
    } else {
      convergeStates[b.branch_id] = "hidden";
    }
  });

  return { branchStates, pointStates, flowStates, convergeStates, cardConnectors, activePoint, activeFlowStep, activeBranch, allMastered };
}

let lastActiveBranchId = null;
let lastActivePointId = null;
let lastActiveFlowStepKey = null;
let userScrolledUntil = 0;

function scrollToCard(el, smooth = true){
  const stage = document.getElementById("mm-scroll-stage");
  if(!stage || !el) return;
  const stageRect = stage.getBoundingClientRect();
  const elRect = el.getBoundingClientRect();
  
  // Visible area: viewport height minus top bar (64px) and bottom dock+subtitle bar (120px)
  const topBarH = 64;
  const bottomBarH = 120;
  const visibleH = window.innerHeight - topBarH - bottomBarH;
  
  let targetY;
  if(elRect.height > visibleH){
    // If card is taller than visible area, align top 80px below top bar
    targetY = stage.scrollTop + (elRect.top - topBarH) - 16;
  } else {
    // Center card in visible area
    const visibleCenter = topBarH + (visibleH / 2);
    const elCenter = elRect.top + (elRect.height / 2);
    targetY = stage.scrollTop + (elCenter - visibleCenter);
  }
  stage.scrollTo({ top: Math.max(0, targetY), behavior: smooth ? 'smooth' : 'auto' });
}

function handleAutoScroll(activeBranchId, isManualScrub = false, activePointId = null, activeFlowStepKey = null){
  const stage = document.getElementById("mm-scroll-stage");
  if(!stage) return;
  const now = Date.now();

  if(isManualScrub){
    lastActiveBranchId = activeBranchId;
    lastActivePointId = activePointId;
    lastActiveFlowStepKey = activeFlowStepKey;
    userScrolledUntil = 0;
    if(activePointId){
      const pEl = document.getElementById("mm-card-" + activePointId);
      if(pEl){ scrollToCard(pEl, false); return; }
    }
    if(activeFlowStepKey){
      const fEl = document.getElementById("mm-fstep-" + activeFlowStepKey);
      if(fEl){ scrollToCard(fEl, false); return; }
    }
    if(activeBranchId === "root" || (audio.currentTime || 0) < 0.8){
      const rootEl = document.getElementById("mm-node-root");
      if(rootEl) scrollToCard(rootEl, false);
      else stage.scrollTop = 0;
    } else if(activeBranchId){
      const el = document.getElementById("mm-block-" + activeBranchId);
      if(el) scrollToCard(el, false);
    }
    return;
  }

  // Auto-scroll to active flow step
  if(now >= userScrolledUntil && activeFlowStepKey && activeFlowStepKey !== lastActiveFlowStepKey){
    lastActiveFlowStepKey = activeFlowStepKey;
    const fEl = document.getElementById("mm-fstep-" + activeFlowStepKey);
    if(fEl){
      scrollToCard(fEl, true);
      return;
    }
  }

  // Auto-scroll to active spoken point card
  if(now >= userScrolledUntil && activePointId && activePointId !== lastActivePointId){
    lastActivePointId = activePointId;
    const pEl = document.getElementById("mm-card-" + activePointId);
    if(pEl){
      scrollToCard(pEl, true);
      return;
    }
  }

  // Active branch transition
  if(activeBranchId !== lastActiveBranchId){
    lastActiveBranchId = activeBranchId;
    userScrolledUntil = 0;
    if(activeBranchId === "root"){
      const rootEl = document.getElementById("mm-node-root");
      if(rootEl) scrollToCard(rootEl, true);
      else stage.scrollTo({ top: 0, behavior: 'smooth' });
    } else if(activeBranchId){
      const el = document.getElementById("mm-block-" + activeBranchId);
      if(el) scrollToCard(el, true);
    }
    return;
  }

  if(now < userScrolledUntil) return;
}

function refreshMindMapLayout(){
  if(vtheater && vtheater.classList.contains("open")){
    updateConnectorPaths(getState(mm, audio.currentTime || 0));
  }
}

function updateConnectorPaths(st){
  if(!mm || !mm.branches) return;
  const svg = document.getElementById("mm-connector-svg");
  const container = document.getElementById("mm-canvas-container");
  const rootCard = document.getElementById("mm-node-root");
  if(!svg || !container || !rootCard) return;

  const cRect = container.getBoundingClientRect();
  let prevRect = rootCard.getBoundingClientRect();

  // 1. Inter-Block Connectors (Root -> B1 -> B2 -> B3 -> B4)
  mm.branches.forEach((b, bi) => {
    const bEl = document.getElementById("mm-bpill-" + b.branch_id);
    const blockEl = document.getElementById("mm-block-" + b.branch_id);
    if(!bEl || !blockEl) return;
    const currRect = bEl.getBoundingClientRect();

    const x0 = prevRect.left - cRect.left + prevRect.width / 2;
    const y0 = prevRect.bottom - cRect.top;
    const x1 = currRect.left - cRect.left + currRect.width / 2;
    const y1 = currRect.top - cRect.top;

    let path = document.getElementById("mm-path-" + b.branch_id);
    if(!path){
      path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.id = "mm-path-" + b.branch_id;
      path.classList.add("mm-branch-path");
      svg.appendChild(path);
    }

    const dy = y1 - y0;
    const cpOffset = (bi % 2 === 0 ? 10 : -10);
    const cp1x = x0 + cpOffset;
    const cp1y = y0 + dy * 0.45;
    const cp2x = x1 - cpOffset;
    const cp2y = y1 - dy * 0.45;
    const d = `M ${x0.toFixed(1)} ${y0.toFixed(1)} C ${cp1x.toFixed(1)} ${cp1y.toFixed(1)}, ${cp2x.toFixed(1)} ${cp2y.toFixed(1)}, ${x1.toFixed(1)} ${y1.toFixed(1)}`;

    if(path.getAttribute("d") !== d){
      path.setAttribute("d", d);
    }

    const bState = (st && st.branchStates && st.branchStates[b.branch_id]) || { status: "hidden", progress: 0 };
    let len = 0;
    try { len = path.getTotalLength() || 100; } catch(e){ len = 100; }

    path.style.strokeDasharray = len.toFixed(1);
    const offset = len * (1 - Math.min(1, Math.max(0, bState.progress)));
    path.style.strokeDashoffset = offset.toFixed(1);
    path.className.baseVal = `mm-branch-path path-${bState.status}`;

    // Step badge in the vertical gap
    const midX = (x0 + x1) / 2;
    const midY = (y0 + y1) / 2;
    let badgeGroup = document.getElementById("mm-badge-" + b.branch_id);
    if(!badgeGroup){
      badgeGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      badgeGroup.id = "mm-badge-" + b.branch_id;
      badgeGroup.innerHTML = `
        <circle class="mm-badge-bg" r="13" />
        <text class="mm-badge-text" text-anchor="middle" dy="4">${bi + 1}</text>
      `;
      svg.appendChild(badgeGroup);
    }
    badgeGroup.setAttribute("transform", `translate(${midX.toFixed(1)}, ${midY.toFixed(1)})`);
    badgeGroup.className.baseVal = `mm-step-badge-group badge-${bState.status}`;

    // 2. Individual Curved Connectors from Block Pill to Card Top
    (b.points || []).forEach((pt, pi) => {
      const cEl = document.getElementById("mm-card-" + pt.id);
      if(!cEl) return;
      const cardRect = cEl.getBoundingClientRect();
      const px0 = currRect.left - cRect.left + currRect.width / 2;
      const py0 = currRect.bottom - cRect.top;
      const px1 = cardRect.left - cRect.left + cardRect.width / 2;
      const py1 = cardRect.top - cRect.top;

      let cardPath = document.getElementById("mm-cpath-to-" + pt.id);
      if(!cardPath){
        cardPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
        cardPath.id = "mm-cpath-to-" + pt.id;
        cardPath.classList.add("mm-card-path");
        svg.appendChild(cardPath);
      }

      const pdy = py1 - py0;
      const cd = `M ${px0.toFixed(1)} ${py0.toFixed(1)} C ${px0.toFixed(1)} ${(py0 + pdy * 0.45).toFixed(1)}, ${px1.toFixed(1)} ${(py1 - pdy * 0.45).toFixed(1)}, ${px1.toFixed(1)} ${py1.toFixed(1)}`;
      if(cardPath.getAttribute("d") !== cd){
        cardPath.setAttribute("d", cd);
      }

      const connData = (st && st.cardConnectors && st.cardConnectors[pt.id]) || { status: "hidden", progress: 0 };
      let cLen = 0;
      try { cLen = cardPath.getTotalLength() || 80; } catch(e){ cLen = 80; }

      cardPath.style.strokeDasharray = cLen.toFixed(1);
      const cOffset = cLen * (1 - Math.min(1, Math.max(0, connData.progress)));
      cardPath.style.strokeDashoffset = cOffset.toFixed(1);

      // Color mapping
      let markerColor = "blue";
      let strokeColor = "#1C7ED6";
      if(pt.trap_data){ markerColor = "trap"; strokeColor = "#FA5252"; }
      else if(pt.table_data){ markerColor = "blue"; strokeColor = "#1C7ED6"; }
      else if(pt.example_calc){ markerColor = "green"; strokeColor = "#12A150"; }
      else {
        const pal = [
          { m: "green", s: "#12A150" },
          { m: "orange", s: "#E8590C" },
          { m: "purple", s: "#7048E8" },
          { m: "blue", s: "#1C7ED6" },
          { m: "teal", s: "#0CA678" }
        ];
        const item = pal[pi % pal.length];
        markerColor = item.m;
        strokeColor = item.s;
      }

      cardPath.style.stroke = strokeColor;
      cardPath.setAttribute("marker-end", `url(#arrow-${markerColor})`);
      cardPath.className.baseVal = `mm-card-path path-${connData.status}`;
    });

    // Chain from bottom of this block's flow steps to the next block
    const fstepsEl = document.getElementById("mm-fsteps-" + b.branch_id);
    prevRect = fstepsEl ? fstepsEl.getBoundingClientRect() : blockEl.getBoundingClientRect();

    // 3. Converging Connectors inside this block (Cards -> Flow Summary Pill)
    const convSvg = document.getElementById("mm-converge-" + b.branch_id);
    const convWrap = document.getElementById("mm-conv-wrap-" + b.branch_id);
    const flowPill = document.getElementById("mm-fpill-" + b.branch_id);
    if(convSvg && convWrap && flowPill){
      const wRect = convWrap.getBoundingClientRect();
      const fRect = flowPill.getBoundingClientRect();
      const fx = fRect.left - wRect.left + fRect.width / 2;
      const fy = 44;

      (b.points || []).forEach(pt => {
        const cEl = document.getElementById("mm-card-" + pt.id);
        if(!cEl) return;
        const cardRect = cEl.getBoundingClientRect();
        const cx = cardRect.left - wRect.left + cardRect.width / 2;
        const cy = 0;

        let cPath = document.getElementById("mm-cpath-" + pt.id);
        if(!cPath){
          cPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
          cPath.id = "mm-cpath-" + pt.id;
          cPath.classList.add("mm-converge-path");
          convSvg.appendChild(cPath);
        }

        const cd = `M ${cx.toFixed(1)} ${cy.toFixed(1)} C ${cx.toFixed(1)} ${(fy * 0.5).toFixed(1)}, ${fx.toFixed(1)} ${(fy * 0.5).toFixed(1)}, ${fx.toFixed(1)} ${fy.toFixed(1)}`;
        if(cPath.getAttribute("d") !== cd){
          cPath.setAttribute("d", cd);
        }
        const convStatus = (st && st.convergeStates && st.convergeStates[b.branch_id]) || "hidden";
        cPath.className.baseVal = `mm-converge-path path-${convStatus}`;
      });
    }
  });
}

function syncMindMap(cur){
  if(!mm) return;
  const st = getState(mm, cur);

  // Update Infographic Blocks
  mm.branches.forEach(b => {
    const blockEl = document.getElementById("mm-block-" + b.branch_id);
    const bState = st.branchStates[b.branch_id] || { status: "hidden" };

    if(blockEl){
      blockEl.className = `mm-infographic-block status-${bState.status}`;
    }

    // Update Cards
    (b.points || []).forEach((pt, pi) => {
      const cardEl = document.getElementById("mm-card-" + pt.id);
      const cTagEl = document.getElementById("tag-pt-" + pt.id);
      if(cardEl){
        const pStatus = st.pointStates[pt.id] || "hidden";
        const isFull = !!(pt.table_data || pt.example_calc);
        let theme = 'theme-blue';
        if (pt.trap_data) theme = 'theme-trap';
        else if (pt.table_data) theme = 'theme-blue';
        else if (pt.example_calc) theme = 'theme-green';
        else {
          const pal = ['theme-green', 'theme-orange', 'theme-purple', 'theme-blue', 'theme-teal'];
          theme = pal[pi % pal.length];
        }

        cardEl.className = `mm-infographic-card ${theme} ${isFull ? 'card-fullwidth' : ''} status-${pStatus}`;
        if(cTagEl){
          if(pStatus === "active"){
            cTagEl.textContent = "● EXPLAINING NOW";
            cTagEl.className = "mm-card-live-strip tag-active";
          } else if(pStatus === "done"){
            cTagEl.textContent = "✓ Done";
            cTagEl.className = "mm-card-live-strip tag-done";
          } else if(pStatus === "reference"){
            cTagEl.textContent = "Reference";
            cTagEl.className = "mm-card-live-strip tag-ref";
          } else {
            cTagEl.textContent = "";
            cTagEl.className = "mm-card-live-strip";
          }
        }
      }
    });

    // Update Flow Summary Pill & Steps
    const flowPill = document.getElementById("mm-fpill-" + b.branch_id);
    if(flowPill){
      const cState = st.convergeStates[b.branch_id] || "hidden";
      flowPill.className = `mm-flow-pill status-flow-${cState}`;
    }

    (b.flow_summary || []).forEach((step, si) => {
      const stepEl = document.getElementById("mm-fstep-" + b.branch_id + "-" + si);
      if(stepEl){
        const fStatus = st.flowStates[b.branch_id + '_' + si] || "hidden";
        stepEl.className = `mm-flow-step-box status-${fStatus}`;
      }
    });
  });

  // Update connector paths
  updateConnectorPaths(st);

  // Auto-scroll view smoothly to active card or flow step
  const activeBranchId = st.activeBranch ? st.activeBranch.branch_id : (cur < 1.0 ? "root" : (st.allMastered ? mm.branches[mm.branches.length - 1].branch_id : null));
  const activePointId = st.activePoint ? st.activePoint.id : null;
  const activeFlowStepKey = st.activeFlowStep ? (st.activeFlowStep.branch_id + '-' + st.activeFlowStep.index) : null;
  handleAutoScroll(activeBranchId, false, activePointId, activeFlowStepKey);

  // Update Explaining Now Live Bar (shows exact Malayalam narration sentence)
  const liveText = $("#mm-live-text");
  if(liveText){
    if(st.activePoint && st.activePoint.voice_sync_text){
      liveText.textContent = st.activePoint.voice_sync_text;
    } else if(st.activeFlowStep && st.activeFlowStep.step){
      liveText.textContent = `Flow Step ${st.activeFlowStep.index + 1}: ${st.activeFlowStep.step.label} (${st.activeFlowStep.step.sub || ''})`;
    } else if(st.activeBranch && st.activeBranch.branch_title){
      liveText.textContent = `Explaining: ${st.activeBranch.branch_title}`;
    } else if(st.allMastered){
      liveText.textContent = "✓ Complete Concept Tree Mastered!";
    } else {
      liveText.textContent = `§ ${esc(mm.doctrine || '')} · Spoken Malayalam Teacher Audio`;
    }
  }

  // Update Dock Label
  const vtdLabel = $("#vtd-label");
  if(vtdLabel){
    if(st.activePoint){
      vtdLabel.textContent = `${st.activeBranch ? st.activeBranch.branch_title + ' · ' : ''}${st.activePoint.title}`;
    } else if(st.activeFlowStep && st.activeFlowStep.step){
      vtdLabel.textContent = `${st.activeBranch ? st.activeBranch.branch_title + ' · ' : ''}Step: ${st.activeFlowStep.step.label}`;
    } else if(st.activeBranch){
      vtdLabel.textContent = st.activeBranch.branch_title;
    } else if(st.allMastered){
      vtdLabel.textContent = "✓ Concept Tree Complete";
    } else {
      vtdLabel.textContent = `§ ${mm.root?.badge || "Direct Tax"}`;
    }
  }
}"""

if old_engine_pattern.search(content):
    content = old_engine_pattern.sub(lambda m: new_engine, content)
    print("[OK] Replaced getState, handleAutoScroll, updateConnectorPaths, syncMindMap")
else:
    print("[WARN] Engine pattern not matched")

# Also add user scroll listener on mm-scroll-stage
old_attach_listeners = "const stageEl = document.getElementById('mm-scroll-stage');"
if "mm-scroll-stage" in content and "userScrolledUntil = Date.now() + 4000" not in content:
    scroll_listener_patch = """
    const scrollStageEl = document.getElementById('mm-scroll-stage');
    if(scrollStageEl){
      scrollStageEl.addEventListener('scroll', () => {
        userScrolledUntil = Date.now() + 4000;
      }, { passive: true });
    }
    """
    content = content.replace("requestAnimationFrame(refreshMindMapLayout);", scroll_listener_patch + "\n    requestAnimationFrame(refreshMindMapLayout);", 1)
    print("[OK] Attached 4s user scroll suppression listener")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Finished patching JavaScript in index.html")
