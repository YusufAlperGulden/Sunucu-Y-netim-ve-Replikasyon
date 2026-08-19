import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Improvement:</span> Giri&#351; ekran&#305;ndaki "Kullan&#305;c&#305; Ad&#305;" ve "&#350;ifre" girdi alanlar&#305;n&#305;n kenarl&#305;klar&#305; (border) kal&#305;nla&#351;t&#305;r&#305;larak daha g&#246;r&#252;n&#252;r hale getirildi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Giri&#351; (Login) ekran&#305;ndaki"""

content = content.replace('<li><span style="font-weight: 600;">Improvement:</span> Giri&#351; (Login) ekran&#305;ndaki', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Changelog updated.")
