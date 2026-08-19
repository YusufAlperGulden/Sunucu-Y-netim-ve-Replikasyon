import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<a href="#" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">View nodes</a>',
    '<a href="#" onclick="document.querySelector(\'a[data-view=\\\'nodes-view\\\']\').click(); return false;" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">View nodes</a>'
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML link patched")
