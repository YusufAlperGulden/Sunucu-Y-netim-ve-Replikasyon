import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# After the "version" update, add cpu/ram/plates/uptime updates
OLD = '''{ const TMP_EL = document.getElementById("metric-" + node.id + "-version"); if(TMP_EL) {                         TMP_EL.innerText = m.version; } }'''

NEW = '''{ const TMP_EL = document.getElementById("metric-" + node.id + "-version"); if(TMP_EL) { TMP_EL.innerText = m.version; } }
                          { const TMP_EL = document.getElementById("metric-" + node.id + "-cpu"); if(TMP_EL) { TMP_EL.innerText = m.cpu_usage || "N/A"; } }
                          { const TMP_EL = document.getElementById("metric-" + node.id + "-ram"); if(TMP_EL) { TMP_EL.innerText = m.ram_usage || "N/A"; } }
                          { const TMP_EL = document.getElementById("metric-" + node.id + "-plates"); if(TMP_EL) { TMP_EL.innerText = m.row_count !== undefined ? m.row_count.toLocaleString() : "N/A"; } }
                          { const TMP_EL = document.getElementById("metric-" + node.id + "-uptime"); if(TMP_EL) { TMP_EL.innerText = m.uptime || "N/A"; } }'''

if "metric-\" + node.id + \"-cpu\"" not in content:
    content = content.replace(OLD, NEW)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added cpu/ram/plates/uptime DOM updates")
else:
    print("Already present")
