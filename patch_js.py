import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update submenu click
old_submenu_click = """a.className = "submenu-item"; a.onclick = (e) => {
                            e.preventDefault();
                            if (window.location.hash !== '#dashboard-view') {
                                window.location.hash = 'dashboard-view';
                            } else {
                                handleRouting();
                            }
                        };"""

new_submenu_click = """a.className = "submenu-item"; a.onclick = async (e) => {
                            e.preventDefault();
                            if (window.location.hash !== '#projects-view') {
                                window.location.hash = 'projects-view';
                            }
                            try {
                                const res = await apiFetch(`/api/projects/${proj.id}`);
                                if (res.ok) {
                                    showDetailView(await res.json());
                                    refreshCurrentProject();
                                }
                            } catch(err) { console.error(err); }
                        };"""

if old_submenu_click in content:
    content = content.replace(old_submenu_click, new_submenu_click)
else:
    print("Could not find old_submenu_click")

# 2. Add cluster-tab logic
cluster_tab_logic = """
    // Initialize cluster tabs
    document.querySelectorAll('.cluster-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.cluster-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            
            tab.classList.add('active');
            const targetId = 'tab-content-' + tab.dataset.tab;
            const targetEl = document.getElementById(targetId);
            if (targetEl) targetEl.style.display = 'block';

            if (tab.dataset.tab === 'dashboards') {
                if(typeof startDashboardInterval === 'function') startDashboardInterval();
            } else {
                if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            }
        });
    });
"""

# Insert cluster_tab_logic at the end of DOMContentLoaded (or anywhere inside it)
# We can just put it after `sidebarLinks.forEach`
insert_marker = "sidebarLinks.forEach(link => {"
if insert_marker in content:
    content = content.replace(insert_marker, cluster_tab_logic + "\n    " + insert_marker)
else:
    print("Could not find insert_marker")

# 3. Update hash routing for dashboard-view
routing_old = """} else if (hash === 'dashboard-view') {
            if(typeof startDashboardInterval === 'function') startDashboardInterval();
        }"""
if routing_old in content:
    content = content.replace(routing_old, "}")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched main.js")
