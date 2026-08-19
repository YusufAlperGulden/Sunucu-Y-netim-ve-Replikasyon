# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the previous submenu_logic we inserted.
# In the previous patch, we used: let a = document.createElement('a'); a.href = "#"; a.className = "submenu-item";
# We will change it to div.
content = content.replace("let a = document.createElement('a');", "let a = document.createElement('div');")
content = content.replace('a.href = "#";', "")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS submenu a to div patched")
