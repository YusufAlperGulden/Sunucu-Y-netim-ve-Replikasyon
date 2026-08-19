import re

js_path = 'fastapi_app/static/main.js'
html_path = 'fastapi_app/templates/index.html'

for path in [js_path, html_path]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('v=39', 'v=40')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Bumped to v=40")
