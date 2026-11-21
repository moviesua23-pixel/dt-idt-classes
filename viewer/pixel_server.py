import http.server
import json
import os
import socketserver
import sys
import time
from urllib.parse import urlparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.key_rotator import KeyRotator
from google.genai import types

CHOREOGRAPHY_SYSTEM_PROMPT = """You are an expert Direct Tax & Indirect Tax CA Faculty and Creative Kinetic Choreographer.
The user will give you a tax section, statutory provision, or case study.

YOUR TASK HAS TWO MANDATORY PHASES:

PHASE 1: INVENT A UNIQUE TEACHING STORY
- Create an original, specific, realistic educational scenario (e.g. an architect in Kochi selling shares to build a house; a tech company forfeiting an office lease deposit; a real estate agreement with circle rate discrepancy in Kozhikode; a partner retiring from a firm in Ernakulam).
- DO NOT use the same generic scenario. Invent unique characters, real assets, and specific Indian Rupee numbers.
- Write the teacher explanation in natural, engaging Malayalam teacher style with STRICT ENGLISH legal, statutory, and computation terms (Manglish CA education standard per Universal Domain Principle).

PHASE 2: CHOREOGRAPH THE 1000x500 MONOCHROME PIXEL SCREEN
- You have complete freedom over the 1000x500 pixel canvas (0,0 to 1000,500). Pure white background (#FFFFFF) with black pixels (#000000).
- CRITICAL STAGE BOUNDS: The top header banner occupies y: 20 to 75. ALL elements must be placed strictly between y: 90 and y: 470, and x: 50 and x: 950.
- DO NOT use fixed templates or the same layout for every section.
- Design 3 to 4 sequential scenes where EVERY visual object and EVERY pixel movement matches the specific concept of this provision!
  * If the concept is valuation dispute / tolerance -> Choreograph a balancing scale tilting or comparison towers.
  * If the concept is deadline / time limit -> Choreograph a ticking countdown clock or milestone timeline.
  * If the concept is a statutory cap / overflow -> Choreograph an overflow tank or physical barrier stopper.
  * If the concept is proportional deduction -> Choreograph a ratio balance or asset being built brick-by-brick.
  * If the concept is diversion / TDS -> Choreograph a split diversion pipe.

You MUST return valid JSON matching this exact schema:
{
  "section_code": "SEC 50C",
  "title": "Descriptive provision title",
  "concept_metaphor": "e.g. The Safe Harbor Breach Scale",
  "story_summary": "1-sentence summary of the scenario",
  "scenes": [
    {
      "id": 1,
      "tab_title": "1 Transaction & Agreement",
      "tag": "SCENE 1: THE TRANSACTION",
      "duration_ms": 12000,
      "dialogue": "Natural Malayalam teacher explanation with strict English statutory terms.",
      "elements": [
        {
          "id": "elem1",
          "type": "icon",
          "icon": "document",
          "x": 200,
          "y": 180,
          "w": 90,
          "h": 110,
          "label": "Sale Agreement",
          "timeline": [
            { "start_ms": 500, "end_ms": 1500, "action": "draw_stroke" },
            { "start_ms": 3000, "end_ms": 4500, "action": "move", "to_x": 450, "to_y": 180 }
          ]
        },
        {
          "id": "elem2",
          "type": "box",
          "x": 650,
          "y": 160,
          "w": 250,
          "h": 120,
          "title": "Stamp Duty Value",
          "subtitle": "Sub-Registrar Circle Rate",
          "timeline": [
            { "start_ms": 2000, "end_ms": 3000, "action": "fade_in" }
          ]
        },
        {
          "id": "elem3",
          "type": "counter",
          "x": 670,
          "y": 240,
          "from_val": 0,
          "to_val": 11500000,
          "prefix": "₹ ",
          "timeline": [
            { "start_ms": 2500, "end_ms": 4000, "action": "count_up" }
          ]
        },
        {
          "id": "elem4",
          "type": "stamp",
          "x": 500,
          "y": 380,
          "w": 400,
          "h": 46,
          "text": "110% SAFE HARBOR EXCEEDED",
          "timeline": [
            { "start_ms": 7500, "end_ms": 8200, "action": "stamp" }
          ]
        }
      ]
    }
  ]
}

SUPPORTED ELEMENT TYPES:
- "icon": { icon: "house"|"factory"|"warehouse"|"scale"|"vault"|"document"|"bonds"|"coins"|"calendar"|"clock"|"car"|"ship"|"barrier"|"pipe_split"|"person"|"firm_circle", x, y, w, h, label, angle? }
- "box": { x, y, w, h, title, subtitle, fill_dither? }
- "text": { x, y, text, font_size?, align?, font_weight? }
- "counter": { x, y, from_val, to_val, prefix, suffix, font_size? }
- "badge": { x, y, w, h, text, inverted? }
- "line": { x1, y1, x2, y2, dashed?, label? }
- "scale": { x, y, pivot_y, left_val, right_val, left_label, right_label, tilt_angle, threshold_line? }
- "tank": { x, y, w, h, fill_pct, cap_pct, cap_label, overflow_label? }
- "equation_chips": { x, y, chips: [ { "label": "...", "val": 100 }, { "op": "−" }, ... ] }
- "stamp": { x, y, w, h, text }
- "polygon": { points: [[x1, y1], [x2, y2], ...], label? }

SUPPORTED ACTIONS:
- "draw_stroke": outlines the element from 0% to 100%
- "fade_in": element appears
- "move": translates element smoothly to { to_x, to_y }
- "count_up": animates numeric counter from from_val to to_val
- "stamp": scales down with impact bounce to lock in place
- "dissolve": breaks region into scattering pixel dots
- "particle_stream": streams dots from { from_x, from_y } to { to_x, to_y }
- "tilt": smoothly tilts element by { to_angle } degrees (for scales/gauges)
- "fill_progress": fills liquid/meter to { to_pct }
- "strike": draws an audit strike-through line across element
"""

