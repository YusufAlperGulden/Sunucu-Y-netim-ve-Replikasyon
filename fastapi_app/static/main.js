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
                this.reset(true);
            }
            reset(initial = false) {
                this.x = width / 2;
                this.y = height / 2;
                this.angle = Math.random() * Math.PI * 2;
                this.speed = Math.random() * 0.15 + 0.05;
                this.swirl = (Math.random() - 0.5) * 0.005;
                this.radius = initial ? Math.random() * (Math.max(width, height) / 2) : Math.random() * 20;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                this.size = Math.random() * 80 + 30;
                this.life = initial ? Math.random() * 200 : 0;
                this.maxLife = Math.random() * 300 + 150;
            }
            update() {
                this.angle += this.swirl;
                this.radius += this.speed;
                this.x = width / 2 + Math.cos(this.angle) * this.radius;
                this.y = height / 2 + Math.sin(this.angle) * this.radius;
                this.life++;
                if (this.life > this.maxLife || this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
                    this.reset();
                }
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                let alpha = 1;
                if (this.life < 50) alpha = this.life / 50;
                else if (this.life > this.maxLife - 50) alpha = (this.maxLife - this.life) / 50;
                ctx.globalAlpha = alpha * 0.7;
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
        
        for (let i = 0; i < 250; i++) {
            particles.push(new Particle());
            // Fast forward initial particles slightly so it's not starting from absolute center
            particles[i].x = width / 2 + Math.cos(particles[i].angle) * particles[i].radius;
            particles[i].y = height / 2 + Math.sin(particles[i].angle) * particles[i].radius;
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

    const btnDeployCluster = document.getElementById('btn-deploy-cluster');
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
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    const viewSections = document.querySelectorAll('.view-section');
    
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active class from all links
            sidebarLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');
            
            // Hide all views
            viewSections.forEach(section => {
                section.style.display = 'none';
            });
            
            // Show target view
            const targetId = link.getAttribute('data-view');
            if (targetId) {
                const view = document.getElementById(targetId);
                if (view) view.style.display = 'block';
            }
            
            // If projects view is shown, ensure detail view is hidden
            if(targetId === 'projects-view') {
                showProjectsView();
                stopDashboardInterval();
            } else if (targetId === 'audit-logs-view') {
                window.fetchAuditLogs();
                stopDashboardInterval();
            } else if (targetId === 'settings-view') {
                stopDashboardInterval();
            } else if (targetId === 'dashboard-view') {
                startDashboardInterval();
            }
        });
    });

    let dashboardInterval = null;
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
                    const ct = document.getElementById('cluster-hover-tooltip'); 
                    if (ct) { 
                        document.getElementById('tt-cluster-id').innerText = proj.id; 
                        document.getElementById('tt-cluster-name').innerText = proj.name; 
                        let vendor = 'PostgreSQL Streaming v16'; 
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
                        let disabledNode = null;
                        if (proj.nodes && proj.nodes.length > 0) {
                           // For demonstration, let's randomly pick one node to be shutdown if the status is Warning
                           if (proj.sync_status === 'FAILED' || proj.nodesCount < 2) {
                               disabledNode = proj.nodes[0];
                           }
                        }
                        
                        // BUT let's also hardcode some messages based on project name matching user screenshots
                        let msg = null;
                        if (nameLower.includes('maria')) msg = 'br4-ccdemo-svr1:3306 (Replica): Node is shutdown by user';
                        if (nameLower.includes('percona mysql')) msg = 'br2-ccdemo-svr2:3306 (Replica): Node is shutdown by user';
                        
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
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>R - Replica</span><span>P - Primary</span><span>HA - HAProxy</span><span style="color:#3b82f6;">? Shut Down</span></div>`;
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
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>S - Secondary</span><span>P - Primary</span><span style="color:var(--success);">? Operational</span></div>`;
                        } else if (vendorType === 'timescale') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="200" height="120" viewBox="0 0 200 120"><defs>${arrow}</defs>
                                <g transform="translate(40,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                                <g transform="translate(100,10)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <g transform="translate(100,60)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">R</text></g>
                                <line x1="80" y1="58" x2="100" y2="33" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                                <line x1="80" y1="58" x2="100" y2="83" stroke="#d1d5db" stroke-width="1.5" marker-end="url(#arrow)"></line>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span style="color:var(--success);">? Operational</span></div>`;
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
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span>PS - ProxySQL</span><span style="color:var(--success);">? Operational</span></div>`;
                        } else if (vendorType === 'mssql') {
                            topoHtml = `<div style="position: relative; display: flex; justify-content: center;">
                            <svg width="200" height="120" viewBox="0 0 200 120">
                                <g transform="translate(80,35)">${hex} ${cG}/><text x="20" y="27" fill="white" font-size="12" font-weight="bold" text-anchor="middle">P</text></g>
                            </svg></div>
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span style="color:var(--success);">? Operational</span></div>`;
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
                            <div style="margin-top: 10px; font-size: 0.75rem; color: #9ca3af; display: flex; gap: 15px; justify-content: center;"><span>P - Primary</span><span>R - Replica</span><span>PB - PgBouncer</span><span>HA - HAProxy</span><span style="color:var(--success);">? Operational</span></div>`;
                        }
                        
                        topoContainer.innerHTML = topoHtml;

                        const rect = tr.getBoundingClientRect(); 
                        ct.style.display = 'block'; 
                        let topPos = rect.bottom + 5; 
                        if (topPos + 350 > window.innerHeight) topPos = rect.top - 350; 
                        ct.style.top = topPos + 'px'; 
                        ct.style.left = (rect.left + 50) + 'px'; 
                    } 
                };
                tr.onmouseleave = (e) => { tr.style.backgroundColor = 'transparent'; const ct = document.getElementById('cluster-hover-tooltip'); if (ct) ct.style.display = 'none'; };

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
                document.getElementById('cc-donut-center-text').style.color = donutCircle.style.stroke;
            }
            
            // Update Legend
            const warningCount = data.length - operationalCount;
            document.getElementById('cc-donut-legend').innerHTML = `
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--success);">● ${operationalCount} Operational</span>
                </div>
                ${warningCount > 0 ? `<div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: var(--warning);">● ${warningCount} Warning</span>
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
                let hexHtml = '<svg width="100%" height="200" viewBox="0 0 240 200"><defs><polygon id="hex" points="50,0 93,25 93,75 50,100 7,75 7,25" stroke="var(--glass-bg)" stroke-width="4" /></defs>';
                
                const positions = [
                    {x:10, y:20}, {x:96, y:20}, {x:53, y:95}, {x:139, y:95},
                    {x:182, y:20}, {x:225, y:95}, {x:10, y:170}, {x:96, y:170}
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
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})"><use href="#hex" fill="${node.color}" /></g>`;
                    
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
                
                document.querySelectorAll('.node-hex-hover').forEach(el => {
                    el.onmouseenter = (e) => {
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
                            
                            if (data.status === 'Shut Down') {
                                header.style.background = '#3b82f6';
                                msgBox.style.display = 'flex';
                                stat.innerHTML = '<span style="color:#3b82f6;">? Shut Down</span>';
                                document.getElementById('ntt-repl-col').style.display = 'block';
                            } else {
                                header.style.background = 'var(--success)';
                                msgBox.style.display = 'none';
                                stat.innerHTML = '<span style="color:var(--success);">? Operational</span>';
                                document.getElementById('ntt-repl-col').style.display = 'none';
                            }
                            
                            ntt.style.display = 'block';
                            const rect = el.getBoundingClientRect();
                            let topPos = rect.top - 200;
                            if (topPos < 0) topPos = rect.bottom + 10;
                            ntt.style.top = topPos + 'px';
                            ntt.style.left = Math.max(20, rect.left - 100) + 'px';
                        }
                    };
                    el.onmouseleave = (e) => {
                        const ntt = document.getElementById('node-hover-tooltip');
                        if (ntt) ntt.style.display = 'none';
                    };
                });
                
                document.getElementById('cc-total-nodes').innerText = allNodes.length + ' Nodes';
                const dnSlice = document.getElementById('nodes-donut-slice');
                if (dnSlice) {
                   if (allNodes.length === 0) dnSlice.style.strokeDashoffset = '439.8';
                   else {
                       const ratio = (allNodes.length - shutDownCount) / allNodes.length;
                       dnSlice.style.strokeDashoffset = 439.8 * (1 - ratio);
                   }
                }
                
                const nodeStats = document.getElementById('nodes-donut-slice').parentNode.parentNode.nextElementSibling;
                if (nodeStats) {
                    nodeStats.innerHTML = `<span style="color: var(--success);">? ${allNodes.length - shutDownCount} Operational</span><span style="color: var(--primary);">? ${shutDownCount} Shut Down</span>`;
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
            if(!res.ok) return;
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
    btnBackProjects.addEventListener('click', showProjectsView);

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


// Nodes Donut Tooltip
const nodesSvg = document.getElementById('nodes-donut-svg');
const tooltip = document.getElementById('custom-tooltip');
if (nodesSvg && tooltip) {
    nodesSvg.addEventListener('mousemove', (e) => {
        tooltip.style.display = 'block';
        tooltip.innerHTML = '4 Operational';
        tooltip.style.left = (e.pageX + 10) + 'px';
        tooltip.style.top = (e.pageY + 10) + 'px';
    });
    nodesSvg.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
    });
}


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
