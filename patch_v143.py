with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Left Sidebar in Changelog
old_left_sidebar = """                <!-- Left Sidebar -->
                <div style="width: 250px; border-right: 1px solid #e5e7eb; padding: 32px 24px; display: flex; flex-direction: column; gap: 16px; font-size: 0.9rem; background: #fafafa;">
                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.2 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault();" style="color: #9ca3af; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px; cursor: default;" title="Archived versions coming soon">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>
                </div>"""

new_left_sidebar = """                <!-- Left Sidebar -->
                <div style="width: 250px; border-right: 1px solid #e5e7eb; padding: 32px 24px; display: flex; flex-direction: column; gap: 16px; font-size: 0.9rem; background: #fafafa;">
                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.3 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.2</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault();" style="color: #9ca3af; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px; cursor: default;" title="Archived versions coming soon">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>
                </div>"""

if old_left_sidebar in html:
    html = html.replace(old_left_sidebar, new_left_sidebar, 1)
    print("Updated Left Sidebar with v1.4.3 (Latest)")

# 2. Update Table of Contents (Right sidebar)
old_toc = """                <!-- Right Sidebar (TOC) -->
                <div style="width: 250px; border-left: 1px solid #e5e7eb; padding: 32px 24px; font-size: 0.85rem; background: #fafafa;">
                    <div style="color: #9ca3af; margin-bottom: 16px;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>
                </div>"""

new_toc = """                <!-- Right Sidebar (TOC) -->
                <div style="width: 250px; border-left: 1px solid #e5e7eb; padding: 32px 24px; font-size: 0.85rem; background: #fafafa;">
                    <div style="color: #9ca3af; margin-bottom: 16px;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.3 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>
                </div>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.4.3 Release")

# 3. Create v1.4.3 section in Middle Content and separate v1.4.2
V143_CONTENT = """                    <h2 id="v1-4-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.3</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Nodes View):</span> Nodes sayfasında düğümlerin listelenmesini engelleyen çift döngü ve eski closure referansı temizlendi. Tüm cluster'lardaki sunucular (Primary &amp; Standby) anında stat kartlarına (Operational, Failed, Offline vb.) ve envanter tablosuna gerçek zamanlı olarak bağlandı.</li>
                        <li><span style="font-weight: 600;">Feature (Audit Log Search &amp; Export):</span> Audit Log sekmesine anlık <b>Arama Çubuğu (Search Bar)</b>, <b>Filtre Sıfırlama ("Clear all filters")</b>, <b>Yenileme (Refresh)</b> ve ClusterControl formatında birebir uyumlu <b>CSV Dışa Aktarma ("Export CSV")</b> özelliği eklendi.</li>
                        <li><span style="font-weight: 600;">UI/UX (Loading Animation):</span> ClusterControl tasarımı ile birebir uyumlu <b>Circular Loading Spinner (Dönen Dairesel Animasyon)</b> tüm tablolara, kartlara ve yükleme durumlarına eklendi. Ham metin ("Yükleniyor...") yerine zarif dönen çember animasyonu gösterilmektedir.</li>
                        <li><span style="font-weight: 600;">Feature (Activity Center):</span> Activity Center ekranı orijinal ClusterControl yapısına uygun olarak 4 sekmeye ayrıldı: <b>Alarms</b>, <b>Jobs</b> (Yedekleme ve sistem işleri), <b>Audit Log</b> (Kullanıcı eylem ve denetim kayıtları) ve <b>Watchlists (Beta)</b>.</li>
                        <li><span style="font-weight: 600;">Fix (Replication &amp; Metrics):</span> Frankfurt (Ana Sunucu) ve Londra (Yedek Sunucu) Neon PostgreSQL veritabanı bağlantı şifreleri ve SSL parametreleri otomatik senkronize edilerek TPS, Ping, Storage ve Ana Tablo (vehicles) kayıt sayısı canlı metrikleri bağlandı.</li>
                    </ul>

                    <h2 id="v1-4-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.2</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
"""

# Find where <h2 id="v1-4-2" begins in Middle Content
v142_start = html.find('<h2 id="v1-4-2"')
# Find where the old list ends before <h2 id="v1-4-1"
v141_start = html.find('<h2 id="v1-4-1"')

# Let's extract the previous v1.4.2 items (excluding the 5 new ones that belong to v1.4.3)
old_v142_block = html[v142_start:v141_start]

# Replace the 5 newest items from the old v1.4.2 list so they are now solely in v1.4.3
import re
cleaned_v142_items = old_v142_block
for tag in ['Fix (Nodes View)', 'Feature (Audit Log Search &amp; Export)', 'UI/UX (Loading Animation)', 'Feature (Activity Center)', 'Fix (Replication &amp; Metrics)']:
    cleaned_v142_items = re.sub(r'<li><span style="font-weight: 600;">' + re.escape(tag) + r':</span>.*?</li>\n?', '', cleaned_v142_items)

# Remove the old h2, release-cycle, and whats-new headers from the v1.4.2 block so it's just the v1.4.2 list
cleaned_v142_items = re.sub(r'<h2 id="v1-4-2".*?<ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">\n?', '', cleaned_v142_items, flags=re.DOTALL)

new_middle_content = V143_CONTENT + cleaned_v142_items.strip() + "\n\n                    "

html = html[:v142_start] + new_middle_content + html[v141_start:]
print("Separated v1.4.3 and v1.4.2 in content")

# Bump asset version to v=50
html = html.replace('v=49', 'v=50')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("changelogAnchors = ['v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=49', 'v=50')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with v1.4.3 anchor and v=50")
