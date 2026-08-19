content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
import re

# Find the full nodes-view div and show it
idx = content.find('id="nodes-view"')
# Get a big chunk to see the full section
print(repr(content[idx:idx+2000]))
