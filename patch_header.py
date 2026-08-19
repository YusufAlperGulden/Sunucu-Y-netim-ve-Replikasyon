import os

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_main_start = """
        <!-- Main Content Wrapper -->
        <div style="flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; background: #ffffff;">
            <!-- GLOBAL TOP BAR -->
            <div style="height: 60px; min-height: 60px; display: flex; justify-content: flex-end; align-items: center; padding: 0 40px; gap: 24px; z-index: 100; border-bottom: 1px solid var(--glass-border);">
                
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #b45309; background: #fef3c7; padding: 6px 16px; border-radius: 4px; border: 1px solid #fcd34d; margin-right: auto; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    This is a demo environment. Any changes made to the nodes and clusters will be reset daily.
                </div>

                <button id="btn-deploy-cluster-global" style="background: white; border: 1px solid #d1d5db; border-radius: 20px; padding: 6px 16px; font-size: 0.85rem; font-weight: 500; color: #374151; display: flex; align-items: center; gap: 6px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                    Deploy a cluster
                </button>
                <div style="display: flex; align-items: center; color: #4b5563; cursor: pointer;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; color: #3a1c94; font-size: 0.9rem; font-weight: 500; cursor: pointer;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    Demo ClusterControl
                </div>
            </div>

            <main class="main-content" style="flex: 1; padding: 20px 40px 40px 40px; overflow-y: auto;">
"""

if '<main class="main-content">' in content:
    content = content.replace('<main class="main-content">', new_main_start)
    
if '</main>\n    </div>' in content:
    content = content.replace('</main>\n    </div>', '</main>\n        </div>\n    </div>')
    
content = content.replace('<button class="btn-primary" id="btn-deploy-cluster">+ Deploy a cluster</button>', '')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace btn-deploy-cluster with btn-deploy-cluster-global
js_content = js_content.replace("document.getElementById('btn-deploy-cluster')", "document.getElementById('btn-deploy-cluster-global')")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Patched.")
