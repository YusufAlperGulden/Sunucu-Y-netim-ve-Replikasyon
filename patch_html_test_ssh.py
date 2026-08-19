import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_button_group = """                    <div style="display: flex; gap: 10px;">
                        <button type="submit" class="btn-primary" style="flex: 1;" id="btn-submit-edit-node">Kaydet ve Yeniden Başlat</button>
                        <button type="button" class="btn-primary" style="background: var(--danger); color: white;" id="btn-delete-node">Sunucuyu Sil</button>
                    </div>"""
new_button_group = """                    <div style="display: flex; gap: 10px;">
                        <button type="button" class="btn-secondary" style="flex: 1; border: 1px solid var(--primary); color: var(--primary);" onclick="testSshConnection()">Test SSH</button>
                        <button type="submit" class="btn-primary" style="flex: 1;" id="btn-submit-edit-node">Kaydet ve Yeniden Başlat</button>
                        <button type="button" class="btn-primary" style="background: var(--danger); color: white;" id="btn-delete-node">Sunucuyu Sil</button>
                    </div>"""
content = content.replace(old_button_group, new_button_group)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added Test SSH button")
