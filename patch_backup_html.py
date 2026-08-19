import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make the 'Create backup' button have an ID
btn_pattern = r'<button class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px;">\s*<svg[^>]*>.*?</svg>\s*Create backup\s*</button>'
replacement = '''<button id="btn-global-create-backup" class="btn-primary" style="background: #3a1c94; color: white; display: flex; align-items: center; gap: 8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                    Create backup
                </button>'''

if 'id="btn-global-create-backup"' not in content:
    content = re.sub(btn_pattern, replacement, content, flags=re.DOTALL)

# Add Modals before </body>
modals_html = """
<!-- Modal: Backup Type Selection -->
<div class="modal-overlay" id="modal-backup-type-select" style="display: none; align-items: center; justify-content: center;">
    <div class="modal-content" style="max-width: 700px; width: 100%; padding: 40px; border-radius: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <div></div> <!-- Spacer -->
            <h2 style="font-size: 1.5rem; font-weight: 500; text-align: center; flex-grow: 1;">Create backup</h2>
            <button class="btn-close-modal" id="btn-close-backup-type-modal" style="background: none; border: none; cursor: pointer; font-size: 1.2rem; color: #9ca3af;">✕</button>
        </div>
        <p style="text-align: center; color: #4b5563; margin-bottom: 32px;">Create backups on-demand or schedule backups to run at specific times.</p>
        
        <div style="display: flex; flex-direction: column; gap: 16px;">
            <!-- Option 1 -->
            <div id="btn-select-backup-ondemand" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; display: flex; gap: 20px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#3a1c94'; this.style.boxShadow='0 4px 6px rgba(0,0,0,0.05)';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none';">
                <div style="color: #3a1c94;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                </div>
                <div>
                    <h3 style="margin: 0 0 8px 0; font-size: 1.1rem; color: #111827;">Backup on Demand</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #4b5563; font-size: 0.9rem; line-height: 1.5;">
                        <li>Create a single backup instantly</li>
                        <li>Store backups on premise or in the cloud</li>
                        <li>Compress and encrypt backups for secure storage</li>
                    </ul>
                </div>
            </div>
            
            <!-- Option 2 -->
            <div id="btn-select-backup-schedule" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; display: flex; gap: 20px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#3a1c94'; this.style.boxShadow='0 4px 6px rgba(0,0,0,0.05)';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none';">
                <div style="color: #3a1c94;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line><path d="M12 14v4"></path><path d="M10 16h4"></path></svg>
                </div>
                <div>
                    <h3 style="margin: 0 0 8px 0; font-size: 1.1rem; color: #111827;">Schedule a Backup</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #4b5563; font-size: 0.9rem; line-height: 1.5;">
                        <li>Define a schedule to periodically create backups</li>
                        <li>Store backups on premise or in the cloud</li>
                        <li>Compress and encrypt backups for secure storage</li>
                        <li>Automate backup verification</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal: Create a Backup Configuration -->
<div class="modal-overlay" id="modal-create-backup-config" style="display: none; align-items: center; justify-content: center;">
    <div class="modal-content" style="max-width: 800px; width: 100%; border-radius: 12px; padding: 0; display: flex; flex-direction: column;">
        
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #e5e7eb;">
            <h2 style="font-size: 1.1rem; font-weight: 600; margin: 0; color: #111827;">Create a Backup</h2>
            <button class="btn-close-modal" id="btn-close-backup-config-modal" style="background: none; border: none; cursor: pointer; font-size: 1.2rem; color: #9ca3af;">✕</button>
        </div>
        
        <!-- Body (Sidebar + Content) -->
        <div style="display: flex; flex-grow: 1; min-height: 400px;">
            <!-- Left Sidebar -->
            <div style="width: 200px; border-right: 1px solid #e5e7eb; padding: 24px;">
                <div style="display: flex; flex-direction: column; gap: 24px;">
                    <div style="display: flex; align-items: center; gap: 12px; color: #3a1c94; font-weight: 500;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; background: #3a1c94; color: white; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;">1</div>
                        Configuration
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; color: #9ca3af;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; border: 1px solid #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;">2</div>
                        Advanced settings
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; color: #9ca3af;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; border: 1px solid #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;">3</div>
                        Storage
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; color: #9ca3af;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; border: 1px solid #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;">4</div>
                        Preview
                    </div>
                </div>
            </div>
            
            <!-- Right Content -->
            <div style="flex-grow: 1; padding: 24px;">
                <h3 style="margin: 0 0 24px 0; font-size: 1.1rem; color: #111827;">Configuration</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; color: #374151;"><span style="color: red;">*</span> Cluster</label>
                        <select id="backup-config-cluster" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; outline: none;">
                            <option value="">Select a cluster...</option>
                        </select>
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; color: #374151;"><span style="color: red;">*</span> Backup host</label>
                        <select id="backup-config-host" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; outline: none;" disabled>
                            <option value="">Select a cluster first...</option>
                        </select>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; color: #374151;"><span style="color: red;">*</span> Backup method</label>
                        <select id="backup-config-method" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; outline: none;">
                            <option value="pg_dump">pg_dump</option>
                            <option value="pg_basebackup">pg_basebackup</option>
                        </select>
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; color: #374151;"><span style="color: red;">*</span> Dump type</label>
                        <select id="backup-config-dumptype" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; outline: none;">
                            <option value="schema_data">Schema And Data</option>
                            <option value="schema_only">Schema Only</option>
                            <option value="data_only">Data Only</option>
                        </select>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; justify-content: space-between; border-top: 1px solid #f3f4f6; padding-top: 24px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 0.9rem; color: #374151;">Upload backup to cloud</span>
                        <!-- Fake Toggle Switch -->
                        <div style="width: 44px; height: 24px; background: #e5e7eb; border-radius: 12px; position: relative; cursor: not-allowed; opacity: 0.7;" title="Requires S3 integration">
                            <div style="width: 20px; height: 20px; background: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.2);"></div>
                            <span style="position: absolute; right: 6px; top: 4px; font-size: 10px; color: #9ca3af; font-weight: bold;">Off</span>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
        
        <!-- Footer -->
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; border-top: 1px solid #e5e7eb; background: #f9fafb; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">
            <div style="font-size: 0.8rem; color: #ef4444;">* Required</div>
            <div style="display: flex; gap: 12px;">
                <button id="btn-backup-config-back" style="padding: 8px 16px; background: white; border: 1px solid #d1d5db; border-radius: 6px; color: #374151; cursor: pointer;">Back</button>
                <button id="btn-backup-config-continue" style="padding: 8px 24px; background: #3a1c94; border: none; border-radius: 6px; color: white; font-weight: 500; cursor: pointer;">Continue</button>
            </div>
        </div>
        
    </div>
</div>
"""

if 'id="modal-backup-type-select"' not in content:
    content = content.replace('</body>', modals_html + '\n</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html with backup modals")
