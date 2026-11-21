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

PHASE 2: CHOREOGRAPH THE 1000x500 HIGH-DETAIL MONOCHROME PIXEL SCREEN
- You have complete freedom over the 1000x500 pixel canvas (0,0 to 1000,500). Pure white background (#FFFFFF) with crisp black pixels (#000000).
- CRITICAL STAGE BOUNDS:
  * Top header banner occupies y: 20 to 75. NEVER place anything above y: 90!
  * ALL stage elements MUST be strictly placed within: x: 50 to 950, and y: 90 to 470.
- 4-ZONE STAGE ARCHITECTURE (RECOMMENDED FOR HIGH VISUAL DENSITY):
  * Zone 1 (Left: x: 60 to 280, y: 95 to 280): Input / Source Asset (e.g. "asset_node" for original property, commercial plot, or gross receipts).
  * Zone 2 (Center: x: 320 to 660, y: 90 to 300): The Kinetic Physical Metaphor Engine (e.g. "funnel", "scale", "tank", "clock", or "barrier").
  * Zone 3 (Right: x: 700 to 940, y: 95 to 280): Output / Target Asset (e.g. "asset_node" for net consideration, new house, or TDS deposit).
  * Zone 4 (Bottom: x: 60 to 940, y: 310 to 460): Statutory Accounting Ledger ("breakdown_card" with multi-line calculations and total verdict badge).
- CRITICAL ZERO-COLLISION RULES:
  * NEVER place text or counters on top of each other.
  * For any asset that has an icon, title, and Rupee amount, ALWAYS use "asset_node" (which automatically encapsulates the icon, labels, and framed counter tray with guaranteed zero collision).
  * Do NOT leave the canvas sparse or empty. Fill the stage with the mechanical metaphor, connecting pipes/lines, and the statutory ledger card below!

You MUST return valid JSON matching this exact schema:
{
  "section_code": "SEC 48 & 54F",
  "title": "Descriptive provision title",
  "concept_metaphor": "The Net Consideration Funnel & Sieve",
  "story_summary": "1-sentence summary of the scenario",
  "scenes": [
    {
      "id": 1,
      "tab_title": "1 Net Consideration Funnel",
      "tag": "SCENE 1: THE NET CONSIDERATION FUNNEL",
      "duration_ms": 12000,
      "dialogue": "Natural Malayalam teacher explanation with strict English statutory terms.",
      "elements": [
        {
          "id": "source_asset",
          "type": "asset_node",
          "x": 60,
          "y": 95,
          "w": 220,
          "h": 180,
          "icon": "warehouse",
          "label": "Commercial Plot",
          "subtitle": "Gross Consideration",
          "amount_val": 10000000,
          "timeline": [
            { "start_ms": 500, "end_ms": 2000, "action": "fade_in" }
          ]
        },
        {
          "id": "funnel_engine",
          "type": "funnel",
          "x": 330,
          "y": 90,
          "w": 320,
          "h": 220,
          "deduct_val": 200000,
          "deduct_label": "2% Transfer Brokerage",
          "timeline": [
            { "start_ms": 1000, "end_ms": 3000, "action": "fade_in" },
            { "start_ms": 3500, "end_ms": 8000, "action": "fill_progress", "to_pct": 0.85 }
          ]
        },
        {
          "id": "dest_asset",
          "type": "asset_node",
          "x": 700,
          "y": 95,
          "w": 240,
          "h": 180,
          "icon": "document",
          "label": "Net Consideration (Sec 48)",
          "subtitle": "Basis for 54F Audit",
          "amount_val": 9800000,
          "timeline": [
            { "start_ms": 4500, "end_ms": 6500, "action": "fade_in" }
          ]
        },
        {
          "id": "ledger_card",
          "type": "breakdown_card",
          "x": 60,
          "y": 315,
          "w": 880,
          "h": 140,
          "verdict_badge": "SEC 48 QUALIFYING BASE VERIFIED",
          "rows": [
            { "label": "Full Value of Consideration (Gross Sale Price)", "val": 10000000 },
            { "label": "LESS: Expenses on transfer (Sec 48(i))", "val": 200000, "isDeduction": true, "prefix": "(-) " },
            { "label": "NET CONSIDERATION (Qualifying base for Sec 54F)", "val": 9800000, "isTotal": true }
          ],
          "timeline": [
            { "start_ms": 6000, "end_ms": 7500, "action": "fade_in" }
          ]
        }
      ]
    }
  ]
}

SUPPORTED ELEMENT TYPES:
- "asset_node": { x, y, w, h, icon, label, subtitle?, amount_val? } -> Encapsulated card with icon, title, subtitle, and bottom counter tray. Zero text collision!
- "funnel": { x, y, w, h, deduct_val?, deduct_label?, fill_pct? } -> Mechanical conical funnel, sieve filter, side deduction jar, and bottom collection flask.
- "breakdown_card": { x, y, w, h, rows: [{ label, val, isDeduction?, isTotal?, prefix? }], verdict_badge? } -> Statutory multi-line accounting calculation card with dotted lines.
- "scale": { x, y, arm_length?, left_label?, right_label?, tilt_angle? } -> Tilting mechanical balance scale with central pillar and pans.
- "tank": { x, y, w, h, fill_pct?, cap_pct?, cap_label?, overflow_label? } -> Liquid capacity tank with statutory cap threshold line.
- "equation_chips": { x, y, chips: [ { "label": "...", "val": 100 }, { "op": "−" }, { "label": "...", "val": 50, "isTotal": true } ] }
- "icon": { icon: "house"|"factory"|"warehouse"|"scale"|"vault"|"document"|"bonds"|"coins"|"calendar"|"clock"|"car"|"ship"|"barrier"|"pipe_split"|"person", x, y, w, h, label?, angle? }
- "box": { x, y, w, h, title?, subtitle?, fill_dither? }
- "text": { x, y, text, font_size?, align?, font_weight? }
- "counter": { x, y, from_val, to_val, prefix?, suffix?, font_size? }
- "badge": { x, y, w, h, text, inverted? }
- "line": { x1, y1, x2, y2, dashed?, label? }
- "stamp": { x, y, w, h, text }

SUPPORTED ACTIONS:
- "draw_stroke": outlines the element from 0% to 100%
- "fade_in": element appears smoothly
- "move": translates element smoothly to { to_x, to_y }
- "count_up": animates numeric counter from from_val to to_val
- "stamp": scales down with impact bounce to lock in place
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
