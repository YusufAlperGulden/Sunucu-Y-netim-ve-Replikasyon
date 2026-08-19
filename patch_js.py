import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add tab listeners
tabs_logic = """
    // Cluster Detail Tabs
    document.querySelectorAll('.cluster-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.cluster-tab').forEach(t => {
                t.classList.remove('active');
                t.style.borderBottom = 'none';
                t.style.color = '#6b7280';
            });
            tab.classList.add('active');
            tab.style.borderBottom = '2px solid #6366f1';
            tab.style.color = '#6366f1';
            
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            const target = 'tab-content-' + tab.dataset.tab;
            const el = document.getElementById(target);
            if(el) el.style.display = 'block';
        });
    });
    
    // Node Subtabs
    document.querySelectorAll('.cluster-subtab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.cluster-subtab').forEach(t => {
                t.classList.remove('active');
                t.style.borderBottom = 'none';
                t.style.color = '#6b7280';
            });
            tab.classList.add('active');
            tab.style.borderBottom = '2px solid #6366f1';
            tab.style.color = '#6366f1';
            
            document.querySelectorAll('.subtab-content').forEach(c => c.style.display = 'none');
            const target = 'subtab-' + tab.dataset.subtab;
            const el = document.getElementById(target);
            if(el) el.style.display = 'block';
        });
    });
"""
if 'Cluster Detail Tabs' not in content:
    content = content.replace('// Routing logic', tabs_logic + '\n    // Routing logic')

# Now modify showDetailView
old_showDetailView = """        function showDetailView(proj) {
            currentProjectId = proj.id;
            document.getElementById('detail-proj-name').innerText = proj.name;
            document.getElementById('detail-proj-desc').innerText = proj.description || 'No description';"""

new_showDetailView = """        function showDetailView(proj) {
            currentProjectId = proj.id;
            document.getElementById('detail-proj-name').innerText = proj.name;
            document.getElementById('detail-proj-breadcrumb-name').innerText = proj.name + ' (ID: ' + proj.id + ')';
            """

content = content.replace(old_showDetailView, new_showDetailView)

# We need to fetch metrics immediately when showDetailView is called, to populate the new tables.
# Let's add a call to a new function `refreshClusterDetailMetrics()` at the end of showDetailView
if 'refreshClusterDetailMetrics();' not in content:
    content = content.replace("document.getElementById('nodes-container').innerHTML = hexHtml;", "document.getElementById('nodes-container').innerHTML = hexHtml;\n            refreshClusterDetailMetrics(proj);")

# And define refreshClusterDetailMetrics
metrics_logic = """
    let previousMetrics = {}; // to calculate TPS
    
    async function refreshClusterDetailMetrics(proj) {
        if (!proj) return;
        
        // Populate node list immediately with basic data
        const tbodyNode = document.querySelector('#node-list-table tbody');
        if (tbodyNode) {
            tbodyNode.innerHTML = proj.nodes.map(n => {
                const ip = n.url ? (n.url.split('@')[1] || '').split(':')[0] : 'Unknown';
                const port = n.url ? (n.url.split(':')[2] || '').split('/')[0] : '5432';
                return `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 0; color: #111827;">${n.name}</td>
                        <td style="padding: 10px 0;">${port}</td>
                        <td style="padding: 10px 0;">${ip}</td>
                        <td style="padding: 10px 0; color: #10b981;">&#8226; Operational</td>
                        <td style="padding: 10px 0; color: #6366f1;">PostgreSQL</td>
                        <td style="padding: 10px 0;">${n.role}</td>
                        <td style="padding: 10px 0;" id="nodelist-ver-${n.id}">Loading...</td>
                    </tr>
                `;
            }).join('');
            
            document.getElementById('stat-all').innerText = proj.nodes.length;
            document.getElementById('stat-operational').innerText = proj.nodes.length; // Simplified for now
        }
        
        try {
            const res = await apiFetch(`/api/projects/${proj.id}/metrics`);
            if (!res.ok) return;
            const metricsData = await res.json();
            
            const tbodyPg = document.querySelector('#pg-overview-table tbody');
            if (tbodyPg) {
                tbodyPg.innerHTML = '';
                
                metricsData.forEach(nodeData => {
                    const m = nodeData.metrics;
                    if (!m) return;
                    
                    // Update node list version
                    const verTd = document.getElementById(`nodelist-ver-${nodeData.id}`);
                    if(verTd) verTd.innerText = m.version || 'Unknown';
                    
                    // Calculate rates
                    let tps = 0, sel = 0, ins = 0, upd = 0, del = 0;
                    const now = Date.now();
                    const prev = previousMetrics[nodeData.id];
                    
                    if (prev && m.commits_raw !== undefined) {
                        const elapsed = (now - prev.time) / 1000;
                        if (elapsed > 0) {
                            const diffCommits = m.commits_raw - prev.commits_raw;
                            const diffRollbacks = m.rollbacks_raw - prev.rollbacks_raw;
                            tps = ((diffCommits + diffRollbacks) / elapsed).toFixed(2);
                            
                            sel = ((m.tup_fetched - prev.tup_fetched) / elapsed).toFixed(2);
                            ins = ((m.tup_inserted - prev.tup_inserted) / elapsed).toFixed(2);
                            upd = ((m.tup_updated - prev.tup_updated) / elapsed).toFixed(2);
                            del = ((m.tup_deleted - prev.tup_deleted) / elapsed).toFixed(2);
                        }
                    }
                    
                    // Save for next calculation
                    if (m.commits_raw !== undefined) {
                        previousMetrics[nodeData.id] = {
                            time: now,
                            commits_raw: m.commits_raw,
                            rollbacks_raw: m.rollbacks_raw,
                            tup_fetched: m.tup_fetched,
                            tup_inserted: m.tup_inserted,
                            tup_updated: m.tup_updated,
                            tup_deleted: m.tup_deleted
                        };
                    }
                    
                    const ip = "Unknown IP"; // Ideally from node url
                    const row = `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 0; color: #111827;">${nodeData.name}</td>
                            <td style="padding: 10px 0; color: #10b981;">Up</td>
                            <td style="padding: 10px 0;">${tps}</td>
                            <td style="padding: 10px 0;">${sel}</td>
                            <td style="padding: 10px 0;">${ins}</td>
                            <td style="padding: 10px 0;">${upd}</td>
                            <td style="padding: 10px 0;">${del}</td>
                            <td style="padding: 10px 0;">${m.connections || 0}</td>
                            <td style="padding: 10px 0; color: #10b981;">${m.active_conn || 0}</td>
                            <td style="padding: 10px 0; color: #10b981;">${m.cache_hit || '100%'}</td>
                        </tr>
                    `;
                    tbodyPg.innerHTML += row;
                });
            }
        } catch (e) {
            console.error(e);
        }
    }
"""

if 'async function refreshClusterDetailMetrics' not in content:
    content += '\n' + metrics_logic

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main.js")
