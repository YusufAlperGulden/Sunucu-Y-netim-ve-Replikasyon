import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Also add offline error message to the metric cards
old_offline_block = """} else if(m && m.status === 'offline') {
                          document.getElementById("metric-" + node.id + "-status").className = 'status-badge status-offline';"""

# Check if there's already offline handling
if "m.status === 'offline'" not in content:
    # Find where the if block ends (after all metric updates) and add else clause
    old_cpu_update = '''{ const TMP_EL = document.getElementById("metric-" + node.id + "-uptime"); if(TMP_EL) { TMP_EL.innerText = m.uptime || "N/A"; } }'''
    new_cpu_update = '''{ const TMP_EL = document.getElementById("metric-" + node.id + "-uptime"); if(TMP_EL) { TMP_EL.innerText = m.uptime || "N/A"; } }
                      } else if (m && m.status === 'offline') {
                          const statusEl = document.getElementById("metric-" + node.id + "-status");
                          if(statusEl) { statusEl.className = 'status-badge status-offline'; statusEl.innerText = 'Çevrimdışı'; }
                          const errMsg = m.error || 'Bağlantı kurulamadı';
                          ['cpu','ram','ping','lag','storage','conn','xact','plates','cache','uptime'].forEach(k => {
                              const el = document.getElementById("metric-" + node.id + "-" + k);
                              if(el) el.innerText = '-';
                          });'''
    content = content.replace(old_cpu_update, new_cpu_update)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added offline handling")
else:
    print("Offline handling already exists")
