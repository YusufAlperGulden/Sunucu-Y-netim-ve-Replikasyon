import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix clusterCard click
old_cluster_card_click = """                clusterCard.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

new_cluster_card_click = """                clusterCard.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    if (window.location.hash !== '#projects-view') {
                        window.location.hash = 'projects-view';
                    }
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

content = content.replace(old_cluster_card_click, new_cluster_card_click)

# Fix tr click
old_tr_click = """                tr.addEventListener('click', async (e) => {
                    if(e.target.closest('button') || e.target.closest('.dropdown-menu')) return;
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

new_tr_click = """                tr.addEventListener('click', async (e) => {
                    if(e.target.closest('button') || e.target.closest('.dropdown-menu')) return;
                    if (window.location.hash !== '#projects-view') {
                        window.location.hash = 'projects-view';
                    }
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);"""

if old_tr_click in content:
    content = content.replace(old_tr_click, new_tr_click)

# Update showDetailView to ensure clusters-view is hidden just in case
old_show_detail = """    function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        detailView.style.display = 'block';"""

new_show_detail = """    function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';"""

content = content.replace(old_show_detail, new_show_detail)

# Bump version
content = content.replace('v=13', 'v=14')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=13', 'v=14')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fixed view stacking bug")
