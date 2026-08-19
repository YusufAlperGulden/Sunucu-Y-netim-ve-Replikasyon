with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's find the exact old block and remove it / replace it
old_start = js.find('// --- NODES PAGE MANAGEMENT ---')
if old_start == -1:
    old_start = js.find("document.addEventListener('DOMContentLoaded', () => {\n    \n\n\n    let currentFilter = 'All';")

print("Old block starts at:", old_start)

# Let's find where the old block ends
old_end = js.find("renderNodesPage();\n});", old_start)
if old_end != -1:
    old_end += len("renderNodesPage();\n});")
print("Old block ends at:", old_end)

# Also check where fetchNodesPage is at the bottom of the file
idx_fn = js.find('window.fetchNodesPage = async function')
print("fetchNodesPage at bottom is at:", idx_fn)
