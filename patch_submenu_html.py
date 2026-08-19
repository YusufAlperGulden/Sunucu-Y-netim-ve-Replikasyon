# -*- coding: utf-8 -*-
import re

with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Clusters link in the sidebar
old_clusters_link = """<a href="#" data-view="clusters-view" class="active">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg> <span class="sidebar-text">Clusters</span>
                </a>"""

new_clusters_link = """<div style="display: flex; flex-direction: column;">
                <a href="#" data-view="clusters-view" class="active" style="display: flex; justify-content: space-between; align-items: center; padding-right: 16px;">
                    <div style="display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px; vertical-align: middle;"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg> <span class="sidebar-text">Clusters</span>
                    </div>
                    <svg id="clusters-chevron" onclick="event.preventDefault(); event.stopPropagation(); const sub = document.getElementById('clusters-submenu'); const chev = document.getElementById('clusters-chevron'); if(sub.style.display==='none'){sub.style.display='flex'; chev.style.transform='rotate(180deg)';}else{sub.style.display='none'; chev.style.transform='rotate(0deg)';}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.2s; cursor: pointer; display: none;"><polyline points="6 9 12 15 18 9"></polyline></svg>
                </a>
                <div id="clusters-submenu" style="display: none; flex-direction: column; background: #0b0f19; padding: 4px 0;">
                    <!-- JS will populate submenu items here -->
                </div>
                </div>"""

# I need to set display: block on chevron only when sidebar is expanded. 
# But wait, there's a "sidebar-text" class. I can use standard css or just show it via JS. I'll let JS handle it, or just use css.

content = content.replace(old_clusters_link, new_clusters_link)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML submenu base patched")
