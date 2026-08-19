import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

nodes_js = """
// --- NODES PAGE MANAGEMENT ---
document.addEventListener('DOMContentLoaded', () => {
    const nodesPageData = [
        { host: 'br4-ccdemo-svr2', port: '3306', ip: '10.0.20.20', status: 'Operational', type: 'MariaDB', role: 'Primary', badge: {text: 'Writable', color: '#16a34a', bg: '#dcfce7'}, cluster: 'MariaDB (ID:21)', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', version: '11.8.6-MariaDB-ubu2404-log', seen: 'in 5 minutes' },
        { host: 'br4-ccdemo-svr3', port: '3306', ip: '10.0.20.21', status: 'Operational', type: 'MariaDB', role: 'Replica', badge: {text: 'Readonly', color: '#4b5563', bg: '#f3f4f6'}, cluster: 'MariaDB (ID:21)', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', version: '11.8.6 MariaDB ubu2404-log', seen: 'in 5 minutes' },
        { host: 'br4-ccdemo-svr1', port: '9600', ip: '10.0.20.19', status: 'Operational', type: 'HAProxy', role: 'None', badge: null, cluster: 'MariaDB (ID:21)', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', version: '2.8.16', seen: 'in 4 minutes' },
        { host: 'br4-ccdemo-svr2', port: '9600', ip: '10.0.20.20', status: 'Operational', type: 'HAProxy', role: 'None', badge: null, cluster: 'MariaDB (ID:21)', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', version: '2.8.16', seen: 'in 4 minutes' },
        { host: '10.10.20.103', port: '9090', ip: '10.10.20.103', status: 'Operational', type: 'Prometheus', role: 'None', badge: null, cluster: 'MariaDB (ID:21)', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', version: '2.53.5', seen: 'in 4 minutes' },
        { host: 'br8-ccdemo-svr1', port: '27017', ip: '10.0.20.36', status: 'Operational', type: 'MongoDB', role: 'Secondary', badge: null, cluster: 'MongoDB Replicaset (ID:30)', clusterLogo: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>', clusterColor: '#eab308', version: '8.0.21-9', seen: 'in 5 minutes' }
    ];

    function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';
        
        nodesPageData.forEach((n, i) => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--glass-border)';
            tr.style.background = 'white';
            
            let statusHtml = `<span style="color: var(--success); display: inline-flex; align-items: center; gap: 6px;"><div style="width: 6px; height: 6px; border-radius: 50%; background: var(--success);"></div> ${n.status}</span>`;
            
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
            `;
            tbody.appendChild(tr);
        });
    }

    renderNodesPage();
});

"""

content += nodes_js

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Nodes JS patched")
