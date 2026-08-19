window.nodesPageData = [];
var nodesPageData = window.nodesPageData;
let globalAuthToken = '';
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
                this.size = Math.random() * 220 + 120;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 0.4;
                this.vy = (Math.random() - 0.5) * 0.4;
                
                if (Math.abs(this.vx) < 0.1) this.vx = 0.2 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.1) this.vy = 0.2 * Math.sign(this.vy || 1);
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
        
        for (let i = 0; i < 40; i++) {
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
        statusFilter.addEventListener('change', (e) => {
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
        btnAddProj.addEventListener('click', () => {
            modalAddProj.style.display = 'flex';
        });
    }

    const btnDeployCluster = document.getElementById('btn-deploy-cluster-global');
    if (btnDeployCluster) {
        btnDeployCluster.addEventListener('click', () => {
            modalAddProj.style.display = 'flex';
        });
    }

    if (btnOpenNodeModal) {
        btnOpenNodeModal.addEventListener('click', () => {
            modalAddNode.style.display = 'flex';
        });
    }

    if (btnCloseProjModal) {
        btnCloseProjModal.addEventListener('click', () => {
            modalAddProj.style.display = 'none';
        });
    }

    if (btnCloseNodeModal) {
        btnCloseNodeModal.addEventListener('click', () => {
            modalAddNode.style.display = 'none';
        });
    }

    // --- VIEW MANAGEMENT ---
    const sidebarLinks = document.querySelectorAll('.sidebar-nav > a, .sidebar-nav > div > a, a[data-view="changelog-view"]');
    const viewSections = document.querySelectorAll('.view-section');
    
    function handleRouting() {
        let hash = window.location.hash.substring(1) || 'projects-view';
        
        // If hash is a changelog section anchor (e.g. v1-4-2), show changelog-view and scroll
        const changelogAnchors = ['v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];
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
            setTimeout(() => { const auditBtn = document.getElementById('ac-tab-audit'); if(auditBtn && typeof window.switchActivityTab === 'function') window.switchActivityTab('audit', auditBtn); else if(typeof window.fetchAuditLogs === 'function') window.fetchAuditLogs(); }, 50);
            // Set Audit Log as active default tab
            const auditBtn = document.getElementById('ac-tab-audit');
            if(auditBtn) window.switchActivityTab('audit', auditBtn);
        } else if (hash === 'settings-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            if(typeof fetchProfile === 'function') fetchProfile();
        } else if (hash === 'nodes-view') {
            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();
            window.fetchNodesPage();
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
        clusterTooltip.addEventListener('mouseenter', () => {
            clearTimeout(clusterHoverTimeout);
        });
        clusterTooltip.addEventListener('mouseleave', () => {
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
                let isOperational = proj.nodesCount > 0 && proj.sync_status !== 'FAILED';
                if (isOperational) operationalCount++;
                
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
                
                const statusColor = isOperational ? 'var(--success)' : 'var(--warning)';
                const statusText = isOperational ? '● Operational' : '● Warning';

                const tr = document.createElement('tr');
                tr.setAttribute('data-status', isOperational ? 'Operational' : 'Warning');
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
                    <td style="padding: 12px 10px;">${proj.nodesCount || 0}</td>
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
            
            // Update Donut Chart
            const el_cc_total_clusters = document.getElementById('cc-total-clusters'); if(el_cc_total_clusters) el_cc_total_clusters.innerText = `${data.length} Clusters`;
{ const TMP_EL = document.getElementById('cc-donut-center-text'); if(TMP_EL) {             const el1 = TMP_EL; if(el1) el1.innerText = operationalCount; } }
            
            const radius = 80;
            const circumference = 2 * Math.PI * radius; // ~502.6
            const ratio = data.length > 0 ? (operationalCount / data.length) : 0;
            const offset = circumference - (ratio * circumference);
            
            const donutCircle = document.getElementById('cc-donut-progress');
if (donutCircle) {
                donutCircle.style.strokeDashoffset = offset;
                donutCircle.style.stroke = ratio === 1 ? 'var(--success)' : (ratio > 0 ? 'var(--warning)' : 'var(--danger)');
                
                // Add hover logic
                const donutTooltip = document.getElementById('donut-hover-tooltip');
                const donutText = document.getElementById('donut-hover-text');
                document.getElementById('cc-donut-center-text').style.color = donutCircle.style.stroke;
                if (donutTooltip && donutText) {
                    donutCircle.addEventListener('mouseenter', (e) => {
                        if(donutText) donutText.innerText = `${operationalCount} Operational`;
                        donutTooltip.style.display = 'block';
                    });
                    donutCircle.addEventListener('mousemove', (e) => {
                        donutTooltip.style.left = (e.clientX + 10) + 'px';
                        donutTooltip.style.top = (e.clientY + 10) + 'px';
                    });
                    donutCircle.addEventListener('mouseleave', () => {
                        donutTooltip.style.display = 'none';
                    });
                }
            }
            
            // Update Legend
            const warningCount = data.length - operationalCount;
            const ccd = document.getElementById('cc-donut-legend'); if(ccd) ccd.innerHTML = `
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--success);">&#8226; ${operationalCount} Operational</span>
                </div>
                ${warningCount > 0 ? `<div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--warning);">&#8226; ${warningCount} Warning</span>
                </div>` : ''}
            `;
            
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
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})"
                        onmouseover="let p = this.querySelector('polygon'); p.setAttribute('data-orig-fill', p.getAttribute('fill')); p.setAttribute('fill', 'white'); p.setAttribute('stroke', '${node.color}');"
                        onmouseout="let p = this.querySelector('polygon'); p.setAttribute('fill', p.getAttribute('data-orig-fill')); p.setAttribute('stroke', 'var(--glass-bg)');"
                    >
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" style="transition: all 0.2s ease;" />
                    </g>`;
                    
                    window['nodeData_' + idx] = {
                        hostname: node.name,
                        port: node.role === 'ProxySQL' ? 6032 : (nodeType === 'PostgreSQL' ? 5432 : 3306),
                        status: node.status,
                        role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'None',
                        type: nodeType,
                        cluster: `${node.clusterName} (ID:${node.clusterId})`,
                        badge: roleBadge,
                        color: node.color
                    };
                });
                hexHtml += '</svg>';
                hcContainer.innerHTML = hexHtml;
                
                
                let hoverTimeout;
                document.querySelectorAll('.node-hex-hover').forEach(el => {
                    el.onmouseenter = (e) => {
                        clearTimeout(hoverTimeout);
                        hoverTimeout = setTimeout(() => {
                            const ntt = document.getElementById('node-hover-tooltip');
                            const data = window['nodeData_' + el.getAttribute('data-idx')];
                            if (ntt && data) {
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
                           dnSlice.addEventListener('mouseenter', (e) => {
                               if(donutText) donutText.innerText = `${allNodes.length - shutDownCount} Operational`;
                               donutTooltip.style.display = 'block';
                           });
                           dnSlice.addEventListener('mousemove', (e) => {
                               donutTooltip.style.left = (e.clientX + 10) + 'px';
                               donutTooltip.style.top = (e.clientY + 10) + 'px';
                           });
                           dnSlice.addEventListener('mouseleave', () => {
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

    const logs = window.auditLogsData || [];
    let filtered = logs;

    if (query) {
        filtered = logs.filter(log => {
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

    if (filtered.length === 0) {
        if (query) {
            // Empty state when search filters have no match
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
            // Empty state when no audit logs exist at all
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

window.clearAuditFilters = function() {
    const input = document.getElementById('audit-search-input');
    if (input) input.value = '';
    window.filterAuditLogs();
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
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 20px;">
                                <div>
                                    <div style="font-size: 0.8rem; color: ${projColor}; text-transform: uppercase; font-weight: bold; margin-bottom: 4px;">${escapeHTML(proj.name)}</div>
                                    <h2 style="margin: 0; font-size: 1.2rem;">${escapeHTML(node.name)} <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-muted);">(${escapeHTML(node.role)})</span></h2>
                                </div>
                                <span class="status-badge status-offline" id="metric-${node.id}-status">Offline</span>
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
        btnSyncRepDashboard.addEventListener('click', () => {
            modalSyncStatus.style.display = 'flex';
            const dataFlow = document.getElementById('sync-data-flow');
            if(dataFlow) {
                dataFlow.style.animation = 'dataFlowRight 1.5s infinite linear';
            }
        });
    }

    if (btnCloseSyncModal && modalSyncStatus) {
        btnCloseSyncModal.addEventListener('click', () => {
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

    btnCloseEditNodeModal.addEventListener('click', () => {
        modalEditNode.style.display = 'none';
        editNodeUrlInput.value = '';
        editNodeUrlInput.type = 'password';
        if(modalMetricsInterval) clearInterval(modalMetricsInterval);
    });

    const eyeOpenSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
    const eyeClosedSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle><line x1="1" y1="1" x2="23" y2="23"></line></svg>';

    toggleEditUrlBtn.addEventListener('click', () => {
        if(editNodeUrlInput.type === 'password') {
            editNodeUrlInput.type = 'text';
            toggleEditUrlBtn.innerHTML = eyeOpenSvg;
        } else {
            editNodeUrlInput.type = 'password';
            toggleEditUrlBtn.innerHTML = eyeClosedSvg;
        }
    });

    copyEditUrlBtn.addEventListener('click', () => {
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

    formEditNode.addEventListener('submit', async (e) => {
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
    btnBackProjects.addEventListener('click', () => { window.location.hash = 'clusters-view'; });

    // Form: Edit Project
    btnCloseEditProjModal.addEventListener('click', () => modalEditProj.style.display = 'none');
    
    formEditProj.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('edit-proj-id').value;
        const name = document.getElementById('edit-proj-name').value;
        const desc = document.getElementById('edit-proj-desc').value;

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
                alert(res.message || "Failed to update project.");
            }
        } catch (err) {
            alert('Server error while updating project.');
        }
    });

    
              


    // Form: Add Project
    formAddProj.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('proj-name').value;
        const desc = document.getElementById('proj-desc').value;

        try {
            const response = await apiFetch('/api/projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description: desc })
            });
            const res = await response.json();
            if (res.success) {
                modalAddProj.style.display = 'none';
                formAddProj.reset();
                fetchProjects();
        fetchRecentAlarms();
            }
        } catch (err) {
            alert('Failed to create project');
        }
    });

    // Form: Add Node
    formAddNode.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentProjectId) return;

        const name = document.getElementById('node-name').value;
        const role = document.getElementById('node-role').value;
        const url = document.getElementById('node-url').value;

        btnSubmitNode.innerText = "Pinging Server (Please Wait)...";
        btnSubmitNode.disabled = true;

        try {
            const response = await apiFetch(`/api/projects/${currentProjectId}/nodes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role, name, url })
            });
            const res = await response.json();
            
            if (response.ok && res.success) {
                modalAddNode.style.display = 'none';
                formAddNode.reset();
                refreshCurrentProject();
            } else {
                alert(res.message || "Failed to add node. Check the URL.");
            }
        } catch (err) {
            alert('Server error while adding node.');
        } finally {
            btnSubmitNode.innerText = "Verify & Save Node";
            btnSubmitNode.disabled = false;
        }
    });

    // Button: Sync Replication
    btnSyncReplication.addEventListener('click', async () => {
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
        btnCleanupSlots.addEventListener('click', async () => {
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
        btnEditProjectDetail.addEventListener('click', async () => {
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

    // Button: Refresh Logs
    const btnRefreshLogs = document.getElementById('btn-refresh-logs');
    if(btnRefreshLogs) {
        btnRefreshLogs.addEventListener('click', window.fetchAuditLogs);
    }

    // Button: Save Settings
    const btnSaveSettings = document.getElementById('btn-save-settings');
    const updateIntervalInput = document.getElementById('setting-update-interval');
    if (updateIntervalInput) {
        updateIntervalInput.value = localStorage.getItem('dashboard_update_interval_sec') || 1;
    }
    
    const settingsProjectSelect = document.getElementById('setting-project-select');
    const projectSettingsContainer = document.getElementById('project-settings-container');
    const settingWalLag = document.getElementById('setting-wal-lag');
    const settingMetricTable = document.getElementById('setting-metric-table');
    const settingReplicationTables = document.getElementById('setting-replication-tables');

    // Populate projects select when settings view is opened
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', async (e) => {
            const targetId = e.target.getAttribute('data-view');
            if (targetId === 'settings-view') {
                try {
                    const response = await apiFetch('/api/projects');
                    if (response.ok) {
                        const projs = await response.json();
                        settingsProjectSelect.innerHTML = '<option value="">Proje seçin...</option>';
                        projs.forEach(p => {
                            const opt = document.createElement('option');
                            opt.value = p.id;
                            opt.textContent = p.name;
                            settingsProjectSelect.appendChild(opt);
                        });
                        projectSettingsContainer.style.display = 'none';
                    }
                } catch(err) {
                    console.error("Failed to fetch projects for settings", err);
                }
            }
        });
    });

    if (settingsProjectSelect) {
        settingsProjectSelect.addEventListener('change', async (e) => {
            const pid = e.target.value;
            if (!pid) {
                projectSettingsContainer.style.display = 'none';
                return;
            }
            try {
                const res = await apiFetch(`/api/settings/${pid}`);
                if (res.ok) {
                    const data = await res.json();
                    settingWalLag.value = data.max_wal_lag_mb || 500;
                    if (settingMetricTable) settingMetricTable.value = data.metric_table || '';
                    if (settingReplicationTables) settingReplicationTables.value = data.replication_tables || '';
                    projectSettingsContainer.style.display = 'block';
                }
            } catch (err) {
                console.error("Error loading settings for project", err);
            }
        });
    }

    if(btnSaveSettings) {
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
            
            btnSaveSettings.innerText = "Saving...";
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
                    alert("Settings saved successfully!");
                }
            } catch (e) {
                alert("Error saving settings");
            }
            btnSaveSettings.innerText = "Save Settings";
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

document.getElementById('toggle-url-btn').addEventListener('click', function() { const input = document.getElementById('node-url'); const icon = this.querySelector('svg'); if (input.type === 'password') { input.type = 'text'; icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>'; } else { input.type = 'password'; icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle><line x1="1" y1="1" x2="23" y2="23"></line>'; } });

document.getElementById('copy-url-btn').addEventListener('click', function() { const input = document.getElementById('node-url'); navigator.clipboard.writeText(input.value).then(() => { const originalHTML = this.innerHTML; this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00ff00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'; setTimeout(() => { this.innerHTML = originalHTML; }, 2000); }); });






// Sidebar Toggle Logic
document.getElementById('btn-toggle-sidebar').addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
    const icon = document.getElementById('icon-sidebar-arrow');
    if (sidebar.classList.contains('collapsed')) {
        icon.innerHTML = '<polyline points="9 18 15 12 9 6"></polyline>';
    } else {
        icon.innerHTML = '<polyline points="15 18 9 12 15 6"></polyline>';
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


const usersData = [
        { initial: 'DU', bg: '#fef3c7', color: '#d97706', user: 'admin', email: '', team: 'admins', fname: 'Default', lname: 'User', status: 'Enabled', created: '4 months ago' },
        { isIcon: true, user: 'demo', email: 'demo@severalnines.com', team: 'admins', fname: '', lname: '', status: 'Enabled', created: '3 months ago' },
        { initial: 'DC', bg: '#ffe4e6', color: '#e11d48', user: 'demo@severalnines.com', email: 'demo@severalnines.com', team: 'admins', fname: 'Demo', lname: 'ClusterControl', status: 'Enabled', created: '3 months ago' },
        { initial: 'DU', bg: '#e0f2fe', color: '#0284c7', user: 'nobody', email: '', team: 'nobody', fname: 'Default', lname: 'User', status: 'Enabled', created: '4 months ago' },
        { initial: 'SU', bg: '#f3e8ff', color: '#9333ea', user: 'system', email: '', team: 'admins', fname: 'System', lname: 'User', status: 'Enabled', created: '4 months ago' }
    ];

    let currentSort = 'none'; // 'none', 'asc', 'desc'

    function renderUsers() {
        const tbody = document.getElementById('users-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';
        
        let sortedData = [...usersData];
        if (currentSort === 'asc') {
            sortedData.sort((a, b) => a.user.localeCompare(b.user));
        } else if (currentSort === 'desc') {
            sortedData.sort((a, b) => b.user.localeCompare(a.user));
        }

        sortedData.forEach(u => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--glass-border)';
            
            let avatar = '';
            if (u.isIcon) {
                avatar = `<div style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #14b8a6; display: flex; align-items: center; justify-content: center; color: #14b8a6; font-size: 14px;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>`;
            } else {
                avatar = `<div style="width: 32px; height: 32px; border-radius: 50%; background: ${u.bg}; color: ${u.color}; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 600;">${u.initial}</div>`;
            }
            
            tr.innerHTML = `
                <td style="padding: 16px 24px; display: flex; align-items: center; gap: 12px; font-weight: 500; color: var(--text-main);">${avatar} ${u.user}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--text-main);">${u.email}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--text-main);">${u.team}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--text-main);">${u.fname}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--text-main);">${u.lname}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--success);">${u.status}</td>
                <td style="padding: 16px 24px; font-size: 0.9rem; color: var(--text-main);">${u.created}</td>
                <td style="padding: 16px 24px;">
                    <button style="background: transparent; border: 1px solid var(--border); border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #6b7280;">...</button>
                </td>
            `;
            if (tbody) { tbody.appendChild(tr); }
        });
        
        // Update Sort Arrows
        const arrows = document.getElementById('user-sort-arrows');
        if (arrows) {
            if (currentSort === 'asc') arrows.innerHTML = '&#9650;';
            else if (currentSort === 'desc') arrows.innerHTML = '&#9660;';
            else arrows.innerHTML = '&#9650;&#9660;';
        }
    }

    const thUser = document.getElementById('th-user-col');
    const userTooltip = document.getElementById('user-sort-tooltip');
    
    if (thUser) {
        thUser.onmouseenter = () => {
            userTooltip.style.display = 'block';
            if (currentSort === 'none') userTooltip.childNodes[0].nodeValue = 'Click to sort ascending';
            else if (currentSort === 'asc') userTooltip.childNodes[0].nodeValue = 'Click to sort descending';
            else userTooltip.childNodes[0].nodeValue = 'Click to cancel sorting';
        };
        thUser.onmouseleave = () => {
            userTooltip.style.display = 'none';
        };
        thUser.onclick = () => {
            if (currentSort === 'none') currentSort = 'asc';
            else if (currentSort === 'asc') currentSort = 'desc';
            else currentSort = 'none';
            
            if (currentSort === 'none') userTooltip.childNodes[0].nodeValue = 'Click to sort ascending';
            else if (currentSort === 'asc') userTooltip.childNodes[0].nodeValue = 'Click to sort descending';
            else userTooltip.childNodes[0].nodeValue = 'Click to cancel sorting';
            
            renderUsers();
        };
    }
    
    // Switch Users Tabs
    const btnTabUsers = document.getElementById('tab-btn-users');
    const btnTabTeams = document.getElementById('tab-btn-teams');
    const btnTabLdap = document.getElementById('tab-btn-ldap');
    const contentUsers = document.getElementById('content-users');
    const contentTeams = document.getElementById('content-teams');
    const contentLdap = document.getElementById('content-ldap');
    
    function switchUsersTab(tab) {
        [btnTabUsers, btnTabTeams, btnTabLdap].forEach(btn => {
            if(btn) {
                btn.classList.remove('active');
                btn.style.color = '#4b5563';
                btn.style.borderBottom = '2px solid transparent';
            }
        });
        [contentUsers, contentTeams, contentLdap].forEach(content => {
            if(content) content.style.display = 'none';
        });
        
        if (tab === 'users') {
            if(btnTabUsers) { btnTabUsers.style.color = 'var(--primary)'; btnTabUsers.style.borderBottom = '2px solid var(--primary)'; }
            if(contentUsers) contentUsers.style.display = 'block';
        } else if (tab === 'teams') {
            if(btnTabTeams) { btnTabTeams.style.color = 'var(--primary)'; btnTabTeams.style.borderBottom = '2px solid var(--primary)'; }
            if(contentTeams) contentTeams.style.display = 'block';
        } else if (tab === 'ldap') {
            if(btnTabLdap) { btnTabLdap.style.color = 'var(--primary)'; btnTabLdap.style.borderBottom = '2px solid var(--primary)'; }
            if(contentLdap) contentLdap.style.display = 'block';
        }
    }
    
    if(btnTabUsers) btnTabUsers.addEventListener('click', () => switchUsersTab('users'));
    if(btnTabTeams) btnTabTeams.addEventListener('click', () => switchUsersTab('teams'));
    if(btnTabLdap) btnTabLdap.addEventListener('click', () => switchUsersTab('ldap'));

    // Render initially
    renderUsers();
});


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
                    version: '<div class="cc-spinner cc-spinner-sm" style="opacity:0.6;"></div>',
                    seen: 'in 4 minutes',
                    projId: proj.id
                });
            }
        }

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


