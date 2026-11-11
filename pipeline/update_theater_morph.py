import os

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'index.html')
with open(frontend_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace start(), stop(), ui(), and event listeners in makePlayer
start_block_old = """ async function start(){
  try {
   audio.playbackRate = speeds[si];
   await audio.play();
   playing = true;
   root.classList.add("playing");
   playB.innerHTML = I.pause;
   playB.setAttribute("aria-label", "Pause audio");
   note.textContent = "Playing Malayalam explainer: " + (p.doctrine || "Statutory Rule") + " · " + (p.voice || "Gemini Voice (Aoede)");
   if(vtheater){
    vtheater.style.display = "block";
    if(fvideo){
     fvideo.currentTime = audio.currentTime;
     fvideo.playbackRate = speeds[si];
     fvideo.play().catch(()=>{});
    }
   }
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
  if(fvideo){
   try { fvideo.pause(); } catch(e){}
  }
  if(vtheater){
   vtheater.style.display = "none";
  }
  cancelAnimationFrame(vraf);
  vizOff();
  root.classList.remove("playing");
  playB.innerHTML = I.play;
  playB.setAttribute("aria-label", "Play audio");
 }"""

start_block_new = """ async function start(){
  try {
   audio.playbackRate = speeds[si];
   await audio.play();
   playing = true;
   root.classList.add("playing");
   playB.innerHTML = I.pause;
   playB.setAttribute("aria-label", "Pause audio");
   note.textContent = "Playing Malayalam explainer: " + (p.doctrine || "Statutory Rule") + " · " + (p.voice || "Gemini Voice (Aoede)");
   if(vtheater){
    vtheater.classList.add("vfullscreen");
    vtheater.style.display = "flex";
    document.body.style.overflow = "hidden";
    if(fvideo){
     fvideo.currentTime = audio.currentTime;
     fvideo.playbackRate = speeds[si];
     fvideo.play().catch(()=>{});
    }
   }
   const vtdPlay = $("#vtd-play");
   if(vtdPlay) vtdPlay.innerHTML = I.pause;
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
  if(fvideo){
   try { fvideo.pause(); } catch(e){}
  }
  if(vtheater){
   vtheater.classList.remove("vfullscreen");
   vtheater.style.display = "none";
   document.body.style.overflow = "";
  }
  const vtdPlay = $("#vtd-play");
  if(vtdPlay) vtdPlay.innerHTML = I.play;
  cancelAnimationFrame(vraf);
  vizOff();
  root.classList.remove("playing");
  playB.innerHTML = I.play;
  playB.setAttribute("aria-label", "Play audio");
 }"""

if start_block_old in html:
    html = html.replace(start_block_old, start_block_new)
    print("Replaced start and stop successfully!")
else:
    print("start_block_old not found")

# Replace ui()
ui_old = """ function ui(){
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
  if(fvideo && !fvideo.paused && Math.abs(fvideo.currentTime - cur) > 0.35){
   fvideo.currentTime = cur;
  }
  syncFlowchart(cur);
 }"""

ui_new = """ function ui(){
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
  if(fvideo && !fvideo.paused && Math.abs(fvideo.currentTime - cur) > 0.35){
   fvideo.currentTime = cur;
  }
  const vtdTime = $("#vtd-time");
  if(vtdTime) vtdTime.textContent = fmt(cur) + " / " + fmt(T);
  const vtdSeek = $("#vtd-seek");
  if(vtdSeek) vtdSeek.value = Math.round(f * 1000);
  const vtdPlay = $("#vtd-play");
  if(vtdPlay) vtdPlay.innerHTML = playing ? I.pause : I.play;
  syncFlowchart(cur);
 }"""

if ui_old in html:
    html = html.replace(ui_old, ui_new)
    print("Replaced ui() successfully!")
else:
    print("ui_old not found")

# Replace wire up section
wire_old = """ note.textContent = "Spoken Malayalam audio explainer · " + (p.voice || "Gemini Voice (Aoede)");
 ui();

 return {
  destroy(){
   dead = true;
   if(fvideo){
    try { fvideo.pause(); fvideo.src = ""; } catch(e){}
   }
   stop();
   audio.src = "";
  }
 };
}"""

wire_new = """ // Wire up slide nav dots for instant slide-to-slide jump
 $$(".ppt-nav-dot").forEach(dot => {
  dot.onclick = (e) => {
   e.stopPropagation();
   const t0 = parseFloat(dot.dataset.t0 || "0");
   audio.currentTime = t0;
   if(fvideo) fvideo.currentTime = t0;
   if(!playing) start();
   ui();
  };
 });

 // Wire up dock controls in fullscreen presentation
 const vtdPlay = $("#vtd-play");
 if(vtdPlay) vtdPlay.onclick = togglePlay;
 const vtdSeek = $("#vtd-seek");
 if(vtdSeek){
  vtdSeek.oninput = () => {
   const T = total();
   const target = (vtdSeek.value / 1000) * T;
   if(isFinite(target)){
    audio.currentTime = target;
    if(fvideo) fvideo.currentTime = target;
   }
   ui();
  };
 }
 const vtdSpeed = $("#vtd-speed");
 if(vtdSpeed){
  vtdSpeed.onclick = () => {
   si = (si + 1) % speeds.length;
   const txt = speeds[si] === 1 ? "1.0x" : speeds[si] + "x";
   spd.textContent = txt;
   vtdSpeed.textContent = txt;
   audio.playbackRate = speeds[si];
   if(fvideo) fvideo.playbackRate = speeds[si];
  };
 }
 const vtdClose = $("#vtd-close");
 if(vtdClose) vtdClose.onclick = stop;

 // Escape key exits fullscreen presentation
 const escListener = (e) => {
  if(e.key === "Escape" && vtheater && vtheater.classList.contains("vfullscreen")){
   stop();
  }
 };
 window.addEventListener("keydown", escListener);

 note.textContent = "Spoken Malayalam audio explainer · " + (p.voice || "Gemini Voice (Aoede)");
 ui();

 return {
  destroy(){
   dead = true;
   if(fvideo){
    try { fvideo.pause(); fvideo.src = ""; } catch(e){}
   }
   stop();
   window.removeEventListener("keydown", escListener);
   audio.src = "";
  }
 };
}"""

if wire_old in html:
    html = html.replace(wire_old, wire_new)
    print("Replaced wire section successfully!")
else:
    print("wire_old not found")

with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved index.html successfully!")
