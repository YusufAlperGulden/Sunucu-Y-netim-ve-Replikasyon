import re

js_path = 'fastapi_app/static/main.js'
html_path = 'fastapi_app/templates/index.html'

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()
js = js.replace('v=36', 'v=37')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('v=36', 'v=37')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Bumped to v=37")
