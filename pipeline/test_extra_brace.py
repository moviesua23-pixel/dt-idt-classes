import subprocess
import tempfile

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

js = text.split('<script>')[1].split('</script>')[0]
lines = js.splitlines()

func_lines = [i for i, l in enumerate(lines) if l.strip().startswith('function ') or '$$(".mm-' in l or '/* Auto-Hiding' in l]
print(f"Checking {len(func_lines)} function/block boundaries...")

for fl in func_lines:
    test_lines = list(lines)
    test_lines.insert(fl, "}")
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
        tf.write('\n'.join(test_lines))
        tname = tf.name
    res = subprocess.run(['node', '--check', tname], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"VALID AT LINE {fl+1}! Line content: {lines[fl][:60]}")
        break
