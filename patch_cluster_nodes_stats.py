with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace duplicate stat IDs inside id="tab-content-nodes"
tab_nodes_start = html.find('id="tab-content-nodes"')
tab_nodes_end = html.find('id="tab-content-performance"', tab_nodes_start)

tab_nodes_chunk = html[tab_nodes_start:tab_nodes_end]
tab_nodes_chunk_updated = tab_nodes_chunk.replace('id="stat-operational"', 'id="cluster-stat-operational"') \
                                         .replace('id="stat-failed"', 'id="cluster-stat-failed"') \
                                         .replace('id="stat-offline"', 'id="cluster-stat-offline"') \
                                         .replace('id="stat-shutdown"', 'id="cluster-stat-shutdown"') \
                                         .replace('id="stat-recovering"', 'id="cluster-stat-recovering"') \
                                         .replace('id="stat-unknown"', 'id="cluster-stat-unknown"') \
                                         .replace('id="stat-all"', 'id="cluster-stat-all"')

html = html[:tab_nodes_start] + tab_nodes_chunk_updated + html[tab_nodes_end:]
print("Updated tab-content-nodes stat IDs in index.html")

# 2. Update Left Sidebar in Changelog for v1.4.7
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.6 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-5').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.5</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.7 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.6</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-5').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.5</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.4.7 (Latest)")

# 3. Update TOC for v1.4.7
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.6 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-5').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.5 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.7 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-6').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.6 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-5').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.5 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.4.7 Release")

# 4. Update Middle Content for v1.4.7
old_content_top = """                    <h2 id="v1-4-6" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.6</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Improvement (Sunucu Yönetim Dashboard):</span> Sunucu Yönetim Dashboard ekranındaki metrik biçimlendirmeleri (İşlem Yükü: <code>1,152,848 ✓ / 551,667 ✗</code>, Çalışma Süresi: <code>6 gün</code>, Depolama ve Bağlantılar) Araç Plaka Yönetim Sistemi formatı ile birebir uyumlu ve estetik hale getirildi. Canlı Render API doğrulaması tamamlandı.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-4-7" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.7</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Cluster Detail Nodes Tab):</span> Cluster Detay sayfasındaki Nodes sekmesinde düğüm sayısı kartlarının <code>0</code> olarak görünmesine sebep olan DOM ID çakışması giderildi (<code>cluster-stat-*</code>). Artık seçili cluster'a ait tüm düğümler anında <code>Operational: 2</code>, <code>All: 2</code> vb. olarak dinamik şekilde kartlara yansıtılmaktadır.</li>
                    </ul>

                    <h2 id="v1-4-6" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.6</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Improvement (Sunucu Yönetim Dashboard):</span> Sunucu Yönetim Dashboard ekranındaki metrik biçimlendirmeleri (İşlem Yükü: <code>1,152,848 ✓ / 551,667 ✗</code>, Çalışma Süresi: <code>6 gün</code>, Depolama ve Bağlantılar) Araç Plaka Yönetim Sistemi formatı ile birebir uyumlu ve estetik hale getirildi. Canlı Render API doğrulaması tamamlandı.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.4.7")

# Bump asset version to v=54
html = html.replace('v=53', 'v=54')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update main.js renderNodes function to target cluster-stat-* IDs
old_render_nodes_stats = """        // Update stats
        ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(id => {
            const el = document.getElementById('stat-' + id);
            let val = 0;
            if (id === 'operational') val = stats['Operational'];
            if (id === 'failed') val = stats['Failed'];
            if (id === 'offline') val = stats['Offline'];
            if (id === 'shutdown') val = stats['Shut Down'];
            if (id === 'recovering') val = stats['Recovering'];
            if (id === 'unknown') val = stats['Unknown State'];
            if (el) el.innerText = val;
        });
        const elAll = document.getElementById('stat-all');
        if (elAll) elAll.innerText = nodes.length;"""

new_render_nodes_stats = """        // Update stats for cluster detail nodes tab
        ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(id => {
            const el = document.getElementById('cluster-stat-' + id);
            let val = 0;
            if (id === 'operational') val = stats['Operational'];
            if (id === 'failed') val = stats['Failed'];
            if (id === 'offline') val = stats['Offline'];
            if (id === 'shutdown') val = stats['Shut Down'];
            if (id === 'recovering') val = stats['Recovering'];
            if (id === 'unknown') val = stats['Unknown State'];
            if (el) el.innerText = val;
        });
        const elAll = document.getElementById('cluster-stat-all');
        if (elAll) elAll.innerText = nodes.length;"""

if old_render_nodes_stats in js:
    js = js.replace(old_render_nodes_stats, new_render_nodes_stats, 1)
    print("Updated renderNodes stats in main.js")

# Also reset stats in renderNodes when no nodes
old_reset_stats = """            // Reset stats
            ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown', 'all'].forEach(id => {
                const el = document.getElementById('stat-' + id);
                if (el) el.innerText = '0';
            });"""

new_reset_stats = """            // Reset stats for cluster detail nodes tab
            ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown', 'all'].forEach(id => {
                const el = document.getElementById('cluster-stat-' + id);
                if (el) el.innerText = '0';
            });"""

if old_reset_stats in js:
    js = js.replace(old_reset_stats, new_reset_stats, 1)
    print("Updated reset stats in main.js")

js = js.replace("changelogAnchors = ['v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=53', 'v=54')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with v1.4.7 anchor and v=54")
