import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Add User Modal
modal_html = """
    <!-- Add User Modal -->
    <div class="modal-overlay" id="modal-add-user" style="display: none;">
        <div class="modal glass-panel">
            <div class="modal-header">
                <h3>Add New User</h3>
                <button class="btn-close" onclick="document.getElementById('modal-add-user').style.display='none'">&#10005;</button>
            </div>
            <div class="modal-body">
                <form id="form-add-user">
                    <div class="input-group">
                        <label>Username</label>
                        <input type="text" id="new-user-username" required style="width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); border-radius: 8px; color: white;">
                    </div>
                    <div class="input-group">
                        <label>Password</label>
                        <input type="password" id="new-user-password" required style="width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); border-radius: 8px; color: white;">
                    </div>
                    <div class="input-group">
                        <label>Role</label>
                        <select id="new-user-role" required style="width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); border-radius: 8px; color: white;">
                            <option value="viewer" style="color: black;">Viewer</option>
                            <option value="admin" style="color: black;">Admin</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary" style="width: 100%; margin-top: 10px;" id="btn-submit-user">Add User</button>
                </form>
            </div>
        </div>
    </div>
"""

old_btn = '<button class="btn-primary" style="background: var(--primary); color: white;">Add user</button>'
new_btn = '<button class="btn-primary" style="background: var(--primary); color: white;" onclick="document.getElementById(\'modal-add-user\').style.display=\'flex\'">Add user</button>'

if "modal-add-user" not in content:
    content = content.replace("<!-- Modals -->", "<!-- Modals -->\n" + modal_html)
    content = content.replace(old_btn, new_btn)

# Replace table body
old_tbody = """<tbody>
                            <tr>
                                <td>
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:32px; height:32px; border-radius:50%; background:var(--primary); display:flex; align-items:center; justify-content:center; color:white; font-weight:600;">
                                            A
                                        </div>
                                        <div>
                                            <div style="font-weight:500;">admin@example.com</div>
                                            <div style="font-size:0.8rem; color:var(--text-secondary);">Super Admin</div>
                                        </div>
                                    </div>
                                </td>
                                <td><span class="status-badge status-online">Active</span></td>
                                <td>2024-03-01</td>
                                <td>
                                    <button class="btn-icon">✎</button>
                                </td>
                            </tr>
                        </tbody>"""

new_tbody = """<tbody id="users-tbody">
                            <!-- Populated dynamically -->
                        </tbody>"""

content = content.replace(old_tbody, new_tbody)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML with User modal and tbody")
