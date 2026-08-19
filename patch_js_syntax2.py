import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find "window.fetchAuditLogs = async function() {"
start_idx = content.find("window.fetchAuditLogs = async function() {")

if start_idx != -1:
    # I need to find the REAL end of this function.
    # The stray code is:
    # });
    #         
    #     } catch (e) {
    #         tbody.innerHTML = `<tr><td colspan="6" style="padding: 16px 24px; text-align: center; color: var(--danger);">Network error fetching logs.</td></tr>`;
    #     }
    # }
    
    # Let's find the `Network error fetching logs`
    error_str = "Network error fetching logs"
    error_idx = content.find(error_str, start_idx)
    
    if error_idx != -1:
        # Find the next } } after the error_idx
        end_idx = content.find("}\n    }", error_idx)
        if end_idx != -1:
            end_idx += len("}\n    }")
            
            # Now we replace from start_idx to end_idx with our fresh function
            fresh_func = """window.fetchAuditLogs = async function() {
    const res = await apiFetch('/api/audit-logs');
    if (res.ok) {
        const data = await res.json();
        const tbody = document.getElementById('activity-tbody') || document.getElementById('audit-table-body');
        if (!tbody) return;
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">No activities or alarms recorded yet.</td></tr>`;
        } else {
            tbody.innerHTML = data.map(log => `
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px 24px;">${log.timestamp}</td>
                    <td style="padding: 12px 24px;">
                        <span style="background: rgba(139,92,246,0.1); color: #8b5cf6; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 500;">
                            ${escapeHTML(log.user || 'System')}
                        </span>
                    </td>
                    <td style="padding: 12px 24px; font-weight: 500; color: #111827;">${escapeHTML(log.action)}</td>
                    <td style="padding: 12px 24px; color: #4b5563;">${escapeHTML(log.details || "-")}</td>
                </tr>
            `).join('');
        }
    }
}"""
            content = content[:start_idx] + fresh_func + content[end_idx:]
            
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Fixed fetchAuditLogs syntax error")
        else:
            print("End of fetchAuditLogs not found")
    else:
        print("Network error string not found")
else:
    print("start_idx not found")

