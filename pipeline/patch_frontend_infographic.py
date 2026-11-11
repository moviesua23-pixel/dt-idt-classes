"""
pipeline/patch_frontend_infographic.py
Updates frontend/index.html with:
1. Light theme background (#F4F7FB) for mindmap stage.
2. 3 cards per row grid (2 on tablet, 1 on phone).
3. 56px circular white icon badge with colored ring overlapping top-left.
4. Per-card individual curved SVG connectors with arrowheads from block pill to card top.
5. Exact visibility:hidden for future items (layout space reserved, no dim placeholders, no lock icons).
6. Explaining now tag as separate strip with pulsing dot and glow.
7. Pure getState(t) with instant scrubbing and seeking.
8. Accurate auto-scroll centering in visible area with 80px top alignment for tall cards and 4s user scroll suppression.
9. Subtitle bar displaying exact source sentence.
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

# Backup index.html if not already backed up
bak_path = os.path.join(PROJECT_ROOT, "frontend", "index.html.bak_req10")
if not os.path.exists(bak_path):
    with open(bak_path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Update CSS styles for mind map
# We will inject/replace the mind map CSS block

css_target_start = "/* ===== Mind Map Theater Styles ===== */"
css_target_end = "/* ===== End Mind Map Theater Styles ===== */"

new_css = """
/* ===== Mind Map Theater Styles (Request 10 Infographic Redesign) ===== */
.ppt-mindmap-view{
  width:100%;
  height:100%;
  max-width:100%;
  margin:0 auto;
  display:flex;
  flex-direction:column;
  overflow:hidden;
  min-height:0;
  box-sizing:border-box;
  position:relative;
  background:#F4F7FB !important;
  animation:fadeIn .35s ease;
}
.ppt-mindmap-view[hidden]{display:none!important}
.ppt-stage-wrapper[hidden]{display:none!important}

.mm-scroll-stage{
  flex:1;
  width:100%;
  height:100%;
  min-height:0;
  overflow-y:auto;
  overflow-x:hidden;
  padding:80px 32px 160px; /* 160px bottom padding ensures dock & subtitle bar never cover cards */
  box-sizing:border-box;
  background:#F4F7FB !important;
  scroll-behavior:auto;
  scrollbar-width:thin;
  scrollbar-color:#CBD5E1 transparent;
}
.mm-scroll-stage::-webkit-scrollbar{
  width:8px;
}
.mm-scroll-stage::-webkit-scrollbar-track{
  background:transparent;
}
.mm-scroll-stage::-webkit-scrollbar-thumb{
  background:#CBD5E1;
  border-radius:999px;
}

.mm-canvas-container{
  position:relative;
  width:100%;
  max-width:1260px;
  margin:0 auto;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:72px;
  box-sizing:border-box;
}

.mm-connector-svg{
  position:absolute;
  top:0;
  left:0;
  width:100%;
  height:100%;
  pointer-events:none;
  z-index:1;
  overflow:visible;
}

/* Inter-Block Path (Root -> B1 -> B2 -> B3 -> B4) */
.mm-branch-path{
  fill:none;
  stroke:#94A3B8;
  stroke-width:2.5px;
  stroke-linecap:round;
  transition:stroke .3s, opacity .3s;
}
.mm-branch-path.path-hidden{
  visibility:hidden;
  opacity:0;
}
.mm-branch-path.path-drawing,
.mm-branch-path.path-active{
  stroke:#1C7ED6;
  stroke-width:3px;
  filter:drop-shadow(0 0 6px rgba(28,126,214,0.6));
}
.mm-branch-path.path-mastered{
  stroke:#12A150;
  stroke-width:2.5px;
  opacity:0.9;
}

/* Step Badges between Blocks */
.mm-step-badge-group{
  transition:opacity .3s;
}
.mm-step-badge-group.badge-hidden{
  visibility:hidden;
  opacity:0;
}
.mm-step-badge-group.badge-drawing,
.mm-step-badge-group.badge-active{
  opacity:1;
}
.mm-badge-bg{
  fill:#1E293B;
  stroke:#94A3B8;
  stroke-width:2px;
}
.badge-drawing .mm-badge-bg,
.badge-active .mm-badge-bg{
  stroke:#1C7ED6;
  fill:#0D3B66;
  filter:drop-shadow(0 0 6px rgba(28,126,214,0.6));
}
.badge-mastered .mm-badge-bg{
  stroke:#12A150;
  fill:#0B5B31;
}
.mm-badge-text{
  font-family:var(--f-mono);
  font-size:11px;
  font-weight:800;
  fill:#FFFFFF;
  dominant-baseline:central;
}

