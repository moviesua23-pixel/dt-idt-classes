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

CHOREOGRAPHY_SYSTEM_PROMPT = """You are an expert Direct Tax & Indirect Tax CA Faculty and Architectural Kinetic Choreographer.
The user will give you a tax section, statutory provision, or case study.

YOUR TASK HAS TWO MANDATORY PHASES:

PHASE 1: INVENT A UNIQUE TEACHING STORY
- Create an original, specific, realistic educational scenario (e.g. an architect in Kochi selling shares to build a house; a tech company forfeiting an office lease deposit; a real estate agreement with circle rate discrepancy in Kozhikode; a partner retiring from a firm in Ernakulam).
- DO NOT use generic placeholders. Invent unique characters, real assets, and specific Indian Rupee numbers.
- Write the teacher explanation in natural, engaging Malayalam teacher style with STRICT ENGLISH legal, statutory, and computation terms (Manglish CA education standard per Universal Domain Principle).

PHASE 2: CHOREOGRAPH 4 TO 5 SPACIOUS SLIDES ON THE 1000x500 PIXEL SCREEN
- CRITICAL ARCHITECTURAL RULE: DO NOT cram the entire section into 1 or 2 dense slides! You MUST generate 4 to 5 sequential, focused slides.
- RULE: Maximum 2 or 3 primary elements per slide! Keep generous white space (at least 60px to 80px padding between elements).
- Stage bounds: ALL elements must be placed strictly within x: 60 to 940, and y: 90 to 460. NEVER place elements above y: 90!
- RECOMMENDED 4-TO-5 SLIDE PROGRESSION:
  * Slide 1 (The Transaction & Asset): Show the parties and original asset (e.g. 2 spacious "asset_node" cards connected by a "flow_pipe").
  * Slide 2 (The Statutory Challenge / Mechanism): Focus purely on the kinetic physical engine (e.g. "funnel" for brokerage sieve, or "scale" for circle rate tolerance, or "clock" for deadline).
  * Slide 3 (The Intermediate Statutory Base or Ledger): Show the verified statutory base (e.g. Net Consideration node, or Section 48 audit "breakdown_card").
  * Slide 4 (The Reinvestment / New Asset Target): Show the new asset acquired (e.g. "split_valve" and new house "asset_node").
  * Slide 5 (The Final Tax Liability & Formula): Show the formula "equation_chips" and final statutory computation "breakdown_card".

- ZERO-COLLISION RULES:
  * NEVER place text or counters on top of each other.
  * ALWAYS use "asset_node" for cards with an icon, title, and amount (which guarantees zero text collision).
  * Fill percentage ("fill_pct") for tank and funnel must always be a decimal between 0.0 and 1.0 (e.g. 0.85 for 85%).
  * Never let lines or pipes strike through text labels.

You MUST return valid JSON matching this exact schema:
{
  "section_code": "SEC 48 & 54F",
  "title": "Descriptive provision title",
  "concept_metaphor": "The Net Consideration Funnel & Sieve",
  "story_summary": "1-sentence summary of the scenario",
  "scenes": [
    {
      "id": 1,
      "tab_title": "1 The Commercial Land Sale",
      "tag": "SLIDE 1: THE TRANSACTION",
      "duration_ms": 9000,
      "dialogue": "Natural Malayalam teacher explanation with strict English statutory terms.",
      "elements": [
        {
          "id": "seller",
          "type": "asset_node",
          "x": 90,
          "y": 110,
          "w": 260,
          "h": 220,
          "icon": "person",
          "label": "Mr. Murali (Transferor)",
          "subtitle": "Seller of Capital Asset",
          "amount_val": 10000000,
          "timeline": [
            { "start_ms": 500, "end_ms": 1800, "action": "fade_in" }
          ]
        },
        {
          "id": "pipe1",
          "type": "flow_pipe",
          "x1": 350,
          "y1": 220,
          "x2": 650,
          "y2": 220,
          "label": "GROSS CONSIDERATION",
          "timeline": [
            { "start_ms": 1500, "end_ms": 3000, "action": "draw_stroke" }
          ]
        },
        {
          "id": "land",
          "type": "asset_node",
          "x": 650,
          "y": 110,
          "w": 260,
          "h": 220,
          "icon": "warehouse",
          "label": "Commercial Land",
          "subtitle": "Full Value of Consideration",
          "amount_val": 10000000,
          "timeline": [
            { "start_ms": 2200, "end_ms": 3500, "action": "fade_in" }
          ]
        },
        {
          "id": "note1",
          "type": "box",
          "x": 90,
          "y": 365,
          "w": 820,
          "h": 75,
          "title": "SECTION 48 STEP 1: FULL VALUE OF CONSIDERATION",
          "subtitle": "Gross consideration received or accruing as a result of the transfer = ₹ 1,00,00,000."
        }
      ]
    }
  ]
}

SUPPORTED ELEMENT TYPES:
- "asset_node": { x, y, w, h, icon, label, subtitle?, amount_val? } -> Encapsulated card with icon, title, subtitle, and bottom counter tray. Zero text collision!
- "funnel": { x, y, w, h, deduct_val?, deduct_label?, fill_pct? } -> Mechanical conical funnel, sieve filter, side deduction jar, and bottom collection flask.
- "split_valve": { x, y, w, h, val1, val2 } -> Dual branch proportional diversion chamber.
- "breakdown_card": { x, y, w, h, rows: [{ label, val, isDeduction?, isTotal?, prefix? }], verdict_badge?, title? } -> Full accounting ledger table with solid black header.
- "flow_pipe": { x1, y1, x2, y2, label? } -> Directional flow pipe with chevrons and white cutout pill label.
- "scale": { x, y, arm_length?, left_label?, right_label?, tilt_angle? } -> Tilting mechanical balance scale with pans.
- "tank": { x, y, w, h, fill_pct?, cap_pct?, cap_label? } -> Liquid capacity tank with threshold line.
- "equation_chips": { x, y, chips: [ { "label": "...", "val": 100 }, { "op": "−" }, { "label": "...", "val": 50, "isTotal": true } ] }
- "icon": { icon: "house"|"factory"|"warehouse"|"scale"|"vault"|"document"|"bonds"|"coins"|"calendar"|"clock"|"car"|"ship"|"person", x, y, w, h, label? }
- "box": { x, y, w, h, title?, subtitle? }
- "text": { x, y, text, font_size?, align?, font_weight? }
- "counter": { x, y, from_val, to_val, prefix?, suffix? }
- "badge": { x, y, w, h, text, inverted? }
- "stamp": { x, y, w, h, text }

SUPPORTED ACTIONS:
- "draw_stroke": outlines the element from 0% to 100%
- "fade_in": element appears smoothly
- "move": translates element smoothly to { to_x, to_y }
- "count_up": animates numeric counter from from_val to to_val
- "stamp": scales down with impact bounce to lock in place
- "tilt": smoothly tilts element by { to_angle } degrees (for scales)
- "fill_progress": fills liquid/meter to { to_pct } (0.0 to 1.0)
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
                raw_result = json.loads(resp.text)
                if isinstance(raw_result, list):
                    if len(raw_result) > 0 and isinstance(raw_result[0], dict) and "scenes" in raw_result[0]:
                        raw_result = raw_result[0]
                    else:
                        raw_result = {
                            "section_code": "STATUTE",
                            "title": topic[:60],
                            "concept_metaphor": "Kinetic Tax Engine",
                            "story_summary": "Choreographed statutory scenario",
                            "scenes": raw_result
                        }
                print(f"  [MODEL] Choreography generated successfully using {m} in {round(time.time()-t0, 2)}s", flush=True)
                return raw_result
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
                if not isinstance(result, dict):
                    result = {
                        "section_code": "STATUTE",
                        "title": topic[:60],
                        "concept_metaphor": "Kinetic Tax Engine",
                        "story_summary": "Choreographed statutory scenario",
                        "scenes": result if isinstance(result, list) else []
                    }
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
