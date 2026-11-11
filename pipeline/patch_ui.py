import os

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'index.html')
with open(frontend_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = ''' if(tabDiag && tabVid && vdiag && vvidwrap){
  tabDiag.onclick = () => {
   vdiag.style.display = "block";
   vvidwrap.style.display = "none";
   tabDiag.style.background = "var(--accent)";
   tabDiag.style.color = "#fff";
   tabVid.style.background = "rgba(255,255,255,0.06)";
   tabVid.style.color = "#94A3B8";
  };
  tabVid.onclick = () => {
   vdiag.style.display = "none";
   vvidwrap.style.display = "block";
   tabVid.style.background = "var(--accent)";
   tabVid.style.color = "#fff";
   tabDiag.style.background = "rgba(255,255,255,0.06)";
   tabDiag.style.color = "#94A3B8";
   if(fvideo){
    fvideo.currentTime = audio.currentTime;
    if(playing) fvideo.play().catch(()=>{});
   }
  };
 }'''

replacement = ''' if(tabDiag && tabVid && vdiag && vvidwrap){
  tabDiag.onclick = () => {
   vdiag.style.display = "block";
   vvidwrap.style.display = "none";
   tabDiag.style.background = "var(--accent)";
   tabDiag.style.color = "#fff";
   tabDiag.style.borderColor = "var(--accent)";
   tabVid.style.background = "#F8FAFC";
   tabVid.style.color = "#475569";
   tabVid.style.borderColor = "#CBD5E1";
  };
  tabVid.onclick = () => {
   vdiag.style.display = "none";
   vvidwrap.style.display = "block";
   tabVid.style.background = "var(--accent)";
   tabVid.style.color = "#fff";
   tabVid.style.borderColor = "var(--accent)";
   tabDiag.style.background = "#F8FAFC";
   tabDiag.style.color = "#475569";
   tabDiag.style.borderColor = "#CBD5E1";
   if(fvideo){
    fvideo.currentTime = audio.currentTime;
    if(playing) fvideo.play().catch(()=>{});
   }
  };
 }'''

if target in c:
    c = c.replace(target, replacement)
    with open(frontend_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated index.html tab styling successfully!")
else:
    print("target not found")
