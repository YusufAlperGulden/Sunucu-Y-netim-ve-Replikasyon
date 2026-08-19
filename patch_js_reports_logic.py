import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

reports_js = """
// --- OPERATIONAL REPORTS LOGIC ---
async function loadReports() {
    const tbody = document.querySelector('#table-reports tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="8" style="padding: 20px; text-align: center; color: #6b7280;">Loading reports...</td></tr>';
    
    try {
        const res = await apiFetch('/api/reports');
        if (res.ok) {
            const data = await res.json();
            if (data.length === 0) {
                tbody.innerHTML = '';
                document.querySelector('#table-reports > div').style.display = 'block'; // Show empty state
                document.querySelector('#table-reports table').style.display = 'none';
            } else {
                document.querySelector('#table-reports > div').style.display = 'none'; // Hide empty state
                document.querySelector('#table-reports table').style.display = 'table';
                
                tbody.innerHTML = '';
                data.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.created_at}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #3b82f6; font-weight: 500; cursor: pointer;">${r.file_name}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.report_type}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.cluster}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.created_by}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.data_range}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: #374151;">${r.recipients}</td>
                        <td style="padding: 12px 0; font-size: 0.85rem; color: var(--primary); cursor: pointer; font-weight: 500;">View</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }
    } catch (err) {
        console.error(err);
        tbody.innerHTML = '<tr><td colspan="8" style="padding: 20px; text-align: center; color: #ef4444;">Error loading reports</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btnSubmitReport = document.getElementById('btn-submit-report');
    if (btnSubmitReport) {
        btnSubmitReport.addEventListener('click', async () => {
            const clusterId = document.getElementById('report-cluster-select').value;
            const reportType = document.getElementById('report-type-select').value;
            const dataRange = document.getElementById('report-data-range').value;
            const recipients = document.getElementById('report-recipients').value;
            
            if (!clusterId || !reportType || !dataRange) {
                alert("Please fill in Cluster, Type, and Data range.");
                return;
            }
            
            btnSubmitReport.innerText = "Creating...";
            btnSubmitReport.disabled = true;
            
            try {
                const res = await apiFetch('/api/reports', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        project_id: parseInt(clusterId),
                        report_type: reportType,
                        data_range_days: parseInt(dataRange),
                        recipients: recipients
                    })
                });
                
                if (res.ok) {
                    document.getElementById('modal-create-report').style.display = 'none';
                    // Reset form
                    document.getElementById('report-cluster-select').value = '';
                    document.getElementById('report-type-select').value = '';
                    document.getElementById('report-recipients').value = '';
                    
                    loadReports();
                } else {
                    alert("Error creating report");
                }
            } catch (err) {
                console.error(err);
                alert("Error: " + err);
            }
            
            btnSubmitReport.innerText = "Create";
            btnSubmitReport.disabled = false;
        });
    }
});
"""

if "async function loadReports()" not in content:
    content += "\n" + reports_js
    
    # Let's also call loadReports() when user clicks on "Operational reports" sidebar link
    # The sidebar logic is: else if (viewId === 'reports-view') { ... }
    sidebar_hook = "} else if (viewId === 'reports-view') {"
    new_sidebar_hook = sidebar_hook + "\n            loadReports();"
    content = content.replace(sidebar_hook, new_sidebar_hook)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added reports JS logic")
else:
    print("Already exists")
