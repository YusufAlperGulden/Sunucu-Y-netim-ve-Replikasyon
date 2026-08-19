# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("a.className = \"submenu-item\";", "a.className = \"submenu-item\"; a.onclick = () => document.querySelector('a[data-view=\"clusters-view\"]').click();")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS submenu click patched")
