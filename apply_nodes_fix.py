with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

NEW_NODES_MODULE = """// --- NODES PAGE MANAGEMENT ---
window.nodesPageData = [];
window.currentNodesFilter = 'All';
window.currentSortCol = null;
window.currentSortDir = null;

window.renderNodesPage = function() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const allData = window.nodesPageData || [];

    // Calculate and update stats counters
    let stats = {
        'Operational': 0,
        'Failed': 0,
        'Offline': 0,
        'Shut Down': 0,
        'Recovering': 0,
        'Unknown State': 0
    };

    allData.forEach(n => {
        const s = n.status || 'Operational';
        if (stats[s] !== undefined) stats[s]++;
        else stats['Unknown State']++;
    });

    const statOp = document.getElementById('stat-operational');
    const statAll = document.getElementById('stat-all');
    if (statOp) statOp.innerText = stats['Operational'];
    if (statAll) statAll.innerText = allData.length;
    ['failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(k => {
        const el = document.getElementById('stat-' + k);
        let val = 0;
        if (k === 'failed') val = stats['Failed'];
        if (k === 'offline') val = stats['Offline'];
        if (k === 'shutdown') val = stats['Shut Down'];
        if (k === 'recovering') val = stats['Recovering'];
        if (k === 'unknown') val = stats['Unknown State'];
        if (el) el.innerText = val;
    });

    // Filter by currentNodesFilter
    let filteredData = allData.filter(n => window.currentNodesFilter === 'All' || n.status === window.currentNodesFilter);

    // Sort if active
    if (window.currentSortCol && window.currentSortDir) {
        filteredData.sort((a, b) => {
            let valA = (a[window.currentSortCol] || '').toString().toLowerCase();
            let valB = (b[window.currentSortCol] || '').toString().toLowerCase();
            if (valA < valB) return window.currentSortDir === 'asc' ? -1 : 1;
            if (valA > valB) return window.currentSortDir === 'asc' ? 1 : -1;
            return 0;
        });
    }

    if (filteredData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: #9ca3af; font-size: 0.9rem;">There are no matches</td></tr>`;
        return;
    }

    filteredData.forEach(n => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #f3f4f6';
        tr.style.background = 'white';

        let statusColor = 'var(--success, #10b981)';
        let dotColor = 'var(--success, #10b981)';
        if (n.status === 'Shut Down') { statusColor = '#3b82f6'; dotColor = '#3b82f6'; }
        if (n.status === 'Failed') { statusColor = '#ef4444'; dotColor = '#ef4444'; }
        if (n.status === 'Offline') { statusColor = '#6b7280'; dotColor = '#6b7280'; }

        let statusHtml = `<span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: ${dotColor};"></div> ${escapeHTML(n.status)}</span>`;

        let typeColor = '#059669';
        if (n.type === 'HAProxy') typeColor = '#8b5cf6';
        if (n.type === 'Prometheus') typeColor = '#eab308';
        if (n.type === 'MongoDB') typeColor = '#059669';

        let roleHtml = `<span>${escapeHTML(n.role)}</span>`;
        if (n.badge) {
            roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: ${n.badge.bg}; color: ${n.badge.color}; border: 1px solid ${n.badge.color}; margin-left: 6px;">${n.badge.text}</span>`;
        }

        let logoColor = n.clusterColor || '#059669';
        let logoSvg = n.clusterLogo || '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>';

        tr.innerHTML = `
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(n.host)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(n.port)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: #6b7280; white-space: nowrap;">${escapeHTML(n.ip)}</td>
            <td style="padding: 16px; font-size: 0.85rem; white-space: nowrap;">${statusHtml}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: ${typeColor}; white-space: nowrap;">${escapeHTML(n.type)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; display: flex; align-items: center;">${roleHtml}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${logoColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${logoSvg}</svg>
                    ${escapeHTML(n.cluster)}
                </div>
            </td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.version}</td>
            <td style="padding: 16px; font-size: 0.8rem; color: #6b7280; white-space: nowrap;">${escapeHTML(n.seen)}</td>
            <td style="padding: 16px; font-size: 0.85rem; text-align: center;"><button style="background: none; border: 1px solid var(--border); padding: 4px 8px; border-radius: 4px; cursor: pointer;">...</button></td>
        `;
        tbody.appendChild(tr);
    });
};

window.filterNodes = function(status, el) {
    window.currentNodesFilter = status;
    const cards = document.querySelectorAll('.node-status-card');
    cards.forEach(card => {
        card.style.borderBottom = 'none';
        card.style.background = 'transparent';
    });
    if (el) {
        el.style.borderBottom = '2px solid var(--primary, #6366f1)';
        el.style.background = '#f9fafb';
    }
    window.renderNodesPage();
};

window.sortNodes = function(col) {
    if (window.currentSortCol !== col) {
        window.currentSortCol = col;
        window.currentSortDir = 'asc';
    } else {
        if (window.currentSortDir === 'asc') window.currentSortDir = 'desc';
        else if (window.currentSortDir === 'desc') window.currentSortDir = null;
        else window.currentSortDir = 'asc';
    }

    ['host', 'port', 'status', 'type', 'role', 'cluster', 'seen'].forEach(c => {
        const arr = document.getElementById('nodes-sort-arrows-' + c);
        const txt = document.getElementById('nodes-sort-text-' + c);
        if (arr) arr.innerHTML = '&#9650;&#9660;';
        if (txt) txt.innerText = 'Click to sort ascending';
    });

    if (window.currentSortDir) {
        const arr = document.getElementById('nodes-sort-arrows-' + col);
        const txt = document.getElementById('nodes-sort-text-' + col);
        if (window.currentSortDir === 'asc') {
            if (arr) arr.innerHTML = '&#9650;';
            if (txt) txt.innerText = 'Click to sort descending';
        } else {
            if (arr) arr.innerHTML = '&#9660;';
            if (txt) txt.innerText = 'Click to Cancel Sorting';
        }
    }
    window.renderNodesPage();
};

window.fetchNodesPage = async function() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr>';
    }

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Failed to load clusters.</td></tr>';
            return;
        }
        const projects = await res.json();

        window.nodesPageData = [];
        let nodeIndex = 0;

        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                nodeIndex++;
                const isPrimary = (node.role || '').toLowerCase() === 'primary';
                window.nodesPageData.push({
                    id: node.id,
                    host: node.name,
                    port: '5432',
                    ip: '10.0.20.' + (18 + nodeIndex),
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown',
                    badge: isPrimary ? { text: 'Writable', bg: '#dcfce7', color: '#16a34a' } : { text: 'Readonly', bg: '#f3f4f6', color: '#4b5563' },
                    cluster: `${proj.name} (ID:${proj.id})`,
                    clusterLogo: '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>',
                    clusterColor: '#059669',
                    version: '<div class="cc-spinner cc-spinner-sm" style="opacity:0.6;"></div>',
                    seen: 'in 4 minutes',
                    projId: proj.id
                });
            }
        }

        window.renderNodesPage();

        // Fetch live metrics in background to resolve versions and actual statuses
        for (const proj of projects) {
            if (!proj.nodes || proj.nodes.length === 0) continue;
            try {
                const mr = await apiFetch('/api/projects/' + proj.id + '/metrics');
                if (!mr.ok) continue;
                const nodeMetrics = await mr.json();
                for (const nm of nodeMetrics) {
                    const m = nm.metrics;
                    if (!m) continue;
                    const matchedNode = window.nodesPageData.find(n => n.id === nm.id);
                    if (matchedNode) {
                        if (m.status === 'online') {
                            matchedNode.status = 'Operational';
                            matchedNode.version = m.version ? escapeHTML(m.version) : 'PostgreSQL 16.4';
                        } else if (m.status === 'offline') {
                            matchedNode.status = 'Offline';
                            matchedNode.version = '-';
                        }
                    }
                }
                window.renderNodesPage();
            } catch(e) { /* ignore */ }
        }

    } catch(e) {
        console.error('fetchNodesPage error:', e);
        if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>';
    }
};
"""

# Replace the old block (136676 to 143338)
old_start = js.find('// --- NODES PAGE MANAGEMENT ---')
old_end = js.find("renderNodesPage();\n});", old_start)
if old_end != -1:
    old_end += len("renderNodesPage();\n});")

if old_start != -1 and old_end != -1:
    js = js[:old_start] + NEW_NODES_MODULE + "\n\n" + js[old_end:]
    print("Replaced old nodes block with unified nodes module")

# Remove redundant second fetchNodesPage definition at the bottom if present
idx_fn2 = js.find('window.fetchNodesPage = async function fetchNodesPage()', js.find(NEW_NODES_MODULE) + len(NEW_NODES_MODULE))
if idx_fn2 != -1:
    # find end of that function
    depth = 0
    in_fn = False
    idx_fn2_end = -1
    for pos in range(idx_fn2, min(idx_fn2 + 9000, len(js))):
        if js[pos] == '{':
            depth += 1
            in_fn = True
        elif js[pos] == '}':
            depth -= 1
            if in_fn and depth == 0:
                idx_fn2_end = pos + 1
                break
    if idx_fn2_end != -1:
        js = js[:idx_fn2] + js[idx_fn2_end:]
        print("Removed duplicate fetchNodesPage definition at bottom")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
