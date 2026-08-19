import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=24', 'v=25')

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> Rapor oluturma motoru (Operational Reports) tmyle ii dolu ve aktif hale getirildi! Artk seilen veritaban kmesi (Cluster), Rapor Tp (System, Backup, Upgrade vb.), Gn says (Sadece rakam alacak ekilde) ve Alc mailleriyle <b>gerek</b> rapor kaytlar oluturuluyor. Veriler dorudan PostgreSQL veritabanna iilip sayfa her yenilendiinde sunucudan canl ekiliyor.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=24', 'v=25')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=25 and updated changelog")
