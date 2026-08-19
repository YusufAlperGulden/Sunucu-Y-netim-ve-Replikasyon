content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
# Find ALL section tags and their positions + IDs
import re
sections = list(re.finditer(r'<(section|div)\s[^>]*id="([^"]+)"[^>]*>', content))
print(f"Total elements with IDs: {len(sections)}")

# Find where the nodes sidebar link is defined
sidebar_links = re.findall(r'data-view="([^"]+)"', content)
print("All data-view values:", sidebar_links)

# Check if there's a dedicated nodes view div at all
print("\nIs 'nodes-view' present as an ID?", 'id="nodes-view"' in content)
print("Total file size:", len(content))
