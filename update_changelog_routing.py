import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Feature:</span> Taray&#305;c&#305; ge&#231;mi&#351;i (Browser History / Back Button) deste&#287;i i&#231;in Hash tabanl&#305; y&#246;nlendirme (Routing) sistemi eklendi. Art&#305;k sayfalar aras&#305; ge&#231;i&#351;lerde taray&#305;c&#305;n&#305;n "Geri" ve "&#304;leri" butonlar&#305; tam fonksiyonalite ile &#231;al&#305;&#351;maktad&#305;r.</li>
                        <li><span style="font-weight: 600;">Fix:</span> Sol men&#252;deki"""

content = content.replace('<li><span style="font-weight: 600;">Fix:</span> Sol men&#252;deki', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated.")
