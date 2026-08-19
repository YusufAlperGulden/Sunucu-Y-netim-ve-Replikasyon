import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog = """<li><span style="font-weight: 600;">Improvement:</span> "Sunucu Yönetim Dashboard" (Canlı Metrikler) ayrı bir sayfa olmak yerine, doğrudan her projenin detaylarındaki "Dashboards" sekmesinin altına taşındı. Böylece ekran karmaşası giderildi ve menü navigasyonu daha tutarlı hale getirildi.</li>
"""

# Insert right after `<ul ...> \n <li><span style="font-weight: 600;">Feature:</span> Cluster detay sayfas`
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
content = re.sub(pattern, r'\g<1>' + new_changelog, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated changelog")
