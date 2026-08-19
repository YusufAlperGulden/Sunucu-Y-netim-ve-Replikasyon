import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_email_tab = """<div style="color: #6b7280; font-weight: 500; font-size: 0.9rem; padding-bottom: 10px; cursor: pointer;">Email notifications</div>"""
new_email_tab = """<div style="color: #6b7280; font-weight: 500; font-size: 0.9rem; padding-bottom: 10px; cursor: default; opacity: 0.7;">Email notifications <span style="font-size: 0.65rem; color: #ef4444; font-weight: bold; margin-left: 5px;">[PLACEHOLDER]</span></div>"""

if old_email_tab in content:
    content = content.replace(old_email_tab, new_email_tab)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added placeholder to Email tab")
else:
    print("Could not find old_email_tab")
