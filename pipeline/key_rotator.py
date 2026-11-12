import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from google import genai
from google.genai import types
import itertools

class AllKeysQuotaExhaustedError(Exception):
    """Raised when all available Gemini API keys have exhausted their quota / rate limits (429)."""
    pass

def is_quota_error(e: Exception) -> bool:
    msg = str(e).lower()
    return "429" in msg or "resource_exhausted" in msg or "quota" in msg or "too many requests" in msg or "rate limit" in msg

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
        self.total_keys = len(self.keys)
        print(f"KeyRotator initialized with {self.total_keys} active keys.")

    def get_client(self, timeout_ms=None):
        if not self.keys:
            raise RuntimeError("No Gemini API keys configured.")
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

    def execute_with_retry(self, api_func, *args, **kwargs):
        """
        Executes a callable api_func(client, *args, **kwargs).
        If a 429 quota/rate limit error occurs, rotates through all available keys.
        If all keys in the pool are exhausted, raises AllKeysQuotaExhaustedError.
        """
        if not self.keys:
            raise RuntimeError("No Gemini API keys configured.")

        quota_failures = 0
        last_error = None

        for attempt in range(self.total_keys):
            client = self.get_client()
            try:
                return api_func(client, *args, **kwargs)
            except Exception as e:
                last_error = e
                if is_quota_error(e):
                    quota_failures += 1
                    print(f"  [KEY ROTATION] Key {attempt + 1}/{self.total_keys} hit quota limit (429/ResourceExhausted). Rotating to next key...")
                else:
                    # Non-quota error, re-raise or continue
                    raise e

        if quota_failures >= self.total_keys:
            raise AllKeysQuotaExhaustedError(
                f"All {self.total_keys} Gemini API keys have exhausted their quota: {last_error}"
            )
        raise last_error

rotator = KeyRotator()
