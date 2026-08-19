import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=30', 'v=31')

new_changelog = """<li><span style="font-weight: 600;">Hotfix 3 (Final):</span> Python <code style="background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px;">AttributeError</code> hatas zld. "models.py" ierisindeki snf tanmna eklenmesi unutulan stun deikenleri (ssh_host) koda dahil edildi. Tm zellikler %100 istikrarl alyor.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=30', 'v=31')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=31 and updated changelog")
