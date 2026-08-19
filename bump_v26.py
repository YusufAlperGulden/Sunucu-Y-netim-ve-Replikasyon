import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=25', 'v=26')

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> Uzun zamandr beklenen <b>Fiziksel Sunucu Mdahelesi (SSH Altyaps)</b> in ilk byk adm atld! Sunucu ekleme ve dzenleme formlarna SSH IP, Port, Username ve Password/PEM key alanlar eklendi. Girdiiniz ifreler veya private keyler veritabannda dorudan (Plain text) tutulmaz; ayn PostgreSQL URL'leriniz gibi AES-256 algoritmasyla ifrelenerek gvenle muhafaza edilir. Bu altyap, yaknda Linux ilerine szp <code style="background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px;">pgbackrest.conf</code> gibi fiziksel konfigrasyon dosyalarnda deiiklik yapabilmemizi salayacak.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=25', 'v=26')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=26 and updated changelog")
