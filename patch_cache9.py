import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('style.css?v=8', 'style.css?v=9')
content = content.replace('main.js?v=8', 'main.js?v=9')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache busters to v9")
