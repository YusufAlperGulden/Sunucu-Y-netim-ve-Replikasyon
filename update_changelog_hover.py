import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Fix:</span> "Home" sayfas&#305;ndaki "Clusters" tablosunda sunucular&#305;n &#252;zerine fare ile gelindi&#287;inde (hover) a&#231;&#305;lan "Cluster information" penceresinin, fare ba&#351;ka bir yere kayd&#305;r&#305;ld&#305;&#287;&#305;nda ekranda as&#305;l&#305; kalmas&#305; (kapanmamas&#305;) hatas&#305; giderildi. Art&#305;k fare pencereden veya sat&#305;rdan &#231;&#305;kt&#305;&#287;&#305;nda pencere do&#287;ru &#351;ekilde kapan&#305;yor.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Dashboard"""

content = content.replace('<li><span style="font-weight: 600;">Improvement:</span> Dashboard', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated.")
