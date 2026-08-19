import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position of </body>
body_pos = content.find('</body>')
if body_pos != -1:
    content = content[:body_pos + 7] + '\n</html>\n'

# Wait, if I put it before </body> it is better!
content = content.replace('</body>\n</html>', '')
content = content.replace('</body>', '')
content = content.replace('</html>', '')

clean_tooltip = """
<div id="cluster-hover-tooltip" style="display: none; position: fixed; background: white; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 400px; z-index: 10000; overflow: hidden; font-family: 'Inter', sans-serif; transition: opacity 0.2s ease, transform 0.2s ease; opacity: 0; transform: translateY(10px);">
    <div style="background: var(--success); color: white; padding: 12px 20px; display: flex; align-items: center; gap: 8px; font-weight: 600;">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg>
        Cluster information
    </div>
    <div style="padding: 20px; color: #374151;">
        <div id="tt-cluster-message" style="display: none; background: #eff6ff; color: #1e40af; padding: 10px 15px; border-radius: 4px; border: 1px solid #bfdbfe; font-size: 0.85rem; margin-bottom: 20px; align-items: center; gap: 8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span id="tt-cluster-message-text"></span>
        </div>
        <div style="display: flex; gap: 40px; margin-bottom: 20px;">
            <div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 4px;">ID</div>
                <div style="font-weight: 500;" id="tt-cluster-id"></div>
            </div>
            <div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 4px;">Name</div>
                <div style="font-weight: 600;" id="tt-cluster-name"></div>
            </div>
        </div>
        
        <div style="display: flex; gap: 40px; margin-bottom: 20px;">
            <div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 4px;">Vendor and version</div>
                <div style="display: flex; align-items: center; gap: 6px; font-weight: 500;">
                    <span id="tt-cluster-vendor"></span>
                </div>
            </div>
            <div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 4px;">Status</div>
                <div id="tt-cluster-status" style="color: var(--success); font-weight: 500;">&#8226; Operational</div>
            </div>
        </div>
        
        <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 12px;">Topology</div>
        <div id="tt-cluster-topology-container" style="position: relative; display: flex; justify-content: center; flex-direction: column;">
        </div>
    </div>
</div>

</body>
</html>
"""

content = content + clean_tooltip

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up garbage html at end of file")
