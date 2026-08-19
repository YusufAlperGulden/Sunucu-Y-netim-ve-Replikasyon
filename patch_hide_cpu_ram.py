with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update metricsHtml in main.js to give CPU and RAM cards unique IDs and hide them by default if N/A
old_metrics_html = """                        const metricsHtml = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel"><div class="metric-label">CPU Kullanımı</div><div class="metric-val" id="metric-${node.id}-cpu" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">RAM Kullanımı</div><div class="metric-val" id="metric-${node.id}-ram" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-${node.id}-ping">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Senkronizasyon (Lag)</div><div class="metric-val" id="metric-${node.id}-lag">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Depolama (Storage)</div><div class="metric-val" id="metric-${node.id}-storage">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Bağlantılar (Aktif/Top.)</div><div class="metric-val" id="metric-${node.id}-conn">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">İşlem Yükü (Başarılı / İptal)</div><div class="metric-val" id="metric-${node.id}-xact">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ana Tablo Kaydı</div><div class="metric-val" id="metric-${node.id}-plates">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Önbellek Başarısı</div><div class="metric-val" id="metric-${node.id}-cache">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Çalışma Süresi</div><div class="metric-val" id="metric-${node.id}-uptime">-</div></div>
                            </div>
                            <div style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted); text-align: right;">
                                Motor Sürümü: <span id="metric-${node.id}-version">-</span>
                            </div>
                        `;"""

new_metrics_html = """                        const metricsHtml = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel" id="metric-${node.id}-card-cpu" style="display: none;"><div class="metric-label">CPU Kullanımı</div><div class="metric-val" id="metric-${node.id}-cpu" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel" id="metric-${node.id}-card-ram" style="display: none;"><div class="metric-label">RAM Kullanımı</div><div class="metric-val" id="metric-${node.id}-ram" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-${node.id}-ping">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Senkronizasyon (Lag)</div><div class="metric-val" id="metric-${node.id}-lag">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Depolama (Storage)</div><div class="metric-val" id="metric-${node.id}-storage">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Bağlantılar (Aktif/Top.)</div><div class="metric-val" id="metric-${node.id}-conn">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">İşlem Yükü (Başarılı / İptal)</div><div class="metric-val" id="metric-${node.id}-xact">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ana Tablo Kaydı</div><div class="metric-val" id="metric-${node.id}-plates">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Önbellek Başarısı</div><div class="metric-val" id="metric-${node.id}-cache">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Çalışma Süresi</div><div class="metric-val" id="metric-${node.id}-uptime">-</div></div>
                            </div>
                            <div style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted); text-align: right;">
                                Motor Sürümü: <span id="metric-${node.id}-version">-</span>
                            </div>
                        `;"""

if old_metrics_html in js:
    js = js.replace(old_metrics_html, new_metrics_html, 1)
    print("Updated metricsHtml card IDs")

# Update the CPU/RAM display logic in main.js
old_cpu_ram_update = """                        setEl("metric-" + node.id + "-cpu", m.cpu_usage || "N/A");
                        setEl("metric-" + node.id + "-ram", m.ram_usage || "N/A");"""

new_cpu_ram_update = """                        // Only display CPU and RAM cards if real SSH/Linux VPS metrics exist
                        const cardCpu = document.getElementById(`metric-${node.id}-card-cpu`);
                        if (cardCpu) {
                            if (m.cpu_usage && m.cpu_usage !== 'N/A') {
                                cardCpu.style.display = 'block';
                                setEl(`metric-${node.id}-cpu`, m.cpu_usage);
                            } else {
                                cardCpu.style.display = 'none';
                            }
                        }
                        
                        const cardRam = document.getElementById(`metric-${node.id}-card-ram`);
                        if (cardRam) {
                            if (m.ram_usage && m.ram_usage !== 'N/A') {
                                cardRam.style.display = 'block';
                                setEl(`metric-${node.id}-ram`, m.ram_usage);
                            } else {
                                cardRam.style.display = 'none';
                            }
                        }"""

if old_cpu_ram_update in js:
    js = js.replace(old_cpu_ram_update, new_cpu_ram_update, 1)
    print("Updated CPU/RAM card visibility logic in main.js")

# Bump router anchors and asset version to v=57
js = js.replace("changelogAnchors = ['v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=56', 'v=57')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html Changelog for v1.5.0
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.5.0
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.9 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.8</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.0 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.9</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.8</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.5.0 (Latest)")

# Update TOC for v1.5.0
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.9 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.8 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.0 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.9 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.8 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.5.0 Release")

# Update Middle Content for v1.5.0
old_content_top = """                    <h2 id="v1-4-9" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.9</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Detail Dashboard):</span> Belirli bir cluster'ın detay sayfasına girildiğinde (örn: <b>Araç Plaka Takip Sistemi</b>), diğer ilgisiz cluster'ların metrik kartlarının karışmasını önleyen filtreleme eklendi. Artık her cluster'ın Dashboard sekmesinde yalnızca o cluster'a ait sunucu düğümleri (Primary &amp; Standby) gösterilir. Ayrıca breadcrumb navigasyonu (<code>Project Name (ID: X)</code>) dinamikleştirildi.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-0" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.0</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">UI/UX (Dynamic CPU/RAM Visibility):</span> Sunucu Yönetim Dashboard ekranında, Linux VPS / SSH yapılandırması olmayan sunucularda <code>N/A</code> gösteren CPU ve RAM kartları otomatik olarak tamamen gizlendi. Yalnızca gerçek SSH/OS metrikleri mevcut olduğunda kartlar görünür hale getirilir; böylece arayüz gereksiz N/A kutucuklarından arındırılmış temiz bir görünüme kavuşturuldu.</li>
                    </ul>

                    <h2 id="v1-4-9" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.9</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Detail Dashboard):</span> Belirli bir cluster'ın detay sayfasına girildiğinde (örn: <b>Araç Plaka Takip Sistemi</b>), diğer ilgisiz cluster'ların metrik kartlarının karışmasını önleyen filtreleme eklendi. Artık her cluster'ın Dashboard sekmesinde yalnızca o cluster'a ait sunucu düğümleri (Primary &amp; Standby) gösterilir. Ayrıca breadcrumb navigasyonu (<code>Project Name (ID: X)</code>) dinamikleştirildi.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.5.0")

# Bump asset version to v=57
html = html.replace('v=56', 'v=57')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with v1.5.0 and v=57")
