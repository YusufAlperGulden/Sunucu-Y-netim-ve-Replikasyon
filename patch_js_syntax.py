import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "});" and i > 2380 and i < 2400:
        continue # skip the errant });
    new_lines.append(line)

with open(js_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Removed errant });")
