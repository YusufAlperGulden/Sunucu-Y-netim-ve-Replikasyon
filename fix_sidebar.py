import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the sidebar link to add data-view="users-view"
pattern_link = r'<a href="#">\s*<svg[^>]+><path d="M11\.5 15H7a4 4 0 0 0-4 4v2".*?</svg>\s*<span class="sidebar-text">User management</span>\s*</a>'
replacement_link = r'''<a href="#" data-view="users-view">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><path d="M11.5 15H7a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M21.378 10.626a1 1 0 1 0-3.004-3.004l-4.01 4.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"></path></svg> <span class="sidebar-text">User management</span>
                  </a>'''

content = re.sub(pattern_link, replacement_link, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Sidebar link fixed")
