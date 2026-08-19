import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Create Backup Modal
modal_html = """
    <!-- Create Backup Modal -->
    <div class="modal-overlay" id="modal-create-backup" style="display: none;">
        <div class="modal glass-panel">
            <div class="modal-header">
                <h3>Create New Backup</h3>
                <button class="btn-close" onclick="document.getElementById('modal-create-backup').style.display='none'">&#10005;</button>
            </div>
            <div class="modal-body">
                <form id="form-create-backup">
                    <div class="input-group">
                        <label>Cluster</label>
                        <select id="backup-cluster-select" required style="width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); border-radius: 8px; color: white;">
                            <!-- Populated dynamically -->
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Backup Type</label>
                        <select id="backup-type-select" required style="width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); border-radius: 8px; color: white;">
                            <option value="FULL" style="color: black;">Full Backup</option>
                            <option value="INCR" style="color: black;">Incremental Backup</option>
                            <option value="DIFF" style="color: black;">Differential Backup</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary" style="width: 100%; margin-top: 10px;" id="btn-submit-backup">Create</button>
                </form>
            </div>
        </div>
    </div>
"""

# Modify the Backup button to open modal
old_btn = '<button class="btn-primary" style="background: var(--primary); color: white;">Create backup</button>'
new_btn = '<button class="btn-primary" style="background: var(--primary); color: white;" onclick="document.getElementById(\'modal-create-backup\').style.display=\'flex\'">Create backup</button>'

if "modal-create-backup" not in content:
    content = content.replace("<!-- Modals -->", "<!-- Modals -->\n" + modal_html)
    content = content.replace(old_btn, new_btn)

# Add polling interval in JS for backups
js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# I will add a setInterval to fetchBackups every 5 seconds if we are on the backups page
polling_code = """
setInterval(() => {
    if (document.getElementById('backups-view').style.display === 'block') {
        fetchBackups();
    }
}, 5000);
"""
if "fetchBackups();" in js_content and "setInterval" not in js_content.split("fetchBackups")[1]:
    js_content += "\n" + polling_code
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML with Backup modal and JS polling")
