with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Global nodesPageData declaration at the top
if 'var nodesPageData = [];' not in js and 'let nodesPageData = [];' not in js and 'window.nodesPageData = [];' not in js:
    js = 'window.nodesPageData = [];\nvar nodesPageData = window.nodesPageData;\n' + js
    print("Added global nodesPageData declaration")

# 2. Update renderNodesPage to support version containing HTML (like spinner) and cluster logos
# Let's inspect where renderNodesPage handles version and clusterLogo
print("renderNodesPage present:", 'function renderNodesPage()' in js)
