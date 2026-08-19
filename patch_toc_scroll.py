with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add id="release-cycle" and id="whats-new" to h3 headings
old_rc = '<h3 style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>'
new_rc = '<h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>'

old_wn = '<h3 style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What\'s New</h3>'
new_wn = '<h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What\'s New</h3>'

if old_rc in html:
    html = html.replace(old_rc, new_rc, 1)
    print("Added id='release-cycle'")
else:
    print("Could not find old release-cycle heading")

if old_wn in html:
    html = html.replace(old_wn, new_wn, 1)
    print("Added id='whats-new'")
else:
    print("Could not find old whats-new heading")

# 2. Update Table of Contents links
old_toc = """                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); " style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); " style="color: inherit; text-decoration: none; ">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); " style="color: inherit; text-decoration: none; ">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); " style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>"""

new_toc = """                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)
    print("Updated TOC links")
else:
    print("Could not find exact old TOC block")

# Bump to v=48
html = html.replace('v=47', 'v=48')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("changelogAnchors = ['v1-4-2', 'v1-4-1'];", "changelogAnchors = ['v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=47', 'v=48')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js and bumped to v=48")
