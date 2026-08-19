import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog = """<li><span style="font-weight: 600;">Fix:</span> "Clusters" listesi ve "Proje Detay" sayfalarının (Dashboard) aynı ekranda üst üste binmesi (Stacking) hatası giderildi. Yönlendirme (Routing) mantığı düzeltilerek her sayfanın kendi özel bağlantısına sahip olması sağlandı. Artık bir kümeye tıkladığınızda tertemiz yepyeni bir sayfada detaylar açılıyor.</li>
"""

pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
content = re.sub(pattern, r'\g<1>' + new_changelog, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated changelog for view stacking")
