import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=19', 'v=20')

new_changelog = """<li><span style="font-weight: 600;">Fix:</span> "Settings" (Ayarlar) sayfasndaki sahte etiketlerin kaldrlmas/gizlenmesi ileminde meydana gelen kk bir HTML kapan etiketi kaymas nedeniyle 'User management' ve 'Backups' sayfalarnn saa doru kayarak yapsnn bozulmas (UI Bug) sorunu dzeltildi. Artk tm ekranlar ana gvdeye tam oturuyor.</li>
<li><span style="font-weight: 600;">Fix:</span> Uygulama srm geikmesi (Render Cache) nedeniyle "Clusters" sayfasnda tklanan projelerin yeni ekranda/sekmede almayp i ie gemesi sorunu son v=20 srmyle tamamen zld. Eer u an kullanyorsanz sayfay tamamen yenileyip (CTRL+F5) dzeldiini grebilirsiniz.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=19', 'v=20')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=20 and updated changelog")
