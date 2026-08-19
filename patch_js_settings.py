import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

settings_js = """
    // --- SETTINGS TAB LOGIC ---
    const settingsDefs = [
        { key: 'backup_cloud_retention', desc: 'Setting of how many days to keep the backups uploaded to a cloud. Backups matching retention period are removed.' },
        { key: 'backup_create_checksum', desc: 'Configures cmon if it has to calculate checksum (md5sum) on the created backup files and verify them.' },
        { key: 'backup_delete_all_job_max_reattempts', desc: 'Max number of attempts on DELETE_ALL_BACKUPS jobs it can be triggered on cluster drop operation.' },
        { key: 'backup_delete_all_job_min_delay_on_reattempts', desc: 'Delay between attempts on DELETE_ALL_BACKUPS jobs it can be triggered on cluster drop operation.' },
        { key: 'backup_encryption_key', desc: 'The AES encryption key to encrypt backups. The format of the string is base64 encoded.' },
        { key: 'backup_n_safety_copies', desc: 'Setting of how many completed full backups will be kept regardless of their retention status.' },
        { key: 'backup_post_script', desc: 'This script is executed after the backup happens, but after a candidate has been elected.' },
        { key: 'backup_pre_script', desc: 'This script is executed before the backup happens, but after a candidate has been elected.' },
        { key: 'backup_retention', desc: 'Setting of how many days to keep the backups. Backups matching retention period are removed.' },
        { key: 'backup_subdir', desc: 'Set the name of the backup subdirectory. This string may hold standard %X field separators.' },
        { key: 'backup_user', desc: 'The username of the database account used for managing backups.' },
        { key: 'backup_user_password', desc: 'The database password for backup user.' },
        { key: 'backupdir', desc: 'The default backup directory, to be pre-filled in Frontend.' },
        { key: 'clud_part_size_mb', desc: 'Part size (in MB) for multipart uploads of backups to cloud storage with clud.' },
        { key: 'clud_timeout', desc: 'Timeout (in seconds) for interrupting cloud operations when no progress.' },
        { key: 'datadir_backup_path', desc: 'During restore/rebuild operations a backup of the existing datadir may be performed.' },
        { key: 'disable_backup_email', desc: 'This setting controls if emails are sent or not if a backup finished or failed.' },
        { key: 'netcat_port', desc: 'List of netcat ports and port ranges used to stream backups.' },
        { key: 'pgbackrest_cipher_pass', desc: 'The AES key to be used to encrypt backup repository of PgBackRest.' },
        { key: 'pgbackrest_cipher_type', desc: 'Cipher to be used to encrypt backup repository of PgBackRest.' },
        { key: 'pgbackrest_repo_hostname', desc: 'The name of the repository host where to save backup data of PgBackRest.' },
        { key: 'pgbackrest_repo_path', desc: 'The path of the repository directory where to save backup data of PgBackRest.' },
        { key: 'pgbackrest_stanza_name', desc: 'The name of the stanza to be used to save and restore backups of the cluster.' },
        { key: 'pitr_retention_hours', desc: 'Retention hours (to erase old WAL archive logs) for PITR.' }
    ];

    async function loadSettings() {
        if (!currentProjectId) return;
        const tbody = document.getElementById('settings-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="3" style="padding: 20px; text-align: center; color: #6b7280;">Loading...</td></tr>';
        
        try {
            const res = await apiFetch(`/api/projects/${currentProjectId}/settings`);
            const data = res.ok ? await res.json() : {};
            
            tbody.innerHTML = '';
            
            settingsDefs.forEach(def => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--border)';
                
                let val = data[def.key];
                if (val === undefined || val === null) val = '';
                
                // Truncate long descriptions or mask passwords
                let displayVal = escapeHTML(String(val));
                if (def.key.includes('password') || def.key.includes('encryption_key') || def.key.includes('cipher_pass')) {
                    displayVal = val ? '**********' : '';
                }
                
                tr.innerHTML = `
                    <td style="padding: 12px 20px; font-size: 0.85rem; color: #374151;">${def.key}</td>
                    <td style="padding: 12px 20px; font-size: 0.85rem; color: #374151; min-width: 150px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                            <span>${displayVal}</span>
                            <span class="edit-setting-icon" style="cursor: pointer; color: var(--primary);" title="Edit">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </span>
                        </div>
                    </td>
                    <td style="padding: 12px 20px; font-size: 0.8rem; color: #6b7280; max-width: 400px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${def.desc}">${def.desc}</td>
                `;
                
                const editIcon = tr.querySelector('.edit-setting-icon');
                editIcon.addEventListener('click', async () => {
                    const newVal = prompt(`Edit value for ${def.key}:\\n\\n${def.desc}`, val);
                    if (newVal !== null && newVal !== val) {
                        try {
                            const updateRes = await apiFetch(`/api/projects/${currentProjectId}/settings`, {
                                method: 'PUT',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ [def.key]: newVal })
                            });
                            if (updateRes.ok) {
                                loadSettings();
                            } else {
                                alert("Failed to save setting");
                            }
                        } catch (err) {
                            alert("Error saving setting: " + err);
                        }
                    }
                });
                
                tbody.appendChild(tr);
            });
            
        } catch(e) {
            tbody.innerHTML = '<tr><td colspan="3" style="padding: 20px; text-align: center; color: #ef4444;">Error loading settings.</td></tr>';
        }
    }
"""

if "function loadSettings" not in content:
    insert_marker = "// --- TAB LOGIC ---"
    content = content.replace(insert_marker, settings_js + "\n    " + insert_marker)
    
    # Trigger loadSettings when settings tab is clicked
    old_tab_click = """                    if (targetEl) targetEl.style.display = 'block';"""
    new_tab_click = """                    if (targetEl) targetEl.style.display = 'block';
                    if (tab.dataset.tab === 'settings') {
                        loadSettings();
                    }"""
    content = content.replace(old_tab_click, new_tab_click)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added settings JS logic")
else:
    print("loadSettings already exists")
