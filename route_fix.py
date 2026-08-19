import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make it route to project-detail
old_cluster_card_click = """                clusterCard.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    if (window.location.hash !== '#projects-view') {
                        window.location.hash = 'projects-view';
                    }
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

new_cluster_card_click = """                clusterCard.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

content = content.replace(old_cluster_card_click, new_cluster_card_click)

# Also fix the submenu click!
old_submenu_click = """a.className = "submenu-item"; a.onclick = async (e) => {
                            e.preventDefault();
                            if (window.location.hash !== '#projects-view') {
                                window.location.hash = 'projects-view';
                            }
                            try {"""

new_submenu_click = """a.className = "submenu-item"; a.onclick = async (e) => {
                            e.preventDefault();
                            try {"""
                            
if old_submenu_click in content:
    content = content.replace(old_submenu_click, new_submenu_click)

# Update showDetailView to just change the hash, but wait, if it changes hash, it triggers handleRouting!
# If we do window.location.hash = 'project-detail-view', handleRouting runs and shows it.
# Then we populate it!
old_show_detail = """    function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';"""

new_show_detail = """    function showDetailView(proj) {
        window.location.hash = 'project-detail-view';
        // wait for routing to finish or just populate directly
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';"""

content = content.replace(old_show_detail, new_show_detail)

# Add project-detail-view to handleRouting
old_routing = """        if (hash === 'projects-view') {"""
new_routing = """        if (hash === 'project-detail-view') {
            document.querySelectorAll('.view-section').forEach(section => section.style.display = 'none');
            const dv = document.getElementById('project-detail-view');
            if(dv) dv.style.display = 'block';
        } else if (hash === 'projects-view') {"""

content = content.replace(old_routing, new_routing)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update index.html to make project-detail-view a view-section
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

old_html = """<div id="project-detail-view" style="display: none;">"""
new_html = """<div id="project-detail-view" class="view-section" style="display: none;">"""
html_content = html_content.replace(old_html, new_html)

# Bump version
html_content = html_content.replace('v=14', 'v=15')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=14', 'v=15')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Fixed view stacking with proper routing")
