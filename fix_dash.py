# -*- coding: utf-8 -*-

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_idx = js.find('    async function fetchDashboardMetrics() {')
if start_idx != -1:
    end_idx = js.find('    const btnSyncRepDashboard', start_idx)
    if end_idx != -1:
        # We replace everything between start_idx and end_idx
        old_func = js[start_idx:end_idx]
        
        new_func = '''    async function fetchDashboardMetrics() {
        try {
            const projRes = await apiFetch('/api/projects');
            if (!projRes.ok) return;
            const projs = await projRes.json();
            
            const container = document.getElementById('dashboard-metrics-container');
            if(!container) return;

            if (projs.length === 0) {
                container.innerHTML = '<div class="loading-state">No projects found. Add a project to view metrics.</div>';
                return;
            }
            
            if (container.querySelector('.loading-state')) {
                container.innerHTML = '';
            }
            
            // Remove columns for nodes that no longer exist
            const allNodeIds = projs.flatMap(p => p.nodes.map(n => "dash-node-" + n.id));
            Array.from(container.children).forEach(child => {
                if (!allNodeIds.includes(child.id)) {
                    child.remove();
                }
            });
            
            // Fetch metrics for all projects concurrently
            const metricPromises = projs.map(p => apiFetch("/api/projects/" + p.id + "/metrics").then(r => r.ok ? r.json() : []));
            const metricsResults = await Promise.all(metricPromises);
            
            projs.forEach((proj, i) => {
                const dataList = metricsResults[i];
                if (!dataList || dataList.length === 0) return;
                
                dataList.forEach(node => {
                    let col = document.getElementById("dash-node-" + node.id);
                    if(!col) {
                        col = document.createElement('div');
                        col.className = 'metrics-column';
                        col.id = "dash-node-" + node.id;
                        
                        const headerHtml = 
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 20px;">
                                <div>
                                    <div style="font-size: 0.8rem; color: var(--primary); text-transform: uppercase; font-weight: bold; margin-bottom: 4px;">\</div>
                                    <h2 style="margin: 0; font-size: 1.2rem;">\ <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-muted);">(\)</span></h2>
                                </div>
                                <span class="status-badge status-offline" id="metric-\-status">Offline</span>
                            </div>
                        ;
                        
                        const metricsHtml = 
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-\-ping">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Senkronizasyon (Lag)</div><div class="metric-val" id="metric-\-lag">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Depolama (Storage)</div><div class="metric-val" id="metric-\-storage">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Bağlantılar (Aktif/Top.)</div><div class="metric-val" id="metric-\-conn">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">İşlem Yükü (Başarılı / İptal)</div><div class="metric-val" id="metric-\-xact">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Kayıtlı Araç Sayısı</div><div class="metric-val" id="metric-\-plates">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Önbellek Başarısı</div><div class="metric-val" id="metric-\-cache">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Çalışma Süresi</div><div class="metric-val" id="metric-\-uptime">-</div></div>
                            </div>
                            <div style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted); text-align: right;">
                                Motor Sürümü: <span id="metric-\-version">-</span>
                            </div>
                        ;
                        col.innerHTML = headerHtml + metricsHtml;
                        container.appendChild(col);
                    }
                    
                    const m = node.metrics;
                    if(m && m.ping !== undefined) {
                        document.getElementById("metric-" + node.id + "-status").className = 'status-badge status-online';
                        document.getElementById("metric-" + node.id + "-status").innerText = 'Aktif';
                        
                        document.getElementById("metric-" + node.id + "-ping").innerText = m.ping + 'ms';
                        document.getElementById("metric-" + node.id + "-lag").innerText = m.lag !== 'N/A' ? (m.lag + 'ms') : 'N/A';
                        document.getElementById("metric-" + node.id + "-storage").innerText = m.storage + ' kB';
                        document.getElementById("metric-" + node.id + "-conn").innerText = m.conn_active + ' / ' + m.conn_max;
                        document.getElementById("metric-" + node.id + "-xact").innerText = m.xact_commit + ' ✔ / ' + m.xact_rollback + ' ✖';
                        document.getElementById("metric-" + node.id + "-cache").innerText = m.blks_hit_percent + '%';
                        document.getElementById("metric-" + node.id + "-version").innerText = m.version;
                        document.getElementById("metric-" + node.id + "-uptime").innerText = m.uptime;
                        document.getElementById("metric-" + node.id + "-plates").innerText = m.plates;
                    } else {
                        document.getElementById("metric-" + node.id + "-status").className = 'status-badge status-offline';
                        document.getElementById("metric-" + node.id + "-status").innerText = 'Çevrimdışı';
                    }
                });
            });
        } catch (e) {
            console.error("Dashboard error:", e);
        }
    }
    
'''
        js_updated = js[:start_idx] + new_func + js[end_idx:]
        with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
            f.write(js_updated)
        print("Updated js successfully")
