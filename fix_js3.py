# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix the corrupted JS strings
content = re.sub(r'const statusText = isOperational \? \'[^\']*Operational\' : \'[^\']*Warning\';', "const statusText = isOperational ? '&#8226; Operational' : '&#8226; Warning';", content)
content = re.sub(r"if \(!confirm\('Primary sunucudaki eski/kay.*t d.*Y.* replikasyon slotlar.* \(orphan slots\) temizlenecek. Onayl.*yor musunuz\?'\)\) return;", "if (!confirm('Primary sunucudaki eski/kayıt dışı replikasyon slotları (orphan slots) temizlenecek. Onaylıyor musunuz?')) return;", content)
content = re.sub(r"if \(!confirm\('Bu sunucuyu silmek istedi.*Yinize emin misiniz\?'\)\) return;", "if (!confirm('Bu sunucuyu silmek istediğinize emin misiniz?')) return;", content)

# Also fix tooltip for nodes donut chart and add center text
# In index.html, we need to add the center text div to nodes-donut-svg
