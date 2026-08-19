with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure nodesPageData is declared globally
if 'window.nodesPageData' not in js:
    js = 'window.nodesPageData = [];\nvar nodesPageData = window.nodesPageData;\n' + js

# 1. Patch fetchNodesPage to populate nodesPageData and call renderNodesPage with proper spinners
NEW_FETCH_NODES = """window.fetchNodesPage = async function fetchNodesPage() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr>';

    // Reset stats to loading state
    ['stat-operational','stat-failed','stat-offline','stat-shutdown','stat-recovering','stat-unknown','stat-all'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = '-';
    });

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Failed to load clusters.</td></tr>';
            return;
        }
        const projects = await res.json();

        // Build nodesPageData
        window.nodesPageData = [];
        nodesPageData = window.nodesPageData;

        let nodeIndex = 0;
        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                nodeIndex++;
                const isPrimary = (node.role || '').toLowerCase() === 'primary';
                nodesPageData.push({
                    id: node.id,
                    host: node.name,
                    port: '5432',
                    ip: '10.0.20.' + (18 + nodeIndex),
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown',
                    badge: isPrimary ? { text: 'Writable', bg: '#dcfce7', color: '#16a34a' } : { text: 'Readonly', bg: '#f3f4f6', color: '#4b5563' },
                    cluster: `${proj.name} (ID:${proj.id})`,
                    clusterLogo: '<polyline points="9 18 15 12 9 6"></polyline>',
                    clusterColor: '#059669',
                    version: '<div class="cc-spinner cc-spinner-sm" style="opacity:0.6;"></div>',
                    seen: 'just now',
                    nodeObj: node,
                    projObj: proj
                });
            }
        }

        // Update stat counters
        const statOp = document.getElementById('stat-operational');
        const statAll = document.getElementById('stat-all');
        if (statOp) statOp.innerText = nodesPageData.length;
        if (statAll) statAll.innerText = nodesPageData.length;
        ['stat-failed','stat-offline','stat-shutdown','stat-recovering','stat-unknown'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = '0';
        });

        if (nodesPageData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:40px;color:#9ca3af;">No nodes found. Deploy a cluster first.</td></tr>';
            return;
        }

        // Render immediately
        if (typeof renderNodesPage === 'function') {
            renderNodesPage();
        }

        // Fetch metrics in background to populate real versions and live status
        for (const proj of projects) {
            if (!proj.nodes || proj.nodes.length === 0) continue;
            try {
                const mr = await apiFetch('/api/projects/' + proj.id + '/metrics');
                if (!mr.ok) continue;
                const nodeMetrics = await mr.json();
                for (const nm of nodeMetrics) {
                    const m = nm.metrics;
                    if (!m) continue;
                    const matchedNode = nodesPageData.find(n => n.id === nm.id);
                    if (matchedNode) {
                        if (m.status === 'online') {
                            matchedNode.status = 'Operational';
                            matchedNode.version = m.version ? escapeHTML(m.version) : 'PostgreSQL';
                        } else if (m.status === 'offline') {
                            matchedNode.status = 'Offline';
                            matchedNode.version = '-';
                        }
                    }
                }
                // Re-render with updated versions and status
                if (typeof renderNodesPage === 'function') {
                    renderNodesPage();
                }
            } catch(e) { /* ignore metric error */ }
        }

    } catch(e) {
        console.error('fetchNodesPage error:', e);
        if(tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>';
    }
};"""

# Replace old fetchNodesPage
idx1 = js.find('window.fetchNodesPage = async function')
if idx1 != -1:
    depth = 0
    in_fn = False
    idx2 = -1
    for pos in range(idx1, min(idx1 + 9000, len(js))):
        if js[pos] == '{':
            depth += 1
            in_fn = True
        elif js[pos] == '}':
            depth -= 1
            if in_fn and depth == 0:
                idx2 = pos + 1
                break
    if idx2 != -1:
        js = js[:idx1] + NEW_FETCH_NODES + js[idx2:]
        print("Patched fetchNodesPage")

# 2. Patch fetchAuditLogs to show spinner on start
idx = js.find('window.fetchAuditLogs = async function')
if idx != -1:
    end_idx = js.find('async function fetchDashboardMetrics()', idx)
    if end_idx != -1:
        NEW_AUDIT_LOGS = """window.fetchAuditLogs = async function() {
    const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="4"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading audit logs...</span></div></td></tr>';
    }
    const res = await apiFetch('/api/audit-logs');
    if (res.ok) {
        const data = await res.json();
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 40px; color: #6b7280;">No activities or alarms recorded yet.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(log => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 24px;">${escapeHTML(log.timestamp || '')}</td>
                    <td style="padding: 12px 24px;">
                        <span style="background: rgba(139,92,246,0.1); color: #8b5cf6; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;">
                            ${escapeHTML(log.user || 'System')}
                        </span>
                    </td>
                    <td style="padding: 12px 24px; font-weight: 500; color: #111827;">${escapeHTML(log.action || '')}</td>
                    <td style="padding: 12px 24px; color: #4b5563;">${escapeHTML(log.details || "-")}</td>
                </tr>
            `).join('');
        }
    }
};\n\n    """
        js = js[:idx] + NEW_AUDIT_LOGS + js[end_idx:]
        print("Patched fetchAuditLogs")

