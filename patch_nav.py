import re

with open('fastapi_app/static/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'color: #a0aec0;',
    'color: #ffffff;'
)

with open('fastapi_app/static/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied css")
