import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_metrics_html = """                        const metricsHtml = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-${node.id}-ping">-</div></div>"""

new_metrics_html = """                        const metricsHtml = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="metric-card glass-panel"><div class="metric-label">CPU Kullanımı</div><div class="metric-val" id="metric-${node.id}-cpu" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">RAM Kullanımı</div><div class="metric-val" id="metric-${node.id}-ram" style="color: var(--primary);">-</div></div>
                                <div class="metric-card glass-panel"><div class="metric-label">Ağ Gecikmesi (Ping)</div><div class="metric-val" id="metric-${node.id}-ping">-</div></div>"""

if old_metrics_html in content:
    content = content.replace(old_metrics_html, new_metrics_html)
    print("Added CPU/RAM html to main.js")
else:
    print("Could not find old_metrics_html")

# Now update the assignment
old_assign = """                        document.getElementById(`metric-${node.id}-ping`).innerText = `${metrics.ping_ms} ms`;"""
new_assign = """                        document.getElementById(`metric-${node.id}-cpu`).innerText = metrics.cpu_usage || 'N/A';
                        document.getElementById(`metric-${node.id}-ram`).innerText = metrics.ram_usage || 'N/A';
                        document.getElementById(`metric-${node.id}-ping`).innerText = `${metrics.ping_ms} ms`;"""
content = content.replace(old_assign, new_assign)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated js assignment")
