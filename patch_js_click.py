import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

click_js = """
    // Add click listeners to sidebar categories
    document.querySelectorAll('.settings-sidebar-item').forEach(item => {
        item.addEventListener('click', () => {
            // Remove active styling from all
            document.querySelectorAll('.settings-sidebar-item').forEach(el => {
                el.style.color = '#4b5563';
                el.style.fontWeight = 'normal';
                el.style.borderLeft = 'none';
                el.style.paddingLeft = '13px';
            });
            // Add active styling to clicked
            item.style.color = 'var(--primary)';
            item.style.fontWeight = '500';
            item.style.borderLeft = '3px solid var(--primary)';
            item.style.paddingLeft = '10px';
            
            // Load settings for this category
            loadSettings(item.dataset.category);
        });
    });
"""

insert_marker = "function loadSettings(category = null) {"
if "click listeners to sidebar" not in content:
    content = content.replace(insert_marker, click_js + "\n    " + insert_marker)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added click listener JS")
else:
    print("Click listener already exists")

