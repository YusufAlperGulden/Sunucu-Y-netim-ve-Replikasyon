# -*- coding: utf-8 -*-
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="settings-view"' in line:
        print(f"Line {i+1}: {line.strip()}")
