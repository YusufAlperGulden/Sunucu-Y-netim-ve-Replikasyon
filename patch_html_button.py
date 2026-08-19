import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the main button
old_button = '<button id="btn-create-report-action" class="btn-primary" style="display: flex; align-items: center; gap: 8px; border-radius: 20px; padding: 8px 16px;"'
new_button = '<button id="btn-create-report-action" class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px; border-radius: 20px; padding: 8px 16px; border: none; cursor: pointer;"'
content = content.replace(old_button, new_button)

# Fix the modal button
old_modal_button = '<button class="btn-primary" onclick="document.getElementById(\'modal-create-report\').style.display=\'none\'">Create'
new_modal_button = '<button class="btn-primary" style="background: #3a1c94; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;" onclick="document.getElementById(\'modal-create-report\').style.display=\'none\'">Create'
content = content.replace(old_modal_button, new_modal_button)

# Add an ID to the cluster select so we can populate it
old_select = '<select style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">\n                        <option value="">Select cluster [PLACEHOLDER]</option>\n                    </select>'
new_select = '<select id="report-cluster-select" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">\n                        <option value="">Select cluster</option>\n                    </select>'
content = content.replace(old_select, new_select)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed button colors and select ID")

