import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('style.css?v=6', 'style.css?v=7')
content = content.replace('main.js?v=6', 'main.js?v=7')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache busters to v7")
