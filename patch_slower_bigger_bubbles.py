with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Particle size (bigger: 150-370px) and speed (slower: 0.35x)
old_particle_block = """        class Particle {
            constructor() {
                this.size = Math.random() * 45 + 15;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 3.5;
                this.vy = (Math.random() - 0.5) * 3.5;
                
                if (Math.abs(this.vx) < 1.2) this.vx = 1.6 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 1.2) this.vy = 1.6 * Math.sign(this.vy || 1);
            }"""

new_particle_block = """        class Particle {
            constructor() {
                this.size = Math.random() * 220 + 150;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 0.35;
                this.vy = (Math.random() - 0.5) * 0.35;
                
                if (Math.abs(this.vx) < 0.1) this.vx = 0.18 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.1) this.vy = 0.18 * Math.sign(this.vy || 1);
            }"""

if old_particle_block in js:
    js = js.replace(old_particle_block, new_particle_block, 1)
    print("Updated particle size (150-370px) and speed (slower: 0.35x)")

# Adjust particle count back to 35 for large bubbles
js = js.replace("for (let i = 0; i < 65; i++) {", "for (let i = 0; i < 35; i++) {")

# Update Changelog anchors and asset version in main.js
js = js.replace("changelogAnchors = ['v1-6-2', 'v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-6-3', 'v1-6-2', 'v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=69', 'v=70')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.6.3
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.2 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.1</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.3 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.2</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.1</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# Update TOC for v1.6.3
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.1 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.3 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.2 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.1 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# Update Middle Content for v1.6.3
old_content_top = """                    <h2 id="v1-6-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.2</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (Live UI Audit Data Collection &amp; Export):</span> Ayarlar (Settings) altındaki <b>UI audit data collection</b> aracı tamamen çalışır ve etkileşimli hale getirildi. Anahtar açıldığında arayüz olayları (tıklamalar, sayfa geçişleri, API istekleri ve performans metrikleri) kaydedilir ve <code>download audit data</code> butonu ile anında teşhis JSON raporu olarak indirilebilir.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-6-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.3</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Visual Harmony (Calm, Slower &amp; Extra Large Floating Bubbles):</span> Giriş ekranındaki baloncuklar tekrar büyük ve ferah boyutlara yükseltildi (150px - 370px yarıçap / 300px - 740px çap), hareket hızları yumuşak ve sakin bir akışa (`0.35x`) çekildi.</li>
                    </ul>

                    <h2 id="v1-6-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.2</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (Live UI Audit Data Collection &amp; Export):</span> Ayarlar (Settings) altındaki <b>UI audit data collection</b> aracı tamamen çalışır ve etkileşimli hale getirildi. Anahtar açıldığında arayüz olayları (tıklamalar, sayfa geçişleri, API istekleri ve performans metrikleri) kaydedilir ve <code>download audit data</code> butonu ile anında teşhis JSON raporu olarak indirilebilir.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=70
html = html.replace('v=69', 'v=70')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html and main.js with slower & bigger bubbles and v1.6.3 (v70)")
