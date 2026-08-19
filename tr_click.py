import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_tr_click = """                tr.addEventListener('click', async (e) => {
                    if(e.target.closest('button') || e.target.closest('.dropdown-menu')) return;
                    if (window.location.hash !== '#projects-view') {
                        window.location.hash = 'projects-view';
                    }
                    try {"""

new_tr_click = """                tr.addEventListener('click', async (e) => {
                    if(e.target.closest('button') || e.target.closest('.dropdown-menu')) return;
                    try {"""
                    
if old_tr_click in content:
    content = content.replace(old_tr_click, new_tr_click)
else:
    print("Not found tr_click")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed tr click")
