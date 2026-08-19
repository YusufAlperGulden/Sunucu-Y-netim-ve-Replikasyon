import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=22', 'v=23')

new_changelog = """<li><span style="font-weight: 600;">UI/UX:</span> "Operational reports" (Operasyonel Raporlar) ekran baa dnlerek aslnn (ClusterControl) yapsna tam sadk kalnacak ekilde yeniden ina edildi. Artk sayfada i ie gemi "Reports" ve "Schedules" sekmeleri yer alyor ve tablolarn seenekleri (Created by, File name, Data range vb.) deiiyor. Ayrca sa stte beliren "Create report" ve "Create schedule" butonlar ve onlara tklaynca alan orijinal tasarmdaki form (Modal) birebir kodland. Kzarm [PLACEHOLDER] etiketleri sadece gerekli grlen input alanlarna eklenerek sayfa zenginletirildi.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=22', 'v=23')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=23 and updated changelog")
