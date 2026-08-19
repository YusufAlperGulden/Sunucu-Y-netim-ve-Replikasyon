import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderNodes to use node.ip, node.port etc.
old_render_nodes_table = """            if(tbody) {
                // Find matching data in nodesPageData if exists
                let nData = (typeof nodesPageData !== 'undefined') ? nodesPageData.find(nd => nd.host === node.name) : null;
                
                let ip = nData ? nData.ip : 'N/A';
                let port = nData ? nData.port : '5432';
                let status = nData ? nData.status : 'Operational';
                let type = nData ? nData.type : 'PostgreSQL';
                let version = nData ? nData.version : '16.4';
                let seen = nData ? nData.seen : 'in 1 minute';"""

new_render_nodes_table = """            if(tbody) {
                let ip = node.ip || 'N/A';
                let port = node.port || '5432';
                let status = node.status || 'Operational';
                let type = node.type || 'PostgreSQL';
                let version = node.version || '16.4';
                let seen = 'in 1 minute';"""

content = content.replace(old_render_nodes_table, new_render_nodes_table)

# 2. Update renderNodesPage to fetch real nodes
old_render_nodes_page = r'function renderNodesPage\(\) \{[\s\S]*?\}\s*\}'

new_render_nodes_page = """async function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 40px; color: #9ca3af;">Loading nodes...</td></tr>';
        
        try {
            const res = await apiFetch('/api/projects');
            if(!res.ok) throw new Error("Failed to fetch");
            const projects = await res.json();
            
            // Extract all nodes from projects
            let allNodes = [];
            
            // Fetch detail for each project to get IP and Port
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
    }"""

content = re.sub(old_render_nodes_page, new_render_nodes_page, content, flags=re.DOTALL)

# Delete the nodesPageData array completely!
content = re.sub(r'const nodesPageData = \[[\s\S]*?\];', '', content)

# Bump version to v=13
content = content.replace('v=12', 'v=13')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
html_content = html_content.replace('v=12', 'v=13')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Removed nodesPageData and updated JS to use real nodes.")
