with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Particle size to much bigger
old_particle_size = "this.size = Math.random() * 80 + 30;"
new_particle_size = "this.size = Math.random() * 220 + 120;"

if old_particle_size in js:
    js = js.replace(old_particle_size, new_particle_size, 1)
    print("Updated particle size to bigger and more bigger (120 - 340 radius)")

# Adjust alpha and particle count
old_alpha = "ctx.globalAlpha = 0.5;"
new_alpha = "ctx.globalAlpha = 0.42;"
if old_alpha in js:
    js = js.replace(old_alpha, new_alpha, 1)

old_count = "for (let i = 0; i < 50; i++) {"
new_count = "for (let i = 0; i < 40; i++) {"
if old_count in js:
    js = js.replace(old_count, new_count, 1)

# Update Changelog anchors and asset version
js = js.replace("changelogAnchors = ['v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=61', 'v=62')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.5.5
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.4 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.3</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.5 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.4</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.3</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# Update TOC for v1.5.5
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.4 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.3 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-5').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.5 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.4 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.3 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# Update Middle Content for v1.5.5
old_content_top = """                    <h2 id="v1-5-4" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.4</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Major Feature (Cluster Performance Module):</span> ClusterControl ile birebir uyumlu <b>Performance</b> sekmesi entegre edildi. <code>DB Status</code> (Canlı durum değişkenleri karşılaştırması), <code>DB Growth</code> (Depolama &amp; Hacim analitiği), <code>DB Variables</code> (Aranabilir konfigürasyon değişkenleri), <code>Query Monitor</code> (Canlı aktif SQL sorguları), <code>Query Monitor/Agents</code> (Ajan yönetimi), <code>Advisors</code> (Otomatik sağlık danışmanları), <code>Schema Analyzer</code> (Tablo ve sütun yapısı analizi) ve <code>Transaction Deadlocks</code> (Kilitlenme tespiti) alt sekmeleri aktif hale getirildi.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-5" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.5</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Visual Design (Larger Floating Bubbles):</span> Giriş ekranındaki (Login screen) hareketli baloncuklar (floating bubbles) daha büyük, canlı ve estetik boyutlara yükseltildi (120px - 340px yarıçap). Yumuşak geçişler ve şeffaf katman efektleri uygulandı.</li>
                    </ul>

                    <h2 id="v1-5-4" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.4</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Major Feature (Cluster Performance Module):</span> ClusterControl ile birebir uyumlu <b>Performance</b> sekmesi entegre edildi. <code>DB Status</code> (Canlı durum değişkenleri karşılaştırması), <code>DB Growth</code> (Depolama &amp; Hacim analitiği), <code>DB Variables</code> (Aranabilir konfigürasyon değişkenleri), <code>Query Monitor</code> (Canlı aktif SQL sorguları), <code>Query Monitor/Agents</code> (Ajan yönetimi), <code>Advisors</code> (Otomatik sağlık danışmanları), <code>Schema Analyzer</code> (Tablo ve sütun yapısı analizi) ve <code>Transaction Deadlocks</code> (Kilitlenme tespiti) alt sekmeleri aktif hale getirildi.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=62
html = html.replace('v=61', 'v=62')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with v1.5.5 (v62)")
