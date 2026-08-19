import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace document.getElementById('cc-projects-tbody').innerHTML = ...
content = content.replace(
    "document.getElementById('cc-projects-tbody').innerHTML = '<tr><td colspan=\"6\" style=\"text-align:center; padding: 20px;\">No clusters found. Click + Add Project to start.</td></tr>';",
    "const cptbody = document.getElementById('cc-projects-tbody'); if (cptbody) cptbody.innerHTML = '<tr><td colspan=\"6\" style=\"text-align:center; padding: 20px;\">No clusters found. Click + Add Project to start.</td></tr>';"
)

content = content.replace(
    "const tbody = document.getElementById('cc-projects-tbody');\n            tbody.innerHTML = data.map(",
    "const tbody = document.getElementById('cc-projects-tbody');\n            if(tbody) tbody.innerHTML = data.map("
)

content = content.replace(
    "document.getElementById('cc-donut-legend').innerHTML =",
    "const ccd = document.getElementById('cc-donut-legend'); if(ccd) ccd.innerHTML ="
)

content = content.replace(
    "document.getElementById('ntt-badge').innerHTML =",
    "const nttb = document.getElementById('ntt-badge'); if(nttb) nttb.innerHTML ="
)

content = content.replace(
    "topoContainer.innerHTML = topoHtml;",
    "if(topoContainer) topoContainer.innerHTML = topoHtml;"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added guards to innerHTML assignments")
