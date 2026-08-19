import re

html_path = 'fastapi_app/templates/index.html'
js_path = 'fastapi_app/static/main.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=26', 'v=27')

new_changelog = """<li><span style="font-weight: 600;">Feature:</span> SSH Altyap iin <b>Paramiko</b> entegrasyonu tamamland! Artk Backend tarafnda, sunucularnza kaydedilen ifreler veya PEM Private Key'ler zlerek dorudan Linux Terminaline erisim saglanabiliyor. "Edit Node" penceresine eklenen "Test SSH" butonu ile, sunucuya baaryla bala-balanamadnz (whoami vb. temel komutlarla) test edebilirsiniz.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
html_content = re.sub(pattern, r'\g<1>' + new_changelog, html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=26', 'v=27')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Bumped version to v=27 and updated changelog")
