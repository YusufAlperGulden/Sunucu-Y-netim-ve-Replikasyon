content = open('fastapi_app/templates/index.html', encoding='utf-8').read()
import re

# Find the start of nodes-view div
start_marker = 'id="nodes-view" class="view-section"'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: nodes-view not found")
    exit()

# Find the opening tag start
tag_start = content.rfind('<', 0, start_idx)
print(f"Tag starts at: {tag_start}")
print(f"Tag: {content[tag_start:tag_start+80]}")

# Now find the matching closing </div> by counting braces
depth = 0
i = tag_start
in_tag = False
found_end = -1

pos = tag_start
while pos < len(content):
    if content[pos:pos+4] == '<div':
        depth += 1
        pos += 4
    elif content[pos:pos+6] == '</div>':
        depth -= 1
        if depth == 0:
            found_end = pos + 6
            break
        pos += 6
    else:
        pos += 1

print(f"Closing div at: {found_end}")
print(f"Last 100 chars of section: {repr(content[found_end-100:found_end])}")
