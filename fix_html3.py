import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = re.sub(r'<span style="color: var\(--success\);">.*?4 Operational</span>', '<span style="color: var(--success);">&#8226; 4 Operational</span>', content)
content = re.sub(r'<span style="color: var\(--primary\);">.*?0 Shut Down</span>', '<span style="color: var(--primary);">&#8226; 0 Shut Down</span>', content)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML manual fixed")
