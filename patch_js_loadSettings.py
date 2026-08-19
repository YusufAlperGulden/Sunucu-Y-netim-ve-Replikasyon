import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the async function loadSettings
old_load = r'async function loadSettings\(\) \{.*?\n        \} catch\(e\) \{\s*tbody\.innerHTML =.*?\n        \}\s*\}'

new_load = """let currentSettingsCategory = 'Backup';
    async function loadSettings(category = null) {
        if (!currentProjectId) return;
        if (category) currentSettingsCategory = category;
        
        const tbody = document.getElementById('settings-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="3" style="padding: 20px; text-align: center; color: #6b7280;">Loading...</td></tr>';
        
        try {
            const res = await apiFetch(`/api/projects/${currentProjectId}/settings`);
            const data = res.ok ? await res.json() : {};
            
            tbody.innerHTML = '';
            
            let filteredDefs = settingsDefs.filter(d => d.category === currentSettingsCategory);
            
            if (filteredDefs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" style="padding: 40px; text-align: center; color: #9ca3af;">No settings available in this category.</td></tr>';
                return;
            }
            
            filteredDefs.forEach(def => {
                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--border)';
                
                let val = data[def.key];
                if (val === undefined || val === null) val = '';
                
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

content = re.sub(old_load, new_load, content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated loadSettings")
