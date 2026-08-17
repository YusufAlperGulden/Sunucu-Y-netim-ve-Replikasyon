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
            document.getElementById(targetId).style.display = 'block';
            
            // If projects view is shown, ensure detail view is hidden
            if(targetId === 'projects-view') {
                showProjectsView();
                stopDashboardInterval();
            } else if (targetId === 'audit-logs-view') {
                fetchAuditLogs();
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
                projectsContainer.innerHTML = '<div class="loading-state">No projects found. Click + Add Project to start.</div>';
                return;
            }

            projectsContainer.innerHTML = '';
            data.forEach(proj => {
                const card = document.createElement('div');
                card.className = 'project-card glass-panel';
                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                        <h3 style="margin: 0; padding-right: 10px; word-break: break-all;">${escapeHTML(proj.name)}</h3>
                        <div style="display: flex; gap: 8px; flex-shrink: 0;">
                            <button class="icon-btn edit-proj-btn" style="position: static; padding: 6px; background: rgba(255,255,255,0.05); border-radius: 4px; border: 1px solid var(--border);" title="Edit Project">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </button>
                            <button class="icon-btn delete-proj-btn" style="position: static; padding: 6px; background: rgba(255,255,255,0.05); border-radius: 4px; border: 1px solid var(--border);" title="Delete Project">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--danger)"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                            </button>
                        </div>
                    </div>
                    <p>${escapeHTML(proj.description || 'No description provided')}</p>
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 15px;">Nodes: ${proj.nodesCount || 0}</div>
                `;
                card.addEventListener('click', async (e) => {
                    // Ignore clicks on action buttons
                    if(e.target.closest('button')) return;
                    
                    // Fetch full detail when clicked
                    const res = await apiFetch(`/api/projects/${proj.id}`);
                    const detailData = await res.json();
                    showDetailView(detailData);
                });
                
                // Add button listeners
                const editBtn = card.querySelector('.edit-proj-btn');
                editBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.getElementById('edit-proj-id').value = proj.id;
                    document.getElementById('edit-proj-name').value = proj.name;
                    document.getElementById('edit-proj-desc').value = proj.description || '';
                    modalEditProj.style.display = 'flex';
                });
                
                const delBtn = card.querySelector('.delete-proj-btn');
                delBtn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    if(confirm("Are you sure you want to delete this project? All associated nodes will be deleted permanently.")) {
                        try {
                            const res = await apiFetch(`/api/projects/${proj.id}`, { method: 'DELETE' });
                            if(res.ok) fetchProjects();
                            else alert("Failed to delete project");
                        } catch(err) {
                            alert("Error deleting project");
                        }
                    }
                });
                
                projectsContainer.appendChild(card);
            });
        } catch (error) {
            projectsContainer.innerHTML = `<div class="loading-state" style="color: var(--danger)">Error loading projects. Exception: ${escapeHTML(error.toString())}</div>`;
        }
    }

    async function refreshCurrentProject() {
        if (!currentProjectId) return;
        const res = await apiFetch(`/api/projects/${currentProjectId}`);
        const detailData = await res.json();
        renderNodes(detailData.nodes);
    }

    async function fetchAuditLogs() {
        const tbody = document.getElementById('logs-table-body');
        tbody.innerHTML = '<tr><td colspan="3" style="padding: 16px; text-align: center; color: var(--text-muted);">Loading logs...</td></tr>';
        try {
            const res = await apiFetch('/api/audit-logs');
            if (!res.ok) {
                const errText = await res.text();
                tbody.innerHTML = `<tr><td colspan="3" style="padding: 16px; text-align: center; color: var(--danger);">Failed to load logs. Server returned ${res.status}: ${escapeHTML(errText)}</td></tr>`;
                return;
            }
            const data = await res.json();
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" style="padding: 16px; text-align: center; color: var(--text-muted);">No audit logs found.</td></tr>';
                return;
            }
            tbody.innerHTML = '';
            data.forEach(log => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${escapeHTML(log.action)}</td>
                    <td style="color: var(--text-secondary);">${new Date(log.timestamp).toLocaleString()}</td>
                    <td style="color: var(--text-secondary);">${escapeHTML(log.details || '-')}</td>
                `;
                tbody.appendChild(row);
            });
        } catch (e) {
            tbody.innerHTML = `<tr><td colspan="3" style="padding: 16px; text-align: center; color: var(--danger);">Failed to load logs. Exception: ${escapeHTML(e.toString())}</td></tr>`;
        }
    }

    async function fetchDashboardMetrics() {
        let pid = currentProjectId;
        if (!pid) {
            try {
                const projRes = await apiFetch('/api/projects');
                if (!projRes.ok) return;
                const projs = await projRes.json();
                if (projs.length > 0) {
                    pid = projs[0].id;
                    currentProjectId = pid;
                } else {
                    return;
                }
            } catch (e) {
                return;
            }
        }
        
        try {
            const res = await apiFetch(`/api/projects/${pid}/metrics`);
            if(!res.ok) return;
            const dataList = await res.json();
            
            const container = document.getElementById('dashboard-metrics-container');
            if(!container) return;
            
            // clear loading state if it exists
            if (container.querySelector('.loading-state')) {
                container.innerHTML = '';
            }
            
            dataList.forEach(node => {
                let col = document.getElementById(`dash-node-${node.id}`);
                if(!col) {
                    // Create column dynamically
                    col = document.createElement('div');
                    col.className = 'metrics-column';
                    col.id = `dash-node-${node.id}`;
                    
                    const headerHtml = `
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 20px;">
                            <h2 style="margin: 0; font-size: 1.2rem;">${escapeHTML(node.name)} <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-muted);">(${escapeHTML(node.role)})</span></h2>
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
                            <div class="metric-card glass-panel"><div class="metric-label">Kayıtlı Araç Sayısı</div><div class="metric-val" id="metric-${node.id}-plates">-</div></div>
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
                
                // Update metrics
                const d = node.metrics;
                const prefix = node.id;
                
                if(!d || d.status !== 'online') {
                    document.getElementById(`metric-${prefix}-status`).className = 'status-badge status-offline';
                    document.getElementById(`metric-${prefix}-status`).innerText = 'Offline';
                } else {
                    document.getElementById(`metric-${prefix}-status`).className = 'status-badge status-online';
                    document.getElementById(`metric-${prefix}-status`).innerText = 'Aktif';
                    
                    document.getElementById(`metric-${prefix}-ping`).innerText = d.ping || '-';
                    document.getElementById(`metric-${prefix}-lag`).innerText = d.lag || '0ms';
                    document.getElementById(`metric-${prefix}-storage`).innerText = d.storage || '-';
                    document.getElementById(`metric-${prefix}-conn`).innerText = d.connections || '-';
                    document.getElementById(`metric-${prefix}-xact`).innerText = d.xact || '-';
                    document.getElementById(`metric-${prefix}-cache`).innerText = d.cache_hit || '-';
                    document.getElementById(`metric-${prefix}-uptime`).innerText = d.uptime || '-';
                    document.getElementById(`metric-${prefix}-version`).innerText = d.version || '-';
                    document.getElementById(`metric-${prefix}-plates`).innerText = d.plates || 'N/A';
                }
            });
            
        } catch (e) {
            console.error("Metrics error:", e);
        }
    }

    // --- EVENT LISTENERS ---
    
    // Modals
    btnAddProj.addEventListener('click', () => modalAddProj.style.display = 'flex');
    btnCloseProjModal.addEventListener('click', () => modalAddProj.style.display = 'none');
    btnOpenNodeModal.addEventListener('click', () => modalAddNode.style.display = 'flex');
    btnCloseNodeModal.addEventListener('click', () => modalAddNode.style.display = 'none');
    
    // Sync Modal specific
    const btnSyncRep = document.getElementById('btn-sync-replication');
    const modalSyncStatus = document.getElementById('modal-sync-status');
    const btnCloseSyncModal = document.getElementById('btn-close-sync-modal');
    
    if (btnSyncRep) {
        btnSyncRep.addEventListener('click', () => {
            modalSyncStatus.style.display = 'flex';
            const dataFlow = document.getElementById('sync-data-flow');
            if(dataFlow) {
                dataFlow.style.animation = 'dataFlowRight 1.5s infinite linear';
            }
        });
    }
    
    const btnSyncRepDashboard = document.getElementById('btn-sync-replication-dashboard');
    if (btnSyncRepDashboard) {
        btnSyncRepDashboard.addEventListener('click', () => {
            modalSyncStatus.style.display = 'flex';
            const dataFlow = document.getElementById('sync-data-flow');
            if(dataFlow) {
                dataFlow.style.animation = 'dataFlowRight 1.5s infinite linear';
            }
        });
    }

    if (btnCloseSyncModal) {
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
        
        btnSyncReplication.innerText = "Syncing...";
        btnSyncReplication.disabled = true;

        try {
            const response = await apiFetch(`/api/projects/${currentProjectId}/sync`, {
                method: 'POST'
            });
            const res = await response.json();
            
            if (response.ok && res.success) {
                alert("SUCCESS! " + res.message);
            } else {
                alert("ERROR: " + (res.message || "Sync failed."));
            }
        } catch (err) {
            alert('Server error during replication sync.');
        } finally {
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
                const res = await apiFetch(/api/projects//cleanup-slots, { method: 'POST' });
                const data = await res.json();
                if (res.ok && data.success) {
                    alert(data.message);
                    fetchAuditLogs();
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
        btnRefreshLogs.addEventListener('click', fetchAuditLogs);
    }

    // Button: Save Settings
    const btnSaveSettings = document.getElementById('btn-save-settings');
    const updateIntervalInput = document.getElementById('setting-update-interval');
    if (updateIntervalInput) {
        updateIntervalInput.value = localStorage.getItem('dashboard_update_interval_sec') || 1;
    }
    
    if(btnSaveSettings) {
        btnSaveSettings.addEventListener('click', async () => {
            const lagVal = document.getElementById('setting-wal-lag').value;
            const updateIntervalVal = updateIntervalInput ? updateIntervalInput.value : 1;
            localStorage.setItem('dashboard_update_interval_sec', updateIntervalVal);
            
            // If on dashboard view, restart interval
            if (document.getElementById('dashboard-view').style.display === 'block') {
                stopDashboardInterval();
                startDashboardInterval();
            }

            // Assuming saving to project ID 1 for demonstration if none selected
            const pid = currentProjectId || 1; 
            btnSaveSettings.innerText = "Saving...";
            try {
                const res = await apiFetch(`/api/settings/${pid}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({max_wal_lag_mb: parseInt(lagVal)})
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
        const token = btoa(u + ':' + p);
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




