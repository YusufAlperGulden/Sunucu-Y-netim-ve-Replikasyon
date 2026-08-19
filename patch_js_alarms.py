import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

alarms_js = """
async function fetchRecentAlarms() {
    const container = document.getElementById('recent-alarms-container');
    if (!container) return;
    
    try {
        const res = await apiFetch('/api/audit-logs');
        if (res.ok) {
            const data = await res.json();
            // Filter logs that look like alarms/errors
            const alarms = data.filter(log => log.action.toLowerCase().includes('failed') || log.action.toLowerCase().includes('error') || log.action.toLowerCase().includes('alarm')).slice(0, 5);
            
            if (alarms.length === 0) {
                container.innerHTML = `
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color: var(--text-muted); font-size: 0.95rem; padding: 24px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                    No alarms
                </div>`;
            } else {
                container.innerHTML = alarms.map(alarm => `
                <div style="padding: 12px; border-bottom: 1px solid var(--border); display: flex; flex-direction: column; gap: 4px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #ef4444; font-size: 0.85rem;">${escapeHTML(alarm.action)}</span>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">${escapeHTML(alarm.timestamp)}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">${escapeHTML(alarm.details)}</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">Cluster ID: ${alarm.project_id}</div>
                </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error("Failed to fetch alarms", e);
    }
}
"""

if "fetchRecentAlarms" not in content:
    content += "\n" + alarms_js
    
    # inject into showProjectsView
    if "fetchProjects();" in content:
        content = content.replace("fetchProjects();", "fetchProjects();\n        fetchRecentAlarms();")
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added fetchRecentAlarms")
else:
    print("fetchRecentAlarms already exists")
