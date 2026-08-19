with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add changelog entry for v49
NEW_CHANGELOG = """                        <li><span style="font-weight: 600;">Fix (Nodes View):</span> Nodes sayfasında düğümlerin listelenmesini engelleyen çift döngü ve eski closure referansı temizlendi. Tüm cluster'lardaki sunucular (Primary &amp; Standby) anında stat kartlarına (Operational, Failed, Offline vb.) ve envanter tablosuna gerçek zamanlı olarak bağlandı.</li>
"""

whats_new_marker = "<h3 style=\"color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;\">What's New</h3>\n                    <ul style=\"color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;\">\n"

if whats_new_marker in html:
    html = html.replace(whats_new_marker, whats_new_marker + NEW_CHANGELOG, 1)
    print("Added Changelog entry for v49")

# Bump version to v=49
html = html.replace('v=48', 'v=49')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('v=48', 'v=49')
with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Bumped version to v=49")
