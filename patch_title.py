import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'<h1 style="color: var\(--primary\); font-size: 3rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">(.*?)</h1>',
    r'<h1 style="color: var(--primary); font-size: 3rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">ClusterControl</h1>',
    content
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML patched successfully")
