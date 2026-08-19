with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

AUDIT_JS_FUNCS = """// ---- AUDIT LOG MANAGEMENT ----
window.auditLogsData = [];

window.fetchAuditLogs = async function() {
    const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading audit logs...</span></div></td></tr>';
    }
    try {
        const res = await apiFetch('/api/audit-logs');
        if (res.ok) {
            window.auditLogsData = await res.json();
            window.filterAuditLogs();
        } else {
            if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 40px; color: #ef4444;">Failed to load audit logs.</td></tr>';
        }
    } catch(e) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 40px; color: #ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>';
    }
};

window.filterAuditLogs = function() {
    const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
    if (!tbody) return;

    const input = document.getElementById('audit-search-input');
    const query = input ? input.value.trim().toLowerCase() : '';

    const logs = window.auditLogsData || [];
    let filtered = logs;

    if (query) {
        filtered = logs.filter(log => {
            const action = (log.action || '').toLowerCase();
            const details = (log.details || '').toLowerCase();
            const user = (log.user || log.username || '').toLowerCase();
            const ts = (log.timestamp || '').toLowerCase();
            const hostname = (log.hostname || '127.0.0.1').toLowerCase();
            const cluster = (log.cluster_name || log.project_name || 'N/A').toLowerCase();
            const type = (log.entry_type || (action.includes('log') ? 'authentication' : 'system')).toLowerCase();
            return action.includes(query) || details.includes(query) || user.includes(query) ||
                   ts.includes(query) || hostname.includes(query) || cluster.includes(query) || type.includes(query);
        });
    }

    if (filtered.length === 0) {
        if (query) {
            // Empty state when search filters have no match
            tbody.innerHTML = `
            <tr>
              <td colspan="6" style="text-align: center; padding: 60px 20px; background: white;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block; margin: 0 auto 16px;">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <div style="color: #4b5563; font-size: 0.95rem; margin-bottom: 8px;">No audit log entries match your current filters.</div>
                <a href="#" onclick="event.preventDefault(); window.clearAuditFilters();" style="color: #7c3aed; font-size: 0.85rem; font-weight: 500; text-decoration: none; cursor: pointer;">Clear all filters</a>
              </td>
            </tr>`;
        } else {
            // Empty state when no audit logs exist at all
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 40px; color: #6b7280;">No audit logs recorded yet.</td></tr>`;
        }
        return;
    }

    tbody.innerHTML = filtered.map(log => {
        const action = log.action || '';
        const details = log.details || '';
        const entryType = log.entry_type || (action.toLowerCase().includes('log') ? 'authentication' : 'system');
        const user = log.user || log.username || 'demo@severalnines.com';
        const hostname = log.hostname || '127.0.0.1';
        const cluster = log.cluster_name || log.project_name || 'N/A';
        const activityText = details ? `${action}: ${details}` : action;

        return `
            <tr style="border-bottom: 1px solid #f3f4f6; transition: background 0.15s;" onmouseenter="this.style.background='#fafafa'" onmouseleave="this.style.background='white'">
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #374151; white-space: nowrap;">${escapeHTML(log.timestamp || '')}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; font-weight: 500; color: #111827;">${escapeHTML(activityText)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(entryType)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(user)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(hostname)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(cluster)}</td>
            </tr>
        `;
    }).join('');
};

window.clearAuditFilters = function() {
    const input = document.getElementById('audit-search-input');
    if (input) input.value = '';
    window.filterAuditLogs();
};

window.exportAuditLogsCsv = function() {
    const logs = window.auditLogsData || [];
    if (logs.length === 0) {
        alert("No audit log entries to export.");
        return;
    }

    const headers = ['"id"', '"timestamp"', '"cluster_id"', '"cluster_name"', '"entry_type"', '"username"', '"client_hostname"', '"message"'];
    const rows = [headers.join(',')];

    logs.forEach((log, index) => {
        const id = log.id || (logs.length - index);
        const ts = log.timestamp || '';
        const clusterId = log.project_id || 0;
        const clusterName = log.cluster_name || log.project_name || "";
        const entryType = log.entry_type || (log.action && log.action.toLowerCase().includes('log') ? 'authentication' : 'system');
        const username = log.user || log.username || 'demo@severalnines.com';
        const hostname = log.hostname || '127.0.0.1';
        const message = log.action ? (log.details ? `${log.action}: ${log.details}` : log.action) : 'Logged in.';

        const escapeCsv = (val) => '"' + String(val || '').replace(/"/g, '""') + '"';

        rows.push([
            id,
            escapeCsv(ts),
            clusterId,
            escapeCsv(clusterName),
            escapeCsv(entryType),
            escapeCsv(username),
            escapeCsv(hostname),
            escapeCsv(message)
        ].join(','));
    });

    const csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(rows.join('\\n'));
    const link = document.createElement("a");
    // Generate random 6-character suffix like ClusterControl (e.g. cmon_audit_8duFmV.csv)
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let randStr = '';
    for (let i = 0; i < 6; i++) {
        randStr += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    link.setAttribute("href", csvContent);
    link.setAttribute("download", `cmon_audit_${randStr}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
"""

# Replace window.fetchAuditLogs definition in main.js
idx = js.find('window.fetchAuditLogs = async function')
if idx != -1:
    end_idx = js.find('async function fetchDashboardMetrics()', idx)
    if end_idx != -1:
        js = js[:idx] + AUDIT_JS_FUNCS + "\n\n    " + js[end_idx:]
        print("Replaced fetchAuditLogs with full Audit Log feature suite")
    else:
        print("Could not find end of fetchAuditLogs")
else:
    print("Could not find window.fetchAuditLogs in main.js")

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
