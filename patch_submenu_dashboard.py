# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The current code: a.onclick = () => document.querySelector('a[data-view="clusters-view"]').click();
# We need to change it to show dashboard-view
dashboard_onclick = """a.onclick = (e) => {
                          e.preventDefault();
                          document.querySelectorAll('.view-section').forEach(v => v.style.display = 'none');
                          document.getElementById('dashboard-view').style.display = 'block';
                          document.querySelectorAll('.sidebar-nav a').forEach(l => l.classList.remove('active'));
                          const clustersLink = document.querySelector('a[data-view="clusters-view"]');
                          if (clustersLink) clustersLink.classList.add('active');
                          if (typeof startDashboardInterval === 'function') startDashboardInterval();
                      };"""

content = content.replace("a.onclick = () => document.querySelector('a[data-view=\"clusters-view\"]').click();", dashboard_onclick)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS submenu dashboard patched")
