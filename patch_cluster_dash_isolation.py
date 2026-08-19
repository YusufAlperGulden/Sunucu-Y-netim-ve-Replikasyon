with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update showDetailView to clean container and update breadcrumb
old_show_detail = """    function showDetailView(proj) {
        window.location.hash = 'project-detail-view';
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';
        currentProjectId = proj.id;
        
        const el_detail_proj_name = document.getElementById('detail-proj-name'); if(el_detail_proj_name) el_detail_proj_name.innerText = proj.name;
        const el_detail_proj_desc = document.getElementById('detail-proj-desc'); if(el_detail_proj_desc) el_detail_proj_desc.innerText = proj.description || 'No description';
        
        renderNodes(proj.nodes);
        
        // Ensure "Dashboards" tab is active by default
        const dashTab = document.querySelector('.cluster-tab[data-tab="dashboards"]');
        if(dashTab) dashTab.click();
    }"""

new_show_detail = """    function showDetailView(proj) {
        window.location.hash = 'project-detail-view';
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';
        currentProjectId = proj.id;
        
        const el_detail_proj_name = document.getElementById('detail-proj-name'); if(el_detail_proj_name) el_detail_proj_name.innerText = proj.name;
        const el_detail_proj_desc = document.getElementById('detail-proj-desc'); if(el_detail_proj_desc) el_detail_proj_desc.innerText = proj.description || 'No description';
        const el_breadcrumb = document.getElementById('detail-proj-breadcrumb-name'); if(el_breadcrumb) el_breadcrumb.innerText = `${proj.name} (ID: ${proj.id})`;
        
        // Clear previous cluster cards from container
        const container = document.getElementById('dashboard-metrics-container');
        if (container) container.innerHTML = '';
        
        renderNodes(proj.nodes);
        
        // Ensure "Dashboards" tab is active by default
        const dashTab = document.querySelector('.cluster-tab[data-tab="dashboards"]');
        if(dashTab) dashTab.click();
        
        fetchDashboardMetrics();
    }"""

if old_show_detail in js:
    js = js.replace(old_show_detail, new_show_detail, 1)
    print("Updated showDetailView")

# 2. Update fetchDashboardMetrics to only display current project's nodes when in detail view
idx_start = js.find('async function fetchDashboardMetrics()')
idx_end = js.find('function startDashboardInterval()', idx_start)

