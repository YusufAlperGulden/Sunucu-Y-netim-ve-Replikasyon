import re

# 1. Make fetchNodesPage a window-exposed function
js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Expose as window function so it works regardless of scope
js = js.replace(
    'async function fetchNodesPage() {',
    'window.fetchNodesPage = async function fetchNodesPage() {'
)
# Close the function properly - find the end
# Also update the call in handleRouting to use window.
js = js.replace(
    "if(typeof fetchNodesPage === 'function') fetchNodesPage();",
    "window.fetchNodesPage();"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Exposed fetchNodesPage as window function")
