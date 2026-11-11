import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('<script>')
if len(parts) < 2:
    print("Could not find <script>")
    exit(1)

js = parts[1].split('</script>')[0]

import subprocess
import tempfile

with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
    tf.write(js)
    tname = tf.name

res = subprocess.run(['node', '--check', tname], capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
