import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

subtab_logic = """
    // Initialize cluster subtabs (Node list vs Topology)
    document.querySelectorAll('.cluster-subtab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const parent = tab.closest('.glass-panel');
            if(parent) {
                parent.querySelectorAll('.cluster-subtab').forEach(t => {
                    t.classList.remove('active');
                    t.style.color = '#6b7280';
                    t.style.borderBottom = 'none';
                });
                parent.querySelectorAll('.subtab-content').forEach(c => c.style.display = 'none');
                
                tab.classList.add('active');
                tab.style.color = '#6366f1';
                tab.style.borderBottom = '2px solid #6366f1';
                
                const targetId = 'subtab-' + tab.dataset.subtab;
                const targetEl = document.getElementById(targetId);
                if (targetEl) targetEl.style.display = 'block';
            }
        });
    });
"""

insert_marker = "document.querySelectorAll('.cluster-tab').forEach(tab => {"
if insert_marker in content:
    content = content.replace(insert_marker, subtab_logic + "\n    " + insert_marker)
else:
    print("Could not find insert_marker")

# Bump version to v=11
content = content.replace('v=10', 'v=11')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=10', 'v=11')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Added subtab listener and bumped version")
