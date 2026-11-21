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

SYSTEM_PROMPT = """You are an expert Direct Tax & Indirect Tax CA Faculty and Visual Kinetic Architect.
Given a tax section, statutory provision, or case study scenario, decompose it into a 4-scene animated presentation for a 1000x500 monochrome pixel screen.

The presentation must follow these strict rules:
1. Universal Domain Principle: ALL statutory sections, sub-sections, dates, numbers, legal terms, and tax concepts MUST be in English (e.g. 'Section 54EC', 'Section 50C', 'Assessment Year 2024-25', 'Stamp Duty Value', 'Full Value of Consideration', 'Indexation').
2. Teacher Dialogue: Friendly, conversational Malayalam teacher explanation with embedded English legal terminology (Manglish code-switching standard in Kerala CA education).
3. Realistic Indian Rupee Amounts: Every scene must have realistic, situation-specific Indian Rupee amounts (e.g. ₹50,00,000, ₹75,00,000, ₹1,10,00,000).

You MUST return valid JSON matching this schema:
{
  "section_code": "SEC 54EC",
  "title": "Short descriptive title of provision",
  "summary": "1-sentence statutory summary",
  "scenes": [
    {
      "id": 1,
      "tab_title": "1 Transaction & Asset Setup",
      "tag": "SCENE 1: STATUTORY TRANSACTION",
      "type": "transfer",
      "dialogue": "Natural Manglish teacher explanation with English legal terms.",
      "actor_left": { "name": "Assessee Name", "role": "Transferor description" },
      "actor_right": { "name": "Buyer / Specified Authority", "role": "Transferee description" },
      "asset": { "name": "Asset Name (e.g. Industrial Land & Building)", "type": "Land / Building / Shares / Undertaking" },
      "transfer_label": "TRANSFER DEED / STATUTORY ORDER",
      "amount_badge": "₹ 75,00,000",
      "amount_val": 7500000,
      "amount_label": "TOTAL CAPITAL GAIN / SALE CONSIDERATION"
    },
    {
      "id": 2,
      "tab_title": "2 Statutory Gatekeeper Checklist",
      "tag": "SCENE 2: STATUTORY PREREQUISITES",
      "type": "gatekeeper",
      "dialogue": "Teacher explanation of the 3 prerequisite conditions to unlock statutory relief.",
      "portal_title": "SECTION STATUTORY RELIEF PORTAL",
      "conditions": [
        { "label": "1. Condition text with exact time limit or asset rule", "cue": 1.0 },
        { "label": "2. Second statutory prerequisite condition", "cue": 4.0 },
        { "label": "3. Third statutory condition", "cue": 7.0 }
      ],
      "unlock_badge": "ALL CONDITIONS MET",
      "unlock_subtitle": "Statutory Relief Admissible"
    },
    {
      "id": 3,
      "tab_title": "3 Statutory Cap & Deduction",
      "tag": "SCENE 3: STATUTORY LIMIT & DEDUCTION",
      "type": "deduction_slice",
      "dialogue": "Teacher explanation of deduction, reduction from cost, or ceiling limit comparison.",
      "base_title": "Original Inflow / Cost of Acquisition",
      "base_val": 6000000,
      "deduct_title": "Statutory Cap / Forfeited Advance",
      "deduct_val": 5000000,
      "deduct_subtitle": "Brief subtitle explaining deduction rule",
      "result_title": "Net Qualifying Relief / Adjusted COA",
      "result_val": 5000000,
      "result_badge": "STATUTORY AUDIT VERIFIED",
      "statutory_note_title": "Statutory Limit Note (Proviso):",
      "statutory_note_text": "Crucial statutory warning or proviso explaining limits or exceptions!"
    },
    {
      "id": 4,
      "tab_title": "4 Final Tax Computation",
      "tag": "SCENE 4: FINAL TAX ARITHMETIC",
      "type": "formula",
      "dialogue": "Teacher explanation walking through the final capital gain equation.",
      "chips": [
        { "label": "Total Consideration / Gain", "val": 7500000, "cue": 1.0 },
        { "op": "−", "cue": 3.5 },
        { "label": "Statutory Exemption", "val": 5000000, "cue": 4.5 },
        { "op": "=", "cue": 7.0 },
        { "label": "Net Taxable Gain", "val": 2500000, "isTotal": true, "cue": 8.0 }
      ],
      "verification_title": "Statutory Arithmetic Verification",
      "verification_equation": "₹ 75,00,000 − ₹ 50,00,000 = ₹ 25,00,000 Net Taxable Capital Gain",
      "verification_note": "• Clear conclusion of tax liability or exemption."
    }
  ]
}
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
        prompt = f"Decompose this tax topic into a 4-scene pixel presentation:\nTopic: {topic}"
        last_err = None
        for m in models_to_try:
            try:
                t0 = time.time()
                resp = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json"
                    )
                )
                print(f"  [MODEL] Generated successfully using {m} in {round(time.time()-t0, 2)}s", flush=True)
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
        # Concise logging
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def end_headers(self):
        # Enable CORS for local testing
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

                print(f"\n[PIXEL SERVER] Generating presentation for topic: {topic}", flush=True)
                result = generate_pixel_presentation(topic)
                print(f"[PIXEL SERVER] Generation complete: {result.get('section_code')} - {result.get('title')}", flush=True)

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
