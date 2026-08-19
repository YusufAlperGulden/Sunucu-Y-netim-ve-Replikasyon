content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
import re
# Find the actual id="nodes-view" element
m = re.search(r'id="nodes-view"[^>]*>', content)
if m:
    idx = m.start()
    print("Found at position:", idx)
    print("Element:", content[idx-10:idx+200])
    # Check what class it has
    print("\nClass info:", re.search(r'class="([^"]+)"', content[idx:idx+100]))
else:
    print("NOT FOUND")
