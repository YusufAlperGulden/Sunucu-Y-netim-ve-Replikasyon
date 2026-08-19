import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<a href="#" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">View alarms</a>',
    '<a href="#" onclick="document.querySelector(\'a[data-view=\\\'activity-view\\\']\').click(); document.getElementById(\'tab-btn-alarms\').click(); return false;" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">View alarms</a>'
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied")