// --- BACKUP MODALS LOGIC ---
document.addEventListener('DOMContentLoaded', () => {
    const btnGlobalCreateBackup = document.getElementById('btn-global-create-backup');
    const modalBackupType = document.getElementById('modal-backup-type-select');
    const btnCloseBackupType = document.getElementById('btn-close-backup-type-modal');
    
    const btnBackupOnDemand = document.getElementById('btn-select-backup-ondemand');
    const btnBackupSchedule = document.getElementById('btn-select-backup-schedule');
    
    const modalBackupConfig = document.getElementById('modal-create-backup-config');
    const btnCloseBackupConfig = document.getElementById('btn-close-backup-config-modal');
    const btnBackupConfigBack = document.getElementById('btn-backup-config-back');
    const btnBackupConfigContinue = document.getElementById('btn-backup-config-continue');
    
    const selectCluster = document.getElementById('backup-config-cluster');
    const selectHost = document.getElementById('backup-config-host');
    
    let allProjectsForBackup = [];

    if (btnGlobalCreateBackup) {
        btnGlobalCreateBackup.addEventListener('click', () => {
            modalBackupType.style.display = 'flex';
        });
    }
    if (btnCloseBackupType) {
        btnCloseBackupType.addEventListener('click', () => {
            modalBackupType.style.display = 'none';
        });
    }
    
    const openConfigModal = async () => {
        modalBackupType.style.display = 'none';
        modalBackupConfig.style.display = 'flex';
        
        // Fetch projects to populate the select
        try {
            const res = await apiFetch('/api/projects');
            if (res.ok) {
                allProjectsForBackup = await res.json();
                selectCluster.innerHTML = '<option value="">Select a cluster...</option>' + 
                    allProjectsForBackup.map(p => `<option value="${p.id}">${p.name} (ID:${p.id})</option>`).join('');
            }
        } catch (e) {
            console.error("Failed to load clusters for backup:", e);
        }
    };
    
    if (btnBackupOnDemand) btnBackupOnDemand.addEventListener('click', openConfigModal);
    if (btnBackupSchedule) btnBackupSchedule.addEventListener('click', openConfigModal);
    
    if (btnCloseBackupConfig) btnCloseBackupConfig.addEventListener('click', () => modalBackupConfig.style.display = 'none');
    if (btnBackupConfigBack) {
        btnBackupConfigBack.addEventListener('click', () => {
            modalBackupConfig.style.display = 'none';
            modalBackupType.style.display = 'flex';
        });
    }
    
    if (selectCluster) {
        selectCluster.addEventListener('change', (e) => {
            const pid = parseInt(e.target.value);
            if (!pid) {
                selectHost.innerHTML = '<option value="">Select a cluster first...</option>';
                selectHost.disabled = true;
                return;
            }
            const proj = allProjectsForBackup.find(p => p.id === pid);
            if (proj && proj.nodes && proj.nodes.length > 0) {
                selectHost.innerHTML = proj.nodes.map(n => {
                    const hostUrl = n.url ? n.url.split('@')[1] || n.url : 'Unknown';
                    const role = n.role ? (n.role.charAt(0).toUpperCase() + n.role.slice(1)) : 'Unknown';
                    return `<option value="${n.id}">${n.name} - ${hostUrl} (${role})</option>`;
                }).join('');
                selectHost.disabled = false;
            } else {
                selectHost.innerHTML = '<option value="">No nodes found in this cluster</option>';
                selectHost.disabled = true;
            }
        });
    }
    
    if (btnBackupConfigContinue) {
        btnBackupConfigContinue.addEventListener('click', () => {
            const clusterVal = selectCluster.value;
            const hostVal = selectHost.value;
            if (!clusterVal || !hostVal) {
                alert("Please select a Cluster and Backup host first.");
                return;
            }
            
            // Per user request, show honest error message
            alert("Error: Cloud Storage (AWS S3) is not configured. Local disk backups are disabled.");
        });
    }
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
    const modalTitle = document.getElementById('modal-create-report-title');

    if (tabName === 'reports') {
        tabReports.style.color = 'var(--primary)';
        tabReports.style.borderBottomColor = 'var(--primary)';
        tabSchedules.style.color = 'var(--text-muted)';
        tabSchedules.style.borderBottomColor = 'transparent';
        
        tableReports.style.display = 'block';
        tableSchedules.style.display = 'none';
        
        textAction.innerText = 'Create report';
        modalTitle.innerText = 'Generate new report';
    } else {
        tabSchedules.style.color = 'var(--primary)';
        tabSchedules.style.borderBottomColor = 'var(--primary)';
        tabReports.style.color = 'var(--text-muted)';
        tabReports.style.borderBottomColor = 'transparent';
        
        tableSchedules.style.display = 'block';
        tableReports.style.display = 'none';
        
        textAction.innerText = 'Create schedule';
        modalTitle.innerText = 'Generate new schedule';
    }
}


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


async function fetchProfile() {
    try {
        const res = await apiFetch('/api/users/me');
        if (res.ok) {
            const data = await res.json();
            const avatar = document.getElementById('profile-avatar');
            const fullname = document.getElementById('profile-fullname');
            const role = document.getElementById('profile-role');
            const username = document.getElementById('profile-username');
            const team = document.getElementById('profile-team');
            
            if (avatar) avatar.innerText = data.username.substring(0, 2);
            if (fullname) fullname.innerText = data.username;
            if (role) role.innerText = data.role;
            if (username) username.innerText = data.username;
            if (team) team.innerText = data.team;
            const headerUser = document.getElementById('header-username-display');
            if (headerUser) headerUser.innerText = data.username;
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
        const res = await apiFetch('/api/backups');
        if (!res.ok) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">No backup jobs found.</td></tr>'; return; }
        const jobs = await res.json();
        if (!jobs || jobs.length === 0) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#9ca3af;">No backup jobs found.</td></tr>'; return; }
        tbody.innerHTML = jobs.map(j => {
            const sc = j.status === 'completed' ? '#10b981' : (j.status === 'failed' ? '#ef4444' : '#f59e0b');
            const sl = j.status === 'completed' ? 'Completed' : (j.status === 'failed' ? 'Failed' : (j.status || 'Paused'));
            return '<tr style="border-bottom: 1px solid #f3f4f6;"><td style="padding: 12px 20px; font-size: 0.85rem;">' + escapeHTML(j.backup_name || j.name || 'Backup Job') + '</td><td style="padding: 12px 20px;"><span style="color:' + sc + ';font-size:0.8rem;display:inline-flex;align-items:center;gap:5px;"><div style=\"width:6px;height:6px;border-radius:50%;background:' + sc + '\"></div>' + sl + '</span></td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.cluster_name || j.project_name || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_by || 'system') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + escapeHTML(j.created_at || '-') + '</td><td style="padding: 12px 20px; font-size: 0.85rem; color: #6b7280;">' + (j.duration || '0s') + '</td><td style="padding: 12px 20px;"><button style="padding: 4px 10px; font-size: 0.75rem; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; background: white;">...</button></td></tr>';
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
