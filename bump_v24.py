import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=23', 'v=24')

new_changelog = """<li><span style="font-weight: 600;">Fix & Feature:</span> Rapor oluturma (Create report) butonunun CSS'teki stil eksiklii nedeniyle grnmez/effaf olmas sorunu zld. Butonlara orijinal mor rengi (Background: #3a1c94) eklendi. Ayrca sahte [PLACEHOLDER] altyaps kaldrlarak, formdaki "Select cluster" (Sunucu Se) alalr menesne <b>gerek veritaban sunucularnz dinamik olarak (API zerinden) eklendi!</b> Artk sahte men yerine gerek projelerinizi seebilirsiniz.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=23', 'v=24')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=24 and updated changelog")
