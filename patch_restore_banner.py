import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

banner_html = """
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #b45309; background: #fef3c7; padding: 6px 16px; border-radius: 4px; border: 1px solid #fcd34d; margin-right: auto; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    <span id="demo-banner-text">This is a demo environment. Any changes made to the nodes and clusters will be reset daily.</span>
                </div>
"""

# Insert it back after <!-- GLOBAL TOP BAR --> and its container
search_str = '<!-- GLOBAL TOP BAR -->\n            <div style="height: 60px; min-height: 60px; display: flex; justify-content: flex-end; align-items: center; padding: 0 40px; gap: 24px; z-index: 100; border-bottom: 1px solid var(--glass-border);">'

if search_str in content:
    content = content.replace(search_str, search_str + banner_html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Banner restored")
else:
    print("Could not find the global top bar")
