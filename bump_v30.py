import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=29', 'v=30')

new_changelog = """<li><span style="font-weight: 600;">Hotfix 2:</span> Internal Server Error (500) tam olarak zld! Bir nceki gncellemede manuel veritaban glerini yaparken tablonun adn "database_nodes" olarak yazdgm iin yeni stunlar eklenememiti (Aslnda tablonun ad "nodes" imi!). Bu isim dzeltilerek gler baaryla altrld. Tm Cluster ve Node grnmleri eski salna kavutu.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=29', 'v=30')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=30 and updated changelog")
