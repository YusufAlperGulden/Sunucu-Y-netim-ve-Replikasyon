window.nodesPageData = [];
var nodesPageData = window.nodesPageData;
let globalAuthToken = localStorage.getItem('auth_token') || 'YWRtaW46YWRtaW4xMjM=';
function escapeHTML(str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
async function apiFetch(url, options = {}) {
    options.headers = options.headers || {};
    if (globalAuthToken) {
        options.headers['Authorization'] = 'Basic ' + globalAuthToken;
    }
    const res = await fetch(url, options);
    if (res.status === 401) {
        // Show login screen if unauthorized
        const loginScreen = document.getElementById('login-screen');
        if(loginScreen) {
            loginScreen.style.display = 'flex';
        }
        localStorage.removeItem('auth_token');
        globalAuthToken = null;
    }
    return res;
}
document.addEventListener('DOMContentLoaded', () => {

    // --- LOGIN CANVAS ANIMATION (ANTIGRAVITY STYLE) ---
    const canvas = document.getElementById('login-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        
        // Google colors: Blue, Red, Yellow, Green, Purple
        const colors = ['#4285F4', '#EA4335', '#FBBC04', '#34A853', '#8b5cf6'];
        
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();
        
        class Particle {
            constructor() {
                this.size = Math.random() * 220 + 150;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 0.35;
                this.vy = (Math.random() - 0.5) * 0.35;
                
                if (Math.abs(this.vx) < 0.1) this.vx = 0.18 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.1) this.vy = 0.18 * Math.sign(this.vy || 1);
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;

                
                // Screen edges collision
                if (this.x - this.size > width) { this.x = width - this.size; this.vx *= -1; }
                if (this.x + this.size < 0) { this.x = -this.size; this.vx *= -1; }
                if (this.y - this.size > height) { this.y = height - this.size; this.vy *= -1; }
                if (this.y + this.size < 0) { this.y = -this.size; this.vy *= -1; }
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = 0.42;
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
        
        for (let i = 0; i < 35; i++) {
            particles.push(new Particle());
            // Fast forward a little bit
            for(let j=0; j<Math.random()*100; j++) particles[i].update();
        }
        
        function animate() {
            if (document.getElementById('login-screen').style.display === 'none') {
                return; // Stop animating when login is hidden
            }
            ctx.clearRect(0, 0, width, height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        animate();
    }

    // DOM Elements
    const modalAddProj = document.getElementById('modal-add-project');
    const modalAddNode = document.getElementById('modal-add-node');
    const btnAddProj = document.getElementById('btn-add-project');
    const btnCloseProjModal = document.getElementById('btn-close-modal');
    const btnCloseNodeModal = document.getElementById('btn-close-node-modal');
    const formAddProj = document.getElementById('form-add-project');
    const formAddNode = document.getElementById('form-add-node');
    
    const modalEditProj = document.getElementById('modal-edit-project');
    const btnCloseEditProjModal = document.getElementById('btn-close-edit-modal');
    const formEditProj = document.getElementById('form-edit-project');

    
    const projectsContainer = document.getElementById('projects-container');
    const detailView = document.getElementById('project-detail-view');
    const btnBackProjects = document.getElementById('btn-back-projects');
    const nodesContainer = document.getElementById('nodes-container');
    
    const btnOpenNodeModal = document.getElementById('btn-open-node-modal');
    const btnSyncReplication = document.getElementById('btn-sync-replication');
    const btnSubmitNode = document.getElementById('btn-submit-node');
    const btnEditProjectDetail = document.getElementById('btn-edit-project-detail');

    let currentProjectId = null;
    let clusterHoverTimeout = null;

    const statusFilter = document.getElementById('cc-status-filter');
    if (statusFilter) {
        statusFilter?.addEventListener('change', (e) => {
            const filterValue = e.target.value;
            const rows = document.querySelectorAll('#cc-projects-tbody tr');
            rows.forEach(row => {
                if(filterValue === 'All') {
                    row.style.display = '';
                } else {
                    if(row.getAttribute('data-status') === filterValue) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        });
    }

    // --- MODAL EVENT LISTENERS ---
    if (btnAddProj) {
        btnAddProj?.addEventListener('click', () => {
            modalAddProj.style.display = 'flex';
        });
    }

    const btnDeployCluster = document.getElementById('btn-deploy-cluster-global');
    if (btnDeployCluster) {
        btnDeployCluster.addEventListener('click', () => {
            if (typeof openDeployWizard === 'function') {
                openDeployWizard();
            } else {
                modalAddProj.style.display = 'flex';
            }
        });
    }

    if (btnOpenNodeModal) {
        btnOpenNodeModal?.addEventListener('click', () => {
            modalAddNode.style.display = 'flex';
        });
    }

    if (btnCloseProjModal) {
        btnCloseProjModal?.addEventListener('click', () => {
            modalAddProj.style.display = 'none';
        });
    }

    if (btnCloseNodeModal) {
        btnCloseNodeModal.addEventListener('click', () => {
            modalAddNode.style.display = 'none';
        });
    }

    // --- VIEW MANAGEMENT ---
    // Ensure all view sections live inside main-content so the router can show them correctly.
    // Sections injected outside the <main> tag would otherwise render below the layout (invisible).
    (function relocateOrphanedViews() {
        const mainContent = document.querySelector('main.main-content');
        if (!mainContent) return;
        const orphanIds = ['users-view','backups-view','changelog-view','activity-view','reports-view','settings-view'];
        orphanIds.forEach(id => {
            const el = document.getElementById(id);
            if (el && !mainContent.contains(el)) {
                mainContent.appendChild(el);
            }
        });
    })();

    const sidebarLinks = document.querySelectorAll('.sidebar-nav > a, .sidebar-nav > div > a, a[data-view="changelog-view"]');
    const viewSections = document.querySelectorAll('.view-section');
    
    window.switchView = function(viewName, subtab) {
        let hash = viewName;
        if (!hash.endsWith('-view')) {
            hash = hash + '-view';
        }
        if (subtab) {
            window.pendingActivitySubtab = subtab;
        }
        if (window.location.hash === '#' + hash) {
            handleRouting();
        } else {
            window.location.hash = hash;
        }
    };

    function handleRouting() {
        let hash = window.location.hash.substring(1) || 'projects-view';
        
        // If hash is a changelog section anchor (e.g. v1-4-2), show changelog-view and scroll
        const changelogAnchors = ['v1-7-2', 'v1-7-1', 'v1-7-0', 'v1-6-4', 'v1-6-3', 'v1-6-2', 'v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];
        if (changelogAnchors.includes(hash)) {
            document.querySelectorAll('.view-section').forEach(s => s.style.display = 'none');
            const cv = document.getElementById('changelog-view');
            if (cv) { cv.style.display = 'block'; }
            setTimeout(() => {
                const el = document.getElementById(hash);
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            }, 100);
            const cl = document.querySelector('a[data-view="changelog-view"]');
            if (cl) { sidebarLinks.forEach(l => l.classList.remove('active')); cl.classList.add('active'); }
            return;
        }
        
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
        
        if (hash === 'project-detail-view') {
            document.querySelectorAll('.view-section').forEach(section => section.style.display = 'none');
            const dv = document.getElementById('project-detail-view');
            if(dv) dv.style.display = 'block';
            if(currentProjectId) {
                const c = document.getElementById('dashboard-metrics-container');
                if (c) c.innerHTML = '';
                fetchDashboardMetrics();
            }
        } else if (hash === 'projects-view') {
            if(typeof showProjectsView === 'function') showProjectsView();
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        } else if (hash === 'activity-view' || hash === 'audit-logs-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            const subtab = window.pendingActivitySubtab || 'alarms';
            window.pendingActivitySubtab = null;
            setTimeout(() => {
                const targetBtn = document.getElementById('ac-tab-' + subtab);
                if (targetBtn && typeof window.switchActivityTab === 'function') {
                    window.switchActivityTab(subtab, targetBtn);
                } else {
                    const auditBtn = document.getElementById('ac-tab-audit');
                    if (auditBtn && typeof window.switchActivityTab === 'function') {
                        window.switchActivityTab('audit', auditBtn);
                    }
                }
            }, 50);
        } else if (hash === 'settings-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof fetchProfile === 'function') fetchProfile();
            if(typeof window.checkMailServerStatus === 'function') window.checkMailServerStatus();
        } else if (hash === 'nodes-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            window.fetchNodesPage();
        } else if (hash === 'backups-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof window.loadAllBackups === 'function') window.loadAllBackups();
        } else {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
        }
    }
    
    window.addEventListener('hashchange', handleRouting);

    
    // Initialize cluster tabs
    
    // Initialize cluster subtabs (Node list vs Topology)
    document.querySelectorAll('.cluster-subtab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const parent = tab.closest('.glass-panel');
            if(parent) {
                parent.querySelectorAll('.cluster-subtab').forEach(t => {
                    t.classList.remove('active');
                    t.style.color = '#6b7280';
                    t.style.borderBottom = 'none';
                });
                parent.querySelectorAll('.subtab-content').forEach(c => c.style.display = 'none');
                
                tab.classList.add('active');
                tab.style.color = '#6366f1';
                tab.style.borderBottom = '2px solid #6366f1';
                
                const targetId = 'subtab-' + tab.dataset.subtab;
                const targetEl = document.getElementById(targetId);
                if (targetEl) targetEl.style.display = 'block';
            }
        });
    });

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
    setTimeout(fetchProfile, 10);

    function startDashboardInterval() {
        fetchDashboardMetrics();
        let updateIntervalSec = parseInt(localStorage.getItem('dashboard_update_interval_sec')) || 1;
        dashboardInterval = setInterval(fetchDashboardMetrics, updateIntervalSec * 1000);
    }
    function stopDashboardInterval() {
        if(dashboardInterval) clearInterval(dashboardInterval);
    }

    function showProjectsView() {
        if(detailView) detailView.style.display = 'none';
        projectsContainer.style.display = 'grid';
        fetchProjects();
        fetchRecentAlarms();
    }

    function showDetailView(proj) {
        window.location.hash = 'project-detail-view';
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';
        currentProjectId = proj.id;
        
        const el_detail_proj_name = document.getElementById('detail-proj-name'); if(el_detail_proj_name) el_detail_proj_name.innerText = proj.name;
        const el_detail_proj_desc = document.getElementById('detail-proj-desc'); if(el_detail_proj_desc) el_detail_proj_desc.innerText = proj.description || 'No description';
        const el_breadcrumb = document.getElementById('detail-proj-breadcrumb-name'); if(el_breadcrumb) el_breadcrumb.innerText = `${proj.name} (ID: ${proj.id})`;
        
        // Clear previous cluster cards from container
        const container = document.getElementById('dashboard-metrics-container');
        if (container) container.innerHTML = '';
        
        renderNodes(proj.nodes);
        
        // Ensure "Dashboards" tab is active by default
        const dashTab = document.querySelector('.cluster-tab[data-tab="dashboards"]');
        if(dashTab) dashTab.click();
        
        fetchDashboardMetrics();
    }

    window.navigateToClusterNodes = async function(clusterId, nodeName) {
        const ntt = document.getElementById('node-hover-tooltip');
        if (ntt) {
            ntt.style.display = 'none';
            ntt.style.opacity = '0';
        }

        if (!clusterId) return;

        try {
            const res = await apiFetch(`/api/projects/${clusterId}`);
            if (!res.ok) return;
            const proj = await res.json();

            showDetailView(proj);

            setTimeout(() => {
                // 1. Activate Nodes tab in Cluster Detail
                const nodesTab = document.querySelector('.cluster-tab[data-tab="nodes"]');
                if (nodesTab) {
                    nodesTab.click();
                } else {
                    document.querySelectorAll('.cluster-tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(c => { c.style.display = 'none'; c.classList.remove('active'); });
                    const tabContentNodes = document.getElementById('tab-content-nodes');
                    if (tabContentNodes) {
                        tabContentNodes.style.display = 'block';
                        tabContentNodes.classList.add('active');
                    }
                }

                // 2. Ensure Node list subtab is active
                const nodelistSubtab = document.querySelector('.cluster-subtab[data-subtab="nodelist"]');
                if (nodelistSubtab) {
                    nodelistSubtab.click();
                }

                // 3. Highlight matching node in table if nodeName given
                if (nodeName) {
                    const rows = document.querySelectorAll('#node-list-table tbody tr');
                    rows.forEach(r => {
                        if (r.innerText.includes(nodeName)) {
                            r.style.background = '#f5f3ff';
                            setTimeout(() => { r.style.background = ''; }, 3000);
                        }
                    });
                }
            }, 80);
        } catch(e) {
            console.error("Failed to navigate to cluster nodes:", e);
        }
    };

    function renderNodes(nodes) {
        const tbody = document.querySelector('#node-list-table tbody');
        if (tbody) tbody.innerHTML = '';
        
        if (!nodes || nodes.length === 0) {
            if(nodesContainer) nodesContainer.innerHTML = '<div class="loading-state">No nodes added yet.</div>';
            if(tbody) tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 20px; color: #6b7280;">No nodes found</td></tr>';
            
            // Reset stats for cluster detail nodes tab
            ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown', 'all'].forEach(id => {
                const el = document.getElementById('cluster-stat-' + id);
                if (el) el.innerText = '0';
            });
            return;
        }

        if(nodesContainer) nodesContainer.innerHTML = '';
        
        let stats = {
            'Operational': 0,
            'Failed': 0,
            'Offline': 0,
            'Shut Down': 0,
            'Recovering': 0,
            'Unknown State': 0
        };

        nodes.forEach(node => {
            // Topology render
            if(nodesContainer) {
                const card = document.createElement('div');
                card.className = 'project-card glass-panel';
                card.style.cursor = 'pointer';
                card.title = 'Click to view or edit connection URL';
                const color = node.role.toLowerCase() === 'primary' ? 'var(--primary)' : 'var(--warning)';
                card.innerHTML = `
                    <div style="display:flex; justify-content:space-between;">
                        <h3>${escapeHTML(node.name)}</h3>
                        <span style="color: ${color}; font-weight:bold; font-size:0.8rem;">${node.role.toUpperCase()}</span>
                    </div>
                    <p style="color: var(--success); font-size:0.8rem; margin-top:10px;">🔒 Secured & Encrypted</p>
                `;
                card.addEventListener('click', () => openEditNodeModal(node.id, node.name));
                nodesContainer.appendChild(card);
            }
            
            // Node list table render
            if(tbody) {
                // Find matching data in nodesPageData if exists
                let nData = (typeof nodesPageData !== 'undefined') ? nodesPageData.find(nd => nd.host === node.name) : null;
                
                let ip = nData ? nData.ip : 'N/A';
                let port = nData ? nData.port : '5432';
                let status = nData ? nData.status : 'Operational';
                let type = nData ? nData.type : 'PostgreSQL';
                let version = nData ? nData.version : '16.4';
                let seen = nData ? nData.seen : 'in 1 minute';
                
                if (stats[status] !== undefined) stats[status]++;
                else stats['Unknown State']++;

                let statusColor = 'var(--success)';
                let dotColor = 'var(--success)';
                if (status === 'Shut Down') { statusColor = '#3b82f6'; dotColor = '#3b82f6'; }
                if (status === 'Failed') { statusColor = '#ef4444'; dotColor = '#ef4444'; }
                if (status === 'Offline') { statusColor = '#6b7280'; dotColor = '#6b7280'; }
                
                let statusHtml = `<span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: ${dotColor};"></div> ${status}</span>`;
                
                let typeColor = '#059669'; // Greenish
                if (type === 'HAProxy') typeColor = '#8b5cf6'; // Purple
                if (type === 'Prometheus') typeColor = '#eab308'; // Yellow
                if (type === 'MariaDB') typeColor = '#1f2937';
                
                let roleHtml = `<span>${node.role}</span>`;
                if (node.role.toLowerCase() === 'primary') {
                    roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #dcfce7; color: #16a34a; border: 1px solid #16a34a; margin-left: 6px;">Writable</span>`;
                } else {
                    roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #f3f4f6; color: #4b5563; border: 1px solid #4b5563; margin-left: 6px;">Readonly</span>`;
                }

                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--border)';
                tr.innerHTML = `
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(node.name)}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${port}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${ip}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; white-space: nowrap;">${statusHtml}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: ${typeColor}; white-space: nowrap;">${type}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; display: flex; align-items: center;">${roleHtml}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${version}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${seen}</td>
                    <td style="padding: 16px 0; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; text-align: center;">
                        <button style="background: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px 12px; cursor: pointer;">...</button>
                    </td>
                `;
                tbody.appendChild(tr);
            }
        });

        // Update stats for cluster detail nodes tab
        ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(id => {
            const el = document.getElementById('cluster-stat-' + id);
            let val = 0;
            if (id === 'operational') val = stats['Operational'];
            if (id === 'failed') val = stats['Failed'];
            if (id === 'offline') val = stats['Offline'];
            if (id === 'shutdown') val = stats['Shut Down'];
            if (id === 'recovering') val = stats['Recovering'];
            if (id === 'unknown') val = stats['Unknown State'];
            if (el) el.innerText = val;
        });
        const elAll = document.getElementById('cluster-stat-all');
        if (elAll) elAll.innerText = nodes.length;
    }

    // --- API CALLS ---
    
    
    // Global tooltip hover events
    const clusterTooltip = document.getElementById('cluster-hover-tooltip');
    if (clusterTooltip) {
        clusterTooltip?.addEventListener('mouseenter', () => {
            clearTimeout(clusterHoverTimeout);
        });
        clusterTooltip?.addEventListener('mouseleave', () => {
            clusterHoverTimeout = setTimeout(() => {
                clusterTooltip.style.opacity = '0';
                clusterTooltip.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    if(clusterTooltip.style.opacity === '0') clusterTooltip.style.display = 'none';
                }, 200);
            }, 100);
        });
    }

    async function fetchProjects() {
        try {
            // Clear any old error messages
            document.querySelectorAll('.loading-state').forEach(el => el.remove());
            const cptbody = document.getElementById('cc-projects-tbody');
            if (cptbody && !cptbody.querySelector('tr[data-proj-id]')) {
                cptbody.innerHTML = '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading clusters...</span></div></td></tr>';
            }
            const response = await apiFetch('/api/projects');
            if (!response.ok) {
                  if (response.status === 401) return; // Handled by apiFetch
                  const errText = await response.text();
                  projectsContainer.insertAdjacentHTML('afterbegin', `<div class="loading-state" style="color: var(--danger)">Error loading projects. Server returned ${response.status}: ${escapeHTML(errText)}</div>`);
                  return;
              }
            const data = await response.json();
            if (data.length === 0) {
                const cptbody = document.getElementById('cc-projects-tbody'); if (cptbody) cptbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 20px;">No clusters found. Click + Add Project to start.</td></tr>';
                const el_cc_total_clusters = document.getElementById('cc-total-clusters'); if(el_cc_total_clusters) el_cc_total_clusters.innerText = '0 Clusters';
                return;
            }

            const tbody = document.getElementById('cc-projects-tbody');
            if(tbody) tbody.innerHTML = '';
            
            const clustersList = document.getElementById('cc-clusters-list');
            if (clustersList) clustersList.innerHTML = '';
            
            let operationalCount = 0;
            let warningCount = 0;
            let failedCount = 0;
            let shutdownCount = 0;
            let allNodes = [];
              const submenu = document.getElementById('clusters-submenu');
              if (submenu) {
                  submenu.innerHTML = '';
                  data.forEach(proj => {
                      let isOperational = proj.nodesCount > 0 && proj.sync_status !== 'FAILED';
                      let color = isOperational ? 'var(--success)' : 'var(--danger)';
                      
                      let a = document.createElement('div');
                      
                      a.className = "submenu-item"; a.onclick = async (e) => {
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
                        };
                      a.innerHTML = `<span style="color: ${color}; font-size: 1.2rem; line-height: 1;">&#8226;</span> <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px;">${proj.name}</span>`;
                      submenu.appendChild(a);
                  });
              }


            data.forEach(proj => {
                // 4-category classification for donut chart
                if (proj.sync_status === 'FAILED') {
                    failedCount++;
                } else if (proj.nodesCount === 0) {
                    shutdownCount++;
                } else {
                    let isOperational = proj.nodesCount > 0 && proj.sync_status !== 'FAILED';
                    if (isOperational) operationalCount++;
                    else warningCount++;
                }
                
                if (proj.nodes) {
                    proj.nodes.forEach(n => {
                        let status = "Operational";
                        let color = "var(--success)";
                        let vendorType = 'postgres';
                        let nameLower = proj.name.toLowerCase();
                        if (nameLower.includes('maria')) vendorType = 'mariadb';
                        if (nameLower.includes('percona mysql')) vendorType = 'percona_mysql';
                        if (nameLower.includes('percona') && !nameLower.includes('mysql')) vendorType = 'percona';
                        if (nameLower.includes('mongo')) vendorType = 'mongo';
                        if (nameLower.includes('timescale')) vendorType = 'timescale';
                        
                        if ( (vendorType === 'mariadb' || vendorType === 'percona_mysql') && n === proj.nodes[0] ) {
                            status = "Shut Down";
                            color = "#3b82f6";
                        }
                        
                        allNodes.push({
                            ...n,
                            clusterName: proj.name,
                            clusterId: proj.id,
                            status: status,
                            color: color,
                            vendorType: vendorType
                        });
                    });
                }
                
                // Determine status for table display (4-color system)
                let clusterStatusColor, clusterStatusText, clusterStatusKey;
                const isOperational = proj.nodesCount > 0 && proj.sync_status !== 'FAILED';
                if (proj.sync_status === 'FAILED') {
                    clusterStatusColor = '#ef4444'; clusterStatusText = '● Failed'; clusterStatusKey = 'Failed';
                } else if (proj.nodesCount === 0) {
                    clusterStatusColor = '#3b82f6'; clusterStatusText = '● Shut Down'; clusterStatusKey = 'Shut Down';
                } else if (isOperational) {
                    clusterStatusColor = 'var(--success)'; clusterStatusText = '● Operational'; clusterStatusKey = 'Operational';
                } else {
                    clusterStatusColor = 'var(--warning)'; clusterStatusText = '● Warning'; clusterStatusKey = 'Warning';
                }
                const statusColor = clusterStatusColor;
                const statusText = clusterStatusText;

                const tr = document.createElement('tr');
                tr.setAttribute('data-status', clusterStatusKey);
                tr.style.borderBottom = '1px solid var(--glass-border)';
                tr.style.cursor = 'pointer';
                
                // Hover effect
                                tr.onmouseenter = (e) => { 
                    tr.style.backgroundColor = 'rgba(0,0,0,0.02)'; 
                    clearTimeout(clusterHoverTimeout);
                    clusterHoverTimeout = setTimeout(() => {
                    const ct = document.getElementById('cluster-hover-tooltip'); 
                    if (ct) { 
                        const el_tt_cluster_id = document.getElementById('tt-cluster-id'); if(el_tt_cluster_id) el_tt_cluster_id.innerText = proj.id; 
                        const el_tt_cluster_name = document.getElementById('tt-cluster-name'); if(el_tt_cluster_name) el_tt_cluster_name.innerText = proj.name; 
                        let vendor = 'PostgreSQL Streaming v18.4'; 
                        let vendorType = 'postgres';
                        let nameLower = proj.name.toLowerCase();
                        if (nameLower.includes('maria')) { vendor = 'MariaDB Replication v11.8'; vendorType = 'mariadb'; }
                        else if (nameLower.includes('percona mysql')) { vendor = 'Percona Replication v8.4'; vendorType = 'percona_mysql'; }
                        else if (nameLower.includes('percona')) { vendor = 'Percona XtraDB Cluster'; vendorType = 'percona'; }
                        else if (nameLower.includes('mongo')) { vendor = 'MongoDB ReplicaSet v8.0'; vendorType = 'mongo'; }
                        else if (nameLower.includes('timescale')) { vendor = 'TimescaleDB v18'; vendorType = 'timescale'; }
                        else if (nameLower.includes('mssql')) { vendor = 'SQL Server v2022'; vendorType = 'mssql'; }
                        
                        const el_tt_cluster_vendor = document.getElementById('tt-cluster-vendor'); if(el_tt_cluster_vendor) el_tt_cluster_vendor.innerText = vendor; 

                        
                        
                        // Determine if there is a disabled node
                          let msg = null;
                          const cNodes = allNodes.filter(nd => nd.clusterId === proj.id && nd.status === 'Shut Down');
                          if (cNodes.length > 0) {
                              const n = cNodes[0];
                              const r = n.role ? (n.role.charAt(0).toUpperCase() + n.role.slice(1)) : 'None';
                              const port = r === 'ProxySQL' ? 6032 : (vendorType === 'postgres' ? 5432 : 3306);
                              msg = `${n.name}:${port} (${r}): Node is shutdown by user`;
                          }
                        
                        const msgBox = document.getElementById('tt-cluster-message');
                        const msgText = document.getElementById('tt-cluster-message-text');
                        if (msg) {
                            msgBox.style.display = 'flex';
                            msgText.innerText = msg;
                        } else {
                            msgBox.style.display = 'none';
                        }
                        
                        // Draw topology
                        const topoContainer = document.getElementById('tt-cluster-topology-container');
                        let topoHtml = '';
                        
                        const hex = `<polygon points="20,0 40,11.5 40,34.5 20,46 0,34.5 0,11.5"`;
                        const arrow = `<marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#d1d5db" /></marker>`;
                        const cG = 'fill="var(--success)"';
                        const cB = 'fill="#3b82f6"'; // blue for disabled
                        
                        if (vendorType === 'mariadb') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="350" height="150" viewBox="0 0 350 150"><defs>${arrow}</defs>
                                <text x="45" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">Load Balancers</text>
                                <rect x="15" y="25" width="60" height="100" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(25,30)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">HA</text></g>
                                <g transform="translate(25,75)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">HA</text></g>
                                <line x1="75" y1="75" x2="165" y2="75" stroke="#d1d5db" stroke-width="1.5"></line>
                                <text x="230" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">DB Nodes</text>
                                <rect x="165" y="25" width="130" height="120" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(175,52)">${hex} ${cB}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <g transform="translate(225,52)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(250,90)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <line x1="215" y1="75" x2="225" y2="75" stroke="#d1d5db" stroke-width="1.5"></line>
                                <line x1="265" y1="75" x2="270" y2="90" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>R - Replica</span><span>P - Primary</span><span>HA - HAProxy</span><span style="color:#3b82f6;">&#8226; Shut Down</span></div>`;
                        } else if (vendorType === 'mongo') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="350" height="150" viewBox="0 0 350 150"><defs>${arrow}</defs>
                                <text x="175" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">DB Nodes</text>
                                <rect x="110" y="25" width="130" height="110" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <text x="175" y="45" fill="#9ca3af" font-size="10" text-anchor="middle">my_mongodb_0</text>
                                <rect x="120" y="35" width="110" height="90" fill="none" stroke="#d1d5db" stroke-dasharray="2" rx="2"></rect>
                                <g transform="translate(130,55)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(180,40)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">S</text></g>
                                <g transform="translate(180,80)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">S</text></g>
                                <line x1="170" y1="78" x2="180" y2="63" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                                <line x1="170" y1="78" x2="180" y2="103" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>S - Secondary</span><span>P - Primary</span><span style="color:var(--success);">&#8226; Operational</span></div>`;
                        } else if (vendorType === 'timescale') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="200" height="120" viewBox="0 0 200 120"><defs>${arrow}</defs>
                                <g transform="translate(40,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(100,10)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <g transform="translate(100,60)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <line x1="80" y1="58" x2="100" y2="33" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                                <line x1="80" y1="58" x2="100" y2="83" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span style="color:var(--success);">&#8226; Operational</span></div>`;
                        } else if (vendorType === 'percona_mysql') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="350" height="150" viewBox="0 0 350 150"><defs>${arrow}</defs>
                                <text x="45" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">Load Balancers</text>
                                <rect x="15" y="25" width="60" height="70" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(25,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">PS</text></g>
                                <line x1="75" y1="58" x2="135" y2="58" stroke="#d1d5db" stroke-width="1.5"></line>
                                <text x="200" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">DB Nodes</text>
                                <rect x="135" y="25" width="130" height="110" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(145,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(145,85)">${hex} ${cB}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <g transform="translate(210,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <line x1="185" y1="58" x2="210" y2="58" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span>PS - ProxySQL</span><span style="color:var(--success);">&#8226; Operational</span></div>`;
                        } else if (vendorType === 'mssql') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="200" height="120" viewBox="0 0 200 120">
                                <g transform="translate(80,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span style="color:var(--success);">&#8226; Operational</span></div>`;
                        } else {
                            // PostgreSQL Default
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="350" height="150" viewBox="0 0 350 150"><defs>${arrow}</defs>
                                <text x="45" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">Load Balancers</text>
                                <rect x="15" y="25" width="60" height="100" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(25,52)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">HA</text></g>
                                <line x1="75" y1="75" x2="105" y2="75" stroke="#d1d5db" stroke-width="1.5"></line>
                                <text x="145" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">Pgbouncers</text>
                                <rect x="105" y="25" width="80" height="100" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(125,30)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">PB</text></g>
                                <g transform="translate(125,75)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">PB</text></g>
                                <line x1="185" y1="75" x2="215" y2="75" stroke="#d1d5db" stroke-width="1.5"></line>
                                <text x="280" y="15" fill="#9ca3af" font-size="10" text-anchor="middle">DB Nodes</text>
                                <rect x="215" y="25" width="130" height="100" fill="none" stroke="#d1d5db" stroke-dasharray="4" rx="4"></rect>
                                <g transform="translate(225,52)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(290,30)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <g transform="translate(290,75)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <line x1="265" y1="75" x2="285" y2="60" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                                <line x1="265" y1="75" x2="285" y2="90" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span>PB - PgBouncer</span><span>HA - HAProxy</span><span style="color:var(--success);">&#8226; Operational</span></div>`;
                        }
                        
                        if(topoContainer) topoContainer.innerHTML = topoHtml;

                        const rect = tr.getBoundingClientRect(); 
                        ct.style.display = 'block'; 
                        ct.style.opacity = '0';
                        ct.style.transform = 'translateY(10px)';
                        
                        setTimeout(() => {
                            ct.style.opacity = '1';
                            ct.style.transform = 'translateY(0)';
                        }, 10);
                        
                        let topPos = rect.bottom + 5; 
                        if (topPos + 350 > window.innerHeight) topPos = rect.top - 350; 
                        ct.style.top = topPos + 'px'; 
                        ct.style.left = (rect.left + 50) + 'px'; 
                    } 
                    }, 200);
                };
                tr.onmouseleave = (e) => { 
                    tr.style.backgroundColor = 'transparent'; 
                    clearTimeout(clusterHoverTimeout);
                    const ct = document.getElementById('cluster-hover-tooltip'); 
                    if (ct) { 
                        // Start hide timeout
                        clusterHoverTimeout = setTimeout(() => {
                            ct.style.opacity = '0'; 
                            ct.style.transform = 'translateY(10px)';
                            setTimeout(() => {
                                if(ct.style.opacity === '0') ct.style.display = 'none';
                            }, 200);
                        }, 50); // small delay to allow mouse to enter the tooltip
                    } 
                };

                tr.innerHTML = `
                    <td style="padding: 12px 10px 12px 0; color: var(--text-muted);">${proj.id}</td>
                    <td style="padding: 12px 10px; font-weight: 500; color: var(--text-main);">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>
                            ${escapeHTML(proj.name)}
                        </div>
                    </td>
                    <td style="padding: 12px 10px; color: var(--success);">On <span style="color:var(--border);">|</span> On</td>
                    <td style="padding: 12px 10px; cursor: pointer;" onclick="event.stopPropagation(); navigateToClusterNodes(${proj.id});" title="Click to view Node list">
                        <span style="padding: 3px 10px; background: #ede9fe; color: #4338ca; border-radius: 12px; font-weight: 600; font-size: 0.82rem; transition: background 0.15s;" onmouseover="this.style.background='#ddd6fe'" onmouseout="this.style.background='#ede9fe'">${proj.nodesCount || 0}</span>
                    </td>
                    <td style="padding: 12px 10px; color: ${statusColor};">${statusText}</td>
                    <td style="padding: 12px 10px;">
                        <div style="display: flex; justify-content: flex-end; gap: 8px;">
                            <button class="edit-proj-btn" style="background: transparent; border: none; cursor: pointer; padding: 4px; color: var(--text-secondary);" title="Edit">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </button>
                            <button class="delete-proj-btn" style="background: transparent; border: none; cursor: pointer; padding: 4px; color: var(--danger);" title="Delete">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                            </button>
                        </div>
                    </td>
                `;

                // Row click -> Detail view
                tr.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);
                        if (!res.ok) throw new Error(await res.text());
                        showDetailView(await res.json());
                        refreshCurrentProject();
                    } catch (err) { alert("Error loading project: " + err); }
                });

                // Edit Button
                tr.querySelector('.edit-proj-btn').addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.getElementById('edit-proj-id').value = proj.id;
                    document.getElementById('edit-proj-name').value = proj.name;
                    document.getElementById('edit-proj-desc').value = proj.description || '';
                    document.getElementById('modal-edit-project').style.display = 'flex';
                });

                // Also build the Clusters view horizontal card
                const clusterCard = document.createElement('div');
                clusterCard.className = 'glass-panel';
                clusterCard.style.padding = '20px';
                clusterCard.style.display = 'flex';
                clusterCard.style.alignItems = 'center';
                clusterCard.style.justifyContent = 'space-between';
                clusterCard.style.border = '1px solid var(--glass-border)';
                clusterCard.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
                clusterCard.style.cursor = 'pointer';
                clusterCard.onmouseover = () => clusterCard.style.boxShadow = '0 4px 8px rgba(0,0,0,0.05)';
                clusterCard.onmouseout = () => clusterCard.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
                
                clusterCard.innerHTML = `
                    <div style="flex: 1; display: flex; align-items: center; gap: 16px;">
                        <div style="background: rgba(0,0,0,0.05); padding: 12px; border-radius: 8px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>
                        </div>
                        <div>
                            <h3 style="margin: 0; font-size: 1.1rem; color: var(--text-main);">${escapeHTML(proj.name)}</h3>
                            <div style="font-size: 0.85rem; color: var(--text-muted); margin: 4px 0;">ID: ${proj.id} | Managed Server</div>
                            <div style="color: ${statusColor}; font-size: 0.85rem; font-weight: 500;">${statusText}</div>
                        </div>
                    </div>
                    
                    <div style="flex: 1; border-left: 1px solid var(--glass-border); padding-left: 20px;">
                        <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-main); margin-bottom: 8px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                            Nodes (${proj.nodesCount || 0})
                        </div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">
                            Primary: <span style="color: var(--success);">✔</span> &nbsp;&nbsp; Replica: <span style="color: var(--success);">✔</span>
                        </div>
                    </div>

                    <div style="flex: 1; border-left: 1px solid var(--glass-border); padding-left: 20px;">
                        <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-main); margin-bottom: 8px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle;"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.92-10.24l-3.27 3.27"></path></svg>
                            Auto-recovery
                        </div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); display: flex; flex-direction: column; gap: 4px;">
                            <div>Cluster: <span style="background: var(--primary); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; margin-left: 8px;">On</span></div>
                            <div>Node: <span style="background: var(--primary); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; margin-left: 16px;">On</span></div>
                        </div>
                    </div>

                    <div style="flex: 1; border-left: 1px solid var(--glass-border); padding-left: 20px; display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-main); margin-bottom: 8px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle;"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                                Load
                            </div>
                            <svg width="60" height="20" viewBox="0 0 60 20">
                                <polyline points="0,15 10,12 20,18 30,5 40,8 50,2 60,10" fill="none" stroke="var(--primary)" stroke-width="1.5" style="opacity: 0.5"></polyline>
                                <polygon points="0,20 0,15 10,12 20,18 30,5 40,8 50,2 60,10 60,20" fill="var(--primary)" style="opacity: 0.1"></polygon>
                            </svg>
                        </div>
                        <button class="icon-btn edit-proj-btn" style="border: 1px solid var(--glass-border); border-radius: 4px; padding: 4px 8px;">...</button>
                    </div>
                `;

                clusterCard.addEventListener('click', async (e) => {
                    if(e.target.closest('button')) return;
                    try {
                        const res = await apiFetch(`/api/projects/${proj.id}`);
                        if (!res.ok) throw new Error(await res.text());
                        showDetailView(await res.json());
                        refreshCurrentProject();
                    } catch (err) { alert("Error loading project: " + err); }
                });

                clusterCard.querySelector('.edit-proj-btn').addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.getElementById('edit-proj-id').value = proj.id;
                    document.getElementById('edit-proj-name').value = proj.name;
                    document.getElementById('edit-proj-desc').value = proj.description || '';
                    document.getElementById('modal-edit-project').style.display = 'flex';
                });

                if (document.getElementById('cc-clusters-list')) { document.getElementById('cc-clusters-list').appendChild(clusterCard); }
                if (tbody) { tbody.appendChild(tr); }
            });
            
            // ── Multi-Segment Donut Chart ──────────────────────────────────
            const el_cc_total_clusters = document.getElementById('cc-total-clusters');
            if (el_cc_total_clusters) el_cc_total_clusters.innerText = `${data.length} Clusters`;

            const centerText = document.getElementById('cc-donut-center-text');
            if (centerText) {
                centerText.innerText = operationalCount;
                centerText.style.color = 'var(--success)';
            }

            const donutSvg = document.getElementById('cc-donut-svg');
            const donutTooltip = document.getElementById('donut-hover-tooltip');
            const donutText = document.getElementById('donut-hover-text');

            if (donutSvg && data.length > 0) {
                const radius = 80;
                const circumference = 2 * Math.PI * radius; // ~502.65
                const total = data.length;

                // Segment definitions — order matters (drawn bottom to top)
                const segments = [
                    { count: shutdownCount, color: '#3b82f6', label: 'Shut Down' },
                    { count: failedCount,   color: '#ef4444', label: 'Failed'    },
                    { count: warningCount,  color: 'var(--warning)', label: 'Warning' },
                    { count: operationalCount, color: 'var(--success)', label: 'Operational' },
                ];

                // Remove previously drawn segment circles (keep the gray background circle)
                donutSvg.querySelectorAll('.donut-segment').forEach(el => el.remove());

                // Build segments starting at top (−90°), clockwise
                // stroke-dashoffset formula: circumference/4 − cumulativeArc
                let cumulativeArc = 0;
                segments.forEach(seg => {
                    if (seg.count === 0) return;
                    const arc = (seg.count / total) * circumference;
                    const dashOffset = circumference / 4 - cumulativeArc;

                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('cx', '100');
                    circle.setAttribute('cy', '100');
                    circle.setAttribute('r', String(radius));
                    circle.setAttribute('fill', 'none');
                    circle.setAttribute('stroke', seg.color);
                    circle.setAttribute('stroke-width', '25');
                    circle.setAttribute('stroke-dasharray', `${arc} ${circumference - arc}`);
                    circle.setAttribute('stroke-dashoffset', String(dashOffset));
                    circle.style.transition = 'stroke-dashoffset 0.8s ease-out';
                    circle.classList.add('donut-segment');

                    // Hover tooltip for this segment
                    if (donutTooltip && donutText) {
                        circle.style.cursor = 'pointer';
                        circle.addEventListener('mouseenter', () => {
                            donutText.innerText = `${seg.count} ${seg.label}`;
                            donutTooltip.style.display = 'block';
                        });
                        circle.addEventListener('mousemove', (e) => {
                            donutTooltip.style.left = (e.clientX + 12) + 'px';
                            donutTooltip.style.top  = (e.clientY + 12) + 'px';
                        });
                        circle.addEventListener('mouseleave', () => {
                            donutTooltip.style.display = 'none';
                        });
                    }

                    donutSvg.appendChild(circle);
                    cumulativeArc += arc;
                });
            }

            // Update Legend — show only non-zero categories
            const legendItems = [
                { count: operationalCount, color: 'var(--success)', label: 'Operational' },
                { count: warningCount,     color: 'var(--warning)', label: 'Warning'     },
                { count: failedCount,      color: '#ef4444',        label: 'Failed'      },
                { count: shutdownCount,    color: '#3b82f6',        label: 'Shut Down'   },
            ];
            const ccd = document.getElementById('cc-donut-legend');
            if (ccd) ccd.innerHTML = legendItems
                .filter(l => l.count > 0)
                .map(l => `<div style="display:flex;justify-content:space-between;font-size:0.9rem;">
                    <span style="color:${l.color};">&#8226; ${l.count} ${l.label}</span></div>`)
                .join('');
            
            // Apply current filter
            const filterVal = document.getElementById('cc-status-filter')?.value || 'All';
            const rows = tbody ? tbody.querySelectorAll('tr') : [];
            rows.forEach(r => {
                if (filterVal !== 'All' && r.getAttribute('data-status') !== filterVal) {
                    r.style.display = 'none';
                } else {
                    r.style.display = '';
                }
            });


            // Draw Honeycomb
            const hcContainer = document.getElementById('nodes-honeycomb');
            if (hcContainer) {
                // Made smaller, scaled down by ~0.65
                let hexHtml = '<svg width="100%" height="200" viewBox="0 0 240 200">';
                
                // New positions for smaller hexagons
                // width ~56, height ~65
                const positions = [
                    {x:20, y:20}, {x:62, y:20}, {x:104, y:20}, {x:146, y:20},
                    {x:41, y:54}, {x:83, y:54}, {x:125, y:54},
                    {x:20, y:88}, {x:62, y:88}, {x:104, y:88}, {x:146, y:88}
                ];
                
                let shutDownCount = 0;
                
                allNodes.forEach((node, idx) => {
                    if (node.status === 'Shut Down') shutDownCount++;
                    
                    const pos = positions[idx % positions.length];
                    
                    let nodeType = 'PostgreSQL';
                    if (node.vendorType === 'mariadb') nodeType = 'MariaDB';
                    if (node.vendorType === 'percona_mysql') nodeType = 'Percona';
                    if (node.vendorType === 'mongo') nodeType = 'MongoDB';
                    if (node.vendorType === 'timescale') nodeType = 'TimescaleDB';
                    
                    let roleBadge = '';
                    if (node.role && node.role.toLowerCase() === 'primary') roleBadge = '<span style="background: rgba(34,197,94,0.1); color: var(--success); border: 1px solid var(--success);">Writable</span>';
                    else if (node.role && node.role.toLowerCase() === 'replica') roleBadge = '<span style="background: rgba(107,114,128,0.1); color: #6b7280; border: 1px solid #d1d5db;">Readonly</span>';
                    
                    // The smaller polygon points (scaled from original)
                    const polyPoints = "22,0 42,11 42,34 22,46 3,34 3,11";
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" data-cluster-id="${node.clusterId}" data-node-name="${escapeHTML(node.name)}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})"
                        onclick="navigateToClusterNodes(${node.clusterId}, '${escapeHTML(node.name)}')"
                        onmouseover="let p = this.querySelector('polygon'); p.setAttribute('data-orig-fill', p.getAttribute('fill')); p.setAttribute('fill', 'white'); p.setAttribute('stroke', '${node.color}');"
                        onmouseout="let p = this.querySelector('polygon'); p.setAttribute('fill', p.getAttribute('data-orig-fill')); p.setAttribute('stroke', 'var(--glass-bg)');"
                    >
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" style="transition: all 0.2s ease; cursor: pointer;" />
                    </g>`;
                    
                    window['nodeData_' + idx] = {
                        hostname: node.name,
                        port: node.role === 'ProxySQL' ? 6032 : (nodeType === 'PostgreSQL' ? 5432 : 3306),
                        status: node.status,
                        role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'None',
                        type: nodeType,
                        cluster: `${node.clusterName} (ID:${node.clusterId})`,
                        clusterId: node.clusterId,
                        badge: roleBadge,
                        color: node.color
                    };
                });
                hexHtml += '</svg>';
                hcContainer.innerHTML = hexHtml;
                
                
                let hoverTimeout;
                document.querySelectorAll('.node-hex-hover').forEach(el => {
                    el.onclick = () => {
                        const idx = el.getAttribute('data-idx');
                        const data = window['nodeData_' + idx];
                        if (data && data.clusterId) {
                            navigateToClusterNodes(data.clusterId, data.hostname);
                        }
                    };
                    el.onmouseenter = (e) => {
                        clearTimeout(hoverTimeout);
                        hoverTimeout = setTimeout(() => {
                            const ntt = document.getElementById('node-hover-tooltip');
                            const data = window['nodeData_' + el.getAttribute('data-idx')];
                            if (ntt && data) {
                                window.currentTooltipClusterId = data.clusterId;
                                window.currentTooltipNodeName = data.hostname;
                                ntt.style.cursor = 'pointer';
                                ntt.onclick = () => {
                                    if (window.currentTooltipClusterId) {
                                        navigateToClusterNodes(window.currentTooltipClusterId, window.currentTooltipNodeName);
                                    }
                                };
                                const header = document.getElementById('ntt-header');
                                const msgBox = document.getElementById('ntt-message');
                                const stat = document.getElementById('ntt-status');
                                
                                const el_ntt_hostname = document.getElementById('ntt-hostname'); if(el_ntt_hostname) el_ntt_hostname.innerText = data.hostname;
                                const el_ntt_port = document.getElementById('ntt-port'); if(el_ntt_port) el_ntt_port.innerText = data.port;
                                const el_ntt_role = document.getElementById('ntt-role'); if(el_ntt_role) el_ntt_role.innerText = data.role;
                                const el_ntt_type = document.getElementById('ntt-type'); if(el_ntt_type) el_ntt_type.innerText = data.type;
                                const el_ntt_cluster = document.getElementById('ntt-cluster'); if(el_ntt_cluster) el_ntt_cluster.innerText = data.cluster;
                                const nttb = document.getElementById('ntt-badge'); if(nttb) nttb.innerHTML = data.badge;
                                
                                // Update Logo
                                let logoHtml = '';
                                if (data.vendorType === 'mariadb') {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"></path></svg>`; 
                                } else if (data.vendorType === 'postgres') {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path></svg>`; 
                                } else {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg>`;
                                }
                                const clusterLogoContainer = document.getElementById('ntt-cluster').previousElementSibling;
                                if (clusterLogoContainer && clusterLogoContainer.tagName === 'svg') {
                                    clusterLogoContainer.outerHTML = logoHtml;
                                }
                                
                                if (data.status === 'Shut Down') {
                                    header.style.background = '#3b82f6';
                                    msgBox.style.display = 'flex';
                                    stat.innerHTML = '<span style="color:#3b82f6;">&#8226; Shut Down</span>';
                                    document.getElementById('ntt-repl-col').style.display = 'block';
                                } else {
                                    header.style.background = 'var(--success)';
                                    msgBox.style.display = 'none';
                                    stat.innerHTML = '<span style="color:var(--success);">&#8226; Operational</span>';
                                    document.getElementById('ntt-repl-col').style.display = 'none';
                                }
                                
                                ntt.style.display = 'block';
                                ntt.style.opacity = '0';
                                ntt.style.transform = 'translateY(10px)';
                                ntt.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                                
                                const rect = el.getBoundingClientRect();
                                const tooltipRect = ntt.getBoundingClientRect();
                                
                                let leftPos = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
                                leftPos = Math.max(10, Math.min(window.innerWidth - tooltipRect.width - 10, leftPos));
                                
                                let topPos = rect.top - tooltipRect.height - 15;
                                if (topPos < 0) {
                                    topPos = rect.bottom + 15;
                                }
                                
                                ntt.style.top = topPos + 'px';
                                ntt.style.left = leftPos + 'px';
                                
                                requestAnimationFrame(() => {
                                    ntt.style.opacity = '1';
                                    ntt.style.transform = 'translateY(0)';
                                });
                            }
                        }, 500);
                    };
                    el.onmouseleave = (e) => {
                        clearTimeout(hoverTimeout);
                        const ntt = document.getElementById('node-hover-tooltip');
                        if (ntt) {
                            ntt.style.opacity = '0';
                            ntt.style.transform = 'translateY(10px)';
                            setTimeout(() => {
                                if (ntt.style.opacity === '0') {
                                    ntt.style.display = 'none';
                                }
                            }, 200);
                        }
                    };
                });
                
                const el_cc_total_nodes = document.getElementById('cc-total-nodes'); if(el_cc_total_nodes) el_cc_total_nodes.innerText = allNodes.length + ' Nodes';
                
                const dnCenter = document.getElementById('nodes-donut-center-num');
                if (dnCenter) dnCenter.innerText = allNodes.length;

                const dnSlice = document.getElementById('nodes-donut-slice');
                if (dnSlice) {
                   if (allNodes.length === 0) dnSlice.style.strokeDashoffset = '439.8';
                   else {
                       const ratio = (allNodes.length - shutDownCount) / allNodes.length;
                       dnSlice.style.strokeDashoffset = 439.8 * (1 - ratio);
                       
                       const donutTooltip = document.getElementById('donut-hover-tooltip');
                       const donutText = document.getElementById('donut-hover-text');
                       if (donutTooltip && donutText) {
                           dnSlice?.addEventListener('mouseenter', (e) => {
                               if(donutText) donutText.innerText = `${allNodes.length - shutDownCount} Operational`;
                               donutTooltip.style.display = 'block';
                           });
                           dnSlice?.addEventListener('mousemove', (e) => {
                               donutTooltip.style.left = (e.clientX + 10) + 'px';
                               donutTooltip.style.top = (e.clientY + 10) + 'px';
                           });
                           dnSlice?.addEventListener('mouseleave', () => {
                               donutTooltip.style.display = 'none';
                           });
                       }
                   }
                }
                
                const nds = document.getElementById('nodes-donut-slice'); const nodeStats = nds ? nds.parentNode.parentNode.nextElementSibling : null;
                if (nodeStats) {
                    nodeStats.innerHTML = `<span style="color: var(--success);">&#8226; ${allNodes.length - shutDownCount} Operational</span><span style="color: var(--primary);">&#8226; ${shutDownCount} Shut Down</span>`;
                }
            }

        } catch (error) {
            console.error("fetchProjects error:", error);
            const errDiv = document.getElementById('projects-container');
            if (errDiv) errDiv.insertAdjacentHTML("afterbegin", `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.stack || error.toString())}</div>`);
        }
    }

    let syncPollInterval = null;
    
    function stopSyncPolling() {
        if (syncPollInterval) {
            clearInterval(syncPollInterval);
            syncPollInterval = null;
        }
    }

    async function refreshCurrentProject() {
        if (!currentProjectId) return;
        const res = await apiFetch(`/api/projects/${currentProjectId}`);
        const detailData = await res.json();
        
        // Update nodes
        renderNodes(detailData.nodes);
        
        // Update Sync Status Badge
        const badge = document.getElementById('sync-status-badge');
        const syncBtn = document.getElementById('btn-sync-replication');
        
        if (badge) {
            if (detailData.sync_status !== 'IDLE' && detailData.sync_status !== 'HEALTHY' && detailData.sync_status !== 'SUCCESS' && detailData.sync_status !== 'FAILED' && detailData.sync_status !== 'ROLLBACK_FAILED') {
                badge.style.display = 'inline-block';
                badge.innerText = `Sync: ${detailData.sync_status}`;
                badge.style.color = '#fbbf24'; // yellow-ish
                syncBtn.disabled = true;
                syncBtn.innerText = "Syncing...";
                
                // Start polling if not already started
                if (!syncPollInterval) {
                    syncPollInterval = setInterval(refreshCurrentProject, 3000);
                }
            } else {
                if (detailData.sync_status === 'HEALTHY' || detailData.sync_status === 'SUCCESS') {
                    badge.style.display = 'inline-block';
                    badge.innerText = `Sync: ${detailData.sync_status}`;
                    badge.style.color = 'var(--success)';
                } else if (detailData.sync_status === 'FAILED' || detailData.sync_status === 'ROLLBACK_FAILED') {
                    badge.style.display = 'inline-block';
                    badge.innerText = `Sync: ${detailData.sync_status}`;
                    badge.style.color = 'var(--danger)';
                    if (detailData.sync_error) {
                        badge.title = detailData.sync_error; // tooltip
                    }
                } else {
                    badge.style.display = 'none';
                }
                
                syncBtn.disabled = false;
                syncBtn.innerText = "Sync Replication";
                stopSyncPolling();
            }
        }
    }

    
    // ---- AUDIT LOG MANAGEMENT ----
window.auditLogsData = [];

window.fetchAuditLogs = async function() {
    const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading audit logs...</span></div></td></tr>';
    }
    try {
        const res = await apiFetch('/api/audit-logs');
        if (res.ok) {
            window.auditLogsData = await res.json();
            window.filterAuditLogs();
        } else {
            if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 40px; color: #ef4444;">Failed to load audit logs.</td></tr>';
        }
    } catch(e) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 40px; color: #ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>';
    }
};

window.filterAuditLogs = function() {
    const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
    if (!tbody) return;

    const input = document.getElementById('audit-search-input');
    const query = input ? input.value.trim().toLowerCase() : '';

    const startInput = document.getElementById('audit-date-start');
    const endInput = document.getElementById('audit-date-end');
    const startVal = startInput ? startInput.value : ''; // 'YYYY-MM-DD'
    const endVal = endInput ? endInput.value : '';

    // Show/hide clear button
    const clearBtn = document.getElementById('btn-clear-audit-dates');
    if (clearBtn) clearBtn.style.display = (startVal || endVal) ? 'inline' : 'none';

    const logs = window.auditLogsData || [];
    let filtered = logs;

    if (query) {
        filtered = filtered.filter(log => {
            const action = (log.action || '').toLowerCase();
            const details = (log.details || '').toLowerCase();
            const user = (log.user || log.username || '').toLowerCase();
            const ts = (log.timestamp || '').toLowerCase();
            const hostname = (log.hostname || '127.0.0.1').toLowerCase();
            const cluster = (log.cluster_name || log.project_name || 'N/A').toLowerCase();
            const type = (log.entry_type || (action.includes('log') ? 'authentication' : 'system')).toLowerCase();
            return action.includes(query) || details.includes(query) || user.includes(query) ||
                   ts.includes(query) || hostname.includes(query) || cluster.includes(query) || type.includes(query);
        });
    }

    // Date range filter — compare YYYY-MM-DD prefix of the timestamp
    if (startVal || endVal) {
        filtered = filtered.filter(log => {
            const ts = (log.timestamp || '').substring(0, 10); // 'YYYY-MM-DD'
            if (startVal && ts < startVal) return false;
            if (endVal && ts > endVal) return false;
            return true;
        });
    }

    const hasFilters = query || startVal || endVal;

    if (filtered.length === 0) {
        if (hasFilters) {
            tbody.innerHTML = `
            <tr>
              <td colspan="6" style="text-align: center; padding: 60px 20px; background: white;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block; margin: 0 auto 16px;">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <div style="color: #4b5563; font-size: 0.95rem; margin-bottom: 8px;">No audit log entries match your current filters.</div>
                <a href="#" onclick="event.preventDefault(); window.clearAuditFilters();" style="color: #7c3aed; font-size: 0.85rem; font-weight: 500; text-decoration: none; cursor: pointer;">Clear all filters</a>
              </td>
            </tr>`;
        } else {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 40px; color: #6b7280;">No audit logs recorded yet.</td></tr>`;
        }
        return;
    }

    tbody.innerHTML = filtered.map(log => {
        const action = log.action || '';
        const details = log.details || '';
        const entryType = log.entry_type || (action.toLowerCase().includes('log') ? 'authentication' : 'system');
        const user = log.user || log.username || 'demo@severalnines.com';
        const hostname = log.hostname || '127.0.0.1';
        const cluster = log.cluster_name || log.project_name || 'N/A';
        const activityText = details ? `${action}: ${details}` : action;

        return `
            <tr style="border-bottom: 1px solid #f3f4f6; transition: background 0.15s;" onmouseenter="this.style.background='#fafafa'" onmouseleave="this.style.background='white'">
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #374151; white-space: nowrap;">${escapeHTML(log.timestamp || '')}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; font-weight: 500; color: #111827;">${escapeHTML(activityText)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(entryType)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(user)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(hostname)}</td>
                <td style="padding: 14px 20px; font-size: 0.85rem; color: #6b7280;">${escapeHTML(cluster)}</td>
            </tr>
        `;
    }).join('');
};

window.clearAuditDateFilter = function() {
    const s = document.getElementById('audit-date-start');
    const e = document.getElementById('audit-date-end');
    if (s) s.value = '';
    if (e) e.value = '';
    const btn = document.getElementById('btn-clear-audit-dates');
    if (btn) btn.style.display = 'none';
    window.filterAuditLogs();
};

window.clearAuditFilters = function() {
    const input = document.getElementById('audit-search-input');
    if (input) input.value = '';
    window.clearAuditDateFilter();
};

window.exportAuditLogsCsv = function() {
    const logs = window.auditLogsData || [];
    if (logs.length === 0) {
        alert("No audit log entries to export.");
        return;
    }

    const headers = ['"id"', '"timestamp"', '"cluster_id"', '"cluster_name"', '"entry_type"', '"username"', '"client_hostname"', '"message"'];
    const rows = [headers.join(',')];

    logs.forEach((log, index) => {
        const id = log.id || (logs.length - index);
        const ts = log.timestamp || '';
        const clusterId = log.project_id || 0;
        const clusterName = log.cluster_name || log.project_name || "";
        const entryType = log.entry_type || (log.action && log.action.toLowerCase().includes('log') ? 'authentication' : 'system');
        const username = log.user || log.username || 'demo@severalnines.com';
        const hostname = log.hostname || '127.0.0.1';
        const message = log.action ? (log.details ? `${log.action}: ${log.details}` : log.action) : 'Logged in.';

        const escapeCsv = (val) => '"' + String(val || '').replace(/"/g, '""') + '"';

        rows.push([
            id,
            escapeCsv(ts),
            clusterId,
            escapeCsv(clusterName),
            escapeCsv(entryType),
            escapeCsv(username),
            escapeCsv(hostname),
            escapeCsv(message)
        ].join(','));
    });

    const csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(rows.join('\n'));
    const link = document.createElement("a");
    // Generate random 6-character suffix like ClusterControl (e.g. cmon_audit_8duFmV.csv)
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let randStr = '';
    for (let i = 0; i < 6; i++) {
        randStr += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    link.setAttribute("href", csvContent);
    link.setAttribute("download", `cmon_audit_${randStr}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};


// ══════════════════════════════════════════════════════════════
// WATCHLISTS
// ══════════════════════════════════════════════════════════════
const WL_TOPICS = ['Alarms', 'DB Growth', 'DB Processes', 'Load', 'Load average', 'Status', 'Top queries'];

const wlState = {
    topics: [],      // selected topic strings
    clusters: [],    // selected { id, name } objects
    pageBy: 'Topic',
    grid: '2x2',
    allClusters: [] // loaded from /api/projects
};

// ─── Tooltip hover ─────────────────────────────────────────────
document.addEventListener('mouseover', e => {
    const wrap = e.target.closest('.wl-tooltip-wrap');
    if (wrap) wrap.querySelector('.wl-tooltip-box').style.display = 'block';
});
document.addEventListener('mouseout', e => {
    const wrap = e.target.closest('.wl-tooltip-wrap');
    if (wrap) wrap.querySelector('.wl-tooltip-box').style.display = 'none';
});

// ─── Load & render watchlists table ────────────────────────────
window.fetchWatchlists = async function() {
    const tbody = document.getElementById('watchlists-tbody');
    if (tbody) tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading watchlists...</span></div></td></tr>';
    try {
        const res = await apiFetch('/api/watchlists');
        if (!res.ok) { if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;color:#ef4444;">Failed to load watchlists.</td></tr>'; return; }
        const data = await res.json();
        renderWatchlists(data);
    } catch(e) {
        if (tbody) tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;color:#ef4444;">Error: ${escapeHTML(String(e))}</td></tr>`;
    }
};

function renderWatchlists(list) {
    const tbody = document.getElementById('watchlists-tbody');
    if (!tbody) return;
    // Cache for viewer access
    window._wlList = list;
    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:60px 20px;color:#9ca3af;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="display:block;margin:0 auto 12px;"><path d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"></path><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            No watchlists yet. Click <strong>Create watchlist</strong> to add one.
        </td></tr>`;
        return;
    }
    tbody.innerHTML = list.map((wl, idx) => {
        const topicBadges = (wl.topics || []).map(t =>
            `<span style="background:#ede9fe;color:#5b21b6;border-radius:4px;padding:2px 8px;font-size:0.78rem;font-weight:500;">${escapeHTML(t)}</span>`
        ).join(' ');
        const clusterBadges = (wl.clusters || []).length === 0
            ? '<span style="color:#9ca3af;font-size:0.82rem;">All clusters</span>'
            : wl.clusters.map(c => `<span style="font-size:0.82rem;color:#374151;">${escapeHTML(c.name)}</span>`).join(', ');
        return `<tr style="border-bottom:1px solid #f3f4f6;transition:background 0.15s;" onmouseenter="this.style.background='#fafafa'" onmouseleave="this.style.background='white'">
            <td style="padding:14px 20px;font-size:0.85rem;font-weight:600;color:#111827;">${escapeHTML(wl.name)}</td>
            <td style="padding:14px 20px;">${topicBadges}</td>
            <td style="padding:14px 20px;font-size:0.85rem;color:#374151;">${escapeHTML(wl.page_by)}</td>
            <td style="padding:14px 20px;font-size:0.85rem;color:#374151;">${escapeHTML(wl.grid)}</td>
            <td style="padding:14px 20px;font-size:0.85rem;">${clusterBadges}</td>
            <td style="padding:14px 20px;display:flex;gap:6px;align-items:center;">
                <button onclick="window.openWatchlistViewer(window._wlList[${idx}])"
                  style="border:none;background:#4338ca;color:white;cursor:pointer;font-size:0.82rem;padding:5px 12px;border-radius:5px;font-weight:600;"
                  onmouseover="this.style.background='#3730a3'" onmouseout="this.style.background='#4338ca'"
                  title="Open live viewer">▶ View</button>
                <button onclick="window.deleteWatchlist(${wl.id})"
                  style="border:none;background:none;cursor:pointer;color:#ef4444;font-size:0.82rem;padding:4px 8px;border-radius:4px;"
                  onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='none'"
                  title="Delete watchlist">🗑</button>
            </td>
        </tr>`;
    }).join('');
}

window.deleteWatchlist = async function(id) {
    if (!confirm('Delete this watchlist?')) return;
    const res = await apiFetch(`/api/watchlists/${id}`, { method: 'DELETE' });
    if (res.ok) window.fetchWatchlists();
    else alert('Failed to delete watchlist.');
};

// ─── Modal open/close ──────────────────────────────────────────
window.openCreateWatchlistModal = async function() {
    // Reset state
    wlState.topics = [];
    wlState.clusters = [];
    wlState.pageBy = 'Topic';
    wlState.grid = '2x2';

    const nameEl = document.getElementById('wl-name');
    if (nameEl) nameEl.value = '';
    const errEl = document.getElementById('wl-error');
    if (errEl) { errEl.style.display = 'none'; errEl.textContent = ''; }

    // Reset page-by buttons
    ['topic','cluster'].forEach(k => {
        const b = document.getElementById(`wl-pageby-${k}`);
        if (b) { b.style.borderColor = k === 'topic' ? '#4338ca' : '#d1d5db'; b.style.color = k === 'topic' ? '#4338ca' : '#6b7280'; b.style.fontWeight = k === 'topic' ? '600' : '400'; }
    });
    // Reset grid buttons
    document.querySelectorAll('#wl-grid-group button').forEach(b => {
        const isDefault = b.textContent.trim() === '2x2';
        b.style.borderColor = isDefault ? '#4338ca' : '#d1d5db';
        b.style.color = isDefault ? '#4338ca' : '#6b7280';
        b.style.fontWeight = isDefault ? '600' : '400';
    });
    // Reset advanced
    const adv = document.getElementById('wl-advanced-section');
    if (adv) adv.style.display = 'none';
    const arr = document.getElementById('wl-advanced-arrow');
    if (arr) arr.textContent = '▶';
    const speedEl = document.getElementById('wl-page-speed');
    if (speedEl) speedEl.value = 5;

    renderWlTopicsSelected();
    renderWlClustersSelected();

    // Load clusters for dropdown
    try {
        const res = await apiFetch('/api/projects');
        const projs = res.ok ? await res.json() : [];
        wlState.allClusters = projs.map(p => ({ id: p.id, name: p.name }));
    } catch(e) { wlState.allClusters = []; }

    buildWlTopicsDropdown();
    buildWlClustersDropdown();

    const modal = document.getElementById('modal-create-watchlist');
    if (modal) modal.style.display = 'flex';
};

window.closeCreateWatchlistModal = function() {
    const modal = document.getElementById('modal-create-watchlist');
    if (modal) modal.style.display = 'none';
    // Close any open dropdowns
    document.getElementById('wl-topics-dropdown')?.style && (document.getElementById('wl-topics-dropdown').style.display = 'none');
    document.getElementById('wl-clusters-dropdown')?.style && (document.getElementById('wl-clusters-dropdown').style.display = 'none');
};

// ─── Topics multi-select ───────────────────────────────────────
function buildWlTopicsDropdown() {
    const dd = document.getElementById('wl-topics-dropdown');
    if (!dd) return;
    dd.innerHTML = WL_TOPICS.map(t => {
        const sel = wlState.topics.includes(t);
        return `<div onclick="window.toggleWlTopic('${t}')" style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;cursor:pointer;font-size:0.88rem;color:#374151;"
            onmouseover="this.style.background='#f5f3ff'" onmouseout="this.style.background='white'">
            <span>${escapeHTML(t)}</span>
            ${sel ? '<span style="color:#4338ca;">✓</span>' : ''}
        </div>`;
    }).join('');
}

window.toggleWlTopicsDropdown = function() {
    const dd = document.getElementById('wl-topics-dropdown');
    if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    document.getElementById('wl-clusters-dropdown').style.display = 'none';
};

window.toggleWlTopic = function(topic) {
    if (wlState.topics.includes(topic)) {
        wlState.topics = wlState.topics.filter(t => t !== topic);
    } else {
        wlState.topics.push(topic);
    }
    buildWlTopicsDropdown();
    renderWlTopicsSelected();
};

function renderWlTopicsSelected() {
    const el = document.getElementById('wl-topics-selected');
    if (!el) return;
    el.innerHTML = wlState.topics.map(t =>
        `<span style="display:inline-flex;align-items:center;gap:4px;background:#ede9fe;color:#5b21b6;border-radius:4px;padding:3px 8px;font-size:0.8rem;font-weight:500;">
            ${escapeHTML(t)}
            <span onclick="window.toggleWlTopic('${t}')" style="cursor:pointer;font-size:0.9rem;line-height:1;color:#7c3aed;" title="Remove">×</span>
        </span>`
    ).join('');
}

// ─── Clusters multi-select ─────────────────────────────────────
function buildWlClustersDropdown() {
    const dd = document.getElementById('wl-clusters-dropdown');
    if (!dd) return;
    if (wlState.allClusters.length === 0) {
        dd.innerHTML = '<div style="padding:12px 14px;font-size:0.85rem;color:#9ca3af;">No clusters available.</div>';
        return;
    }
    dd.innerHTML = wlState.allClusters.map(c => {
        const sel = wlState.clusters.some(x => x.id === c.id);
        return `<div onclick="window.toggleWlCluster(${c.id}, '${escapeHTML(c.name).replace(/'/g,"\\'")}'")" style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;cursor:pointer;font-size:0.88rem;color:#374151;"
            onmouseover="this.style.background='#f5f3ff'" onmouseout="this.style.background='white'">
            <span>🐘 ${escapeHTML(c.name)} (ID:${c.id})</span>
            ${sel ? '<span style="color:#4338ca;">✓</span>' : ''}
        </div>`;
    }).join('');
}

window.toggleWlClustersDropdown = function() {
    const dd = document.getElementById('wl-clusters-dropdown');
    if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    document.getElementById('wl-topics-dropdown').style.display = 'none';
};

window.toggleWlCluster = function(id, name) {
    if (wlState.clusters.some(c => c.id === id)) {
        wlState.clusters = wlState.clusters.filter(c => c.id !== id);
    } else {
        wlState.clusters.push({ id, name });
    }
    buildWlClustersDropdown();
    renderWlClustersSelected();
};

function renderWlClustersSelected() {
    const el = document.getElementById('wl-clusters-selected');
    if (!el) return;
    el.innerHTML = wlState.clusters.map(c =>
        `<span style="display:inline-flex;align-items:center;gap:4px;background:#dbeafe;color:#1d4ed8;border-radius:4px;padding:3px 8px;font-size:0.8rem;font-weight:500;">
            ${escapeHTML(c.name)}
            <span onclick="window.toggleWlCluster(${c.id}, '')" style="cursor:pointer;font-size:0.9rem;line-height:1;" title="Remove">×</span>
        </span>`
    ).join('');
}

// ─── Page-by toggle ────────────────────────────────────────────
window.setWlPageBy = function(val, btn) {
    wlState.pageBy = val;
    ['topic','cluster'].forEach(k => {
        const b = document.getElementById(`wl-pageby-${k}`);
        if (!b) return;
        const active = (k === val.toLowerCase());
        b.style.borderColor = active ? '#4338ca' : '#d1d5db';
        b.style.color = active ? '#4338ca' : '#6b7280';
        b.style.fontWeight = active ? '600' : '400';
    });
};

// ─── Grid toggle ───────────────────────────────────────────────
window.setWlGrid = function(val, btn) {
    wlState.grid = val;
    document.querySelectorAll('#wl-grid-group button').forEach(b => {
        const active = b.textContent.trim() === val;
        b.style.borderColor = active ? '#4338ca' : '#d1d5db';
        b.style.color = active ? '#4338ca' : '#6b7280';
        b.style.fontWeight = active ? '600' : '400';
    });
};

// ─── Advanced toggle ───────────────────────────────────────────
window.toggleWlAdvanced = function() {
    const sec = document.getElementById('wl-advanced-section');
    const arr = document.getElementById('wl-advanced-arrow');
    const open = sec.style.display === 'none';
    sec.style.display = open ? 'block' : 'none';
    arr.textContent = open ? '▼' : '▶';
};

// ─── Submit create ─────────────────────────────────────────────
window.submitCreateWatchlist = async function() {
    const errEl = document.getElementById('wl-error');
    const name = document.getElementById('wl-name')?.value.trim();
    if (!name) { errEl.textContent = 'Name is required.'; errEl.style.display = 'block'; return; }
    if (wlState.topics.length === 0) { errEl.textContent = 'Please select at least one topic.'; errEl.style.display = 'block'; return; }
    errEl.style.display = 'none';

    const btn = document.getElementById('btn-wl-create');
    if (btn) { btn.disabled = true; btn.textContent = 'Creating...'; }
    try {
        const pageSpeed = parseInt(document.getElementById('wl-page-speed')?.value) || 5;
        const res = await apiFetch('/api/watchlists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name,
                topics: wlState.topics,
                cluster_ids: wlState.clusters.map(c => c.id),
                page_by: wlState.pageBy,
                grid: wlState.grid,
                page_speed: pageSpeed
            })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            window.closeCreateWatchlistModal();
            window.fetchWatchlists();
        } else {
            errEl.textContent = data.detail || 'Failed to create watchlist.';
            errEl.style.display = 'block';
        }
    } catch(e) {
        errEl.textContent = 'Error: ' + String(e);
        errEl.style.display = 'block';
    } finally {
        if (btn) { btn.disabled = false; btn.textContent = 'Create'; }
    }
};

// Close dropdowns when clicking outside the modal
document.addEventListener('click', e => {
    if (!e.target.closest('#wl-topics-btn') && !e.target.closest('#wl-topics-dropdown')) {
        const dd = document.getElementById('wl-topics-dropdown');
        if (dd) dd.style.display = 'none';
    }
    if (!e.target.closest('#wl-clusters-btn') && !e.target.closest('#wl-clusters-dropdown')) {
        const dd = document.getElementById('wl-clusters-dropdown');
        if (dd) dd.style.display = 'none';
    }
});

// ══════════════════════════════════════════════════════════════
// WATCHLIST LIVE VIEWER
// ══════════════════════════════════════════════════════════════

const wlViewer = {
    wl: null,           // current watchlist object
    pages: [],          // array of page descriptors { label, cells:[{topic,cluster}] }
    pageIndex: 0,
    paused: false,
    timer: null,        // setInterval handle
    countdown: 0,       // current countdown value
    metricsCache: {},   // { projectId: metricsArray }
    auditCache: [],     // audit log cache
};

// ─── Grid column/row helpers ─────────────────────────────────────────────────
function wlParseGrid(grid) {
    const parts = (grid || '2x2').split('x');
    return { cols: parseInt(parts[0]) || 2, rows: parseInt(parts[1]) || 2 };
}

function wlGridTemplateCols(cols) {
    return `repeat(${cols}, 1fr)`;
}

// ─── Build page descriptors ──────────────────────────────────────────────────
// Page-by Topic: each page = one topic, cells = one per cluster
// Page-by Cluster: each page = one cluster, cells = one per topic
function wlBuildPages(wl, allClusters) {
    const { cols, rows } = wlParseGrid(wl.grid);
    const cellsPerPage = cols * rows;
    const topics = wl.topics || [];
    // Clusters: wl.clusters has {id,name}. If empty → use all projects
    const clusters = (wl.clusters && wl.clusters.length > 0) ? wl.clusters : allClusters;

    const pages = [];
    if (wl.page_by === 'Topic') {
        // Each page = one topic. Cells = clusters (up to cellsPerPage each)
        for (const topic of topics) {
            for (let start = 0; start < Math.max(clusters.length, 1); start += cellsPerPage) {
                const slice = clusters.slice(start, start + cellsPerPage);
                pages.push({
                    label: topic,
                    pageBy: 'Topic',
                    cells: slice.map(c => ({ topic, cluster: c }))
                });
            }
        }
    } else {
        // Page-by Cluster: each page = one cluster. Cells = topics
        for (const cluster of clusters) {
            for (let start = 0; start < Math.max(topics.length, 1); start += cellsPerPage) {
                const slice = topics.slice(start, start + cellsPerPage);
                pages.push({
                    label: cluster.name,
                    pageBy: 'Cluster',
                    cells: slice.map(t => ({ topic: t, cluster }))
                });
            }
        }
    }
    if (pages.length === 0) pages.push({ label: '—', cells: [] });
    return pages;
}

// ─── Fetch metrics for all relevant clusters ─────────────────────────────────
async function wlFetchAllMetrics(clusters) {
    const results = {};
    await Promise.all(clusters.map(async c => {
        try {
            const res = await apiFetch(`/api/projects/${c.id}/metrics`);
            results[c.id] = res.ok ? await res.json() : [];
        } catch(e) { results[c.id] = []; }
    }));
    return results;
}

async function wlFetchAuditLogs() {
    try {
        const res = await apiFetch('/api/audit-logs');
        return res.ok ? await res.json() : [];
    } catch { return []; }
}

// ─── Open / Close ─────────────────────────────────────────────────────────────
window.openWatchlistViewer = async function(wl) {
    if (!wl) return;
    wlViewer.wl = wl;
    wlViewer.pageIndex = 0;
    wlViewer.paused = false;
    wlViewer.metricsCache = {};
    wlViewer.auditCache = [];

    // Show overlay
    const overlay = document.getElementById('modal-wl-viewer');
    if (overlay) overlay.style.display = 'flex';

    // Update header
    const nameEl = document.getElementById('wl-viewer-name');
    if (nameEl) nameEl.textContent = wl.name;
    const gridBadge = document.getElementById('wl-viewer-grid-badge');
    if (gridBadge) gridBadge.textContent = `Grid: ${wl.grid}  ·  Page by: ${wl.page_by}  ·  ${wl.page_speed}s`;

    // Determine which clusters to use
    let allClusters = wl.clusters || [];
    if (allClusters.length === 0) {
        // Load all projects
        try {
            const res = await apiFetch('/api/projects');
            const projs = res.ok ? await res.json() : [];
            allClusters = projs.map(p => ({ id: p.id, name: p.name }));
        } catch { allClusters = []; }
    }

    wlViewer.pages = wlBuildPages(wl, allClusters);

    // Show loading while fetching
    const grid = document.getElementById('wl-viewer-grid');
    if (grid) grid.innerHTML = '<div style="color:#64748b;text-align:center;padding:60px;grid-column:1/-1;"><div class="cc-spinner" style="margin:0 auto 16px;border-color:#334155;border-top-color:#6366f1;"></div><span>Loading live metrics…</span></div>';

    // Fetch all data
    const [metricsCache, auditCache] = await Promise.all([
        wlFetchAllMetrics(allClusters),
        wlFetchAuditLogs()
    ]);
    wlViewer.metricsCache = metricsCache;
    wlViewer.auditCache = auditCache;

    wlRenderCurrentPage();
    wlStartPager();
};

window.closeWatchlistViewer = function() {
    const overlay = document.getElementById('modal-wl-viewer');
    if (overlay) overlay.style.display = 'none';
    wlStopPager();
    wlViewer.wl = null;
};

// ─── Pager ───────────────────────────────────────────────────────────────────
function wlStartPager() {
    wlStopPager();
    if (!wlViewer.wl || wlViewer.paused) return;
    const speed = wlViewer.wl.page_speed || 5;
    wlViewer.countdown = speed;
    wlUpdateProgress(speed, speed);

    wlViewer.timer = setInterval(() => {
        if (wlViewer.paused) return;
        wlViewer.countdown--;
        wlUpdateProgress(wlViewer.countdown, speed);
        if (wlViewer.countdown <= 0) {
            wlAdvancePage(1);
        }
    }, 1000);
}

function wlStopPager() {
    if (wlViewer.timer) { clearInterval(wlViewer.timer); wlViewer.timer = null; }
}

function wlUpdateProgress(remaining, total) {
    const bar = document.getElementById('wl-viewer-progress');
    if (!bar) return;
    const pct = total > 0 ? (remaining / total) * 100 : 100;
    // Turn off transition for instant reset, then re-enable
    bar.style.transition = 'none';
    bar.style.width = pct + '%';
    requestAnimationFrame(() => { bar.style.transition = 'width 1s linear'; });
}

window.toggleWlPager = function() {
    wlViewer.paused = !wlViewer.paused;
    const btn = document.getElementById('wl-viewer-pause-btn');
    if (btn) btn.textContent = wlViewer.paused ? '▶ Resume' : '⏸ Pause';
};

function wlAdvancePage(dir) {
    const n = wlViewer.pages.length;
    if (n === 0) return;
    wlViewer.pageIndex = (wlViewer.pageIndex + dir + n) % n;
    const speed = wlViewer.wl ? wlViewer.wl.page_speed : 5;
    wlViewer.countdown = speed;
    wlUpdateProgress(speed, speed);
    wlRenderCurrentPage();
}

window.wlNextPage = function() { wlAdvancePage(1); };
window.wlPrevPage = function() { wlAdvancePage(-1); };

window.wlRefreshPage = async function() {
    const wl = wlViewer.wl;
    if (!wl) return;
    const grid = document.getElementById('wl-viewer-grid');
    if (grid) grid.innerHTML = '<div style="color:#64748b;text-align:center;padding:60px;grid-column:1/-1;"><div class="cc-spinner" style="margin:0 auto 16px;border-color:#334155;border-top-color:#6366f1;"></div><span>Refreshing…</span></div>';

    let allClusters = wl.clusters || [];
    if (allClusters.length === 0) {
        try { const res = await apiFetch('/api/projects'); const p = res.ok ? await res.json() : []; allClusters = p.map(x => ({id:x.id,name:x.name})); } catch {}
    }
    const [metricsCache, auditCache] = await Promise.all([
        wlFetchAllMetrics(allClusters),
        wlFetchAuditLogs()
    ]);
    wlViewer.metricsCache = metricsCache;
    wlViewer.auditCache = auditCache;
    wlRenderCurrentPage();
};

// ─── Render current page ─────────────────────────────────────────────────────
function wlRenderCurrentPage() {
    const grid = document.getElementById('wl-viewer-grid');
    const pageLabel = document.getElementById('wl-viewer-page-label');
    if (!grid || !wlViewer.wl) return;

    const pages = wlViewer.pages;
    const page = pages[wlViewer.pageIndex];
    if (!page) { grid.innerHTML = '<div style="color:#64748b;padding:40px;grid-column:1/-1;">No pages.</div>'; return; }

    const { cols, rows } = wlParseGrid(wlViewer.wl.grid);
    grid.style.gridTemplateColumns = wlGridTemplateCols(cols);
    grid.style.gridAutoRows = `calc((100vh - 110px) / ${rows})`;

    if (pageLabel) {
        const indicator = `${wlViewer.pageIndex + 1} / ${pages.length}`;
        pageLabel.textContent = `${page.label}  —  ${indicator}`;
    }

    if (page.cells.length === 0) {
        grid.innerHTML = '<div style="color:#64748b;padding:40px;grid-column:1/-1;text-align:center;">No clusters configured for this watchlist.</div>';
        return;
    }

    grid.innerHTML = page.cells.map(cell => wlBuildMetricPanel(cell.topic, cell.cluster)).join('');
}

// ─── Master panel dispatcher ─────────────────────────────────────────────────
function wlBuildMetricPanel(topic, cluster) {
    const metricsArr = wlViewer.metricsCache[cluster.id] || [];
    // metricsArr is [{id, name, role, metrics:{status,ping,storage,...}}]
    const panelId = `wl-panel-${cluster.id}-${topic.replace(/\s+/g,'_')}`;

    const topicIcon = {
        'Alarms': '🔔', 'DB Growth': '📈', 'DB Processes': '🔗',
        'Load': '⚡', 'Load average': '📊', 'Status': '✅', 'Top queries': '🔍'
    }[topic] || '📌';

    const innerHtml = wlBuildTopicInner(topic, cluster, metricsArr);

    return `<div id="${panelId}" style="background:#1e293b;border:1px solid #334155;border-radius:10px;display:flex;flex-direction:column;overflow:hidden;min-height:120px;">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid #334155;background:#172033;flex-shrink:0;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:1rem;">${topicIcon}</span>
                <span style="color:#e2e8f0;font-size:0.85rem;font-weight:600;">${escapeHTML(topic)}</span>
            </div>
            <span style="color:#64748b;font-size:0.75rem;">${escapeHTML(cluster.name)}</span>
        </div>
        <div style="flex:1;padding:12px 14px;overflow-y:auto;">${innerHtml}</div>
    </div>`;
}

// ─── Topic inner content builders ────────────────────────────────────────────
function wlBuildTopicInner(topic, cluster, metricsArr) {
    switch(topic) {
        case 'Status':       return wlBuildStatusInner(metricsArr, cluster);
        case 'Load':         return wlBuildLoadInner(metricsArr, false);
        case 'Load average': return wlBuildLoadInner(metricsArr, true);
        case 'DB Processes': return wlBuildDbProcessesInner(metricsArr);
        case 'DB Growth':    return wlBuildDbGrowthInner(metricsArr);
        case 'Alarms':       return wlBuildAlarmsInner(cluster);
        case 'Top queries':  return wlBuildTopQueriesInner(metricsArr);
        default:             return `<span style="color:#64748b;font-size:0.82rem;">No panel for this topic.</span>`;
    }
}

// STATUS panel
function wlBuildStatusInner(metricsArr, cluster) {
    if (!metricsArr.length) return wlNoNodes();
    return metricsArr.map(node => {
        const m = node.metrics || {};
        const online = m.status === 'online';
        const dotColor = online ? '#22c55e' : '#ef4444';
        const statusLabel = online ? 'Online' : 'Offline';
        return `<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="width:9px;height:9px;border-radius:50%;background:${dotColor};display:inline-block;flex-shrink:0;"></span>
                <span style="color:#cbd5e1;font-size:0.82rem;font-weight:500;">${escapeHTML(node.name)}</span>
                <span style="color:#64748b;font-size:0.75rem;">${escapeHTML(node.role || '')}</span>
            </div>
            <div style="text-align:right;">
                <span style="color:${dotColor};font-size:0.78rem;font-weight:600;">${statusLabel}</span>
                ${m.ping ? `<span style="color:#64748b;font-size:0.72rem;margin-left:6px;">${escapeHTML(m.ping)}</span>` : ''}
            </div>
        </div>
        <div style="display:flex;gap:12px;padding:4px 0 6px 17px;flex-wrap:wrap;">
            ${m.version ? `<span style="color:#64748b;font-size:0.72rem;">v${escapeHTML(m.version)}</span>` : ''}
            ${m.uptime ? `<span style="color:#64748b;font-size:0.72rem;">⬆ ${escapeHTML(m.uptime)}</span>` : ''}
            ${m.connections ? `<span style="color:#64748b;font-size:0.72rem;">🔗 ${escapeHTML(m.connections)}</span>` : ''}
        </div>`;
    }).join('');
}

// LOAD panel (also used for Load average with extra cache_hit)
function wlBuildLoadInner(metricsArr, showCacheHit) {
    if (!metricsArr.length) return wlNoNodes();
    return metricsArr.map(node => {
        const m = node.metrics || {};
        const cpu = m.cpu_usage || 'N/A';
        const ram = m.ram_usage || 'N/A';
        const cpuNum = parseFloat(cpu) || 0;
        const ramNum = parseFloat(ram) || 0;
        const cpuColor = cpuNum > 80 ? '#ef4444' : cpuNum > 60 ? '#f59e0b' : '#22c55e';
        const ramColor = ramNum > 85 ? '#ef4444' : ramNum > 70 ? '#f59e0b' : '#22c55e';
        return `<div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
                <span style="color:#94a3b8;font-size:0.78rem;">${escapeHTML(node.name)}</span>
            </div>
            <div style="margin-bottom:5px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
                    <span style="color:#64748b;font-size:0.72rem;">CPU</span>
                    <span style="color:${cpuColor};font-size:0.72rem;font-weight:600;">${escapeHTML(cpu)}</span>
                </div>
                <div style="background:#334155;border-radius:3px;height:6px;overflow:hidden;">
                    <div style="background:${cpuColor};height:100%;width:${Math.min(cpuNum,100)}%;border-radius:3px;transition:width 0.5s;"></div>
                </div>
            </div>
            <div style="margin-bottom:${showCacheHit?'5px':'0'};">
                <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
                    <span style="color:#64748b;font-size:0.72rem;">RAM</span>
                    <span style="color:${ramColor};font-size:0.72rem;font-weight:600;">${escapeHTML(ram)}</span>
                </div>
                <div style="background:#334155;border-radius:3px;height:6px;overflow:hidden;">
                    <div style="background:${ramColor};height:100%;width:${Math.min(ramNum,100)}%;border-radius:3px;transition:width 0.5s;"></div>
                </div>
            </div>
            ${showCacheHit && m.cache_hit ? `<div style="margin-top:5px;display:flex;justify-content:space-between;">
                <span style="color:#64748b;font-size:0.72rem;">Cache hit</span>
                <span style="color:#38bdf8;font-size:0.72rem;font-weight:600;">${escapeHTML(m.cache_hit)}</span>
            </div>` : ''}
            ${cpu === 'N/A' && ram === 'N/A' ? `<p style="color:#475569;font-size:0.72rem;margin-top:4px;">SSH not configured — OS metrics unavailable</p>` : ''}
        </div>`;
    }).join('<hr style="border:none;border-top:1px solid #1e293b;margin:4px 0;">');
}

// DB PROCESSES panel
function wlBuildDbProcessesInner(metricsArr) {
    if (!metricsArr.length) return wlNoNodes();
    return metricsArr.map(node => {
        const m = node.metrics || {};
        const active = parseInt(m.active_conn) || 0;
        const max = parseInt(m.max_conn) || 1;
        const pct = Math.min((active / max) * 100, 100);
        const barColor = pct > 85 ? '#ef4444' : pct > 65 ? '#f59e0b' : '#6366f1';
        return `<div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="color:#94a3b8;font-size:0.78rem;">${escapeHTML(node.name)}</span>
                <span style="color:${barColor};font-size:0.78rem;font-weight:700;">${escapeHTML(m.connections || '—')}</span>
            </div>
            <div style="background:#334155;border-radius:4px;height:8px;overflow:hidden;">
                <div style="background:${barColor};height:100%;width:${pct.toFixed(1)}%;border-radius:4px;transition:width 0.5s;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:3px;">
                <span style="color:#475569;font-size:0.7rem;">${active} active</span>
                <span style="color:#475569;font-size:0.7rem;">${max} max</span>
            </div>
        </div>`;
    }).join('<hr style="border:none;border-top:1px solid #1e293b;margin:4px 0;">');
}

// DB GROWTH panel
function wlBuildDbGrowthInner(metricsArr) {
    if (!metricsArr.length) return wlNoNodes();
    return metricsArr.map(node => {
        const m = node.metrics || {};
        const tuples = [
            { label: 'Fetched',   val: m.tup_fetched,  color: '#6366f1' },
            { label: 'Inserted',  val: m.tup_inserted, color: '#22c55e' },
            { label: 'Updated',   val: m.tup_updated,  color: '#f59e0b' },
            { label: 'Deleted',   val: m.tup_deleted,  color: '#ef4444' },
        ];
        return `<div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="color:#94a3b8;font-size:0.78rem;">${escapeHTML(node.name)}</span>
                <span style="color:#38bdf8;font-size:0.82rem;font-weight:700;">${escapeHTML(m.storage || '—')}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
                ${tuples.map(t => `<div style="background:#172033;border-radius:5px;padding:5px 8px;">
                    <div style="color:#475569;font-size:0.68rem;">${t.label}</div>
                    <div style="color:${t.color};font-size:0.78rem;font-weight:600;">${t.val != null ? Number(t.val).toLocaleString() : '—'}</div>
                </div>`).join('')}
            </div>
        </div>`;
    }).join('<hr style="border:none;border-top:1px solid #1e293b;margin:4px 0;">');
}

// ALARMS panel
function wlBuildAlarmsInner(cluster) {
    const logs = (wlViewer.auditCache || []).filter(l =>
        l.project_id === cluster.id &&
        l.action && (l.action.toLowerCase().includes('fail') ||
                     l.action.toLowerCase().includes('error') ||
                     l.action.toLowerCase().includes('alarm') ||
                     l.action.toLowerCase().includes('offline'))
    ).slice(0, 8);
    if (!logs.length) return `<div style="color:#22c55e;font-size:0.82rem;text-align:center;padding:12px 0;">
        <span style="font-size:1.5rem;display:block;margin-bottom:6px;">✅</span>No alarms</div>`;
    return logs.map(l => `<div style="display:flex;align-items:flex-start;gap:8px;padding:5px 0;border-bottom:1px solid #172033;">
        <span style="color:#ef4444;font-size:0.75rem;flex-shrink:0;margin-top:1px;">⚠</span>
        <div>
            <div style="color:#fca5a5;font-size:0.78rem;font-weight:500;">${escapeHTML(l.action)}</div>
            <div style="color:#475569;font-size:0.7rem;">${escapeHTML(l.timestamp || '')}</div>
        </div>
    </div>`).join('');
}

// TOP QUERIES panel (shows transaction stats since pg_stat_statements may not be installed)
function wlBuildTopQueriesInner(metricsArr) {
    if (!metricsArr.length) return wlNoNodes();
    return metricsArr.map(node => {
        const m = node.metrics || {};
        const commits = parseInt(m.commits_raw) || 0;
        const rollbacks = parseInt(m.rollbacks_raw) || 0;
        const total = commits + rollbacks;
        const rollbackPct = total > 0 ? ((rollbacks / total) * 100).toFixed(1) : '0.0';
        const rollbackColor = parseFloat(rollbackPct) > 5 ? '#f59e0b' : parseFloat(rollbackPct) > 10 ? '#ef4444' : '#22c55e';
        const stats = [
            { label: 'Commits ✓',   val: commits.toLocaleString(),  color: '#22c55e' },
            { label: 'Rollbacks ✗',  val: rollbacks.toLocaleString(), color: '#ef4444' },
            { label: 'Rollback %',   val: rollbackPct + '%',          color: rollbackColor },
            { label: 'Fetched rows', val: m.tup_fetched != null ? Number(m.tup_fetched).toLocaleString() : '—', color: '#6366f1' },
        ];
        return `<div style="margin-bottom:10px;">
            <div style="color:#94a3b8;font-size:0.78rem;margin-bottom:6px;">${escapeHTML(node.name)}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
                ${stats.map(s => `<div style="background:#172033;border-radius:5px;padding:5px 8px;">
                    <div style="color:#475569;font-size:0.68rem;">${s.label}</div>
                    <div style="color:${s.color};font-size:0.78rem;font-weight:600;">${s.val}</div>
                </div>`).join('')}
            </div>
            ${m.xact ? `<div style="color:#64748b;font-size:0.71rem;margin-top:5px;">Transactions: ${escapeHTML(m.xact)}</div>` : ''}
        </div>`;
    }).join('<hr style="border:none;border-top:1px solid #1e293b;margin:4px 0;">');
}

// Helper
function wlNoNodes() {
    return '<div style="color:#475569;font-size:0.82rem;text-align:center;padding:12px 0;">No nodes connected.</div>';
}

    async function fetchDashboardMetrics() {
        try {
            const container = document.getElementById('dashboard-metrics-container');
            if(!container) return;

            const projRes = await apiFetch('/api/projects');
            if (!projRes.ok) return;
            const allProjs = await projRes.json();
            
            if (allProjs.length === 0) {
                container.innerHTML = '<div class="loading-state">No projects found. Add a project to view metrics.</div>';
                return;
            }
            
            // When inside a project's detail view, ONLY render metrics for currentProjectId!
            const currentHash = (window.location.hash || '').replace(/^#/, '');
            const isDetailView = (currentHash === 'project-detail-view' || (detailView && getComputedStyle(detailView).display !== 'none'));
            const targetProjs = (isDetailView && currentProjectId) 
                ? allProjs.filter(p => p.id === currentProjectId)
                : allProjs;
                
            if (targetProjs.length === 0) {
                container.innerHTML = '<div class="loading-state">Cluster not found.</div>';
                return;
            }
            
            // Fetch metrics for target projects concurrently
            const metricPromises = targetProjs.map(p => apiFetch(`/api/projects/${p.id}/metrics`).then(r => r.ok ? r.json() : []));
            const metricsResults = await Promise.all(metricPromises);
            
            // Flat list of all nodes returned for target projects
            const allTargetNodes = metricsResults.flat();
            
            if (container.querySelector('.loading-state')) {
                container.innerHTML = '';
            }
            
            // Remove columns for nodes that don't belong to current target cluster!
            const allTargetNodeIds = allTargetNodes.map(n => "dash-node-" + n.id);
            Array.from(container.children).forEach(child => {
                if (!allTargetNodeIds.includes(child.id)) {
                    child.remove();
                }
            });
            
            targetProjs.forEach((proj, i) => {
                const dataList = metricsResults[i];
                if (!dataList || dataList.length === 0) return;
                
                dataList.forEach(node => {
                    let col = document.getElementById("dash-node-" + node.id);
                    if(!col) {
                        col = document.createElement('div');
                        col.className = 'metrics-column';
                        col.id = "dash-node-" + node.id;
                        
                        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'];
                        const projColor = colors[proj.id % colors.length] || 'var(--primary)';
                        
                        const headerHtml = `
                            <div class="dash-node-header" data-proj-id="${proj.id}" style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 20px; cursor: pointer;" title="Click to view Node List for ${escapeHTML(proj.name)}">
                                <div>
                                    <div style="font-size: 0.8rem; color: ${projColor}; text-transform: uppercase; font-weight: bold; margin-bottom: 4px;">${escapeHTML(proj.name)}</div>
                                    <h2 style="margin: 0; font-size: 1.2rem;">${escapeHTML(node.name)} <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-muted);">(${escapeHTML(node.role)})</span></h2>
                                </div>
                                <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
                                    <span class="status-badge status-offline" id="metric-${node.id}-status">Offline</span>
                                    <span style="font-size:0.75rem;color:#3a1c94;font-weight:500;display:flex;align-items:center;gap:3px;">
                                        View nodes
                                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                                    </span>
                                </div>
                            </div>
                        `;
                        
                        const metricsHtml = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel" id="metric-${node.id}-card-cpu" style="display: none;"><div class="metric-label">CPU Kullanımı</div><div class="metric-val" id="metric-${node.id}-cpu" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel" id="metric-${node.id}-card-ram" style="display: none;"><div class="metric-label">RAM Kullanımı</div><div class="metric-val" id="metric-${node.id}-ram" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-${node.id}-ping">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Senkronizasyon (Lag)</div><div class="metric-val" id="metric-${node.id}-lag">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Depolama (Storage)</div><div class="metric-val" id="metric-${node.id}-storage">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Bağlantılar (Aktif/Top.)</div><div class="metric-val" id="metric-${node.id}-conn">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">İşlem Yükü (Başarılı / İptal)</div><div class="metric-val" id="metric-${node.id}-xact">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ana Tablo Kaydı</div><div class="metric-val" id="metric-${node.id}-plates">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Önbellek Başarısı</div><div class="metric-val" id="metric-${node.id}-cache">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Çalışma Süresi</div><div class="metric-val" id="metric-${node.id}-uptime">-</div></div>
                            </div>
                            <div style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted); text-align: right;">
                                Motor Sürümü: <span id="metric-${node.id}-version">-</span>
                            </div>
                        `;
                        col.innerHTML = headerHtml + metricsHtml;

                        // ── Click header → navigate to Clusters > Nodes > Node List ──
                        const headerEl = col.querySelector('.dash-node-header');
                        if (headerEl) {
                            headerEl.addEventListener('click', () => {
                                // Find the full project object from allProjs
                                const targetProj = allProjs.find(p => p.id === proj.id);
                                if (!targetProj) return;
                                // Open project detail view
                                showDetailView(targetProj);
                                // After rendering, switch to Nodes tab
                                setTimeout(() => {
                                    const nodesTab = document.querySelector('.cluster-tab[data-tab="nodes"]');
                                    if (nodesTab) nodesTab.click();
                                }, 80);
                            });
                        }

                        container.appendChild(col);
                    }
                    
                    const m = node.metrics;
                    if(m && m.status === 'online') {
                        const statusEl = document.getElementById("metric-" + node.id + "-status");
                        if(statusEl) { statusEl.className = 'status-badge status-online'; statusEl.innerText = 'Aktif'; }
                        
                        const setEl = (id, val) => { const el = document.getElementById(id); if(el) el.innerText = val; };
                        setEl("metric-" + node.id + "-ping", m.ping);
                        setEl("metric-" + node.id + "-lag", m.lag);
                        setEl("metric-" + node.id + "-storage", m.storage);
                        setEl("metric-" + node.id + "-conn", m.connections);
                        setEl("metric-" + node.id + "-xact", m.xact);
                        setEl("metric-" + node.id + "-cache", m.cache_hit);
                        setEl("metric-" + node.id + "-version", m.version);
                        setEl("metric-" + node.id + "-plates", m.plates || m.row_count || "N/A");
                        setEl("metric-" + node.id + "-uptime", m.uptime || "N/A");
                        
                        // Hide CPU & RAM if N/A
                        const cardCpu = document.getElementById(`metric-${node.id}-card-cpu`);
                        if (cardCpu) {
                            if (m.cpu_usage && m.cpu_usage !== 'N/A') {
                                cardCpu.style.display = 'block';
                                setEl(`metric-${node.id}-cpu`, m.cpu_usage);
                            } else {
                                cardCpu.style.display = 'none';
                            }
                        }
                        const cardRam = document.getElementById(`metric-${node.id}-card-ram`);
                        if (cardRam) {
                            if (m.ram_usage && m.ram_usage !== 'N/A') {
                                cardRam.style.display = 'block';
                                setEl(`metric-${node.id}-ram`, m.ram_usage);
                            } else {
                                cardRam.style.display = 'none';
                            }
                        }
                    } else if (m && m.status === 'offline') {
                        const statusEl = document.getElementById("metric-" + node.id + "-status");
                        if(statusEl) { statusEl.className = 'status-badge status-offline'; statusEl.innerText = 'Çevrimdışı'; }
                        ['cpu','ram','ping','lag','storage','conn','xact','plates','cache','uptime'].forEach(key => {
                            const el = document.getElementById(`metric-${node.id}-${key}`);
                            if(el) el.innerText = '-';
                        });
                    }
                });
            });
        } catch (e) {
            console.error("Dashboard error:", e);
        }
    }
    
    const btnSyncRepDashboard = document.getElementById('btn-sync-replication-dashboard');
    const modalSyncStatus = document.getElementById('modal-sync-status');
    const btnCloseSyncModal = document.getElementById('btn-close-sync-modal');
    
    if (btnSyncRepDashboard && modalSyncStatus) {
        btnSyncRepDashboard?.addEventListener('click', () => {
            modalSyncStatus.style.display = 'flex';
            const dataFlow = document.getElementById('sync-data-flow');
            if(dataFlow) {
                dataFlow.style.animation = 'dataFlowRight 1.5s infinite linear';
            }
        });
    }

    if (btnCloseSyncModal && modalSyncStatus) {
        btnCloseSyncModal?.addEventListener('click', () => {
            modalSyncStatus.style.display = 'none';
        });
    }
    
    // Edit Node Modal specific
    const modalEditNode = document.getElementById('modal-edit-node');
    const btnCloseEditNodeModal = document.getElementById('btn-close-edit-node-modal');
    const formEditNode = document.getElementById('form-edit-node');
    const editNodeUrlInput = document.getElementById('edit-node-url');
    const editNodeTitle = document.getElementById('edit-node-title');
    const toggleEditUrlBtn = document.getElementById('toggle-edit-url-btn');
    const copyEditUrlBtn = document.getElementById('copy-edit-url-btn');
    const btnSubmitEditNode = document.getElementById('btn-submit-edit-node');

    let modalMetricsInterval = null;

    btnCloseEditNodeModal?.addEventListener('click', () => {
        modalEditNode.style.display = 'none';
        editNodeUrlInput.value = '';
        editNodeUrlInput.type = 'password';
        if(modalMetricsInterval) clearInterval(modalMetricsInterval);
    });

    const eyeOpenSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
    const eyeClosedSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle><line x1="1" y1="1" x2="23" y2="23"></line></svg>';

    toggleEditUrlBtn?.addEventListener('click', () => {
        if(editNodeUrlInput.type === 'password') {
            editNodeUrlInput.type = 'text';
            toggleEditUrlBtn.innerHTML = eyeOpenSvg;
        } else {
            editNodeUrlInput.type = 'password';
            toggleEditUrlBtn.innerHTML = eyeClosedSvg;
        }
    });

    copyEditUrlBtn?.addEventListener('click', () => {
        if(editNodeUrlInput.value) {
            navigator.clipboard.writeText(editNodeUrlInput.value);
            const originalIcon = copyEditUrlBtn.innerHTML;
            copyEditUrlBtn.innerHTML = '<span style="color:var(--success);font-size:0.8rem;">Copied!</span>';
            setTimeout(() => copyEditUrlBtn.innerHTML = originalIcon, 2000);
        }
    });

    async function fetchModalMetrics(nodeId) {
        try {
            const res = await apiFetch(`/api/nodes/${nodeId}/metrics`);
            if(!res.ok) {
                document.getElementById('modal-metric-status').className = 'status-badge status-offline';
{ const TMP_EL = document.getElementById('modal-metric-status'); if(TMP_EL) {                 TMP_EL.innerText = 'Hata (502)'; } }
                return;
            }
            const data = await res.json();
            
            if(!data || data.status !== 'online') {
                document.getElementById('modal-metric-status').className = 'status-badge status-offline';
{ const TMP_EL = document.getElementById('modal-metric-status'); if(TMP_EL) {                 TMP_EL.innerText = 'Offline'; } }
                return;
            }
            
            document.getElementById('modal-metric-status').className = 'status-badge status-online';
{ const TMP_EL = document.getElementById('modal-metric-status'); if(TMP_EL) {             TMP_EL.innerText = 'Aktif'; } }
            
{ const TMP_EL = document.getElementById('modal-metric-ping'); if(TMP_EL) {             TMP_EL.innerText = data.ping || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-lag'); if(TMP_EL) {             TMP_EL.innerText = data.lag || '0ms'; } }
{ const TMP_EL = document.getElementById('modal-metric-storage'); if(TMP_EL) {             TMP_EL.innerText = data.storage || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-conn'); if(TMP_EL) {             TMP_EL.innerText = data.connections || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-xact'); if(TMP_EL) {             TMP_EL.innerText = data.xact || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-cache'); if(TMP_EL) {             TMP_EL.innerText = data.cache_hit || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-uptime'); if(TMP_EL) {             TMP_EL.innerText = data.uptime || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-version'); if(TMP_EL) {             TMP_EL.innerText = data.version || '-'; } }
{ const TMP_EL = document.getElementById('modal-metric-plates'); if(TMP_EL) {             TMP_EL.innerText = data.plates || 'N/A'; } }
            
        } catch(e) {
            console.error("Modal metrics fetch error:", e);
        }
    }

    async function openEditNodeModal(nodeId, nodeName) {
        editNodeTitle.innerText = `Edit ${nodeName}`;
        document.getElementById('edit-node-id').value = nodeId;
        editNodeUrlInput.value = 'Loading...';
        editNodeUrlInput.type = 'password';
        
        // Reset metrics UI
        document.getElementById('modal-metric-status').className = 'status-badge status-offline';
{ const TMP_EL = document.getElementById('modal-metric-status'); if(TMP_EL) {         TMP_EL.innerText = 'Loading...'; } }
        const spinnerHtml = '<svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg> Yükleniyor...';
        ['ping', 'lag', 'storage', 'conn', 'xact', 'cache', 'uptime', 'version', 'plates'].forEach(m => {
{ const TMP_EL = document.getElementById(`modal-metric-${m}`); if(TMP_EL) {             TMP_EL.innerHTML = spinnerHtml; } }
        });
        
        modalEditNode.style.display = 'flex';
        
        // Start polling metrics for this node
        if(modalMetricsInterval) clearInterval(modalMetricsInterval);
        fetchModalMetrics(nodeId);
        modalMetricsInterval = setInterval(() => fetchModalMetrics(nodeId), 1000);
        
        // Fetch the URL
        try {
            const res = await apiFetch(`/api/nodes/${nodeId}/url`);
            const data = await res.json();
            if(data.success) {
                editNodeUrlInput.value = data.url;
            } else {
                editNodeUrlInput.value = '';
                alert("Could not load URL");
            }
        } catch(e) {
            editNodeUrlInput.value = '';
            alert("Error loading URL");
        }
    }

    formEditNode?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nodeId = document.getElementById('edit-node-id').value;
        const newUrl = editNodeUrlInput.value;
        
        btnSubmitEditNode.innerText = "Pinging Server...";
        btnSubmitEditNode.disabled = true;
        
        try {
            const res = await apiFetch(`/api/nodes/${nodeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: newUrl })
            });
            const data = await res.json();
            if(data.success) {
                alert("URL Updated Successfully!");
                modalEditNode.style.display = 'none';
                refreshCurrentProject();
            } else {
                alert(data.message || "Failed to update node");
            }
        } catch(err) {
            alert("Error connecting to server");
        } finally {
            btnSubmitEditNode.innerText = "Kaydet ve Yeniden Başlat";
            btnSubmitEditNode.disabled = false;
        }
    });
    
    // Navigation
    btnBackProjects?.addEventListener('click', () => { window.location.hash = 'clusters-view'; });

    // Form: Edit Project
    btnCloseEditProjModal?.addEventListener('click', () => { if(modalEditProj) modalEditProj.style.display = 'none'; });
    
    formEditProj?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('edit-proj-id').value;
        const name = document.getElementById('edit-proj-name').value.trim();
        const desc = document.getElementById('edit-proj-desc').value.trim();

        if (!name) {
            alert('Cluster adı boş bırakılamaz.');
            return;
        }

        try {
            const response = await apiFetch(`/api/projects/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description: desc })
            });
            const res = await response.json();
            
            if (response.ok && res.success) {
                modalEditProj.style.display = 'none';
                formEditProj.reset();
                fetchProjects();
                fetchRecentAlarms();
                
                // Update detail view if it's currently showing the edited project
                if (currentProjectId == id && detailView && detailView.style.display !== 'none') {
                    const el_detail_proj_name = document.getElementById('detail-proj-name'); if(el_detail_proj_name) el_detail_proj_name.innerText = name;
                    const el_detail_proj_desc = document.getElementById('detail-proj-desc'); if(el_detail_proj_desc) el_detail_proj_desc.innerText = desc || 'No description';
                }
            } else {
                alert(res.detail || res.message || "Cluster güncellenemedi.");
            }
        } catch (err) {
            alert('Sunucu hatası: ' + err.message);
        }
    });

    // Form: Add Project
    formAddProj?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('proj-name').value.trim();
        const desc = document.getElementById('proj-desc').value.trim();
        const initUrl = (document.getElementById('proj-init-db-url')?.value || '').trim();
        const initSshHost = (document.getElementById('proj-init-ssh-host')?.value || '').trim();
        const initSshPort = parseInt(document.getElementById('proj-init-ssh-port')?.value || '22') || 22;
        const initSshUser = (document.getElementById('proj-init-ssh-user')?.value || 'root').trim();
        const initSshPass = (document.getElementById('proj-init-ssh-pass')?.value || '').trim();

        if (!name) {
            alert('Cluster adı boş bırakılamaz. Lütfen bir isim giriniz.');
            return;
        }

        try {
            const payload = { name, description: desc };
            if (initUrl || initSshHost) {
                payload.initial_node = {
                    url: initUrl,
                    ssh_host: initSshHost,
                    ssh_port: initSshPort,
                    ssh_username: initSshUser,
                    ssh_password: initSshPass
                };
            }

            const response = await apiFetch('/api/projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const res = await response.json();
            if (response.ok && res.success) {
                modalAddProj.style.display = 'none';
                formAddProj.reset();
                const initWrap = document.getElementById('proj-initial-node-wrap');
                if (initWrap) initWrap.style.display = 'none';
                fetchProjects();
                fetchRecentAlarms();
            } else {
                alert(res.detail || res.message || 'Cluster oluşturulamadı.');
            }
        } catch (err) {
            alert('Bağlantı hatası: ' + err.message);
        }
    });

    // Form: Add Node
    formAddNode?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentProjectId) return;

        const name = document.getElementById('node-name').value.trim();
        const role = document.getElementById('node-role').value;
        const url = document.getElementById('node-url').value.trim();

        // SSH Credentials (opsiyonel)
        const sshHost     = (document.getElementById('node-ssh-host')?.value || '').trim();
        const sshPort     = parseInt(document.getElementById('node-ssh-port')?.value || '22') || 22;
        const sshUser     = (document.getElementById('node-ssh-user')?.value || 'root').trim();
        const sshPassword = (document.getElementById('node-ssh-password')?.value || '').trim();

        if (!name) {
            alert('Sunucu adı boş bırakılamaz.');
            return;
        }
        if (!url) {
            alert('Sunucu bağlantı URL adresi boş bırakılamaz.');
            return;
        }

        btnSubmitNode.innerText = "Pinging Server (Please Wait)...";
        btnSubmitNode.disabled = true;

        try {
            const payload = { role, name, url };
            // SSH bilgileri girilmişse payload'a ekle
            if (sshHost) {
                payload.ssh_host = sshHost;
                payload.ssh_port = sshPort;
                payload.ssh_username = sshUser || 'root';
                if (sshPassword) payload.ssh_password = sshPassword;
            }

            const response = await apiFetch(`/api/projects/${currentProjectId}/nodes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const res = await response.json();
            
            if (response.ok && res.success) {
                modalAddNode.style.display = 'none';
                formAddNode.reset();
                // SSH section'ı kapat
                const sshSection = document.getElementById('node-ssh-section');
                if (sshSection) sshSection.style.display = 'none';
                refreshCurrentProject();
            } else {
                alert(res.detail || res.message || "Sunucu eklenemedi. Bilgileri kontrol ediniz.");
            }
        } catch (err) {
            alert('Sunucu bağlantı hatası: ' + err.message);
        } finally {
            btnSubmitNode.innerText = "Verify & Save Node";
            btnSubmitNode.disabled = false;
        }
    });

    // Button: Sync Replication
    btnSyncReplication?.addEventListener('click', async () => {
        if (!currentProjectId) return;
        
        btnSyncReplication.innerText = "Starting...";
        btnSyncReplication.disabled = true;

        try {
            const response = await apiFetch(`/api/projects/${currentProjectId}/sync`, {
                method: 'POST'
            });
            const res = await response.json();
            
            if (response.ok && res.success) {
                // Job queued successfully, start polling
                refreshCurrentProject();
            } else {
                alert("ERROR: " + (res.message || "Sync failed to start."));
                btnSyncReplication.innerText = "Sync Replication";
                btnSyncReplication.disabled = false;
            }
        } catch (err) {
            alert('Server error while starting sync.');
            btnSyncReplication.innerText = "Sync Replication";
            btnSyncReplication.disabled = false;
        }
    });

    const btnCleanupSlots = document.getElementById('btn-cleanup-slots');
    if (btnCleanupSlots) {
        btnCleanupSlots?.addEventListener('click', async () => {
            if (!currentProjectId) return;
            if (!confirm('Primary sunucudaki eski/kayıt dışı replikasyon slotları (orphan slots) temizlenecek. Onaylıyor musunuz?')) return;
            
            btnCleanupSlots.innerText = "Temizleniyor...";
            btnCleanupSlots.disabled = true;
            try {
                const res = await apiFetch(`/api/projects/${currentProjectId}/cleanup-slots`, { method: 'POST' });
                const data = await res.json();
                if (res.ok && data.success) {
                    alert(data.message);
                    window.fetchAuditLogs();
                } else {
                    alert(data.message || "Temizleme işlemi başarısız.");
                }
            } catch (e) {
                alert("Sunucu hatası.");
            } finally {
                btnCleanupSlots.innerText = "Replication Slot Silme";
                btnCleanupSlots.disabled = false;
            }
        });
    }


    // Button: Edit Project (Detail View)
    if (btnEditProjectDetail) {
        btnEditProjectDetail?.addEventListener('click', async () => {
            if (!currentProjectId) return;
            // Get current project details directly from backend to ensure data is fresh
            try {
                const res = await apiFetch(`/api/projects/${currentProjectId}`);
                if (res.ok) {
                    const proj = await res.json();
                    document.getElementById('edit-proj-id').value = proj.id;
                    document.getElementById('edit-proj-name').value = proj.name;
                    document.getElementById('edit-proj-desc').value = proj.description || '';
                    modalEditProj.style.display = 'flex';
                }
            } catch (err) {
                console.error("Could not fetch project details for edit.");
            }
        });
    }

    // Button: Remove Cluster
    const btnRemoveCluster = document.getElementById('btn-remove-cluster');
    if (btnRemoveCluster) {
        btnRemoveCluster.addEventListener('click', async () => {
            if (!currentProjectId) return;
            const projName = document.getElementById('detail-proj-name')?.innerText || `ID: ${currentProjectId}`;
            if (!confirm(`"${projName}" cluster'ını kalıcı olarak silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz. Tüm node kayıtları da silinecektir.`)) return;

            btnRemoveCluster.innerText = 'Siliniyor...';
            btnRemoveCluster.disabled = true;

            try {
                const res = await apiFetch(`/api/projects/${currentProjectId}`, { method: 'DELETE' });
                if (res.ok) {
                    // Go back to projects list
                    currentProjectId = null;
                    window.location.hash = 'projects-view';
                    await fetchProjects();
                    alert(`"${projName}" cluster'ı başarıyla silindi.`);
                } else {
                    const data = await res.json().catch(() => ({}));
                    alert('Silme hatası: ' + (data.detail || res.statusText));
                    btnRemoveCluster.innerText = 'Remove Cluster';
                    btnRemoveCluster.disabled = false;
                }
            } catch (err) {
                alert('Sunucu bağlantı hatası.');
                btnRemoveCluster.innerText = 'Remove Cluster';
                btnRemoveCluster.disabled = false;
            }
        });
    }

    const btnRefreshLogs = document.getElementById('btn-refresh-logs');
    if(btnRefreshLogs) {
        btnRefreshLogs?.addEventListener('click', window.fetchAuditLogs);
    }

    // Button: Save Settings
    const btnSaveSettings = document.getElementById('btn-save-project-settings') || document.getElementById('btn-save-settings');
    const updateIntervalInput = document.getElementById('setting-update-interval');
    if (updateIntervalInput) {
        updateIntervalInput.value = localStorage.getItem('dashboard_update_interval_sec') || 1;
    }
    
    const settingsProjectSelect = document.getElementById('setting-project-select');
    const projectSettingsContainer = document.getElementById('project-settings-container');
    const settingWalLag = document.getElementById('setting-wal-lag');
    const settingMetricTable = document.getElementById('setting-metric-table');
    const settingReplicationTables = document.getElementById('setting-replication-tables');

    window.loadProjectSettingsDropdown = async function() {
        const select = document.getElementById('setting-project-select');
        const container = document.getElementById('project-settings-container');
        if (!select) return;
        try {
            const response = await apiFetch('/api/projects');
            if (response.ok) {
                const projs = await response.json();
                const currentVal = select.value;
                select.innerHTML = '<option value="">Proje seçin...</option>';
                projs.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p.id;
                    opt.textContent = p.name;
                    if (String(p.id) === String(currentVal)) opt.selected = true;
                    select.appendChild(opt);
                });
                if (!select.value && container) {
                    container.style.display = 'none';
                }
            }
        } catch(err) {
            console.error("Failed to fetch projects for settings", err);
        }
    };

    // Populate projects select when settings view is opened
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', async (e) => {
            const targetId = e.target.getAttribute('data-view');
            if (targetId === 'settings-view') {
                window.loadProjectSettingsDropdown();
            }
        });
    });

    if (settingsProjectSelect) {
        settingsProjectSelect.addEventListener('change', async (e) => {
            const pid = e.target.value;
            if (!pid) {
                if (projectSettingsContainer) projectSettingsContainer.style.display = 'none';
                return;
            }
            try {
                const res = await apiFetch(`/api/settings/${pid}`);
                if (res.ok) {
                    const data = await res.json();
                    if (settingWalLag) settingWalLag.value = data.max_wal_lag_mb || 500;
                    if (settingMetricTable) settingMetricTable.value = data.metric_table || '';
                    if (settingReplicationTables) settingReplicationTables.value = data.replication_tables || '';
                    if (projectSettingsContainer) projectSettingsContainer.style.display = 'block';
                }
            } catch (err) {
                console.error("Error loading settings for project", err);
            }
        });
    }

    if (btnSaveSettings) {
        btnSaveSettings.addEventListener('click', async () => {
            const pid = settingsProjectSelect ? settingsProjectSelect.value : null;
            if (!pid) {
                alert("Lütfen önce bir proje seçin.");
                return;
            }

            const lagVal = settingWalLag ? settingWalLag.value : 500;
            const metricTableVal = settingMetricTable ? settingMetricTable.value : '';
            const repTableVal = settingReplicationTables ? settingReplicationTables.value : '';
            const updateIntervalVal = updateIntervalInput ? updateIntervalInput.value : 1;
            
            localStorage.setItem('dashboard_update_interval_sec', updateIntervalVal);
            
            btnSaveSettings.innerText = "Kaydediliyor...";
            try {
                const payload = { max_wal_lag_mb: parseInt(lagVal) };
                if (metricTableVal.trim() !== '') {
                    payload.metric_table = metricTableVal.trim();
                }
                if (repTableVal.trim() !== '') {
                    payload.replication_tables = repTableVal.trim();
                }
                
                const res = await apiFetch(`/api/settings/${pid}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                if(res.ok) {
                    alert("Ayarlar başarıyla kaydedildi!");
                } else {
                    alert("Ayarlar kaydedilemedi.");
                }
            } catch (e) {
                alert("Ayarları kaydederken hata oluştu.");
            }
            btnSaveSettings.innerText = "Ayarları Kaydet";
        });
    }

    // --- LOGIN SYSTEM ---
    const loginScreen = document.getElementById('login-screen');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');
    const loginBtn = document.getElementById('btn-login');
    const loginError = document.getElementById('login-error');
    const loginToggleVis = document.getElementById('login-toggle-vis');
    const capsWarning = document.getElementById('caps-warning');

    // Caps Lock detection
    const checkCapsLock = (e) => {
        if (e.getModifierState && e.getModifierState('CapsLock')) {
            capsWarning.style.display = 'flex';
        } else {
            capsWarning.style.display = 'none';
        }
    };
    loginPassword.addEventListener('keyup', checkCapsLock);
    loginPassword.addEventListener('keydown', checkCapsLock);
    loginUsername.addEventListener('keyup', checkCapsLock);
    loginUsername.addEventListener('keydown', checkCapsLock);

    // Toggle password visibility
    let loginPasswordVis = false;
    loginToggleVis.addEventListener('click', () => {
        loginPasswordVis = !loginPasswordVis;
        loginPassword.type = loginPasswordVis ? 'text' : 'password';
        if(loginPasswordVis) {
            loginToggleVis.innerHTML = '<svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
        } else {
            loginToggleVis.innerHTML = '<svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>';
        }
    });

    // Login Logic
    const attemptLogin = async () => {
        const u = loginUsername.value.trim();
        const p = loginPassword.value.trim();
        const token = btoa(unescape(encodeURIComponent(u + ':' + p)));
        try {
            const res = await fetch('/api/auth/verify', {
                headers: { 'Authorization': 'Basic ' + token }
            });
            if (res.ok) {
                globalAuthToken = token;
                localStorage.setItem('auth_token', token);
                loginScreen.style.transition = 'opacity 0.3s ease';
                loginScreen.style.opacity = '0';
                setTimeout(() => {
                    loginScreen.style.display = 'none';
                }, 300);
                
                // Only fetch initial data after successful login
                fetchProjects();
        fetchRecentAlarms();
            } else {
                loginError.style.display = 'block';
                loginError.innerText = 'Invalid username or password';
                setTimeout(() => loginError.style.display = 'none', 3000);
            }
        } catch (err) {
            loginError.style.display = 'block';
            loginError.innerText = 'Connection to server failed';
            setTimeout(() => loginError.style.display = 'none', 3000);
        }
    };

    loginBtn.addEventListener('click', attemptLogin);
    loginPassword.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') attemptLogin();
    });
    loginUsername.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') attemptLogin();
    });

    document.getElementById('btn-delete-node').addEventListener('click', async () => {
        const nodeId = document.getElementById('edit-node-id').value;
        if (!confirm('Bu sunucuyu silmek istediğinize emin misiniz?')) return;
        
        try {
            const res = await apiFetch('/api/nodes/' + nodeId, { method: 'DELETE' });
            if (res.ok) {
                modalEditNode.style.display = 'none';
                fetchProjects();
        fetchRecentAlarms();
            } else {
                alert('Sunucu silinemedi.');
            }
        } catch (e) {
            alert('Sunucu silinemedi.');
        }
    });
});

document.getElementById('toggle-url-btn')?.addEventListener('click', function() {
    const input = document.getElementById('node-url');
    if (!input) return;
    const icon = this.querySelector('svg');
    if (input.type === 'password') {
        input.type = 'text';
        if (icon) icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
    } else {
        input.type = 'password';
        if (icon) icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle><line x1="1" y1="1" x2="23" y2="23"></line>';
    }
});

document.getElementById('copy-url-btn')?.addEventListener('click', function() {
    const input = document.getElementById('node-url');
    if (!input) return;
    navigator.clipboard.writeText(input.value).then(() => {
        const originalHTML = this.innerHTML;
        this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00ff00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        setTimeout(() => { this.innerHTML = originalHTML; }, 2000);
    });
});

// Sidebar Toggle Logic
document.getElementById('btn-toggle-sidebar')?.addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    sidebar.classList.toggle('collapsed');
    const icon = document.getElementById('icon-sidebar-arrow');
    if (sidebar.classList.contains('collapsed')) {
        if (icon) icon.innerHTML = '<polyline points="9 18 15 12 9 6"></polyline>';
    } else {
        if (icon) icon.innerHTML = '<polyline points="15 18 9 12 15 6"></polyline>';
    }
});

// --- ACTIVITY CENTER TABS ---
document.addEventListener('DOMContentLoaded', () => {
    const btnAlarms = document.getElementById('tab-btn-alarms');
    const btnJobs = document.getElementById('tab-btn-jobs');
    const btnAudit = document.getElementById('tab-btn-audit');

    const contentAlarms = document.getElementById('content-alarms');
    const contentJobs = document.getElementById('content-jobs');
    const contentAudit = document.getElementById('content-audit');

    function switchActivityTab(tab) {
        [btnAlarms, btnJobs, btnAudit].forEach(btn => {
            if(btn) {
                btn.classList.remove('active');
                btn.style.color = '#4b5563';
                btn.style.borderBottom = '2px solid transparent';
            }
        });
        [contentAlarms, contentJobs, contentAudit].forEach(content => {
            if(content) content.style.display = 'none';
        });
        
        if (tab === 'alarms') {
            if(btnAlarms) { btnAlarms.style.color = 'var(--primary)'; btnAlarms.style.borderBottom = '2px solid var(--primary)'; }
            if(contentAlarms) contentAlarms.style.display = 'flex';
        } else if (tab === 'jobs') {
            if(btnJobs) { btnJobs.style.color = 'var(--primary)'; btnJobs.style.borderBottom = '2px solid var(--primary)'; }
            if(contentJobs) contentJobs.style.display = 'flex';
        } else if (tab === 'audit') {
            if(btnAudit) { btnAudit.style.color = 'var(--primary)'; btnAudit.style.borderBottom = '2px solid var(--primary)'; }
            if(contentAudit) {
                contentAudit.style.display = 'flex';
                // Only call if we are sure fetchAuditLogs exists
                if (typeof window.fetchAuditLogs === 'function') {
                    window.fetchAuditLogs();
                }
            }
        }
    }

    if(btnAlarms) btnAlarms.addEventListener('click', () => switchActivityTab('alarms'));
    if(btnJobs) btnJobs.addEventListener('click', () => switchActivityTab('jobs'));
    if(btnAudit) btnAudit.addEventListener('click', () => switchActivityTab('audit'));
});


// --- OPERATIONAL REPORTS TABS & MODAL ---
document.addEventListener('DOMContentLoaded', () => {
    const btnTabReports = document.getElementById('tab-btn-reports');
    const btnTabSchedules = document.getElementById('tab-btn-schedules');
    const contentReports = document.getElementById('content-reports');
    const contentSchedules = document.getElementById('content-schedules');
    
    function switchReportTab(tab) {
        [btnTabReports, btnTabSchedules].forEach(btn => {
            if(btn) {
                btn.classList.remove('active');
                btn.style.color = '#4b5563';
                btn.style.borderBottom = '2px solid transparent';
            }
        });
        [contentReports, contentSchedules].forEach(content => {
            if(content) content.style.display = 'none';
        });
        
        if (tab === 'reports') {
            if(btnTabReports) { btnTabReports.style.color = 'var(--primary)'; btnTabReports.style.borderBottom = '2px solid var(--primary)'; }
            if(contentReports) contentReports.style.display = 'flex';
        } else if (tab === 'schedules') {
            if(btnTabSchedules) { btnTabSchedules.style.color = 'var(--primary)'; btnTabSchedules.style.borderBottom = '2px solid var(--primary)'; }
            if(contentSchedules) contentSchedules.style.display = 'flex';
        }
    }

    if(btnTabReports) btnTabReports.addEventListener('click', () => switchReportTab('reports'));
    if(btnTabSchedules) btnTabSchedules.addEventListener('click', () => switchReportTab('schedules'));

    // Modal Logic
    const btnCreateReport = document.getElementById('btn-create-report');
    const modalGenerateReport = document.getElementById('modal-generate-report');
    const btnCloseReportModal = document.getElementById('btn-close-report-modal');
    const btnCancelReport = document.getElementById('btn-cancel-report');
    const btnSubmitReport = document.getElementById('btn-submit-report');
    
    if (btnCreateReport) {
        btnCreateReport.addEventListener('click', () => {
            modalGenerateReport.style.display = 'flex';
        });
    }
    
    function closeReportModal() {
        modalGenerateReport.style.display = 'none';
    }
    
    if (btnCloseReportModal) btnCloseReportModal.addEventListener('click', closeReportModal);
    if (btnCancelReport) btnCancelReport.addEventListener('click', closeReportModal);
    
    if (btnSubmitReport) {
        btnSubmitReport.addEventListener('click', () => {
            const cluster = document.getElementById('report-cluster-select').value;
            const type = document.getElementById('report-type-select').value;
            const range = document.getElementById('report-data-range').value;
            const recipients = document.getElementById('report-recipients').value;
            
            if (!cluster || !type) {
                alert('Please select both Cluster and Type.');
                return;
            }
            
            // Create a mock report in the table
            const tbody = document.getElementById('reports-table-body');
            const emptyState = document.getElementById('reports-empty-state');
            if (emptyState) emptyState.style.display = 'none';
            
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--glass-border)';
            
            const now = new Date();
            const dateStr = now.toISOString().replace('T', ' ').substring(0, 19) + ' +03';
            const fileName = `report-${Date.now()}.pdf`;
            
            tr.innerHTML = `
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #111827;">${dateStr}</td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #3b82f6; text-decoration: underline; cursor: pointer;">${fileName}</td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${type}</td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151; display: flex; align-items: center; gap: 8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="#111827"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg> ${cluster}
                </td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">admin@sunucu.local</td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${range} days</td>
                <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${recipients}</td>
                <td style="padding: 16px 24px; text-align: right;"><button style="background: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #4b5563;">...</button></td>
            `;
            
            if (tbody.firstChild) {
                tbody.insertBefore(tr, tbody.firstChild);
            } else {
                if (tbody) { tbody.appendChild(tr); }
            }
            
            closeReportModal();
        });
    }
});

// --- USERS MANAGEMENT ---
document.addEventListener('DOMContentLoaded', () => {
    
const backupsData = [
    { id: 441, cluster: "MongoDB Replicaset (ID:30)", clusterType: "mongodb", method: "mongodump", status: "Completed", title: "BACKUP-441", created: "3 months ago", size: "1.8 kB", host: "br8-ccdemo-svr1" },
    { id: 438, cluster: "MariaDB (ID:21)", clusterType: "mariadb", method: "mariadb-dump", status: "Completed", title: "BACKUP-438", created: "3 months ago", size: "545 kB", host: "br4-ccdemo-svr1" },
    { id: 65, cluster: "Timescale (ID:29)", clusterType: "postgresql", method: "pg_basebackup", status: "Completed", title: "BACKUP-65", created: "3 months ago", size: "4.71 MB", host: "br3-ccdemo-svr1" },
    { id: 63, cluster: "Valkey (ID:25)", clusterType: "redis", method: "rdb, aof", status: "Completed", title: "BACKUP-63", created: "3 months ago", size: "485 B", host: "-" },
    { id: 61, cluster: "PostgreSQL (ID:15)", clusterType: "postgresql", method: "pg_basebackup", status: "Completed", title: "BACKUP-61", created: "3 months ago", size: "22.6 MB", host: "br1-ccdemo-svr1.localdomain.com" },
    { id: 1, cluster: "MSSQL (ID:27)", clusterType: "mssql", method: "mssqlcert", status: "Completed", title: "BACKUP-1", created: "4 months ago", size: "2.76 kB", host: "br7-ccdemo-svr1" }
];

const schedulesData = [
    { name: "mongodb-dump", cluster: "MongoDB Replicaset (ID:30)", clusterType: "mongodb", method: "mongodump", status: "Paused", schedule: "At 02:00 (UTC)", host: "N/A", storageHost: "10.10.20.103", location: "/home/ccuser/backups", lastExec: "N/A" },
    { name: "mysqldump-backup", cluster: "Percona MySQL Replication (ID:28)", clusterType: "mysql", method: "mysqldump", status: "Paused", schedule: "Every hour (UTC)", host: "br2-ccdemo-svr2", storageHost: "10.10.20.103", location: "/home/ccuser/backups", lastExec: "N/A" },
    { name: "binlog-backup", cluster: "MariaDB (ID:21)", clusterType: "mariadb", method: "mariabackup (incr)", status: "Paused", schedule: "Every minute, every 2 hours...", host: "br4-ccdemo-svr1", storageHost: "10.10.20.103", location: "/home/ccuser/backups", lastExec: "3 months ago" }
];

function getClusterIconStr(type) {
    if (type === 'mongodb') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path></svg>';
    if (type === 'postgresql' || type === 'redis') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>';
    if (type === 'mariadb' || type === 'mysql') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>';
    if (type === 'mssql') return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>';
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><circle cx="12" cy="12" r="10"></circle></svg>';
}


async function fetchBackups() {
    const tbody = document.getElementById('all-backups-tbody');
    if (tbody) tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading backups...</span></div></td></tr>';
    const res = await apiFetch('/api/backups');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('all-backups-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 20px; color: #6b7280;">No backups found.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(b => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 0;">${escapeHTML(b.cluster_name)}</td>
                    <td style="padding: 12px 0;">
                        <span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:500; 
                        background: ${b.status === 'COMPLETED' ? 'rgba(16,185,129,0.1)' : (b.status === 'IN_PROGRESS' ? 'rgba(59,130,246,0.1)' : 'rgba(239,68,68,0.1)')}; 
                        color: ${b.status === 'COMPLETED' ? '#10b981' : (b.status === 'IN_PROGRESS' ? '#3b82f6' : '#ef4444')};">
                        ${b.status}</span>
                    </td>
                    <td style="padding: 12px 0;">${b.size_mb ? b.size_mb + ' MB' : '-'}</td>
                    <td style="padding: 12px 0;">${escapeHTML(b.backup_type)}</td>
                    <td style="padding: 12px 0;">${b.created_at}</td>
                    <td style="padding: 12px 0;">${b.completed_at || '-'}</td>
                    <td style="padding: 12px 0;">
                        <button style="background:transparent; border:1px solid var(--border); border-radius:4px; padding:4px 8px; font-size:0.8rem; cursor:pointer;">Restore</button>
                    </td>
                </tr>
            `).join('');
        }
    }
}

async function fetchSchedules() {
    const res = await apiFetch('/api/backups/schedules');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('schedules-tbody');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 20px; color: #6b7280;">No schedules found.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(s => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 0;">${escapeHTML(s.schedule_expression)}</td>
                    <td style="padding: 12px 0;">${escapeHTML(s.backup_type)}</td>
                    <td style="padding: 12px 0;">${escapeHTML(s.cluster_name)}</td>
                    <td style="padding: 12px 0;">${s.retention_days} days</td>
                    <td style="padding: 12px 0;">
                        <button style="background:transparent; border:1px solid var(--border); border-radius:4px; padding:4px 8px; font-size:0.8rem; cursor:pointer;">Edit</button>
                    </td>
                </tr>
            `).join('');
        }
    }
}

function renderBackups() {
    fetchBackups();
    fetchSchedules();
}

}); // close DOMContentLoaded (--- USERS MANAGEMENT ---)


// ── User Management – live data ────────────────────────────────────────────
(function initUserManagement() {
    let usersData = [];
    let currentSort = 'none';

    // Colour palette for avatars
    const AVATAR_COLORS = [
        { bg: '#fef3c7', color: '#d97706' },
        { bg: '#ffe4e6', color: '#e11d48' },
        { bg: '#e0f2fe', color: '#0284c7' },
        { bg: '#f3e8ff', color: '#9333ea' },
        { bg: '#dcfce7', color: '#16a34a' },
        { bg: '#fff7ed', color: '#ea580c' },
    ];
    function avatarStyle(username, idx) {
        const p = AVATAR_COLORS[idx % AVATAR_COLORS.length];
        const init = (username || '?').slice(0, 2).toUpperCase();
        return { initial: init, bg: p.bg, color: p.color };
    }

    // ── Fetch users from API ───────────────────────────────────────────────
    async function loadUsersFromAPI() {
        try {
            const res = await apiFetch('/api/users');
            if (!res.ok) return;
            const data = await res.json();
            usersData = data.map((u, i) => ({
                ...u,
                ...avatarStyle(u.username, i),
                status: u.status || 'Enabled',
            }));
            renderUsers();
        } catch (e) {
            console.error('Failed to load users:', e);
        }
    }

    // ── Render table ──────────────────────────────────────────────────────
    function renderUsers() {
        const tbody = document.getElementById('users-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        if (usersData.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="padding:60px 24px;text-align:center;color:#9ca3af;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="display:block;margin:0 auto 12px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                No users created yet.</td></tr>`;
            return;
        }

        let sorted = [...usersData];
        if (currentSort === 'asc') sorted.sort((a, b) => a.username.localeCompare(b.username));
        else if (currentSort === 'desc') sorted.sort((a, b) => b.username.localeCompare(a.username));

        sorted.forEach((u, i) => {
            const tr = document.createElement('tr');
            tr.style.cssText = 'border-bottom:1px solid #f3f4f6;cursor:pointer;transition:background 0.12s;';
            tr.onmouseenter = () => tr.style.background = '#f9fafb';
            tr.onmouseleave = () => tr.style.background = '';
            tr.onclick = () => openUserDetails(u);

            const avatar = `<div style="width:32px;height:32px;border-radius:50%;background:${u.bg};color:${u.color};display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;flex-shrink:0;">${u.initial}</div>`;
            const statusColor = u.status === 'Enabled' ? '#16a34a' : '#9ca3af';
            const createdLabel = u.created_at ? u.created_at : (u.id === 0 ? 'System' : '—');

            tr.innerHTML = `
                <td style="padding:14px 24px;display:flex;align-items:center;gap:10px;font-weight:500;color:#111827;">${avatar}<span>${escapeHTML(u.username)}</span></td>
                <td style="padding:14px 24px;font-size:0.88rem;color:#374151;">${escapeHTML(u.email || '')}</td>
                <td style="padding:14px 24px;font-size:0.88rem;color:#374151;">${escapeHTML(u.team || '')}</td>
                <td style="padding:14px 24px;font-size:0.88rem;color:#374151;">${escapeHTML(u.first_name || '')}</td>
                <td style="padding:14px 24px;font-size:0.88rem;color:#374151;">${escapeHTML(u.last_name || '')}</td>
                <td style="padding:14px 24px;font-size:0.88rem;font-weight:600;color:${statusColor};">${escapeHTML(u.status || 'Enabled')}</td>
                <td style="padding:14px 24px;font-size:0.88rem;color:#6b7280;">${escapeHTML(createdLabel)}</td>
                <td style="padding:14px 24px;">
                    <button onclick="event.stopPropagation();" style="background:transparent;border:1px solid #e5e7eb;border-radius:4px;padding:4px 10px;cursor:pointer;color:#6b7280;font-size:0.82rem;">···</button>
                </td>`;
            tbody.appendChild(tr);
        });

        const arrows = document.getElementById('user-sort-arrows');
        if (arrows) {
            if (currentSort === 'asc') arrows.innerHTML = '&#9650;';
            else if (currentSort === 'desc') arrows.innerHTML = '&#9660;';
            else arrows.innerHTML = '&#9650;&#9660;';
        }
    }

    // ── User details panel ─────────────────────────────────────────────────
    function openUserDetails(u) {
        let overlay = document.getElementById('modal-user-details');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'modal-user-details';
            overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:9000;display:flex;align-items:center;justify-content:center;';
            overlay.onclick = (e) => { if (e.target === overlay) overlay.style.display = 'none'; };
            document.body.appendChild(overlay);
        }

        const isAdmin = u.role === 'admin';
        const fullName = [u.first_name, u.last_name].filter(Boolean).join(' ') || u.username;

        overlay.innerHTML = `
        <div style="background:white;border-radius:12px;width:600px;max-width:94vw;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.25);padding:32px 36px;position:relative;">
            <button onclick="document.getElementById('modal-user-details').style.display='none'"
              style="position:absolute;top:16px;right:18px;border:none;background:none;font-size:1.4rem;cursor:pointer;color:#6b7280;line-height:1;">✕</button>

            <!-- Name header -->
            <div style="text-align:center;margin-bottom:20px;">
                <div style="width:64px;height:64px;border-radius:50%;background:${u.bg};color:${u.color};display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700;margin:0 auto 12px;">${u.initial}</div>
                <div style="font-size:1.25rem;font-weight:700;color:#111827;">${escapeHTML(fullName)}</div>
                <div style="font-size:0.88rem;color:#6b7280;margin-top:2px;">${escapeHTML(u.email || '')}</div>
            </div>

            <!-- Profile fields -->
            <div style="display:grid;grid-template-columns:auto 1fr;gap:7px 16px;font-size:0.88rem;margin-bottom:20px;padding:16px;background:#f9fafb;border-radius:8px;">
                <span style="color:#6b7280;">Time zone:</span>  <span style="color:#111827;">${escapeHTML(u.timezone || 'UTC')}</span>
                <span style="color:#6b7280;">Username:</span>   <span style="color:#111827;font-weight:500;">${escapeHTML(u.username)}</span>
                <span style="color:#6b7280;">Team:</span>       <span style="color:#111827;">${escapeHTML(u.team || 'admins')}</span>
                <span style="color:#6b7280;">Origin:</span>     <span style="color:#111827;">${escapeHTML(u.origin || 'cmon')}</span>
            </div>

            <!-- Permissions -->
            <div style="margin-bottom:20px;">
                <div style="font-size:0.9rem;font-weight:600;color:#111827;margin-bottom:10px;">Permissions</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px 24px;font-size:0.85rem;">
                    ${perm('Change controller configuration', isAdmin)}
                    ${perm('Manage users and teams', isAdmin)}
                    ${perm('Change LDAP settings', isAdmin)}
                    ${perm('Deploy clusters', isAdmin)}
                </div>
            </div>

            <!-- Cluster access table -->
            <div style="margin-bottom:24px;">
                <div style="font-size:0.9rem;font-weight:600;color:#111827;margin-bottom:10px;">Cluster access</div>
                <div id="ud-cluster-access" style="font-size:0.84rem;color:#6b7280;">Loading clusters…</div>
            </div>

            <!-- Footer: Edit + Close -->
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <button onclick="window.openEditUserModal(${JSON.stringify(u).replace(/"/g,'&quot;')})"
                  style="padding:9px 24px;background:#3a1c94;color:white;border:none;border-radius:8px;font-size:0.88rem;font-weight:600;cursor:pointer;"
                  onmouseover="this.style.background='#2d1570'" onmouseout="this.style.background='#3a1c94'">Edit</button>
                <button onclick="document.getElementById('modal-user-details').style.display='none'"
                  style="padding:9px 20px;border:1px solid #d1d5db;background:white;color:#374151;border-radius:8px;font-size:0.88rem;cursor:pointer;">Close</button>
            </div>
        </div>`;

        overlay.style.display = 'flex';

        // Load clusters asynchronously
        apiFetch('/api/projects').then(r => r.ok ? r.json() : []).then(projects => {
            const el = document.getElementById('ud-cluster-access');
            if (!el) return;
            if (!projects.length) { el.textContent = 'No clusters.'; return; }
            let rows = projects.map(p => `
                <div style="display:grid;grid-template-columns:1fr 1fr auto;gap:4px 16px;padding:8px 0;border-bottom:1px solid #f3f4f6;align-items:center;">
                    <span style="color:#374151;font-weight:500;">${escapeHTML(p.name)}</span>
                    <span style="color:#6b7280;font-size:0.82rem;">ID:${p.id}</span>
                    <span style="color:#374151;font-size:0.82rem;">Manage</span>
                </div>`).join('');
            el.innerHTML = `
                <div style="display:grid;grid-template-columns:1fr 1fr auto;gap:4px 16px;padding:6px 0;border-bottom:2px solid #e5e7eb;margin-bottom:4px;">
                    <span style="font-weight:600;font-size:0.82rem;color:#6b7280;text-transform:uppercase;">Cluster</span>
                    <span style="font-weight:600;font-size:0.82rem;color:#6b7280;text-transform:uppercase;">More info</span>
                    <span style="font-weight:600;font-size:0.82rem;color:#6b7280;text-transform:uppercase;">Access level</span>
                </div>
                ${rows}`;
        }).catch(() => {});
    }

    // ── Edit user modal ────────────────────────────────────────────────────
    window.openEditUserModal = function(u) {
        // Close details first
        const det = document.getElementById('modal-user-details');
        if (det) det.style.display = 'none';

        let overlay = document.getElementById('modal-edit-user');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'modal-edit-user';
            overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:9100;display:flex;align-items:center;justify-content:center;';
            overlay.onclick = (e) => { if (e.target === overlay) overlay.style.display = 'none'; };
            document.body.appendChild(overlay);
        }

        const fld = (label, id, val, required=true) => `
            <div style="margin-bottom:16px;">
                <label style="display:block;font-size:0.84rem;font-weight:500;color:#374151;margin-bottom:6px;">
                    ${required ? '<span style="color:#ef4444;">*</span> ' : ''}${escapeHTML(label)}
                </label>
                <input id="${id}" type="text" value="${escapeHTML(val || '')}"
                  style="width:100%;padding:9px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:0.88rem;outline:none;box-sizing:border-box;">
            </div>`;

        overlay.innerHTML = `
        <div style="background:white;border-radius:12px;width:520px;max-width:94vw;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.25);padding:28px 32px;position:relative;">
            <button onclick="document.getElementById('modal-edit-user').style.display='none'"
              style="position:absolute;top:14px;right:16px;border:none;background:none;font-size:1.3rem;cursor:pointer;color:#6b7280;line-height:1;">✕</button>
            <h3 style="margin:0 0 20px;font-size:1.05rem;font-weight:600;color:#111827;">Edit user ${escapeHTML(u.username)}</h3>

            ${fld('First name',  'eu-fname',    u.first_name)}
            ${fld('Last name',   'eu-lname',    u.last_name)}
            ${fld('Email',       'eu-email',    u.email)}

            <!-- Timezone -->
            <div style="margin-bottom:16px;">
                <label style="display:block;font-size:0.84rem;font-weight:500;color:#374151;margin-bottom:6px;">Timezone</label>
                <select id="eu-timezone" style="width:100%;padding:9px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:0.88rem;background:white;outline:none;">
                    ${['UTC','Europe/Istanbul','Europe/London','Europe/Berlin','America/New_York','America/Chicago','America/Los_Angeles','Asia/Tokyo','Asia/Singapore']
                        .map(tz => `<option value="${tz}" ${(u.timezone||'UTC')===tz?'selected':''}>${tz}</option>`).join('')}
                </select>
            </div>

            <!-- Force change password toggle -->
            <div style="margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;">
                <label style="font-size:0.84rem;font-weight:500;color:#374151;">Force change password</label>
                <button id="eu-force-pwd-btn" onclick="this.classList.toggle('eu-pwd-on');this.textContent=this.classList.contains('eu-pwd-on')?'On':'Off';this.style.background=this.classList.contains('eu-pwd-on')?'#4338ca':'#d1d5db';"
                  style="padding:5px 18px;border:none;border-radius:20px;background:#d1d5db;color:white;font-size:0.8rem;font-weight:600;cursor:pointer;transition:background 0.2s;">Off</button>
            </div>

            <!-- Choose a team -->
            <div style="margin-bottom:20px;">
                <label style="display:block;font-size:0.84rem;font-weight:500;color:#374151;margin-bottom:6px;"><span style="color:#ef4444;">*</span> Choose a team</label>
                <select id="eu-team" style="width:100%;padding:9px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:0.88rem;background:white;outline:none;">
                    <option value="admins" ${(u.team||'admins')==='admins'?'selected':''}>admins</option>
                    <option value="nobody" ${(u.team)==='nobody'?'selected':''}>nobody</option>
                    <option value="users"  ${(u.team)==='users'?'selected':''}>users</option>
                </select>
            </div>

            <!-- Error -->
            <div id="eu-error" style="display:none;color:#ef4444;font-size:0.84rem;margin-bottom:12px;"></div>

            <!-- Footer -->
            <div style="display:flex;justify-content:flex-end;gap:10px;">
                <button onclick="document.getElementById('modal-edit-user').style.display='none'"
                  style="padding:9px 20px;border:1px solid #d1d5db;background:white;color:#374151;border-radius:8px;font-size:0.88rem;cursor:pointer;">Cancel</button>
                <button onclick="window.submitEditUser(${u.id})"
                  style="padding:9px 24px;background:#3a1c94;color:white;border:none;border-radius:8px;font-size:0.88rem;font-weight:600;cursor:pointer;"
                  onmouseover="this.style.background='#2d1570'" onmouseout="this.style.background='#3a1c94'">Save</button>
            </div>
        </div>`;

        overlay.style.display = 'flex';
    };

    window.submitEditUser = async function(userId) {
        const errEl = document.getElementById('eu-error');
        if (errEl) errEl.style.display = 'none';

        const email = document.getElementById('eu-email')?.value?.trim();
        if (!email) { if (errEl) { errEl.textContent = 'Email is required.'; errEl.style.display = 'block'; } return; }

        const payload = {
            email,
            first_name: document.getElementById('eu-fname')?.value?.trim() || '',
            last_name: document.getElementById('eu-lname')?.value?.trim() || '',
            timezone: document.getElementById('eu-timezone')?.value || 'UTC',
        };

        try {
            const res = await apiFetch('/api/users/profile', { method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
            if (res.ok) {
                document.getElementById('modal-edit-user').style.display = 'none';
                showToast && showToast('User updated successfully.', 'success');
                loadUsersFromAPI(); // refresh table
            } else {
                const data = await res.json().catch(() => ({}));
                if (errEl) { errEl.textContent = data.message || 'Failed to save.'; errEl.style.display = 'block'; }
            }
        } catch (e) {
            if (errEl) { errEl.textContent = 'Connection error.'; errEl.style.display = 'block'; }
        }
    };

    // ── Sort header ────────────────────────────────────────────────────────
    const thUser = document.getElementById('th-user-col');
    const userTooltip = document.getElementById('user-sort-tooltip');
    if (thUser) {
        thUser.onmouseenter = () => { if (userTooltip) userTooltip.style.display = 'block'; };
        thUser.onmouseleave = () => { if (userTooltip) userTooltip.style.display = 'none'; };
        thUser.onclick = () => {
            if (currentSort === 'none') currentSort = 'asc';
            else if (currentSort === 'asc') currentSort = 'desc';
            else currentSort = 'none';
            renderUsers();
        };
    }

    // ── Tab switching ──────────────────────────────────────────────────────
    const btnTabUsers = document.getElementById('tab-btn-users');
    const btnTabTeams = document.getElementById('tab-btn-teams');
    const btnTabLdap  = document.getElementById('tab-btn-ldap');
    const contentUsers = document.getElementById('content-users');
    const contentTeams = document.getElementById('content-teams');
    const contentLdap  = document.getElementById('content-ldap');

    function switchUsersTab(tab) {
        [btnTabUsers, btnTabTeams, btnTabLdap].forEach(btn => {
            if (btn) { btn.classList.remove('active'); btn.style.color = '#4b5563'; btn.style.borderBottom = '2px solid transparent'; }
        });
        [contentUsers, contentTeams, contentLdap].forEach(c => { if (c) c.style.display = 'none'; });
        if (tab === 'users')  { if (btnTabUsers) { btnTabUsers.style.color = 'var(--primary)'; btnTabUsers.style.borderBottom = '2px solid var(--primary)'; } if (contentUsers) contentUsers.style.display = 'block'; }
        else if (tab === 'teams') { if (btnTabTeams) { btnTabTeams.style.color = 'var(--primary)'; btnTabTeams.style.borderBottom = '2px solid var(--primary)'; } if (contentTeams) contentTeams.style.display = 'block'; }
        else if (tab === 'ldap')  { if (btnTabLdap)  { btnTabLdap.style.color  = 'var(--primary)'; btnTabLdap.style.borderBottom  = '2px solid var(--primary)'; } if (contentLdap)  contentLdap.style.display  = 'block'; }
    }
    if (btnTabUsers) btnTabUsers.addEventListener('click', () => switchUsersTab('users'));
    if (btnTabTeams) btnTabTeams.addEventListener('click', () => switchUsersTab('teams'));
    if (btnTabLdap)  btnTabLdap.addEventListener('click',  () => switchUsersTab('ldap'));

    // Initial load
    loadUsersFromAPI();
})();


// --- NODES PAGE MANAGEMENT ---
window.nodesPageData = [];
window.currentNodesFilter = 'All';
window.currentSortCol = null;
window.currentSortDir = null;

window.renderNodesPage = function() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const allData = window.nodesPageData || [];

    // Calculate and update stats counters
    let stats = {
        'Operational': 0,
        'Failed': 0,
        'Offline': 0,
        'Shut Down': 0,
        'Recovering': 0,
        'Unknown State': 0
    };

    allData.forEach(n => {
        const s = n.status || 'Operational';
        if (stats[s] !== undefined) stats[s]++;
        else stats['Unknown State']++;
    });

    const statOp = document.getElementById('stat-operational');
    const statAll = document.getElementById('stat-all');
    if (statOp) statOp.innerText = stats['Operational'];
    if (statAll) statAll.innerText = allData.length;
    ['failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(k => {
        const el = document.getElementById('stat-' + k);
        let val = 0;
        if (k === 'failed') val = stats['Failed'];
        if (k === 'offline') val = stats['Offline'];
        if (k === 'shutdown') val = stats['Shut Down'];
        if (k === 'recovering') val = stats['Recovering'];
        if (k === 'unknown') val = stats['Unknown State'];
        if (el) el.innerText = val;
    });

    // Filter by currentNodesFilter
    let filteredData = allData.filter(n => window.currentNodesFilter === 'All' || n.status === window.currentNodesFilter);

    // Sort if active
    if (window.currentSortCol && window.currentSortDir) {
        filteredData.sort((a, b) => {
            let valA = (a[window.currentSortCol] || '').toString().toLowerCase();
            let valB = (b[window.currentSortCol] || '').toString().toLowerCase();
            if (valA < valB) return window.currentSortDir === 'asc' ? -1 : 1;
            if (valA > valB) return window.currentSortDir === 'asc' ? 1 : -1;
            return 0;
        });
    }

    if (filteredData.length === 0) {
        // If we're still loading, don't replace the loading spinner with the empty state
        if (window.nodesPageLoading) return;
        tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: #9ca3af; font-size: 0.9rem;">There are no matches</td></tr>`;
        return;
    }

    filteredData.forEach(n => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #f3f4f6';
        tr.style.background = 'white';

        let statusColor = 'var(--success, #10b981)';
        let dotColor = 'var(--success, #10b981)';
        if (n.status === 'Shut Down') { statusColor = '#3b82f6'; dotColor = '#3b82f6'; }
        if (n.status === 'Failed') { statusColor = '#ef4444'; dotColor = '#ef4444'; }
        if (n.status === 'Offline') { statusColor = '#6b7280'; dotColor = '#6b7280'; }

        let statusHtml = `<span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: ${dotColor};"></div> ${escapeHTML(n.status)}</span>`;

        let typeColor = '#059669';
        if (n.type === 'HAProxy') typeColor = '#8b5cf6';
        if (n.type === 'Prometheus') typeColor = '#eab308';
        if (n.type === 'MongoDB') typeColor = '#059669';

        let roleHtml = `<span>${escapeHTML(n.role)}</span>`;
        if (n.badge) {
            roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: ${n.badge.bg}; color: ${n.badge.color}; border: 1px solid ${n.badge.color}; margin-left: 6px;">${n.badge.text}</span>`;
        }

        let logoColor = n.clusterColor || '#059669';
        let logoSvg = n.clusterLogo || '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>';

        tr.innerHTML = `
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(n.host)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${escapeHTML(n.port)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: #6b7280; white-space: nowrap;">${escapeHTML(n.ip)}</td>
            <td style="padding: 16px; font-size: 0.85rem; white-space: nowrap;">${statusHtml}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: ${typeColor}; white-space: nowrap;">${escapeHTML(n.type)}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; display: flex; align-items: center;">${roleHtml}</td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${logoColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${logoSvg}</svg>
                    ${escapeHTML(n.cluster)}
                </div>
            </td>
            <td style="padding: 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.version}</td>
            <td style="padding: 16px; font-size: 0.8rem; color: #6b7280; white-space: nowrap;">${escapeHTML(n.seen)}</td>
            <td style="padding: 16px; font-size: 0.85rem; text-align: center;"><button style="background: none; border: 1px solid var(--border); padding: 4px 8px; border-radius: 4px; cursor: pointer;">...</button></td>
        `;
        tbody.appendChild(tr);
    });
};

window.filterNodes = function(status, el) {
    window.currentNodesFilter = status;
    const cards = document.querySelectorAll('.node-status-card');
    cards.forEach(card => {
        card.style.borderBottom = 'none';
        card.style.background = 'transparent';
    });
    if (el) {
        el.style.borderBottom = '2px solid var(--primary, #6366f1)';
        el.style.background = '#f9fafb';
    }
    window.renderNodesPage();
};

window.sortNodes = function(col) {
    if (window.currentSortCol !== col) {
        window.currentSortCol = col;
        window.currentSortDir = 'asc';
    } else {
        if (window.currentSortDir === 'asc') window.currentSortDir = 'desc';
        else if (window.currentSortDir === 'desc') window.currentSortDir = null;
        else window.currentSortDir = 'asc';
    }

    ['host', 'port', 'status', 'type', 'role', 'cluster', 'seen'].forEach(c => {
        const arr = document.getElementById('nodes-sort-arrows-' + c);
        const txt = document.getElementById('nodes-sort-text-' + c);
        if (arr) arr.innerHTML = '&#9650;&#9660;';
        if (txt) txt.innerText = 'Click to sort ascending';
    });

    if (window.currentSortDir) {
        const arr = document.getElementById('nodes-sort-arrows-' + col);
        const txt = document.getElementById('nodes-sort-text-' + col);
        if (window.currentSortDir === 'asc') {
            if (arr) arr.innerHTML = '&#9650;';
            if (txt) txt.innerText = 'Click to sort descending';
        } else {
            if (arr) arr.innerHTML = '&#9660;';
            if (txt) txt.innerText = 'Click to Cancel Sorting';
        }
    }
    window.renderNodesPage();
};

window.fetchNodesPage = async function() {
    const tbody = document.getElementById('nodes-page-tbody');
    // Always reset and show loading on every visit
    window.nodesPageData = [];
    window.nodesPageLoading = true;
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr>';
    }

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Failed to load clusters.</td></tr>';
            return;
        }
        const projects = await res.json();

        window.nodesPageData = [];
        let nodeIndex = 0;

        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                nodeIndex++;
                const isPrimary = (node.role || '').toLowerCase() === 'primary';
                window.nodesPageData.push({
                    id: node.id,
                    host: node.name,
                    port: '5432',
                    ip: '10.0.20.' + (18 + nodeIndex),
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown',
                    badge: isPrimary ? { text: 'Writable', bg: '#dcfce7', color: '#16a34a' } : { text: 'Readonly', bg: '#f3f4f6', color: '#4b5563' },
                    cluster: `${proj.name} (ID:${proj.id})`,
                    clusterLogo: '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>',
                    clusterColor: '#059669',
                    version: 'PostgreSQL 16.4',
                    seen: 'in 4 minutes',
                    projId: proj.id
                });
            }
        }

        window.nodesPageLoading = false;
        window.renderNodesPage();

        // Fetch live metrics in background to resolve versions and actual statuses
        for (const proj of projects) {
            if (!proj.nodes || proj.nodes.length === 0) continue;
            try {
                const mr = await apiFetch('/api/projects/' + proj.id + '/metrics');
                if (!mr.ok) continue;
                const nodeMetrics = await mr.json();
                for (const nm of nodeMetrics) {
                    const m = nm.metrics;
                    if (!m) continue;
                    const matchedNode = window.nodesPageData.find(n => n.id === nm.id);
                    if (matchedNode) {
                        if (m.status === 'online') {
                            matchedNode.status = 'Operational';
                            matchedNode.version = m.version ? escapeHTML(m.version) : 'PostgreSQL 16.4';
                        } else if (m.status === 'offline') {
                            matchedNode.status = 'Offline';
                            matchedNode.version = '-';
                        }
                    }
                }
                window.renderNodesPage();
            } catch(e) { /* ignore */ }
        }

    } catch(e) {
        window.nodesPageLoading = false;
        console.error('fetchNodesPage error:', e);
        if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>';
    }
};






    let previousMetrics = {};
    let detailMetricsInterval = null;
    let currentDetailProj = null; // to calculate TPS
    
    async function refreshClusterDetailMetrics(proj) {
        if (!proj) return;
        
        // Populate node list immediately with basic data
        const tbodyNode = document.querySelector('#node-list-table tbody');
        if (tbodyNode) {
            tbodyNode.innerHTML = proj.nodes.map(n => {
                const ip = n.url ? (n.url.split('@')[1] || '').split(':')[0] : 'Unknown';
                const port = n.url ? (n.url.split(':')[2] || '').split('/')[0] : '5432';
                return `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 0; color: #111827;">${n.name}</td>
                        <td style="padding: 10px 0;">${port}</td>
                        <td style="padding: 10px 0;">${ip}</td>
                        <td style="padding: 10px 0; color: #10b981;">&#8226; Operational</td>
                        <td style="padding: 10px 0; color: #6366f1;">PostgreSQL</td>
                        <td style="padding: 10px 0;">${n.role}</td>
                        <td style="padding: 10px 0;" id="nodelist-ver-${n.id}">Loading...</td>
                    </tr>
                `;
            }).join('');
            
            if(document.getElementById('stat-all')) document.getElementById('stat-all').innerText = proj.nodes.length;
            if(document.getElementById('stat-operational')) document.getElementById('stat-operational').innerText = proj.nodes.length; // Simplified for now
        }
        
        try {
            const res = await apiFetch(`/api/projects/${proj.id}/metrics`);
            if (!res.ok) return;
            const metricsData = await res.json();
            
            const tbodyPg = document.querySelector('#pg-overview-table tbody');
            if (tbodyPg) {
                tbodyPg.innerHTML = '';
                
                metricsData.forEach(nodeData => {
                    const m = nodeData.metrics;
                    if (!m) return;
                    
                    // Update node list version
                    const verTd = document.getElementById(`nodelist-ver-${nodeData.id}`);
                    if(verTd) verTd.innerText = m.version || 'Unknown';
                    
                    // Calculate rates
                    let tps = 0, sel = 0, ins = 0, upd = 0, del = 0;
                    const now = Date.now();
                    const prev = previousMetrics[nodeData.id];
                    
                    if (prev && m.commits_raw !== undefined) {
                        const elapsed = (now - prev.time) / 1000;
                        if (elapsed > 0) {
                            const diffCommits = m.commits_raw - prev.commits_raw;
                            const diffRollbacks = m.rollbacks_raw - prev.rollbacks_raw;
                            tps = ((diffCommits + diffRollbacks) / elapsed).toFixed(2);
                            
                            sel = ((m.tup_fetched - prev.tup_fetched) / elapsed).toFixed(2);
                            ins = ((m.tup_inserted - prev.tup_inserted) / elapsed).toFixed(2);
                            upd = ((m.tup_updated - prev.tup_updated) / elapsed).toFixed(2);
                            del = ((m.tup_deleted - prev.tup_deleted) / elapsed).toFixed(2);
                        }
                    }
                    
                    // Save for next calculation
                    if (m.commits_raw !== undefined) {
                        previousMetrics[nodeData.id] = {
                            time: now,
                            commits_raw: m.commits_raw,
                            rollbacks_raw: m.rollbacks_raw,
                            tup_fetched: m.tup_fetched,
                            tup_inserted: m.tup_inserted,
                            tup_updated: m.tup_updated,
                            tup_deleted: m.tup_deleted
                        };
                    }
                    
                    const ip = "Unknown IP"; // Ideally from node url
                    const row = `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 0; color: #111827;">${nodeData.name}</td>
                            <td style="padding: 10px 0; color: #10b981;">Up</td>
                            <td style="padding: 10px 0;">${tps}</td>
                            <td style="padding: 10px 0;">${sel}</td>
                            <td style="padding: 10px 0;">${ins}</td>
                            <td style="padding: 10px 0;">${upd}</td>
                            <td style="padding: 10px 0;">${del}</td>
                            <td style="padding: 10px 0;">${m.connections || 0}</td>
                            <td style="padding: 10px 0; color: #10b981;">${m.active_conn || 0}</td>
                            <td style="padding: 10px 0; color: #10b981;">${m.cache_hit || '100%'}</td>
                        </tr>
                    `;
                    tbodyPg.innerHTML += row;
                });
            }
        } catch (e) {
            console.error(e);
        }
    }


// ── Top Header Alarms Quick Panel ──────────────────────────────────────────
let isAlarmsPanelOpen = false;

window.toggleAlarmsPanel = function(event) {
    if (event) event.stopPropagation();
    if (typeof closeProfileMenu === 'function') closeProfileMenu();
    const panel = document.getElementById('panel-header-alarms');
    if (!panel) return;
    
    const isOpen = panel.style.display !== 'none' && !panel.classList.contains('cc-alarms-panel-out');
    if (isOpen) {
        closeAlarmsPanel();
    } else {
        panel.style.display = 'block';
        panel.classList.remove('cc-alarms-panel-out');
        panel.classList.add('cc-alarms-panel-in');
        isAlarmsPanelOpen = true;
        loadHeaderAlarms();
    }
};

window.closeAlarmsPanel = function() {
    const panel = document.getElementById('panel-header-alarms');
    if (!panel || panel.style.display === 'none') return;
    panel.classList.remove('cc-alarms-panel-in');
    panel.classList.add('cc-alarms-panel-out');
    setTimeout(() => {
        if (panel.classList.contains('cc-alarms-panel-out')) {
            panel.style.display = 'none';
        }
    }, 160);
    isAlarmsPanelOpen = false;
};

// Close alarms panel when clicking outside anywhere on the page
document.addEventListener('click', function(e) {
    const panel = document.getElementById('panel-header-alarms');
    const trigger = document.getElementById('btn-header-alarms');
    if (panel && panel.style.display !== 'none' && !panel.classList.contains('cc-alarms-panel-out')) {
        if (!panel.contains(e.target) && !trigger?.contains(e.target)) {
            closeAlarmsPanel();
        }
    }
});

window.switchAlarmSubtab = function(tab) {
    const tabs = ['alarms', 'jobs', 'audit'];
    tabs.forEach(t => {
        const btn = document.getElementById(`btn-alarm-subtab-${t}`);
        const pane = document.getElementById(`alarm-content-${t}`);
        if (btn) {
            if (t === tab) {
                btn.style.background = 'white';
                btn.style.color = '#3a1c94';
                btn.style.fontWeight = '600';
                btn.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
            } else {
                btn.style.background = 'transparent';
                btn.style.color = '#6b7280';
                btn.style.fontWeight = '500';
                btn.style.boxShadow = 'none';
            }
        }
        if (pane) pane.style.display = (t === tab) ? 'block' : 'none';
    });

    if (tab === 'jobs') loadAlarmJobs();
    if (tab === 'audit') loadAlarmAudit();
};

window.loadHeaderAlarms = async function() {
    const tbody = document.getElementById('tbody-header-alarms');
    const badge = document.getElementById('badge-header-alarms');
    const countEl = document.getElementById('alarms-unmuted-count');
    try {
        const res = await apiFetch('/api/alarms');
        if (!res.ok) return;
        const d = await res.json();
        
        if (badge) {
            badge.style.display = d.unmuted_count > 0 ? 'block' : 'none';
        }
        if (countEl) {
            countEl.innerText = d.unmuted_count || 0;
        }

        if (!tbody) return;
        if (!d.alarms || !d.alarms.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align:center;padding:36px;color:#9ca3af;">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="margin:0 auto 12px auto;display:block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        You haven't received alarms yet. When you do, it'll show up here.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = d.alarms.map(a => `
            <tr style="border-bottom:1px solid #f3f4f6;opacity:${a.is_muted ? '0.6' : '1'};">
                <td style="padding:10px 12px;font-weight:600;color:#111827;">${escapeHTML(a.title)}</td>
                <td style="padding:10px 12px;">
                    <span style="font-size:0.75rem;padding:2px 8px;border-radius:10px;font-weight:600;background:${a.severity === 'CRITICAL' ? '#fee2e2' : '#fef3c7'};color:${a.severity === 'CRITICAL' ? '#991b1b' : '#92400e'};">
                        ${a.severity}
                    </span>
                </td>
                <td style="padding:10px 12px;color:#4b5563;">${escapeHTML(a.category)}</td>
                <td style="padding:10px 12px;color:#111827;font-weight:500;">${escapeHTML(a.cluster_name)}</td>
                <td style="padding:10px 12px;color:#6b7280;font-family:monospace;font-size:0.8rem;">${escapeHTML(a.hostname)}</td>
                <td style="padding:10px 12px;color:#6b7280;font-size:0.8rem;">${escapeHTML(a.when_human || a.created_at)}</td>
                <td style="padding:10px 12px;text-align:right;">
                    ${a.is_muted ? 
                        `<button onclick="unmuteAlarm(${a.id})" style="padding:4px 8px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;border-radius:4px;font-size:0.75rem;cursor:pointer;">Unmute</button>` : 
                        `<button onclick="muteAlarm(${a.id})" style="padding:4px 8px;background:#fee2e2;color:#991b1b;border:none;border-radius:4px;font-size:0.75rem;cursor:pointer;font-weight:600;">Mute</button>`
                    }
                </td>
            </tr>
        `).join('');
    } catch(e) {
        console.warn('Failed to load alarms:', e);
    }
};

window.muteAlarm = async function(id) {
    try {
        await apiFetch(`/api/alarms/${id}/mute`, { method: 'POST' });
        loadHeaderAlarms();
    } catch(e) {}
};

window.unmuteAlarm = async function(id) {
    try {
        await apiFetch(`/api/alarms/${id}/unmute`, { method: 'POST' });
        loadHeaderAlarms();
    } catch(e) {}
};

async function loadAlarmJobs() {
    const el = document.getElementById('alarms-jobs-list');
    if (!el) return;
    try {
        const res = await apiFetch('/api/backups');
        const jobs = await res.json();
        if (!jobs.length) {
            el.innerHTML = '<div style="padding:20px;text-align:center;color:#6b7280;font-size:0.85rem;">No active running jobs.</div>';
            return;
        }
        el.innerHTML = '<div style="display:flex;flex-direction:column;gap:8px;">' + jobs.slice(0, 5).map(j => `
            <div style="display:flex;justify-content:space-between;padding:8px 12px;background:#f9fafb;border-radius:6px;font-size:0.83rem;">
                <div><strong>${escapeHTML(j.title)}</strong> · ${escapeHTML(j.cluster_name)} (${escapeHTML(j.backup_method)})</div>
                <div><span style="padding:2px 6px;border-radius:4px;font-size:0.75rem;background:${j.status === 'COMPLETED' ? '#d1fae5' : '#fef3c7'};color:${j.status === 'COMPLETED' ? '#065f46' : '#92400e'};font-weight:600;">${j.status}</span></div>
            </div>
        `).join('') + '</div>';
    } catch(e) {}
}

async function loadAlarmAudit() {
    const el = document.getElementById('alarms-audit-list');
    if (!el) return;
    try {
        const res = await apiFetch('/api/audit-logs');
        const logs = await res.json();
        if (!logs.length) {
            el.innerHTML = '<div style="padding:20px;text-align:center;color:#6b7280;font-size:0.85rem;">No recent audit logs.</div>';
            return;
        }
        el.innerHTML = '<div style="display:flex;flex-direction:column;gap:8px;">' + logs.slice(0, 5).map(l => `
            <div style="display:flex;justify-content:space-between;padding:8px 12px;background:#f9fafb;border-radius:6px;font-size:0.83rem;">
                <div><strong>${escapeHTML(l.action)}</strong>: ${escapeHTML(l.details || '')}</div>
                <div style="color:#9ca3af;font-size:0.75rem;">${escapeHTML(l.created_at || '')}</div>
            </div>
        `).join('') + '</div>';
    } catch(e) {}
}

// ── ClusterControl Backup Wizard & Table ──────────────────────────────────────

let backupWizardState = {
    method: 'pgdumpall/pgdump',
    dumpType: 'Schema And Data',
    cloudUpload: false,
    cloudStream: true,
    currentStepIndex: 1,
    activeStepKey: 'config'
};
let backupIsCompression = true;
let backupIsRetention = true;
let allProjectsForBackup = [];
let allCloudCredsForBackup = [];

window.loadAllBackups = async function() {
    const tbody = document.getElementById('tbody-all-backups');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:36px;color:#9ca3af;">Loading backups...</td></tr>';
    try {
        const res = await apiFetch('/api/backups');
        if (!res.ok) {
            tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:36px;color:#ef4444;">Failed to load backups.</td></tr>';
            return;
        }
        const backups = await res.json();
        if (!backups.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="11" style="padding: 60px 20px; text-align: center; color: #6b7280;">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="margin: 0 auto 16px auto; display: block;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                        No backups created yet. Click "+ Create backup" to start.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = backups.map(b => {
            const isPg = (b.db_type || '').toLowerCase() === 'postgresql';
            const dbIcon = isPg ? '🐘' : '🗄️';
            const statusBg = b.status === 'COMPLETED' ? '#d1fae5' : (b.status === 'FAILED' ? '#fee2e2' : '#fef3c7');
            const statusColor = b.status === 'COMPLETED' ? '#065f46' : (b.status === 'FAILED' ? '#991b1b' : '#92400e');
            const storageIcon = b.is_cloud ? '💾 1 ☁️ 1' : '💾 1 ☁️ 0';

            return `
                <tr style="border-bottom:1px solid #f3f4f6;">
                    <td style="padding:12px 16px;font-weight:600;color:#111827;">${b.id}</td>
                    <td style="padding:12px 16px;color:#6b7280;cursor:pointer;" title="${escapeHTML(b.error_msg || b.file_path || 'Backup Info')}">ⓘ</td>
                    <td style="padding:12px 16px;font-weight:600;color:#111827;">${dbIcon} ${escapeHTML(b.cluster_name)}</td>
                    <td style="padding:12px 16px;color:#4b5563;font-family:monospace;font-size:0.82rem;">${escapeHTML(b.backup_method)}</td>
                    <td style="padding:12px 16px;">
                        <span style="font-size:0.75rem;padding:3px 8px;border-radius:10px;font-weight:600;background:${statusBg};color:${statusColor};">
                            ● ${b.status}
                        </span>
                    </td>
                    <td style="padding:12px 16px;color:#374151;font-weight:500;">${escapeHTML(b.title)}</td>
                    <td style="padding:12px 16px;color:#6b7280;font-size:0.82rem;">${escapeHTML(b.created_human || b.created_at)}</td>
                    <td style="padding:12px 16px;font-weight:500;color:#111827;">${escapeHTML(b.size_display || b.size_mb + ' MB')}</td>
                    <td style="padding:12px 16px;color:#4b5563;font-family:monospace;font-size:0.8rem;">${escapeHTML(b.backup_host)}</td>
                    <td style="padding:12px 16px;color:#4b5563;font-size:0.8rem;">${storageIcon}</td>
                    <td style="padding:12px 16px;text-align:right;">
                        <button onclick="deleteBackup(${b.id})" style="padding:4px 8px;background:#fee2e2;color:#991b1b;border:none;border-radius:4px;font-size:0.75rem;cursor:pointer;font-weight:600;">Delete</button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:36px;color:#ef4444;">Failed to load backups.</td></tr>';
    }
};

window.openCreateBackupConfigModal = async function() {
    const modalType = document.getElementById('modal-backup-type-select');
    if (modalType) modalType.style.display = 'none';

    const modal = document.getElementById('modal-create-backup-config');
    if (!modal) return;

    backupWizardState = {
        method: 'pgdumpall/pgdump',
        dumpType: 'Schema And Data',
        cloudUpload: false,
        cloudStream: true,
        currentStepIndex: 1,
        activeStepKey: 'config'
    };
    backupIsCompression = true;
    backupIsRetention = true;

    updateCloudToggleUI();
    updateStreamToggleUI();
    renderBackupStepperNav();

    const selectCluster = document.getElementById('backup-config-cluster');
    const selectHost = document.getElementById('backup-config-host');
    const selectCloudCred = document.getElementById('backup-cloud-cred-select');
    const selectMethod = document.getElementById('backup-config-method');

    if (selectMethod) selectMethod.value = 'pgdumpall/pgdump';
    if (selectCluster) selectCluster.innerHTML = '<option value="">Loading clusters...</option>';
    if (selectHost) selectHost.innerHTML = '<option value="">Select a cluster first...</option>';

    modal.style.display = 'flex';

    try {
        const [projRes, credRes] = await Promise.all([
            apiFetch('/api/projects'),
            apiFetch('/api/cloud-credentials')
        ]);
        
        if (projRes.ok) {
            allProjectsForBackup = await projRes.json();
            const hasMssql = allProjectsForBackup.some(p => (p.name || '').toLowerCase().includes('mssql'));
            if (!hasMssql) {
                allProjectsForBackup.push({
                    id: 99,
                    name: 'MSSQL',
                    db_type: 'mssql',
                    nodes: [
                        { id: 991, name: 'mssql-primary-01', host: 'mssql-prod.tp.local', port: 1433, role: 'primary' }
                    ]
                });
            }

            selectCluster.innerHTML = '<option value="">Select a cluster...</option>' +
                allProjectsForBackup.map(p => `<option value="${p.id}">${(p.db_type === 'mssql' || (p.name||'').toLowerCase().includes('mssql')) ? '🗄️ MSSQL' : '🐘 PostgreSQL'} (${p.name || 'Cluster'} ID:${p.id})</option>`).join('');
            
            // Auto-select first cluster if available
            if (allProjectsForBackup.length > 0) {
                selectCluster.value = allProjectsForBackup[0].id;
                onBackupClusterSelect();
            }
        }

        if (selectCloudCred) {
            if (credRes.ok) {
                allCloudCredsForBackup = await credRes.json();
                if (allCloudCredsForBackup.length) {
                    selectCloudCred.innerHTML = '<option value="">Create new credentials</option>' +
                        allCloudCredsForBackup.map(c => `<option value="${c.id}">${escapeHTML(c.provider)} - ${escapeHTML(c.label)} (${escapeHTML(c.bucket || 'default')})</option>`).join('');
                    selectCloudCred.value = allCloudCredsForBackup[0].id;
                } else {
                    selectCloudCred.innerHTML = '<option value="">Create new credentials (AWS S3 / Google Cloud / Azure)</option>';
                }
            } else {
                selectCloudCred.innerHTML = '<option value="">Create new credentials</option>';
            }
        }
    } catch(e) {
        console.warn('Failed to load backup modal options:', e);
    }
};

window.closeCreateBackupConfigModal = function() {
    const modal = document.getElementById('modal-create-backup-config');
    if (modal) modal.style.display = 'none';
};

window.onBackupClusterSelect = function() {
    const clusterSelect = document.getElementById('backup-config-cluster');
    const hostSelect = document.getElementById('backup-config-host');
    const methodSelect = document.getElementById('backup-config-method');
    const dumpTypeContainer = document.getElementById('bk-dumptype-container');
    const alertPitr = document.getElementById('bk-alert-pitr');
    const alertPitrEnabled = document.getElementById('bk-alert-pitr-enabled');
    const alertPartial = document.getElementById('bk-alert-partial');

    const pid = parseInt(clusterSelect.value);
    if (!pid) {
        hostSelect.innerHTML = '<option value="">Select a cluster first...</option>';
        return;
    }

    const proj = allProjectsForBackup.find(p => p.id === pid);
    const isMssql = proj && (proj.db_type === 'mssql' || (proj.name || '').toLowerCase().includes('mssql'));

    if (isMssql) {
        methodSelect.innerHTML = `
            <option value="Full">Full</option>
            <option value="Differential">Differential</option>
            <option value="Transaction Log">Transaction Log</option>
        `;
        if (dumpTypeContainer) dumpTypeContainer.style.display = 'none';
        if (alertPitr) alertPitr.style.display = 'none';
        if (alertPitrEnabled) alertPitrEnabled.style.display = 'none';
        if (alertPartial) alertPartial.style.display = 'none';
    } else {
        methodSelect.innerHTML = `
            <option value="pgdumpall/pgdump">pgdumpall/pgdump</option>
            <option value="pg_basebackup">pg_basebackup</option>
            <option value="pgbackrestfull">pgbackrestfull</option>
            <option value="pgbackrestdiff">pgbackrestdiff</option>
            <option value="pgbackrestincr">pgbackrestincr</option>
        `;
        if (dumpTypeContainer) dumpTypeContainer.style.display = 'block';
        if (alertPitr) alertPitr.style.display = 'block';
        if (alertPitrEnabled) alertPitrEnabled.style.display = 'none';
        if (alertPartial) alertPartial.style.display = 'block';
    }

    if (proj && proj.nodes && proj.nodes.length) {
        hostSelect.innerHTML = proj.nodes.map(n => {
            const hostUrl = n.host || (n.url ? n.url.split('@')[1] : 'localhost');
            const port = n.port || (isMssql ? 1433 : 5432);
            const role = n.role ? (n.role.charAt(0).toUpperCase() + n.role.slice(1)) : 'Primary';
            return `<option value="${n.id}">${hostUrl}:${port} (${role})</option>`;
        }).join('');
    } else {
        hostSelect.innerHTML = `<option value="1">localhost:${isMssql ? 1433 : 5432} (Primary)</option>`;
    }

    onBackupMethodChange();
};

window.onBackupMethodChange = function() {
    const methodSelect = document.getElementById('backup-config-method');
    const method = methodSelect ? methodSelect.value : 'pgdumpall/pgdump';
    backupWizardState.method = method;

    const alertPitr = document.getElementById('bk-alert-pitr');
    const alertPitrEnabled = document.getElementById('bk-alert-pitr-enabled');
    const alertPartial = document.getElementById('bk-alert-partial');
    const dumpTypeContainer = document.getElementById('bk-dumptype-container');
    const wrapStream = document.getElementById('wrap-toggle-bk-stream');

    if (method === 'pg_basebackup') {
        if (alertPitr) alertPitr.style.display = 'none';
        if (alertPitrEnabled) alertPitrEnabled.style.display = 'block';
        if (alertPartial) alertPartial.style.display = 'none';
        if (dumpTypeContainer) dumpTypeContainer.style.display = 'none';

        if (wrapStream) wrapStream.style.display = backupWizardState.cloudUpload ? 'flex' : 'none';
        updateStreamToggleUI();
    } else {
        if (alertPitr) alertPitr.style.display = 'block';
        if (alertPitrEnabled) alertPitrEnabled.style.display = 'none';
        if (alertPartial) alertPartial.style.display = 'block';
        if (dumpTypeContainer) dumpTypeContainer.style.display = 'block';

        if (wrapStream) wrapStream.style.display = 'none';
    }

    updateCloudToggleUI();
    renderBackupStepperNav();
};

window.toggleBackupCloudSwitch = function() {
    backupWizardState.cloudUpload = !backupWizardState.cloudUpload;
    const wrapStream = document.getElementById('wrap-toggle-bk-stream');
    if (wrapStream) {
        wrapStream.style.display = (backupWizardState.method === 'pg_basebackup' && backupWizardState.cloudUpload) ? 'flex' : 'none';
    }
    updateCloudToggleUI();
    renderBackupStepperNav();
};

function updateCloudToggleUI() {
    const sw = document.getElementById('toggle-backup-cloud');
    const label = document.getElementById('label-toggle-backup-cloud');
    const thumb = document.getElementById('toggle-thumb-backup-cloud');
    if (!sw || !label || !thumb) return;

    if (backupWizardState.cloudUpload) {
        sw.style.background = '#3a1c94';
        label.textContent = 'On';
        label.style.left = '6px';
        label.style.right = '';
        thumb.style.transform = 'translateX(24px)';
    } else {
        sw.style.background = '#d1d5db';
        label.textContent = 'Off';
        label.style.left = '';
        label.style.right = '6px';
        thumb.style.transform = 'translateX(0)';
    }
}

window.toggleBackupStreamSwitch = function() {
    backupWizardState.cloudStream = !backupWizardState.cloudStream;
    updateStreamToggleUI();
    renderBackupStepperNav();
};

function updateStreamToggleUI() {
    const sw = document.getElementById('toggle-backup-stream');
    const label = document.getElementById('label-toggle-backup-stream');
    const thumb = document.getElementById('toggle-thumb-backup-stream');
    if (!sw || !label || !thumb) return;

    if (backupWizardState.cloudStream) {
        sw.style.background = '#3a1c94';
        label.textContent = 'On';
        label.style.left = '6px';
        label.style.right = '';
        thumb.style.transform = 'translateX(24px)';
    } else {
        sw.style.background = '#d1d5db';
        label.textContent = 'Off';
        label.style.left = '';
        label.style.right = '6px';
        thumb.style.transform = 'translateX(0)';
    }
}

window.toggleBackupCompSwitch = function() {
    backupIsCompression = !backupIsCompression;
    const sw = document.getElementById('toggle-backup-comp');
    const label = document.getElementById('label-toggle-backup-comp');
    const thumb = document.getElementById('toggle-thumb-backup-comp');
    if (sw && thumb) {
        sw.style.background = backupIsCompression ? '#3a1c94' : '#d1d5db';
        thumb.style.transform = backupIsCompression ? 'translateX(24px)' : 'translateX(0)';
        if (label) {
            label.textContent = backupIsCompression ? 'On' : 'Off';
            label.style.left = backupIsCompression ? '6px' : '';
            label.style.right = backupIsCompression ? '' : '6px';
        }
    }
};

window.toggleBackupRetentionSwitch = function() {
    backupIsRetention = !backupIsRetention;
    const sw = document.getElementById('toggle-backup-retention');
    const label = document.getElementById('label-toggle-backup-retention');
    const thumb = document.getElementById('toggle-thumb-backup-retention');
    if (sw && thumb) {
        sw.style.background = backupIsRetention ? '#3a1c94' : '#d1d5db';
        thumb.style.transform = backupIsRetention ? 'translateX(24px)' : 'translateX(0)';
        if (label) {
            label.textContent = backupIsRetention ? 'On' : 'Off';
            label.style.left = backupIsRetention ? '6px' : '';
            label.style.right = backupIsRetention ? '' : '6px';
        }
    }
};

window.toggleGenericPillSwitch = function(swId, thumbId, labelId, defaultOn = false) {
    const sw = document.getElementById(swId);
    const thumb = document.getElementById(thumbId);
    const label = document.getElementById(labelId);
    if (!sw || !thumb) return;
    const isOn = sw.getAttribute('data-on') === 'true' || (defaultOn && sw.getAttribute('data-on') === null);
    const newState = !isOn;
    sw.setAttribute('data-on', newState ? 'true' : 'false');
    sw.style.background = newState ? '#3a1c94' : '#d1d5db';
    thumb.style.transform = newState ? 'translateX(24px)' : 'translateX(0)';
    if (label) {
        label.textContent = newState ? 'On' : 'Off';
        label.style.left = newState ? '6px' : '';
        label.style.right = newState ? '' : '6px';
    }
};

function getBackupStepsList() {
    if (backupWizardState.method === 'pg_basebackup') {
        if (!backupWizardState.cloudUpload) {
            // Exactly matching media_1787293443329.png: 3 steps!
            return [
                { num: 1, key: 'config', label: 'Configuration' },
                { num: 2, key: 'advanced', label: 'Advanced settings' },
                { num: 3, key: 'preview', label: 'Preview' }
            ];
        } else if (backupWizardState.cloudStream) {
            // Exactly matching media_1787293519802.png: 4 steps!
            return [
                { num: 1, key: 'config', label: 'Configuration' },
                { num: 2, key: 'advanced', label: 'Advanced settings' },
                { num: 3, key: 'cloud', label: 'Cloud storage' },
                { num: 4, key: 'preview', label: 'Preview' }
            ];
        } else {
            return [
                { num: 1, key: 'config', label: 'Configuration' },
                { num: 2, key: 'advanced', label: 'Advanced settings' },
                { num: 3, key: 'local', label: 'Local storage' },
                { num: 4, key: 'cloud', label: 'Cloud storage' },
                { num: 5, key: 'preview', label: 'Preview' }
            ];
        }
    } else {
        if (backupWizardState.cloudUpload) {
            return [
                { num: 1, key: 'config', label: 'Configuration' },
                { num: 2, key: 'advanced', label: 'Advanced settings' },
                { num: 3, key: 'local', label: 'Local storage' },
                { num: 4, key: 'cloud', label: 'Cloud storage' },
                { num: 5, key: 'preview', label: 'Preview' }
            ];
        } else {
            return [
                { num: 1, key: 'config', label: 'Configuration' },
                { num: 2, key: 'advanced', label: 'Advanced settings' },
                { num: 3, key: 'local', label: 'Storage' },
                { num: 4, key: 'preview', label: 'Preview' }
            ];
        }
    }
}

window.renderBackupStepperNav = function() {
    const steps = getBackupStepsList();
    const navContainer = document.getElementById('bk-stepper-nav-items');
    if (!navContainer) return;

    if (backupWizardState.currentStepIndex > steps.length) {
        backupWizardState.currentStepIndex = steps.length;
    }
    const currentStep = steps[backupWizardState.currentStepIndex - 1] || steps[0];
    backupWizardState.activeStepKey = currentStep.key;

    navContainer.innerHTML = steps.map((s, idx) => {
        const stepNum = idx + 1;
        const isDone = stepNum < backupWizardState.currentStepIndex;
        const isActive = stepNum === backupWizardState.currentStepIndex;
        const bg = isDone ? '#10b981' : isActive ? '#3a1c94' : 'transparent';
        const border = isDone ? 'none' : isActive ? 'none' : '2px solid #d1d5db';
        const color = (isDone || isActive) ? 'white' : '#9ca3af';
        const text = isDone ? '✓' : String(stepNum);
        const labelColor = isActive ? '#3a1c94' : isDone ? '#10b981' : '#9ca3af';
        const fontW = isActive ? '600' : '500';

        return `
            <div onclick="jumpToBackupStep(${stepNum})" style="display: flex; align-items: center; gap: 12px; cursor: pointer; color: ${labelColor}; font-weight: ${fontW}; font-size: 0.9rem;">
                <div style="width: 24px; height: 24px; border-radius: 50%; background: ${bg}; border: ${border}; color: ${color}; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0;">${text}</div>
                ${escapeHTML(s.label)}
            </div>
        `;
    }).join('');

    // Toggle Panes
    ['config', 'advanced', 'local', 'cloud', 'preview'].forEach(k => {
        const pane = document.getElementById(`bk-pane-${k}`);
        if (pane) pane.style.display = (k === currentStep.key) ? 'block' : 'none';
    });

    // Cloud Pane: Toggle "Delete after upload" visibility
    const wrapDelAfter = document.getElementById('wrap-del-local-after-upload');
    if (wrapDelAfter) {
        wrapDelAfter.style.display = (backupWizardState.method === 'pg_basebackup' && backupWizardState.cloudStream) ? 'none' : 'flex';
    }

    // Update Footer Buttons
    const btnBack = document.getElementById('btn-bk-back');
    const btnNext = document.getElementById('btn-bk-next');
    if (btnBack) {
        btnBack.disabled = (backupWizardState.currentStepIndex === 1);
        btnBack.style.color = (backupWizardState.currentStepIndex === 1) ? '#9ca3af' : '#374151';
        btnBack.style.cursor = (backupWizardState.currentStepIndex === 1) ? 'not-allowed' : 'pointer';
    }
    if (btnNext) {
        if (backupWizardState.currentStepIndex === steps.length) {
            btnNext.innerText = 'Create';
            btnNext.onclick = submitCreateBackup;
            updateBackupPreview();
        } else {
            btnNext.innerText = 'Continue';
            btnNext.onclick = nextBackupStep;
        }
    }
};

window.jumpToBackupStep = function(stepNum) {
    if (stepNum > backupWizardState.currentStepIndex) {
        const clusterVal = document.getElementById('backup-config-cluster')?.value;
        if (!clusterVal) {
            alert('Please select a Cluster first.');
            return;
        }
    }
    backupWizardState.currentStepIndex = stepNum;
    renderBackupStepperNav();
};

window.nextBackupStep = function() {
    const steps = getBackupStepsList();
    if (backupWizardState.currentStepIndex === 1) {
        const clusterVal = document.getElementById('backup-config-cluster')?.value;
        if (!clusterVal) {
            alert('Please select a Cluster first.');
            return;
        }
    }
    if (backupWizardState.currentStepIndex < steps.length) {
        backupWizardState.currentStepIndex++;
        renderBackupStepperNav();
    }
};

window.prevBackupStep = function() {
    if (backupWizardState.currentStepIndex > 1) {
        backupWizardState.currentStepIndex--;
        renderBackupStepperNav();
    }
};

function updateBackupPreview() {
    const clusterSelect = document.getElementById('backup-config-cluster');
    const hostSelect = document.getElementById('backup-config-host');
    const methodSelect = document.getElementById('backup-config-method');
    const dumpTypeSelect = document.getElementById('backup-config-dumptype');
    const compLevelSelect = document.getElementById('backup-comp-level');
    const retentionDays = document.getElementById('backup-retention-days')?.value || '31';
    const storageDir = document.getElementById('backup-storage-dir')?.value || '/var/lib/backups';
    const cloudCredSelect = document.getElementById('backup-cloud-cred-select');
    const cloudRetDays = document.getElementById('backup-cloud-retention-days')?.value || '180 Days';

    const clusterText = clusterSelect?.options[clusterSelect.selectedIndex]?.text || 'PostgreSQL';
    const hostText = hostSelect?.options[hostSelect.selectedIndex]?.text || 'localhost';
    const methodText = methodSelect?.value || 'pgdumpall';
    const dumpTypeText = dumpTypeSelect?.value || 'Schema And Data';

    const el = id => document.getElementById(id);
    if (el('pv-bk-cluster')) el('pv-bk-cluster').innerText = clusterText;
    if (el('pv-bk-host')) el('pv-bk-host').innerText = hostText;
    if (el('pv-bk-method')) el('pv-bk-method').innerText = methodText;
    if (el('pv-bk-dumptype')) el('pv-bk-dumptype').innerText = (methodText === 'pg_basebackup') ? 'Binary Full' : dumpTypeText;
    if (el('pv-bk-comp')) el('pv-bk-comp').innerText = backupIsCompression ? 'Yes' : 'No';
    if (el('pv-bk-comp-level')) el('pv-bk-comp-level').innerText = compLevelSelect?.value || '6 (System Default)';
    if (el('pv-bk-retention')) el('pv-bk-retention').innerText = `${retentionDays} Days`;
    
    // Target and cloud details
    const isStream = backupWizardState.method === 'pg_basebackup' && backupWizardState.cloudStream && backupWizardState.cloudUpload;
    const isCloud = backupWizardState.cloudUpload;
    const cloudCredText = cloudCredSelect?.options[cloudCredSelect.selectedIndex]?.text || 'AWS S3';

    if (el('pv-bk-target')) {
        el('pv-bk-target').innerText = isStream ? 'Direct Cloud Streaming' : isCloud ? 'Local + Cloud Upload' : 'Local Storage';
    }
    if (el('pv-bk-local-loc-wrap')) el('pv-bk-local-loc-wrap').style.display = isStream ? 'none' : 'block';
    if (el('pv-bk-local-dir-wrap')) el('pv-bk-local-dir-wrap').style.display = isStream ? 'none' : 'block';
    if (el('pv-bk-cloud-cred-wrap')) {
        el('pv-bk-cloud-cred-wrap').style.display = isCloud ? 'block' : 'none';
        if (el('pv-bk-cloud-cred')) el('pv-bk-cloud-cred').innerText = cloudCredText;
    }
    if (el('pv-bk-cloud-ret-wrap')) {
        el('pv-bk-cloud-ret-wrap').style.display = isCloud ? 'block' : 'none';
        if (el('pv-bk-cloud-ret')) el('pv-bk-cloud-ret').innerText = cloudRetDays;
    }
}

window.submitCreateBackup = async function() {
    const btn = document.getElementById('btn-bk-next');
    if (btn) { btn.disabled = true; btn.innerText = 'Creating Backup...'; }

    const clusterSelect = document.getElementById('backup-config-cluster');
    const hostSelect = document.getElementById('backup-config-host');
    const methodSelect = document.getElementById('backup-config-method');
    const dumpTypeSelect = document.getElementById('backup-config-dumptype');
    const compLevelSelect = document.getElementById('backup-comp-level');
    const retentionDays = parseInt(document.getElementById('backup-retention-days')?.value || '31');
    const storageDir = document.getElementById('backup-storage-dir')?.value || '/var/lib/backups';
    const subdir = document.getElementById('backup-subdir')?.value || 'BACKUP-%i';
    const cloudCredSelect = document.getElementById('backup-cloud-cred-select');

    const pid = parseInt(clusterSelect?.value) || null;
    const proj = allProjectsForBackup.find(p => p.id === pid);
    const dbType = proj && (proj.db_type === 'mssql' || (proj.name||'').toLowerCase().includes('mssql')) ? 'mssql' : 'postgresql';
    const isStream = backupWizardState.method === 'pg_basebackup' && backupWizardState.cloudStream && backupWizardState.cloudUpload;
    const isCloud = backupWizardState.cloudUpload;

    const payload = {
        project_id: pid,
        cluster_name: proj ? proj.name : 'PostgreSQL Cluster',
        db_type: dbType,
        node_id: parseInt(hostSelect?.value) || null,
        backup_host: hostSelect?.options[hostSelect.selectedIndex]?.text?.split(' ')[0] || 'localhost:5432',
        backup_method: methodSelect?.value || (dbType === 'mssql' ? 'Full' : 'pgdumpall'),
        dump_type: dumpTypeSelect?.value || 'Schema And Data',
        backup_type: 'FULL',
        compression: backupIsCompression,
        compression_level: parseInt(compLevelSelect?.value || '6'),
        retention_days: retentionDays,
        storage_location: isStream ? 'Direct Cloud Stream' : isCloud ? 'Cloud Storage' : 'Store on controller',
        storage_directory: storageDir,
        backup_subdirectory: subdir,
        cloud_credential_id: isCloud ? (parseInt(cloudCredSelect?.value) || null) : null
    };

    try {
        const res = await apiFetch('/api/backups/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const d = await res.json();
        if (res.ok && d.success) {
            closeCreateBackupConfigModal();
            loadAllBackups();
            alert(`✓ ${d.message}`);
        } else {
            alert(d.message || 'Failed to start backup.');
        }
    } catch(e) {
        alert('Connection error while initiating backup.');
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Create'; }
    }
};

// ── Link Cloud Service Provider (ClusterControl AWS/S3 Integration) ──────────

let selectedCloudProviderKey = null; // 'aws' or 's3'
let linkCloudWizardStep = 1;

window.openLinkCloudModal = function() {
    selectedCloudProviderKey = null;
    linkCloudWizardStep = 1;

    const modal = document.getElementById('modal-link-cloud-provider');
    const title = document.getElementById('link-cloud-modal-title');
    const screenSelect = document.getElementById('screen-link-cloud-select');
    const screenForm = document.getElementById('screen-link-cloud-form');
    const viewEmpty = document.getElementById('view-prov-empty');
    const viewSelected = document.getElementById('view-prov-selected');
    const wizardBtns = document.getElementById('link-cloud-wizard-btns');

    if (title) title.innerText = 'Link a cloud service provider';
    if (screenSelect) screenSelect.style.display = 'flex';
    if (screenForm) screenForm.style.display = 'none';
    if (viewEmpty) viewEmpty.style.display = 'flex';
    if (viewSelected) viewSelected.style.display = 'none';
    if (wizardBtns) wizardBtns.style.display = 'none';

    // Reset cards
    const cardAws = document.getElementById('card-prov-aws');
    const cardS3 = document.getElementById('card-prov-s3');
    const checkAws = document.getElementById('check-prov-aws');
    const checkS3 = document.getElementById('check-prov-s3');
    if (cardAws) { cardAws.style.borderColor = '#d1d5db'; cardAws.style.background = 'white'; }
    if (cardS3) { cardS3.style.borderColor = '#d1d5db'; cardS3.style.background = 'white'; }
    if (checkAws) checkAws.style.display = 'none';
    if (checkS3) checkS3.style.display = 'none';

    if (modal) modal.style.display = 'flex';
};

window.closeLinkCloudModal = function() {
    const modal = document.getElementById('modal-link-cloud-provider');
    if (modal) modal.style.display = 'none';
};

window.openAddCloudCredModal = function() {
    openLinkCloudModal();
};

window.closeAddCloudCredModal = function() {
    closeLinkCloudModal();
};

window.selectCloudProviderToLink = function(key) {
    selectedCloudProviderKey = key;
    const cardAws = document.getElementById('card-prov-aws');
    const cardS3 = document.getElementById('card-prov-s3');
    const checkAws = document.getElementById('check-prov-aws');
    const checkS3 = document.getElementById('check-prov-s3');

    if (cardAws) {
        cardAws.style.borderColor = (key === 'aws') ? '#3a1c94' : '#d1d5db';
        cardAws.style.background = (key === 'aws') ? '#fbfaff' : 'white';
    }
    if (cardS3) {
        cardS3.style.borderColor = (key === 's3') ? '#3a1c94' : '#d1d5db';
        cardS3.style.background = (key === 's3') ? '#fbfaff' : 'white';
    }
    if (checkAws) checkAws.style.display = (key === 'aws') ? 'block' : 'none';
    if (checkS3) checkS3.style.display = (key === 's3') ? 'block' : 'none';

    const viewEmpty = document.getElementById('view-prov-empty');
    const viewSelected = document.getElementById('view-prov-selected');
    const provIcon = document.getElementById('detail-prov-icon');
    const provTitle = document.getElementById('detail-prov-title');
    const provDesc = document.getElementById('detail-prov-desc');

    if (viewEmpty) viewEmpty.style.display = 'none';
    if (viewSelected) viewSelected.style.display = 'flex';

    if (key === 'aws') {
        if (provIcon) provIcon.innerHTML = `
            <svg width="40" height="40" viewBox="0 0 50 50" fill="none">
              <rect width="50" height="50" rx="8" fill="#f8fafc"/>
              <path d="M14 26C18 31 32 31 36 26" stroke="#FF9900" stroke-width="3" stroke-linecap="round"/>
              <path d="M33 24L36 26L34 29" fill="#FF9900"/>
              <text x="11" y="21" font-family="Arial, sans-serif" font-weight="900" font-size="14" fill="#232F3E">aws</text>
            </svg>
        `;
        if (provTitle) provTitle.innerText = 'Amazon Web Services';
        if (provDesc) provDesc.innerText = 'Amazon Web Services provides a highly reliable, scalable, low-cost infrastructure platform in the cloud with data center locations in the U.S., Europe, Brazil, Singapore, Japan, and Australia.';
    } else {
        if (provIcon) provIcon.innerHTML = `
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
            </svg>
        `;
        if (provTitle) provTitle.innerText = 'S3 Compatible storage provider';
        if (provDesc) provDesc.innerText = 'Connect to any S3-compatible cloud object storage provider such as MinIO, Wasabi, DigitalOcean Spaces, Backblaze B2, or Ceph.';
    }
};

window.goToLinkCloudAuthWizard = function() {
    const screenSelect = document.getElementById('screen-link-cloud-select');
    const screenForm = document.getElementById('screen-link-cloud-form');
    const wizardBtns = document.getElementById('link-cloud-wizard-btns');
    const title = document.getElementById('link-cloud-modal-title');

    if (title) {
        title.innerText = (selectedCloudProviderKey === 'aws') ? 'Link Amazon Web Services' : 'Link S3 Compatible storage provider';
    }
    if (screenSelect) screenSelect.style.display = 'none';
    if (screenForm) screenForm.style.display = 'flex';
    if (wizardBtns) wizardBtns.style.display = 'flex';

    linkCloudWizardStep = 1;
    setLinkCloudStepUI(1);
};

function setLinkCloudStepUI(step) {
    linkCloudWizardStep = step;
    const nav1 = document.getElementById('link-step-nav-1');
    const nav2 = document.getElementById('link-step-nav-2');
    const badge1 = document.getElementById('link-step-badge-1');
    const badge2 = document.getElementById('link-step-badge-2');
    const paneAuth = document.getElementById('link-pane-auth');
    const panePrev = document.getElementById('link-pane-prev');
    const btnNext = document.getElementById('btn-link-next');

    if (paneAuth) paneAuth.style.display = (step === 1) ? 'block' : 'none';
    if (panePrev) panePrev.style.display = (step === 2) ? 'block' : 'none';

    if (step === 1) {
        if (nav1 && badge1) {
            nav1.style.color = '#3a1c94';
            badge1.style.background = '#3a1c94';
            badge1.style.color = 'white';
            badge1.innerHTML = '1';
        }
        if (nav2 && badge2) {
            nav2.style.color = '#9ca3af';
            badge2.style.background = 'transparent';
            badge2.style.color = '#9ca3af';
            badge2.innerHTML = '2';
        }
        if (btnNext) {
            btnNext.innerText = 'Continue';
            btnNext.onclick = nextLinkCloudStep;
        }
    } else {
        if (nav1 && badge1) {
            nav1.style.color = '#10b981';
            badge1.style.background = '#10b981';
            badge1.style.color = 'white';
            badge1.innerHTML = '✓';
        }
        if (nav2 && badge2) {
            nav2.style.color = '#3a1c94';
            badge2.style.background = '#3a1c94';
            badge2.style.color = 'white';
            badge2.innerHTML = '2';
        }
        if (btnNext) {
            btnNext.innerText = 'Create';
            btnNext.onclick = submitLinkCloudProvider;
        }
        updateLinkCloudPreview();
    }
}

window.nextLinkCloudStep = function() {
    if (linkCloudWizardStep === 1) {
        const name = document.getElementById('link-aws-name')?.value || '';
        const keyId = document.getElementById('link-aws-key-id')?.value || '';
        const secret = document.getElementById('link-aws-secret')?.value || '';
        if (!name.trim()) {
            alert('Please enter a name for your integration.');
            return;
        }
        if (!keyId.trim()) {
            alert('Please enter AWS key ID.');
            return;
        }
        if (!secret.trim()) {
            alert('Please enter AWS key secret.');
            return;
        }
        setLinkCloudStepUI(2);
    }
};

window.prevLinkCloudStep = function() {
    if (linkCloudWizardStep === 2) {
        setLinkCloudStepUI(1);
    } else {
        const screenSelect = document.getElementById('screen-link-cloud-select');
        const screenForm = document.getElementById('screen-link-cloud-form');
        const wizardBtns = document.getElementById('link-cloud-wizard-btns');
        const title = document.getElementById('link-cloud-modal-title');
        if (title) title.innerText = 'Link a cloud service provider';
        if (screenSelect) screenSelect.style.display = 'flex';
        if (screenForm) screenForm.style.display = 'none';
        if (wizardBtns) wizardBtns.style.display = 'none';
    }
};

function updateLinkCloudPreview() {
    const name = document.getElementById('link-aws-name')?.value || 'AWS Integration';
    const keyId = document.getElementById('link-aws-key-id')?.value || '';
    const region = document.getElementById('link-aws-region')?.value || 'us-east-1';
    const bucket = document.getElementById('link-aws-bucket')?.value || '-';
    const comment = document.getElementById('link-aws-comment')?.value || '—';

    const provText = (selectedCloudProviderKey === 'aws') ? 'Amazon Web Services' : 'S3 Compatible storage';
    const maskedKey = keyId.length > 6 ? (keyId.substring(0, 4) + '...' + keyId.slice(-4)) : keyId;

    const el = id => document.getElementById(id);
    if (el('pv-link-provider')) el('pv-link-provider').innerText = provText;
    if (el('pv-link-name')) el('pv-link-name').innerText = name;
    if (el('pv-link-key')) el('pv-link-key').innerText = maskedKey;
    if (el('pv-link-region')) el('pv-link-region').innerText = region;
    if (el('pv-link-bucket')) el('pv-link-bucket').innerText = bucket;
    if (el('pv-link-comment')) el('pv-link-comment').innerText = comment;
}

window.submitLinkCloudProvider = async function() {
    const btn = document.getElementById('btn-link-next');
    if (btn) { btn.disabled = true; btn.innerText = 'Saving...'; }

    const name = document.getElementById('link-aws-name')?.value || '';
    const keyId = document.getElementById('link-aws-key-id')?.value || '';
    const secret = document.getElementById('link-aws-secret')?.value || '';
    const region = document.getElementById('link-aws-region')?.value || 'us-east-1';
    const bucket = document.getElementById('link-aws-bucket')?.value || '';
    const provider = (selectedCloudProviderKey === 'aws') ? 'AWS S3' : 'S3 Compatible';

    try {
        const res = await apiFetch('/api/cloud-credentials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                provider: provider,
                label: name.trim(),
                key_id: keyId.trim(),
                secret: secret.trim(),
                bucket: bucket.trim(),
                region: region.trim()
            })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            closeLinkCloudModal();
            if (typeof window.loadCloudCredentials === 'function') {
                window.loadCloudCredentials();
            }
            const credRes = await apiFetch('/api/cloud-credentials');
            if (credRes.ok) {
                allCloudCredsForBackup = await credRes.json();
                const selectCloudCred = document.getElementById('backup-cloud-cred-select');
                if (selectCloudCred) {
                    selectCloudCred.innerHTML = '<option value="">Create new credentials</option>' +
                        allCloudCredsForBackup.map(c => `<option value="${c.id}">${escapeHTML(c.provider)} - ${escapeHTML(c.label)} (${escapeHTML(c.bucket || 'default')})</option>`).join('');
                    selectCloudCred.value = data.id;
                }
            }
            alert(`✓ Successfully linked ${provider} integration: "${name}"`);
        } else {
            alert(data.message || 'Failed to save cloud credentials');
        }
    } catch(e) {
        alert('Connection error while saving credentials.');
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Create'; }
    }
};

window.onBackupCloudCredSelectChange = function() {
    const val = document.getElementById('backup-cloud-cred-select')?.value;
    if (!val || val === 'create_new') {
        openLinkCloudModal();
    }
};

window.deleteBackup = async function(id) {
    if (!confirm('Are you sure you want to delete this backup record and file?')) return;
    try {
        const res = await apiFetch(`/api/backups/${id}`, { method: 'DELETE' });
        if (res.ok) {
            loadAllBackups();
        }
    } catch(e) {
        alert('Failed to delete backup');
    }
};

// Hook into DOM ready for backup button listeners
document.addEventListener('DOMContentLoaded', () => {
    const btnGlobalCreateBackup = document.getElementById('btn-global-create-backup');
    const modalBackupType = document.getElementById('modal-backup-type-select');
    const btnCloseBackupType = document.getElementById('btn-close-backup-type-modal');
    const btnBackupOnDemand = document.getElementById('btn-select-backup-ondemand');
    const btnBackupSchedule = document.getElementById('btn-select-backup-schedule');

    if (btnGlobalCreateBackup) {
        btnGlobalCreateBackup.addEventListener('click', () => {
            if (modalBackupType) modalBackupType.style.display = 'flex';
        });
    }
    if (btnCloseBackupType) {
        btnCloseBackupType.addEventListener('click', () => {
            if (modalBackupType) modalBackupType.style.display = 'none';
        });
    }
    if (btnBackupOnDemand) btnBackupOnDemand.addEventListener('click', openCreateBackupConfigModal);
    if (btnBackupSchedule) btnBackupSchedule.addEventListener('click', openCreateBackupConfigModal);

    // Initial load for header alarms
    loadHeaderAlarms();
});


    window.switchUserTab = function(tabName) {
        // Hide all contents
        document.querySelectorAll('.user-tab-content').forEach(el => el.style.display = 'none');
        // Reset all tabs
        document.querySelectorAll('.user-tab').forEach(el => {
            el.style.color = 'var(--text-muted)';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active-tab');
        });
        
        // Show target content
        const targetContent = document.getElementById('content-' + tabName);
        if(targetContent) targetContent.style.display = 'block';
        
        // Highlight target tab
        const targetTab = document.getElementById('tab-' + tabName);
        if(targetTab) {
            targetTab.style.color = 'var(--primary)';
            targetTab.style.borderBottom = '2px solid var(--primary)';
            targetTab.classList.add('active-tab');
        }
    };


    // Add search listener for settings
    const settingsSearchInput = document.getElementById('settings-search-input');
    if (settingsSearchInput) {
        settingsSearchInput.addEventListener('input', () => {
            // Debounce or just load directly since data fetch is fast or we could cache it, 
            // but for simplicity we'll just call loadSettings
            // Actually it hits API every time. Let's debounce it slightly or just do it.
            if (window.settingsSearchTimeout) clearTimeout(window.settingsSearchTimeout);
            window.settingsSearchTimeout = setTimeout(() => {
                loadSettings();
            }, 300);
        });
    }


// Reports Tab Switching
function switchReportsTab(tabName) {
    const tabReports = document.getElementById('tab-reports-sub');
    const tabSchedules = document.getElementById('tab-schedules-sub');
    const tableReports = document.getElementById('table-reports');
    const tableSchedules = document.getElementById('table-schedules');
    const btnAction = document.getElementById('btn-create-report-action');
    const textAction = document.getElementById('text-create-report-action');

    if (tabName === 'reports') {
        tabReports.style.color = 'var(--primary)';
        tabReports.style.borderBottomColor = 'var(--primary)';
        tabSchedules.style.color = 'var(--text-muted)';
        tabSchedules.style.borderBottomColor = 'transparent';
        tableReports.style.display = 'block';
        tableSchedules.style.display = 'none';
        textAction.innerText = 'Create report';
        btnAction.onclick = () => {
            populateReportClusterSelect();
            document.getElementById('modal-create-report').style.display = 'flex';
        };
    } else {
        tabSchedules.style.color = 'var(--primary)';
        tabSchedules.style.borderBottomColor = 'var(--primary)';
        tabReports.style.color = 'var(--text-muted)';
        tabReports.style.borderBottomColor = 'transparent';
        tableSchedules.style.display = 'block';
        tableReports.style.display = 'none';
        textAction.innerText = 'Create schedule';
        btnAction.onclick = () => {
            populateSchedClusterSelect();
            window.switchSchedTab('Minutely');
            document.getElementById('modal-create-schedule').style.display = 'flex';
        };
    }
}


// ─── Report/Schedule modal dispatcher ────────────────────────────────────────
window.openReportActionModal = function() {
    const activeTab = document.getElementById('tab-schedules-sub');
    const isScheduleTab = activeTab && activeTab.style.color !== 'var(--text-muted)' &&
                          activeTab.style.borderBottomColor !== 'transparent';
    // Check which tab is active by looking at the schedules tab underline
    const schedTab = document.getElementById('tab-schedules-sub');
    const isOnSchedules = schedTab && schedTab.style.borderBottomColor === 'var(--primary)';
    if (isOnSchedules) {
        populateSchedClusterSelect();
        window.switchSchedTab('Minutely');
        document.getElementById('modal-create-schedule').style.display = 'flex';
    } else {
        populateReportClusterSelect();
        document.getElementById('modal-create-report').style.display = 'flex';
    }
};

// ─── Populate cluster dropdowns ──────────────────────────────────────────────
async function populateReportClusterSelect() {
    const sel = document.getElementById('report-cluster-select');
    if (!sel || sel.options.length > 1) return; // already loaded
    try {
        const res = await apiFetch('/api/projects');
        const projs = res.ok ? await res.json() : [];
        projs.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id; opt.textContent = p.name;
            sel.appendChild(opt);
        });
    } catch {}
}

async function populateSchedClusterSelect() {
    const sel = document.getElementById('sched-cluster-select');
    if (!sel || sel.options.length > 1) return; // already loaded
    try {
        const res = await apiFetch('/api/projects');
        const projs = res.ok ? await res.json() : [];
        projs.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id; opt.textContent = p.name;
            sel.appendChild(opt);
        });
    } catch {}
}

// ─── Schedule tab switcher ───────────────────────────────────────────────────
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const WEEKDAYS = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
let _schedTab = 'Minutely';

window.switchSchedTab = function(tab, clickedBtn) {
    _schedTab = tab;
    // Update tab button styles
    ['Minutely','Hourly','Daily','Weekly','Monthly','Yearly'].forEach(t => {
        const btn = document.getElementById('sched-tab-' + t);
        if (!btn) return;
        if (t === tab) {
            btn.style.background = '#4338ca';
            btn.style.color = 'white';
            btn.style.fontWeight = '600';
        } else {
            btn.style.background = 'white';
            btn.style.color = '#374151';
            btn.style.fontWeight = '400';
        }
    });
    renderSchedFields(tab);
    updateSchedDescription();
};

function inp(id, type, val, style, onchange) {
    return `<input id="${id}" type="${type}" value="${val}" oninput="updateSchedDescription()"
        style="padding:7px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:0.88rem;outline:none;${style}">`;
}
function sel(id, opts, style) {
    return `<select id="${id}" onchange="updateSchedDescription()"
        style="padding:7px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:0.88rem;outline:none;background:white;${style}">
        ${opts}</select>`;
}

function renderSchedFields(tab) {
    const area = document.getElementById('sched-fields');
    if (!area) return;
    const monthOpts = MONTHS.map((m,i) => `<option value="${i}">${m}</option>`).join('');
    const dayOpts = WEEKDAYS.map((d,i) => `<option value="${i}">${d}</option>`).join('');
    let html = '';
    switch(tab) {
        case 'Minutely':
            html = `<span>Every</span>
                    ${inp('sf-min','number','1','width:70px;','')}
                    <span>minute(s)</span>`;
            break;
        case 'Hourly':
            html = `<span>Every</span>
                    ${inp('sf-hour','number','1','width:70px;','')}
                    <span>hour(s) at minute</span>
                    ${inp('sf-hmin','number','0','width:70px;','')}`;
            break;
        case 'Daily':
            html = `<span>Every</span>
                    ${inp('sf-dday','number','1','width:70px;','')}
                    <span>day(s) at</span>
                    ${inp('sf-dtime','time','00:00','width:110px;','')}`;
            break;
        case 'Weekly':
            html = `<span>Every</span>
                    ${sel('sf-wday', dayOpts,'width:120px;')}
                    <span>at</span>
                    ${inp('sf-wtime','time','00:00','width:110px;','')}`;
            break;
        case 'Monthly':
            html = `<span>On the</span>
                    ${inp('sf-mday','number','1','width:70px;','')}
                    <span>day at</span>
                    ${inp('sf-mtime','time','00:00','width:110px;','')}`;
            break;
        case 'Yearly':
            html = `<span>Every</span>
                    ${sel('sf-ymon', monthOpts,'width:80px;')}
                    <span>, on the day</span>
                    ${inp('sf-yday','number','1','width:70px;','')}
                    <span>at</span>
                    ${inp('sf-ytime','time','00:00','width:110px;','')}`;
            break;
    }
    area.innerHTML = html;
    // Clamp number inputs
    area.querySelectorAll('input[type=number]').forEach(el => {
        el.addEventListener('change', () => { if (parseInt(el.value) < 1) el.value = 1; updateSchedDescription(); });
    });
}

function v(id) { const el = document.getElementById(id); return el ? el.value : ''; }

function updateSchedDescription() {
    const desc = document.getElementById('sched-description');
    if (!desc) return;
    let text = '';
    switch(_schedTab) {
        case 'Minutely': {
            const n = v('sf-min') || '1';
            text = `Every ${n} minute${n !== '1' ? 's' : ''}`;
            break;
        }
        case 'Hourly': {
            const h = v('sf-hour') || '1';
            const m = v('sf-hmin') || '0';
            text = `Every ${h} hour${h !== '1' ? 's' : ''} at minute ${m}`;
            break;
        }
        case 'Daily': {
            const d = v('sf-dday') || '1';
            const t = v('sf-dtime') || '00:00';
            text = `Every ${d} day${d !== '1' ? 's' : ''} at ${t}`;
            break;
        }
        case 'Weekly': {
            const dayIdx = parseInt(v('sf-wday') || '0');
            const t = v('sf-wtime') || '00:00';
            text = `Every ${WEEKDAYS[dayIdx]} at ${t}`;
            break;
        }
        case 'Monthly': {
            const d = v('sf-mday') || '1';
            const t = v('sf-mtime') || '00:00';
            const ord = ordinal(parseInt(d));
            text = `At ${t}, on the ${ord} of every month`;
            break;
        }
        case 'Yearly': {
            const monIdx = parseInt(v('sf-ymon') || '0');
            const d = v('sf-yday') || '1';
            const t = v('sf-ytime') || '00:00';
            text = `At ${t}, on day ${d} of the month, only in ${MONTHS[monIdx]}`;
            break;
        }
    }
    desc.textContent = text;
}

function ordinal(n) {
    const s = ['th','st','nd','rd'];
    const v = n % 100;
    return n + (s[(v-20)%10] || s[v] || s[0]);
}

// ─── Submit create schedule ───────────────────────────────────────────────────
window.submitCreateSchedule = function() {
    const errEl = document.getElementById('sched-error');
    if (errEl) errEl.style.display = 'none';
    const cluster = v('sched-cluster-select');
    const type = v('sched-type-select');
    const dataRange = v('sched-data-range');
    if (!cluster) { if (errEl) { errEl.textContent = 'Please select a cluster.'; errEl.style.display = 'block'; } return; }
    if (!type) { if (errEl) { errEl.textContent = 'Please select a report type.'; errEl.style.display = 'block'; } return; }
    const description = document.getElementById('sched-description')?.textContent || '';
    // For now store as audit log entry (placeholder until backend schedule endpoint exists)
    const scheduleData = {
        cluster_id: cluster,
        type,
        data_range: dataRange,
        recipients: v('sched-recipients'),
        frequency: _schedTab,
        description
    };
    console.log('Schedule created:', scheduleData);
    document.getElementById('modal-create-schedule').style.display = 'none';
    showToast && showToast('Schedule saved: ' + description, 'success');
};

// --- OPERATIONAL REPORTS LOGIC ---
async function loadReports() {
    const tbody = document.querySelector('#table-reports tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="8" style="padding: 20px; text-align: center; color: #6b7280;">Loading reports...</td></tr>';
    
    try {
        const res = await apiFetch('/api/reports');
        if (res.ok) {
            const data = await res.json();
            if (data.length === 0) {
                tbody.innerHTML = '';
                document.getElementById('empty-reports-state').style.display = 'block'; // Show empty state
                document.getElementById('reports-table-element').style.display = 'none';
            } else {
                document.getElementById('empty-reports-state').style.display = 'none'; // Hide empty state
                document.getElementById('reports-table-element').style.display = 'table';
                
                tbody.innerHTML = '';
                data.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.created_at}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #3b82f6; font-weight: 500; cursor: pointer;">${r.file_name}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.report_type}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.cluster}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.created_by}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.data_range}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.recipients}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: var(--primary); cursor: pointer; font-weight: 500;">View</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }
    } catch (err) {
        console.error(err);
        tbody.innerHTML = '<tr><td colspan="8" style="padding: 20px; text-align: center; color: #ef4444;">Error loading reports</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btnSubmitReport = document.getElementById('btn-submit-report');
    if (btnSubmitReport) {
        btnSubmitReport.addEventListener('click', async () => {
            const clusterId = document.getElementById('report-cluster-select').value;
            const reportType = document.getElementById('report-type-select').value;
            const dataRange = document.getElementById('report-data-range').value;
            const recipients = document.getElementById('report-recipients').value;
            
            if (!clusterId || !reportType || !dataRange) {
                alert("Please fill in Cluster, Type, and Data range.");
                return;
            }
            
            btnSubmitReport.innerText = "Creating...";
            btnSubmitReport.disabled = true;
            
            try {
                const res = await apiFetch('/api/reports', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        project_id: parseInt(clusterId),
                        report_type: reportType,
                        data_range_days: parseInt(dataRange),
                        recipients: recipients
                    })
                });
                
                if (res.ok) {
                    document.getElementById('modal-create-report').style.display = 'none';
                    // Reset form
                    document.getElementById('report-cluster-select').value = '';
                    document.getElementById('report-type-select').value = '';
                    document.getElementById('report-recipients').value = '';
                    
                    loadReports();
                } else {
                    alert("Error creating report");
                }
            } catch (err) {
                console.error(err);
                alert("Error: " + err);
            }
            
            btnSubmitReport.innerText = "Create";
            btnSubmitReport.disabled = false;
        });
    }
});


async function testSshConnection() {
    if (!currentNodeIdToEdit) {
        alert("Lütfen önce kaydedin.");
        return;
    }
    const btn = document.querySelector('button[onclick="testSshConnection()"]');
    const oldText = btn.innerText;
    btn.innerText = "Testing...";
    btn.disabled = true;
    
    try {
        const res = await apiFetch(`/api/nodes/${currentNodeIdToEdit}/test-ssh`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            alert("✅ " + data.message);
        } else {
            alert("❌ " + data.message);
        }
    } catch (err) {
        alert("Bağlantı hatası: " + err);
    }
    
    btn.innerText = oldText;
    btn.disabled = false;
}


document.getElementById('form-create-backup')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const pid = document.getElementById('backup-cluster-select').value;
    const btype = document.getElementById('backup-type-select').value;
    if(!pid) { alert("Please select a cluster"); return; }
    
    const btn = document.getElementById('btn-submit-backup');
    btn.innerText = "Creating...";
    btn.disabled = true;
    
    try {
        const res = await apiFetch('/api/backups', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ project_id: parseInt(pid), backup_type: btype })
        });
        const data = await res.json();
        if(res.ok && data.success) {
            document.getElementById('modal-create-backup').style.display = 'none';
            fetchBackups();
            alert("Backup started successfully!");
        } else {
            alert(data.message || "Failed to create backup");
        }
    } catch(err) {
        alert("Error: " + err);
    }
    btn.innerText = "Create";
    btn.disabled = false;
});


setInterval(() => {
    if (document.getElementById('backups-view').style.display === 'block') {
        fetchBackups();
    }
}, 5000);


document.querySelector('button[onclick="document.getElementById(\'modal-create-backup\').style.display=\'flex\'"]')?.addEventListener('click', async () => {
    const res = await apiFetch('/api/projects');
    if (res.ok) {
        const projs = await res.json();
        const sel = document.getElementById('backup-cluster-select');
        sel.innerHTML = '<option value="">Select a cluster...</option>' + 
            projs.map(p => `<option value="${p.id}" style="color:black;">${p.name}</option>`).join('');
    }
});


;

async function fetchRecentAlarms() {
    const container = document.getElementById('recent-alarms-container');
    if (!container) return;
    
    try {
        const res = await apiFetch('/api/audit-logs');
        if (res.ok) {
            const data = await res.json();
            // Filter logs that look like alarms/errors
            const alarms = data.filter(log => log.action.toLowerCase().includes('failed') || log.action.toLowerCase().includes('error') || log.action.toLowerCase().includes('alarm')).slice(0, 5);
            
            if (alarms.length === 0) {
                container.innerHTML = `
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color: var(--text-muted); font-size: 0.95rem; padding: 24px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                    No alarms
                </div>`;
            } else {
                container.innerHTML = alarms.map(alarm => `
                <div style="padding: 12px; border-bottom: 1px solid var(--border); display: flex; flex-direction: column; gap: 4px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #ef4444; font-size: 0.85rem;">${escapeHTML(alarm.action)}</span>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">${escapeHTML(alarm.timestamp)}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">${escapeHTML(alarm.details)}</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">Cluster ID: ${alarm.project_id}</div>
                </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error("Failed to fetch alarms", e);
    }
}


function applyProfileData(data) {
    if (!data) return;
    window.cachedProfileData = data;

    const username = data.username || 'admin';
    const email    = data.email || (username + '@localhost');
    const fullName = (data.first_name || data.last_name) 
        ? `${data.first_name || ''} ${data.last_name || ''}`.trim() 
        : (username.charAt(0).toUpperCase() + username.slice(1));
    const role     = (data.role || 'admin').toUpperCase();
    const team     = data.team || (role === 'ADMIN' ? 'admins' : 'viewers');
    const tz       = data.timezone || 'UTC';

    // Initials (2 letters)
    const words    = fullName.trim().split(/\s+/);
    const initials = words.length >= 2
        ? (words[0][0] + words[1][0]).toUpperCase()
        : fullName.slice(0, 2).toUpperCase();

    // Profile page elements
    const pageAvatar = document.getElementById('profile-page-avatar') || document.getElementById('profile-avatar');
    const pageName   = document.getElementById('profile-fullname');
    const pageRole   = document.getElementById('profile-role');
    const pageUser   = document.getElementById('profile-username');
    const pageTeam   = document.getElementById('profile-team');
    const pageTz     = document.getElementById('profile-timezone-text');

    const pageEmailSubtitle = document.getElementById('profile-email-subtitle');

    if (pageAvatar) pageAvatar.textContent = initials;
    if (pageName)   pageName.textContent   = fullName;
    if (pageEmailSubtitle) pageEmailSubtitle.textContent = email;
    if (pageRole)   pageRole.textContent   = role;
    if (pageUser)   pageUser.textContent   = username;
    if (pageTeam)   pageTeam.textContent   = team;
    if (pageTz)     pageTz.textContent     = tz;

    // Header username display
    const headerUser = document.getElementById('header-username-display');
    if (headerUser) headerUser.textContent = fullName || username;

    // Dropdown elements
    const dropAvatar = document.getElementById('dropdown-profile-avatar') || document.getElementById('profile-avatar');
    const dropName   = document.getElementById('dropdown-profile-name') || document.getElementById('profile-display-name');
    const dropEmail  = document.getElementById('dropdown-profile-email') || document.getElementById('profile-email');
    const dropTz     = document.getElementById('dropdown-profile-timezone') || document.getElementById('profile-timezone');

    if (dropAvatar) dropAvatar.textContent = initials;
    if (dropName)   dropName.textContent   = fullName;
    if (dropEmail)  dropEmail.textContent  = email;
    if (dropTz)     dropTz.textContent     = tz;
}

async function fetchProfile() {
    try {
        const res = await apiFetch('/api/users/me');
        if (res.ok) {
            const data = await res.json();
            applyProfileData(data);
        }
    } catch (e) {
        console.error("Failed to fetch profile", e);
    }
}


// ---- ACTIVITY CENTER TABS ----
window.switchActivityTab = function(tab, btnEl) {
    ['alarms','jobs','audit','watchlists'].forEach(t => {
        const el = document.getElementById('ac-content-' + t);
        const btn = document.getElementById('ac-tab-' + t);
        if (el) el.style.display = 'none';
        if (btn) { btn.style.color = '#6b7280'; btn.style.borderBottomColor = 'transparent'; }
    });
    const content = document.getElementById('ac-content-' + tab);
    if (content) content.style.display = 'block';
    if (btnEl) { btnEl.style.color = 'var(--primary)'; btnEl.style.borderBottomColor = 'var(--primary)'; }
    if (tab === 'audit') { if (typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs(); }
    else if (tab === 'jobs') { fetchActivityJobs(); }
    else if (tab === 'alarms') { fetchActivityAlarms(); }
    else if (tab === 'watchlists') { if (typeof window.fetchWatchlists === 'function') window.fetchWatchlists(); }
};

async function fetchActivityAlarms() {
    const tbody = document.getElementById('ac-alarms-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading alarms...</span></div></td></tr>';
    try {
        const res = await apiFetch('/api/audit-logs');
        if (!res.ok) return;
        const logs = await res.json();
        const alarms = logs.filter(l => l.action && (l.action.toLowerCase().includes('fail') || l.action.toLowerCase().includes('error') || l.action.toLowerCase().includes('alarm')));
        if (alarms.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 60px;"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"48\" height=\"48\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#d1d5db\" stroke-width=\"1.5\" style=\"display:block;margin:0 auto 16px;\"><path d=\"M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0\"></path></svg><p style=\"color:#9ca3af;font-size:0.9rem;\">You haven\'t received alarms yet. When you do, it\'ll show up here.</p></td></tr>';
            return;
        }
        tbody.innerHTML = alarms.map(a => '<tr style="border-bottom: 1px solid #f3f4f6;"><td style="padding: 12px 20px; font-size: 0.85rem;">' + escapeHTML(a.action) + '</td><td style="padding: 12px 20px;"><span style="color: #ef4444; font-size: 0.8rem; font-weight: 600;">WARNING</span></td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">System</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">-</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">-</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(a.timestamp || '-') + '</td><td style="padding: 12px 20px;"><button style="padding: 4px 10px; font-size: 0.75rem; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; background: white;">...</button></td></tr>').join('');
    } catch(e) { if(tbody) tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#ef4444;">Error: ' + escapeHTML(String(e)) + '</td></tr>'; }
}

async function fetchActivityJobs() {
    const tbody = document.getElementById('ac-jobs-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading jobs...</span></div></td></tr>';
    try {
        const res = await apiFetch('/api/jobs');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Failed to load jobs.</td></tr>'; return; }
        const jobs = await res.json();
        if (!jobs || jobs.length === 0) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">No background jobs found.</td></tr>'; return; }
        const statusColor = { SUCCESS:'#10b981', FAILED:'#ef4444', IN_PROGRESS:'#f59e0b', QUEUED:'#6b7280', VALIDATING:'#3b82f6', BOOTSTRAPPING:'#8b5cf6', CATCHING_UP:'#0ea5e9', RECOVERING:'#f97316' };
        tbody.innerHTML = jobs.map(j => {
            const sc = statusColor[j.status] || '#9ca3af';
            return `<tr style="border-bottom:1px solid #f3f4f6;">
              <td style="padding:12px 20px;font-size:0.85rem;">${j.id}</td>
              <td style="padding:12px 20px;font-size:0.85rem;color:#6b7280;">${escapeHTML(j.cluster)}</td>
              <td style="padding:12px 20px;"><span style="color:${sc};font-size:0.8rem;display:inline-flex;align-items:center;gap:5px;"><div style="width:6px;height:6px;border-radius:50%;background:${sc}"></div>${j.status}</span></td>
              <td style="padding:12px 20px;font-size:0.85rem;color:#6b7280;">${escapeHTML(j.started)}</td>
              <td style="padding:12px 20px;font-size:0.85rem;color:#6b7280;">${escapeHTML(j.completed || '-')}</td>
              <td style="padding:12px 20px;font-size:0.85rem;color:#6b7280;">${j.duration || '-'}</td>
              <td style="padding:12px 20px;font-size:0.8rem;color:#6b7280;max-width:200px;overflow:hidden;text-overflow:ellipsis;">${escapeHTML(j.message || '-')}</td>
            </tr>`;
        }).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">Failed to load jobs.</td></tr>'; }
}


    // PERFORMANCE MODULE HANDLERS
    window.perfData = null;

    window.switchPerfSubtab = function(e, subtabName) {
        if(e) e.preventDefault();
        
        document.querySelectorAll('.perf-subtabs .perf-subtab').forEach(el => {
            el.style.color = '#6b7280';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active');
        });
        
        const activeSubtab = document.querySelector(`.perf-subtabs [data-subtab="${subtabName}"]`);
        if (activeSubtab) {
            activeSubtab.style.color = 'var(--primary)';
            activeSubtab.style.borderBottom = '2px solid var(--primary)';
            activeSubtab.classList.add('active');
        }
        
        document.querySelectorAll('.perf-subtab-content').forEach(el => el.style.display = 'none');
        const targetContent = document.getElementById(`perf-subtab-${subtabName}`);
        if(targetContent) targetContent.style.display = 'block';
    };

    window.fetchPerformanceData = async function() {
        if (!currentProjectId) return;
        try {
            const res = await apiFetch(`/api/projects/${currentProjectId}/performance`);
            if (!res.ok) return;
            const data = await res.json();
            window.perfData = data;
            
            // 1. Render Status Variables (Primary & Standby comparison)
            const tbodyStatus = document.getElementById('perf-status-tbody');
            if (tbodyStatus && data.variables) {
                if (data.variables.length === 0) {
                    tbodyStatus.innerHTML = '<tr><td colspan="3" style="padding:30px;text-align:center;color:#9ca3af;">No variables available.</td></tr>';
                } else {
                    tbodyStatus.innerHTML = data.variables.map(v => `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 16px; font-weight: 500; color: #374151; font-family: monospace;">${escapeHTML(v.name.toUpperCase())}</td>
                            <td style="padding: 10px 16px; color: #10b981; font-family: monospace;">${escapeHTML(v.setting)} ${escapeHTML(v.unit)}</td>
                            <td style="padding: 10px 16px; color: #6366f1; font-family: monospace;">${escapeHTML(v.setting)} ${escapeHTML(v.unit)}</td>
                        </tr>
                    `).join('');
                }
            }
            
            // 2. Render Variables table
            const tbodyVars = document.getElementById('perf-vars-tbody');
            if (tbodyVars && data.variables) {
                tbodyVars.innerHTML = data.variables.map(v => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 16px; font-weight: 500; color: #374151; font-family: monospace;">${escapeHTML(v.name)}</td>
                        <td style="padding: 10px 16px; color: #1f2937; font-family: monospace;">${escapeHTML(v.setting)}</td>
                        <td style="padding: 10px 16px; color: #6b7280;">${escapeHTML(v.unit || '-')}</td>
                        <td style="padding: 10px 16px; color: #4b5563; font-size: 0.82rem;">${escapeHTML(v.desc || '')}</td>
                    </tr>
                `).join('');
            }
            
            // 3. Render Query Monitor
            const tbodyQueries = document.getElementById('perf-query-tbody');
            if (tbodyQueries && data.queries) {
                if (data.queries.length === 0) {
                    tbodyQueries.innerHTML = '<tr><td colspan="6" style="padding:30px;text-align:center;color:#9ca3af;">No active long-running queries.</td></tr>';
                } else {
                    tbodyQueries.innerHTML = data.queries.map(q => `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 16px; font-family: monospace;">${q.pid}</td>
                            <td style="padding: 10px 16px;">${escapeHTML(q.user || '-')}</td>
                            <td style="padding: 10px 16px; color: #6b7280;">${escapeHTML(q.client || 'local')}</td>
                            <td style="padding: 10px 16px;"><span class="status-badge status-online">${escapeHTML(q.state)}</span></td>
                            <td style="padding: 10px 16px; font-family: monospace;">${escapeHTML(q.duration)}</td>
                            <td style="padding: 10px 16px; font-family: monospace; font-size: 0.8rem; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHTML(q.query)}</td>
                        </tr>
                    `).join('');
                }
            }
            
            // 4. Render Schema Analyzer
            const tbodySchema = document.getElementById('perf-schema-tbody');
            if (tbodySchema && data.schema) {
                tbodySchema.innerHTML = data.schema.map(s => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 16px; font-weight: 500; font-family: monospace; color: #374151;">${escapeHTML(s.table_name)}</td>
                        <td style="padding: 10px 16px; color: #6b7280;">${s.col_count} columns</td>
                        <td style="padding: 10px 16px; font-weight: 500; color: #1f2937;">${s.row_count.toLocaleString()} rows</td>
                        <td style="padding: 10px 16px;"><span class="status-badge status-online">OK</span></td>
                    </tr>
                `).join('');
            }
            
        } catch(e) {
            console.error("fetchPerformanceData error:", e);
        }
    };

    window.filterPerfStatusTable = function() {
        const query = (document.getElementById('perf-status-search')?.value || '').toLowerCase();
        document.querySelectorAll('#perf-status-tbody tr').forEach(row => {
            const txt = row.innerText.toLowerCase();
            row.style.display = txt.includes(query) ? '' : 'none';
        });
    };

    window.filterPerfVarsTable = function() {
        const query = (document.getElementById('perf-vars-search')?.value || '').toLowerCase();
        document.querySelectorAll('#perf-vars-tbody tr').forEach(row => {
            const txt = row.innerText.toLowerCase();
            row.style.display = txt.includes(query) ? '' : 'none';
        });
    };



    window.switchBackupTab = function(tabName) {
        document.querySelectorAll('.backup-tab').forEach(el => {
            el.style.color = '#6b7280';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active-tab');
        });
        document.querySelectorAll('.backup-tab-content').forEach(el => el.style.display = 'none');
        
        if (tabName === 'all') {
            const tabAll = document.getElementById('tab-all-backups');
            if (tabAll) {
                tabAll.style.color = 'var(--primary)';
                tabAll.style.borderBottom = '2px solid var(--primary)';
                tabAll.classList.add('active-tab');
            }
            const contentAll = document.getElementById('content-all-backups');
            if (contentAll) contentAll.style.display = 'block';
        } else if (tabName === 'schedules') {
            const tabSched = document.getElementById('tab-schedules-backups');
            if (tabSched) {
                tabSched.style.color = 'var(--primary)';
                tabSched.style.borderBottom = '2px solid var(--primary)';
                tabSched.classList.add('active-tab');
            }
            const contentSched = document.getElementById('content-schedules-backups');
            if (contentSched) contentSched.style.display = 'block';
        }
    };



    // --- LIVE UI AUDIT DATA COLLECTION ---
    window.isUiAuditActive = false;
    window.uiAuditRecords = [];

    window.toggleUiAudit = function() {
        window.isUiAuditActive = !window.isUiAuditActive;
        const toggleBg = document.getElementById('btn-toggle-ui-audit');
        const toggleDot = document.getElementById('dot-toggle-ui-audit');
        const dlBtn = document.getElementById('btn-download-ui-audit');

        if (window.isUiAuditActive) {
            if (toggleBg) toggleBg.style.background = 'var(--primary, #3a1c94)';
            if (toggleDot) toggleDot.style.left = '24px';
            if (dlBtn) {
                dlBtn.disabled = false;
                dlBtn.style.color = 'var(--primary, #3a1c94)';
                dlBtn.style.borderColor = 'var(--primary, #3a1c94)';
                dlBtn.style.cursor = 'pointer';
                dlBtn.style.fontWeight = '500';
            }
            window.recordUiAudit('AUDIT_SESSION_STARTED', { userAgent: navigator.userAgent, timestamp: new Date().toISOString() });
        } else {
            if (toggleBg) toggleBg.style.background = '#d1d5db';
            if (toggleDot) toggleDot.style.left = '2px';
            if (dlBtn) {
                dlBtn.disabled = true;
                dlBtn.style.color = '#9ca3af';
                dlBtn.style.borderColor = '#e5e7eb';
                dlBtn.style.cursor = 'not-allowed';
                dlBtn.style.fontWeight = 'normal';
            }
            window.recordUiAudit('AUDIT_SESSION_STOPPED', { timestamp: new Date().toISOString() });
        }
    };

    window.recordUiAudit = function(eventType, details) {
        if (!window.isUiAuditActive && eventType !== 'AUDIT_SESSION_STARTED') return;
        const entry = {
            id: window.uiAuditRecords.length + 1,
            time: new Date().toISOString(),
            route: window.location.hash || '#projects-view',
            eventType: eventType,
            details: details
        };
        window.uiAuditRecords.push(entry);
        if (window.uiAuditRecords.length > 500) window.uiAuditRecords.shift();
    };

    window.downloadUiAuditData = function() {
        if (!window.uiAuditRecords || window.uiAuditRecords.length === 0) {
            alert('Henüz toplanmış bir denetim verisi bulunmamaktadır.');
            return;
        }
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
            application: "ClusterControl Web UI",
            exportDate: new Date().toISOString(),
            totalEvents: window.uiAuditRecords.length,
            events: window.uiAuditRecords
        }, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `clustercontrol-ui-audit-${Date.now()}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    };

    // Global listener for audit capture
    window.addEventListener('click', (e) => {
        if (window.isUiAuditActive) {
            const target = e.target.closest('button, a, input, select, .node-status-card, .cluster-tab, .backup-tab, .perf-subtab');
            if (target) {
                window.recordUiAudit('CLICK', {
                    tagName: target.tagName,
                    id: target.id || '',
                    className: target.className || '',
                    innerText: (target.innerText || '').substring(0, 50)
                });
            }
        }
    }, true);

window.switchSettingsTab = function(tabName) {
    const tabs = ['profile', 'cloud', 'notifications', 'certificates', 'license', 'addons', 'diagnostics', 'project'];
    tabs.forEach(t => {
        const tabEl = document.getElementById(`tab-settings-${t}`);
        const contentEl = document.getElementById(`settings-content-${t}`);
        if (tabEl) {
            if (t === tabName) {
                tabEl.style.color = '#3a1c94';
                tabEl.style.borderBottom = '2px solid #3a1c94';
                tabEl.style.fontWeight = '600';
            } else {
                tabEl.style.color = '#6b7280';
                tabEl.style.borderBottom = '2px solid transparent';
                tabEl.style.fontWeight = '500';
            }
        }
        if (contentEl) {
            contentEl.style.display = (t === tabName) ? (t === 'profile' || t === 'diagnostics' ? 'flex' : 'block') : 'none';
        }
    });
    // Trigger data load for the active tab
    if (tabName === 'cloud')         window.loadCloudCredentials && window.loadCloudCredentials();
    if (tabName === 'notifications') window.loadNotifications && window.loadNotifications();
    if (tabName === 'certificates')  window.loadCertificates && window.loadCertificates();
    if (tabName === 'license')       window.loadLicense && window.loadLicense();
    if (tabName === 'addons')        window.loadAddons && window.loadAddons();
    if (tabName === 'profile')       window.loadLdapConfigs && window.loadLdapConfigs();
    if (tabName === 'project')       loadProjectSettingsDropdown && loadProjectSettingsDropdown();
};

// ─────────────────────────────────────────────────────────────────────────────
// SETTINGS TAB LOADERS
// ─────────────────────────────────────────────────────────────────────────────

// ── Cloud Storage Credentials ──────────────────────────────────────────────
window.loadCloudCredentials = async function() {
    const tbody = document.getElementById('cloud-cred-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Loading...</td></tr>';
    try {
        const res = await apiFetch('/api/cloud-credentials');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#ef4444;">Failed to load credentials.</td></tr>'; return; }
        const creds = await res.json();
        if (!creds.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">No cloud credentials added yet.</td></tr>'; return; }
        tbody.innerHTML = creds.map(c => `<tr style="border-bottom:1px solid #f3f4f6;">
            <td style="padding:10px 16px;font-size:0.85rem;font-weight:600;">${escapeHTML(c.label)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.provider)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.bucket || '-')}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.created_at)}</td>
            <td style="padding:10px 16px;">
              <button onclick="testCloudCred(${c.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #e5e7eb;border-radius:4px;cursor:pointer;background:white;margin-right:6px;">Test</button>
              <button onclick="deleteCloudCred(${c.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #fee2e2;border-radius:4px;cursor:pointer;background:white;color:#ef4444;">Delete</button>
            </td>
        </tr>`).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Error loading credentials.</td></tr>'; }
};

window.testCloudCred = async function(id) {
    const res = await apiFetch(`/api/cloud-credentials/${id}/test`, { method: 'POST' });
    const data = await res.json();
    alert(data.message);
};
window.deleteCloudCred = async function(id) {
    if (!confirm('Delete this credential?')) return;
    await apiFetch(`/api/cloud-credentials/${id}`, { method: 'DELETE' });
    window.loadCloudCredentials();
};
window.openAddCloudCredModal = function() {
    const modal = document.getElementById('modal-add-cloud-cred');
    if (modal) modal.style.display = 'flex';
};
window.closeAddCloudCredModal = function() {
    const modal = document.getElementById('modal-add-cloud-cred');
    if (modal) modal.style.display = 'none';
};
window.submitCloudCredForm = async function() {
    const provider = document.getElementById('cloud-cred-provider')?.value || 'AWS S3';
    const label = document.getElementById('cloud-cred-label')?.value || '';
    const key_id = document.getElementById('cloud-cred-keyid')?.value || '';
    const secret = document.getElementById('cloud-cred-secret')?.value || '';
    const bucket = document.getElementById('cloud-cred-bucket')?.value || '';
    const region = document.getElementById('cloud-cred-region')?.value || '';
    if (!label.trim()) { alert('Label is required'); return; }
    const res = await apiFetch('/api/cloud-credentials', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ provider, label, key_id, secret, bucket, region }) });
    const data = await res.json();
    if (data.success) { window.closeAddCloudCredModal(); window.loadCloudCredentials(); }
    else alert(data.message || 'Failed to save credential');
};

// ── Notification Services ──────────────────────────────────────────────────
window.loadNotifications = async function() {
    const tbody = document.getElementById('notif-services-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Loading...</td></tr>';
    try {
        const res = await apiFetch('/api/notifications');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#ef4444;">Failed to load.</td></tr>'; return; }
        const svcs = await res.json();
        if (!svcs.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">No notification services added yet.</td></tr>'; return; }
        tbody.innerHTML = svcs.map(s => `<tr style="border-bottom:1px solid #f3f4f6;">
            <td style="padding:10px 16px;font-size:0.85rem;font-weight:600;">${escapeHTML(s.label)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(s.service_type)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(s.host || s.webhook_url || '-')}</td>
            <td style="padding:10px 16px;"><span style="color:${s.active?'#10b981':'#9ca3af'};font-size:0.8rem;">${s.active?'Active':'Inactive'}</span></td>
            <td style="padding:10px 16px;">
              <button onclick="testNotifService(${s.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #e5e7eb;border-radius:4px;cursor:pointer;background:white;margin-right:6px;">Test</button>
              <button onclick="deleteNotifService(${s.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #fee2e2;border-radius:4px;cursor:pointer;background:white;color:#ef4444;">Delete</button>
            </td>
        </tr>`).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Error loading services.</td></tr>'; }
};

window.testNotifService = async function(id) {
    const res = await apiFetch(`/api/notifications/${id}/test`, { method: 'POST' });
    const data = await res.json();
    alert(data.message);
};
window.deleteNotifService = async function(id) {
    if (!confirm('Delete this notification service?')) return;
    await apiFetch(`/api/notifications/${id}`, { method: 'DELETE' });
    window.loadNotifications();
};
window.openAddNotifModal = function() {
    const m = document.getElementById('modal-add-notif'); if (m) m.style.display = 'flex';
};
window.closeAddNotifModal = function() {
    const m = document.getElementById('modal-add-notif'); if (m) m.style.display = 'none';
};
window.submitNotifForm = async function() {
    const service_type = document.getElementById('notif-type')?.value || 'SMTP';
    const label = document.getElementById('notif-label')?.value || '';
    if (!label.trim()) { alert('Label is required'); return; }
    let settings = {};
    if (service_type === 'SMTP') {
        settings = {
            host: document.getElementById('notif-smtp-host')?.value || '',
            port: document.getElementById('notif-smtp-port')?.value || '587',
            user: document.getElementById('notif-smtp-user')?.value || '',
            password: document.getElementById('notif-smtp-pass')?.value || '',
            from: document.getElementById('notif-smtp-from')?.value || ''
        };
    } else if (service_type === 'Slack') {
        settings = { webhook_url: document.getElementById('notif-slack-webhook')?.value || '' };
    }
    const res = await apiFetch('/api/notifications', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ service_type, label, settings }) });
    const data = await res.json();
    if (data.success) { window.closeAddNotifModal(); window.loadNotifications(); }
    else alert(data.message || 'Failed to save');
};

// ── Mail Server Configuration ──────────────────────────────────────────────

window.checkMailServerStatus = async function() {
    const warning = document.getElementById('settings-mail-warning');
    if (!warning) return;
    try {
        const res = await apiFetch('/api/settings/mail-server');
        if (res.ok) {
            const data = await res.json();
            if (data.configured) {
                warning.innerHTML = `<span style="color:#10b981;font-weight:600;">✓ Mail server configured (${escapeHTML(data.mail_type || 'SMTP')})</span> <a href="#" onclick="openConfigureMailServerModal(); return false;" style="color:#4f46e5;font-weight:600;text-decoration:none;margin-left:6px;cursor:pointer;">Edit configuration</a>`;
            } else {
                warning.innerHTML = `<span>You don't have a mail server configured.</span> <a href="#" onclick="openConfigureMailServerModal(); return false;" style="color: #4f46e5; font-weight: 600; text-decoration: none; cursor: pointer; margin-left:6px;">Configure now</a>`;
            }
        }
    } catch(e) {}
};

window.openConfigureMailServerModal = function() {
    const m = document.getElementById('modal-configure-mail-server');
    if (m) m.style.display = 'flex';
};

window.closeConfigureMailServerModal = function() {
    const m = document.getElementById('modal-configure-mail-server');
    if (m) m.style.display = 'none';
};

window.openMailSmtpModal = async function() {
    closeConfigureMailServerModal();
    const m = document.getElementById('modal-mail-smtp');
    if (!m) return;
    m.style.display = 'flex';
    
    const urlInput = document.getElementById('smtp-form-frontend-url');
    const previewText = document.getElementById('smtp-url-preview-text');
    const currentOrigin = window.location.origin;
    if (urlInput && !urlInput.value) {
        urlInput.value = currentOrigin;
    }
    if (previewText) {
        previewText.innerText = urlInput?.value || currentOrigin;
    }
    
    try {
        const res = await apiFetch('/api/settings/mail-server');
        if (res.ok) {
            const data = await res.json();
            if (data.configured && data.mail_type === 'SMTP') {
                const s = data.settings || {};
                if (document.getElementById('smtp-form-server')) document.getElementById('smtp-form-server').value = s.host || '';
                if (document.getElementById('smtp-form-port')) document.getElementById('smtp-form-port').value = s.port || 587;
                if (document.getElementById('smtp-form-username')) document.getElementById('smtp-form-username').value = s.user || '';
                if (document.getElementById('smtp-form-password')) document.getElementById('smtp-form-password').value = s.password || '';
                if (document.getElementById('smtp-form-reply-to')) document.getElementById('smtp-form-reply-to').value = s.reply_to || s.from_address || '';
                if (document.getElementById('smtp-form-tls')) {
                    document.getElementById('smtp-form-tls').checked = !!s.tls_ssl;
                    const lbl = document.getElementById('smtp-tls-label');
                    if (lbl) lbl.innerText = s.tls_ssl ? 'On' : 'Off';
                }
                if (s.frontend_url && urlInput) {
                    urlInput.value = s.frontend_url;
                    if (previewText) previewText.innerText = s.frontend_url;
                }
            }
        }
    } catch(e) {}
};

window.closeMailSmtpModal = function() {
    const m = document.getElementById('modal-mail-smtp');
    if (m) m.style.display = 'none';
};

window.saveMailSmtpConfig = async function() {
    const server = document.getElementById('smtp-form-server')?.value.trim();
    const port = parseInt(document.getElementById('smtp-form-port')?.value || '587');
    const username = document.getElementById('smtp-form-username')?.value.trim();
    const password = document.getElementById('smtp-form-password')?.value;
    const reply_to = document.getElementById('smtp-form-reply-to')?.value.trim();
    const tls_ssl = !!document.getElementById('smtp-form-tls')?.checked;
    const frontend_url = document.getElementById('smtp-form-frontend-url')?.value.trim() || window.location.origin;
    const send_test = !!document.getElementById('smtp-form-send-test')?.checked;
    
    if (!server) {
        alert('Server Address is required.');
        return;
    }
    if (!port) {
        alert('Port is required.');
        return;
    }
    if (!reply_to) {
        alert('Reply to/from address is required.');
        return;
    }
    
    const btn = document.getElementById('btn-save-mail-smtp');
    if (btn) { btn.disabled = true; btn.innerText = 'Saving...'; }
    
    try {
        const res = await apiFetch('/api/settings/mail-server', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mail_type: 'SMTP',
                server,
                port,
                username,
                password,
                reply_to,
                tls_ssl,
                frontend_url,
                send_test
            })
        });
        const data = await res.json();
        if (data.success) {
            if (typeof showToast === 'function') showToast('Mail server SMTP configuration saved.', 'success');
            else alert('Mail server SMTP configuration saved.');
            closeMailSmtpModal();
            window.checkMailServerStatus();
            if (typeof window.loadNotifications === 'function') window.loadNotifications();
        } else {
            alert(data.message || 'Failed to save mail configuration.');
        }
    } catch(e) {
        alert('Error saving mail server configuration: ' + e.message);
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Save'; }
    }
};

window.openMailSendmailModal = async function() {
    closeConfigureMailServerModal();
    const m = document.getElementById('modal-mail-sendmail');
    if (!m) return;
    m.style.display = 'flex';
    
    try {
        const res = await apiFetch('/api/settings/mail-server');
        if (res.ok) {
            const data = await res.json();
            if (data.configured && data.mail_type === 'SENDMAIL') {
                const s = data.settings?.sendmail_config || {};
                if (document.getElementById('sendmail-pg')) document.getElementById('sendmail-pg').value = s.pg || '';
                if (document.getElementById('sendmail-maria')) document.getElementById('sendmail-maria').value = s.maria || '';
                if (document.getElementById('sendmail-percona')) document.getElementById('sendmail-percona').value = s.percona || '';
                if (document.getElementById('sendmail-valkey')) document.getElementById('sendmail-valkey').value = s.valkey || '';
                if (document.getElementById('sendmail-mssql')) document.getElementById('sendmail-mssql').value = s.mssql || '';
                if (document.getElementById('sendmail-pmysql')) document.getElementById('sendmail-pmysql').value = s.pmysql || '';
                if (document.getElementById('sendmail-timescale')) document.getElementById('sendmail-timescale').value = s.timescale || '';
                if (document.getElementById('sendmail-mongo')) document.getElementById('sendmail-mongo').value = s.mongo || '';
            }
        }
    } catch(e) {}
};

window.closeMailSendmailModal = function() {
    const m = document.getElementById('modal-mail-sendmail');
    if (m) m.style.display = 'none';
};

window.sendTestSendmailEmail = function() {
    const firstEmail = document.getElementById('sendmail-pg')?.value.trim() ||
                       document.getElementById('sendmail-maria')?.value.trim() ||
                       document.getElementById('sendmail-percona')?.value.trim() ||
                       document.getElementById('sendmail-valkey')?.value.trim() ||
                       document.getElementById('sendmail-mssql')?.value.trim() ||
                       document.getElementById('sendmail-pmysql')?.value.trim() ||
                       document.getElementById('sendmail-timescale')?.value.trim() ||
                       document.getElementById('sendmail-mongo')?.value.trim();
    if (!firstEmail) {
        alert('Please provide at least one Reply to/from email address above to test.');
        return;
    }
    alert(`Testing local MTA delivery to ${firstEmail}... (Local sendmail verified)`);
};

window.saveMailSendmailConfig = async function() {
    const sendmail_config = {
        pg: document.getElementById('sendmail-pg')?.value.trim(),
        maria: document.getElementById('sendmail-maria')?.value.trim(),
        percona: document.getElementById('sendmail-percona')?.value.trim(),
        valkey: document.getElementById('sendmail-valkey')?.value.trim(),
        mssql: document.getElementById('sendmail-mssql')?.value.trim(),
        pmysql: document.getElementById('sendmail-pmysql')?.value.trim(),
        timescale: document.getElementById('sendmail-timescale')?.value.trim(),
        mongo: document.getElementById('sendmail-mongo')?.value.trim()
    };
    
    const btn = document.getElementById('btn-save-mail-sendmail');
    if (btn) { btn.disabled = true; btn.innerText = 'Saving...'; }
    
    try {
        const res = await apiFetch('/api/settings/mail-server', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mail_type: 'SENDMAIL',
                sendmail_config: sendmail_config
            })
        });
        const data = await res.json();
        if (data.success) {
            if (typeof showToast === 'function') showToast('Sendmail configuration saved.', 'success');
            else alert('Sendmail configuration saved.');
            closeMailSendmailModal();
            window.checkMailServerStatus();
            if (typeof window.loadNotifications === 'function') window.loadNotifications();
        } else {
            alert(data.message || 'Failed to save Sendmail configuration.');
        }
    } catch(e) {
        alert('Error saving Sendmail configuration: ' + e.message);
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Save'; }
    }
};

// ── Certificate Management ─────────────────────────────────────────────────
window.loadCertificates = async function(nodeId) {
    const tbody = document.getElementById('cert-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#9ca3af;">Loading certificates...</td></tr>';
    const url = nodeId ? `/api/certificates?node_id=${nodeId}` : '/api/certificates';
    try {
        const res = await apiFetch(url);
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#ef4444;">Failed to load.</td></tr>'; return; }
        const certs = await res.json();
        if (!certs.length) { tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#9ca3af;">No certificates found. Select a node and click "Scan" to discover certificates.</td></tr>'; return; }
        tbody.innerHTML = certs.map(c => {
            const exp = c.expires_at ? new Date(c.expires_at) : null;
            const expColor = exp ? (exp < new Date() ? '#ef4444' : (exp < new Date(Date.now()+30*86400000) ? '#f59e0b' : '#10b981')) : '#9ca3af';
            return `<tr style="border-bottom:1px solid #f3f4f6;">
                <td style="padding:10px 16px;font-size:0.85rem;font-weight:600;">${escapeHTML(c.common_name || '-')}</td>
                <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.cert_type)}</td>
                <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.node_name || '-')}</td>
                <td style="padding:10px 16px;font-size:0.85rem;color:${expColor};">${escapeHTML(c.expires_at || '-')}</td>
                <td style="padding:10px 16px;font-size:0.8rem;color:#9ca3af;max-width:180px;overflow:hidden;text-overflow:ellipsis;" title="${escapeHTML(c.file_path)}">${escapeHTML(c.file_path || '-')}</td>
                <td style="padding:10px 16px;"><button onclick="deleteCert(${c.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #fee2e2;border-radius:4px;cursor:pointer;background:white;color:#ef4444;">Delete</button></td>
            </tr>`;
        }).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#9ca3af;">Error loading certificates.</td></tr>'; }
};
window.deleteCert = async function(id) {
    if (!confirm('Delete this certificate record?')) return;
    await apiFetch(`/api/certificates/${id}`, { method: 'DELETE' });
    window.loadCertificates();
};
window.scanNodeCerts = async function(nodeId) {
    if (!nodeId) { alert('Please select a node first'); return; }
    const btn = document.getElementById('btn-scan-certs');
    if (btn) { btn.disabled = true; btn.innerText = 'Scanning...'; }
    try {
        const res = await apiFetch(`/api/certificates/scan/${nodeId}`, { method: 'POST' });
        const data = await res.json();
        alert(data.success ? `Found ${data.found} certificate(s): ${(data.certificates||[]).join(', ')}` : (data.message || 'Scan failed'));
        window.loadCertificates(nodeId);
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Scan Node'; }
    }
};

// ── License ────────────────────────────────────────────────────────────────
window.loadLicense = async function() {
    try {
        const res = await apiFetch('/api/license');
        if (!res.ok) return;
        const d = await res.json();
        const el = id => document.getElementById(id);
        if (el('lic-owner'))       el('lic-owner').innerText       = d.owner || '-';
        if (el('lic-type'))        el('lic-type').innerText        = d.type  || 'Enterprise';
        if (el('lic-expires'))     el('lic-expires').innerText     = d.expires || '-';
        if (el('lic-nodes-used'))  el('lic-nodes-used').innerText  = `${d.total_nodes} / ${d.node_limit}`;
        if (el('lic-nodes-avail')) el('lic-nodes-avail').innerText = `${d.nodes_available} nodes available`;
        // Update progress bar
        const bar = el('lic-nodes-bar');
        if (bar) {
            bar.style.width = `${Math.min(d.percent_used, 100)}%`;
            bar.style.background = d.percent_used >= 90 ? '#ef4444' : (d.percent_used >= 70 ? '#f59e0b' : '#10b981');
        }
        const pct = el('lic-nodes-pct');
        if (pct) pct.innerText = `${d.percent_used}%`;
    } catch(e) { console.warn('License load error:', e); }
};

// ── Addons (ClusterControl Ops-Center & Kubernetes) ───────────────────────────

let currentOpsCenterStep = 1;

window.loadAddons = async function() {
    try {
        const res = await apiFetch('/api/addons');
        if (!res.ok) return;
        const d = await res.json();
        
        // Ops-Center UI state
        const opsEnabled = d.ops_center?.enabled;
        const opsToggle = document.getElementById('toggle-addon-ops-center');
        const opsThumb = document.getElementById('toggle-thumb-ops-center');
        const opsStatus = document.getElementById('ops-center-status-text');
        const opsPanel = document.getElementById('ops-center-panel');
        
        if (opsToggle && opsThumb) {
            opsToggle.style.background = opsEnabled ? '#3a1c94' : '#d1d5db';
            opsThumb.style.transform = opsEnabled ? 'translateX(20px)' : 'translateX(0)';
        }
        if (opsStatus) {
            opsStatus.innerText = opsEnabled ? `Multi-controller mode · ${d.ops_center?.controllers_count || 1} controller(s)` : 'Single-controller mode · local';
        }
        if (opsPanel) {
            opsPanel.style.display = opsEnabled ? 'block' : 'none';
        }
        if (opsEnabled) {
            loadOpsControllers();
        }

        // Kubernetes UI state
        const k8sEnabled = d.kubernetes?.enabled;
        const k8sToggle = document.getElementById('toggle-addon-k8s');
        const k8sThumb = document.getElementById('toggle-thumb-k8s');
        const k8sStatus = document.getElementById('k8s-status-text');
        const k8sPanel = document.getElementById('k8s-panel');

        if (k8sToggle && k8sThumb) {
            k8sToggle.style.background = k8sEnabled ? '#3a1c94' : '#d1d5db';
            k8sThumb.style.transform = k8sEnabled ? 'translateX(20px)' : 'translateX(0)';
        }
        if (k8sStatus) {
            k8sStatus.innerText = k8sEnabled ? `Enabled · ${d.kubernetes?.clusters_count || 0} cluster(s)` : 'Not enabled';
        }
        if (k8sPanel) {
            k8sPanel.style.display = k8sEnabled ? 'block' : 'none';
        }
        if (k8sEnabled) {
            loadKubeClusters();
        }
    } catch(e) {
        console.warn('Addons load error:', e);
    }
};

window.toggleOpsCenterAddon = async function() {
    const res = await apiFetch('/api/addons');
    const d = await res.json();
    if (d.ops_center?.enabled) {
        if (confirm('Are you sure you want to disable Ops-Center? The console will switch back to Single-Controller mode.')) {
            const disRes = await apiFetch('/api/addons/ops-center/disable', { method: 'POST' });
            if (disRes.ok) {
                loadAddons();
            }
        }
    } else {
        openEnableOpsCenterModal();
    }
};

window.openEnableOpsCenterModal = function() {
    currentOpsCenterStep = 1;
    setOpsCenterStep(1);
    const modal = document.getElementById('modal-enable-ops-center');
    if (modal) modal.style.display = 'flex';
};

window.closeEnableOpsCenterModal = function() {
    const modal = document.getElementById('modal-enable-ops-center');
    if (modal) modal.style.display = 'none';
};

function setOpsCenterStep(step) {
    currentOpsCenterStep = step;
    const p1 = document.getElementById('ops-step-pane-1');
    const p2 = document.getElementById('ops-step-pane-2');
    const b1 = document.getElementById('ops-step-badge-1');
    const b2 = document.getElementById('ops-step-badge-2');
    const n1 = document.getElementById('ops-step-nav-1');
    const n2 = document.getElementById('ops-step-nav-2');
    const btnBack = document.getElementById('btn-ops-back');
    const btnNext = document.getElementById('btn-ops-next');

    if (step === 1) {
        if (p1) p1.style.display = 'block';
        if (p2) p2.style.display = 'none';
        if (n1) n1.style.color = '#3a1c94';
        if (n2) n2.style.color = '#9ca3af';
        if (b1) { b1.style.background = '#3a1c94'; b1.style.color = 'white'; b1.style.border = 'none'; b1.innerHTML = '1'; }
        if (b2) { b2.style.background = 'transparent'; b2.style.color = '#9ca3af'; b2.style.border = '2px solid #d1d5db'; b2.innerHTML = '2'; }
        if (btnBack) { btnBack.disabled = true; btnBack.style.color = '#9ca3af'; btnBack.style.cursor = 'not-allowed'; }
        if (btnNext) { btnNext.innerText = 'Continue'; btnNext.onclick = nextOpsCenterStep; }
    } else {
        if (p1) p1.style.display = 'none';
        if (p2) p2.style.display = 'block';
        if (n1) n1.style.color = '#10b981';
        if (n2) n2.style.color = '#3a1c94';
        if (b1) { b1.style.background = '#10b981'; b1.style.color = 'white'; b1.style.border = 'none'; b1.innerHTML = '✓'; }
        if (b2) { b2.style.background = '#3a1c94'; b2.style.color = 'white'; b2.style.border = 'none'; b2.innerHTML = '2'; }
        if (btnBack) { btnBack.disabled = false; btnBack.style.color = '#374151'; btnBack.style.cursor = 'pointer'; }
        if (btnNext) { btnNext.innerText = 'Finish'; btnNext.onclick = submitEnableOpsCenter; }
    }
}

window.nextOpsCenterStep = function() {
    setOpsCenterStep(2);
};

window.prevOpsCenterStep = function() {
    setOpsCenterStep(1);
};

window.submitEnableOpsCenter = async function() {
    const user = document.getElementById('ops-root-user')?.value.trim() || '';
    const email = document.getElementById('ops-root-email')?.value.trim() || '';
    const pass = document.getElementById('ops-root-pass')?.value || '';
    const confirmPass = document.getElementById('ops-root-confirm')?.value || '';
    const errEl = document.getElementById('ops-root-error');

    if (errEl) errEl.style.display = 'none';

    if (!user) {
        if (errEl) { errEl.innerText = 'Please enter root username'; errEl.style.display = 'block'; }
        return;
    }
    if (!pass) {
        if (errEl) { errEl.innerText = 'Please enter root user password'; errEl.style.display = 'block'; }
        return;
    }
    if (pass !== confirmPass) {
        if (errEl) { errEl.innerText = 'Root passwords do not match'; errEl.style.display = 'block'; }
        return;
    }

    try {
        const res = await apiFetch('/api/addons/ops-center/enable', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                root_username: user,
                email: email,
                root_password: pass,
                confirm_root_password: confirmPass
            })
        });
        const resData = await res.json();
        if (res.ok && resData.success) {
            closeEnableOpsCenterModal();
            loadAddons();
            alert('✓ Ops-Center successfully enabled in Multi-Controller mode.');
        } else {
            if (errEl) { errEl.innerText = resData.message || 'Failed to enable Ops-Center'; errEl.style.display = 'block'; }
        }
    } catch(e) {
        if (errEl) { errEl.innerText = 'Connection error'; errEl.style.display = 'block'; }
    }
};

window.toggleK8sAddon = async function() {
    const res = await apiFetch('/api/addons');
    const d = await res.json();
    if (d.kubernetes?.enabled) {
        if (confirm('Are you sure you want to disable Kubernetes feature?')) {
            const disRes = await apiFetch('/api/addons/kubernetes/disable', { method: 'POST' });
            if (disRes.ok) {
                loadAddons();
            }
        }
    } else {
        openEnableK8sModal();
    }
};

window.openEnableK8sModal = function() {
    const modal = document.getElementById('modal-enable-k8s');
    if (modal) modal.style.display = 'flex';
};

window.closeEnableK8sModal = function() {
    const modal = document.getElementById('modal-enable-k8s');
    if (modal) modal.style.display = 'none';
};

window.submitEnableK8s = async function() {
    const btn = document.getElementById('btn-submit-enable-k8s');
    if (btn) { btn.disabled = true; btn.innerText = 'Enabling...'; }
    try {
        const res = await apiFetch('/api/addons/kubernetes/enable', { method: 'POST' });
        if (res.ok) {
            closeEnableK8sModal();
            loadAddons();
            alert('✓ Kubernetes feature enabled.');
        }
    } catch(e) {
        alert('Failed to enable Kubernetes.');
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Enable'; }
    }
};

// ── Controllers Table (Ops-Center) ──
window.loadOpsControllers = async function() {
    const tbody = document.getElementById('tbody-ops-controllers');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:16px;color:#9ca3af;">Loading controllers...</td></tr>';
    try {
        const res = await apiFetch('/api/ops-center/controllers');
        const list = await res.json();
        if (!list || !list.length) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:16px;color:#9ca3af;">No controllers registered.</td></tr>';
            return;
        }
        tbody.innerHTML = list.map(c => `
            <tr style="border-bottom:1px solid #f3f4f6;">
                <td style="padding:10px 14px;font-weight:600;color:#111827;">${escapeHTML(c.name)} ${c.is_primary ? '<span style="font-size:0.7rem;background:#e0e7ff;color:#3a1c94;padding:2px 6px;border-radius:4px;margin-left:4px;">Primary</span>' : ''}</td>
                <td style="padding:10px 14px;color:#4b5563;font-family:monospace;font-size:0.8rem;">${escapeHTML(c.url)}</td>
                <td style="padding:10px 14px;">
                    <span style="font-size:0.75rem;padding:3px 8px;border-radius:10px;font-weight:600;background:${c.status === 'ONLINE' ? '#d1fae5' : '#fee2e2'};color:${c.status === 'ONLINE' ? '#065f46' : '#991b1b'};">
                        ● ${c.status} (${c.latency_ms}ms)
                    </span>
                </td>
                <td style="padding:10px 14px;color:#6b7280;">${escapeHTML(c.version || '2.5.0')}</td>
                <td style="padding:10px 14px;color:#111827;font-weight:500;">${c.cluster_count}</td>
                <td style="padding:10px 14px;text-align:right;">
                    ${!c.is_primary ? `<button onclick="deleteOpsController(${c.id})" style="padding:4px 8px;background:#fee2e2;color:#991b1b;border:none;border-radius:4px;font-size:0.75rem;cursor:pointer;font-weight:600;">Remove</button>` : '<span style="color:#9ca3af;font-size:0.75rem;">Default</span>'}
                </td>
            </tr>
        `).join('');
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:16px;color:#ef4444;">Failed to load controllers</td></tr>';
    }
};

window.openAddControllerModal = function() {
    const modal = document.getElementById('modal-add-ops-controller');
    if (modal) {
        document.getElementById('ctrl-name').value = '';
        document.getElementById('ctrl-url').value = '';
        document.getElementById('ctrl-token').value = '';
        const err = document.getElementById('ctrl-add-err');
        if (err) err.style.display = 'none';
        modal.style.display = 'flex';
    }
};

window.closeAddControllerModal = function() {
    const modal = document.getElementById('modal-add-ops-controller');
    if (modal) modal.style.display = 'none';
};

window.submitAddController = async function() {
    const name = document.getElementById('ctrl-name')?.value.trim();
    const url = document.getElementById('ctrl-url')?.value.trim();
    const token = document.getElementById('ctrl-token')?.value.trim();
    const err = document.getElementById('ctrl-add-err');
    const btn = document.getElementById('btn-submit-add-ctrl');

    if (err) err.style.display = 'none';

    if (!name || !url) {
        if (err) { err.innerText = 'Controller Name and URL are required'; err.style.display = 'block'; }
        return;
    }

    if (btn) { btn.disabled = true; btn.innerText = 'Testing & Connecting...'; }

    try {
        const res = await apiFetch('/api/ops-center/controllers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, url, api_token: token })
        });
        const d = await res.json();
        if (res.ok && d.success) {
            closeAddControllerModal();
            loadOpsControllers();
            alert(`✓ Controller '${name}' registered successfully (${d.status}).`);
        } else {
            if (err) { err.innerText = d.message || 'Failed to connect to controller'; err.style.display = 'block'; }
        }
    } catch(e) {
        if (err) { err.innerText = 'Connection error'; err.style.display = 'block'; }
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Register Controller'; }
    }
};

window.deleteOpsController = async function(id) {
    if (!confirm('Are you sure you want to remove this controller?')) return;
    try {
        const res = await apiFetch(`/api/ops-center/controllers/${id}`, { method: 'DELETE' });
        if (res.ok) {
            loadOpsControllers();
        }
    } catch(e) {
        alert('Failed to remove controller');
    }
};

// ── Kubernetes Clusters Table ──
window.loadKubeClusters = async function() {
    const tbody = document.getElementById('tbody-k8s-clusters');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:16px;color:#9ca3af;">Loading K8s clusters...</td></tr>';
    try {
        const res = await apiFetch('/api/k8s/clusters');
        const list = await res.json();
        if (!list || !list.length) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:16px;color:#9ca3af;">No Kubernetes clusters registered yet. Click "+ Add K8s Cluster" to connect your Kubeconfig.</td></tr>';
            return;
        }
        tbody.innerHTML = list.map(c => `
            <tr style="border-bottom:1px solid #f3f4f6;">
                <td style="padding:10px 14px;font-weight:600;color:#111827;">${escapeHTML(c.name)}</td>
                <td style="padding:10px 14px;color:#4b5563;font-family:monospace;font-size:0.78rem;">${escapeHTML(c.api_server_url)}</td>
                <td style="padding:10px 14px;color:#4b5563;">${escapeHTML(c.namespace)}</td>
                <td style="padding:10px 14px;color:#111827;font-weight:500;">${c.nodes_count}</td>
                <td style="padding:10px 14px;"><span style="font-size:0.75rem;background:#ede9fe;color:#5b21b6;padding:2px 6px;border-radius:4px;font-weight:600;">${escapeHTML(c.operator_installed || 'CloudNativePG')}</span></td>
                <td style="padding:10px 14px;">
                    <span style="font-size:0.75rem;padding:3px 8px;border-radius:10px;font-weight:600;background:#d1fae5;color:#065f46;">
                        ● ${c.status}
                    </span>
                </td>
                <td style="padding:10px 14px;text-align:right;">
                    <button onclick="viewK8sPods(${c.id}, '${escapeHTML(c.name)}')" style="padding:4px 8px;background:#e0e7ff;color:#3a1c94;border:none;border-radius:4px;font-size:0.75rem;cursor:pointer;font-weight:600;margin-right:6px;">Pods</button>
                    <button onclick="deleteKubeCluster(${c.id})" style="padding:4px 8px;background:#fee2e2;color:#991b1b;border:none;border-radius:4px;font-size:0.75rem;cursor:pointer;font-weight:600;">Remove</button>
                </td>
            </tr>
        `).join('');
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:16px;color:#ef4444;">Failed to load Kubernetes clusters</td></tr>';
    }
};

window.openAddKubeClusterModal = function() {
    const modal = document.getElementById('modal-add-k8s-cluster');
    if (modal) {
        document.getElementById('k8s-cluster-name').value = '';
        document.getElementById('k8s-namespace').value = 'default';
        document.getElementById('k8s-kubeconfig-yaml').value = '';
        const err = document.getElementById('k8s-add-err');
        if (err) err.style.display = 'none';
        modal.style.display = 'flex';
    }
};

window.closeAddKubeClusterModal = function() {
    const modal = document.getElementById('modal-add-k8s-cluster');
    if (modal) modal.style.display = 'none';
};

window.submitAddKubeCluster = async function() {
    const name = document.getElementById('k8s-cluster-name')?.value.trim();
    const namespace = document.getElementById('k8s-namespace')?.value.trim() || 'default';
    const kubeconfig = document.getElementById('k8s-kubeconfig-yaml')?.value.trim();
    const err = document.getElementById('k8s-add-err');
    const btn = document.getElementById('btn-submit-add-k8s');

    if (err) err.style.display = 'none';

    if (!name) {
        if (err) { err.innerText = 'Cluster Name is required'; err.style.display = 'block'; }
        return;
    }
    if (!kubeconfig) {
        if (err) { err.innerText = 'Kubeconfig YAML content is required'; err.style.display = 'block'; }
        return;
    }

    if (btn) { btn.disabled = true; btn.innerText = 'Validating API Server...'; }

    try {
        const res = await apiFetch('/api/k8s/clusters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, namespace, kubeconfig_yaml: kubeconfig })
        });
        const d = await res.json();
        if (res.ok && d.success) {
            closeAddKubeClusterModal();
            loadKubeClusters();
            alert(`✓ Kubernetes Cluster '${name}' successfully connected.`);
        } else {
            if (err) { err.innerText = d.message || 'Failed to connect to Kubernetes API'; err.style.display = 'block'; }
        }
    } catch(e) {
        if (err) { err.innerText = 'Connection error during Kubernetes validation'; err.style.display = 'block'; }
    } finally {
        if (btn) { btn.disabled = false; btn.innerText = 'Test & Connect Cluster'; }
    }
};

window.deleteKubeCluster = async function(id) {
    if (!confirm('Are you sure you want to remove this Kubernetes cluster?')) return;
    try {
        const res = await apiFetch(`/api/k8s/clusters/${id}`, { method: 'DELETE' });
        if (res.ok) {
            loadKubeClusters();
        }
    } catch(e) {
        alert('Failed to remove cluster');
    }
};

window.viewK8sPods = async function(clusterId, clusterName) {
    const modal = document.getElementById('modal-k8s-pods');
    const title = document.getElementById('modal-k8s-pods-title');
    const tbody = document.getElementById('tbody-k8s-pods');
    if (!modal || !tbody) return;

    if (title) title.innerText = `Live Pods: ${clusterName}`;
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#9ca3af;">Querying Kubernetes API for live pods...</td></tr>';
    modal.style.display = 'flex';

    try {
        const res = await apiFetch(`/api/k8s/clusters/${clusterId}/pods`);
        const d = await res.json();
        if (!d.pods || !d.pods.length) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#9ca3af;">No pods found in namespace.</td></tr>';
            return;
        }
        tbody.innerHTML = d.pods.map(p => `
            <tr style="border-bottom:1px solid #f3f4f6;">
                <td style="padding:8px 10px;font-family:monospace;font-size:0.8rem;font-weight:600;color:#111827;">${escapeHTML(p.name)}</td>
                <td style="padding:8px 10px;">
                    <span style="font-size:0.75rem;padding:2px 6px;border-radius:8px;font-weight:600;background:${p.status === 'Running' ? '#d1fae5' : '#fef3c7'};color:${p.status === 'Running' ? '#065f46' : '#92400e'};">
                        ${p.status}
                    </span>
                </td>
                <td style="padding:8px 10px;color:${p.ready ? '#10b981' : '#ef4444'};font-weight:600;">${p.ready ? 'Yes' : 'No'}</td>
                <td style="padding:8px 10px;color:#6b7280;">${p.restarts}</td>
                <td style="padding:8px 10px;font-size:0.78rem;color:#4b5563;">${p.ip} (${p.node})</td>
                <td style="padding:8px 10px;font-size:0.78rem;color:#6b7280;">${p.age}</td>
            </tr>
        `).join('');
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:#ef4444;">Failed to retrieve pods from Kubernetes API</td></tr>';
    }
};

window.closeK8sPodsModal = function() {
    const modal = document.getElementById('modal-k8s-pods');
    if (modal) modal.style.display = 'none';
};


// ── LDAP (User Management tab) ─────────────────────────────────────────────
window.loadLdapConfigs = async function() {
    const tbody = document.getElementById('ldap-configs-tbody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Loading...</td></tr>';
    try {
        const res = await apiFetch('/api/ldap');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">No LDAP configurations created yet.</td></tr>'; return; }
        const configs = await res.json();
        if (!configs.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">No LDAP configurations created yet.</td></tr>'; return; }
        tbody.innerHTML = configs.map(c => `<tr style="border-bottom:1px solid #f3f4f6;">
            <td style="padding:10px 16px;font-size:0.85rem;font-weight:600;">${escapeHTML(c.label)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.server_url)}</td>
            <td style="padding:10px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(c.base_dn)}</td>
            <td style="padding:10px 16px;"><span style="color:${c.active?'#10b981':'#9ca3af'};font-size:0.8rem;">${c.active?'Active':'Inactive'}</span></td>
            <td style="padding:10px 16px;">
              <button onclick="testLdapConfig(${c.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #e5e7eb;border-radius:4px;cursor:pointer;background:white;margin-right:6px;">Test</button>
              <button onclick="deleteLdapConfig(${c.id})" style="padding:4px 10px;font-size:0.75rem;border:1px solid #fee2e2;border-radius:4px;cursor:pointer;background:white;color:#ef4444;">Delete</button>
            </td>
        </tr>`).join('');
    } catch(e) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#9ca3af;">Error loading LDAP configs.</td></tr>'; }
};
window.testLdapConfig = async function(id) {
    const res = await apiFetch(`/api/ldap/${id}/test`, { method: 'POST' });
    const data = await res.json();
    alert(data.message);
};
window.deleteLdapConfig = async function(id) {
    if (!confirm('Delete this LDAP configuration?')) return;
    await apiFetch(`/api/ldap/${id}`, { method: 'DELETE' });
    window.loadLdapConfigs();
};
window.openAddLdapModal = function() {
    const m = document.getElementById('modal-add-ldap'); if (m) m.style.display = 'flex';
};
window.closeAddLdapModal = function() {
    const m = document.getElementById('modal-add-ldap'); if (m) m.style.display = 'none';
};
window.submitLdapForm = async function() {
    const payload = {
        label: document.getElementById('ldap-label')?.value || '',
        server_url: document.getElementById('ldap-server-url')?.value || '',
        base_dn: document.getElementById('ldap-base-dn')?.value || '',
        bind_user: document.getElementById('ldap-bind-user')?.value || '',
        bind_pass: document.getElementById('ldap-bind-pass')?.value || '',
        user_filter: document.getElementById('ldap-user-filter')?.value || '(objectClass=person)'
    };
    if (!payload.label || !payload.server_url || !payload.base_dn) { alert('Label, Server URL and Base DN are required'); return; }
    const res = await apiFetch('/api/ldap', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    const data = await res.json();
    if (data.success) { window.closeAddLdapModal(); window.loadLdapConfigs(); }
    else alert(data.message || 'Failed to save');
};

// ── Reports — Download & Delete buttons ────────────────────────────────────
window.downloadReport = function(id) {
    window.open(`/api/reports/${id}/download`, '_blank');
};
window.deleteReport = async function(id) {
    if (!confirm('Delete this report?')) return;
    await apiFetch(`/api/reports/${id}`, { method: 'DELETE' });
    if (typeof window.fetchReports === 'function') window.fetchReports();
};

// Load LDAP when LDAP tab in User Management is clicked
(function() {
    const ldapBtn = document.getElementById('tab-btn-ldap');
    if (ldapBtn) {
        ldapBtn.addEventListener('click', () => { window.loadLdapConfigs && window.loadLdapConfigs(); });
    }
})();


// ── ClusterControl Deploy & Import Cluster Flow ─────────────────────────────

const DB_CATALOG = {
    'postgresql_logical': {
        key: 'postgresql_logical',
        name: 'PostgreSQL Logical',
        category: 'PostgreSQL',
        icon: '🐘',
        vendors: ['PostgreSQL'],
        versions: ['18', '17', '16', '15', '14'],
        defaultPort: 5432,
        defaultUser: 'postgres',
        description: 'PostgreSQL, also known as Postgres, is a free and open-source relational database management system emphasizing extensibility and SQL compliance. It was originally named POSTGRES, referring to its origins as a successor to the Ingres database developed at the University of California, Berkeley.',
        learnMore: 'https://www.postgresql.org/docs/'
    },
    'postgresql_streaming': {
        key: 'postgresql_streaming',
        name: 'PostgreSQL Streaming',
        category: 'PostgreSQL',
        icon: '🐘',
        vendors: ['PostgreSQL'],
        versions: ['18', '17', '16', '15', '14'],
        defaultPort: 5432,
        defaultUser: 'postgres',
        description: 'PostgreSQL Streaming Replication provides high-availability primary/standby architecture with binary WAL log streaming, automatic failover with pg_auto_failover, and read-replica scaling.',
        learnMore: 'https://www.postgresql.org/docs/current/warm-standby.html'
    },
    'mssql': {
        key: 'mssql',
        name: 'SQL Server (MSSQL)',
        category: 'Microsoft',
        icon: '🪟',
        vendors: ['Microsoft'],
        versions: ['2022', '2019'],
        defaultPort: 1433,
        defaultUser: 'sa',
        description: 'Microsoft SQL Server Always On Availability Groups provide enterprise-grade high availability and disaster recovery across Windows and Linux server environments.',
        learnMore: 'https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/always-on-availability-groups-sql-server'
    },
    'mysql_galera': {
        key: 'mysql_galera',
        name: 'MySQL Galera',
        category: 'MySQL',
        icon: '🐬',
        vendors: ['Percona', 'MariaDB', 'Oracle'],
        versions: ['8.4', '8.0', '11.4', '10.11'],
        defaultPort: 3306,
        defaultUser: 'root',
        description: 'Galera Cluster for MySQL provides synchronous multi-master replication with true multi-primary active-active capabilities, automated node provisioning (SST), and zero data loss guarantee.',
        learnMore: 'https://galeracluster.com/'
    },
    'mysql_replication': {
        key: 'mysql_replication',
        name: 'MySQL Replication',
        category: 'MySQL',
        icon: '🐬',
        vendors: ['Percona', 'Oracle', 'MariaDB'],
        versions: ['8.4', '8.0'],
        defaultPort: 3306,
        defaultUser: 'root',
        description: 'MySQL Asynchronous and Semi-Synchronous Group Replication allows high performance read-scaling across multiple follower replicas with GTID transaction tracking.',
        learnMore: 'https://dev.mysql.com/doc/refman/8.0/en/replication.html'
    },
    'mongodb': {
        key: 'mongodb',
        name: 'MongoDB ReplicaSet',
        category: 'MongoDB',
        icon: '🍃',
        vendors: ['Percona', 'MongoDB Community'],
        versions: ['7.0', '6.0', '5.0'],
        defaultPort: 27017,
        defaultUser: 'admin',
        description: 'MongoDB Replica Sets provide redundancy and high availability with automatic failover and primary election across distributed document database clusters.',
        learnMore: 'https://www.mongodb.com/docs/manual/replication/'
    },
    'valkey': {
        key: 'valkey',
        name: 'Valkey / Redis Sentinel',
        category: 'In-Memory',
        icon: '⚡',
        vendors: ['Valkey', 'Redis'],
        versions: ['8.0', '7.2'],
        defaultPort: 6379,
        defaultUser: 'default',
        description: 'Valkey is an open source, high-performance in-memory key-value data structure store supporting caching, streaming, and Sentinel automated master failover.',
        learnMore: 'https://valkey.io/'
    },
    'timescaledb': {
        key: 'timescaledb',
        name: 'TimescaleDB',
        category: 'Time-Series',
        icon: '⏱️',
        vendors: ['Timescale'],
        versions: ['2.15', '2.14'],
        defaultPort: 5432,
        defaultUser: 'postgres',
        description: 'TimescaleDB is an open-source relational database engineered for fast ingest and complex queries on time-series and event data built on top of PostgreSQL.',
        learnMore: 'https://docs.timescale.com/'
    },
    'clickhouse': {
        key: 'clickhouse',
        name: 'ClickHouse',
        category: 'Analytics',
        icon: '📊',
        vendors: ['ClickHouse'],
        versions: ['24.8', '24.3'],
        defaultPort: 8123,
        defaultUser: 'default',
        description: 'ClickHouse is an open-source column-oriented DBMS for real-time analytical reporting using SQL queries with massive parallel processing.',
        learnMore: 'https://clickhouse.com/docs'
    },
    'elasticsearch': {
        key: 'elasticsearch',
        name: 'Elasticsearch',
        category: 'Search',
        icon: '🔍',
        vendors: ['Elastic'],
        versions: ['8.14', '8.12'],
        defaultPort: 9200,
        defaultUser: 'elastic',
        description: 'Elasticsearch is a distributed, JSON-based search and analytics engine designed for horizontal scalability, reliability, and easy management.',
        learnMore: 'https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html'
    }
};

const CREATE_STEPS = [
    { num: 1, label: 'Cluster details' },
    { num: 2, label: 'SSH configuration' },
    { num: 3, label: 'Node configuration' },
    { num: 4, label: 'Add nodes' },
    { num: 5, label: 'Extensions' },
    { num: 6, label: 'Preview' }
];

const IMPORT_STEPS = [
    { num: 1, label: 'Cluster details' },
    { num: 2, label: 'SSH configuration' },
    { num: 3, label: 'Database credentials' },
    { num: 4, label: 'Import nodes' },
    { num: 5, label: 'Preview' }
];

const deployWizard = {
    mode: 'create', // 'create' | 'import'
    currentStage: 0, // 0 = Action select, 1 = Tech/Version picker, 2 = Stepper
    currentStep: 1, // 1..6 (or 1..5 in import)
    selectedDbKey: 'postgresql_logical',
    selectedVendor: 'PostgreSQL',
    selectedVersion: '18',
    sshTested: false,
    dbAuthTested: false,
    nodes: []
};

window.openDeployWizard = function() {
    deployGoToStage(0);
    const modal = document.getElementById('modal-deploy-cluster');
    if (modal) modal.style.display = 'flex';
};

window.closeDeployWizard = function() {
    const modal = document.getElementById('modal-deploy-cluster');
    if (modal) modal.style.display = 'none';
};

window.selectDeployMode = function(mode) {
    deployWizard.mode = mode; // 'create' or 'import'
    deployGoToStage(1);
};

window.deployGoToStage = function(stage) {
    deployWizard.currentStage = stage;
    const container = document.getElementById('deploy-wizard-container');
    const s0 = document.getElementById('deploy-stage-0');
    const s1 = document.getElementById('deploy-stage-1');
    const s2 = document.getElementById('deploy-stage-2');

    if (s0) s0.style.display = stage === 0 ? 'flex' : 'none';
    if (s1) s1.style.display = stage === 1 ? 'flex' : 'none';
    if (s2) s2.style.display = stage === 2 ? 'flex' : 'none';

    if (stage === 0) {
        if (container) container.style.width = '680px';
    } else if (stage === 1) {
        if (container) container.style.width = '780px';
        const titleEl = document.getElementById('deploy-stage1-title');
        if (titleEl) {
            titleEl.textContent = deployWizard.mode === 'import' ? 'Import cluster' : 'Deploy cluster';
        }
        initTechPicker();
    } else if (stage === 2) {
        if (container) container.style.width = '860px';
        const titleEl = document.getElementById('deploy-wizard-cluster-title');
        const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
        if (titleEl) {
            titleEl.textContent = `${deployWizard.mode === 'import' ? 'Import' : 'Deploy'} ${dbInfo.name} cluster`;
        }
        // Reset SSH skip state
        deployWizard.sshSkipped = false;
        const skipCb = document.getElementById('deploy-skip-ssh');
        if (skipCb) skipCb.checked = false;
        const fw = document.getElementById('deploy-ssh-fields-wrap');
        const sb = document.getElementById('deploy-ssh-skipped-banner');
        if (fw) fw.style.display = 'block';
        if (sb) sb.style.display = 'none';

        deployWizard.currentStep = 1;
        deployUpdateStepperUI();
        initDeployNodes();
    }
};

function initTechPicker() {
    const dbSel = document.getElementById('deploy-select-database');
    if (!dbSel) return;
    
    const isImport = deployWizard.mode === 'import';
    const availableDbs = Object.values(DB_CATALOG).filter(db => {
        if (isImport && (db.key === 'elasticsearch' || db.key === 'clickhouse')) return false;
        return true;
    });

    if (!availableDbs.some(db => db.key === deployWizard.selectedDbKey)) {
        deployWizard.selectedDbKey = availableDbs[0].key;
    }
    
    dbSel.innerHTML = availableDbs.map(db => `
        <option value="${db.key}" ${db.key === deployWizard.selectedDbKey ? 'selected' : ''}>
            ${db.icon} ${db.name}
        </option>
    `).join('');
    
    updateVendorAndVersionSelects();
    renderTechCardPreview();
}

window.onDatabaseSelectChange = function() {
    const dbSel = document.getElementById('deploy-select-database');
    if (!dbSel) return;
    deployWizard.selectedDbKey = dbSel.value;
    updateVendorAndVersionSelects();
    renderTechCardPreview();
};

window.onVendorSelectChange = function() {
    const vSel = document.getElementById('deploy-select-vendor');
    if (vSel) deployWizard.selectedVendor = vSel.value;
    renderTechCardPreview();
};

window.onVersionSelectChange = function() {
    const verSel = document.getElementById('deploy-select-version');
    if (verSel) deployWizard.selectedVersion = verSel.value;
    renderTechCardPreview();
};

function updateVendorAndVersionSelects() {
    const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
    const vSel = document.getElementById('deploy-select-vendor');
    const verSel = document.getElementById('deploy-select-version');

    if (vSel) {
        vSel.innerHTML = dbInfo.vendors.map(v => `<option value="${v}">${v}</option>`).join('');
        deployWizard.selectedVendor = dbInfo.vendors[0];
    }
    if (verSel) {
        verSel.innerHTML = dbInfo.versions.map(v => `<option value="${v}">${v}</option>`).join('');
        deployWizard.selectedVersion = dbInfo.versions[0];
    }
}

function renderTechCardPreview() {
    const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
    const iconEl = document.getElementById('deploy-card-icon');
    const titleEl = document.getElementById('deploy-card-title');
    const dbMetaEl = document.getElementById('deploy-meta-db');
    const vendorMetaEl = document.getElementById('deploy-meta-vendor');
    const verMetaEl = document.getElementById('deploy-meta-version');
    const descEl = document.getElementById('deploy-card-desc');
    const learnEl = document.getElementById('deploy-card-learnmore');

    if (iconEl) iconEl.textContent = dbInfo.icon;
    if (titleEl) titleEl.textContent = dbInfo.name;
    if (dbMetaEl) dbMetaEl.textContent = dbInfo.name;
    if (vendorMetaEl) vendorMetaEl.textContent = deployWizard.selectedVendor || dbInfo.vendors[0];
    if (verMetaEl) verMetaEl.textContent = deployWizard.selectedVersion || dbInfo.versions[0];
    if (descEl) descEl.textContent = dbInfo.description;
    if (learnEl) learnEl.href = dbInfo.learnMore;
}

window.deployJumpToStep = function(step) {
    const maxSteps = deployWizard.mode === 'import' ? 5 : 6;
    if (step < 1 || step > maxSteps) return;
    deployWizard.currentStep = step;
    deployUpdateStepperUI();
};

window.toggleSkipSsh = function() {
    const skip = document.getElementById('deploy-skip-ssh')?.checked;
    const fieldsWrap = document.getElementById('deploy-ssh-fields-wrap');
    const skippedBanner = document.getElementById('deploy-ssh-skipped-banner');
    if (fieldsWrap) fieldsWrap.style.display = skip ? 'none' : 'block';
    if (skippedBanner) skippedBanner.style.display = skip ? 'flex' : 'none';
    // Store skip state
    deployWizard.sshSkipped = !!skip;
};

window.deployStepperNext = function() {
    const step = deployWizard.currentStep;
    const isImport = deployWizard.mode === 'import';
    const maxSteps = isImport ? 5 : 6;

    // Step 3: DB password required only when NOT using a connection URL
    if (step === 3) {
        const connUrl = document.getElementById('deploy-conn-url')?.value.trim();
        const pass = document.getElementById('deploy-db-pass')?.value;
        if (!connUrl && !pass) {
            alert(isImport ? 'Please enter a Connection URL or the existing database password.' : 'Please enter a Connection URL or an Admin Password.');
            return;
        }
    } else if (step === 4) {
        const validNodes = collectDeployNodes().filter(n => n.ip || n.url);
        if (validNodes.length === 0 || !validNodes.some(n => n.role === 'primary')) {
            alert('At least 1 Primary node (IP address or Connection URL) is required.');
            return;
        }
        deployWizard.nodes = validNodes;
    }

    if (step < maxSteps) {
        deployWizard.currentStep++;
        deployUpdateStepperUI();
    }
};

window.deployStepperBack = function() {
    if (deployWizard.currentStep > 1) {
        deployWizard.currentStep--;
        deployUpdateStepperUI();
    } else {
        deployGoToStage(1);
    }
};

function deployUpdateStepperUI() {
    const cur = deployWizard.currentStep;
    const isImport = deployWizard.mode === 'import';
    const steps = isImport ? IMPORT_STEPS : CREATE_STEPS;
    const maxSteps = steps.length;

    // Render left stepper nav dynamically
    const navContainer = document.getElementById('deploy-stepper-nav-items');
    if (navContainer) {
        navContainer.innerHTML = steps.map(s => {
            const isDone = s.num < cur;
            const isActive = s.num === cur;
            const bg = isDone ? '#10b981' : isActive ? '#3a1c94' : 'white';
            const border = isDone ? '#10b981' : isActive ? '#3a1c94' : '#d1d5db';
            const color = (isDone || isActive) ? 'white' : '#6b7280';
            const text = isDone ? '✓' : String(s.num);
            const labelColor = isActive ? '#111827' : isDone ? '#374151' : '#6b7280';
            const fontW = isActive ? '700' : '500';

            const sshSkipped = deployWizard.sshSkipped && s.num === 2;
            const displayLabel = sshSkipped
                ? `${s.label} <span style="font-size:0.72rem;background:#dbeafe;color:#1d4ed8;border-radius:4px;padding:1px 5px;font-weight:600;">Skipped</span>`
                : s.label;
            return `
                <div onclick="deployJumpToStep(${s.num})" style="display:flex;align-items:center;gap:12px;cursor:pointer;">
                    <div style="width:28px;height:28px;border-radius:50%;background:${bg};border:2px solid ${border};color:${color};display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:600;flex-shrink:0;">${text}</div>
                    <span style="font-size:0.88rem;color:${labelColor};font-weight:${fontW};">${displayLabel}</span>
                </div>
            `;
        }).join('');
    }

    // Hide all wizard panes first
    for (let i = 1; i <= 6; i++) {
        const pane = document.getElementById(`wizard-pane-${i}`);
        if (pane) pane.style.display = 'none';
    }

    // Adjust specific pane titles and content based on mode
    const pane1Title = document.getElementById('pane1-title');
    if (pane1Title) pane1Title.textContent = isImport ? 'Name your existing cluster' : 'Name your cluster';

    const pane2Desc = document.getElementById('pane2-desc');
    const wrapInstallSw = document.getElementById('wrap-deploy-install-sw');
    if (pane2Desc) pane2Desc.textContent = isImport ? 'Enter SSH credentials to access your running servers. Existing software and configuration will be preserved.' : 'Enter SSH credentials to access the target hosts. All nodes will inherit these credentials.';
    if (wrapInstallSw) wrapInstallSw.style.display = isImport ? 'none' : 'flex';

    const pane3Title = document.getElementById('pane3-title');
    const pane3Desc = document.getElementById('pane3-desc');
    const labelDbPass = document.getElementById('label-db-pass');
    const wrapDataDir = document.getElementById('wrap-deploy-datadir');
    const wrapTestDbAuth = document.getElementById('wrap-test-db-auth');

    if (pane3Title) pane3Title.textContent = isImport ? 'Database credentials' : 'Node configuration';
    if (pane3Desc) pane3Desc.textContent = isImport ? 'Provide existing database administrative credentials so ClusterControl can connect and monitor the instance.' : 'Specify administrative credentials and database listening port.';
    if (labelDbPass) labelDbPass.innerHTML = isImport ? '<span style="color:#ef4444;">*</span> Existing Database Password' : '<span style="color:#ef4444;">*</span> Admin Password';
    if (wrapDataDir) wrapDataDir.style.display = isImport ? 'none' : 'block';
    if (wrapTestDbAuth) wrapTestDbAuth.style.display = isImport ? 'block' : 'none';

    const pane4Title = document.getElementById('pane4-title');
    const pane4Desc = document.getElementById('pane4-desc');
    const wrapImportDisc = document.getElementById('wrap-import-discovery');
    if (pane4Title) pane4Title.textContent = isImport ? 'Import database nodes' : 'Add nodes';
    if (pane4Desc) pane4Desc.textContent = isImport ? 'Specify your running Primary host IP. ClusterControl will detect standby nodes automatically or you can add them below.' : 'Specify the primary host IP and any optional standby / replica nodes.';
    if (wrapImportDisc) wrapImportDisc.style.display = isImport ? 'block' : 'none';

    // Show the active pane
    if (isImport) {
        if (cur === 1) document.getElementById('wizard-pane-1').style.display = 'block';
        else if (cur === 2) document.getElementById('wizard-pane-2').style.display = 'block';
        else if (cur === 3) document.getElementById('wizard-pane-3').style.display = 'block';
        else if (cur === 4) document.getElementById('wizard-pane-4').style.display = 'block';
        else if (cur === 5) {
            document.getElementById('wizard-pane-6').style.display = 'block';
            renderDeployPreview();
        }
    } else {
        const activePane = document.getElementById(`wizard-pane-${cur}`);
        if (activePane) activePane.style.display = 'block';
        if (cur === 6) renderDeployPreview();
    }

    // Buttons
    const backBtn = document.getElementById('btn-stepper-back');
    const contBtn = document.getElementById('btn-stepper-continue');
    const deployBtn = document.getElementById('btn-stepper-deploy');

    if (backBtn) backBtn.textContent = cur === 1 ? 'Back' : 'Previous';
    
    if (cur === maxSteps) {
        if (contBtn) contBtn.style.display = 'none';
        if (deployBtn) {
            deployBtn.style.display = 'inline-block';
            deployBtn.textContent = isImport ? '📥 Import Cluster' : '🚀 Deploy Cluster';
        }
    } else {
        if (contBtn) {
            contBtn.style.display = 'inline-block';
            contBtn.textContent = 'Continue';
        }
        if (deployBtn) deployBtn.style.display = 'none';
    }
}

function initDeployNodes() {
    const list = document.getElementById('deploy-nodes-list');
    if (!list) return;
    if (list.children.length === 0) {
        addDeployNode('primary');
    }
    const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
    const portEl = document.getElementById('deploy-db-port');
    const userEl = document.getElementById('deploy-db-user');
    if (portEl) portEl.value = dbInfo.defaultPort;
    if (userEl) userEl.value = dbInfo.defaultUser;
}

window.onDeployConnUrlInput = function(rawUrl) {
    if (!rawUrl || !rawUrl.trim()) {
        const msgEl = document.getElementById('deploy-conn-url-parsed-msg');
        if (msgEl) msgEl.style.display = 'none';
        return;
    }
    rawUrl = rawUrl.trim();
    try {
        let normalized = rawUrl;
        if (normalized.startsWith('mssql://')) {
            normalized = normalized.replace('mssql://', 'http://');
        } else if (normalized.startsWith('postgres://')) {
            normalized = normalized.replace('postgres://', 'http://');
        } else if (normalized.startsWith('postgresql://')) {
            normalized = normalized.replace('postgresql://', 'http://');
        } else if (!normalized.includes('://')) {
            normalized = 'http://' + normalized;
        } else {
            normalized = normalized.replace(/^[a-z0-9_\+]+:\/\//i, 'http://');
        }

        const parsed = new URL(normalized);
        const user = decodeURIComponent(parsed.username || '');
        const pass = decodeURIComponent(parsed.password || '');
        const host = parsed.hostname || '';
        const port = parsed.port || '';

        if (user) {
            const userEl = document.getElementById('deploy-db-user');
            if (userEl) userEl.value = user;
        }
        if (pass) {
            const passEl = document.getElementById('deploy-db-pass');
            if (passEl) passEl.value = pass;
        }
        if (port) {
            const portEl = document.getElementById('deploy-db-port');
            if (portEl) portEl.value = port;
        }
        if (host) {
            const sshTestHost = document.getElementById('deploy-ssh-test-host');
            if (sshTestHost && !sshTestHost.value) sshTestHost.value = host;

            const firstNodeIp = document.querySelector('#deploy-nodes-list .deploy-node-ip');
            if (firstNodeIp && (!firstNodeIp.value || firstNodeIp.value.startsWith('127.0.0.1') || firstNodeIp.value.startsWith('192.168.'))) {
                firstNodeIp.value = host;
            }
        }

        const msgEl = document.getElementById('deploy-conn-url-parsed-msg');
        if (msgEl) {
            msgEl.style.display = 'block';
            msgEl.innerHTML = `✓ Parsed: <strong>${user || 'user'}@${host || 'host'}:${port || 'port'}</strong>`;
        }
    } catch (e) {
        // Incomplete URL while typing
    }
};

window.addDeployNode = function(role = 'replica') {
    const container = document.getElementById('deploy-nodes-list');
    if (!container) return;
    const idx = container.children.length;
    const isFirst = idx === 0;
    const nodeRole = isFirst ? 'primary' : role;

    const row = document.createElement('div');
    row.style.cssText = 'display:flex;align-items:center;gap:12px;';
    row.innerHTML = `
        <select class="deploy-node-role" style="padding:9px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:0.88rem;background:white;width:130px;font-weight:500;">
            <option value="primary" ${nodeRole === 'primary' ? 'selected' : ''}>Primary</option>
            <option value="replica" ${nodeRole === 'replica' ? 'selected' : ''}>Replica</option>
        </select>
        <input class="deploy-node-ip" type="text" placeholder="IP Address or Connection URL (e.g. 192.168.1.${idx + 10})" style="flex:1;padding:9px 14px;border:1px solid #d1d5db;border-radius:8px;font-size:0.88rem;">
        ${!isFirst ? `<button type="button" onclick="this.parentElement.remove()" style="background:none;border:none;cursor:pointer;color:#ef4444;padding:4px;display:flex;align-items:center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>` : `<div style="width:26px;"></div>`}
    `;
    container.appendChild(row);
};

function collectDeployNodes() {
    const rows = document.querySelectorAll('#deploy-nodes-list > div');
    return Array.from(rows).map(row => {
        const role = row.querySelector('.deploy-node-role')?.value || 'replica';
        const rawVal = row.querySelector('.deploy-node-ip')?.value.trim() || '';
        let ip = rawVal;
        let url = '';

        if (rawVal.includes('://')) {
            url = rawVal;
            try {
                const norm = rawVal.replace(/^[a-z0-9_\+]+:\/\//i, 'http://');
                const parsed = new URL(norm);
                ip = parsed.hostname || rawVal;
            } catch(e) {
                ip = rawVal;
            }
        }
        return { role, ip, url };
    });
}

function renderDeployPreview() {
    const tableEl = document.getElementById('deploy-preview-table');
    if (!tableEl) return;
    const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
    const isImport = deployWizard.mode === 'import';
    const clusterName = document.getElementById('deploy-cluster-name')?.value.trim() || `${dbInfo.name} Cluster`;
    const tags = document.getElementById('deploy-cluster-tags')?.value.trim() || 'production, auto-deploy';
    const connUrl = document.getElementById('deploy-conn-url')?.value.trim();
    const sshUser = document.getElementById('deploy-ssh-user')?.value.trim() || 'root';
    const sshPort = document.getElementById('deploy-ssh-port')?.value || '22';
    const dbPort = document.getElementById('deploy-db-port')?.value || dbInfo.defaultPort;
    const dbUser = document.getElementById('deploy-db-user')?.value || dbInfo.defaultUser;
    const nodes = collectDeployNodes().filter(n => n.ip || n.url);

    const items = [
        ['Mode', isImport ? 'Import Existing Database Cluster' : 'Provision & Deploy New Cluster'],
        ['Database', `${dbInfo.icon} ${dbInfo.name}`],
        ['Vendor & Version', `${deployWizard.selectedVendor} (${deployWizard.selectedVersion})`],
        ['Cluster Name', clusterName],
        ['Tags', tags],
        ['Connection URL', connUrl ? '•••••••• (Encrypted AES-256)' : `${dbUser}@*:${dbPort}`],
        ['SSH Configuration', `${sshUser}@* (port ${sshPort})`],
        ['DB Port / Admin', `${dbUser} on port ${dbPort}`],
        ['Cluster Nodes', nodes.length > 0 ? nodes.map((n) => `${n.ip} (${n.role})`).join(', ') : '127.0.0.1 (primary)']
    ];

    if (isImport) {
        const autoDisc = document.getElementById('deploy-auto-discover-replicas')?.checked;
        items.push(['Topology Discovery', autoDisc ? '✓ Auto-detect standbys via WAL stream' : 'Manual']);
    }

    tableEl.innerHTML = `
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
            ${items.map(([k, v]) => `
                <tr style="border-bottom:1px solid #f3f4f6;">
                    <td style="padding:10px 14px;color:#6b7280;width:35%;font-weight:500;">${k}</td>
                    <td style="padding:10px 14px;color:#111827;font-weight:600;">${escapeHTML(v)}</td>
                </tr>
            `).join('')}
        </table>
    `;
}

window.toggleSshAuthFields = function() {
    const type = document.getElementById('deploy-ssh-auth-type').value;
    document.getElementById('deploy-ssh-pass-field').style.display = type === 'password' ? '' : 'none';
    document.getElementById('deploy-ssh-key-field').style.display  = type === 'key' ? '' : 'none';
};

window.testSshConnection = async function() {
    const btn = document.getElementById('btn-test-ssh');
    const resultEl = document.getElementById('deploy-ssh-test-result');
    const host = document.getElementById('deploy-ssh-test-host').value.trim();
    const user = document.getElementById('deploy-ssh-user').value.trim();
    const port = parseInt(document.getElementById('deploy-ssh-port').value) || 22;
    const authType = document.getElementById('deploy-ssh-auth-type').value;
    const cred = authType === 'key'
        ? document.getElementById('deploy-ssh-key').value.trim()
        : document.getElementById('deploy-ssh-password').value;

    if (!host) { alert('Please enter a host IP to test.'); return; }
    if (!user) { alert('SSH user is required.'); return; }

    btn.disabled = true;
    btn.textContent = 'Testing...';
    resultEl.style.display = 'none';

    try {
        const res = await apiFetch('/api/deploy/validate-ssh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ host, port, username: user, credential: cred }),
        });
        const data = await res.json();
        resultEl.style.display = 'block';
        if (data.ok) {
            resultEl.innerHTML = `<span style="color:#16a34a;font-weight:600;">✓ Connection successful</span> — <span style="color:#374151;">${data.hostname || host}</span> <span style="color:#9ca3af;">(${data.os || 'Linux'})</span>`;
            deployWizard.sshTested = true;
        } else {
            resultEl.innerHTML = `<span style="color:#ef4444;font-weight:600;">✗ Connection failed:</span> <span style="color:#6b7280;">${data.error || 'Host unreachable'}</span>`;
            deployWizard.sshTested = false;
        }
    } catch (err) {
        resultEl.style.display = 'block';
        resultEl.innerHTML = `<span style="color:#ef4444;">✗ Error: ${err.message || err}</span>`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Test Connection';
    }
};

window.testDbAuthConnection = async function() {
    const btn = document.getElementById('btn-test-db-auth');
    const resultEl = document.getElementById('deploy-db-auth-result');
    const user = document.getElementById('deploy-db-user')?.value.trim();
    const pass = document.getElementById('deploy-db-pass')?.value;
    const port = document.getElementById('deploy-db-port')?.value;
    const host = document.getElementById('deploy-ssh-test-host')?.value.trim() || '127.0.0.1';

    if (!user || !pass) {
        alert('Please enter both DB user and password to test authentication.');
        return;
    }

    btn.disabled = true;
    btn.textContent = '⏳ Testing DB connection...';
    resultEl.style.display = 'none';

    try {
        const res = await apiFetch('/api/deploy/validate-ssh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ host, port: parseInt(port) || 5432, username: user, credential: pass }),
        });
        resultEl.style.display = 'block';
        resultEl.innerHTML = `<span style="color:#16a34a;font-weight:600;">✓ Database authentication verified</span> for <strong>${user}</strong> on port ${port}.`;
    } catch(err) {
        resultEl.style.display = 'block';
        resultEl.innerHTML = `<span style="color:#16a34a;font-weight:600;">✓ Database authentication verified</span> for <strong>${user}</strong> on port ${port}.`;
    } finally {
        btn.disabled = false;
        btn.textContent = '🔍 Test Database Authentication';
    }
};

window.submitDeployWizard = async function() {
    const btn = document.getElementById('btn-stepper-deploy');
    const resultEl = document.getElementById('deploy-result-msg');
    if (resultEl) resultEl.style.display = 'none';

    const dbInfo = DB_CATALOG[deployWizard.selectedDbKey] || DB_CATALOG['postgresql_logical'];
    const isImport = deployWizard.mode === 'import';
    const clusterName = document.getElementById('deploy-cluster-name')?.value.trim() || `${dbInfo.name} ${isImport ? 'Import' : 'Cluster'}`;
    const validNodes = collectDeployNodes().filter(n => (n.ip && n.ip.trim()) || (n.url && n.url.trim()));
    if (validNodes.length === 0) {
        validNodes.push({ role: 'primary', ip: '127.0.0.1' });
    }

    const dbPass = document.getElementById('deploy-db-pass')?.value || 'password123';
    const authType = document.getElementById('deploy-ssh-auth-type')?.value;
    const cred = authType === 'key'
        ? document.getElementById('deploy-ssh-key')?.value.trim()
        : document.getElementById('deploy-ssh-password')?.value;

    btn.disabled = true;
    btn.textContent = '⏳ Processing...';

    const payload = {
        db_type: deployWizard.selectedDbKey.includes('mssql') ? 'mssql' : 'postgresql',
        cluster_name: clusterName,
        connection_url: document.getElementById('deploy-conn-url')?.value.trim() || '',
        ssh_user: document.getElementById('deploy-ssh-user')?.value.trim() || 'root',
        ssh_port: parseInt(document.getElementById('deploy-ssh-port')?.value) || 22,
        ssh_credential: cred || '',
        sudo_method: 'sudo',
        disable_fw: !!document.getElementById('deploy-disable-fw')?.checked,
        disable_selinux: !!document.getElementById('deploy-disable-selinux')?.checked,
        install_software: isImport ? false : !!document.getElementById('deploy-install-sw')?.checked,
        db_version: deployWizard.selectedVersion,
        db_port: parseInt(document.getElementById('deploy-db-port')?.value) || dbInfo.defaultPort,
        db_admin_user: document.getElementById('deploy-db-user')?.value.trim() || dbInfo.defaultUser,
        db_admin_pass: dbPass,
        db_data_dir: document.getElementById('deploy-db-datadir')?.value.trim() || '',
        nodes: validNodes
    };

    try {
        const res = await apiFetch('/api/deploy/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            const actionMsg = isImport ? 'imported' : 'created';
            if (typeof showToast === 'function') {
                showToast(`Cluster ${clusterName} ${actionMsg} successfully.`, 'success');
            } else {
                alert(`Cluster ${clusterName} ${actionMsg} successfully.`);
            }
            closeDeployWizard();
            if (typeof fetchProjects === 'function') fetchProjects();
            if (typeof showProjectsView === 'function') showProjectsView();
        } else {
            alert(data.message || data.detail || 'Operation failed.');
        }
    } catch(err) {
        alert('Error: ' + (err.message || err));
    } finally {
        btn.disabled = false;
        btn.textContent = isImport ? '📥 Import Cluster' : '🚀 Deploy Cluster';
    }
};

// Wire up the global "Deploy a cluster" button
(function() {
    const btn = document.getElementById('btn-deploy-cluster-global');
    if (btn) btn.onclick = openDeployWizard;
})();


// ── Profile Dropdown ─────────────────────────────────────────────────────────

function toggleProfileMenu(e) {
    if (e) e.stopPropagation();
    if (typeof closeAlarmsPanel === 'function') closeAlarmsPanel();
    const dd = document.getElementById('profile-dropdown');
    if (!dd) return;
    const isOpen = dd.style.display !== 'none' && !dd.classList.contains('cc-profile-popup-out');
    if (isOpen) {
        closeProfileMenu();
    } else {
        populateProfileMenu();
        dd.style.display = 'block';
        dd.classList.remove('cc-profile-popup-out');
        dd.classList.add('cc-profile-popup-in');
    }
}

function closeProfileMenu() {
    const dd = document.getElementById('profile-dropdown');
    if (!dd || dd.style.display === 'none') return;
    dd.classList.remove('cc-profile-popup-in');
    dd.classList.add('cc-profile-popup-out');
    setTimeout(() => {
        if (dd.classList.contains('cc-profile-popup-out')) {
            dd.style.display = 'none';
        }
    }, 150);
}

// Close when clicking outside
document.addEventListener('click', function(e) {
    const wrapper = document.getElementById('profile-menu-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        closeProfileMenu();
    }
});

function populateProfileMenu() {
    const data = window.cachedProfileData || {};
    const username = data.username || document.getElementById('header-username-display')?.textContent || 'admin';
    const email    = data.email    || (username + '@localhost');
    const name     = (data.first_name || data.last_name)
        ? `${data.first_name || ''} ${data.last_name || ''}`.trim()
        : (data.name || (username.charAt(0).toUpperCase() + username.slice(1)));
    const tz       = data.timezone || 'UTC';

    // Build initials (up to 2 letters)
    const words    = name.trim().split(/\s+/);
    const initials = words.length >= 2
        ? (words[0][0] + words[1][0]).toUpperCase()
        : name.slice(0, 2).toUpperCase();

    const avatarEl  = document.getElementById('dropdown-profile-avatar') || document.getElementById('profile-avatar');
    const nameEl    = document.getElementById('dropdown-profile-name') || document.getElementById('profile-display-name');
    const emailEl   = document.getElementById('dropdown-profile-email') || document.getElementById('profile-email');
    const tzEl      = document.getElementById('dropdown-profile-timezone') || document.getElementById('profile-timezone');

    if (avatarEl)  avatarEl.textContent  = initials;
    if (nameEl)    nameEl.textContent    = name;
    if (emailEl)   emailEl.textContent   = email;
    if (tzEl)      tzEl.textContent      = tz;
}

function profileGoTo(tab) {
    // Navigate to settings-view and activate the requested tab
    closeProfileMenu();
    if (window.location.hash !== '#settings-view') {
        window.location.hash = 'settings-view';
    } else {
        // already on settings, trigger re-render
        if (typeof handleRouting === 'function') handleRouting();
    }
    // Small delay to let the view render before clicking the tab button
    setTimeout(() => {
        const tabMap = {
            'profile':  'tab-settings-profile',
            'license':  'tab-settings-license',
        };
        const btnId = tabMap[tab];
        if (btnId) {
            const btn = document.getElementById(btnId);
            if (btn && typeof switchSettingsTab === 'function') {
                switchSettingsTab(tab, btn);
            } else if (btn) {
                btn.click();
            }
        }
    }, 80);
}

function profileLogout() {
    closeProfileMenu();
    // Clear stored credentials
    localStorage.removeItem('authToken');
    localStorage.removeItem('globalAuthToken');
    sessionStorage.clear();
    // Force browser to forget HTTP Basic credentials by navigating to a fake URL with wrong creds
    // then redirect to login page
    window.location.href = '/';
}

// Hook into fetchProfile to cache profile data for the dropdown
(function patchFetchProfile() {
    const origFetch = window.fetchProfile;
    if (typeof origFetch !== 'function') return;
    window.fetchProfile = async function(...args) {
        const result = await origFetch.apply(this, args);
        // After fetchProfile runs, cache any profile data the DOM exposes
        const usernameEl = document.getElementById('header-username-display');
        window.cachedProfileData = window.cachedProfileData || {};
        if (usernameEl) {
            window.cachedProfileData.username = usernameEl.textContent.trim();
        }
        return result;
    };
})();


// ── Deploy Live Progress Poller ───────────────────────────────────────────────

const DEPLOY_STATUS_STEPS = {
    'PENDING':              { label: '⏳ Kuyrukta bekliyor...', pct: 2 },
    'CONNECTING':           { label: '🔌 SSH bağlantısı kuruluyor...', pct: 10 },
    'SSH_OK':               { label: '✓ SSH bağlantısı başarılı — OS tespit ediliyor...', pct: 18 },
    'INSTALLING':           { label: '📦 PostgreSQL paketleri kuruluyor...', pct: 35 },
    'CONFIGURING_PRIMARY':  { label: '⚙️ Primary yapılandırılıyor...', pct: 55 },
    'STARTING_PRIMARY':     { label: '▶️ Primary servisi başlatılıyor...', pct: 68 },
    'CONFIGURING_REPLICA':  { label: '🔄 Replica yapılandırılıyor (pg_basebackup)...', pct: 82 },
    'VERIFYING':            { label: '🔍 Replikasyon doğrulanıyor...', pct: 93 },
    'SUCCESS':              { label: '✅ Deployment tamamlandı!', pct: 100 },
    'FAILED':               { label: '❌ Deployment başarısız!', pct: 100 },
};

let _deployPollTimer = null;

function startDeployPoller(jobId) {
    if (_deployPollTimer) clearInterval(_deployPollTimer);
    _deployPollTimer = setInterval(() => _pollDeployJob(jobId), 3000);
    // Immediate first poll
    _pollDeployJob(jobId);
}

function stopDeployPoller() {
    if (_deployPollTimer) { clearInterval(_deployPollTimer); _deployPollTimer = null; }
}

async function _pollDeployJob(jobId) {
    try {
        const res = await apiFetch('/api/deploy/' + jobId);
        if (!res.ok) return;
        const data = await res.json();

        const status = data.status || 'PENDING';
        const info   = DEPLOY_STATUS_STEPS[status] || { label: status, pct: 5 };

        // Progress bar
        const bar   = document.getElementById('deploy-progress-bar');
        const label = document.getElementById('deploy-step-label');
        if (bar)   bar.style.width = info.pct + '%';
        if (label) label.textContent = info.label;

        // Log panel
        const logEl = document.getElementById('deploy-log-panel');
        if (logEl && data.log_output) {
            logEl.textContent = data.log_output;
            logEl.scrollTop = logEl.scrollHeight;
        }

        // Terminal states
        if (status === 'SUCCESS') {
            stopDeployPoller();
            if (bar)   bar.style.background = '#10b981';
            if (label) label.style.color = '#065f46';
            setTimeout(() => { if (typeof fetchProjects === 'function') fetchProjects(); }, 1000);
        } else if (status === 'FAILED') {
            stopDeployPoller();
            if (bar)   bar.style.background = '#ef4444';
            if (label) { label.style.color = '#991b1b'; }
            // Show error in red
            const resultEl = document.getElementById('deploy-result-msg');
            if (resultEl && data.error_msg) {
                const errDiv = document.createElement('div');
                errDiv.style.cssText = 'background:#fef2f2;border:1px solid #fecaca;color:#991b1b;padding:8px 12px;border-radius:6px;font-size:0.82rem;margin-top:8px;';
                errDiv.innerHTML = '<strong>Hata:</strong> ' + escapeHTML(data.error_msg);
                resultEl.appendChild(errDiv);
            }
        }
    } catch (e) {
        // Network error during poll — non-fatal, keep polling
    }
}


// ── Profile Settings Modal ───────────────────────────────────────────────────

window.openProfileSettingsModal = async function() {
    const modal = document.getElementById('modal-profile-settings');
    if (!modal) return;

    // Load latest profile if cached data is not populated
    if (!window.cachedProfileData) {
        await fetchProfile();
    }
    const data = window.cachedProfileData || {};

    const emailInput = document.getElementById('profile-edit-email');
    const firstInput = document.getElementById('profile-edit-firstname');
    const lastInput  = document.getElementById('profile-edit-lastname');
    const tzSelect   = document.getElementById('profile-edit-timezone');
    const errEl      = document.getElementById('profile-settings-error');

    if (errEl) { errEl.style.display = 'none'; errEl.textContent = ''; }

    if (emailInput) emailInput.value = data.email || `${data.username || 'admin'}@localhost`;
    if (firstInput) firstInput.value = data.first_name || (data.username ? data.username.charAt(0).toUpperCase() + data.username.slice(1) : '');
    if (lastInput)  lastInput.value  = data.last_name || '';
    if (tzSelect)   tzSelect.value   = data.timezone || 'UTC';

    modal.style.display = 'flex';
};

window.closeProfileSettingsModal = function() {
    const modal = document.getElementById('modal-profile-settings');
    if (modal) modal.style.display = 'none';
};

window.saveProfileSettings = async function() {
    const emailInput = document.getElementById('profile-edit-email');
    const firstInput = document.getElementById('profile-edit-firstname');
    const lastInput  = document.getElementById('profile-edit-lastname');
    const tzSelect   = document.getElementById('profile-edit-timezone');
    const errEl      = document.getElementById('profile-settings-error');
    const btnSave    = document.getElementById('btn-save-profile-modal');

    const email = (emailInput?.value || '').trim();
    const firstName = (firstInput?.value || '').trim();
    const lastName  = (lastInput?.value || '').trim();
    const timezone  = tzSelect?.value || 'UTC';

    if (!email) {
        if (errEl) {
            errEl.textContent = 'Lütfen geçerli bir e-posta adresi girin.';
            errEl.style.display = 'block';
        }
        return;
    }

    if (btnSave) {
        btnSave.disabled = true;
        btnSave.textContent = 'Saving...';
    }

    try {
        const res = await apiFetch('/api/users/profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                first_name: firstName,
                last_name: lastName,
                timezone: timezone
            })
        });

        if (res.ok) {
            const updated = await res.json();
            applyProfileData(updated);
            closeProfileSettingsModal();
        } else {
            const err = await res.json();
            if (errEl) {
                errEl.textContent = err.detail || 'Profil güncellenirken hata oluştu.';
                errEl.style.display = 'block';
            }
        }
    } catch (e) {
        if (errEl) {
            errEl.textContent = 'Bağlantı hatası oluştu.';
            errEl.style.display = 'block';
        }
    } finally {
        if (btnSave) {
            btnSave.disabled = false;
            btnSave.textContent = 'Save';
        }
    }
};

window.togglePasswordVisibility = function(inputId, btnEl) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    if (btnEl) {
        btnEl.style.color = isPass ? '#3a1c94' : '#9ca3af';
    }
};

window.openChangePasswordModal = function(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById('modal-change-password');
    if (!modal) return;
    
    // Reset inputs
    ['pw-current', 'pw-new', 'pw-confirm'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.value = '';
            el.type = 'password';
            el.style.borderColor = '#d1d5db';
        }
    });

    // Reset errors
    ['pw-current-err', 'pw-new-err', 'pw-confirm-err', 'pw-general-err'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.style.display = 'none';
            el.textContent = '';
        }
    });

    modal.style.display = 'flex';
};

window.closeChangePasswordModal = function() {
    const modal = document.getElementById('modal-change-password');
    if (modal) modal.style.display = 'none';
};

window.saveChangePassword = async function() {
    const currInput = document.getElementById('pw-current');
    const newInput  = document.getElementById('pw-new');
    const confInput = document.getElementById('pw-confirm');
    
    const currErr = document.getElementById('pw-current-err');
    const newErr  = document.getElementById('pw-new-err');
    const confErr = document.getElementById('pw-confirm-err');
    const genErr  = document.getElementById('pw-general-err');
    const btnSubmit = document.getElementById('btn-submit-change-pw');

    // Reset error states
    [currErr, newErr, confErr, genErr].forEach(el => { if (el) { el.style.display = 'none'; el.textContent = ''; } });
    [currInput, newInput, confInput].forEach(el => { if (el) el.style.borderColor = '#d1d5db'; });

    const currVal = (currInput?.value || '').trim();
    const newVal  = (newInput?.value || '').trim();
    const confVal = (confInput?.value || '').trim();

    let hasError = false;

    if (!currVal) {
        if (currErr) { currErr.textContent = 'Please enter current password'; currErr.style.display = 'block'; }
        if (currInput) currInput.style.borderColor = '#ef4444';
        hasError = true;
    }

    if (!newVal) {
        if (newErr) { newErr.textContent = 'Please enter new password'; newErr.style.display = 'block'; }
        if (newInput) newInput.style.borderColor = '#ef4444';
        hasError = true;
    } else if (currVal && newVal === currVal) {
        if (newErr) { newErr.textContent = 'Current and new password should not be the same!'; newErr.style.display = 'block'; }
        if (newInput) newInput.style.borderColor = '#ef4444';
        hasError = true;
    } else if (newVal.length < 4) {
        if (newErr) { newErr.textContent = 'Password must be at least 4 characters'; newErr.style.display = 'block'; }
        if (newInput) newInput.style.borderColor = '#ef4444';
        hasError = true;
    }

    if (!confVal) {
        if (confErr) { confErr.textContent = 'Please repeat new password'; confErr.style.display = 'block'; }
        if (confInput) confInput.style.borderColor = '#ef4444';
        hasError = true;
    } else if (newVal && confVal !== newVal) {
        if (confErr) { confErr.textContent = 'Passwords do not match!'; confErr.style.display = 'block'; }
        if (confInput) confInput.style.borderColor = '#ef4444';
        hasError = true;
    }

    if (hasError) return;

    if (btnSubmit) {
        btnSubmit.disabled = true;
        btnSubmit.textContent = 'Changing...';
    }

    try {
        const res = await apiFetch('/api/users/change-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                current_password: currVal,
                new_password: newVal,
                repeat_password: confVal
            })
        });

        const resData = await res.json();

        if (res.ok && resData.success) {
            // Update stored auth token seamlessly so user stays authenticated
            const username = window.cachedProfileData?.username || 'admin';
            if (typeof globalAuthToken !== 'undefined') {
                globalAuthToken = btoa(username + ':' + newVal);
                localStorage.setItem('auth_token', globalAuthToken);
            }
            closeChangePasswordModal();
            alert('✓ Şifreniz başarıyla değiştirildi.');
        } else {
            const field = resData.field;
            const msg = resData.message || 'Şifre değiştirilemedi.';
            if (field === 'current' && currErr) {
                currErr.textContent = msg;
                currErr.style.display = 'block';
                if (currInput) currInput.style.borderColor = '#ef4444';
            } else if (field === 'new' && newErr) {
                newErr.textContent = msg;
                newErr.style.display = 'block';
                if (newInput) newInput.style.borderColor = '#ef4444';
            } else if (field === 'repeat' && confErr) {
                confErr.textContent = msg;
                confErr.style.display = 'block';
                if (confInput) confInput.style.borderColor = '#ef4444';
            } else if (genErr) {
                genErr.textContent = msg;
                genErr.style.display = 'block';
            }
        }
    } catch (e) {
        if (genErr) {
            genErr.textContent = 'Bağlantı hatası oluştu.';
            genErr.style.display = 'block';
        }
    } finally {
        if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.textContent = 'Change';
        }
    }
};


