import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Routing Fix
old_routing_1 = """        if (hash === 'projects-view') {"""
new_routing_1 = """        if (hash === 'project-detail-view') {
            document.querySelectorAll('.view-section').forEach(section => section.style.display = 'none');
            const dv = document.getElementById('project-detail-view');
            if(dv) dv.style.display = 'block';
        } else if (hash === 'projects-view') {"""
if "if (hash === 'project-detail-view')" not in content:
    content = content.replace(old_routing_1, new_routing_1)

old_routing_2 = """    function showDetailView(proj) {
        projectsContainer.style.display = 'none';
        detailView.style.display = 'block';"""
new_routing_2 = """    function showDetailView(proj) {
        window.location.hash = 'project-detail-view';
        projectsContainer.style.display = 'none';
        const clustersView = document.getElementById('clusters-view');
        if (clustersView) clustersView.style.display = 'none';
        detailView.style.display = 'block';"""
if "window.location.hash = 'project-detail-view';" not in content:
    content = content.replace(old_routing_2, new_routing_2)

old_routing_3 = """    btnBackProjects.addEventListener('click', () => { window.location.hash = 'projects-view'; });"""
new_routing_3 = """    btnBackProjects.addEventListener('click', () => { window.location.hash = 'clusters-view'; });"""
if "hash = 'clusters-view';" not in content:
    content = content.replace(old_routing_3, new_routing_3)

# 2. Nodes Data Fix (Remove nodesPageData and fetch real nodes)
# We need to replace the entire renderNodesPage function and remove nodesPageData
if "const nodesPageData =" in content:
    content = re.sub(r'const nodesPageData = \[.*?\];', '', content, flags=re.DOTALL)
    
    old_render_nodes = r'async function renderNodesPage\(\) \{.*?\}\s*renderNodesPage\(\);'
    new_render_nodes = """async function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 40px; color: #6b7280; font-size: 0.9rem;">Loading...</td></tr>';
        
        try {
            const res = await apiFetch('/api/projects');
            if(!res.ok) throw new Error("API err");
            const projects = await res.json();
            
            let allNodes = [];
            for(let p of projects) {
                try {
                    const detailRes = await apiFetch(`/api/projects/${p.id}`);
                    if(detailRes.ok) {
                        const detail = await detailRes.json();
                        detail.nodes.forEach(n => {
                            allNodes.push({
                                ...n,
                                cluster: p.name,
                                clusterLogo: '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>',
                                clusterColor: '#3b82f6',
                                seen: 'in 1 minute'
                            });
                        });
                    }
                } catch(e) {}
            }
            
            let filteredData = allNodes.filter(n => currentFilter === 'All' || n.status === currentFilter);
            
            if (filteredData.length === 0) {
                tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: #9ca3af; font-size: 0.9rem;">There are no nodes found in the database.</td></tr>`;
                return;
            }
            
            tbody.innerHTML = '';
            filteredData.forEach((n, i) => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--glass-border)';
                tr.style.background = 'white';
                
                let statusColor = 'var(--success)';
                let dotColor = 'var(--success)';
                if (n.status === 'Shut Down') { statusColor = '#3b82f6'; dotColor = '#3b82f6'; }
                if (n.status === 'Failed') { statusColor = '#ef4444'; dotColor = '#ef4444'; }
                
                let statusHtml = `<span style="color: ${statusColor}; display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: ${dotColor};"></div> ${n.status || 'Operational'}</span>`;
                
                let typeColor = '#059669'; // Greenish
                let t = n.type || 'PostgreSQL';
                if (t === 'HAProxy') typeColor = '#8b5cf6'; // Purple
                if (t === 'Prometheus') typeColor = '#eab308'; // Yellow
                if (t === 'MariaDB') typeColor = '#1f2937'; // Yellow
                
                let roleHtml = `<span>${n.role}</span>`;
                if (n.role && n.role.toLowerCase() === 'primary') {
                    roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #dcfce7; color: #16a34a; border: 1px solid #16a34a; margin-left: 6px;">Writable</span>`;
                } else if(n.role) {
                    roleHtml += ` <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #f3f4f6; color: #4b5563; border: 1px solid #4b5563; margin-left: 6px;">Readonly</span>`;
                }
                
                let logoColor = n.clusterColor || '#1f2937';
                
                tr.innerHTML = `
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.name}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.port || '5432'}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.ip || 'N/A'}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; white-space: nowrap;">${statusHtml}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: ${typeColor}; white-space: nowrap;">${t}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; display: flex; align-items: center;">${roleHtml}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">
                        <span style="display: inline-flex; align-items: center; gap: 8px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${logoColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${n.clusterLogo}</svg>
                            ${n.cluster}
                        </span>
                    </td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.version || '16.4'}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap;">${n.seen}</td>
                    <td style="padding: 16px 16px; font-size: 0.85rem; color: var(--text-main); white-space: nowrap; text-align: center;">
                        <button style="background: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px 12px; cursor: pointer;">...</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } catch(e) {
            tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 40px; color: #ef4444; font-size: 0.9rem;">Error fetching nodes</td></tr>`;
        }
    }

    renderNodesPage();"""
    content = re.sub(old_render_nodes, new_render_nodes, content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Re-applied routing and node decryption fixes")
