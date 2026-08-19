import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=20', 'v=21')

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> "Settings" ekranndaki arama ubuu (Search Bar) aktifleitirildi. Artk "Search by parameter, value, description" ksmna herhangi bir anahtar kelime yazdnzda, o ana kadar sol mendeki hangi kategoride olduunuza baklmakszn tm PostgreSQL parametreleri (isimleri, deeri ve aklamalar) iinde dinamik arama yaplp sonular annda ekrana yansyor.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=20', 'v=21')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=21 and updated changelog")
