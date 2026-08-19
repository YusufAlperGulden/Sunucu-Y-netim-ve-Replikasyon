with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add Auto-Login / Auto-Data fetch on DOMContentLoaded
old_login_bottom = """    loginBtn.addEventListener('click', attemptLogin);
    loginPassword.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') attemptLogin();
    });
    loginUsername.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loginPassword.focus();
    });"""

new_login_bottom = """    loginBtn.addEventListener('click', attemptLogin);
    loginPassword.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') attemptLogin();
    });
    loginUsername.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loginPassword.focus();
    });

    // Auto-authenticate & immediately fetch global clusters if token exists
    if (globalAuthToken) {
        if (loginScreen) loginScreen.style.display = 'none';
        fetchProjects();
        fetchRecentAlarms();
    }"""

if old_login_bottom in js:
    js = js.replace(old_login_bottom, new_login_bottom, 1)
    print("Added auto-authenticate & global fetchProjects on startup")

# 2. Make fetchNodesPage robust & immediate
old_fetch_nodes = """window.fetchNodesPage = async function() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (tbody) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr>';
    }

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Failed to load clusters.</td></tr>';
            return;
        }
        const projects = await res.json();

        window.nodesPageData = [];
        let nodeIndex = 0;

        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                nodeIndex++;
                const isPrimary = (node.role || '').toLowerCase() === 'primary';
                window.nodesPageData.push({
                    id: node.id,
                    host: node.name,
                    port: '5432',
                    ip: '10.0.20.' + (18 + nodeIndex),
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown',
                    badge: isPrimary ? { text: 'Writable', bg: '#dcfce7', color: '#16a34a' } : { text: 'Readonly', bg: '#f3f4f6', color: '#4b5563' },
                    cluster: `${proj.name} (ID:${proj.id})`,
                    clusterLogo: '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>',
                    clusterColor: '#059669',
                    version: '<div class="cc-spinner cc-spinner-sm" style="opacity:0.6;"></div>',
                    seen: 'in 4 minutes',
                    projId: proj.id
                });
            }
        }

        window.renderNodesPage();"""

new_fetch_nodes = """window.fetchNodesPage = async function() {
    const tbody = document.getElementById('nodes-page-tbody');
    if (tbody && (!window.nodesPageData || window.nodesPageData.length === 0)) {
        tbody.innerHTML = '<tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr>';
    }

    try {
        const res = await apiFetch('/api/projects');
        if (!res.ok) {
            if (tbody) tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:#ef4444;">Failed to load clusters.</td></tr>';
            return;
        }
        const projects = await res.json();

        window.nodesPageData = [];
        let nodeIndex = 0;

        for (const proj of projects) {
            for (const node of (proj.nodes || [])) {
                nodeIndex++;
                const isPrimary = (node.role || '').toLowerCase() === 'primary';
                window.nodesPageData.push({
                    id: node.id,
                    host: node.name,
                    port: '5432',
                    ip: '10.0.20.' + (18 + nodeIndex),
                    status: 'Operational',
                    type: 'PostgreSQL',
                    role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'Unknown',
                    badge: isPrimary ? { text: 'Writable', bg: '#dcfce7', color: '#16a34a' } : { text: 'Readonly', bg: '#f3f4f6', color: '#4b5563' },
                    cluster: `${proj.name} (ID:${proj.id})`,
                    clusterLogo: '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>',
                    clusterColor: '#059669',
                    version: 'PostgreSQL 16.4',
                    seen: 'in 4 minutes',
                    projId: proj.id
                });
            }
        }

        window.renderNodesPage();"""

if old_fetch_nodes in js:
    js = js.replace(old_fetch_nodes, new_fetch_nodes, 1)
    print("Optimized fetchNodesPage to render immediately without delays")

# 3. Update Changelog anchors and asset version in main.js
js = js.replace("changelogAnchors = ['v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=67', 'v=68')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update index.html
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Left Sidebar in Changelog for v1.6.1
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.0 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-9').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.9</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.6.1 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.6.0</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-9').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.9</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# Update TOC for v1.6.1
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.0 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-9').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.9 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.6.1 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-6-0').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.6.0 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-9').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.9 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# Update Middle Content for v1.6.1
old_content_top = """                    <h2 id="v1-6-0" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.0</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Persistent Auth &amp; Instant Nodes View Loading):</span> Doğrudan <code>#nodes-view</code> veya sol menüdeki <b>Nodes</b> sekmesine geçildiğinde yaşanan takılma/sonsuz yüklenme (infinite loading) sorunu çözüldü. Kimlik doğrulama belirteci (<code>globalAuthToken</code>) kalıcı olarak <code>localStorage</code> ile ilişkilendirildi ve tüm direkt sayfa geçişlerinin anında yüklenmesi sağlandı.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-6-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.1</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Zero-Dependency Direct Nodes Initialization):</span> Nodes sayfasının açılabilmesi için önce Dashboard sayfasına gitme zorunluluğuna neden olan sayfa başlatma döngüsü tamamen bağımsızlaştırıldı. Sayfa yüklendiğinde arka planda tüm cluster ve node ağacı otomatik senkronize edilerek doğrudan Nodes sekmesine girildiğinde düğümlerin anında, gecikmesiz listelenmesi sağlandı.</li>
                    </ul>

                    <h2 id="v1-6-0" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.6.0</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Persistent Auth &amp; Instant Nodes View Loading):</span> Doğrudan <code>#nodes-view</code> veya sol menüdeki <b>Nodes</b> sekmesine geçildiğinde yaşanan takılma/sonsuz yüklenme (infinite loading) sorunu çözüldü. Kimlik doğrulama belirteci (<code>globalAuthToken</code>) kalıcı olarak <code>localStorage</code> ile ilişkilendirildi ve tüm direkt sayfa geçişlerinin anında yüklenmesi sağlandı.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=68
html = html.replace('v=67', 'v=68')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html and main.js with direct zero-dependency Nodes initialization and v1.6.1 (v68)")
