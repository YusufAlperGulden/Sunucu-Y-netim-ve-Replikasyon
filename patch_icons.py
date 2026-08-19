import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Clusters in Home
old_clusters_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>'
new_clusters_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg>'

# Nodes in Home
old_nodes_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>'
new_nodes_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="6" rx="1" ry="1"></rect><rect x="2" y="14" width="20" height="6" rx="1" ry="1"></rect><line x1="6" y1="7" x2="6.01" y2="7"></line><line x1="10" y1="7" x2="18" y2="7"></line><line x1="6" y1="17" x2="6.01" y2="17"></line><line x1="10" y1="17" x2="18" y2="17"></line></svg>'

content = content.replace(old_clusters_icon, new_clusters_icon)
content = content.replace(old_nodes_icon, new_nodes_icon)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Icons patched successfully")