rotator = None

def get_rotator():
    global rotator
    if rotator is None:
        rotator = KeyRotator()
    return rotator

def generate_pixel_presentation(topic: str):
    r = get_rotator()
    models_to_try = ["gemini-3-flash-preview", "gemini-3.6-flash", "gemini-3.1-flash-lite"]

    def _call(client):
        prompt = f"Choreograph an original educational story and millisecond pixel animation for this tax provision:\nTopic: {topic}"
        last_err = None
        for m in models_to_try:
            try:
                t0 = time.time()
                resp = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=CHOREOGRAPHY_SYSTEM_PROMPT,
                        response_mime_type="application/json"
                    )
                )
                print(f"  [MODEL] Choreography generated successfully using {m} in {round(time.time()-t0, 2)}s", flush=True)
                return json.loads(resp.text)
            except Exception as e:
                last_err = e
                print(f"  [MODEL] {m} failed: {e}. Trying next fast model...", flush=True)
        raise last_err
    
    return r.execute_with_retry(_call)

class PixelScreenHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/generate_pixel_presentation':
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                req_data = json.loads(body.decode('utf-8'))
                topic = req_data.get('topic', '').strip()

                if not topic:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'topic is required'}).encode('utf-8'))
                    return

                print(f"\n[PIXEL SERVER] Choreographing presentation for topic: {topic}", flush=True)
                result = generate_pixel_presentation(topic)
                print(f"[PIXEL SERVER] Choreography complete: {result.get('section_code')} - {result.get('title')} ({result.get('concept_metaphor')})", flush=True)

                resp_bytes = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.end_headers()
                self.wfile.write(resp_bytes)
            except (ConnectionResetError, ConnectionAbortedError):
                print(f"[PIXEL SERVER] Client disconnected early.", flush=True)
            except Exception as e:
                print(f"[PIXEL SERVER] Error: {e}", flush=True)
                err_bytes = json.dumps({'error': str(e)}).encode('utf-8')
                try:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', str(len(err_bytes)))
                    self.end_headers()
                    self.wfile.write(err_bytes)
                except Exception:
                    pass
        else:
            self.send_response(404)
            self.end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def run_server(port=8080):
    for p in [port, 8085, 8090, 8888]:
        try:
            httpd = ThreadingHTTPServer(("", p), PixelScreenHandler)
            print(f"\n========================================================")
            print(f" Pixel Screen Server running at http://localhost:{p}")
            print(f" Demo URL: http://localhost:{p}/viewer/pixel_screen_demo.html")
            print(f" API: POST http://localhost:{p}/api/generate_pixel_presentation")
            print(f"========================================================\n", flush=True)
            httpd.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e) or "10048" in str(e):
                print(f"Port {p} in use, trying next port...", flush=True)
                continue
            raise

if __name__ == "__main__":
    run_server(8080)
