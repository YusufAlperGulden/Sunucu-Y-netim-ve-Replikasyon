with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx_start = js.find('async function fetchDashboardMetrics()')
if idx_start == -1:
    idx_start = js.find('function fetchDashboardMetrics()')

idx_end = js.find('const btnSyncRepDashboard', idx_start)

print("idx_start:", idx_start, "idx_end:", idx_end)

new_fetch_func = """async function fetchDashboardMetrics() {
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
            
            // When inside a project's detail view, ONLY render metrics for currentProjectId!
            const currentHash = (window.location.hash || '').replace(/^#/, '');
            const isDetailView = (currentHash === 'project-detail-view' || (detailView && getComputedStyle(detailView).display !== 'none'));
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
            
            // Remove columns for nodes that don't belong to current target cluster!
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
                        setEl("metric-" + node.id + "-plates", m.plates || m.row_count || "N/A");
                        setEl("metric-" + node.id + "-uptime", m.uptime || "N/A");
                        
                        // Hide CPU & RAM if N/A
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
                        }
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
        } catch (e) {
            console.error("Dashboard error:", e);
        }
    }
    
    """

js = js[:idx_start] + new_fetch_func + js[idx_end:]

# Update Changelog & version anchors to v1.5.3 (v60)
js = js.replace("changelogAnchors = ['v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=59', 'v=60')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.5.3
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.2 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.1</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.3 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.2</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.1</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)
    print("Updated Left Sidebar with v1.5.3 (Latest)")

# Update TOC for v1.5.3
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.1 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.3 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.2 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.1 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC with v1.5.3 Release")

# Update Middle Content for v1.5.3
old_content_top = """                    <h2 id="v1-5-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.2</h2>
                    
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
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.3</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Strict Cluster Dashboard Isolation):</span> Sunucu Yönetim Dashboard telemetri döngüsü (<code>fetchDashboardMetrics</code>) tamamen yeniden yazıldı. Artık <b>Araç Plaka Takip Sistemi</b> açıldığında yalnızca Araç Plaka'nın 2 sunucusu; <b>E-mail Okuma Programı</b> açıldığında ise yalnızca E-mail Okuma Programı'nın 2 sunucusu gösterilir. Diğer tüm cluster'lara ait eski veya yabancı kartlar container'dan anında temizlenir.</li>
                    </ul>

                    <h2 id="v1-5-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.2</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Improvement (Cluster Metric Table Dynamic Mapping):</span> Her cluster için takip edilen ana tablo ayrıştırıldı. <b>Araç Plaka Takip Sistemi</b> için <code>vehicles</code> tablosu (<code>6 Araç (vehicles)</code>), <b>E-mail Okuma Programı</b> için ise PostgreSQL üzerindeki canlı <code>emails</code> tablosu (<code>3 E-posta (emails)</code>) otomatik sorgulanarak ekrana canlı ve doğru şekilde yansıtıldı.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)
    print("Updated Middle Content with v1.5.3")

# Bump asset version to v=60
html = html.replace('v=59', 'v=60')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with v1.5.3 and v=60")
