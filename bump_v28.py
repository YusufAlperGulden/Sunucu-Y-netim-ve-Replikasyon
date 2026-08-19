import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=27', 'v=28')

new_changelog = """<li><span style="font-weight: 600;">Hotfix:</span> Sunucu Ynetimi sekmesindeki <code style="background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px;">Internal Server Error</code> (Web Sitesi kmesi) sorunu tespit edilip giderildi. Bir nceki gncellmede (v=27) veritaban modline eklenen SSH stnlarnn (ssh_host vb.) Render zerindeki mevcut veritaban tablosuna yansmamas (Migration eksiklii) sebebiyle yaanan 500 hatas zlerek uygulumann balangcnda otomatik <code style="background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px;">ALTER TABLE</code> sorgular altrlmas saland. Artk Sunucularnz (Nodes) listesi sorunsuzca yklenmektedir.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=27', 'v=28')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=28 and updated changelog")
