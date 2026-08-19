import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=15', 'v=16')

# Add changelog entry
new_changelog = """<li><span style="font-weight: 600;">Feature:</span> Sistem Altyapısı Değişimi: Kullanıcının talebi üzerine, Cluster detay sayfasına "Settings" (Sistem Ayarları) sekmesi ve veritabanına bu ayarları tutacak altyapı eklendi. Artık CMON ayarları, PostgreSQL pgBackRest şifrelemeleri ve Cloud yedekleme politikaları (retention) FAKE (sahte) olmayan ve gerçekten veritabanında saklanan, güncellenebilen ayarlardır. İlgili arkaplan işlemcileri yazıldığında bu ayarlara direkt entegre olacak şekilde tasarlandı.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=15', 'v=16')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=16 and updated changelog")
