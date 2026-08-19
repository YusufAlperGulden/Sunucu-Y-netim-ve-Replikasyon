import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = re.sub(r'<span style="color:#3b82f6;">\? Shut Down</span>', '<span style="color:#3b82f6;">&#8226; Shut Down</span>', content)
content = content.replace("-? Operational", "&#8226; Operational")
content = content.replace("-? Warning", "&#8226; Warning")
content = content.replace("-? ", "&#8226; ")
content = content.replace("-? ", "&#8226; ")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS bullets fixed")
