js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Find function boundaries
old_fn_start = js.find('window.fetchNodesPage = async function fetchNodesPage()')
depth = 0
in_fn = False
found_end = -1
for pos in range(old_fn_start, min(old_fn_start + 8000, len(js))):
    c = js[pos]
    if c == '{':
        depth += 1
        in_fn = True
    elif c == '}':
        depth -= 1
        if in_fn and depth == 0:
            found_end = pos + 1
            break

NEW_FN = """window.fetchNodesPage = async function fetchNodesPage() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#9ca3af;">Yukleniyor...</td></tr>';

    // Reset stats to loading state
    ['stat-operational','stat-failed','stat-offline','stat-shutdown','stat-recovering','stat-unknown','stat-all'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = '-';
    });

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Projeler yuklenemedi.</td></tr>';
            return;
        }
        const projects = await res.json();

        // Flatten all nodes from all projects
        const allNodes = [];
        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                allNodes.push({ node, proj });
            }
        }

        // Update stat counters immediately
        const statOp = document.getElementById('stat-operational');
        const statAll = document.getElementById('stat-all');
        if (statOp) statOp.innerText = allNodes.length;
        if (statAll) statAll.innerText = allNodes.length;
        ['stat-failed','stat-offline','stat-shutdown','stat-recovering','stat-unknown'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = '0';
        });

        if (allNodes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:40px;color:#9ca3af;">Cluster ekleyip node tanimlayin.</td></tr>';
            return;
        }

        // Render rows immediately without waiting for metrics
        tbody.innerHTML = '';
        allNodes.forEach(({ node, proj }) => {
            const roleLower = (node.role || '').toLowerCase();
            const isWritable = roleLower === 'primary';
            const statusColor = 'var(--success)';
            const roleLabel = node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown';
            const roleExtra = isWritable
                ? '<span style="font-size:0.7rem;padding:2px 6px;border-radius:4px;background:#dcfce7;color:#16a34a;border:1px solid #16a34a;margin-left:6px;">Writable</span>'
                : '<span style="font-size:0.7rem;padding:2px 6px;border-radius:4px;background:#f3f4f6;color:#4b5563;border:1px solid #4b5563;margin-left:6px;">Readonly</span>';

            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid #f3f4f6';
            tr.setAttribute('data-node-id', node.id);
            tr.innerHTML = `
                <td style="padding:12px 16px;font-size:0.85rem;color:var(--text-main);white-space:nowrap;">${escapeHTML(node.name)}</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#6b7280;">5432</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#9ca3af;" id="nd-ip-${node.id}">N/A</td>
                <td style="padding:12px 16px;font-size:0.85rem;white-space:nowrap;">
                    <span style="color:${statusColor};display:inline-flex;align-items:center;gap:6px;" id="nd-status-${node.id}">
                        <div style="width:6px;height:6px;border-radius:50%;background:${statusColor};"></div>Operational
                    </span>
                </td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#059669;">PostgreSQL</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:var(--text-main);display:flex;align-items:center;">${escapeHTML(roleLabel)}${roleExtra}</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#6b7280;">${escapeHTML(proj.name)} (ID:${proj.id})</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#9ca3af;" id="nd-ver-${node.id}">-</td>
                <td style="padding:12px 16px;font-size:0.85rem;color:#9ca3af;" id="nd-seen-${node.id}">Az once</td>
                <td style="padding:12px 16px;text-align:center;"><button style="padding:4px 10px;font-size:0.75rem;border:1px solid #e5e7eb;border-radius:4px;cursor:pointer;background:white;">...</button></td>
            `;
            tbody.appendChild(tr);
        });

        // Now fetch metrics in background to fill in version/status
        for (const proj of projects) {
            if (!proj.nodes || proj.nodes.length === 0) continue;
            try {
                const mr = await apiFetch('/api/projects/' + proj.id + '/metrics');
                if (!mr.ok) continue;
                const nodeMetrics = await mr.json();
                for (const nm of nodeMetrics) {
                    const m = nm.metrics;
                    if (!m) continue;
                    const statusEl = document.getElementById('nd-status-' + nm.id);
                    const verEl = document.getElementById('nd-ver-' + nm.id);
                    if (m.status === 'online') {
                        if (statusEl) statusEl.innerHTML = '<div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div> Operational';
                        if (verEl) verEl.innerText = m.version || '-';
                    } else if (m.status === 'offline') {
                        if (statusEl) {
                            statusEl.style.color = '#6b7280';
                            statusEl.innerHTML = '<div style="width:6px;height:6px;border-radius:50%;background:#6b7280;"></div> Offline';
                        }
                    }
                }
            } catch(e) { /* ignore metric errors */ }
        }

    } catch(e) {
        console.error('fetchNodesPage error:', e);
        if(tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Hata: ' + escapeHTML(String(e)) + '</td></tr>';
    }
}"""

new_js = js[:old_fn_start] + NEW_FN + js[found_end:]
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_js)
print(f"Replaced fetchNodesPage: {found_end - old_fn_start} -> {len(NEW_FN)} bytes")
