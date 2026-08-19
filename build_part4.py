# -*- coding: utf-8 -*-
unified_html = """
                    <!-- Diagnostics Content -->
                    <div id="settings-content-diagnostics" class="settings-content-pane" style="display: none; padding: 40px; display: flex; flex-direction: column; align-items: center; color: #111827;">
                        <h2 style="font-size: 1.5rem; margin-bottom: 16px; font-weight: 500;">UI audit data collection</h2>
                        <p style="text-align: center; max-width: 600px; font-size: 0.9rem; color: #4b5563; line-height: 1.5; margin-bottom: 16px;">
                            Enable 'UI Audit Data Collection' to record and capture the necessary data while reproducing an issue in the user interface. Once the issue has been replicated, download the audit data for analysis.
                        </p>
                        <p style="text-align: center; max-width: 600px; font-size: 0.9rem; color: #4b5563; line-height: 1.5; margin-bottom: 16px;">
                            Remember to switch off the setting afterward to stop audit data collection.
                        </p>
                        <p style="text-align: center; max-width: 600px; font-size: 0.9rem; color: #4b5563; font-weight: 600; margin-bottom: 32px;">
                            Please, note that we are not collecting any personal data during this process.
                        </p>
                        
                        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 40px;">
                            <span style="font-size: 0.9rem;">UI audit data collection</span>
                            <div style="width: 40px; height: 20px; background: #d1d5db; border-radius: 10px; position: relative;">
                                <div style="width: 16px; height: 16px; background: white; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                            </div>
                            <button style="background: white; color: #9ca3af; border: 1px solid #e5e7eb; border-radius: 4px; padding: 6px 16px; font-size: 0.85rem; cursor: not-allowed; display: flex; align-items: center; gap: 8px;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg> download audit data
                            </button>
                        </div>
                        
                        <!-- Embedded Project Configuration from second view -->
                        <div style="border-top: 1px solid #e5e7eb; padding-top: 40px; width: 100%; max-width: 600px; text-align: left;">
                            <h3 style="font-size: 1.2rem; margin-bottom: 8px; color: #111827;">Project Configuration</h3>
                            <p style="color: #6b7280; font-size: 0.85rem; margin-bottom: 24px;">Buradan projelere özel senkronizasyon ve metrik ayarlarını değiştirebilirsiniz.</p>
                            
                            <div style="margin-bottom: 16px;">
                                <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Select Project</label>
                                <select id="setting-project-select" style="background: white; border: 1px solid #d1d5db; color: #111827; padding: 10px; border-radius: 4px; width: 100%; font-size: 0.9rem;">
                                    <option value="">Proje seçin...</option>
                                </select>
                            </div>

                            <div id="project-settings-container" style="display: none; margin-top: 24px;">
                                <div style="margin-bottom: 16px;">
                                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Max WAL Lag Threshold (MB)</label>
                                    <input type="number" id="setting-wal-lag" value="500" min="50" max="10000" style="background: white; border: 1px solid #d1d5db; color: #111827; padding: 10px; border-radius: 4px; width: 100%; font-size: 0.9rem;">
                                    <small style="color: #6b7280; display: block; margin-top: 6px; font-size: 0.75rem;">Eğer ana sunucu bu MB değerinden fazla WAL dosyası biriktirirse, yedek ile arasındaki bağ acil olarak koparılır.</small>
                                </div>
                                
                                <div style="margin-bottom: 16px;">
                                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Target Metric Table (Optional)</label>
                                    <input type="text" id="setting-metric-table" placeholder="e.g. vehicles, email_records" style="background: white; border: 1px solid #d1d5db; color: #111827; padding: 10px; border-radius: 4px; width: 100%; font-size: 0.9rem;">
                                    <small style="color: #6b7280; display: block; margin-top: 6px; font-size: 0.75rem;">Eğer belirtilirse Dashboard sadece bu tablodaki net (exact) veri sayısını okur. Boş bırakırsanız metrik sayılmaz.</small>
                                </div>
                                
                                <div style="margin-bottom: 16px;">
                                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Replication Tables (Optional)</label>
                                    <input type="text" id="setting-replication-tables" placeholder="e.g. vehicles, users" style="background: white; border: 1px solid #d1d5db; color: #111827; padding: 10px; border-radius: 4px; width: 100%; font-size: 0.9rem;">
                                    <small style="color: #6b7280; display: block; margin-top: 6px; font-size: 0.75rem;">Virgülle ayrılarak girilen tablolar yayınlanır (Publication). Boş bırakılırsa FOR ALL TABLES çalıştırılır (Superuser gerektirir).</small>
                                </div>
                                
                                <div style="margin-bottom: 16px; border-top: 1px solid #e5e7eb; padding-top: 16px;">
                                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Global Dashboard Update Interval (Seconds)</label>
                                    <input type="number" id="setting-update-interval" value="1" min="1" max="60" style="background: white; border: 1px solid #d1d5db; color: #111827; padding: 10px; border-radius: 4px; width: 100%; font-size: 0.9rem;">
                                    <small style="color: #6b7280; display: block; margin-top: 6px; font-size: 0.75rem;">Dashboard üzerindeki canlı metriklerin kaç saniyede bir güncelleneceğini belirler (Varsayılan: 1).</small>
                                </div>
                                
                                <button class="btn-primary" id="btn-save-settings" style="margin-top: 16px; background: #3a1c94; color: white; border: none; padding: 10px 20px; border-radius: 4px; font-size: 0.9rem; cursor: pointer;">Save Settings</button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    function switchSettingsTab(tabName) {
                        // Reset all tabs
                        document.querySelectorAll('.settings-tab').forEach(t => {
                            t.style.color = 'var(--text-main)';
                            t.style.borderBottom = 'none';
                            t.style.fontWeight = 'normal';
                        });
                        // Hide all contents
                        document.querySelectorAll('.settings-content-pane').forEach(c => {
                            c.style.display = 'none';
                        });
                        
                        // Active selected tab
                        const activeTab = document.getElementById('tab-' + tabName);
                        if (activeTab) {
                            activeTab.style.color = '#3a1c94';
                            activeTab.style.borderBottom = '2px solid #3a1c94';
                            activeTab.style.fontWeight = '500';
                        }
                        
                        // Show selected content
                        const activeContent = document.getElementById('settings-content-' + tabName);
                        if (activeContent) {
                            // If it's diagnostics, it uses flex layout initially but was hidden
                            if(tabName === 'profile' || tabName === 'cloud' || tabName === 'notifications' || tabName === 'diagnostics') {
                                activeContent.style.display = 'flex';
                            } else {
                                activeContent.style.display = 'block';
                            }
                        }
                    }
                </script>
            </div>
"""
with open('unified.part4', 'w', encoding='utf-8') as f:
    f.write(unified_html)
