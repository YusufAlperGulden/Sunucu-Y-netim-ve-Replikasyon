import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

switch_func = """
    window.switchUserTab = function(tabName) {
        // Hide all contents
        document.querySelectorAll('.user-tab-content').forEach(el => el.style.display = 'none');
        // Reset all tabs
        document.querySelectorAll('.user-tab').forEach(el => {
            el.style.color = 'var(--text-muted)';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active-tab');
        });
        
        // Show target content
        const targetContent = document.getElementById('content-' + tabName);
        if(targetContent) targetContent.style.display = 'block';
        
        // Highlight target tab
        const targetTab = document.getElementById('tab-' + tabName);
        if(targetTab) {
            targetTab.style.color = 'var(--primary)';
            targetTab.style.borderBottom = '2px solid var(--primary)';
            targetTab.classList.add('active-tab');
        }
    };
"""

# Append to main.js if not already there
if "window.switchUserTab" not in content:
    content += "\n" + switch_func

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("switchUserTab added")
