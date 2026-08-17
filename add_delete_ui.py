# -*- coding: utf-8 -*-
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

submit_btn = '<button type="submit" class="btn-primary w-100" id="btn-submit-edit-node">Kaydet ve Yeniden Başlat</button>'
new_btns = '''<div style="display: flex; gap: 10px;">
                        <button type="submit" class="btn-primary" style="flex: 1;" id="btn-submit-edit-node">Kaydet ve Yeniden Başlat</button>
                        <button type="button" class="btn-primary" style="background: var(--danger); color: white;" id="btn-delete-node">Sunucuyu Sil</button>
                    </div>'''

text = text.replace(submit_btn, new_btns)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

delete_logic = '''
    document.getElementById('btn-delete-node').addEventListener('click', async () => {
        const nodeId = document.getElementById('edit-node-id').value;
        if (!confirm('Bu sunucuyu silmek istediğinize emin misiniz?')) return;
        
        try {
            const res = await apiFetch(/api/nodes/, { method: 'DELETE' });
            if (res.ok) {
                modalEditNode.style.display = 'none';
                fetchProjects();
            } else {
                alert('Sunucu silinemedi.');
            }
        } catch (e) {
            alert('Sunucu silinemedi.');
        }
    });
'''

if 'btn-delete-node' not in js_text:
    # Append to the end of main.js
    js_text += delete_logic
    with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
        f.write(js_text)

print('Added delete UI')
