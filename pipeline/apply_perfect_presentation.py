import os

FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")

with open(FRONTEND_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# =========================================================================
# 1. Update CSS
# =========================================================================
css_start = "/* ===== PowerPoint Explainer Theater & Morphing Deck ===== */"
css_end = "@media (max-width:860px){"
idx_css1 = text.find(css_start)
idx_css2 = text.find(css_end, idx_css1)

if idx_css1 == -1 or idx_css2 == -1:
    print("ERROR: CSS markers not found")
    exit(1)

new_css = """/* ===== PowerPoint Explainer Theater & Morphing Deck ===== */
.vtheater{
  display:none !important;
  position:fixed !important;
  inset:0 !important;
  width:100vw !important;
  height:100vh !important;
  z-index:99999999 !important;
  background:#070B14 !important;
  flex-direction:column !important;
  overflow:hidden !important;
  margin:0 !important;
  border:0 !important;
  border-radius:0 !important;
  box-shadow:none !important;
}
.vtheater.open{
  display:flex !important;
  animation:theaterFadeIn .25s cubic-bezier(.16,1,.3,1);
}
@keyframes theaterFadeIn{
  from{opacity:0;transform:scale(0.99)}
  to{opacity:1;transform:scale(1)}
}

.vtheater-topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 32px;
  background:rgba(15,23,42,0.95);
  backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.08);
  gap:18px;
  flex-shrink:0;
  z-index:50;
}
.vtb-left{
  display:flex;
  align-items:center;
  gap:12px;
  min-width:0;
  flex-shrink:1;
}
.vtb-badge{
  font-family:var(--f-mono);
  font-size:.74rem;
  background:rgba(37,99,235,0.18);
  color:#93C5FD;
  border:1px solid rgba(59,130,246,0.4);
  padding:4px 12px;
  border-radius:999px;
  font-weight:700;
  white-space:nowrap;
  flex-shrink:0;
  letter-spacing:.04em;
}
.vtb-title{
  font-size:1.02rem;
  font-weight:700;
  color:#F8FAFC;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  max-width:340px;
}
.vtb-center{
  display:flex;
  align-items:center;
  justify-content:center;
  flex:1;
  min-width:0;
}
.vtb-right{
  display:flex;
  align-items:center;
  gap:12px;
  flex-shrink:0;
}
.vtb-close-btn{
  display:inline-flex;
  align-items:center;
  gap:8px;
  color:#FFFFFF;
  background:#EF4444;
  border:1.5px solid #F87171;
  padding:8px 20px;
  border-radius:10px;
  font-size:.86rem;
  font-weight:700;
  cursor:pointer;
  transition:all .2s cubic-bezier(.16,1,.3,1);
  box-shadow:0 4px 14px rgba(239,68,68,0.35);
}
.vtb-close-btn:hover{
  background:#DC2626;
  border-color:#EF4444;
  transform:scale(1.03);
  box-shadow:0 6px 20px rgba(239,68,68,0.5);
}
.vtb-close-btn:active{
  transform:scale(0.97);
}

.ppt-nav-rail{
  display:inline-flex;
  align-items:center;
  gap:6px;
  background:rgba(30,41,59,0.7);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:999px;
  padding:4px;
  max-width:640px;
  overflow-x:auto;
  scrollbar-width:none;
}
.ppt-nav-rail::-webkit-scrollbar{display:none;}
.ppt-nav-dot{
  display:inline-flex;
  align-items:center;
  gap:8px;
  background:transparent;
  border:0;
  border-radius:999px;
  padding:6px 14px;
  cursor:pointer;
  color:#94A3B8;
  font-size:.78rem;
  font-weight:600;
  white-space:nowrap;
  transition:all .2s;
  flex-shrink:0;
}
.ppt-nav-dot:hover{
  background:rgba(255,255,255,0.08);
  color:#FFFFFF;
}
.ppt-nav-dot.active{
  background:#2563EB;
  color:#FFFFFF;
  font-weight:700;
  box-shadow:0 0 16px rgba(37,99,235,0.5);
  transform:translateY(-1px);
}
.ppt-dot-num{
  width:18px;
  height:18px;
  border-radius:50%;
  background:rgba(255,255,255,0.12);
  display:grid;
  place-items:center;
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
}
.ppt-nav-dot.active .ppt-dot-num{
  background:#FFFFFF;
  color:#1D4ED8;
}
.ppt-dot-label{
  max-width:130px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  display:inline-block;
}

.vfullscreen-stage{
  flex:1;
  overflow-y:auto;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px 24px 84px;
  background:radial-gradient(ellipse at 50% 20%, #172554 0%, #0B1120 55%, #050811 100%);
  box-sizing:border-box;
  position:relative;
}

.ppt-stage-wrapper{
  display:flex;
  align-items:center;
  justify-content:center;
  width:100%;
  max-width:1360px;
  gap:18px;
  position:relative;
}

.ppt-arrow-btn{
  width:46px;
  height:46px;
  border-radius:50%;
  background:rgba(30,41,59,0.7);
  border:1px solid rgba(255,255,255,0.12);
  color:#E2E8F0;
  display:grid;
  place-items:center;
  cursor:pointer;
  backdrop-filter:blur(12px);
  transition:all .2s cubic-bezier(.16,1,.3,1);
  box-shadow:0 8px 24px rgba(0,0,0,0.3);
  flex-shrink:0;
  z-index:10;
}
.ppt-arrow-btn:hover{
  background:#2563EB;
  border-color:#60A5FA;
  color:#FFFFFF;
  transform:scale(1.12);
  box-shadow:0 0 20px rgba(37,99,235,0.5);
}
.ppt-arrow-btn:active{
  transform:scale(0.95);
}

.ppt-presentation{
  display:flex;
  flex-direction:column;
  align-items:center;
  width:100%;
  max-width:1180px;
  margin:0 auto;
}

.ppt-viewport{
  position:relative;
  width:100%;
  max-width:1180px;
  min-height:500px;
  max-height:calc(100vh - 165px);
  overflow-y:auto;
  background:#FFFFFF;
  border-radius:24px;
  box-shadow:0 30px 80px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.1);
  padding:36px 44px;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  box-sizing:border-box;
}
.ppt-slide{
  display:none;
  opacity:0;
  transform:scale(0.97) translateY(12px);
  will-change:transform, opacity, filter;
}
.ppt-slide.active{
  display:flex;
  flex-direction:column;
  opacity:1;
  transform:scale(1) translateY(0);
  animation:morphSlideIn .5s cubic-bezier(.16,1,.3,1) forwards;
}

@keyframes morphSlideIn{
  0%{
    opacity:0;
    transform:scale(0.97) translateY(14px);
    filter:blur(5px);
  }
  60%{
    filter:blur(0px);
  }
  100%{
    opacity:1;
    transform:scale(1) translateY(0);
    filter:blur(0px);
  }
}

.ppt-slide.active .ppt-card{
  animation:morphCardIn .55s cubic-bezier(.16,1,.3,1) both;
  animation-delay:calc(var(--ci, 0) * 80ms);
}
@keyframes morphCardIn{
  0%{
    opacity:0;
    transform:translateY(20px) scale(0.94);
  }
  100%{
    opacity:1;
    transform:translateY(0) scale(1);
  }
}

.ppt-slide.active .ppt-formula-box{
  animation:morphFormulaIn .6s cubic-bezier(.16,1,.3,1) both;
  animation-delay:240ms;
}
@keyframes morphFormulaIn{
  0%{
    opacity:0;
    transform:scale(0.94) translateY(16px);
  }
  100%{
    opacity:1;
    transform:scale(1) translateY(0);
  }
}

.ppt-slide-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:12px;
  flex-wrap:wrap;
  gap:10px;
}
.ppt-slide-badges{
  display:flex;
  align-items:center;
  gap:10px;
}
.ppt-badge-slide{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:700;
  background:#EFF6FF;
  color:#1D4ED8;
  border:1px solid #BFDBFE;
  padding:3px 10px;
  border-radius:6px;
}
.ppt-badge-sec{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:600;
  background:#F1F5F9;
  color:#475569;
  border:1px solid #CBD5E1;
  padding:3px 10px;
  border-radius:6px;
}
.ppt-badge-live{
  display:inline-flex;
  align-items:center;
  gap:6px;
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:700;
  color:#059669;
  background:#ECFDF5;
  border:1px solid #A7F3D0;
  padding:3px 10px;
  border-radius:999px;
  letter-spacing:.03em;
}
.ppt-live-dot{
  width:7px;
  height:7px;
  border-radius:50%;
  background:#10B981;
  animation:livePulse 1.8s infinite;
}
@keyframes livePulse{
  0%,100%{transform:scale(1);opacity:1}
  50%{transform:scale(1.4);opacity:.6}
}

.ppt-slide-title-wrap{
  display:flex;
  align-items:center;
  gap:14px;
  margin-bottom:20px;
}
.ppt-title-bar{
  width:6px;
  height:30px;
  background:linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%);
  border-radius:999px;
  flex-shrink:0;
}
.ppt-slide-title{
  font-family:var(--f-display);
  font-size:1.55rem;
  font-weight:800;
  color:#0F172A;
  margin:0;
  letter-spacing:-.02em;
}

.ppt-cards-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));
  gap:18px;
  margin-bottom:16px;
  width:100%;
  box-sizing:border-box;
}
@media (min-width: 860px){
  .ppt-cards-grid.cards-3{
    grid-template-columns:repeat(3, minmax(0, 1fr)) !important;
  }
  .ppt-cards-grid.cards-2{
    grid-template-columns:repeat(2, minmax(0, 1fr)) !important;
  }
  .ppt-cards-grid.cards-4{
    grid-template-columns:repeat(2, minmax(0, 1fr)) !important;
  }
}

.ppt-card{
  background:#F8FAFC;
  border:1.5px solid #E2E8F0;
  border-radius:18px;
  padding:22px 24px;
  min-width:0;
  box-sizing:border-box;
  display:flex;
  flex-direction:column;
  word-break:break-word;
  overflow-wrap:break-word;
  transition:all .3s cubic-bezier(.16,1,.3,1);
  box-shadow:0 2px 6px rgba(0,0,0,0.02);
}
.ppt-card.highlight{
  background:linear-gradient(180deg, #F0F7FF 0%, #FFFFFF 100%);
  border:2px solid #2563EB;
  box-shadow:0 10px 30px rgba(37,99,235,0.14);
  transform:translateY(-2px);
}
.ppt-card-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:10px;
}
.ppt-card-badge{
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:700;
  color:#64748B;
  background:#FFFFFF;
  border:1px solid #CBD5E1;
  padding:3px 10px;
  border-radius:6px;
}
.ppt-card.highlight .ppt-card-badge{
  color:#1D4ED8;
  background:#DBEAFE;
  border-color:#93C5FD;
}
.ppt-card-heading{
  font-size:1.15rem;
  font-weight:700;
  color:#0F172A;
  margin-bottom:12px;
  line-height:1.35;
}
.ppt-card.highlight .ppt-card-heading{
  color:#1D4ED8;
}
.ppt-card-bullets{
  list-style:none;
  margin:0;
  padding:0;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.ppt-bullet{
  position:relative;
  padding-left:18px;
  font-size:.92rem;
  line-height:1.6;
  color:#334155;
}
.ppt-bullet-dot{
  position:absolute;
  left:0;
  top:8px;
  width:6px;
  height:6px;
  border-radius:50%;
  background:#2563EB;
}

.ppt-formula-box{
  background:linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border:2px solid #F59E0B;
  border-radius:18px;
  padding:20px 24px;
  margin-top:16px;
  box-sizing:border-box;
  box-shadow:0 6px 20px rgba(245,158,11,0.12);
}
.ppt-formula-tag{
  display:inline-flex;
  align-items:center;
  gap:6px;
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:800;
  background:#D97706;
  color:#FFFFFF;
  padding:4px 10px;
  border-radius:6px;
  text-transform:uppercase;
  letter-spacing:.04em;
  margin-bottom:10px;
}
.ppt-formula-text{
  font-family:var(--f-mono);
  font-size:1.06rem;
  font-weight:800;
  color:#78350F;
  margin-bottom:8px;
  line-height:1.5;
  background:rgba(255,255,255,0.75);
  padding:10px 14px;
  border-radius:10px;
  border:1px solid rgba(245,158,11,0.3);
}
.ppt-formula-example{
  font-size:.9rem;
  color:#92400E;
  background:rgba(254,243,199,0.8);
  border:1px solid rgba(245,158,11,0.3);
  padding:10px 14px;
  border-radius:10px;
  line-height:1.55;
}
.pfe-tag{
  display:inline-block;
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
  background:#F59E0B;
  color:#FFFFFF;
  padding:2px 6px;
  border-radius:4px;
  margin-right:8px;
}

.theater-launch-card{
  background:linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  border:1.5px solid #334155;
  border-radius:16px;
  padding:16px 20px;
  margin-bottom:20px;
  color:#FFFFFF;
  cursor:pointer;
  transition:all .25s ease;
  box-shadow:0 4px 16px rgba(0,0,0,0.06);
  display:flex;
  flex-direction:column;
  gap:10px;
}
.theater-launch-card:hover{
  border-color:#3B82F6;
  box-shadow:0 8px 24px rgba(37,99,235,0.18);
  transform:translateY(-1px);
}
.tlc-badge{
  display:inline-block;
  align-self:flex-start;
  font-family:var(--f-mono);
  font-size:.7rem;
  font-weight:700;
  background:rgba(59,130,246,0.2);
  color:#60A5FA;
  border:1px solid rgba(59,130,246,0.4);
  padding:3px 10px;
  border-radius:4px;
  letter-spacing:.02em;
}
.tlc-inner{
  display:flex;
  align-items:center;
  gap:16px;
  flex-wrap:wrap;
}
.tlc-icon{
  font-size:2rem;
  flex-shrink:0;
  background:rgba(255,255,255,0.08);
  width:48px;
  height:48px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:12px;
}
.tlc-text{
  flex:1;
  min-width:220px;
}
.tlc-text h4{
  margin:0 0 4px;
  font-size:1.02rem;
  font-weight:700;
  color:#F8FAFC;
}
.tlc-text p{
  margin:0;
  font-size:.85rem;
  color:#94A3B8;
  line-height:1.4;
}
.tlc-btn{
  background:#2563EB;
  color:#FFFFFF;
  border:none;
  padding:10px 18px;
  border-radius:10px;
  font-size:.86rem;
  font-weight:700;
  cursor:pointer;
  transition:background .2s;
  flex-shrink:0;
}
.tlc-btn:hover{
  background:#1D4ED8;
}

/* Fullscreen Bottom Playback Dock */
.vtheater-dock{
  position:sticky;
  bottom:0;
  left:0;
  right:0;
  background:rgba(15,23,42,0.94);
  backdrop-filter:blur(20px);
  border-top:1px solid rgba(255,255,255,0.08);
  padding:12px 32px;
  display:flex;
  align-items:center;
  gap:18px;
  z-index:50;
}
.vtd-play{
  width:44px;
  height:44px;
  border-radius:50%;
  background:#2563EB;
  color:#FFFFFF;
  display:grid;
  place-items:center;
  border:0;
  cursor:pointer;
  flex-shrink:0;
  transition:transform .2s, background .2s;
  box-shadow:0 4px 14px rgba(37,99,235,0.4);
}
.vtd-play:hover{
  transform:scale(1.08);
  background:#1D4ED8;
}
.vtd-info{
  display:flex;
  flex-direction:column;
  min-width:130px;
  max-width:280px;
}
.vtd-time{
  font-family:var(--f-mono);
  font-size:.86rem;
  font-weight:700;
  color:#F8FAFC;
}
.vtd-label{
  font-size:.76rem;
  color:#94A3B8;
  font-weight:600;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.vtd-seek{
  flex:1;
  accent-color:#2563EB;
  cursor:pointer;
  height:6px;
}
.vtd-speed-pill{
  font-family:var(--f-mono);
  font-weight:700;
  font-size:.82rem;
  background:#1E293B;
  color:#F8FAFC;
  border:1px solid #334155;
  padding:6px 14px;
  border-radius:999px;
  cursor:pointer;
  transition:all .2s;
}
.vtd-speed-pill:hover{
  background:#334155;
}
.vtd-close-pill{
  font-size:.84rem;
  font-weight:700;
  border:1.5px solid rgba(239,68,68,0.45);
  background:rgba(239,68,68,0.15);
  color:#FCA5A5;
  padding:7px 18px;
  border-radius:999px;
  cursor:pointer;
  transition:all .2s;
}
.vtd-close-pill:hover{
  background:#EF4444;
  color:#FFFFFF;
  border-color:#F87171;
  box-shadow:0 0 14px rgba(239,68,68,0.4);
}

.flow-grid{
  display:grid;
  gap:16px;
}
.flow-node{
  background:#F8FAFC;
  border:2px solid #E2E8F0;
  border-radius:16px;
  padding:20px 22px;
  transition:all .3s cubic-bezier(.2,.8,.2,1);
  position:relative;
  cursor:pointer;
  user-select:none;
  color:#0F172A;
}
.flow-node:hover{
  border-color:#CBD5E1;
  background:#F1F5F9;
  transform:translateY(-2px);
}
.flow-node.flow-active{
  border-color:#2563EB !important;
  background:#EFF6FF !important;
  box-shadow:0 8px 24px rgba(37,99,235,0.15);
  transform:translateY(-3px);
}
.flow-node.flow-active .flow-active-badge{
  display:inline-flex;
}
.flow-active-badge{
  display:none;
  align-items:center;
  gap:6px;
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:700;
  color:#FFFFFF;
  background:#2563EB;
  padding:3px 10px;
  border-radius:999px;
  letter-spacing:.04em;
  box-shadow:0 2px 8px rgba(37,99,235,0.3);
}
.flow-badge{
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:700;
  letter-spacing:.06em;
  text-transform:uppercase;
  padding:3px 9px;
  border-radius:6px;
  display:inline-block;
}
.flow-badge.blue{background:#EFF6FF;color:#2563EB;border:1px solid #BFDBFE}
.flow-badge.gold{background:#FFFBEB;color:#D97706;border:1px solid #FDE68A}
.flow-badge.green{background:#ECFDF5;color:#059669;border:1px solid #A7F3D0}
.flow-badge.red{background:#FEF2F2;color:#DC2626;border:1px solid #FECACA}

.flow-title{
  font-size:1.18rem;
  font-weight:700;
  color:#0F172A;
  margin:10px 0 6px;
  letter-spacing:-.01em;
}
.flow-desc{
  font-size:.92rem;
  color:#475569;
  line-height:1.55;
  margin:0;
}
.flow-node.flow-active .flow-desc{
  color:#1E293B;
}

"""

text = text[:idx_css1] + new_css + text[idx_css2:]
print("1. Applied new presentation CSS")

# =========================================================================
# 2. Update renderFlowchartHtml and renderTheaterModalHtml
# =========================================================================
rf_start = "function renderFlowchartHtml(q, p){"
idx_rf = text.find(rf_start)
idx_vstudio = text.find("function vStudio(r){", idx_rf)

new_render_functions = """function renderFlowchartHtml(q, p){
  const qn = q.n;
  const sbKey = 'q' + qn;
  const sb = (D.storyboards && (D.storyboards[sbKey] || D.storyboards[p.file ? p.file.replace('.mp3', '') : '']));

  if (sb && sb.slides && sb.slides.length > 0) {
    return `
      <!-- Slide Viewport: ONLY ONE SLIDE DISPLAYED AT A TIME WITH MORPH TRANSITIONS -->
      ${sb.slides.map((s, idx) => {
        const cardsCount = (s.cards || []).length;
        const cardsClass = cardsCount > 0 ? ('cards-' + cardsCount) : '';
        return `
        <div class="ppt-slide ${idx === 0 ? 'active' : ''}" data-t0="${s.t0 || 0}" data-t1="${s.t1 || 999}" data-slide-idx="${idx}" id="slide-${qn}-${s.slide_number}">
          <div class="ppt-slide-header">
            <div class="ppt-slide-badges">
              <span class="ppt-badge-slide">SLIDE ${s.slide_number} OF ${sb.slides.length}</span>
              ${s.section_badge ? `<span class="ppt-badge-sec">${esc(s.section_badge)}</span>` : ''}
            </div>
            <span class="ppt-badge-live"><span class="ppt-live-dot"></span>EXPLAINING IN MALAYALAM</span>
          </div>

          <div class="ppt-slide-title-wrap">
            <span class="ppt-title-bar"></span>
            <h2 class="ppt-slide-title">${esc(s.slide_title)}</h2>
          </div>

          <div class="ppt-cards-grid ${cardsClass}">
            ${(s.cards || []).map((c, ci) => `
              <div class="ppt-card ${c.is_highlight ? 'highlight' : ''}" style="--ci:${ci}">
                <div class="ppt-card-top">
                  ${c.badge ? `<span class="ppt-card-badge">${esc(c.badge)}</span>` : '<span></span>'}
                </div>
                <div class="ppt-card-heading">${esc(c.title)}</div>
                <ul class="ppt-card-bullets">
                  ${(c.bullets || []).map(b => `<li class="ppt-bullet"><span class="ppt-bullet-dot"></span><span>${esc(b)}</span></li>`).join('')}
                </ul>
              </div>
            `).join('')}
          </div>

          ${s.formula_box ? `
            <div class="ppt-formula-box">
              <div class="ppt-formula-tag">🧮 STATUTORY COMPUTATIONAL FORMULA</div>
              <div class="ppt-formula-text">${esc(s.formula_box.formula_text || '')}</div>
              ${s.formula_box.example_calc ? `<div class="ppt-formula-example"><span class="pfe-tag">WORKED EXAMPLE</span>${esc(s.formula_box.example_calc)}</div>` : ''}
            </div>
          ` : ''}
        </div>
      `}).join('')}`;
  }

  if(qn === 9 || qn === 10){
    return `
    <div class="ppt-slide active" data-t0="0" data-t1="999" id="slide-${qn}-1">
      <div class="flow-grid" style="grid-template-columns:1fr 1fr;gap:18px">
        <div class="flow-node" data-t0="0" data-t1="7.5" id="fn-q9-1">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span class="flow-badge blue">Step 1 · Base Tax Rate</span>
            <span class="flow-active-badge">● EXPLAINING NOW</span>
          </div>
          <div class="flow-title">Domestic Co. Turnover ≤ ₹ 400 Cr</div>
          <div class="flow-desc">Tax rate is <b>25%</b> if turnover in previous year ≤ ₹ 400 Cr. Otherwise standard rate of <b>30%</b> applies.</div>
        </div>
        <div class="flow-node" data-t0="7.5" data-t1="16.0" id="fn-q9-2">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span class="flow-badge gold">Step 2 · Surcharge Slabs</span>
            <span class="flow-active-badge">● EXPLAINING NOW</span>
          </div>
          <div class="flow-title">Total Income > ₹ 1 Cr vs > ₹ 10 Cr</div>
          <div class="flow-desc">Surcharge is <b>7%</b> if TI > ₹ 1 Cr up to ₹ 10 Cr. Surcharge increases to <b>12%</b> if Total Income exceeds ₹ 10 Crores.</div>
        </div>
      </div>
    </div>`;
  }

  return `
  <div class="ppt-slide active" data-t0="0" data-t1="999" id="slide-${qn}-1">
    <div class="ppt-slide-title-wrap">
      <span class="ppt-title-bar"></span>
      <h2 class="ppt-slide-title">${esc(p.doctrine)}</h2>
    </div>
    <div class="ppt-cards-grid cards-1">
      <div class="ppt-card highlight">
        <div class="ppt-card-heading">Statutory Rule Principle</div>
        <p style="color:#334155;line-height:1.6;font-size:1.05rem">${esc(p.principle || "Detailed provision explainer audio playing in spoken Malayalam.")}</p>
      </div>
    </div>
  </div>`;
}

function renderTheaterModalHtml(q, p){
  const qn = q.n;
  const sbKey = 'q' + qn;
  const sb = (D.storyboards && (D.storyboards[sbKey] || D.storyboards[p.file ? p.file.replace('.mp3', '') : ''])) || { slides: [] };
  const hasSlides = sb && sb.slides && sb.slides.length > 0;

  return `
  <div class="vtheater" id="vtheater" role="dialog" aria-modal="true" aria-label="Statutory Presentation">
    <!-- Top Navigation Bar -->
    <div class="vtheater-topbar">
      <div class="vtb-left">
        <span class="vtb-badge">§ DIRECT TAX</span>
        <span class="vtb-title" title="${esc(p.doctrine)}">${esc(p.doctrine)}</span>
      </div>

      <!-- Center: Slide Navigation Rail -->
      <div class="vtb-center">
        ${hasSlides ? `
        <div class="ppt-nav-rail" role="tablist">
          ${sb.slides.map((s, idx) => `
            <button class="ppt-nav-dot ${idx === 0 ? 'active' : ''}" data-t0="${s.t0 || 0}" data-slide-idx="${idx}" title="Slide ${s.slide_number}: ${esc(s.slide_title)}" aria-label="Go to slide ${s.slide_number}">
              <span class="ppt-dot-num">${s.slide_number}</span>
              <span class="ppt-dot-label">${esc(s.slide_title)}</span>
            </button>
          `).join('')}
        </div>
        ` : ''}
      </div>

      <!-- Right: Direct Close Button (No Video Toggle) -->
      <div class="vtb-right">
        <button id="vclose" class="vtb-close-btn" aria-label="Close presentation (Escape)" title="Close presentation (Escape)">
          <span style="font-size:1.1rem;line-height:1">✕</span> Close Presentation
        </button>
      </div>
    </div>

    <!-- Presentation Stage with Floating Navigation Arrows -->
    <div id="vdiag" class="vfullscreen-stage">
      <div class="ppt-stage-wrapper">
        <button class="ppt-arrow-btn prev" id="ppt-prev-btn" title="Previous Slide (Left Arrow)" aria-label="Previous Slide">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
        </button>

        <div class="ppt-viewport">
          ${renderFlowchartHtml(q, p)}
        </div>

        <button class="ppt-arrow-btn next" id="ppt-next-btn" title="Next Slide (Right Arrow)" aria-label="Next Slide">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>
    </div>

    <!-- Synchronized Floating Bottom Dock -->
    <div class="vtheater-dock" id="vtheater-dock">
      <button class="vtd-play" id="vtd-play" aria-label="Play/Pause">${I.play}</button>
      <div class="vtd-info">
        <span id="vtd-time" class="vtd-time">0:00 / ${fmt(p.dur)}</span>
        <span id="vtd-label" class="vtd-label">Slide 1 of ${hasSlides ? sb.slides.length : 1}</span>
      </div>
      <input type="range" class="vtd-seek" id="vtd-seek" min="0" max="1000" value="0" aria-label="Seek audio">
      <button id="vtd-speed" class="vtd-speed-pill" title="Toggle Playback Speed">1.0x</button>
      <button id="vtd-close" class="vtd-close-pill" aria-label="Close presentation" title="Close presentation">✕ Close</button>
    </div>
  </div>
  `;
}

"""

text = text[:idx_rf] + new_render_functions + text[idx_vstudio:]
print("2. Applied new renderFlowchartHtml and renderTheaterModalHtml")

# =========================================================================
# 3. Update makePlayer(p)
# =========================================================================
mp_start = "function makePlayer(p){"
idx_mp = text.find(mp_start)
idx_global = text.find("/* ---------- global ---------- */", idx_mp)

new_make_player = """function makePlayer(p){
 const root=$("#player"),playB=$("#play"),seek=$("#seek"),time=$("#time"),spd=$("#speed"),note=$("#anote"),bars=$$("#wave i");
 const vtheater=$("#vtheater"),vtog=$("#vtog"),vclose=$("#vclose");
 const vtdClose=$("#vtd-close"),vtdPlay=$("#vtd-play"),vtdSeek=$("#vtd-seek"),vtdSpeed=$("#vtd-speed");
 const vtogBtn=$("#vtog-btn");
 const prevBtn=$("#ppt-prev-btn"),nextBtn=$("#ppt-next-btn");

 const speeds=[1,1.25,1.5,2];let si=0,playing=false,vraf=0,dead=false;
 const audioFile = p.file || "q1.mp3";
 const audioBase = audioFile.startsWith('/') ? audioFile : "/audio/" + audioFile;
 const audioUrl = audioBase + "?v=aoede_" + Math.round(p.dur || 1);
 
 const audio = new Audio();
 audio.preload = "auto";
 audio.src = audioUrl;

 const total = () => (audio && isFinite(audio.duration) && audio.duration > 0) ? audio.duration : (p.dur || 75);

 function openTheater(){
  if(vtheater){
   vtheater.style.removeProperty("display");
   vtheater.classList.add("open");
  }
  document.body.style.overflow = "hidden";
  if(!playing) start();
 }

 function closeTheater(){
  if(vtheater){
   vtheater.classList.remove("open");
   vtheater.style.setProperty("display", "none", "important");
  }
  document.body.style.overflow = "";
  stop();
 }

 function ui(){
  const cur = audio.currentTime || 0;
  const T = total();
  const f = T > 0 ? Math.min(1, Math.max(0, cur / T)) : 0;
  time.textContent = fmt(cur) + " / " + fmt(T);
  seek.value = Math.round(f * 1000);
  seek.style.setProperty("--p", f);
  const n = Math.round(f * bars.length);
  bars.forEach((b, k) => b.classList.toggle("on", k < n));
  const rc = $("#ringc");
  if(rc) rc.style.strokeDashoffset = 175.9 * (1 - f);
  const vtdTime = $("#vtd-time");
  if(vtdTime) vtdTime.textContent = fmt(cur) + " / " + fmt(T);
  const vtdSeek = $("#vtd-seek");
  if(vtdSeek) vtdSeek.value = Math.round(f * 1000);
  const curVtdPlay = $("#vtd-play");
  if(curVtdPlay) curVtdPlay.innerHTML = playing ? I.pause : I.play;
  syncFlowchart(cur);
 }

 function syncFlowchart(cur){
  // Single Explaining Slide with Morph Transition
  const slides = $$(".ppt-slide");
  if(slides && slides.length > 0){
   let activeIdx = 0;
   slides.forEach((slide, idx) => {
    const t0 = parseFloat(slide.dataset.t0 || "0");
    const t1 = parseFloat(slide.dataset.t1 || "9999");
    if(cur >= t0 && cur < t1){
     activeIdx = idx;
    }
   });

   slides.forEach((slide, idx) => {
    const wasActive = slide.classList.contains("active");
    const shouldBeActive = (idx === activeIdx);
    if(shouldBeActive && !wasActive){
     slide.classList.add("active");
    } else if(!shouldBeActive && wasActive){
     slide.classList.remove("active");
    }
   });

   // Update slide navigation dots
   const dots = $$(".ppt-nav-dot");
   if(dots && dots.length > 0){
    dots.forEach((dot, idx) => {
     dot.classList.toggle("active", idx === activeIdx);
     dot.classList.toggle("past", idx < activeIdx);
    });
   }

   // Update dock label
   const vtdLabel = $("#vtd-label");
   if(vtdLabel && slides[activeIdx]){
    const sTitle = slides[activeIdx].querySelector(".ppt-slide-title");
    vtdLabel.textContent = `Slide ${activeIdx + 1} of ${slides.length}: ${sTitle ? sTitle.textContent : ''}`;
   }
  }

  // Legacy fallback
  const nodes = $$(".flow-node:not(.ppt-slide)");
  if(nodes && nodes.length > 0){
   nodes.forEach(node => {
    const t0 = parseFloat(node.dataset.t0 || "0");
    const t1 = parseFloat(node.dataset.t1 || "9999");
    const active = (cur >= t0 && cur < t1);
    node.classList.toggle("flow-active", active);
   });
  }
 }

 function vizOn(){
  cancelAnimationFrame(vraf);
  (function f(n){
   if(!playing || dead) return;
   const q = n / 1000 * speeds[si];
   bars.forEach((b, k) => {
    b.style.transform = "scaleY(" + (.55 + .45 * Math.sin(q * 5 + k * .6) * Math.cos(q * 2.3 + k * .21)).toFixed(3) + ")";
   });
   vraf = requestAnimationFrame(f);
  })(performance.now());
 }

 function vizOff(){
  bars.forEach(b => b.style.transform = "");
 }

 async function start(){
  try {
   audio.playbackRate = speeds[si];
   await audio.play();
   playing = true;
   root.classList.add("playing");
   playB.innerHTML = I.pause;
   playB.setAttribute("aria-label", "Pause audio");
   note.textContent = "Playing Malayalam explainer: " + (p.doctrine || "Statutory Rule") + " · " + (p.voice || "Gemini Voice (Aoede)");
   if(vtheater){
    vtheater.style.removeProperty("display");
    vtheater.classList.add("open");
    document.body.style.overflow = "hidden";
   }
   const curVtdPlay = $("#vtd-play");
   if(curVtdPlay) curVtdPlay.innerHTML = I.pause;
   vizOn();
  } catch(err) {
   console.warn("audio.play() error:", err);
   note.textContent = "Tap play to start audio playback (" + (err.message || "User interaction required") + ")";
   stop();
  }
 }

 function stop(){
  playing = false;
  try { audio.pause(); } catch(e){}
  const curVtdPlay = $("#vtd-play");
  if(curVtdPlay) curVtdPlay.innerHTML = I.play;
  cancelAnimationFrame(vraf);
  vizOff();
  root.classList.remove("playing");
  playB.innerHTML = I.play;
  playB.setAttribute("aria-label", "Play audio");
 }

 function finish(){
  stop();
  audio.currentTime = 0;
  ui();
 }

 const togglePlay = (e) => {
  if (e) {
   e.preventDefault();
   e.stopPropagation();
  }
  if (playing) stop();
  else start();
 };

 playB.onclick = togglePlay;
 const wrap = root.querySelector(".playwrap");
 if (wrap) wrap.onclick = togglePlay;

 seek.oninput = () => {
  const T = total();
  const target = (seek.value / 1000) * T;
  if(isFinite(target)){
   audio.currentTime = target;
  }
  ui();
 };

 spd.onclick = () => {
  si = (si + 1) % speeds.length;
  const txt = speeds[si] === 1 ? "1.0x" : speeds[si] + "x";
  spd.textContent = txt;
  if(vtdSpeed) vtdSpeed.textContent = txt;
  audio.playbackRate = speeds[si];
 };

 if(vtog) vtog.onclick = openTheater;
 if(vtogBtn) vtogBtn.onclick = (e) => { e.stopPropagation(); openTheater(); };
 if(vclose) vclose.onclick = closeTheater;
 if(vtdClose) vtdClose.onclick = closeTheater;

 if(vtdPlay){
  vtdPlay.onclick = () => {
   if(playing) stop();
   else start();
  };
 }

 if(vtdSeek){
  vtdSeek.oninput = () => {
   const T = total();
   const target = (vtdSeek.value / 1000) * T;
   if(isFinite(target)){
    audio.currentTime = target;
   }
   ui();
  };
 }

 if(vtdSpeed){
  vtdSpeed.onclick = () => {
   si = (si + 1) % speeds.length;
   const txt = speeds[si] === 1 ? "1.0x" : speeds[si] + "x";
   spd.textContent = txt;
   vtdSpeed.textContent = txt;
   audio.playbackRate = speeds[si];
  };
 }

 $$(".ppt-nav-dot").forEach(dot => {
  dot.onclick = (e) => {
   e.stopPropagation();
   const t0 = parseFloat(dot.dataset.t0 || "0");
   audio.currentTime = t0;
   if(!playing) start();
   ui();
  };
 });

 if(prevBtn){
  prevBtn.onclick = (e) => {
   e.stopPropagation();
   const slides = $$(".ppt-slide");
   if(!slides.length) return;
   let curIdx = 0;
   slides.forEach((s, idx) => { if(s.classList.contains("active")) curIdx = idx; });
   const targetIdx = Math.max(0, curIdx - 1);
   const t0 = parseFloat(slides[targetIdx].dataset.t0 || "0");
   audio.currentTime = t0;
   if(!playing) start();
   ui();
  };
 }

 if(nextBtn){
  nextBtn.onclick = (e) => {
   e.stopPropagation();
   const slides = $$(".ppt-slide");
   if(!slides.length) return;
   let curIdx = 0;
   slides.forEach((s, idx) => { if(s.classList.contains("active")) curIdx = idx; });
   const targetIdx = Math.min(slides.length - 1, curIdx + 1);
   const t0 = parseFloat(slides[targetIdx].dataset.t0 || "0");
   audio.currentTime = t0;
   if(!playing) start();
   ui();
  };
 }

 $$(".flow-node").forEach(node => {
  node.onclick = (e) => {
   e.stopPropagation();
   const t0 = parseFloat(node.dataset.t0 || "0");
   audio.currentTime = t0;
   if(!playing) start();
   ui();
  };
 });

 const globalClickHandler = (e) => {
  if (e.target.closest("#vclose") || e.target.closest("#vtd-close") || e.target.closest(".vtb-close-btn") || e.target.closest(".vtd-close-pill")) {
   e.preventDefault();
   e.stopPropagation();
   closeTheater();
  }
 };
 document.addEventListener("click", globalClickHandler);

 const keyListener = (e) => {
  if(vtheater && vtheater.classList.contains("open")){
   if(e.key === "Escape"){
    closeTheater();
   } else if(e.key === " " && e.target.tagName !== "INPUT" && e.target.tagName !== "BUTTON"){
    e.preventDefault();
    if(playing) stop();
    else start();
   } else if(e.key === "ArrowLeft"){
    if(prevBtn) prevBtn.click();
   } else if(e.key === "ArrowRight"){
    if(nextBtn) nextBtn.click();
   }
  }
 };
 window.addEventListener("keydown", keyListener);

 audio.ontimeupdate = ui;
 audio.onended = finish;
 audio.onerror = () => {
  console.warn("Audio error for", audioUrl);
  note.textContent = "Audio unavailable (" + audioUrl + "). Review provision text below.";
 };

 return {
  destroy(){
   dead = true;
   window.removeEventListener("keydown", keyListener);
   document.removeEventListener("click", globalClickHandler);
   stop();
   audio.src = "";
   const troot = $("#theater-root");
   if(troot) troot.innerHTML = "";
   document.body.style.overflow = "";
  }
 };
}

"""

text = text[:idx_mp] + new_make_player + text[idx_global:]
print("3. Applied new makePlayer")

with open(FRONTEND_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("All updates successfully written to frontend/index.html!")
