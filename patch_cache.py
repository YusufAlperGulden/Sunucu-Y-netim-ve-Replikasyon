import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('style.css?v=4', 'style.css?v=5')
content = content.replace('main.js?v=4', 'main.js?v=5')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache busters")
