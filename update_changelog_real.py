import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog = """<li><span style="font-weight: 600;">Fix:</span> Uygulama içindeki tüm sahte (placeholder) veritabanı düğüm verileri (IP adresleri, portlar, DB tipleri) koddan temizlendi. "Nodes" sekmelerindeki tablolar artık veritabanında şifreli olarak tutulan bağlantı (connection string) url'lerini AES-256 ile çözerek tamamen %100 gerçek IP, Port ve Veritabanı tipini (PostgreSQL vb.) dinamik olarak ekrana yansıtmaktadır.</li>
"""

pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
content = re.sub(pattern, r'\g<1>' + new_changelog, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated changelog for real DB nodes")