new_fetch_dash = """async function fetchDashboardMetrics() {
        try {
            const container = document.getElementById('dashboard-metrics-container');
            if(!container) return;

            const projRes = await apiFetch('/api/projects');
            if (!projRes.ok) return;
            const allProjs = await projRes.json();
            
            if (allProjs.length === 0) {
                container.innerHTML = '<div class="loading-state">No projects found. Add a project to view metrics.</div>';
                return;
            }
            
            // If inside project-detail-view, ONLY display metrics for currentProjectId
            const isDetailView = (window.location.hash === 'project-detail-view' || (detailView && detailView.style.display !== 'none'));
            const targetProjs = (isDetailView && currentProjectId) 
                ? allProjs.filter(p => p.id === currentProjectId)
                : allProjs;
                
            if (targetProjs.length === 0) {
                container.innerHTML = '<div class="loading-state">Cluster not found.</div>';
                return;
            }
            
            // Fetch metrics for target projects concurrently
            const metricPromises = targetProjs.map(p => apiFetch(`/api/projects/${p.id}/metrics`).then(r => r.ok ? r.json() : []));
            const metricsResults = await Promise.all(metricPromises);
            
            // Flat list of all nodes returned for target projects
            const allTargetNodes = metricsResults.flat();
            
            if (container.querySelector('.loading-state')) {
                container.innerHTML = '';
            }
            
            // Remove columns for nodes that don't belong to target projects
            const allTargetNodeIds = allTargetNodes.map(n => "dash-node-" + n.id);
            Array.from(container.children).forEach(child => {
                if (!allTargetNodeIds.includes(child.id)) {
                    child.remove();
                }
            });
            
            targetProjs.forEach((proj, i) => {
                const dataList = metricsResults[i];
                if (!dataList || dataList.length === 0) return;
                
                dataList.forEach(node => {
                    let col = document.getElementById("dash-node-" + node.id);
                    if(!col) {
                        col = document.createElement('div');
                        col.className = 'metrics-column';
                        col.id = "dash-node-" + node.id;
                        
                        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'];
                        const projColor = colors[proj.id % colors.length] || 'var(--primary)';
                        
                        const headerHtml = `
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 20px;">
                                <div>
                                    <div style="font-size: 0.8rem; color: ${projColor}; text-transform: uppercase; font-weight: bold; margin-bottom: 4px;">${escapeHTML(proj.name)}</div>
                                    <h2 style="margin: 0; font-size: 1.2rem;">${escapeHTML(node.name)} <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-muted);">(${escapeHTML(node.role)})</span></h2>
                                </div>
                                <span class="status-badge status-offline" id="metric-${node.id}-status">Offline</span>
                            </div>
                        `;
                        
                        const metricsHtml = `
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
                        `;
                        col.innerHTML = headerHtml + metricsHtml;
                        container.appendChild(col);
                    }
                    
                    const m = node.metrics;
                    if(m && m.status === 'online') {
                        const statusEl = document.getElementById("metric-" + node.id + "-status");
                        if(statusEl) { statusEl.className = 'status-badge status-online'; statusEl.innerText = 'Aktif'; }
                        
                        const setEl = (id, val) => { const el = document.getElementById(id); if(el) el.innerText = val; };
                        setEl("metric-" + node.id + "-ping", m.ping);
                        setEl("metric-" + node.id + "-lag", m.lag);
                        setEl("metric-" + node.id + "-storage", m.storage);
                        setEl("metric-" + node.id + "-conn", m.connections);
                        setEl("metric-" + node.id + "-xact", m.xact);
                        setEl("metric-" + node.id + "-cache", m.cache_hit);
                        setEl("metric-" + node.id + "-version", m.version);
                        setEl("metric-" + node.id + "-cpu", m.cpu_usage || "N/A");
                        setEl("metric-" + node.id + "-ram", m.ram_usage || "N/A");
                        setEl("metric-" + node.id + "-plates", m.plates || "N/A");
                        setEl("metric-" + node.id + "-uptime", m.uptime || "N/A");
                    } else if (m && m.status === 'offline') {
                        const statusEl = document.getElementById("metric-" + node.id + "-status");
                        if(statusEl) { statusEl.className = 'status-badge status-offline'; statusEl.innerText = 'Çevrimdışı'; }
                        ['cpu','ram','ping','lag','storage','conn','xact','plates','cache','uptime'].forEach(key => {
                            const el = document.getElementById(`metric-${node.id}-${key}`);
                            if(el) el.innerText = '-';
                        });
                    }
                });
            });
        } catch(e) {
            console.error('fetchDashboardMetrics error:', e);
        }
    }
    
    """

if idx_start != -1 and idx_end != -1:
    js = js[:idx_start] + new_fetch_dash + js[idx_end:]
    print("Replaced fetchDashboardMetrics")

# Update main.js router anchors and bump to v=56
js = js.replace("changelogAnchors = ['v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=55', 'v=56')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html Changelog for v1.4.9
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.4.9
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.8 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.7</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.9 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.8</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.7</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.4.9 (Latest)")

# Update TOC for v1.4.9
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.8 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.7 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-9').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.9 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-8').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.8 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-7').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.7 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.4.9 Release")

# Update Middle Content for v1.4.9
old_content_top = """                    <h2 id="v1-4-8" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.8</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (User Management - Teams Tab):</span> User Management ekranına <b>Teams</b> sekmesi tablosu eklendi. "Name", "Owner", "Created", "Actions" sütun başlıkları ve standart boş durum mesajı (<code>No teams created yet.</code>) eklendi.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-4-9" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.9</h2>
                    
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
                    </ul>

                    <h2 id="v1-4-8" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.8</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature (User Management - Teams Tab):</span> User Management ekranına <b>Teams</b> sekmesi tablosu eklendi. "Name", "Owner", "Created", "Actions" sütun başlıkları ve standart boş durum mesajı (<code>No teams created yet.</code>) eklendi.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.4.9")

# Bump asset version to v=56
html = html.replace('v=55', 'v=56')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with v1.4.9 and v=56")
