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
    return fetch(url, options);
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
                this.size = Math.random() * 80 + 30;
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
                ctx.globalAlpha = 0.5;
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
        
        for (let i = 0; i < 50; i++) {
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
    }

    function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        detailView.style.display = 'block';
        currentProjectId = proj.id;
        
        document.getElementById('detail-proj-name').innerText = proj.name;
        document.getElementById('detail-proj-desc').innerText = proj.description || 'No description';
        
        renderNodes(proj.nodes);
    }

    function renderNodes(nodes) {
        if (!nodes || nodes.length === 0) {
            nodesContainer.innerHTML = '<div class="loading-state">No nodes added yet.</div>';
            return;
        }

        nodesContainer.innerHTML = '';
        nodes.forEach(node => {
            const card = document.createElement('div');
            card.className = 'project-card glass-panel';
            // Make card look clickable
            card.style.cursor = 'pointer';
            card.title = 'Click to view or edit connection URL';
            const color = node.role.toLowerCase() === 'primary' ? 'var(--primary)' : 'var(--warning)';
            card.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <h3>${escapeHTML(node.name)}</h3>
                    <span style="color: ${color}; font-weight:bold; font-size:0.8rem;">${node.role.toUpperCase()}</span>
                </div>
                <p style="color: var(--success); font-size:0.8rem; margin-top:10px;">🟢 Secured & Encrypted</p>
            `;
            card.addEventListener('click', () => openEditNodeModal(node.id, node.name));
            nodesContainer.appendChild(card);
        });
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
            const response = await apiFetch('/api/projects');
            if (!response.ok) {
                const errText = await response.text();
                projectsContainer.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Server returned ${response.status}: ${escapeHTML(errText)}</div>`;
                return;
            }
            const data = await response.json();
            if (data.length === 0) {
                document.getElementById('cc-projects-tbody').innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 20px;">No clusters found. Click + Add Project to start.</td></tr>';
                document.getElementById('cc-total-clusters').innerText = '0 Clusters';
                return;
            }

            const tbody = document.getElementById('cc-projects-tbody');
            tbody.innerHTML = '';
            
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
                      
                      a.className = "submenu-item"; a.onclick = (e) => {
                            e.preventDefault();
                            if (window.location.hash !== '#dashboard-view') {
                                window.location.hash = 'dashboard-view';
                            } else {
                                handleRouting();
                            }
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
                        document.getElementById('tt-cluster-id').innerText = proj.id; 
                        document.getElementById('tt-cluster-name').innerText = proj.name; 
                        let vendor = 'PostgreSQL Streaming v18.4'; 
                        let vendorType = 'postgres';
                        let nameLower = proj.name.toLowerCase();
                        if (nameLower.includes('maria')) { vendor = 'MariaDB Replication v11.8'; vendorType = 'mariadb'; }
                        else if (nameLower.includes('percona mysql')) { vendor = 'Percona Replication v8.4'; vendorType = 'percona_mysql'; }
                        else if (nameLower.includes('percona')) { vendor = 'Percona XtraDB Cluster'; vendorType = 'percona'; }
                        else if (nameLower.includes('mongo')) { vendor = 'MongoDB ReplicaSet v8.0'; vendorType = 'mongo'; }
                        else if (nameLower.includes('timescale')) { vendor = 'TimescaleDB v18'; vendorType = 'timescale'; }
                        else if (nameLower.includes('mssql')) { vendor = 'SQL Server v2022'; vendorType = 'mssql'; }
                        
                        document.getElementById('tt-cluster-vendor').innerText = vendor; 

                        
                        
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
                        
                        topoContainer.innerHTML = topoHtml;

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

                document.getElementById('cc-clusters-list').appendChild(clusterCard);
                tbody.appendChild(tr);
            });
            
            // Update Donut Chart
            document.getElementById('cc-total-clusters').innerText = `${data.length} Clusters`;
            document.getElementById('cc-donut-center-text').innerText = operationalCount;
            
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
                        donutText.innerText = `${operationalCount} Operational`;
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
            document.getElementById('cc-donut-legend').innerHTML = `
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--success);">&#8226; ${operationalCount} Operational</span>
                </div>
                ${warningCount > 0 ? `<div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--warning);">&#8226; ${warningCount} Warning</span>
                </div>` : ''}
            `;
            
            // Apply current filter
            const filterVal = document.getElementById('cc-status-filter')?.value || 'All';
            const rows = tbody.querySelectorAll('tr');
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
                    {x:20, y:20}, {x:76, y:20}, {x:132, y:20}, {x:188, y:20},
                    {x:48, y:68}, {x:104, y:68}, {x:160, y:68},
                    {x:20, y:116}, {x:76, y:116}, {x:132, y:116}, {x:188, y:116}
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
                    const polyPoints = "32,0 60,16 60,48 32,65 4,48 4,16";
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})">
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" />
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
                                
                                document.getElementById('ntt-hostname').innerText = data.hostname;
                                document.getElementById('ntt-port').innerText = data.port;
                                document.getElementById('ntt-role').innerText = data.role;
                                document.getElementById('ntt-type').innerText = data.type;
                                document.getElementById('ntt-cluster').innerText = data.cluster;
                                document.getElementById('ntt-badge').innerHTML = data.badge;
                                
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
                
                document.getElementById('cc-total-nodes').innerText = allNodes.length + ' Nodes';
                
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
                               donutText.innerText = `${allNodes.length - shutDownCount} Operational`;
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
                
                const nodeStats = document.getElementById('nodes-donut-slice').parentNode.parentNode.nextElementSibling;
                if (nodeStats) {
                    nodeStats.innerHTML = `<span style="color: var(--success);">&#8226; ${allNodes.length - shutDownCount} Operational</span><span style="color: var(--primary);">&#8226; ${shutDownCount} Shut Down</span>`;
                }
            }

        } catch (error) {
            console.error("fetchProjects error:", error);
            const errDiv = document.getElementById('projects-container');
            if (errDiv) errDiv.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.toString())}</div>`;
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

    
    window.fetchAuditLogs = async function() {

        const tbody = document.getElementById('audit-table-body');
        if(!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="6" style="padding: 16px 24px; text-align: center; color: var(--text-muted);">Loading logs...</td></tr>';
        
        try {
            const res = await apiFetch('/api/audit-logs');
            if (!res.ok) {
                const errText = await res.text();
                tbody.innerHTML = `<tr><td colspan="6" style="padding: 16px 24px; text-align: center; color: var(--danger);">Failed to load logs: ${escapeHTML(errText)}</td></tr>`;
                return;
            }
            const data = await res.json();
            
            if (data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="padding: 60px 20px; text-align: center;">
                            <svg width="72" height="72" viewBox="0 0 24 24" fill="#e5e7eb" stroke="none" style="margin-bottom: 24px;">
                                <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
                            </svg>
                            <div style="color: #4b5563; font-size: 0.95rem; font-weight: 400; margin-bottom: 16px;">No audit log entries match your current filters.</div>
                            <a href="#" style="color: var(--primary); font-size: 0.9rem; text-decoration: none; font-weight: 500;">Clear all filters</a>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = '';
            data.forEach(log => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--glass-border)';
                
                let timeStr = log.timestamp;
                if (timeStr) {
                    const d = new Date(timeStr);
                    timeStr = d.toISOString().replace('T', ' ').substring(0, 19) + ' +03';
                } else {
                    timeStr = 'Unknown';
                }
                
                let type = "system";
                let actionLower = log.action ? log.action.toLowerCase() : "";
                if(actionLower.includes('login') || actionLower.includes('auth')) type = "authentication";
                else if(actionLower.includes('project') || actionLower.includes('create') || actionLower.includes('delete')) type = "project_management";
                
                let actionStr = log.action || "Unknown action";
                if (log.details) {
                    actionStr += " - " + log.details;
                }
                
                tr.innerHTML = `
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #111827;">${escapeHTML(timeStr)}</td>
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${escapeHTML(actionStr)}</td>
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${escapeHTML(type)}</td>
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">admin@sunucu.local</td>
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">127.0.0.1</td>
                    <td style="padding: 16px 24px; font-size: 0.85rem; color: #374151;">${log.project_id ? "Project ID: " + log.project_id : "N/A"}</td>
                `;
                tbody.appendChild(tr);
            });
            
        } catch (e) {
            tbody.innerHTML = `<tr><td colspan="6" style="padding: 16px 24px; text-align: center; color: var(--danger);">Network error fetching logs.</td></tr>`;
        }
    }

    async function fetchDashboardMetrics() {
        try {
            const projRes = await apiFetch('/api/projects');
            if (!projRes.ok) return;
            const projs = await projRes.json();
            
            const container = document.getElementById('dashboard-metrics-container');
            if(!container) return;

            if (projs.length === 0) {
                container.innerHTML = '<div class="loading-state">No projects found. Add a project to view metrics.</div>';
                return;
            }
            
            if (container.querySelector('.loading-state')) {
                container.innerHTML = '';
            }
            
            // Fetch metrics for all projects concurrently
            const metricPromises = projs.map(p => apiFetch(`/api/projects/${p.id}/metrics`).then(r => r.ok ? r.json() : []));
            const metricsResults = await Promise.all(metricPromises);
            
            // Flat list of all nodes returned by metrics API
            const allNodes = metricsResults.flat();
            
            // Remove columns for nodes that no longer exist
            const allNodeIds = allNodes.map(n => "dash-node-" + n.id);
            Array.from(container.children).forEach(child => {
                if (!allNodeIds.includes(child.id)) {
                    child.remove();
                }
            });
            
            projs.forEach((proj, i) => {
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
                    if(m && m.ping !== undefined) {
                        document.getElementById("metric-" + node.id + "-status").className = 'status-badge status-online';
                        document.getElementById("metric-" + node.id + "-status").innerText = 'Aktif';
                        
                        document.getElementById("metric-" + node.id + "-ping").innerText = m.ping;
                        document.getElementById("metric-" + node.id + "-lag").innerText = m.lag;
                        document.getElementById("metric-" + node.id + "-storage").innerText = m.storage;
                        document.getElementById("metric-" + node.id + "-conn").innerText = m.connections;
                        document.getElementById("metric-" + node.id + "-xact").innerText = m.xact;
                        document.getElementById("metric-" + node.id + "-cache").innerText = m.cache_hit;
                        document.getElementById("metric-" + node.id + "-version").innerText = m.version;
                        document.getElementById("metric-" + node.id + "-uptime").innerText = m.uptime;
                        document.getElementById("metric-" + node.id + "-plates").innerText = m.plates;
                    } else {
                        document.getElementById("metric-" + node.id + "-status").className = 'status-badge status-offline';
                        document.getElementById("metric-" + node.id + "-status").innerText = 'Çevrimdışı';
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
                document.getElementById('modal-metric-status').innerText = 'Hata (502)';
                return;
            }
            const data = await res.json();
            
            if(!data || data.status !== 'online') {
                document.getElementById('modal-metric-status').className = 'status-badge status-offline';
                document.getElementById('modal-metric-status').innerText = 'Offline';
                return;
            }
            
            document.getElementById('modal-metric-status').className = 'status-badge status-online';
            document.getElementById('modal-metric-status').innerText = 'Aktif';
            
            document.getElementById('modal-metric-ping').innerText = data.ping || '-';
            document.getElementById('modal-metric-lag').innerText = data.lag || '0ms';
            document.getElementById('modal-metric-storage').innerText = data.storage || '-';
            document.getElementById('modal-metric-conn').innerText = data.connections || '-';
            document.getElementById('modal-metric-xact').innerText = data.xact || '-';
            document.getElementById('modal-metric-cache').innerText = data.cache_hit || '-';
            document.getElementById('modal-metric-uptime').innerText = data.uptime || '-';
            document.getElementById('modal-metric-version').innerText = data.version || '-';
            document.getElementById('modal-metric-plates').innerText = data.plates || 'N/A';
            
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
        document.getElementById('modal-metric-status').innerText = 'Loading...';
        const spinnerHtml = '<svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg> Yükleniyor...';
        ['ping', 'lag', 'storage', 'conn', 'xact', 'cache', 'uptime', 'version', 'plates'].forEach(m => {
            document.getElementById(`modal-metric-${m}`).innerHTML = spinnerHtml;
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
    btnBackProjects.addEventListener('click', () => { window.location.hash = 'projects-view'; });

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
                
                // Update detail view if it's currently showing the edited project
                if (currentProjectId == id && detailView && detailView.style.display !== 'none') {
                    document.getElementById('detail-proj-name').innerText = name;
                    document.getElementById('detail-proj-desc').innerText = desc || 'No description';
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
                tbody.appendChild(tr);
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

function renderBackups() {
    const tbodyAll = document.getElementById('all-backups-tbody');
    const tbodySched = document.getElementById('schedules-tbody');
    
    if (tbodyAll) {
        tbodyAll.innerHTML = backupsData.map(b => `
            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.2s; cursor: pointer;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                <td style="padding: 16px 24px; font-size: 0.9rem; color: #111827;">${b.id}</td>
                <td style="padding: 16px 10px; color: #6b7280;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                </td>
                <td style="padding: 16px 10px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        ${getClusterIconStr(b.clusterType)}
                        <span style="font-size: 0.9rem; color: #111827;">${b.cluster}</span>
                    </div>
                </td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #111827;">${b.method}</td>
                <td style="padding: 16px 10px;">
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #16a34a;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: #16a34a;"></span>
                        ${b.status}
                    </div>
                </td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #111827;">${b.title}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${b.created}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${b.size}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${b.host}</td>
                <td style="padding: 16px 10px;">
                    <div style="display: flex; align-items: center; gap: 6px; color: #4b5563;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5"></path><path d="M2 12l10 5 10-5"></path></svg>
                        <span style="font-size: 0.9rem;">0</span>
                    </div>
                </td>
                <td style="padding: 16px 24px;">
                    <button style="background: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #6b7280;">...</button>
                </td>
            </tr>
        `).join('');
    }

    if (tbodySched) {
        tbodySched.innerHTML = schedulesData.map(s => `
            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.2s; cursor: pointer;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                <td style="padding: 16px 24px; font-size: 0.9rem; color: #111827;">${s.name}</td>
                <td style="padding: 16px 10px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        ${getClusterIconStr(s.clusterType)}
                        <span style="font-size: 0.9rem; color: #111827;">${s.cluster}</span>
                    </div>
                </td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #111827;">${s.method}</td>
                <td style="padding: 16px 10px;">
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #d97706;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: #f59e0b;"></span>
                        ${s.status}
                    </div>
                </td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${s.schedule}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${s.host}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${s.storageHost}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${s.location}</td>
                <td style="padding: 16px 10px; font-size: 0.9rem; color: #4b5563;">${s.lastExec}</td>
                <td style="padding: 16px 24px;">
                    <button style="background: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #6b7280;">...</button>
                </td>
            </tr>
        `).join('');
    }
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
            tbody.appendChild(tr);
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
document.addEventListener('DOMContentLoaded', () => {
    const nodesPageData = [
        { host: 'plaka-master-node', port: '5432', ip: '192.168.1.10', status: 'Operational', type: 'PostgreSQL', role: 'Primary', badge: {text: 'Writable', color: '#16a34a', bg: '#dcfce7'}, cluster: 'Araç Plaka Takip Sistemi', clusterLogo: '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>', clusterColor: '#3b82f6', version: '18.4', seen: 'in 1 minute' },
        { host: 'plaka-replica-node', port: '5432', ip: '192.168.1.11', status: 'Operational', type: 'PostgreSQL', role: 'Replica', badge: {text: 'Readonly', color: '#4b5563', bg: '#f3f4f6'}, cluster: 'Araç Plaka Takip Sistemi', clusterLogo: '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>', clusterColor: '#3b82f6', version: '18.4', seen: 'in 1 minute' },
        { host: 'email-master-node', port: '3306', ip: '10.0.0.50', status: 'Operational', type: 'MariaDB', role: 'Primary', badge: {text: 'Writable', color: '#16a34a', bg: '#dcfce7'}, cluster: 'E-mail Okuma Programı', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', clusterColor: '#1f2937', version: '11.8', seen: 'in 2 minutes' },
        { host: 'email-replica-node', port: '3306', ip: '10.0.0.51', status: 'Operational', type: 'MariaDB', role: 'Replica', badge: {text: 'Readonly', color: '#4b5563', bg: '#f3f4f6'}, cluster: 'E-mail Okuma Programı', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', clusterColor: '#1f2937', version: '11.8', seen: 'in 2 minutes' }
    ];


    let currentFilter = 'All';

    window.filterNodes = function(status, el) {
        currentFilter = status;
        
        // Update styling of all cards
        const cards = document.querySelectorAll('.node-status-card');
        cards.forEach(card => {
            card.style.borderBottom = 'none';
            card.style.background = 'transparent';
        });
        
        // Style the clicked card
        if (el) {
            el.style.borderBottom = '2px solid var(--primary)';
            el.style.background = '#f9fafb';
        }
        
        renderNodesPage();
    };

let currentSortCol = null;
    let currentSortDir = null; // 'asc', 'desc', null

    window.sortNodes = function(col) {
        if (currentSortCol !== col) {
            currentSortCol = col;
            currentSortDir = 'asc';
        } else {
            if (currentSortDir === 'asc') currentSortDir = 'desc';
            else if (currentSortDir === 'desc') currentSortDir = null;
            else currentSortDir = 'asc';
        }
        
        // Reset all tooltips and arrows
        ['host', 'port', 'status', 'type', 'role', 'cluster', 'seen'].forEach(c => {
            const arr = document.getElementById('nodes-sort-arrows-' + c);
            const txt = document.getElementById('nodes-sort-text-' + c);
            if(arr) arr.innerHTML = '&#9650;&#9660;';
            if(txt) txt.innerText = 'Click to sort ascending';
        });
        
        // Update current
        if (currentSortDir) {
            const arr = document.getElementById('nodes-sort-arrows-' + col);
            const txt = document.getElementById('nodes-sort-text-' + col);
            if (currentSortDir === 'asc') {
                if(arr) arr.innerHTML = '&#9650;';
                if(txt) txt.innerText = 'Click to sort descending';
            } else {
                if(arr) arr.innerHTML = '&#9660;';
                if(txt) txt.innerText = 'Click to Cancel Sorting';
            }
        }
        
        renderNodesPage();
    };

    function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';
        
        let filteredData = nodesPageData.filter(n => currentFilter === 'All' || n.status === currentFilter);
        
        if (currentSortDir) {
            filteredData.sort((a, b) => {
                let valA = a[currentSortCol];
                let valB = b[currentSortCol];
                
                // For nested fields like cluster, sort by name
                if (currentSortCol === 'cluster') {
                    // Extract text before (ID:xx) if needed, but string comparison works fine
                }
                
                if (valA < valB) return currentSortDir === 'asc' ? -1 : 1;
                if (valA > valB) return currentSortDir === 'asc' ? 1 : -1;
                return 0;
            });
        }
        
        if (filteredData.length === 0) {
            tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: #9ca3af; font-size: 0.9rem;">There are no matches</td></tr>`;
            return;
        }
        
        filteredData.forEach((n, i) => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--glass-border)';
            tr.style.background = 'white';
            
            let statusColor = 'var(--success)';
            let dotColor = 'var(--success)';
            if (n.status === 'Shut Down') { statusColor = '#3b82f6'; dotColor = '#3b82f6'; }
            if (n.status === 'Failed') { statusColor = '#ef4444'; dotColor = '#ef4444'; }
            
            let statusHtml = `<span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: ${dotColor};"></div> ${n.status}</span>`;
            
            let typeColor = '#059669'; // Greenish
            if (n.type === 'HAProxy') typeColor = '#8b5cf6'; // Purple
            if (n.type === 'Prometheus') typeColor = '#eab308'; // Yellow
            if (n.type === 'MongoDB') typeColor = '#059669'; // Greenish
            
            let roleHtml = `<span>${n.role}</span>`;
            if (n.badge) {
                roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: ${n.badge.bg}; color: ${n.badge.color}; border: 1px solid ${n.badge.color}; margin-left: 6px;">${n.badge.text}</span>`;
            }
            
            let logoColor = n.clusterColor || '#1f2937';
            
            tr.innerHTML = `
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.host}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.port}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.ip}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; white-space: nowrap;">${statusHtml}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: ${typeColor}; white-space: nowrap;">${n.type}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; display: flex; align-items: center;">${roleHtml}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${logoColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${n.clusterLogo}</svg>
                        ${n.cluster}
                    </div>
                </td>
                <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.version}</td>
                <td style="padding: 16px 16px; font-size: 0.8rem; color: #6b7280; white-space: nowrap; text-align: right;">${n.seen}</td>
                <td style="padding: 16px 16px; font-size: 0.85rem; text-align: center;"><button style="background: none; border: 1px solid var(--border); padding: 4px 8px; border-radius: 4px; cursor: pointer;">...</button></td>
            `;
            tbody.appendChild(tr);
        });
    }

    renderNodesPage();
});



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
            
            document.getElementById('stat-all').innerText = proj.nodes.length;
            document.getElementById('stat-operational').innerText = proj.nodes.length; // Simplified for now
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
