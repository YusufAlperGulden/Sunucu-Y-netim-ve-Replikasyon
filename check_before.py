import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

index = content.find('<section id="users-view"')
before_content = content[:index]

opens = len(re.findall(r'<div\b', before_content))
closes = len(re.findall(r'</div>', before_content))
print(f"Before users-view: opens={opens}, closes={closes}")
