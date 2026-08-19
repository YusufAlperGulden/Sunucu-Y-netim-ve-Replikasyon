# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_data = """    const nodesPageData = [
        { host: 'plaka-master-node', port: '5432', ip: '192.168.1.10', status: 'Operational', type: 'PostgreSQL', role: 'Primary', badge: {text: 'Writable', color: '#16a34a', bg: '#dcfce7'}, cluster: 'Arac Plaka Takip Sistemi', clusterLogo: '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>', clusterColor: '#3b82f6', version: '16.2', seen: 'in 1 minute' },
        { host: 'plaka-replica-node', port: '5432', ip: '192.168.1.11', status: 'Operational', type: 'PostgreSQL', role: 'Replica', badge: {text: 'Readonly', color: '#4b5563', bg: '#f3f4f6'}, cluster: 'Arac Plaka Takip Sistemi', clusterLogo: '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>', clusterColor: '#3b82f6', version: '16.2', seen: 'in 1 minute' },
        { host: 'email-master-node', port: '3306', ip: '10.0.0.50', status: 'Operational', type: 'MariaDB', role: 'Primary', badge: {text: 'Writable', color: '#16a34a', bg: '#dcfce7'}, cluster: 'E-mail Okuma Programi', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', clusterColor: '#1f2937', version: '11.4', seen: 'in 2 minutes' },
        { host: 'email-replica-node', port: '3306', ip: '10.0.0.51', status: 'Operational', type: 'MariaDB', role: 'Replica', badge: {text: 'Readonly', color: '#4b5563', bg: '#f3f4f6'}, cluster: 'E-mail Okuma Programi', clusterLogo: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>', clusterColor: '#1f2937', version: '11.4', seen: 'in 2 minutes' }
    ];"""

start_idx = content.find('    const nodesPageData = [')
end_idx = content.find('    ];', start_idx) + 6

content = content[:start_idx] + new_data + content[end_idx:]

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS mock data patched")
