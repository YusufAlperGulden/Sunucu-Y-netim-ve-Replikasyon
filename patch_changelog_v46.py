with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add changelog entry for v46
NEW_CHANGELOG = """                        <li><span style="font-weight: 600;">Feature (Audit Log Search &amp; Export):</span> Audit Log sekmesine anlık <b>Arama Çubuğu (Search Bar)</b>, <b>Filtre Sıfırlama ("Clear all filters")</b>, <b>Yenileme (Refresh)</b> ve ClusterControl formatında birebir uyumlu <b>CSV Dışa Aktarma ("Export CSV")</b> özelliği eklendi.</li>
"""

whats_new_marker = "<h3 style=\"color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;\">What's New</h3>\n                    <ul style=\"color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;\">\n"

if whats_new_marker in html:
    html = html.replace(whats_new_marker, whats_new_marker + NEW_CHANGELOG, 1)
    print("Added Changelog entry for v46")

# Bump version to v=46
html = html.replace('v=45', 'v=46')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('v=45', 'v=46')
with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Bumped version to v=46")
