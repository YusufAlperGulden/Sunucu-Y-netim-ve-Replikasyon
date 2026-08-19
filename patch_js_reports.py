import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

switch_reports_tab_js = """
// Reports Tab Switching
function switchReportsTab(tabName) {
    const tabReports = document.getElementById('tab-reports-sub');
    const tabSchedules = document.getElementById('tab-schedules-sub');
    const tableReports = document.getElementById('table-reports');
    const tableSchedules = document.getElementById('table-schedules');
    const btnAction = document.getElementById('btn-create-report-action');
    const textAction = document.getElementById('text-create-report-action');
    const modalTitle = document.getElementById('modal-create-report-title');

    if (tabName === 'reports') {
        tabReports.style.color = 'var(--primary)';
        tabReports.style.borderBottomColor = 'var(--primary)';
        tabSchedules.style.color = 'var(--text-muted)';
        tabSchedules.style.borderBottomColor = 'transparent';
        
        tableReports.style.display = 'block';
        tableSchedules.style.display = 'none';
        
        textAction.innerText = 'Create report';
        modalTitle.innerText = 'Generate new report';
    } else {
        tabSchedules.style.color = 'var(--primary)';
        tabSchedules.style.borderBottomColor = 'var(--primary)';
        tabReports.style.color = 'var(--text-muted)';
        tabReports.style.borderBottomColor = 'transparent';
        
        tableSchedules.style.display = 'block';
        tableReports.style.display = 'none';
        
        textAction.innerText = 'Create schedule';
        modalTitle.innerText = 'Generate new schedule';
    }
}
"""

if "function switchReportsTab" not in content:
    content += "\n" + switch_reports_tab_js
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added switchReportsTab function")
else:
    print("Already exists")
