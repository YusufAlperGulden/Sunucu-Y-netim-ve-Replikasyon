import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'style="display: flex; align-items: center; padding: 12px 24px; color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: all 0.2s;"',
    'style="display: flex; align-items: center; padding: 12px 24px; color: #ffffff; text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: all 0.2s;"'
)

content = content.replace(
    'style="padding: 12px 24px; text-align: center; cursor: pointer; color: var(--text-secondary); margin-top: 10px;"',
    'style="padding: 12px 24px; text-align: center; cursor: pointer; color: #ffffff; margin-top: 10px;"'
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied")
