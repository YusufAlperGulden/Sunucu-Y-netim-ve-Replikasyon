import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

backup_js = """
// --- BACKUP MODALS LOGIC ---
document.addEventListener('DOMContentLoaded', () => {
    const btnGlobalCreateBackup = document.getElementById('btn-global-create-backup');
    const modalBackupType = document.getElementById('modal-backup-type-select');
    const btnCloseBackupType = document.getElementById('btn-close-backup-type-modal');
    
    const btnBackupOnDemand = document.getElementById('btn-select-backup-ondemand');
    const btnBackupSchedule = document.getElementById('btn-select-backup-schedule');
    
    const modalBackupConfig = document.getElementById('modal-create-backup-config');
    const btnCloseBackupConfig = document.getElementById('btn-close-backup-config-modal');
    const btnBackupConfigBack = document.getElementById('btn-backup-config-back');
    const btnBackupConfigContinue = document.getElementById('btn-backup-config-continue');
    
    const selectCluster = document.getElementById('backup-config-cluster');
    const selectHost = document.getElementById('backup-config-host');
    
    let allProjectsForBackup = [];

    if (btnGlobalCreateBackup) {
        btnGlobalCreateBackup.addEventListener('click', () => {
            modalBackupType.style.display = 'flex';
        });
    }
    if (btnCloseBackupType) {
        btnCloseBackupType.addEventListener('click', () => {
            modalBackupType.style.display = 'none';
        });
    }
    
    const openConfigModal = async () => {
        modalBackupType.style.display = 'none';
        modalBackupConfig.style.display = 'flex';
        
        // Fetch projects to populate the select
        try {
            const res = await apiFetch('/api/projects');
            if (res.ok) {
                allProjectsForBackup = await res.json();
                selectCluster.innerHTML = '<option value="">Select a cluster...</option>' + 
                    allProjectsForBackup.map(p => `<option value="${p.id}">${p.name} (ID:${p.id})</option>`).join('');
            }
        } catch (e) {
            console.error("Failed to load clusters for backup:", e);
        }
    };
    
    if (btnBackupOnDemand) btnBackupOnDemand.addEventListener('click', openConfigModal);
    if (btnBackupSchedule) btnBackupSchedule.addEventListener('click', openConfigModal);
    
    if (btnCloseBackupConfig) btnCloseBackupConfig.addEventListener('click', () => modalBackupConfig.style.display = 'none');
    if (btnBackupConfigBack) {
        btnBackupConfigBack.addEventListener('click', () => {
            modalBackupConfig.style.display = 'none';
            modalBackupType.style.display = 'flex';
        });
    }
    
    if (selectCluster) {
        selectCluster.addEventListener('change', (e) => {
            const pid = parseInt(e.target.value);
            if (!pid) {
                selectHost.innerHTML = '<option value="">Select a cluster first...</option>';
                selectHost.disabled = true;
                return;
            }
            const proj = allProjectsForBackup.find(p => p.id === pid);
            if (proj && proj.nodes && proj.nodes.length > 0) {
                selectHost.innerHTML = proj.nodes.map(n => {
                    const hostUrl = n.url ? n.url.split('@')[1] || n.url : 'Unknown';
                    const role = n.role ? (n.role.charAt(0).toUpperCase() + n.role.slice(1)) : 'Unknown';
                    return `<option value="${n.id}">${n.name} - ${hostUrl} (${role})</option>`;
                }).join('');
                selectHost.disabled = false;
            } else {
                selectHost.innerHTML = '<option value="">No nodes found in this cluster</option>';
                selectHost.disabled = true;
            }
        });
    }
    
    if (btnBackupConfigContinue) {
        btnBackupConfigContinue.addEventListener('click', () => {
            const clusterVal = selectCluster.value;
            const hostVal = selectHost.value;
            if (!clusterVal || !hostVal) {
                alert("Please select a Cluster and Backup host first.");
                return;
            }
            
            // Per user request, show honest error message
            alert("Error: Cloud Storage (AWS S3) is not configured. Local disk backups are disabled.");
        });
    }
});
"""

if 'btnGlobalCreateBackup' not in content:
    content += '\n' + backup_js

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.js with backup logic")
