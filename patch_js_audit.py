import re
js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

audit_js = """
async function fetchAuditLogs() {
    const res = await apiFetch('/api/audit-logs');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('activity-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">No activities or alarms recorded yet.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(log => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 24px;">${log.timestamp}</td>
                    <td style="padding: 12px 24px;">
                        <span style="background: rgba(139,92,246,0.1); color: #8b5cf6; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;">
                            ${escapeHTML(log.user)}
                        </span>
                    </td>
                    <td style="padding: 12px 24px; font-weight: 500; color: #111827;">${escapeHTML(log.action)}</td>
                    <td style="padding: 12px 24px; color: #4b5563;">${escapeHTML(log.details || "-")}</td>
                </tr>
            `).join('');
        }
    }
}
"""

if "fetchAuditLogs" not in content:
    content += "\n" + audit_js
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added fetchAuditLogs to main.js")
else:
    print("fetchAuditLogs already exists")
