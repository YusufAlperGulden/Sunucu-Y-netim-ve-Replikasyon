import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace everything between <div id="project-detail-view" style="display: none;"> and </div> <!-- End of project-detail-view -->
old_block = re.search(r'<div id="project-detail-view" style="display: none;">(.*?)</div> <!-- End of project-detail-view -->', content, re.DOTALL)
if not old_block:
    print("Could not find project-detail-view block")
    exit(1)

new_block = """<div id="project-detail-view" style="display: none;">
    <div style="background: white; border-bottom: 1px solid var(--border); padding: 10px 24px;">
        <div style="font-size: 13px; color: #6b7280; display: flex; align-items: center; gap: 8px;">
            <span>Home</span> / <span>Clusters</span> / <span id="detail-proj-breadcrumb-name" style="font-weight: 500; color: #374151;">Project Name (ID: 1)</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <h1 id="detail-proj-name" style="font-size: 1.25rem; font-weight: 600; margin: 0; color: #111827;">Project Name</h1>
                <span id="sync-status-badge" style="display: none; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: rgba(0,0,0,0.05); border: 1px solid var(--border);"></span>
                <span style="font-size: 12px; color: #10b981; display: flex; align-items: center; gap: 4px;"><div style="width:6px;height:6px;border-radius:50%;background:#10b981;"></div> Operational</span>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <button class="btn-primary" id="btn-edit-project-detail" style="background: white; border: 1px solid var(--border); color: #374151;">Edit Project</button>
                <button class="btn-primary" id="btn-open-node-modal" style="background: white; border: 1px solid var(--border); color: #374151;">+ Add Node</button>
                <button class="btn-primary" id="btn-sync-replication" style="background: #e5e7eb; color: #374151; border: none;">Actions...</button>
            </div>
        </div>
        
        <div class="cluster-tabs" style="display: flex; gap: 20px; margin-top: 20px; font-size: 14px;">
            <a href="#cluster-tab-dashboards" class="cluster-tab active" data-tab="dashboards">Dashboards</a>
            <a href="#cluster-tab-nodes" class="cluster-tab" data-tab="nodes">Nodes</a>
            <a href="#cluster-tab-performance" class="cluster-tab" data-tab="performance">Performance</a>
            <a href="#cluster-tab-backups" class="cluster-tab" data-tab="backups">Backups</a>
            <a href="#cluster-tab-alarms" class="cluster-tab" data-tab="alarms">Alarms</a>
            <a href="#cluster-tab-jobs" class="cluster-tab" data-tab="jobs">Jobs</a>
            <a href="#cluster-tab-logs" class="cluster-tab" data-tab="logs">Logs</a>
            <a href="#cluster-tab-reports" class="cluster-tab" data-tab="reports">Reports</a>
            <a href="#cluster-tab-manage" class="cluster-tab" data-tab="manage">Manage</a>
            <a href="#cluster-tab-settings" class="cluster-tab" data-tab="settings">Settings</a>
        </div>
    </div>
    
    <div style="padding: 24px; background: #f9fafb; min-height: calc(100vh - 150px);">
        <!-- TAB: DASHBOARDS -->
        <div id="tab-content-dashboards" class="tab-content active">
            <div class="glass-panel" style="padding: 20px; background: white; border: 1px solid var(--border); margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <select style="padding: 6px 12px; border-radius: 4px; border: 1px solid var(--border); font-size: 14px;"><option>Cluster Overview</option></select>
                    <div style="display: flex; gap: 10px;">
                        <button style="padding: 6px 12px; border-radius: 4px; border: 1px solid var(--border); background: white;">last 15 minutes</button>
                    </div>
                </div>
                
                <h3 style="font-size: 14px; font-weight: 500; margin-bottom: 10px; color: #374151;">Cluster Load (OS Metrics)</h3>
                <div style="height: 150px; background: #f9fafb; border: 1px dashed #d1d5db; display: flex; align-items: center; justify-content: center; color: #6b7280; font-size: 13px;">
                    Real OS metrics unavailable (Requires Prometheus Node Exporter agent installed on servers). No fake placeholder data is being drawn.
                </div>
            </div>
            
            <div class="glass-panel" style="padding: 20px; background: white; border: 1px solid var(--border); margin-bottom: 24px;">
                <h3 style="font-size: 14px; font-weight: 500; margin-bottom: 15px; color: #374151;">PostgreSQL Overview (Real Data)</h3>
                <div style="overflow-x: auto;">
                    <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 13px;" id="pg-overview-table">
                        <thead style="color: #6b7280; border-bottom: 1px solid var(--border);">
                            <tr>
                                <th style="padding: 10px 0; font-weight: 500;">Instance</th>
                                <th style="padding: 10px 0; font-weight: 500;">Status</th>
                                <th style="padding: 10px 0; font-weight: 500;">TPS</th>
                                <th style="padding: 10px 0; font-weight: 500;">SELECT/s</th>
                                <th style="padding: 10px 0; font-weight: 500;">INSERT/s</th>
                                <th style="padding: 10px 0; font-weight: 500;">UPDATE/s</th>
                                <th style="padding: 10px 0; font-weight: 500;">DELETE/s</th>
                                <th style="padding: 10px 0; font-weight: 500;">Connections</th>
                                <th style="padding: 10px 0; font-weight: 500;">Active Connections</th>
                                <th style="padding: 10px 0; font-weight: 500;">Cache Hit Ratio</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Populated via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                <!-- Real OS metrics unavailable blocks -->
                <div class="glass-panel" style="padding: 20px; background: white; border: 1px solid var(--border);">
                    <h3 style="font-size: 14px; font-weight: 500; margin-bottom: 15px; color: #374151;">Load average 1m</h3>
                    <div style="height: 100px; display: flex; align-items: center; justify-content: center; color: #9ca3af; font-size: 12px; text-align: center; border: 1px dashed #e5e7eb;">OS Metrics Unavailable<br/>(No Placeholder)</div>
                </div>
                <div class="glass-panel" style="padding: 20px; background: white; border: 1px solid var(--border);">
                    <h3 style="font-size: 14px; font-weight: 500; margin-bottom: 15px; color: #374151;">Memory available</h3>
                    <div style="height: 100px; display: flex; align-items: center; justify-content: center; color: #9ca3af; font-size: 12px; text-align: center; border: 1px dashed #e5e7eb;">OS Metrics Unavailable<br/>(No Placeholder)</div>
                </div>
                <div class="glass-panel" style="padding: 20px; background: white; border: 1px solid var(--border);">
                    <h3 style="font-size: 14px; font-weight: 500; margin-bottom: 15px; color: #374151;">Network TX</h3>
                    <div style="height: 100px; display: flex; align-items: center; justify-content: center; color: #9ca3af; font-size: 12px; text-align: center; border: 1px dashed #e5e7eb;">OS Metrics Unavailable<br/>(No Placeholder)</div>
                </div>
            </div>
        </div>
        
        <!-- TAB: NODES -->
        <div id="tab-content-nodes" class="tab-content" style="display: none;">
            <div class="glass-panel" style="padding: 24px; background: white; border: 1px solid var(--border);">
                <div class="cluster-subtabs" style="display: flex; gap: 20px; font-size: 14px; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 20px;">
                    <a href="#node-list" class="cluster-subtab active" data-subtab="nodelist" style="color: #6366f1; border-bottom: 2px solid #6366f1; padding-bottom: 10px; margin-bottom: -11px;">Node list</a>
                    <a href="#topology" class="cluster-subtab" data-subtab="topology" style="color: #6b7280; padding-bottom: 10px; margin-bottom: -11px;">Topology</a>
                </div>
                
                <div id="subtab-nodelist" class="subtab-content active">
                    <div style="display: flex; gap: 10px; margin-bottom: 20px; overflow-x: auto;">
                        <div style="padding: 15px 25px; border: 1px solid var(--border); border-radius: 4px; border-left: 2px solid #10b981; min-width: 120px;">
                            <div style="color: #6b7280; font-size: 12px;">Operational</div>
                            <div style="color: #10b981; font-size: 24px;" id="stat-operational">0</div>
                        </div>
                        <div style="padding: 15px 25px; border: 1px solid var(--border); border-radius: 4px; min-width: 120px;">
                            <div style="color: #6b7280; font-size: 12px;">Failed</div>
                            <div style="color: #374151; font-size: 24px;" id="stat-failed">0</div>
                        </div>
                        <div style="padding: 15px 25px; border: 1px solid var(--border); border-radius: 4px; border-color: #8b5cf6; min-width: 120px;">
                            <div style="color: #6b7280; font-size: 12px;">All</div>
                            <div style="color: #374151; font-size: 24px;" id="stat-all">0</div>
                        </div>
                    </div>
                    
                    <div style="overflow-x: auto;">
                        <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 13px;" id="node-list-table">
                            <thead style="color: #6b7280; border-bottom: 1px solid var(--border);">
                                <tr>
                                    <th style="padding: 10px 0; font-weight: 500;">Hostname</th>
                                    <th style="padding: 10px 0; font-weight: 500;">Port</th>
                                    <th style="padding: 10px 0; font-weight: 500;">IP</th>
                                    <th style="padding: 10px 0; font-weight: 500;">Status</th>
                                    <th style="padding: 10px 0; font-weight: 500;">Type</th>
                                    <th style="padding: 10px 0; font-weight: 500;">Role</th>
                                    <th style="padding: 10px 0; font-weight: 500;">Version</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Populated via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div id="subtab-topology" class="subtab-content" style="display: none;">
                    <div id="nodes-container" style="margin-top: 20px;">
                        <!-- Old topology code gets populated here -->
                    </div>
                </div>
            </div>
        </div>

        <!-- OTHER TABS (EMPTY STATES) -->
        <div id="tab-content-alarms" class="tab-content" style="display: none;">
            <div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                <div style="color: #6b7280; font-size: 14px;">You haven't received alarms yet. When you do, it'll show up here.</div>
            </div>
        </div>
        
        <div id="tab-content-jobs" class="tab-content" style="display: none;">
            <div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                <div style="color: #6b7280; font-size: 14px;">You haven't created jobs yet. When you do, it'll show up here.</div>
            </div>
        </div>
        
        <div id="tab-content-reports" class="tab-content" style="display: none;">
            <div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="2" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                <div style="color: #6b7280; font-size: 14px;">You haven't created reports yet. When you do, it'll show up here.</div>
            </div>
        </div>
        
        <div id="tab-content-performance" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Performance data unavailable.</div></div>
        <div id="tab-content-backups" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Backups data unavailable.</div></div>
        <div id="tab-content-logs" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Logs data unavailable.</div></div>
        <div id="tab-content-manage" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Management options unavailable.</div></div>
        <div id="tab-content-settings" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Settings unavailable.</div></div>

    </div>
</div>"""

content = content.replace(old_block.group(0), new_block)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
