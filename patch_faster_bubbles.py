with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Particle size and speed
old_particle_block = """        class Particle {
            constructor() {
                this.size = Math.random() * 220 + 120;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 0.4;
                this.vy = (Math.random() - 0.5) * 0.4;
                
                if (Math.abs(this.vx) < 0.1) this.vx = 0.2 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.1) this.vy = 0.2 * Math.sign(this.vy || 1);
            }"""

new_particle_block = """        class Particle {
            constructor() {
                this.size = Math.random() * 280 + 180;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 2.2;
                this.vy = (Math.random() - 0.5) * 2.2;
                
                if (Math.abs(this.vx) < 0.8) this.vx = 1.1 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.8) this.vy = 1.1 * Math.sign(this.vy || 1);
            }"""

if old_particle_block in js:
    js = js.replace(old_particle_block, new_particle_block, 1)
    print("Updated particle size (180-460px) and speed (2.2x) in main.js")

# Update Changelog anchors and asset version in main.js
js = js.replace("changelogAnchors = ['v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=64', 'v=65')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.5.8
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.7 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.6</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.8 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.7</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.6</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# Update TOC for v1.5.8
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.7 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.6 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.8 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.7 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.6 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# Update Middle Content for v1.5.8
old_content_top = """                    <h2 id="v1-5-7" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.7</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">UI/UX (Cluster Alarms Table Structure):</span> Cluster Detay altındaki <b>Alarms</b> sekmesi ClusterControl ile birebir uyumlu tam tablo yapısına kavuşturuldu. "Title", "Severity", "Category", "Cluster", "Hostname", "When", "Actions" sütun başlıkları ve standart boş durum (<code>You haven't received alarms yet. When you do, it'll show up here.</code>) entegre edildi.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-8" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.8</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Visual Dynamic (Extra Large &amp; Faster Floating Bubbles):</span> Giriş ekranındaki (Login screen) baloncuklar ekstra büyük boyutlara (180px - 460px yarıçap / 360px - 920px çap) yükseltildi ve hareket hızı ~4 kat artırılarak ekran üzerinde daha akıcı ve dinamik yüzmeleri sağlandı.</li>
                    </ul>

                    <h2 id="v1-5-7" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.7</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">UI/UX (Cluster Alarms Table Structure):</span> Cluster Detay altındaki <b>Alarms</b> sekmesi ClusterControl ile birebir uyumlu tam tablo yapısına kavuşturuldu. "Title", "Severity", "Category", "Cluster", "Hostname", "When", "Actions" sütun başlıkları ve standart boş durum (<code>You haven't received alarms yet. When you do, it'll show up here.</code>) entegre edildi.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=65
html = html.replace('v=64', 'v=65')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html and main.js with faster & larger bubbles and v1.5.8 (v65)")
