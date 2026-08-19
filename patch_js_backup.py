import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

render_backups = """
async function fetchBackups() {
    const res = await apiFetch('/api/backups');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('all-backups-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 20px; color: #6b7280;">No backups found.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(b => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 0;">${escapeHTML(b.cluster_name)}</td>
                    <td style="padding: 12px 0;">
                        <span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:500; 
                        background: ${b.status === 'COMPLETED' ? 'rgba(16,185,129,0.1)' : (b.status === 'IN_PROGRESS' ? 'rgba(59,130,246,0.1)' : 'rgba(239,68,68,0.1)')}; 
                        color: ${b.status === 'COMPLETED' ? '#10b981' : (b.status === 'IN_PROGRESS' ? '#3b82f6' : '#ef4444')};">
                        ${b.status}</span>
                    </td>
                    <td style="padding: 12px 0;">${b.size_mb ? b.size_mb + ' MB' : '-'}</td>
                    <td style="padding: 12px 0;">${escapeHTML(b.backup_type)}</td>
                    <td style="padding: 12px 0;">${b.created_at}</td>
                    <td style="padding: 12px 0;">${b.completed_at || '-'}</td>
                    <td style="padding: 12px 0;">
                        <button style="background:transparent; border:1px solid var(--border); border-radius:4px; padding:4px 8px; font-size:0.8rem; cursor:pointer;">Restore</button>
                    </td>
                </tr>
            `).join('');
        }
    }
}

async function fetchSchedules() {
    const res = await apiFetch('/api/backups/schedules');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('schedules-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 20px; color: #6b7280;">No schedules found.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(s => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 0;">${escapeHTML(s.schedule_expression)}</td>
                    <td style="padding: 12px 0;">${escapeHTML(s.backup_type)}</td>
                    <td style="padding: 12px 0;">${escapeHTML(s.cluster_name)}</td>
                    <td style="padding: 12px 0;">${s.retention_days} days</td>
                    <td style="padding: 12px 0;">
                        <button style="background:transparent; border:1px solid var(--border); border-radius:4px; padding:4px 8px; font-size:0.8rem; cursor:pointer;">Edit</button>
                    </td>
                </tr>
            `).join('');
        }
    }
}

function renderBackups() {
    fetchBackups();
    fetchSchedules();
}
"""

content = re.sub(r'function renderBackups\(\)\s*\{[\s\S]*?\}', render_backups, content)

submit_backup = """
document.getElementById('form-create-backup')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const pid = document.getElementById('backup-cluster-select').value;
    const btype = document.getElementById('backup-type-select').value;
    if(!pid) { alert("Please select a cluster"); return; }
    
    const btn = document.getElementById('btn-submit-backup');
    btn.innerText = "Creating...";
    btn.disabled = true;
    
    try {
        const res = await apiFetch('/api/backups', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ project_id: parseInt(pid), backup_type: btype })
        });
        const data = await res.json();
        if(res.ok && data.success) {
            document.getElementById('modal-create-backup').style.display = 'none';
            fetchBackups();
            alert("Backup started successfully!");
        } else {
            alert(data.message || "Failed to create backup");
        }
    } catch(err) {
        alert("Error: " + err);
    }
    btn.innerText = "Create";
    btn.disabled = false;
});
"""

if "fetchBackups" in content and "form-create-backup" not in content:
    content += "\n" + submit_backup
    
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.js with backup logic")
