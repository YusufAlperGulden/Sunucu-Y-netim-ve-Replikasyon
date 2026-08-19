import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace view management logic
old_view_management = r'// --- VIEW MANAGEMENT ---.*?function startDashboardInterval'
new_view_management = """// --- VIEW MANAGEMENT ---
    const sidebarLinks = document.querySelectorAll('.sidebar-nav > a, .sidebar-nav > div > a, a[data-view="changelog-view"]');
    const viewSections = document.querySelectorAll('.view-section');
    
    function handleRouting() {
        let hash = window.location.hash.substring(1) || 'projects-view';
        
        sidebarLinks.forEach(l => l.classList.remove('active'));
        let activeLink = document.querySelector(`a[data-view="${hash}"]`);
        if (!activeLink && hash === 'dashboard-view') {
            activeLink = document.querySelector(`a[data-view="clusters-view"]`);
        }
        if (activeLink) activeLink.classList.add('active');
        
        viewSections.forEach(section => {
            section.style.display = 'none';
        });
        
        const view = document.getElementById(hash);
        if (view) view.style.display = 'block';
        
        if (hash === 'projects-view') {
            if(typeof showProjectsView === 'function') showProjectsView();
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        } else if (hash === 'audit-logs-view') {
            if (typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs();
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        } else if (hash === 'settings-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        } else if (hash === 'dashboard-view') {
            if(typeof startDashboardInterval === 'function') startDashboardInterval();
        } else {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        }
    }
    
    window.addEventListener('hashchange', handleRouting);

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-view');
            if (targetId) {
                if (window.location.hash !== '#' + targetId) {
                    window.location.hash = targetId;
                } else {
                    handleRouting();
                }
            }
        });
    });
    
    // Process initial route
    setTimeout(handleRouting, 10);

    function startDashboardInterval"""

js_content = re.sub(old_view_management, new_view_management, js_content, flags=re.DOTALL)

# Replace the submenu click logic
old_submenu_logic = r'a\.onclick = \(e\) => \{.*?e\.preventDefault\(\);.*?document\.querySelectorAll\(\'.view-section\'\).*?document\.getElementById\(\'dashboard-view\'\).*?document\.querySelectorAll\(\'\.sidebar-nav a\'\).*?const clustersLink = .*?if \(clustersLink\).*?if \(typeof startDashboardInterval === \'function\'\).*?\};'
new_submenu_logic = """a.onclick = (e) => {
                            e.preventDefault();
                            if (window.location.hash !== '#dashboard-view') {
                                window.location.hash = 'dashboard-view';
                            } else {
                                handleRouting();
                            }
                        };"""

js_content = re.sub(old_submenu_logic, new_submenu_logic, js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated main.js")
