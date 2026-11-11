import os
import shutil

FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
BACKUP_PATH = FRONTEND_PATH + ".bak"

# 1. Create a backup
if not os.path.exists(BACKUP_PATH):
    shutil.copyfile(FRONTEND_PATH, BACKUP_PATH)
    print("Created backup at", BACKUP_PATH)

with open(FRONTEND_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ==========================================
# Change 1: Add #theater-root after #app
# ==========================================
app_tag = '<main class="wrap" id="app"></main>'
if '<div id="theater-root"></div>' not in html:
    if app_tag not in html:
        print("ERROR: app_tag not found")
        exit(1)
    html = html.replace(app_tag, app_tag + '\n<div id="theater-root"></div>')
    print("Added #theater-root")

# ==========================================
# Change 2: Update cleanup()
# ==========================================
old_cleanup = 'function cleanup(){if(player){player.destroy();player=null}if(io){io.disconnect();io=null}}'
new_cleanup = """function cleanup(){
  if(player){player.destroy();player=null}
  if(io){io.disconnect();io=null}
  const troot = $("#theater-root");
  if(troot) troot.innerHTML = "";
  document.body.style.overflow = "";
}"""

if old_cleanup in html:
    html = html.replace(old_cleanup, new_cleanup)
    print("Updated cleanup()")
elif 'const troot = $("#theater-root");' in html:
    print("cleanup() already updated")
else:
    print("Warning: old_cleanup pattern not matched, checking variation...")

# ==========================================
# Change 3: Replace PowerPoint CSS
# ==========================================
css_start = '/* ===== PowerPoint Explainer Theater & Morphing Deck ===== */'
css_end = '@media (max-width:860px){'

idx_start = html.find(css_start)
idx_end = html.find(css_end, idx_start)

if idx_start == -1 or idx_end == -1:
    print("ERROR: CSS markers not found!")
    exit(1)

new_css = """/* ===== PowerPoint Explainer Theater & Morphing Deck ===== */
.vtheater{
  position:fixed !important;
  inset:0 !important;
  width:100vw !important;
  height:100vh !important;
  z-index:99999999 !important;
  background:#090D16 !important;
  display:flex !important;
  flex-direction:column !important;
  overflow:hidden !important;
  margin:0 !important;
  border:0 !important;
  border-radius:0 !important;
  box-shadow:none !important;
  animation:theaterFadeIn .25s ease-out;
}
@keyframes theaterFadeIn{
  from{opacity:0;transform:scale(0.98)}
  to{opacity:1;transform:scale(1)}
}

.vtheater-topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 24px;
  background:#0F172A;
  border-bottom:1px solid #1E293B;
  gap:14px;
  flex-shrink:0;
  z-index:30;
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
  background:#1E3A8A;
  color:#93C5FD;
  border:1px solid #3B82F6;
  padding:4px 10px;
  border-radius:6px;
  font-weight:700;
  white-space:nowrap;
  flex-shrink:0;
}
.vtb-title{
  font-size:1.02rem;
  font-weight:700;
  color:#F8FAFC;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  max-width:320px;
}
.vtb-center{
  display:flex;
  align-items:center;
  justify-content:center;
  flex:1;
  min-width:0;
}
.ppt-nav-rail{
  display:flex;
  align-items:center;
  gap:8px;
  max-width:650px;
  overflow-x:auto;
  padding:2px;
  scrollbar-width:none;
}
.ppt-nav-rail::-webkit-scrollbar{display:none;}
.ppt-nav-dot{
  display:inline-flex;
  align-items:center;
  gap:6px;
  background:#1E293B;
  border:1px solid #334155;
  border-radius:999px;
  padding:6px 14px;
  cursor:pointer;
  color:#94A3B8;
  font-size:.78rem;
  white-space:nowrap;
  transition:all .2s;
  flex-shrink:0;
}
.ppt-nav-dot:hover{
  background:#334155;
  color:#FFFFFF;
}
.ppt-nav-dot.active{
  background:#2563EB;
  border-color:#60A5FA;
  color:#FFFFFF;
  font-weight:700;
  box-shadow:0 0 14px rgba(37,99,235,0.45);
  transform:translateY(-1px);
}
.ppt-dot-badge{
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:700;
  opacity:0.9;
}
.ppt-dot-label{
  max-width:140px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  display:inline-block;
}
.vtb-right{
  display:flex;
  align-items:center;
  gap:10px;
  flex-shrink:0;
}
.vtb-mode-btn{
  font-size:.82rem;
  font-weight:700;
  padding:6px 16px;
  border-radius:20px;
  cursor:pointer;
  transition:all .2s;
  background:#1E293B;
  border:1px solid #334155;
  color:#94A3B8;
}
.vtb-mode-btn:hover{
  background:#334155;
  color:#FFFFFF;
}
.vtb-mode-btn.active{
  background:#2563EB;
  border-color:#3B82F6;
  color:#FFFFFF;
  box-shadow:0 0 14px rgba(37,99,235,0.4);
}
.vtb-close-btn{
  color:#F87171;
  padding:6px 14px;
  border-radius:8px;
  font-size:.84rem;
  font-weight:700;
  background:rgba(239,68,68,0.12);
  border:1px solid rgba(239,68,68,0.3);
  cursor:pointer;
  transition:all .2s;
}
.vtb-close-btn:hover{
  background:rgba(239,68,68,0.25);
  color:#FECACA;
}

.vfullscreen-stage{
  flex:1;
  overflow-y:auto;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px 24px 84px;
  background:radial-gradient(circle at 50% 30%, #172554 0%, #090D16 70%);
  box-sizing:border-box;
}

.ppt-viewport{
  position:relative;
  width:min(94vw, 1200px);
  min-height:480px;
  max-height:calc(100vh - 160px);
  overflow-y:auto;
  margin:0 auto;
  border-radius:20px;
  background:#FFFFFF;
  border:1px solid rgba(255,255,255,0.15);
  box-shadow:0 25px 60px rgba(0,0,0,0.55);
  padding:32px 38px;
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
.ppt-sec-badge{
  font-family:var(--f-mono);
  font-size:.78rem;
  background:#F1F5F9;
  color:#475569;
  padding:3px 12px;
  border-radius:6px;
  font-weight:600;
  border:1px solid #E2E8F0;
}
.ppt-slide-title-wrap{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:20px;
}
.ppt-title-bar{
  display:inline-block;
  width:7px;
  height:28px;
  background:#2563EB;
  border-radius:4px;
  flex-shrink:0;
}
.ppt-slide-title{
  font-family:var(--f-display);
  font-size:1.45rem;
  font-weight:800;
  color:#0F172A;
  margin:0;
  letter-spacing:-.01em;
}

.ppt-cards-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));
  gap:16px;
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
  background:#FFFFFF;
  border:1.5px solid #E2E8F0;
  border-radius:16px;
  padding:20px 22px;
  min-width:0;
  box-sizing:border-box;
  word-break:break-word;
  overflow-wrap:break-word;
  transition:border-color .3s, box-shadow .3s;
}
.ppt-card.highlight{
  background:#EFF6FF;
  border:2px solid #2563EB;
  box-shadow:0 8px 24px rgba(37,99,235,0.12);
}
.ppt-card-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:8px;
}
.ppt-card-badge{
  font-size:.74rem;
  font-weight:700;
  font-family:var(--f-mono);
  color:#475569;
  background:#F1F5F9;
  padding:3px 10px;
  border-radius:6px;
}
.ppt-card.highlight .ppt-card-badge{
  color:#2563EB;
  background:#DBEAFE;
}
.ppt-card-heading{
  font-weight:700;
  font-size:1.1rem;
  color:#0F172A;
  margin-bottom:8px;
}
.ppt-card.highlight .ppt-card-heading{
  color:#1D4ED8;
}
.ppt-card-bullets{
  margin:0;
  padding-left:18px;
  color:#334155;
  font-size:.9rem;
  line-height:1.55;
}
.ppt-card-bullets li{
  margin-bottom:4px;
}

.ppt-formula-box{
  background:#FFFBEB;
  border:2px solid #F59E0B;
  border-radius:14px;
  padding:18px 22px;
  margin-top:12px;
  box-sizing:border-box;
}
.ppt-formula-tag{
  display:inline-block;
  font-size:.72rem;
  font-family:var(--f-mono);
  font-weight:800;
  background:#F59E0B;
  color:#FFFFFF;
  padding:3px 9px;
  border-radius:4px;
  margin-bottom:8px;
  text-transform:uppercase;
  letter-spacing:.04em;
}
.ppt-formula-text{
  font-weight:800;
  color:#B45309;
  font-size:1.05rem;
  margin-bottom:6px;
}
.ppt-formula-example{
  font-size:.88rem;
  color:#78350F;
  background:rgba(245,158,11,0.12);
  padding:8px 12px;
  border-radius:8px;
  line-height:1.5;
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
  background:rgba(15,23,42,0.92);
  backdrop-filter:blur(16px);
  border-top:1px solid #1E293B;
  padding:12px 24px;
  display:flex;
  align-items:center;
  gap:16px;
  z-index:40;
}
.vtd-play{
  width:42px;
  height:42px;
  border-radius:50%;
  background:#2563EB;
  color:#FFFFFF;
  display:grid;
  place-items:center;
  border:0;
  cursor:pointer;
  flex-shrink:0;
  transition:transform .2s, background .2s;
}
.vtd-play:hover{
  transform:scale(1.06);
  background:#1D4ED8;
}
.vtd-seek{
  flex:1;
  accent-color:#2563EB;
  cursor:pointer;
  height:6px;
}

#fvideo{
  width:100%;
  max-width:1200px;
  aspect-ratio:16/9;
  max-height:calc(100vh - 160px);
  background:#000;
  object-fit:contain;
  border-radius:16px;
  box-shadow:0 20px 50px rgba(0,0,0,0.6);
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

html = html[:idx_start] + new_css + html[idx_end:]
print("Updated CSS")

with open(FRONTEND_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Stage 1 of patch complete!")
