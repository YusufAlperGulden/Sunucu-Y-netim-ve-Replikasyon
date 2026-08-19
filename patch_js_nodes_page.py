import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add nodes-view routing in handleRouting
old_routing = """        } else if (hash === 'settings-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof fetchProfile === 'function') fetchProfile();
        } else {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        }"""

new_routing = """        } else if (hash === 'settings-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof fetchProfile === 'function') fetchProfile();
        } else if (hash === 'nodes-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof fetchNodesPage === 'function') fetchNodesPage();
        } else {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        }"""

if "nodes-view" not in content:
    content = content.replace(old_routing, new_routing)
    print("Added nodes-view routing")
else:
    print("nodes-view routing already exists")

# 2. Add fetchNodesPage function before the fetchRecentAlarms function
fetch_nodes_page = """
async function fetchNodesPage() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 20px; color: #6b7280;">Yükleniyor...</td></tr>';
    
    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) return;
        const projects = await res.json();
        
        // Flatten all nodes from all projects
        const allNodes = [];
        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                allNodes.push({
                    host: node.name,
                    port: '5432',
                    ip: 'N/A',
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role || 'Unknown',
                    cluster: proj.name + ' (ID:' + proj.id + ')',
                    version: '-',
                    seen: 'Az önce',
                    nodeObj: node,
                    projObj: proj
                });
            }
        }
        
        // Update stat counters
        const statAll = document.getElementById('stat-all');
        const statOp = document.getElementById('stat-operational');
        if (statAll) statAll.innerText = allNodes.length;
        if (statOp) statOp.innerText = allNodes.length;
        ['stat-failed', 'stat-offline', 'stat-shutdown', 'stat-recovering', 'stat-unknown'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = '0';
        });
        
        if (allNodes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 40px; color: #6b7280;">No nodes found. Create a cluster and add nodes first.</td></tr>';
            return;
        }
        
        // Try to get real metrics for version info
        const metricPromises = projects.map(p => 
            apiFetch(`/api/projects/${p.id}/metrics`).then(r => r.ok ? r.json() : []).catch(() => [])
        );
        const metricsAll = (await Promise.all(metricPromises)).flat();
        
        tbody.innerHTML = '';
        const now = new Date();
        
        allNodes.forEach(n => {
            // Try to find metrics for this node
            const nodeMetrics = metricsAll.find(m => m.id === n.nodeObj.id);
            const m = nodeMetrics ? nodeMetrics.metrics : null;
            
            const status = (m && m.status === 'online') ? 'Operational' : (m && m.status === 'offline' ? 'Offline' : 'Operational');
            const version = m ? (m.version || '-') : '-';
            const statusColor = status === 'Operational' ? 'var(--success)' : (status === 'Offline' ? '#6b7280' : '#ef4444');
            
            let roleHtml = `<span>${escapeHTML(n.role)}</span>`;
            if (n.role.toLowerCase() === 'primary') {
                roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #dcfce7; color: #16a34a; border: 1px solid #16a34a; margin-left: 6px;">Writable</span>`;
            } else {
                roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #f3f4f6; color: #4b5563; border: 1px solid #4b5563; margin-left: 6px;">Readonly</span>`;
            }
            
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border)';
            tr.innerHTML = `
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(n.host)}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main);">${n.port}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-muted);">${n.ip}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; white-space: nowrap;">
                    <span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;">
                        <div style="width: 6px; height: 6px; border-radius: 50%; background: ${statusColor};"></div> ${status}
                    </span>
                </td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: #059669;">${n.type}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); display: flex; align-items: center;">${roleHtml}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main);">${escapeHTML(n.cluster)}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-muted);">${escapeHTML(version)}</td>
                <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-muted);">${n.seen}</td>
            `;
            tbody.appendChild(tr);
        });
        
    } catch (e) {
        console.error('fetchNodesPage error:', e);
        tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 20px; color: var(--danger);">Hata: ${escapeHTML(e.toString())}</td></tr>`;
    }
}
"""

if "async function fetchNodesPage()" not in content:
    # Append before fetchRecentAlarms
    content = content.replace("\nasync function fetchRecentAlarms()", fetch_nodes_page + "\nasync function fetchRecentAlarms()")
    print("Added fetchNodesPage function")
else:
    print("fetchNodesPage already exists")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
