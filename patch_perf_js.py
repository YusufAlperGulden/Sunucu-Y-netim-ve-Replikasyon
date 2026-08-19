with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

perf_js_code = """
    // PERFORMANCE MODULE HANDLERS
    window.perfData = null;

    window.switchPerfSubtab = function(e, subtabName) {
        if(e) e.preventDefault();
        
        document.querySelectorAll('.perf-subtabs .perf-subtab').forEach(el => {
            el.style.color = '#6b7280';
            el.style.borderBottom = '2px solid transparent';
            el.classList.remove('active');
        });
        
        const activeSubtab = document.querySelector(`.perf-subtabs [data-subtab="${subtabName}"]`);
        if (activeSubtab) {
            activeSubtab.style.color = 'var(--primary)';
            activeSubtab.style.borderBottom = '2px solid var(--primary)';
            activeSubtab.classList.add('active');
        }
        
        document.querySelectorAll('.perf-subtab-content').forEach(el => el.style.display = 'none');
        const targetContent = document.getElementById(`perf-subtab-${subtabName}`);
        if(targetContent) targetContent.style.display = 'block';
    };

    window.fetchPerformanceData = async function() {
        if (!currentProjectId) return;
        try {
            const res = await apiFetch(`/api/projects/${currentProjectId}/performance`);
            if (!res.ok) return;
            const data = await res.json();
            window.perfData = data;
            
            // 1. Render Status Variables (Primary & Standby comparison)
            const tbodyStatus = document.getElementById('perf-status-tbody');
            if (tbodyStatus && data.variables) {
                if (data.variables.length === 0) {
                    tbodyStatus.innerHTML = '<tr><td colspan="3" style="padding:30px;text-align:center;color:#9ca3af;">No variables available.</td></tr>';
                } else {
                    tbodyStatus.innerHTML = data.variables.map(v => `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 16px; font-weight: 500; color: #374151; font-family: monospace;">${escapeHTML(v.name.toUpperCase())}</td>
                            <td style="padding: 10px 16px; color: #10b981; font-family: monospace;">${escapeHTML(v.setting)} ${escapeHTML(v.unit)}</td>
                            <td style="padding: 10px 16px; color: #6366f1; font-family: monospace;">${escapeHTML(v.setting)} ${escapeHTML(v.unit)}</td>
                        </tr>
                    `).join('');
                }
            }
            
            // 2. Render Variables table
            const tbodyVars = document.getElementById('perf-vars-tbody');
            if (tbodyVars && data.variables) {
                tbodyVars.innerHTML = data.variables.map(v => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 16px; font-weight: 500; color: #374151; font-family: monospace;">${escapeHTML(v.name)}</td>
                        <td style="padding: 10px 16px; color: #1f2937; font-family: monospace;">${escapeHTML(v.setting)}</td>
                        <td style="padding: 10px 16px; color: #6b7280;">${escapeHTML(v.unit || '-')}</td>
                        <td style="padding: 10px 16px; color: #4b5563; font-size: 0.82rem;">${escapeHTML(v.desc || '')}</td>
                    </tr>
                `).join('');
            }
            
            // 3. Render Query Monitor
            const tbodyQueries = document.getElementById('perf-query-tbody');
            if (tbodyQueries && data.queries) {
                if (data.queries.length === 0) {
                    tbodyQueries.innerHTML = '<tr><td colspan="6" style="padding:30px;text-align:center;color:#9ca3af;">No active long-running queries.</td></tr>';
                } else {
                    tbodyQueries.innerHTML = data.queries.map(q => `
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 10px 16px; font-family: monospace;">${q.pid}</td>
                            <td style="padding: 10px 16px;">${escapeHTML(q.user || '-')}</td>
                            <td style="padding: 10px 16px; color: #6b7280;">${escapeHTML(q.client || 'local')}</td>
                            <td style="padding: 10px 16px;"><span class="status-badge status-online">${escapeHTML(q.state)}</span></td>
                            <td style="padding: 10px 16px; font-family: monospace;">${escapeHTML(q.duration)}</td>
                            <td style="padding: 10px 16px; font-family: monospace; font-size: 0.8rem; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHTML(q.query)}</td>
                        </tr>
                    `).join('');
                }
            }
            
            // 4. Render Schema Analyzer
            const tbodySchema = document.getElementById('perf-schema-tbody');
            if (tbodySchema && data.schema) {
                tbodySchema.innerHTML = data.schema.map(s => `
                    <tr style="border-bottom: 1px solid var(--border);">
                        <td style="padding: 10px 16px; font-weight: 500; font-family: monospace; color: #374151;">${escapeHTML(s.table_name)}</td>
                        <td style="padding: 10px 16px; color: #6b7280;">${s.col_count} columns</td>
                        <td style="padding: 10px 16px; font-weight: 500; color: #1f2937;">${s.row_count.toLocaleString()} rows</td>
                        <td style="padding: 10px 16px;"><span class="status-badge status-online">OK</span></td>
                    </tr>
                `).join('');
            }
            
        } catch(e) {
            console.error("fetchPerformanceData error:", e);
        }
    };

    window.filterPerfStatusTable = function() {
        const query = (document.getElementById('perf-status-search')?.value || '').toLowerCase();
        document.querySelectorAll('#perf-status-tbody tr').forEach(row => {
            const txt = row.innerText.toLowerCase();
            row.style.display = txt.includes(query) ? '' : 'none';
        });
    };

    window.filterPerfVarsTable = function() {
        const query = (document.getElementById('perf-vars-search')?.value || '').toLowerCase();
        document.querySelectorAll('#perf-vars-tbody tr').forEach(row => {
            const txt = row.innerText.toLowerCase();
            row.style.display = txt.includes(query) ? '' : 'none';
        });
    };
"""

# Append performance handlers and hook into cluster tabs click
if 'window.fetchPerformanceData' not in js:
    js = js + "\n\n" + perf_js_code

# Hook performance tab click
old_tab_click = "if (tab === 'dashboards') {"
new_tab_click = "if (tab === 'performance') { window.fetchPerformanceData(); } if (tab === 'dashboards') {"
if old_tab_click in js:
    js = js.replace(old_tab_click, new_tab_click, 1)

# Update Changelog anchors and asset version
js = js.replace("changelogAnchors = ['v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=60', 'v=61')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with Performance module and v1.5.4 (v61)")
