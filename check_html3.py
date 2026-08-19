content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
idx = content.find('nodes-page-tbody')
# Search backwards for the nearest section tag
chunk = content[max(0,idx-3000):idx]
import re
sections = list(re.finditer(r'<section[^>]*id="([^"]+)"', chunk))
divs_with_id = list(re.finditer(r'<div[^>]*id="([^"]+)"', chunk[-1500:]))
print("Last section before nodes table:", sections[-1].group() if sections else "NONE")
print("Last 3 divs with ID:", [m.group() for m in divs_with_id[-3:]])
