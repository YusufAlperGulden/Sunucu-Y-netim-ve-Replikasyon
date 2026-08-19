with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add changelog items at the top of What's New list under v1.4.2
NEW_ITEMS = """                        <li><span style="font-weight: 600;">UI/UX (Loading Animation):</span> ClusterControl tasarımı ile birebir uyumlu <b>Circular Loading Spinner (Dönen Dairesel Animasyon)</b> tüm tablolara, kartlara ve yükleme durumlarına eklendi. Ham metin ("Yükleniyor...") yerine zarif dönen çember animasyonu gösterilmektedir.</li>
                        <li><span style="font-weight: 600;">Feature (Activity Center):</span> Activity Center ekranı orijinal ClusterControl yapısına uygun olarak 4 sekmeye ayrıldı: <b>Alarms</b>, <b>Jobs</b> (Yedekleme ve sistem işleri), <b>Audit Log</b> (Kullanıcı eylem ve denetim kayıtları) ve <b>Watchlists (Beta)</b>.</li>
                        <li><span style="font-weight: 600;">Feature (Nodes View):</span> Nodes ekranı tüm cluster'lardaki aktif veritabanı düğümlerini anında listeleyen, durum filtreleme kartları (Operational, Failed, Offline vb.) ve canlı PostgreSQL sürüm kontrolü ile donatılmış gerçek zamanlı envanter tablosuna kavuşturuldu.</li>
                        <li><span style="font-weight: 600;">Fix (Replication & Metrics):</span> Frankfurt (Ana Sunucu) ve Londra (Yedek Sunucu) Neon PostgreSQL veritabanı bağlantı şifreleri ve SSL parametreleri otomatik senkronize edilerek TPS, Ping, Storage ve Ana Tablo (vehicles) kayıt sayısı canlı metrikleri bağlandı.</li>
"""

whats_new_marker = "<h3 style=\"color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;\">What's New</h3>\n                    <ul style=\"color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;\">\n"

if whats_new_marker in html:
    html = html.replace(whats_new_marker, whats_new_marker + NEW_ITEMS, 1)
    print("Added new Changelog items")

# Bump version to v=45
html = html.replace('v=44', 'v=45')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('v=44', 'v=45')
with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Bumped version to v=45")
