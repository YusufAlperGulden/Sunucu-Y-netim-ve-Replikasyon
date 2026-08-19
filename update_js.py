import os

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add backupsData and schedulesData right before usersData
data_code = """
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
"""
content = content.replace('const usersData = [', data_code + '\nconst usersData = [')

# Add call to renderBackups() inside window.addEventListener('DOMContentLoaded')
init_code = """
    renderNodes();
    renderUsers();
    renderBackups();
"""
content = content.replace('renderNodes();\n    renderUsers();', init_code)

# Add event listeners for backups tabs
tabs_code = """
    // Settings Tabs
    window.switchSettingsTab = function(tabId) {
"""
backups_tabs = """
    // Backups Tabs
    const tabAllBackups = document.getElementById('tab-btn-all-backups');
    const tabSchedules = document.getElementById('tab-btn-schedules');
    const contentAllBackups = document.getElementById('content-all-backups');
    const contentSchedules = document.getElementById('content-schedules');

    if (tabAllBackups && tabSchedules) {
        tabAllBackups.addEventListener('click', () => {
            tabAllBackups.classList.add('active');
            tabAllBackups.style.color = '#3a1c94';
            tabAllBackups.style.borderBottom = '2px solid #3a1c94';
            tabSchedules.classList.remove('active');
            tabSchedules.style.color = '#4b5563';
            tabSchedules.style.borderBottom = '2px solid transparent';
            
            contentAllBackups.style.display = 'block';
            contentSchedules.style.display = 'none';
        });

        tabSchedules.addEventListener('click', () => {
            tabSchedules.classList.add('active');
            tabSchedules.style.color = '#3a1c94';
            tabSchedules.style.borderBottom = '2px solid #3a1c94';
            tabAllBackups.classList.remove('active');
            tabAllBackups.style.color = '#4b5563';
            tabAllBackups.style.borderBottom = '2px solid transparent';
            
            contentSchedules.style.display = 'block';
            contentAllBackups.style.display = 'none';
        });
    }

    // Settings Tabs
    window.switchSettingsTab = function(tabId) {
"""
content = content.replace(tabs_code, backups_tabs)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("JS updated.")
