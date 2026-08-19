import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Node
old_add_payload = """        const payload = {
            project_id: parseInt(currentProjectId),
            name: document.getElementById('node-name').value,
            url: document.getElementById('node-url').value,
            is_primary: document.getElementById('node-role').value === 'Primary'
        };"""
new_add_payload = """        const payload = {
            project_id: parseInt(currentProjectId),
            name: document.getElementById('node-name').value,
            url: document.getElementById('node-url').value,
            is_primary: document.getElementById('node-role').value === 'Primary',
            ssh_host: document.getElementById('node-ssh-host').value || null,
            ssh_port: parseInt(document.getElementById('node-ssh-port').value) || 22,
            ssh_username: document.getElementById('node-ssh-user').value || 'root',
            ssh_credential: document.getElementById('node-ssh-cred').value || null
        };"""
content = content.replace(old_add_payload, new_add_payload)

# Pre-fill Edit Node Modal
old_edit_fill = """                document.getElementById('edit-node-name').value = data.name;
                document.getElementById('edit-node-url').value = data.url;
                document.getElementById('edit-node-role').value = data.is_primary ? 'Primary' : 'Standby';"""
new_edit_fill = """                document.getElementById('edit-node-name').value = data.name;
                document.getElementById('edit-node-url').value = data.url;
                document.getElementById('edit-node-role').value = data.is_primary ? 'Primary' : 'Standby';
                document.getElementById('edit-node-ssh-host').value = data.ssh_host || '';
                document.getElementById('edit-node-ssh-port').value = data.ssh_port || 22;
                document.getElementById('edit-node-ssh-user').value = data.ssh_username || 'root';
                document.getElementById('edit-node-ssh-cred').value = '';
                document.getElementById('edit-node-ssh-cred').placeholder = data.has_ssh_credential ? 'Leave blank to keep existing credential' : 'Password or Paste PEM Key here';"""
content = content.replace(old_edit_fill, new_edit_fill)

# Update Node Submit
old_edit_payload = """        const payload = {
            url: document.getElementById('edit-node-url').value,
            name: document.getElementById('edit-node-name').value,
            is_primary: document.getElementById('edit-node-role').value === 'Primary'
        };"""
new_edit_payload = """        const payload = {
            url: document.getElementById('edit-node-url').value,
            name: document.getElementById('edit-node-name').value,
            is_primary: document.getElementById('edit-node-role').value === 'Primary',
            ssh_host: document.getElementById('edit-node-ssh-host').value || null,
            ssh_port: parseInt(document.getElementById('edit-node-ssh-port').value) || 22,
            ssh_username: document.getElementById('edit-node-ssh-user').value || 'root'
        };
        const cred = document.getElementById('edit-node-ssh-cred').value;
        if (cred !== "") {
            payload.ssh_credential = cred;
        }"""
content = content.replace(old_edit_payload, new_edit_payload)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated JS for SSH fields")

