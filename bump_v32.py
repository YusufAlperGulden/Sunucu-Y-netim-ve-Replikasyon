import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=31', 'v=32')

new_changelog = """<li><span style="font-weight: 600;">zellik 4:</span> <b>User Management (Kullanc Ynetimi)</b> motoru aktif edildi. Veritaban desteki <code style="background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px;">User</code> modeli oluturuldu, ifreler bcrypt ile hashlendi ve kullanc silme/ekleme ilemleri yapld.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=31', 'v=32')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=32")
