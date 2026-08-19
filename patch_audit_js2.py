import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the existing fetchAuditLogs
old_func_pattern = r'window\.fetchAuditLogs\s*=\s*async\s*function\(\)\s*\{[\s\S]*?\}\s*\}'

new_func = """window.fetchAuditLogs = async function() {
    const res = await apiFetch('/api/audit-logs');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">No activities or alarms recorded yet.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(log => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 24px;">${log.timestamp}</td>
                    <td style="padding: 12px 24px;">
                        <span style="background: rgba(139,92,246,0.1); color: #8b5cf6; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;">
                            ${escapeHTML(log.user || 'System')}
                        </span>
                    </td>
                    <td style="padding: 12px 24px; font-weight: 500; color: #111827;">${escapeHTML(log.action)}</td>
                    <td style="padding: 12px 24px; color: #4b5563;">${escapeHTML(log.details || "-")}</td>
                </tr>
            `).join('');
        }
    }
}"""

content = re.sub(old_func_pattern, new_func, content)

# Make sure activity-view calls fetchAuditLogs
if "showView('activity-view');" in content and "window.fetchAuditLogs();" not in content.split("showView('activity-view');")[1][:200]:
    content = content.replace("showView('activity-view');", "showView('activity-view');\n        window.fetchAuditLogs();")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated window.fetchAuditLogs")
