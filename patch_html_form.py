import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Type select
old_type_select = """<select style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">
                        <option value="">Select report type [PLACEHOLDER]</option>
                    </select>"""
new_type_select = """<select id="report-type-select" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">
                        <option value="">Select report type</option>
                        <option value="System Report">System Report</option>
                        <option value="Database Availability Report">Database Availability Report</option>
                        <option value="Backup Report">Backup Report</option>
                        <option value="Upgrade Report">Upgrade Report</option>
                        <option value="Schema Change Report">Schema Change Report</option>
                        <option value="Database Growth Report">Database Growth Report</option>
                    </select>"""
content = content.replace(old_type_select, new_type_select)

# Add ID to data range input
old_range_input = '<input type="number" value="7" style="flex: 1; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">'
new_range_input = '<input type="number" id="report-data-range" value="7" min="1" max="365" style="flex: 1; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">'
content = content.replace(old_range_input, new_range_input)

# Add ID to recipients input
old_recipients = '<input type="text" placeholder="Enter email recipients [PLACEHOLDER]" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">'
new_recipients = '<input type="text" id="report-recipients" placeholder="yusufalper@gmail.com, admin@example.com" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">'
content = content.replace(old_recipients, new_recipients)

# Modify Create button
old_create_btn = '<button class="btn-primary" style="background: #3a1c94; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;" onclick="document.getElementById(\'modal-create-report\').style.display=\'none\'">Create <span style="font-size: 0.65rem; color: #ef4444; font-weight: bold; margin-left: 5px;">[PLACEHOLDER]</span></button>'
new_create_btn = '<button id="btn-submit-report" class="btn-primary" style="background: #3a1c94; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">Create</button>'
content = content.replace(old_create_btn, new_create_btn)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML form for reports")

