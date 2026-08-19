import re

css_path = 'fastapi_app/static/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '.login-overlay {\n    position: fixed;',
    '.login-overlay {\n    position: fixed;\n    z-index: 999999;'
)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed login overlay z-index")
