import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=21', 'v=22')

new_changelog = """<li><span style="font-weight: 600;">Fix:</span> "ift Giri Ekran (Double Login Prompt)" sorunu zld. Sayfa yklendiinde arka planda yaplan yetki kontrollerinin (API 401 dnleri) tarayc tarafndan yanl anlalp kendi varsaylan "Oturum an" uyarsn kartmas engellendi. Artk gvenlik bal sadece arka planda nlenip direkt olarak tasarladmz gvenli ve k giri ekranna (Balonlu ekran) ynlendiriliyor.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=21', 'v=22')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=22 and updated changelog")
