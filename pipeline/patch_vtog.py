import os

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'index.html')
with open(frontend_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('if(vtog)')
if idx == -1:
    print('vtog not found!')
    exit(1)

# Find the matching closing bracket for if(vtog)
end_idx = text.find('if(vclose)', idx)
if end_idx == -1:
    print('if(vclose) not found!')
    exit(1)

replacement = """if(vtog){
  vtog.onclick = () => {
   const isShown = vtheater && vtheater.style.display !== "none";
   if(isShown){
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
   }
  };
 }

 """

text = text[:idx] + replacement + text[end_idx:]
with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("vtog successfully replaced and saved!")
