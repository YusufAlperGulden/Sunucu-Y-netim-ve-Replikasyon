js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

ACTIVITY_CENTER_JS = """
// ---- ACTIVITY CENTER TABS ----
window.switchActivityTab = function(tab, btnEl) {
    ['alarms','jobs','audit','watchlists'].forEach(t => {
        const el = document.getElementById('ac-content-' + t);
        const btn = document.getElementById('ac-tab-' + t);
        if (el) el.style.display = 'none';
        if (btn) { btn.style.color = '#6b7280'; btn.style.borderBottomColor = 'transparent'; }
    });
    const content = document.getElementById('ac-content-' + tab);
    if (content) content.style.display = 'block';
    if (btnEl) { btnEl.style.color = 'var(--primary)'; btnEl.style.borderBottomColor = 'var(--primary)'; }
    if (tab === 'audit') { if (typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs(); }
    else if (tab === 'jobs') { fetchActivityJobs(); }
    else if (tab === 'alarms') { fetchActivityAlarms(); }
};

async function fetchActivityAlarms() {
    const tbody = document.getElementById('ac-alarms-tbody');
    if (!tbody) return;
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
    } catch(e) { if(tbody) tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#ef4444;">Hata: ' + escapeHTML(String(e)) + '</td></tr>'; }
}

async function fetchActivityJobs() {
    const tbody = document.getElementById('ac-jobs-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Yukleniyor...</td></tr>';
    try {
        const res = await apiFetch('/api/backups');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Henuz yedek isi yok.</td></tr>'; return; }
        const jobs = await res.json();
        if (!jobs || jobs.length === 0) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Henuz yedek isi yok.</td></tr>'; return; }
        tbody.innerHTML = jobs.map(j => {
            const sc = j.status === 'completed' ? '#10b981' : (j.status === 'failed' ? '#ef4444' : '#f59e0b');
            const sl = j.status === 'completed' ? 'Completed' : (j.status === 'failed' ? 'Failed' : (j.status || 'Paused'));
            return '<tr style="border-bottom: 1px solid #f3f4f6;"><td style="padding: 12px 20px; font-size: 0.85rem;">' + escapeHTML(j.backup_name || j.name || 'Backup Job') + '</td><td style="padding: 12px 20px;"><span style="color:' + sc + ';font-size:0.8rem;display:inline-flex;align-items:center;gap:5px;"><div style=\\"width:6px;height:6px;border-radius:50%;background:' + sc + '\\"></div>' + sl + '</span></td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.cluster_name || j.project_name || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_by || 'system') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_at || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + (j.duration || '0s') + '</td><td style="padding: 12px 20px;"><button style="padding: 4px 10px; font-size: 0.75rem; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; background: white;">...</button></td></tr>';
        }).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Isler yuklenemedi.</td></tr>'; }
}
"""

js += "\n" + ACTIVITY_CENTER_JS

# Update handleRouting to set audit tab as default
js = js.replace(
    "} else if (hash === 'activity-view' || hash === 'audit-logs-view') {\n            if (typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs();\n            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();",
    "} else if (hash === 'activity-view' || hash === 'audit-logs-view') {\n            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();\n            setTimeout(() => { const auditBtn = document.getElementById('ac-tab-audit'); if(auditBtn && typeof window.switchActivityTab === 'function') window.switchActivityTab('audit', auditBtn); else if(typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs(); }, 50);"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Done - added switchActivityTab and fetch functions")
