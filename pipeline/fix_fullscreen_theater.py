import os
import re

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'index.html')
with open(frontend_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .vtheater and .vtheater.vfullscreen CSS
css_old = """.vtheater.vfullscreen{
  position:fixed !important;
  inset:0 !important;
  width:100vw !important;
  height:100vh !important;
  max-height:100vh !important;
  z-index:999999 !important;
  margin:0 !important;
  border-radius:0 !important;
  border:0 !important;
  background:#FFFFFF !important;
  display:flex !important;
  flex-direction:column !important;
  box-shadow:none !important;
  overflow-y:auto !important;
}"""

css_new = """.vtheater.vfullscreen{
  position:fixed !important;
  top:0 !important;
  left:0 !important;
  right:0 !important;
  bottom:0 !important;
  width:100vw !important;
  height:100vh !important;
  max-height:100vh !important;
  z-index:2147483647 !important;
  margin:0 !important;
  border-radius:0 !important;
  border:0 !important;
  background:#0B1120 !important;
  display:flex !important;
  flex-direction:column !important;
  box-shadow:none !important;
  overflow:hidden !important;
}
.vfullscreen-stage{
  flex:1;
  overflow-y:auto;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:24px 20px 80px;
  background:#F1F5F9;
}
@media (min-width: 1024px){
  .vfullscreen-stage{
    padding:36px 40px 90px;
  }
}"""

if css_old in html:
    html = html.replace(css_old, css_new)
    print("Updated CSS fullscreen styles successfully!")
else:
    print("css_old not matched")

# 2. Update .ppt-nav-rail and .ppt-nav-dot to avoid squishing
nav_css_old = """.ppt-nav-rail{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:16px;
  padding:0 4px;
}
.ppt-nav-dot{
  flex:1;
  display:flex;
  flex-direction:column;
  gap:6px;
  background:none;
  border:0;
  padding:6px 0;
  cursor:pointer;
  text-align:left;
  transition:all .25s ease;
}
.ppt-dot-bar{
  height:5px;
  border-radius:999px;
  background:#E2E8F0;
  transition:background .35s ease, transform .35s cubic-bezier(.16,1,.3,1);
}
.ppt-nav-dot.active .ppt-dot-bar{
  background:#2563EB;
  transform:scaleY(1.4);
}
.ppt-nav-dot.past .ppt-dot-bar{
  background:#93C5FD;
}
.ppt-dot-label{
  font-family:var(--f-mono);
  font-size:.74rem;
  font-weight:600;
  color:#64748B;
  transition:color .25s ease;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.ppt-nav-dot.active .ppt-dot-label{
  color:#2563EB;
  font-weight:700;
}"""

nav_css_new = """.ppt-nav-rail{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:20px;
  width:100%;
  max-width:1200px;
  overflow-x:auto;
  padding:4px 2px;
}
.ppt-nav-dot{
  flex:1;
  min-width:140px;
  max-width:280px;
  display:flex;
  flex-direction:column;
  gap:4px;
  background:#FFFFFF;
  border:1.5px solid #E2E8F0;
  border-radius:12px;
  padding:8px 14px;
  cursor:pointer;
  text-align:left;
  transition:all .25s cubic-bezier(.16,1,.3,1);
  box-shadow:0 1px 3px rgba(0,0,0,0.03);
}
.ppt-nav-dot:hover{
  border-color:#CBD5E1;
  background:#F8FAFC;
}
.ppt-nav-dot.active{
  background:#EFF6FF;
  border:2px solid #2563EB;
  box-shadow:0 4px 14px rgba(37,99,235,0.15);
  transform:translateY(-2px);
}
.ppt-dot-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.ppt-dot-badge{
  font-family:var(--f-mono);
  font-size:.7rem;
  font-weight:700;
  color:#64748B;
}
.ppt-nav-dot.active .ppt-dot-badge{
  color:#2563EB;
}
.ppt-dot-bar{
  width:8px;
  height:8px;
  border-radius:50%;
  background:#CBD5E1;
  transition:background .25s ease, transform .25s ease;
}
.ppt-nav-dot.active .ppt-dot-bar{
  background:#2563EB;
  transform:scale(1.25);
  box-shadow:0 0 0 3px rgba(37,99,235,0.25);
}
.ppt-nav-dot.past .ppt-dot-bar{
  background:#93C5FD;
}
.ppt-dot-label{
  font-size:.82rem;
  font-weight:700;
  color:#0F172A;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  display:block;
  max-width:100%;
}
.ppt-nav-dot.active .ppt-dot-label{
  color:#1D4ED8;
}"""

if nav_css_old in html:
    html = html.replace(nav_css_old, nav_css_new)
    print("Updated nav rail CSS successfully!")
else:
    print("nav_css_old not matched")

# 3. Update .ppt-viewport CSS for clean 16:9 keynote slide appearance
viewport_css_old = """.ppt-viewport{
  position:relative;
  min-height:480px;
  width:100%;
  border-radius:20px;
  background:#FFFFFF;
  border:1px solid #E2E8F0;
  box-shadow:0 6px 28px rgba(0,0,0,0.04);
  padding:32px 36px;
  overflow:hidden;
}"""

viewport_css_new = """.ppt-viewport{
  position:relative;
  min-height:500px;
  width:100%;
  max-width:1200px;
  margin:0 auto;
  border-radius:24px;
  background:#FFFFFF;
  border:1px solid #E2E8F0;
  box-shadow:0 12px 40px rgba(15,23,42,0.07);
  padding:36px 42px;
  overflow:hidden;
  display:flex;
  flex-direction:column;
  justify-content:center;
}"""

if viewport_css_old in html:
    html = html.replace(viewport_css_old, viewport_css_new)
    print("Updated viewport CSS successfully!")
else:
    print("viewport_css_old not matched")

# 4. Update renderFlowchartHtml nav dot markup
rail_markup_old = """      <!-- Slide Progress Navigation Bar -->
      <div class="ppt-nav-rail" role="tablist">
        ${sb.slides.map((s, idx) => `
          <button class="ppt-nav-dot ${idx === 0 ? 'active' : ''}" data-t0="${s.t0 || 0}" data-slide-idx="${idx}" title="Slide ${s.slide_number}: ${esc(s.slide_title)}" aria-label="Go to slide ${s.slide_number}">
            <span class="ppt-dot-bar"></span>
            <span class="ppt-dot-label">Slide ${s.slide_number}: ${esc(s.slide_title)}</span>
          </button>
        `).join('')}
      </div>"""

rail_markup_new = """      <!-- Slide Progress Navigation Bar -->
      <div class="ppt-nav-rail" role="tablist">
        ${sb.slides.map((s, idx) => `
          <button class="ppt-nav-dot ${idx === 0 ? 'active' : ''}" data-t0="${s.t0 || 0}" data-slide-idx="${idx}" title="Slide ${s.slide_number}: ${esc(s.slide_title)}" aria-label="Go to slide ${s.slide_number}">
            <div class="ppt-dot-top">
              <span class="ppt-dot-badge">SLIDE ${s.slide_number}</span>
              <span class="ppt-dot-bar"></span>
            </div>
            <span class="ppt-dot-label">${esc(s.slide_title)}</span>
          </button>
        `).join('')}
      </div>"""

if rail_markup_old in html:
    html = html.replace(rail_markup_old, rail_markup_new)
    print("Updated rail markup successfully!")
else:
    print("rail_markup_old not matched")

# 5. Update vdiag wrap to use vfullscreen-stage
vdiag_old = """      <!-- View 1: Interactive Animated Presentation Slide (Only Explaining Slide) -->
      <div id="vdiag" class="vdiag-wrap" style="flex:1;overflow-y:auto;padding:24px">
        ${renderFlowchartHtml(q, p)}
      </div>"""

vdiag_new = """      <!-- View 1: Interactive Animated Presentation Slide (Only Explaining Slide) -->
      <div id="vdiag" class="vfullscreen-stage">
        ${renderFlowchartHtml(q, p)}
      </div>"""

if vdiag_old in html:
    html = html.replace(vdiag_old, vdiag_new)
    print("Updated vdiag wrap successfully!")
else:
    print("vdiag_old not matched")

# 6. Ensure vtheater is appended directly to document.body when opened!
# Look at start() in makePlayer
start_fn_old = """    if(vtheater){
     vtheater.classList.add("vfullscreen");
     vtheater.style.display = "flex";
     document.body.style.overflow = "hidden";
     if(fvideo){
      fvideo.currentTime = audio.currentTime;
      fvideo.playbackRate = speeds[si];
      fvideo.play().catch(()=>{});
     }
    }"""

start_fn_new = """    if(vtheater){
     if(vtheater.parentElement !== document.body){
      document.body.appendChild(vtheater);
     }
     vtheater.classList.add("vfullscreen");
     vtheater.style.display = "flex";
     document.body.style.overflow = "hidden";
     if(fvideo){
      fvideo.currentTime = audio.currentTime;
      fvideo.playbackRate = speeds[si];
      fvideo.play().catch(()=>{});
     }
    }"""

if start_fn_old in html:
    html = html.replace(start_fn_old, start_fn_new)
    print("Updated start() body append successfully!")
else:
    print("start_fn_old not matched")

# Also for vtog button
vtog_old = """    if(isShown){
     if(vtheater) vtheater.style.display = "none";
     if(fvideo) try { fvideo.pause(); } catch(e){}
    } else {
     if(vtheater) vtheater.style.display = "block";
     if(fvideo){
      fvideo.currentTime = audio.currentTime;
      fvideo.playbackRate = speeds[si];
      if(playing) fvideo.play().catch(()=>{});
     }
    }"""

vtog_new = """    if(isShown){
     stop();
    } else {
     if(vtheater){
      if(vtheater.parentElement !== document.body){
       document.body.appendChild(vtheater);
      }
      vtheater.classList.add("vfullscreen");
      vtheater.style.display = "flex";
      document.body.style.overflow = "hidden";
      if(!playing) start();
     }
    }"""

if vtog_old in html:
    html = html.replace(vtog_old, vtog_new)
    print("Updated vtog handler successfully!")
else:
    print("vtog_old not matched")

# In destroy, remove vtheater from body if attached
destroy_old = """ return {
  destroy(){
   dead = true;
   if(fvideo){
    try { fvideo.pause(); fvideo.src = ""; } catch(e){}
   }
   stop();
   window.removeEventListener("keydown", escListener);
   audio.src = "";
  }
 };"""

destroy_new = """ return {
  destroy(){
   dead = true;
   if(fvideo){
    try { fvideo.pause(); fvideo.src = ""; } catch(e){}
   }
   stop();
   window.removeEventListener("keydown", escListener);
   if(vtheater && vtheater.parentElement === document.body){
    vtheater.remove();
   }
   audio.src = "";
  }
 };"""

if destroy_old in html:
    html = html.replace(destroy_old, destroy_new)
    print("Updated destroy() cleanup successfully!")
else:
    print("destroy_old not matched")

with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved frontend/index.html with fullscreen body mount and clean responsive slide stage!")
