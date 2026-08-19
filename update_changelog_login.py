import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Improvement:</span> Giri&#351; (Login) ekran&#305;ndaki kutu k&#252;&#231;&#252;lt&#252;lerek "ClusterControl" ba&#351;l&#305;&#287;&#305; kutunun i&#231;ine al&#305;nd&#305;. Ayr&#305;ca kutu arka plan&#305;na %10 &#351;effafl&#305;k (transparency) ve bulan&#305;kla&#351;t&#305;rma (blur) efekti eklenerek, arkadan ge&#231;en baloncuklar&#305;n estetik bir &#351;ekilde g&#246;z&#252;kmesi sa&#287;land&#305;.</li>
                        <li><span style="font-weight: 600;">Feature:</span> Sidebar men&#252;s&#252;ne"""

content = content.replace('<li><span style="font-weight: 600;">Feature:</span> Sidebar men&#252;s&#252;ne', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Changelog updated.")
