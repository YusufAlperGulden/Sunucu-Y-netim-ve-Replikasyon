with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

audit_js_code = """
    // --- LIVE UI AUDIT DATA COLLECTION ---
    window.isUiAuditActive = false;
    window.uiAuditRecords = [];

    window.toggleUiAudit = function() {
        window.isUiAuditActive = !window.isUiAuditActive;
        const toggleBg = document.getElementById('btn-toggle-ui-audit');
        const toggleDot = document.getElementById('dot-toggle-ui-audit');
        const dlBtn = document.getElementById('btn-download-ui-audit');

        if (window.isUiAuditActive) {
            if (toggleBg) toggleBg.style.background = 'var(--primary, #3a1c94)';
            if (toggleDot) toggleDot.style.left = '24px';
            if (dlBtn) {
                dlBtn.disabled = false;
                dlBtn.style.color = 'var(--primary, #3a1c94)';
                dlBtn.style.borderColor = 'var(--primary, #3a1c94)';
                dlBtn.style.cursor = 'pointer';
                dlBtn.style.fontWeight = '500';
            }
            window.recordUiAudit('AUDIT_SESSION_STARTED', { userAgent: navigator.userAgent, timestamp: new Date().toISOString() });
        } else {
            if (toggleBg) toggleBg.style.background = '#d1d5db';
            if (toggleDot) toggleDot.style.left = '2px';
            if (dlBtn) {
                dlBtn.disabled = true;
                dlBtn.style.color = '#9ca3af';
                dlBtn.style.borderColor = '#e5e7eb';
                dlBtn.style.cursor = 'not-allowed';
                dlBtn.style.fontWeight = 'normal';
            }
            window.recordUiAudit('AUDIT_SESSION_STOPPED', { timestamp: new Date().toISOString() });
        }
    };

    window.recordUiAudit = function(eventType, details) {
        if (!window.isUiAuditActive && eventType !== 'AUDIT_SESSION_STARTED') return;
        const entry = {
            id: window.uiAuditRecords.length + 1,
            time: new Date().toISOString(),
            route: window.location.hash || '#projects-view',
            eventType: eventType,
            details: details
        };
        window.uiAuditRecords.push(entry);
        if (window.uiAuditRecords.length > 500) window.uiAuditRecords.shift();
    };

    window.downloadUiAuditData = function() {
        if (!window.uiAuditRecords || window.uiAuditRecords.length === 0) {
            alert('Henüz toplanmış bir denetim verisi bulunmamaktadır.');
            return;
        }
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
            application: "ClusterControl Web UI",
            exportDate: new Date().toISOString(),
            totalEvents: window.uiAuditRecords.length,
            events: window.uiAuditRecords
        }, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `clustercontrol-ui-audit-${Date.now()}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    };

    // Global listener for audit capture
    window.addEventListener('click', (e) => {
        if (window.isUiAuditActive) {
            const target = e.target.closest('button, a, input, select, .node-status-card, .cluster-tab, .backup-tab, .perf-subtab');
            if (target) {
                window.recordUiAudit('CLICK', {
                    tagName: target.tagName,
                    id: target.id || '',
                    className: target.className || '',
                    innerText: (target.innerText || '').substring(0, 50)
                });
            }
        }
    }, true);
"""

if 'window.toggleUiAudit' not in js:
    js = js + "\n\n" + audit_js_code

# Update Changelog anchors and asset version in main.js
js = js.replace("changelogAnchors = ['v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-6-2', 'v1-6-1', 'v1-6-0', 'v1-5-9', 'v1-5-8', 'v1-5-7', 'v1-5-6', 'v1-5-5', 'v1-5-4', 'v1-5-3', 'v1-5-2', 'v1-5-1', 'v1-5-0', 'v1-4-9', 'v1-4-8', 'v1-4-7', 'v1-4-6', 'v1-4-5', 'v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=68', 'v=69')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with live UI audit data collection and v1.6.2 (v69)")