/* Per-Card Curved Connectors from Block Pill to Card Top */
.mm-card-path{
  fill:none;
  stroke-width:3px;
  stroke-linecap:round;
  transition:stroke .25s ease, opacity .25s ease;
}
.mm-card-path.path-hidden{
  visibility:hidden;
  opacity:0;
}
.mm-card-path.path-active{
  stroke-width:3.5px;
  filter:drop-shadow(0 0 8px currentColor);
}
.mm-card-path.path-done{
  stroke-width:2.5px;
  opacity:0.85;
}

/* Converging Connectors to Flow Pill */
.mm-converge-container{
  width:100%;
  height:44px;
  position:relative;
  margin:4px 0 -8px;
}
.mm-converge-svg{
  width:100%;
  height:100%;
  overflow:visible;
  pointer-events:none;
}
.mm-converge-path{
  fill:none;
  stroke:#64748B;
  stroke-width:2px;
  stroke-linecap:round;
  transition:stroke .3s ease, opacity .3s ease;
}
.mm-converge-path.path-hidden{
  visibility:hidden;
  opacity:0;
}
.mm-converge-path.path-active{
  stroke:#1C7ED6;
  stroke-width:2.5px;
  filter:drop-shadow(0 0 6px rgba(28,126,214,0.5));
}
.mm-converge-path.path-done{
  stroke:#12A150;
  stroke-width:2px;
  opacity:0.85;
}

/* Root Doctrine Card at Top */
.mm-root-card{
  width:clamp(340px, 60vw, 780px);
  max-width:100%;
  margin:0 auto;
  background:#1B2A41;
  border:2.5px solid #1C7ED6;
  border-radius:24px;
  padding:20px 28px;
  color:#FFFFFF;
  position:relative;
  box-shadow:0 12px 36px rgba(27,42,65,0.2);
  cursor:pointer;
  transition:transform .25s, box-shadow .25s;
  box-sizing:border-box;
  z-index:2;
  text-align:center;
}
.mm-root-card:hover{
  transform:translateY(-2px);
  box-shadow:0 16px 44px rgba(28,126,214,0.35);
}
.mm-root-top-row{
  display:inline-flex;
  align-items:center;
  gap:10px;
  margin-bottom:8px;
}
.mm-root-badge{
  font-family:var(--f-mono);
  font-size:.76rem;
  font-weight:800;
  color:#60A5FA;
  background:rgba(96,165,250,0.18);
  border:1px solid rgba(96,165,250,0.4);
  padding:3px 12px;
  border-radius:6px;
}
.mm-root-step-tag{
  font-family:var(--f-mono);
  font-size:.70rem;
  font-weight:700;
  color:#94A3B8;
  letter-spacing:.05em;
}
.mm-root-title{
  font-size:1.24rem;
  font-weight:800;
  line-height:1.35;
  color:#FFFFFF;
}

/* Infographic Block */
.mm-infographic-block{
  width:100%;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:26px;
  position:relative;
  z-index:2;
  box-sizing:border-box;
}
.mm-infographic-block.status-hidden{
  visibility:hidden;
  opacity:0;
  pointer-events:none;
}

