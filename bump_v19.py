import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=18', 'v=19')

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> PostgreSQL Fiziksel Entegrasyonu: "Settings" sekmesinde yer alan PostgreSQL motor parametreleri (shared_buffers, work_mem, max_connections, wal_level, max_replication_slots, log_min_duration_statement vb.) artk sadece veritabanmza kaydedilmekle kalmyor; arkaplanda alan dzenli bir Python isisi sayesinde ilgili kmenin tm Node'larna ngilizce ('ALTER SYSTEM SET...') SQL komutlar araclyla fiziksel olarak gnderilip 'SELECT pg_reload_conf()' komutuyla annda aktif ediliyor. Ayrnca gelecekte kkmeye eklenecek yeni sunuculara da bu proje ayarlarnn otomatik olarak yklenmesi iin eklemeler yapld.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=18', 'v=19')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=19 and updated changelog")
