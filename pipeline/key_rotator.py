import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from google import genai
from google.genai import types
import itertools

class KeyRotator:
    def __init__(self):
        env_file = os.path.join(PROJECT_ROOT, '.env')
        keys_str = os.getenv('GEMINI_API_KEYS', '')
        if not keys_str and os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEYS='):
                        keys_str = line.strip().split('=', 1)[1]
        
        self.keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        if not self.keys:
            single = os.getenv('GEMINI_API_KEY', '')
            if single:
                self.keys = [single]
        self._pool = itertools.cycle(self.keys)
        print(f"KeyRotator initialized with {len(self.keys)} active keys.")

    def get_client(self, timeout_ms=None):
        next_key = next(self._pool)
        if timeout_ms:
            return genai.Client(
                api_key=next_key,
                http_options=types.HttpOptions(
                    timeout=timeout_ms,
                    retry_options=types.HttpRetryOptions(attempts=1)
                )
            )
        return genai.Client(api_key=next_key)

rotator = KeyRotator()
