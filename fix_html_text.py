# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = content.replace("? Paused", "&#8226; Paused")
content = re.sub(r'Hesab.*ok mu\? Yeni kay.*olu.*turun\.', 'Hesabınız yok mu? Yeni kayıt oluşturun.', content)
content = re.sub(r'Sunucu Sa.*k ve D.*zenleme', 'Sunucu Sağlık ve Düzenleme', content)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML text fixed")
