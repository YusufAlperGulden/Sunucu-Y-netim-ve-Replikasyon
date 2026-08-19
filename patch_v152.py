with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.5.2
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.1 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.0</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.2 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.0</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.5.2 (Latest)")

# Update TOC for v1.5.2
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.1 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.0 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.1 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.0 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.5.2 Release")

# Update Middle Content for v1.5.2
old_content_top = """                    <h2 id="v1-5-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.1</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Switch &amp; Telemetry Reset):</span> <b>E-mail Okuma Programı</b> ve <b>Araç Plaka Takip Sistemi</b> gibi farklı cluster'lar arasında geçiş yapılırken metrik kartlarının karışması ve eski kümenin kartlarının ekranda kalması sorunu hash normalizasyonu ve tam DOM temizliği (DOM wipe &amp; fresh reload) ile giderildi. Her cluster kendi başlığı (örn: <code>E-MAIL OKUMA PROGRAMI</code>) ve kendi sunucuları ile anında yüklenir.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.2</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Improvement (Cluster Metric Table Dynamic Mapping):</span> Her cluster için takip edilen ana tablo ayrıştırıldı. <b>Araç Plaka Takip Sistemi</b> için <code>vehicles</code> tablosu (<code>6 Araç (vehicles)</code>), <b>E-mail Okuma Programı</b> için ise PostgreSQL üzerindeki canlı <code>emails</code> tablosu (<code>3 E-posta (emails)</code>) otomatik sorgulanarak ekrana canlı ve doğru şekilde yansıtıldı.</li>
                    </ul>

                    <h2 id="v1-5-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.1</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Switch &amp; Telemetry Reset):</span> <b>E-mail Okuma Programı</b> ve <b>Araç Plaka Takip Sistemi</b> gibi farklı cluster'lar arasında geçiş yapılırken metrik kartlarının karışması ve eski kümenin kartlarının ekranda kalması sorunu hash normalizasyonu ve tam DOM temizliği (DOM wipe &amp; fresh reload) ile giderildi. Her cluster kendi başlığı (örn: <code>E-MAIL OKUMA PROGRAMI</code>) ve kendi sunucuları ile anında yüklenir.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.5.2")

# Bump asset version to v=59
html = html.replace('v=58', 'v=59')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("changelogAnchors = ['v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=58', 'v=59')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated index.html and main.js with v1.5.2 and v=59")
