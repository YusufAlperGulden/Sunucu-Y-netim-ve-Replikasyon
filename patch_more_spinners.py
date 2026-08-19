js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Update fetchBackups
old_fb = """async function fetchBackups() {
    const res = await apiFetch('/api/backups');"""
new_fb = """async function fetchBackups() {
    const tbody = document.getElementById('all-backups-tbody');
    if (tbody) tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading backups...</span></div></td></tr>';
    const res = await apiFetch('/api/backups');"""

if old_fb in js:
    js = js.replace(old_fb, new_fb, 1)
    print("Updated fetchBackups spinner")

# Update fetchProjects
old_fp = """async function fetchProjects() {
        try {
            // Clear any old error messages
            document.querySelectorAll('.loading-state').forEach(el => el.remove());
            const response = await apiFetch('/api/projects');"""

new_fp = """async function fetchProjects() {
        try {
            // Clear any old error messages
            document.querySelectorAll('.loading-state').forEach(el => el.remove());
            const cptbody = document.getElementById('cc-projects-tbody');
            if (cptbody && !cptbody.querySelector('tr[data-proj-id]')) {
                cptbody.innerHTML = '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading clusters...</span></div></td></tr>';
            }
            const response = await apiFetch('/api/projects');"""

if old_fp in js:
    js = js.replace(old_fp, new_fp, 1)
    print("Updated fetchProjects spinner")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
