import subprocess
import tempfile

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

low = 3205 # start of script
high = 4075 # makePlayer start

def check_insert(line_idx):
    test_lines = list(lines)
    test_lines.insert(line_idx, "}")
    code = '\n'.join(test_lines)
    js = code.split('<script>')[1].split('</script>')[0]
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
        tf.write(js)
        tname = tf.name
    res = subprocess.run(['node', '--check', tname], capture_output=True, text=True)
    return res.returncode == 0

# Binary search: find the earliest line where inserting '}' makes it valid
ans = None
l, r = low, high
while l <= r:
    mid = (l + r) // 2
    # Check if inserting at mid or anything after mid is valid
    # If inserting at mid is valid:
    if check_insert(mid):
        ans = mid
        r = mid - 1
    else:
        l = mid + 1

print(f"Earliest valid insertion point: line {ans + 1}: {lines[ans] if ans else 'None'}")
