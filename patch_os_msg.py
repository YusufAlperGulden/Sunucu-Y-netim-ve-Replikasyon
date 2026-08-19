import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_msg = "Real OS metrics unavailable (Requires Prometheus Node Exporter agent installed on servers). No fake placeholder data is being drawn."
new_msg = """
Real OS metrics (CPU, RAM, Disk I/O) cannot be fetched directly from PostgreSQL (port 5432).<br><br>
<strong>How to enable this:</strong><br>
1. SSH into your database servers as root.<br>
2. Install Prometheus Node Exporter: <code>sudo apt install prometheus-node-exporter</code><br>
3. Start the service: <code>sudo systemctl start prometheus-node-exporter</code><br>
4. Ensure port 9100 is open in your firewall.<br>
<br>
<em>Once installed on your servers, this dashboard will automatically detect the OS metrics. No fake placeholder data is being drawn.</em>
"""
content = content.replace(old_msg, new_msg)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated OS metrics message")
