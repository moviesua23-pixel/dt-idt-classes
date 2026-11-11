import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

app = FastAPI(title="TaxMaster Modern API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount("/data/audio", StaticFiles(directory=AUDIO_DIR), name="data_audio")

VIDEO_DIR = os.path.join(DATA_DIR, "video")
os.makedirs(VIDEO_DIR, exist_ok=True)
app.mount("/data/video", StaticFiles(directory=VIDEO_DIR), name="data_video")

def load_json(name):
    p = os.path.join(DATA_DIR, name)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

AUDIO_V2_DIR = os.path.join(DATA_DIR, "audio_v2")
os.makedirs(AUDIO_V2_DIR, exist_ok=True)
app.mount("/data/audio_v2", StaticFiles(directory=AUDIO_V2_DIR), name="data_audio_v2")

@app.get("/api/data")
def get_all_data():
    mm = load_json("mindmaps.json") or {}
    overrides = load_json("mindmap_timing_overrides.json") or {}
    
    # Merge overrides into mindmaps so overrides are applied last
    for topic, beats in overrides.items():
        if topic in mm and "branches" in mm[topic]:
            for b in mm[topic]["branches"]:
                for pt in b.get("points", []):
                    pt_id = pt.get("id")
                    if pt_id in beats:
                        pt["t0"] = beats[pt_id]["t0"]
                        pt["t1"] = beats[pt_id]["t1"]
                
    return {
        "catalog": load_json("catalog.json") or {"chapters": []},
        "questions": load_json("extracted_qna.json") or [],
        "provisions": load_json("provisions.json") or [],
        "storyboards": load_json("ppt_storyboards.json") or {},
        "mindmaps": mm,
        "timing_overrides": overrides
    }

from pydantic import BaseModel

class OverridePayload(BaseModel):
    topic: str
    overrides: dict

@app.post("/api/timing-overrides")
def save_timing_overrides(payload: OverridePayload):
    p = os.path.join(DATA_DIR, "mindmap_timing_overrides.json")
    all_overrides = {}
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                all_overrides = json.load(f)
        except Exception:
            all_overrides = {}
    
    all_overrides[payload.topic] = payload.overrides
    with open(p, "w", encoding="utf-8") as f:
        json.dump(all_overrides, f, indent=2, ensure_ascii=False)
    
    return {"status": "ok", "saved_beats": len(payload.overrides)}

@app.get("/sync-tuner", response_class=HTMLResponse)
def sync_tuner():
    tuner_file = os.path.join(FRONTEND_DIR, "sync_tuner.html")
    if os.path.exists(tuner_file):
        with open(tuner_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Sync Tuner Not Found</h1>"

@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/video/{filename}")
def get_video(filename: str):
    file_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video file not found")

@app.get("/", response_class=HTMLResponse)
def index():
    html_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>TaxMaster Frontend Building...</h1>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8502)
