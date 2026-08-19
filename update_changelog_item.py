import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Feature:</span> Sidebar men&#252;s&#252;ne "Backups" sekmesi eklendi. "All Backups" ve "Schedules" sekmelerini i&#231;eren yeni Backups sayfas&#305; tasarland&#305;.</li>
                        <li><span style="font-weight: 600;">Feature:</span> Sayfalardan ba&#287;&#305;ms&#305;z"""

content = content.replace('<li><span style="font-weight: 600;">Feature:</span> Sayfalardan ba&#287;&#305;ms&#305;z', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Changelog updated.")
