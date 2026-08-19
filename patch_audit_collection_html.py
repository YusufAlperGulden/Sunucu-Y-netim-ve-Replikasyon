with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update UI audit data collection toggle & button in index.html
old_audit_html = """                        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 40px;">
                            <span style="font-size: 0.9rem;">UI audit data collection</span>
                            <div style="width: 40px; height: 20px; background: #d1d5db; border-radius: 10px; position: relative;">
                                <div style="width: 16px; height: 16px; background: white; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                            </div>
                            <button style="background: white; color: #9ca3af; border: 1px solid #e5e7eb; border-radius: 4px; padding: 6px 16px; font-size: 0.85rem; cursor: not-allowed; display: flex; align-items: center; gap: 8px;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg> download audit data
                            </button>
                        </div>"""

new_audit_html = """                        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 40px;">
                            <span style="font-size: 0.9rem;">UI audit data collection</span>
                            <div id="btn-toggle-ui-audit" onclick="window.toggleUiAudit()" style="width: 44px; height: 22px; background: #d1d5db; border-radius: 11px; position: relative; cursor: pointer; transition: all 0.25s ease;">
                                <div id="dot-toggle-ui-audit" style="width: 18px; height: 18px; background: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: all 0.25s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></div>
                            </div>
                            <button id="btn-download-ui-audit" onclick="window.downloadUiAuditData()" disabled style="background: white; color: #9ca3af; border: 1px solid #e5e7eb; border-radius: 4px; padding: 6px 16px; font-size: 0.85rem; cursor: not-allowed; display: flex; align-items: center; gap: 8px; transition: all 0.2s;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg> download audit data
                            </button>
                        </div>"""

if old_audit_html in html:
    html = html.replace(old_audit_html, new_audit_html, 1)
    print("Replaced UI audit toggle & button HTML")

# 2. Update Left Sidebar in Changelog for v1.6.2
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.1 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.0</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.2 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.0</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# 3. Update TOC for v1.6.2
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.1 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.0 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.1 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.0 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# 4. Update Middle Content for v1.6.2
old_content_top = """                    <h2 id="v1-6-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.1</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Zero-Dependency Direct Nodes Initialization):</span> Nodes sayfasının açılabilmesi için önce Dashboard sayfasına gitme zorunluluğuna neden olan sayfa başlatma döngüsü tamamen bağımsızlaştırıldı. Sayfa yüklendiğinde arka planda tüm cluster ve node ağacı otomatik senkronize edilerek doğrudan Nodes sekmesine girildiğinde düğümlerin anında, gecikmesiz listelenmesi sağlandı.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-6-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.2</h2>
                    
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
                    </ul>

                    <h2 id="v1-6-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.1</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Zero-Dependency Direct Nodes Initialization):</span> Nodes sayfasının açılabilmesi için önce Dashboard sayfasına gitme zorunluluğuna neden olan sayfa başlatma döngüsü tamamen bağımsızlaştırıldı. Sayfa yüklendiğinde arka planda tüm cluster ve node ağacı otomatik senkronize edilerek doğrudan Nodes sekmesine girildiğinde düğümlerin anında, gecikmesiz listelenmesi sağlandı.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=69
html = html.replace('v=68', 'v=69')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with live UI audit collection and v1.6.2 (v69)")