/* 1. Section Title Pill (Dark Navy, White Text, Section Badge) */
.mm-block-pill{
  display:inline-flex;
  align-items:center;
  gap:14px;
  background:#1B2A41;
  border:2px solid #334155;
  border-radius:999px;
  padding:12px 28px;
  color:#FFFFFF;
  position:relative;
  cursor:pointer;
  box-shadow:0 8px 24px rgba(27,42,65,0.18);
  transition:all .25s ease;
  z-index:3;
  max-width:92%;
}
.mm-block-pill:hover{
  border-color:#1C7ED6;
  transform:translateY(-1px);
  box-shadow:0 12px 28px rgba(28,126,214,0.25);
}
.mm-infographic-block.status-active .mm-block-pill{
  border-color:#1C7ED6;
  box-shadow:0 0 24px rgba(28,126,214,0.4);
}
.mm-infographic-block.status-mastered .mm-block-pill{
  border-color:#12A150;
}
.mm-bp-icon-badge{
  width:34px;
  height:34px;
  border-radius:50%;
  background:rgba(28,126,214,0.2);
  border:1px solid rgba(28,126,214,0.4);
  display:grid;
  place-items:center;
  flex-shrink:0;
  color:#60A5FA;
}
.mm-bp-step{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:800;
  color:#60A5FA;
  background:rgba(28,126,214,0.18);
  border:1px solid rgba(28,126,214,0.35);
  padding:3px 9px;
  border-radius:6px;
  white-space:nowrap;
}
.mm-bp-title{
  font-size:1.06rem;
  font-weight:800;
  color:#FFFFFF;
  letter-spacing:-.01em;
  white-space:nowrap;
}
.mm-bp-badge{
  font-family:var(--f-mono);
  font-size:.76rem;
  font-weight:700;
  color:#CBD5E1;
  background:rgba(255,255,255,0.1);
  border:1px solid rgba(255,255,255,0.2);
  padding:3px 10px;
  border-radius:6px;
  white-space:nowrap;
}
.mm-bp-underline{
  position:absolute;
  bottom:-2px;
  left:28px;
  right:28px;
  height:2.5px;
  background:linear-gradient(90deg, transparent, #1C7ED6, transparent);
  border-radius:999px;
}

/* 2. Point Cards Grid: 3 per row (2 on tablet, 1 on phone) */
.mm-cards-row{
  display:grid;
  grid-template-columns:repeat(3, minmax(0, 1fr));
  gap:28px;
  width:100%;
  box-sizing:border-box;
  align-items:stretch;
}
@media (max-width: 1080px){
  .mm-cards-row{
    grid-template-columns:repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 680px){
  .mm-cards-row{
    grid-template-columns:1fr;
  }
}

/* 3. Infographic Card Structure */
.mm-infographic-card{
  border-radius:20px;
  border-width:2px;
  border-style:solid;
  position:relative;
  box-shadow:0 6px 20px rgba(0,0,0,0.06);
  transition:border-color .28s ease, box-shadow .28s ease, transform .28s ease, opacity .28s ease;
  box-sizing:border-box;
  display:flex;
  flex-direction:column;
  cursor:pointer;
  overflow:visible;
  margin-top:20px; /* clearance for 56px overlapping badge */
}
.mm-infographic-card.card-fullwidth{
  grid-column:1 / -1 !important;
}
.mm-infographic-card:hover{
  transform:translateY(-2px);
  box-shadow:0 12px 30px rgba(0,0,0,0.1);
}

/* Pre-reserve layout space without showing dim placeholders */
.mm-infographic-card.status-hidden{
  visibility:hidden;
  opacity:0;
  pointer-events:none;
}
.mm-infographic-card.status-active{
  visibility:visible;
  opacity:1;
  transform:translateY(-3px);
  z-index:4;
}
.mm-infographic-card.status-done{
  visibility:visible;
  opacity:1;
  box-shadow:0 4px 16px rgba(0,0,0,0.05);
}
.mm-infographic-card.status-reference{
  visibility:visible;
  opacity:1;
  box-shadow:0 4px 14px rgba(0,0,0,0.04);
}

/* Color Palettes */
/* Green */
.theme-green{
  --card-border:#12A150;
  --card-bg:#E9F8EF;
  --card-head:#12A150;
  --card-glow:rgba(18,161,80,0.45);
}
/* Orange */
.theme-orange{
  --card-border:#E8590C;
  --card-bg:#FFF1E6;
  --card-head:#E8590C;
  --card-glow:rgba(232,89,12,0.45);
}
/* Purple */
.theme-purple{
  --card-border:#7048E8;
  --card-bg:#F3EDFF;
  --card-head:#7048E8;
  --card-glow:rgba(112,72,232,0.45);
}
/* Blue */
.theme-blue{
  --card-border:#1C7ED6;
  --card-bg:#E7F1FF;
  --card-head:#1C7ED6;
  --card-glow:rgba(28,126,214,0.45);
}
/* Teal */
.theme-teal{
  --card-border:#0CA678;
  --card-bg:#E6FCF5;
  --card-head:#0CA678;
  --card-glow:rgba(12,166,120,0.45);
}
/* Trap (Amber/Red) */
.theme-trap{
  --card-border:#FA5252;
  --card-bg:#FFF5F5;
  --card-head:#FA5252;
  --card-glow:rgba(250,82,82,0.45);
}

.mm-infographic-card{
  background:var(--card-bg, #FFFFFF);
  border-color:var(--card-border, #CBD5E1);
}
.mm-infographic-card.status-active{
  border-color:var(--card-border) !important;
  box-shadow:0 0 28px var(--card-glow) !important;
}
.mm-infographic-card.status-done{
  border-color:var(--card-border) !important;
}

/* 56px Circular White Icon Badge with Coloured Ring */
.mm-card-icon-badge{
  position:absolute;
  top:-22px;
  left:20px;
  width:56px;
  height:56px;
  border-radius:50%;
  background:#FFFFFF;
  border:3.5px solid var(--card-border);
  box-shadow:0 6px 16px rgba(0,0,0,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  z-index:5;
}
.mm-card-icon-badge svg{
  stroke:var(--card-border);
}

/* Header Ribbon with White Text (Wraps to 2 lines, NEVER truncated) */
.mm-card-ribbon{
  border-radius:18px 18px 0 0;
  padding:14px 20px 14px 92px; /* clearance for 56px badge */
  background:var(--card-head);
  color:#FFFFFF;
  min-height:48px;
  display:flex;
  align-items:center;
  box-sizing:border-box;
}
.mm-card-title{
  font-size:1.02rem;
  font-weight:700;
  line-height:1.35;
  color:#FFFFFF;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:visible !important;
  text-overflow:clip !important;
  white-space:normal !important;
  word-break:break-word;
  flex:1;
}

/* Separate Live Strip / Tag at Top-Right or Bottom */
.mm-card-live-strip{
  position:absolute;
  top:12px;
  right:14px;
  z-index:6;
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
  padding:3px 10px;
  border-radius:999px;
  letter-spacing:.04em;
  display:none;
}
.mm-card-live-strip.tag-active{
  display:inline-flex;
  align-items:center;
  gap:5px;
  background:#0284C7;
  color:#FFFFFF;
  box-shadow:0 0 12px rgba(2,132,199,0.6);
  animation:tagPulse 1.8s infinite ease-in-out;
}
@keyframes tagPulse{
  0%, 100%{opacity:1}
  50%{opacity:0.85}
}
.mm-card-live-strip.tag-done{
  display:inline-flex;
  align-items:center;
  background:#12A150;
  color:#FFFFFF;
}
.mm-card-live-strip.tag-ref{
  display:inline-flex;
  align-items:center;
  background:#64748B;
  color:#FFFFFF;
}

/* Card Body: 17-18px dark text (#1B2A41), line-height 1.5 */
.mm-card-body{
  padding:22px 24px;
  font-size:17.5px;
  line-height:1.52;
  color:#1B2A41;
  display:flex;
  flex-direction:column;
  gap:12px;
  flex:1;
  box-sizing:border-box;
}
.mm-card-body p{
  margin:0;
}
.mm-card-point-row{
  display:flex;
  align-items:flex-start;
  gap:10px;
}
.mm-card-point-bullet{
  width:7px;
  height:7px;
  border-radius:50%;
  background:var(--card-border);
  margin-top:9px;
  flex-shrink:0;
}
.mm-card-point-text{
  flex:1;
  color:#1B2A41;
}

/* Figure Chips */
.chip-amt{
  display:inline-block;
  background:#FFE066;
  color:#2B2500;
  border:1px solid #FCC419;
  padding:2px 8px;
  border-radius:6px;
  font-weight:700;
  font-family:var(--f-mono);
  font-size:.92em;
  letter-spacing:.02em;
}
.chip-rate{
  display:inline-block;
  background:#E5DBFF;
  color:#5F3DC4;
  border:1px solid #D0BFFF;
  padding:2px 8px;
  border-radius:6px;
  font-weight:700;
  font-family:var(--f-mono);
  font-size:.92em;
}
.chip-sec{
  display:inline-block;
  background:#D0EBFF;
  color:#1864AB;
  border:1px solid #A5D8FF;
  padding:2px 8px;
  border-radius:6px;
  font-weight:700;
  font-family:var(--f-mono);
  font-size:.92em;
}
.chip-key{
  display:inline-block;
  font-weight:700;
  color:#1B2A41;
}

/* Full Slab Tables with Right-Aligned Tabular Numbers */
.mm-table-panel{
  margin-top:10px;
  width:100%;
  overflow-x:auto;
  background:#FFFFFF;
  border:1.5px solid #CBD5E1;
  border-radius:12px;
  padding:12px 16px;
  box-sizing:border-box;
}
.mm-table-title{
  font-size:.94rem;
  font-weight:800;
  color:#0F172A;
  margin-bottom:10px;
}
.mm-stat-table{
  width:100%;
  border-collapse:collapse;
  font-size:.92rem;
}
.mm-stat-table th{
  font-weight:800;
  color:#1E293B;
  border-bottom:2px solid #CBD5E1;
  padding:9px 12px;
  font-family:var(--f-display);
}
.mm-stat-table td{
  padding:9px 12px;
  border-bottom:1px solid #E2E8F0;
  color:#1E293B;
}
.mm-stat-table tr:last-child td{
  border-bottom:none;
}
.cell-mono{
  font-family:var(--f-mono);
  font-weight:700;
  letter-spacing:.02em;
}
.text-right{
  text-align:right !important;
}
.text-left{
  text-align:left !important;
}

/* Worked Calculation Example in Soft Green Panel */
.mm-example-panel{
  margin-top:10px;
  width:100%;
  background:#E9F8EF;
  border:1.5px solid #12A150;
  border-radius:14px;
  padding:16px 20px;
  box-sizing:border-box;
}
.mm-example-head{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:12px;
  flex-wrap:wrap;
}
.mm-example-tag{
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:800;
  background:#12A150;
  color:#FFFFFF;
  padding:3px 10px;
  border-radius:6px;
}
.mm-example-title{
  font-size:.96rem;
  font-weight:800;
  color:#0B5B31;
}
.mm-example-inputs{
  font-size:.92rem;
  color:#1B2A41;
  margin-bottom:10px;
  background:rgba(255,255,255,0.7);
  padding:8px 12px;
  border-radius:8px;
}
.mm-example-steps{
  display:flex;
  flex-direction:column;
  gap:8px;
}
.mm-example-step-line{
  display:flex;
  align-items:flex-start;
  gap:8px;
  font-size:.94rem;
  color:#1B2A41;
  line-height:1.45;
}
.step-bullet{
  color:#12A150;
  font-weight:800;
}
.mm-example-step-line:last-child{
  font-weight:800;
  color:#0B5B31;
  margin-top:4px;
  padding-top:6px;
  border-top:1px dashed #A7F3D0;
}

/* Trap Card Panel: Mistake vs Statutory Rule */
.mm-trap-panel{
  margin-top:8px;
  display:flex;
  flex-direction:column;
  gap:12px;
  width:100%;
}
.mm-trap-row{
  display:flex;
  flex-direction:column;
  gap:6px;
  padding:12px 16px;
  border-radius:10px;
}
.mm-trap-row.wrong{
  background:#FFF5F5;
  border:1px solid #FFA8A8;
}
.mm-trap-row.correct{
  background:#E9F8EF;
  border:1px solid #8CE99A;
}
.mm-trap-badge{
  font-family:var(--f-mono);
  font-size:.70rem;
  font-weight:800;
  padding:2px 8px;
  border-radius:6px;
  display:inline-block;
  align-self:flex-start;
}
.mm-trap-badge.wrong{
  background:#FA5252;
  color:#FFFFFF;
}
.mm-trap-badge.correct{
  background:#12A150;
  color:#FFFFFF;
}
.mm-trap-text{
  font-size:.94rem;
  line-height:1.45;
  color:#1B2A41;
}

/* 4. Flow Summary Pill & Step Boxes */
.mm-flow-pill{
  display:inline-flex;
  align-items:center;
  gap:10px;
  background:#1C7ED6;
  border:1.5px solid #1864AB;
  border-radius:999px;
  padding:8px 22px;
  color:#FFFFFF;
  font-size:.86rem;
  font-weight:800;
  letter-spacing:.03em;
  box-shadow:0 4px 16px rgba(28,126,214,0.25);
  transition:all .25s ease;
  z-index:3;
}
.mm-flow-pill.status-flow-hidden{
  visibility:hidden;
  opacity:0;
  pointer-events:none;
}
.mm-flow-pill.status-flow-active{
  visibility:visible;
  opacity:1;
  box-shadow:0 0 20px rgba(28,126,214,0.5);
}
.mm-flow-pill.status-flow-done{
  visibility:visible;
  opacity:1;
  background:#0B5B31;
  border-color:#12A150;
}

.mm-flow-steps-row{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:14px;
  width:100%;
  flex-wrap:wrap;
  margin-top:2px;
}
.mm-flow-step-box{
  background:#FFFFFF;
  border:1.5px solid #CBD5E1;
  border-radius:14px;
  padding:12px 18px;
  min-width:160px;
  max-width:260px;
  display:flex;
  flex-direction:column;
  gap:4px;
  box-shadow:0 4px 12px rgba(0,0,0,0.05);
  transition:all .25s ease;
  box-sizing:border-box;
}
.mm-flow-step-box.status-hidden{
  visibility:hidden;
  opacity:0;
  pointer-events:none;
}
.mm-flow-step-box.status-active{
  visibility:visible;
  opacity:1;
  border-color:#1C7ED6;
  box-shadow:0 0 18px rgba(28,126,214,0.45);
  transform:scale(1.03);
}
.mm-flow-step-box.status-done{
  visibility:visible;
  opacity:1;
  border-color:#12A150;
}
.mm-fs-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.mm-fs-icon{
  width:24px;
  height:24px;
  border-radius:50%;
  background:rgba(28,126,214,0.12);
  display:grid;
  place-items:center;
  color:#1C7ED6;
}
.status-done .mm-fs-icon{
  background:rgba(18,161,80,0.12);
  color:#12A150;
}
.mm-fs-num{
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
  color:#64748B;
}
.mm-fs-label{
  font-size:.96rem;
  font-weight:800;
  color:#0F172A;
  line-height:1.3;
}
.mm-fs-sub{
  font-size:14px;
  color:#64748B;
  font-weight:600;
}
.mm-fs-arrow{
  display:grid;
  place-items:center;
  color:#94A3B8;
}

/* Subtitle Bar: Exact Spoken Sentence */
.mm-live-bar{
  position:absolute;
  bottom:64px; /* directly above 64px dock */
  left:0;
  right:0;
  background:rgba(15,23,42,0.92);
  backdrop-filter:blur(10px);
  border-top:1px solid rgba(255,255,255,0.12);
  padding:12px 24px;
  display:flex;
  align-items:center;
  gap:16px;
  z-index:20;
  box-sizing:border-box;
  box-shadow:0 -4px 20px rgba(0,0,0,0.25);
  transition:transform .3s ease, opacity .3s ease;
}
.vtheater.controls-hidden .mm-live-bar{
  transform:translateY(100%);
  opacity:0;
  pointer-events:none;
}
.mm-live-badge{
  display:inline-flex;
  align-items:center;
  gap:6px;
  font-family:var(--f-mono);
  font-size:.70rem;
  font-weight:800;
  background:#0284C7;
  color:#FFFFFF;
  padding:3px 10px;
  border-radius:999px;
  white-space:nowrap;
  flex-shrink:0;
}
.mm-live-text{
  font-size:1.02rem;
  font-weight:600;
  color:#F8FAFC;
  line-height:1.45;
  flex:1;
  white-space:normal;
}
/* ===== End Mind Map Theater Styles ===== */
"""

# Replace or inject the CSS block
if css_target_start in content and css_target_end in content:
    pattern = re.compile(re.escape(css_target_start) + r".*?" + re.escape(css_target_end), re.DOTALL)
    content = pattern.sub(new_css.strip(), content)
    print("[OK] Replaced existing Mind Map CSS block")
else:
    # Inject before </style>
    style_end = "</style>"
    if style_end in content:
        content = content.replace(style_end, new_css + "\n" + style_end, 1)
        print("[OK] Injected new Mind Map CSS block before </style>")
    else:
        print("[WARN] Could not find </style> to inject CSS")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Successfully updated CSS in index.html")
