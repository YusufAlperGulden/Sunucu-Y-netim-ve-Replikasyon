import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=17', 'v=18')

new_changelog = """<li><span style="font-weight: 600;">Fix:</span> Uygulamaya yaplan nceki gncellemeler srasnda (Nodes listesinin deiimi srasnda) meydana gelen kk bir yazm hatasndan dolay arka plan animasyonlar (Baloncuklar) dhil tm etkileimlerin bozulmas (Syntax Error) sorunu dzeltildi.</li>
<li><span style="font-weight: 600;">Feature:</span> "Settings" ekrannda artk gerekten var olan PostgreSQL ayarlar (Long Query, Replication, Retention, System vb.) iin API balantlar kuruldu. Sol mendeki deerlere tklandnda tpk "Backup" ksmnda olduu gibi kendi API'lerinden gerek deerleri okuyup yanstan bir altyap eklendi ve baz sahte sekmeler (CmonDB, Controller) veritabanyla hibir ilgisi olmad iin mmknse tasarmdan gizlendi.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=17', 'v=18')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=18 and updated changelog")
