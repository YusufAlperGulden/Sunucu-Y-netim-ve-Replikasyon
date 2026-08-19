with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove v1.4.0 and v1.3.0 links from changelog sidebar
old_sidebar_part = """                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.0</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-3-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.3.0</a>"""

new_sidebar_part = """                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>"""

if old_sidebar_part in html:
    html = html.replace(old_sidebar_part, new_sidebar_part)
    print("Removed v1.4.0 and v1.3.0 links from HTML")
else:
    print("Could not find exact old sidebar part")

# Bump to v=47
html = html.replace('v=46', 'v=47')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update changelogAnchors in main.js
js = js.replace("changelogAnchors = ['v1-4-2', 'v1-4-1', 'v1-4-0', 'v1-3-0'];", "changelogAnchors = ['v1-4-2', 'v1-4-1'];")
js = js.replace('v=46', 'v=47')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js and bumped to v=47")
