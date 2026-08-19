import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def make_scroll_link(href_id, label, extra_style=""):
    return f'<a href="#changelog-view" onclick="event.preventDefault(); document.getElementById(\'{href_id}\').scrollIntoView({{behavior:\'smooth\'}}); " style="color: inherit; text-decoration: none; {extra_style}">{label}</a>'

# Fix TOC links
replacements = [
    ('<a href="#v1-4-2" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>',
     make_scroll_link('v1-4-2', 'v1.4.2 Release', 'font-weight: 500;')),
    ('<a href="#v1-4-2" style="color: inherit; text-decoration: none;">Release cycle</a>',
     make_scroll_link('v1-4-2', 'Release cycle')),
    ('<a href="#v1-4-2" style="color: inherit; text-decoration: none;">What\'s New</a>',
     make_scroll_link('v1-4-2', "What's New")),
    ('<a href="#v1-4-1" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>',
     make_scroll_link('v1-4-1', 'v1.4.1 Release', 'font-weight: 500;')),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        print(f"NOT FOUND: {old[:60]}")

print(f"Fixed {count} TOC links")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
