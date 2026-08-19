import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace inline styles for the two inputs
content = content.replace('style="background: #ffffff; border-color: #d1d5db; color: #111827;"', 'style="background: #ffffff; border: 2px solid #9ca3af; color: #111827;"')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated inputs.")
