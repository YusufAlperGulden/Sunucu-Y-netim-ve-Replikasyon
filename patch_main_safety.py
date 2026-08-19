import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the catch block so it doesn't wipe out projectsContainer
content = content.replace(
    'if (errDiv) errDiv.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.stack || error.toString())}</div>`;',
    'if (errDiv) errDiv.insertAdjacentHTML("afterbegin", `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.stack || error.toString())}</div>`);'
)

# Fix line 319 (tbody.innerHTML = '')
content = content.replace(
    "const tbody = document.getElementById('cc-projects-tbody');\n            tbody.innerHTML = '';",
    "const tbody = document.getElementById('cc-projects-tbody');\n            if(tbody) tbody.innerHTML = '';"
)

# Fix clustersList.innerHTML = '';
content = content.replace(
    "if (clustersList) clustersList.innerHTML = '';",
    "if (clustersList) clustersList.innerHTML = '';"
)

# Fix cc-donut-center-text
content = content.replace(
    "document.getElementById('cc-donut-center-text').innerText = operationalCount;",
    "const el1 = document.getElementById('cc-donut-center-text'); if(el1) el1.innerText = operationalCount;"
)
content = content.replace(
    "document.getElementById('nodes-donut-center-num').innerText = allNodes.length;",
    "const el2 = document.getElementById('nodes-donut-center-num'); if(el2) el2.innerText = allNodes.length;"
)

# Fix nodes-donut-slice
content = content.replace(
    "const nodeStats = document.getElementById('nodes-donut-slice').parentNode.parentNode.nextElementSibling;",
    "const nds = document.getElementById('nodes-donut-slice'); const nodeStats = nds ? nds.parentNode.parentNode.nextElementSibling : null;"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched main.js fetchProjects safety")
