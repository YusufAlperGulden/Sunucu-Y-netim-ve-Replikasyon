import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_render_nodes = r'function renderNodes\(nodes\) \{.*?\n    \}'

new_render_nodes = """function renderNodes(nodes) {
        const tbody = document.querySelector('#node-list-table tbody');
        if (tbody) tbody.innerHTML = '';
        
        if (!nodes || nodes.length === 0) {
            if(nodesContainer) nodesContainer.innerHTML = '<div class="loading-state">No nodes added yet.</div>';
            if(tbody) tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 20px; color: #6b7280;">No nodes found</td></tr>';
            
            // Reset stats
            ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown', 'all'].forEach(id => {
                const el = document.getElementById('stat-' + id);
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

        // Update stats
        ['operational', 'failed', 'offline', 'shutdown', 'recovering', 'unknown'].forEach(id => {
            const el = document.getElementById('stat-' + id);
            let val = 0;
            if (id === 'operational') val = stats['Operational'];
            if (id === 'failed') val = stats['Failed'];
            if (id === 'offline') val = stats['Offline'];
            if (id === 'shutdown') val = stats['Shut Down'];
            if (id === 'recovering') val = stats['Recovering'];
            if (id === 'unknown') val = stats['Unknown State'];
            if (el) el.innerText = val;
        });
        const elAll = document.getElementById('stat-all');
        if (elAll) elAll.innerText = nodes.length;
    }"""

content = re.sub(old_render_nodes, new_render_nodes, content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated renderNodes in main.js")