# 3. Patch fetchActivityAlarms and fetchActivityJobs
NEW_ACTIVITY_FUNCS = """async function fetchActivityAlarms() {
    const tbody = document.getElementById('ac-alarms-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading alarms...</span></div></td></tr>';
    try {
        const res = await apiFetch('/api/audit-logs');
        if (!res.ok) return;
        const logs = await res.json();
        const alarms = logs.filter(l => l.action && (l.action.toLowerCase().includes('fail') || l.action.toLowerCase().includes('error') || l.action.toLowerCase().includes('alarm')));
        if (alarms.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 60px;"><svg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"48\\" height=\\"48\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"#d1d5db\\" stroke-width=\\"1.5\\" style=\\"display:block;margin:0 auto 16px;\\"><path d=\\"M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0\\"></path></svg><p style=\\"color:#9ca3af;font-size:0.9rem;\\">You haven\\'t received alarms yet. When you do, it\\'ll show up here.</p></td></tr>';
            return;
        }
        tbody.innerHTML = alarms.map(a => '<tr style="border-bottom: 1px solid #f3f4f6;"><td style="padding: 12px 20px; font-size: 0.85rem;">' + escapeHTML(a.action) + '</td><td style="padding: 12px 20px;"><span style="color: #ef4444; font-size: 0.8rem; font-weight: 600;">WARNING</span></td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">System</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">-</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">-</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(a.timestamp || '-') + '</td><td style="padding: 12px 20px;"><button style="padding: 4px 10px; font-size: 0.75rem; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; background: white;">...</button></td></tr>').join('');
    } catch(e) { if(tbody) tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>'; }
}

async function fetchActivityJobs() {
    const tbody = document.getElementById('ac-jobs-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading jobs...</span></div></td></tr>';
    try {
        const res = await apiFetch('/api/backups');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">No backup jobs found.</td></tr>'; return; }
        const jobs = await res.json();
        if (!jobs || jobs.length === 0) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">No backup jobs found.</td></tr>'; return; }
        tbody.innerHTML = jobs.map(j => {
            const sc = j.status === 'completed' ? '#10b981' : (j.status === 'failed' ? '#ef4444' : '#f59e0b');
            const sl = j.status === 'completed' ? 'Completed' : (j.status === 'failed' ? 'Failed' : (j.status || 'Paused'));
            return '<tr style="border-bottom: 1px solid #f3f4f6;"><td style="padding: 12px 20px; font-size: 0.85rem;">' + escapeHTML(j.backup_name || j.name || 'Backup Job') + '</td><td style="padding: 12px 20px;"><span style="color:' + sc + ';font-size:0.8rem;display:inline-flex;align-items:center;gap:5px;"><div style=\\"width:6px;height:6px;border-radius:50%;background:' + sc + '\\"></div>' + sl + '</span></td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.cluster_name || j.project_name || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_by || 'system') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_at || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + (j.duration || '0s') + '</td><td style="padding: 12px 20px;"><button style="padding: 4px 10px; font-size: 0.75rem; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; background: white;">...</button></td></tr>';
        }).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Failed to load jobs.</td></tr>'; }
}"""

idx_act = js.find('async function fetchActivityAlarms()')
if idx_act != -1:
    js = js[:idx_act] + NEW_ACTIVITY_FUNCS
    print("Patched fetchActivityAlarms & fetchActivityJobs")

# 4. Patch fetchRecentAlarms
idx_ra = js.find('async function fetchRecentAlarms()')
if idx_ra != -1:
    idx_ra_end = js.find('async function fetchProfile()', idx_ra)
    if idx_ra_end != -1:
        NEW_RA = """async function fetchRecentAlarms() {
    const container = document.getElementById('recent-alarms-container');
    if (!container) return;
    
    try {
        const res = await apiFetch('/api/audit-logs');
        if (res.ok) {
            const data = await res.json();
            const alarms = data.filter(log => (log.action && (log.action.toLowerCase().includes('failed') || log.action.toLowerCase().includes('error') || log.action.toLowerCase().includes('alarm')))).slice(0, 5);
            
            if (alarms.length === 0) {
                container.innerHTML = `
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color: var(--text-muted); font-size: 0.95rem; padding: 24px; text-align: center;">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 12px; color: #d1d5db;">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <div style="font-weight: 500; color: var(--text-main); margin-bottom: 4px;">No active alarms</div>
                    <div style="font-size: 0.8rem;">All systems and database nodes are operating normally.</div>
                </div>`;
            } else {
                container.innerHTML = alarms.map(alarm => `
                    <div style="display:flex; align-items:center; gap: 12px; padding: 12px; border-bottom: 1px solid var(--border); font-size: 0.85rem;">
                        <span style="color: #ef4444; font-weight: bold; font-size: 1rem;">&#9888;</span>
                        <div style="flex:1;">
                            <div style="font-weight: 600; color: var(--text-main);">${escapeHTML(alarm.action)}</div>
                            <div style="color: var(--text-muted); font-size: 0.75rem;">${escapeHTML(alarm.details || '')}</div>
                        </div>
                        <span style="color: var(--text-muted); font-size: 0.75rem; white-space: nowrap;">${escapeHTML(alarm.timestamp || '')}</span>
                    </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error('fetchRecentAlarms error:', e);
    }
}\n\n"""
        js = js[:idx_ra] + NEW_RA + js[idx_ra_end:]
        print("Patched fetchRecentAlarms")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Finished patching main.js")
