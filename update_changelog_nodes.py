import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Improvement:</span> Dashboard &#252;zerindeki "Nodes" (Petek) grafi&#287;indeki petekler k&#252;&#231;&#252;lt&#252;ld&#252; ve fare &#252;zerine geldi&#287;inde beyaz dolgu ve ye&#351;il d&#305;&#351; &#231;izgi (outline) g&#246;sterecek &#351;ekilde estetik bir animasyon eklendi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Cluster &#252;zerine gelindi&#287;inde a&#231;&#305;lan bilgi penceresi (Hover Menu) art&#305;k dinamik olarakkapal&#305;/devre d&#305;&#351;&#305; b&#305;rak&#305;lm&#305;&#351; sunucular&#305; alg&#305;l&#305;yor. E&#287;er kapal&#305; sunucu yoksa ilgili uyar&#305; mesaj&#305; art&#305;k g&#246;sterilmiyor.</li>
                        <li><span style="font-weight: 600;">Feature:</span> Taray&#305;c&#305; ge&#231;mi&#351;i"""

content = content.replace('<li><span style="font-weight: 600;">Feature:</span> Taray&#305;c&#305; ge&#231;mi&#351;i', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated.")
