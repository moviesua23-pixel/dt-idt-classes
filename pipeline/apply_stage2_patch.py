import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(PROJECT_ROOT, "frontend", "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update .vtheater background from #070B14 to #F4F7FB
vth_old = "background:#070B14 !important;"
vth_new = "background:#F4F7FB !important;"
assert vth_old in text, "Could not find vtheater background"
text = text.replace(vth_old, vth_new, 1)
print("[OK] Updated .vtheater background to #F4F7FB")

# 2. Update CSS for cards, themes, chips, and visibility rules
css_start_str = "/* Root Card at Top */"
css_end_str = "/* Full Slab Tables */"

pos1 = text.find(css_start_str)
pos2 = text.find(css_end_str, pos1)
assert pos1 != -1 and pos2 != -1, f"CSS bounds not found ({pos1}, {pos2})"

new_css = """/* Root Card at Top */
.mm-root-card{
  width:clamp(340px, 60vw, 780px);
  max-width:100%;
  margin:0 auto;
  background:#0F172A;
  border:2px solid #38BDF8;
  border-radius:20px;
  padding:16px 24px;
  color:#FFFFFF;
  position:relative;
  box-shadow:0 10px 25px rgba(15,23,42,0.12);
  cursor:pointer;
  transition:transform .25s, box-shadow .25s;
  box-sizing:border-box;
  z-index:2;
  text-align:center;
}
.mm-root-card:hover{
  transform:translateY(-2px);
  box-shadow:0 14px 35px rgba(56,189,248,0.25);
}
.mm-root-top-row{
  display:inline-flex;
  align-items:center;
  gap:10px;
  margin-bottom:6px;
}
.mm-root-badge{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:800;
  color:#38BDF8;
  background:rgba(56,189,248,0.15);
  border:1px solid rgba(56,189,248,0.35);
  padding:3px 10px;
  border-radius:6px;
}
.mm-root-step-tag{
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
  color:#94A3B8;
  letter-spacing:.05em;
}
.mm-root-title{
  font-size:1.24rem;
  font-weight:800;
  line-height:1.35;
  color:#FFFFFF;
}

/* ===== Infographic Block Architecture ===== */
.mm-infographic-block{
  width:100%;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:24px;
  position:relative;
  z-index:2;
  transition:all .3s cubic-bezier(.16,1,.3,1);
  box-sizing:border-box;
}

/* 1. Section Title Pill (Dark Navy, Centered, Icon, Badge, Accent Underline) */
.mm-block-pill{
  display:inline-flex;
  align-items:center;
  gap:14px;
  background:#0F172A;
  border:1.5px solid #334155;
  border-radius:999px;
  padding:10px 26px;
  color:#FFFFFF;
  position:relative;
  cursor:pointer;
  box-shadow:0 8px 24px rgba(15,23,42,0.15);
  transition:all .25s ease;
  z-index:3;
  max-width:92%;
}
.mm-block-pill:hover{
  border-color:#38BDF8;
  transform:translateY(-1px);
  box-shadow:0 12px 30px rgba(56,189,248,0.22);
}
.mm-infographic-block.status-active .mm-block-pill{
  border-color:#38BDF8;
  box-shadow:0 0 24px rgba(56,189,248,0.35);
}
.mm-infographic-block.status-mastered .mm-block-pill{
  border-color:#12A150;
}
.mm-bp-icon-badge{
  width:32px;
  height:32px;
  border-radius:50%;
  background:rgba(56,189,248,0.15);
  border:1px solid rgba(56,189,248,0.35);
  display:grid;
  place-items:center;
  flex-shrink:0;
  color:#38BDF8;
}
.mm-bp-step{
  font-family:var(--f-mono);
  font-size:.72rem;
  font-weight:800;
  color:#38BDF8;
  background:rgba(56,189,248,0.18);
  border:1px solid rgba(56,189,248,0.35);
  padding:3px 8px;
  border-radius:6px;
  letter-spacing:.04em;
  white-space:nowrap;
}
.mm-bp-title{
  font-size:1.05rem;
  font-weight:800;
  color:#FFFFFF;
  letter-spacing:-.01em;
  white-space:nowrap;
}
.mm-bp-badge{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:700;
  color:#94A3B8;
  background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.12);
  padding:3px 10px;
  border-radius:6px;
  white-space:nowrap;
}
.mm-bp-underline{
  position:absolute;
  bottom:-2px;
  left:24px;
  right:24px;
  height:2px;
  background:linear-gradient(90deg, transparent, #38BDF8, transparent);
  border-radius:999px;
}

/* 2. Point Cards Row (3 per row desktop, 2 tablet, 1 phone) */
.mm-cards-row{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(290px, 1fr));
  gap:24px;
  width:100%;
  box-sizing:border-box;
  margin-top:6px;
  align-items:stretch;
}

/* 3. Infographic Card Structure (20px radius, 2px colored border, soft tinted fill) */
.mm-infographic-card{
  border-radius:20px;
  border:2px solid #CBD5E1;
  position:relative;
  box-shadow:0 6px 20px rgba(0,0,0,0.06);
  transition:border-color .28s ease, box-shadow .28s ease, opacity .28s ease, transform .28s ease;
  box-sizing:border-box;
  display:flex;
  flex-direction:column;
  cursor:pointer;
  overflow:visible;
  margin-top:16px; /* clearance for overlapping circular icon badge */
}
.mm-infographic-card.card-fullwidth{
  grid-column:1 / -1;
}
.mm-infographic-card:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 28px rgba(0,0,0,0.1);
}

/* 56px circular white icon badge with colored ring overlapping top-left */
.mm-card-icon-badge{
  position:absolute;
  top:-22px;
  left:20px;
  width:52px;
  height:52px;
  border-radius:50%;
  display:grid;
  place-items:center;
  background:#FFFFFF;
  box-shadow:0 4px 14px rgba(0,0,0,0.12);
  z-index:5;
}

/* Colored Header Ribbon with Card Title (Wraps to 2 lines, NEVER truncated) */
.mm-card-ribbon{
  border-radius:18px 18px 0 0;
  padding:12px 18px 12px 82px; /* clearance for 52px icon badge */
  display:flex;
  align-items:center;
  justify-content:space-between;
  color:#FFFFFF;
  min-height:52px;
  box-sizing:border-box;
}
.mm-card-title{
  flex:1;
  white-space:normal;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:hidden;
  font-weight:800;
  font-size:1.02rem;
  line-height:1.26;
  color:#FFFFFF;
}

/* Separate Live Strip at Top Right */
.mm-card-live-strip{
  position:absolute;
  top:10px;
  right:14px;
  font-family:var(--f-mono);
  font-size:.68rem;
  font-weight:800;
  padding:3px 10px;
  border-radius:999px;
  letter-spacing:.05em;
  z-index:6;
  display:none;
}
.mm-card-live-strip.tag-active{
  display:inline-flex;
  align-items:center;
  background:#FEF08A;
  color:#854D0E;
  border:1px solid #FDE047;
  box-shadow:0 2px 8px rgba(250,204,21,0.4);
}
.mm-card-live-strip.tag-done{
  display:inline-flex;
  align-items:center;
  background:rgba(255,255,255,0.25);
  color:#FFFFFF;
}
.mm-card-live-strip.tag-ref{
  display:inline-flex;
  align-items:center;
  background:#E2E8F0;
  color:#475569;
}

/* Exact Palette Theme Variants (Green, Orange, Purple, Blue, Teal, Trap) */
.theme-green{
  background:#E9F8EF !important;
  border-color:#12A150 !important;
}
.theme-green .mm-card-icon-badge{
  border:3px solid #12A150 !important;
  color:#12A150 !important;
}
.theme-green .mm-card-ribbon{
  background:#12A150 !important;
}

.theme-orange{
  background:#FFF1E6 !important;
  border-color:#E8590C !important;
}
.theme-orange .mm-card-icon-badge{
  border:3px solid #E8590C !important;
  color:#E8590C !important;
}
.theme-orange .mm-card-ribbon{
  background:#E8590C !important;
}

.theme-purple{
  background:#F3EDFF !important;
  border-color:#7048E8 !important;
}
.theme-purple .mm-card-icon-badge{
  border:3px solid #7048E8 !important;
  color:#7048E8 !important;
}
.theme-purple .mm-card-ribbon{
  background:#7048E8 !important;
}

.theme-blue{
  background:#E7F1FF !important;
  border-color:#1C7ED6 !important;
}
.theme-blue .mm-card-icon-badge{
  border:3px solid #1C7ED6 !important;
  color:#1C7ED6 !important;
}
.theme-blue .mm-card-ribbon{
  background:#1C7ED6 !important;
}

.theme-teal{
  background:#E6FCF5 !important;
  border-color:#0CA678 !important;
}
.theme-teal .mm-card-icon-badge{
  border:3px solid #0CA678 !important;
  color:#0CA678 !important;
}
.theme-teal .mm-card-ribbon{
  background:#0CA678 !important;
}

.theme-trap{
  background:#FFF5F5 !important;
  border-color:#FA5252 !important;
}
.theme-trap .mm-card-icon-badge{
  border:3px solid #FA5252 !important;
  color:#FA5252 !important;
}
.theme-trap .mm-card-ribbon{
  background:#FA5252 !important;
}

/* Card Reveal & State Rules */
.mm-infographic-card.status-hidden{
  visibility:hidden !important;
  opacity:0 !important;
  pointer-events:none !important;
}
.mm-infographic-card.status-active{
  visibility:visible !important;
  opacity:1 !important;
  box-shadow:0 12px 36px rgba(0,0,0,0.16), 0 0 0 3.5px rgba(56,189,248,0.6) !important;
  transform:translateY(-4px) scale(1.01);
  transition:transform .25s cubic-bezier(.16,1,.3,1), box-shadow .25s, opacity .25s;
  z-index:4;
}
.mm-infographic-card.status-done{
  visibility:visible !important;
  opacity:0.98 !important;
  transform:none;
}
.mm-infographic-card.status-reference{
  visibility:visible !important;
  opacity:0.94 !important;
}

/* Card Body (Clear 16px text #1E293B, line-height 1.6) */
.mm-card-body{
  padding:18px 20px;
  font-size:16px;
  line-height:1.6;
  color:#1E293B;
  display:flex;
  flex-direction:column;
  gap:10px;
  flex:1;
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
  width:6px;
  height:6px;
  border-radius:50%;
  background:#3B82F6;
  margin-top:9px;
  flex-shrink:0;
}
.mm-card-point-text{
  flex:1;
}

/* Figure Chips (Amounts Yellow #FFE066, Rates Purple, Sections Blue) */
.chip-amt{
  display:inline-block;
  background:#FEF08A;
  color:#713F12;
  border:1px solid #FDE047;
  padding:1px 7px;
  border-radius:6px;
  font-weight:800;
  font-family:var(--f-mono);
  font-size:.92em;
}
.chip-rate{
  display:inline-block;
  background:#F3E8FF;
  color:#581C87;
  border:1px solid #D8B4FE;
  padding:1px 7px;
  border-radius:6px;
  font-weight:800;
  font-family:var(--f-mono);
  font-size:.92em;
}
.chip-sec{
  display:inline-block;
  background:#E0F2FE;
  color:#0369A1;
  border:1px solid #BAE6FD;
  padding:1px 7px;
  border-radius:6px;
  font-weight:800;
  font-family:var(--f-mono);
  font-size:.92em;
}

"""
text = text[:pos1] + new_css + text[pos2:]
print("[OK] Updated CSS with exact infographic styles, palettes, chips, and visibility rules")

# 3. Add data-node-id="${pt.id}" to card element in renderMindMapCanvasHtml
old_card_tag = 'data-point-id="${pt.id}"'
new_card_tag = 'data-node-id="${pt.id}" data-point-id="${pt.id}"'
text = text.replace(old_card_tag, new_card_tag)
print("[OK] Added data-node-id to card element")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Stage 2 patch successfully written to frontend/index.html")
