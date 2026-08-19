import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

show_detail = """function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        detailView.style.display = 'block';
        currentProjectId = proj.id;
        
        const el_detail_proj_name = document.getElementById('detail-proj-name'); if(el_detail_proj_name) el_detail_proj_name.innerText = proj.name;
        const el_detail_proj_desc = document.getElementById('detail-proj-desc'); if(el_detail_proj_desc) el_detail_proj_desc.innerText = proj.description || 'No description';
        
        renderNodes(proj.nodes);
        
        // Ensure "Dashboards" tab is active by default
        const dashTab = document.querySelector('.cluster-tab[data-tab="dashboards"]');
        if(dashTab) dashTab.click();
    }"""

content = re.sub(r'function showDetailView\(proj\) \{.*?renderNodes\(proj\.nodes\);\s*\}', show_detail, content, flags=re.DOTALL)

# Bump version to 10
content = content.replace('v=9', 'v=10')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=9', 'v=10')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated showDetailView and version")
