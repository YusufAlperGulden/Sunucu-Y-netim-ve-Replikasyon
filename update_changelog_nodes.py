import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> Cluster detay sayfasındaki "Nodes" sekmesinin içerisine "Node list" (Tablo ve Özet İstatistikler) ve "Topology" alt sekmeleri eklendi. Node List tablosu orjinal sisteme birebir uyumlu olarak tasarlandı.</li>
"""

# Insert right after `<ul ...> \n <li><span style="font-weight: 600;">Improvement:</span> "Sunucu Y`
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
content = re.sub(pattern, r'\g<1>' + new_changelog, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated changelog")
