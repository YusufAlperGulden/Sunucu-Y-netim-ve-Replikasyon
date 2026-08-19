import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

users_code = """
async function fetchUsers() {
    const res = await apiFetch('/api/users');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('users-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">No users found.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(u => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 0;">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div style="width:32px; height:32px; border-radius:50%; background:var(--primary); display:flex; align-items:center; justify-content:center; color:white; font-weight:600;">
                                ${u.username.substring(0,1).toUpperCase()}
                            </div>
                            <div>
                                <div style="font-weight:500;">${escapeHTML(u.username)}</div>
                                <div style="font-size:0.8rem; color:var(--text-secondary);">User ID: ${u.id}</div>
                            </div>
                        </div>
                    </td>
                    <td style="padding: 12px 0;">
                        <span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:500; 
                        background: ${u.role === 'admin' ? 'rgba(139,92,246,0.1)' : 'rgba(16,185,129,0.1)'}; 
                        color: ${u.role === 'admin' ? '#8b5cf6' : '#10b981'};">
                        ${u.role.toUpperCase()}</span>
                    </td>
                    <td style="padding: 12px 0;">${u.created_at}</td>
                    <td style="padding: 12px 0;">
                        <button style="background:transparent; border:1px solid var(--border); border-radius:4px; padding:4px 8px; font-size:0.8rem; cursor:pointer;" onclick="deleteUser(${u.id})">Delete</button>
                    </td>
                </tr>
            `).join('');
        }
    }
}

async function deleteUser(id) {
    if(!confirm("Are you sure you want to delete this user?")) return;
    try {
        const res = await apiFetch(`/api/users/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if(res.ok && data.success) {
            fetchUsers();
        } else {
            alert(data.message || "Failed to delete user");
        }
    } catch(err) { alert(err); }
}
"""

content = re.sub(r'function fetchUsers\(\)\s*\{[\s\S]*?\}', users_code, content)

submit_user = """
document.getElementById('form-add-user')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const un = document.getElementById('new-user-username').value;
    const pw = document.getElementById('new-user-password').value;
    const rl = document.getElementById('new-user-role').value;
    
    const btn = document.getElementById('btn-submit-user');
    btn.innerText = "Adding...";
    btn.disabled = true;
    
    try {
        const res = await apiFetch('/api/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ username: un, password: pw, role: rl })
        });
        const data = await res.json();
        if(res.ok && data.success) {
            document.getElementById('modal-add-user').style.display = 'none';
            fetchUsers();
            e.target.reset();
        } else {
            alert(data.message || "Failed to add user");
        }
    } catch(err) {
        alert("Error: " + err);
    }
    btn.innerText = "Add User";
    btn.disabled = false;
});
"""

if "fetchUsers();" in content and "form-add-user" not in content:
    content += "\n" + submit_user

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.js with User logic")
