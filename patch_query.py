import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("const rows = tbody.querySelectorAll('tr');", "const rows = tbody ? tbody.querySelectorAll('tr') : [];")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched querySelectorAll")
