# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("display: none;\"><polyline points=\"6 9 12 15 18 9", "display: block;\"><polyline points=\"6 9 12 15 18 9")

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML chevron unhidden")
