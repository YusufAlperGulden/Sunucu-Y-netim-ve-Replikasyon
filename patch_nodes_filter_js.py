import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# First, let's update the status of some nodes in our mock data to make filtering more interesting.
# Right now they are all 'Operational'. Let's make one 'Shut Down' to test.
content = content.replace(
    "{ host: 'br4-ccdemo-svr1', port: '9600', ip: '10.0.20.19', status: 'Operational', type: 'HAProxy'",
    "{ host: 'br4-ccdemo-svr1', port: '9600', ip: '10.0.20.19', status: 'Shut Down', type: 'HAProxy'"
)
content = content.replace(
    "{ host: 'br4-ccdemo-svr2', port: '9600', ip: '10.0.20.20', status: 'Operational', type: 'HAProxy'",
    "{ host: 'br4-ccdemo-svr2', port: '9600', ip: '10.0.20.20', status: 'Shut Down', type: 'HAProxy'"
)

# Now, we need to add the filtering logic to main.js
filter_logic = """
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

    function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';
        
        const filteredData = nodesPageData.filter(n => currentFilter === 'All' || n.status === currentFilter);
        
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
"""

# Replace the old renderNodesPage function
start_idx = content.find('    function renderNodesPage() {')
end_idx = content.find('    renderNodesPage();', start_idx)

content = content[:start_idx] + filter_logic + "\n" + content[end_idx:]

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS patched")
