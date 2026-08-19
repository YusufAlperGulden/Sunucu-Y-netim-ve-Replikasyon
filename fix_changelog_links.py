import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix version links in changelog sidebar - use onclick to scroll instead of hash
content = content.replace(
    '<a href="#v1-4-2" style="color: #4b5563; text-decoration: none;">v1.4.2 (Latest)</a>',
    '<a href="#changelog-view" onclick="event.preventDefault(); document.getElementById(\'v1-4-2\').scrollIntoView({behavior:\'smooth\'}); document.querySelectorAll(\'#changelog-view .cl-sidebar-link\').forEach(e=>e.style.fontWeight=\'normal\'); this.style.fontWeight=\'bold\';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.2 (Latest)</a>'
)
content = content.replace(
    '<a href="#v1-4-1" style="color: #4b5563; text-decoration: none;">v1.4.1</a>',
    '<a href="#changelog-view" onclick="event.preventDefault(); document.getElementById(\'v1-4-1\').scrollIntoView({behavior:\'smooth\'}); document.querySelectorAll(\'#changelog-view .cl-sidebar-link\').forEach(e=>e.style.fontWeight=\'normal\'); this.style.fontWeight=\'bold\';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>'
)
content = content.replace(
    '<a href="#v1-4-0" style="color: #4b5563; text-decoration: none;">v1.4.0</a>',
    '<a href="#changelog-view" onclick="event.preventDefault(); document.getElementById(\'v1-4-0\').scrollIntoView({behavior:\'smooth\'}); document.querySelectorAll(\'#changelog-view .cl-sidebar-link\').forEach(e=>e.style.fontWeight=\'normal\'); this.style.fontWeight=\'bold\';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.0</a>'
)
content = content.replace(
    '<a href="#v1-3-0" style="color: #4b5563; text-decoration: none;">v1.3.0</a>',
    '<a href="#changelog-view" onclick="event.preventDefault(); document.getElementById(\'v1-3-0\').scrollIntoView({behavior:\'smooth\'}); document.querySelectorAll(\'#changelog-view .cl-sidebar-link\').forEach(e=>e.style.fontWeight=\'normal\'); this.style.fontWeight=\'bold\';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.3.0</a>'
)

# 2. Fix Archived link - disable click gracefully
content = content.replace(
    '<a href="#" style="color: #4b5563; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px;">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>',
    '<a href="#changelog-view" onclick="event.preventDefault();" style="color: #9ca3af; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px; cursor: default;" title="Archived versions coming soon">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>'
)

print("Changelog links fixed:", all([
    'cl-sidebar-link' in content,
    'event.preventDefault()' in content
]))

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
