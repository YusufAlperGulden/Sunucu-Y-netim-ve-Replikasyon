import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

ssh_html_add = """
                    <div style="margin-top: 24px; margin-bottom: 16px; font-weight: 500; font-size: 1.1rem; color: #111827;">SSH Configuration (Optional)</div>
                    <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                        <div class="input-group" style="flex: 2;">
                            <label>SSH Host (IP)</label>
                            <input type="text" id="node-ssh-host" placeholder="e.g. 192.168.1.100">
                        </div>
                        <div class="input-group" style="flex: 1;">
                            <label>Port</label>
                            <input type="number" id="node-ssh-port" value="22">
                        </div>
                    </div>
                    <div class="input-group" style="margin-bottom: 16px;">
                        <label>SSH Username</label>
                        <input type="text" id="node-ssh-user" value="root">
                    </div>
                    <div class="input-group">
                        <label>SSH Password or PEM Key</label>
                        <textarea id="node-ssh-cred" placeholder="Password or Paste PEM Key here" style="width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 8px; font-family: monospace; min-height: 80px; outline: none;"></textarea>
                    </div>
"""

# Find the end of the input group for PostgreSQL Connection URL in add node
pattern_add = r'(<input type="text" id="node-url" required placeholder="postgresql://user:password@host:port/dbname">\n\s*</div>)'
content = re.sub(pattern_add, r'\g<1>\n' + ssh_html_add, content, count=1)


ssh_html_edit = """
                    <div style="margin-top: 24px; margin-bottom: 16px; font-weight: 500; font-size: 1.1rem; color: #111827;">SSH Configuration (Optional)</div>
                    <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                        <div class="input-group" style="flex: 2;">
                            <label>SSH Host (IP)</label>
                            <input type="text" id="edit-node-ssh-host" placeholder="e.g. 192.168.1.100">
                        </div>
                        <div class="input-group" style="flex: 1;">
                            <label>Port</label>
                            <input type="number" id="edit-node-ssh-port" value="22">
                        </div>
                    </div>
                    <div class="input-group" style="margin-bottom: 16px;">
                        <label>SSH Username</label>
                        <input type="text" id="edit-node-ssh-user" value="root">
                    </div>
                    <div class="input-group">
                        <label>SSH Password or PEM Key</label>
                        <textarea id="edit-node-ssh-cred" placeholder="Leave blank to keep existing credential" style="width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 8px; font-family: monospace; min-height: 80px; outline: none;"></textarea>
                    </div>
"""

# Find the end of the input group for PostgreSQL Connection URL in edit node
pattern_edit = r'(<input type="text" id="edit-node-url" required placeholder="postgresql://user:password@host:port/dbname">\n\s*</div>)'
content = re.sub(pattern_edit, r'\g<1>\n' + ssh_html_edit, content, count=1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML modals with SSH fields")

