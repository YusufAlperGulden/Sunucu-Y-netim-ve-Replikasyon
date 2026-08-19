import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('}, 1000);', '}, 500);')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied")
