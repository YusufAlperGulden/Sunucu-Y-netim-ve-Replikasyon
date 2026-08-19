import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

test_ssh_js = """
async function testSshConnection() {
    if (!currentNodeIdToEdit) {
        alert("Lütfen önce kaydedin.");
        return;
    }
    const btn = document.querySelector('button[onclick="testSshConnection()"]');
    const oldText = btn.innerText;
    btn.innerText = "Testing...";
    btn.disabled = true;
    
    try {
        const res = await apiFetch(`/api/nodes/${currentNodeIdToEdit}/test-ssh`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            alert("✅ " + data.message);
        } else {
            alert("❌ " + data.message);
        }
    } catch (err) {
        alert("Bağlantı hatası: " + err);
    }
    
    btn.innerText = oldText;
    btn.disabled = false;
}
"""

if "function testSshConnection" not in content:
    content += "\n" + test_ssh_js
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added testSshConnection logic")
else:
    print("Already exists")
