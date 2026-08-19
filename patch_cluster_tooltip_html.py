# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("overflow: hidden; font-family: 'Inter', sans-serif;\">", "overflow: hidden; font-family: 'Inter', sans-serif; transition: opacity 0.2s ease, transform 0.2s ease; opacity: 0; transform: translateY(10px);\">")

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML cluster tooltip patched")
