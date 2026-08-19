js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Find and replace the entire fetchNodesPage function
import re

old_fn_start = js.find('window.fetchNodesPage = async function fetchNodesPage()')
if old_fn_start == -1:
    old_fn_start = js.find('async function fetchNodesPage()')
    
print(f"Found fetchNodesPage at: {old_fn_start}")

# Find the end of the function by brace counting
depth = 0
i = old_fn_start
found_end = -1
in_fn = False
for pos in range(old_fn_start, min(old_fn_start + 8000, len(js))):
    c = js[pos]
    if c == '{':
        depth += 1
        in_fn = True
    elif c == '}':
        depth -= 1
        if in_fn and depth == 0:
            found_end = pos + 1
            break

print(f"Function ends at: {found_end}")
old_fn = js[old_fn_start:found_end]
print(f"Old function length: {len(old_fn)}")
print("First 200 chars:", old_fn[:200])
