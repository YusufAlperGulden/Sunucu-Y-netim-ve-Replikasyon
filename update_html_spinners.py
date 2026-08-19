with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect CSS and make sure cc-spinner is styled perfectly matching ClusterControl
# In ClusterControl: purple circular spinner with animated rotation
SPINNER_CSS = """
/* ---- CLUSTERCONTROL CIRCULAR SPINNER ---- */
@keyframes cc-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.cc-spinner {
    width: 36px;
    height: 36px;
    border: 3.5px solid rgba(99, 102, 241, 0.15);
    border-top: 3.5px solid #6366f1;
    border-right: 3.5px solid #8b5cf6;
    border-radius: 50%;
    animation: cc-spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    display: inline-block;
}
.cc-spinner-sm {
    width: 18px;
    height: 18px;
    border-width: 2px;
}
.cc-spinner-lg {
    width: 44px;
    height: 44px;
    border-width: 4px;
}
.cc-loading-row td {
    text-align: center;
    padding: 50px 20px !important;
    background: transparent !important;
}
.cc-loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 40px 20px;
}
"""

# Let's update or replace the spinner CSS in index.html
if '/* ---- LOADING SPINNER ---- */' in html:
    html = html.replace('/* ---- LOADING SPINNER ---- */', '/* ---- CLUSTERCONTROL CIRCULAR SPINNER ---- */')
    # replace the block
    import re
    html = re.sub(r'/\* ---- CLUSTERCONTROL CIRCULAR SPINNER ---- \*/.*?\.cc-loading-row td \{[^}]*\}', SPINNER_CSS.strip(), html, flags=re.DOTALL)
elif '/* ---- CLUSTERCONTROL CIRCULAR SPINNER ---- */' in html:
    import re
    html = re.sub(r'/\* ---- CLUSTERCONTROL CIRCULAR SPINNER ---- \*/.*?\.cc-loading-row td \{[^}]*\}', SPINNER_CSS.strip(), html, flags=re.DOTALL)
else:
    html = html.replace('</style>', SPINNER_CSS + '\n</style>', 1)

# Now update initial HTML tbodies and loading placeholders
html = html.replace(
    '<tbody id="ac-jobs-tbody">\n            <tr><td colspan="7" style="text-align: center; padding: 40px; color: #9ca3af;">Y?kleniyor...</td></tr>\n          </tbody>',
    '<tbody id="ac-jobs-tbody"><tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading jobs...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tbody id="ac-jobs-tbody">\n            <tr><td colspan="7" style="text-align: center; padding: 40px; color: #9ca3af;">Yükleniyor...</td></tr>\n          </tbody>',
    '<tbody id="ac-jobs-tbody"><tr class="cc-loading-row"><td colspan="7"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading jobs...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tbody id="activity-tbody">\n            <tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">Y?kleniyor...</td></tr>\n          </tbody>',
    '<tbody id="activity-tbody"><tr class="cc-loading-row"><td colspan="4"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading activity logs...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tbody id="activity-tbody">\n            <tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">Yükleniyor...</td></tr>\n          </tbody>',
    '<tbody id="activity-tbody"><tr class="cc-loading-row"><td colspan="4"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading activity logs...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tbody id="nodes-page-tbody">\n                        <tr><td colspan="10" style="text-align:center; padding: 40px; color: #6b7280;">Y?kleniyor...</td></tr>\n                    </tbody>',
    '<tbody id="nodes-page-tbody"><tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tbody id="nodes-page-tbody">\n                        <tr><td colspan="10" style="text-align:center; padding: 40px; color: #6b7280;">Yükleniyor...</td></tr>\n                    </tbody>',
    '<tbody id="nodes-page-tbody"><tr class="cc-loading-row"><td colspan="10"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading nodes...</span></div></td></tr></tbody>'
)
html = html.replace(
    '<tr><td colspan="6" style="text-align:center; padding: 20px;">Loading projects...</td></tr>',
    '<tr class="cc-loading-row"><td colspan="6"><div class="cc-loading-container"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading clusters...</span></div></td></tr>'
)
html = html.replace(
    '<div style="text-align: center; padding: 20px; color: var(--text-muted);">\n                                  Loading alarms...\n                              </div>',
    '<div class="cc-loading-container" style="padding:24px;"><div class="cc-spinner"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading alarms...</span></div>'
)
html = html.replace(
    '<div class="loading-state">Dashboard y?kleniyor...</div>',
    '<div class="cc-loading-container" style="grid-column:1/-1;padding:40px;"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading dashboard metrics...</span></div>'
)
html = html.replace(
    '<div class="loading-state">Dashboard yükleniyor...</div>',
    '<div class="cc-loading-container" style="grid-column:1/-1;padding:40px;"><div class="cc-spinner cc-spinner-lg"></div><span style="color:#9ca3af;font-size:0.85rem;">Loading dashboard metrics...</span></div>'
)

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html spinner styles and initial table placeholders")
