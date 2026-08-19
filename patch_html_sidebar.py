import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace CmonDB and Controller with display:none, and add onclick for the rest.
# Actually I'll rewrite the entire Left sidebar.

old_sidebar = r'<!-- Left sidebar settings categories -->.*?</div>'

new_sidebar = """<!-- Left sidebar settings categories -->
        <div style="width: 200px; display: flex; flex-direction: column; gap: 15px;">
            <div class="settings-sidebar-item" data-category="Backup" style="color: var(--primary); font-size: 0.85rem; font-weight: 500; cursor: pointer; border-left: 3px solid var(--primary); padding-left: 10px;">Backup</div>
            <div class="settings-sidebar-item" data-category="Cluster" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Cluster</div>
            <div class="settings-sidebar-item" data-category="CmonDB" style="display: none;">CmonDB</div>
            <div class="settings-sidebar-item" data-category="Controller" style="display: none;">Controller</div>
            <div class="settings-sidebar-item" data-category="Long Query" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Long Query</div>
            <div class="settings-sidebar-item" data-category="Replication" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Replication</div>
            <div class="settings-sidebar-item" data-category="Retention" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Retention</div>
            <div class="settings-sidebar-item" data-category="Sampling" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Sampling</div>
            <div class="settings-sidebar-item" data-category="Swapping" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Swapping</div>
            <div class="settings-sidebar-item" data-category="System" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">System</div>
            <div class="settings-sidebar-item" data-category="Threshold" style="color: #4b5563; font-size: 0.85rem; cursor: pointer; padding-left: 13px;">Threshold</div>
        </div>"""

content = re.sub(old_sidebar, new_sidebar, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated sidebar HTML")
