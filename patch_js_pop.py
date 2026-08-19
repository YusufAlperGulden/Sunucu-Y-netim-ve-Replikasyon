import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

pop_code = """
document.querySelector('button[onclick="document.getElementById(\\'modal-create-backup\\').style.display=\\'flex\\'"]')?.addEventListener('click', async () => {
    const res = await apiFetch('/api/projects');
    if (res.ok) {
        const projs = await res.json();
        const sel = document.getElementById('backup-cluster-select');
        sel.innerHTML = '<option value="">Select a cluster...</option>' + 
            projs.map(p => `<option value="${p.id}" style="color:black;">${p.name}</option>`).join('');
    }
});
"""

if "backup-cluster-select" in content and "apiFetch('/api/projects')" not in pop_code: # wait, it's a new code block
    pass

if "Select a cluster..." not in content.split("modal-create-backup")[-1]:
    content += "\n" + pop_code
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added cluster select population")
