import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the end of fetchProjects where projects data is rendered, and add logic to populate the report dropdown.
# Inside fetchProjects:
marker = "document.getElementById('total-clusters').innerText = projects.length;"
insert_code = """
            // Populate report cluster dropdown
            const reportSelect = document.getElementById('report-cluster-select');
            if (reportSelect) {
                reportSelect.innerHTML = '<option value="">Select cluster</option>';
                projects.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p.id;
                    opt.innerText = `${p.name} (ID:${p.id})`;
                    reportSelect.appendChild(opt);
                });
            }
"""

if "reportSelect.innerHTML" not in content:
    content = content.replace(marker, marker + "\n" + insert_code)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added cluster population to fetchProjects")
else:
    print("Already added")
