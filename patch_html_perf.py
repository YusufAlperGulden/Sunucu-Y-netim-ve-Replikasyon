import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_perf = """<div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280; font-size: 0.95rem; line-height: 1.6;">
Real OS metrics (CPU, RAM, Disk I/O) cannot be fetched directly from PostgreSQL (port 5432).<br><br>
<strong>How to enable this:</strong><br>
1. SSH into your database servers as root.<br>
2. Install Prometheus Node Exporter: <code>sudo apt install prometheus-node-exporter</code><br>
3. Start the service: <code>sudo systemctl start prometheus-node-exporter</code><br>
4. Ensure port 9100 is open in your firewall.<br>
<br>
<em>Once installed on your servers, this dashboard will automatically detect the OS metrics. No fake placeholder data is being drawn.</em>
</div>"""

new_perf = """<div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280; font-size: 0.95rem; line-height: 1.6;">
<h3 style="color: var(--primary); margin-bottom: 15px;">Real OS Metrics Enabled!</h3>
Gerçek CPU ve RAM kullanımı, sisteme entegre edilen <b>SSH Worker (paramiko)</b> sayesinde doğrudan Linux çekirdeğinden (top & free komutlarıyla) anlık olarak çekilmektedir.<br><br>
Görmek için Sunucularınıza geçerli bir SSH IP, Port, Username ve Password/PEM girilmiş olması yeterlidir.<br><br>
Anlık metrikler "Dashboards" sekmesindeki kartlarda saniyede bir güncellenmektedir.
</div>"""

content = content.replace(old_perf, new_perf)

# bump version
content = content.replace('v=28', 'v=29')
new_changelog = """<li><span style="font-weight: 600;">Feature:</span> Gerçek OS Metrikleri (CPU ve RAM) eklendi! Önceden sahte verilerle gösterilen veya "Veri alınamıyor" denilen CPU/RAM kullanımı, artık SSH altyapısı sayesinde arka planda <code>top</code> ve <code>free</code> komutları çalıştırılarak doğrudan Linux sunucularından anlık çekiliyor. SSH bilgisi girilmiş her sunucunun metrikleri Dashboard ekranında listelenir.</li>
"""
pattern = r'(<h3[^>]*>What\'s New</h3>\s*<ul[^>]*>\s*)'
content = re.sub(pattern, r'\g<1>' + new_changelog, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML perf message and changelog")

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
js_content = js_content.replace('v=28', 'v=29')
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
