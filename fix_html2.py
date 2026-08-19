import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = content.replace('-? 4 Operational', '&#8226; 4 Operational')
content = content.replace('-? 0 Shut Down', '&#8226; 0 Shut Down')
content = content.replace('-? 8 Operational', '&#8226; 8 Operational')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML bullets fixed manual")
