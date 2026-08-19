import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

users_js = """
// --- USERS MANAGEMENT ---
document.addEventListener('DOMContentLoaded', () => {
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

"""

content += users_js

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS patched")
