import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Fix:</span> Sol men&#252;deki "Changelog" butonuna t&#305;kland&#305;&#287;&#305;nda sayfan&#305;n a&#231;&#305;lmamas&#305; sorunu (Javascript se&#231;ici hatas&#305;) giderildi. Art&#305;k Changelog sayfas&#305;na sorunsuz ge&#231;i&#351; yap&#305;labiliyor.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Giri&#351; ekran&#305;ndaki"""

content = content.replace('<li><span style="font-weight: 600;">Improvement:</span> Giri&#351; ekran&#305;ndaki', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Changelog updated.")
