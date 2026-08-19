with open("fastapi_app/static/main.js", "r", encoding="utf-8") as f:
    content = f.read()

old_fetch = """        try {
            const res = await apiFetch(`/api/nodes/${nodeId}/metrics`);
            if(!res.ok) return;
            const data = await res.json();"""

new_fetch = """        try {
            const res = await apiFetch(`/api/nodes/${nodeId}/metrics`);
            if(!res.ok) {
                document.getElementById('modal-metric-status').className = 'status-badge status-offline';
                document.getElementById('modal-metric-status').innerText = 'Hata (502)';
                return;
            }
            const data = await res.json();"""

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch)
    with open("fastapi_app/static/main.js", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched main.js")
else:
    print("Not found main.js")
