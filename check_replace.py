import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add declaration if missing
if 'let clusterHoverTimeout' not in js_content:
    js_content = js_content.replace('let currentProjectId = null;', 'let currentProjectId = null;\n    let clusterHoverTimeout = null;')

# We need to replace the tr.onmouseenter and tr.onmouseleave block
old_hover_code = r'tr\.onmouseenter = \(e\) => \{[\s\S]*?tr\.onmouseleave = \(e\) => \{[\s\S]*?\}\s*;\s*'

# Let's find exactly the block to replace by getting the substring
match = re.search(r'(tr\.onmouseenter = \(e\) => \{[\s\S]*?tr\.onmouseleave = \(e\) => \{[\s\S]*?\} \n                  ;)', js_content)
if not match:
    # Try another pattern
    match = re.search(r'(tr\.onmouseenter = \(e\) => \{[\s\S]*?tr\.onmouseleave = \(e\) => \{[\s\S]*?\} \n                  ;)', js_content)
