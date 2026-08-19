# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(".sidebar-nav a.submenu-item", ".sidebar-nav .submenu-item")

with open('fastapi_app/static/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS submenu a to any patched")
