import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

modal_html = """
    <!-- Modal: Create Report / Schedule -->
    <div id="modal-create-report" class="modal-overlay" style="display: none;">
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h3 style="margin: 0; font-weight: 500; font-size: 1.1rem; color: #111827;" id="modal-create-report-title">Generate new report</h3>
                <span class="modal-close" onclick="document.getElementById('modal-create-report').style.display='none'">&times;</span>
            </div>
            <div class="modal-body">
                <div style="margin-bottom: 16px;">
                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Cluster <span style="color: #ef4444;">*</span></label>
                    <select style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">
                        <option value="">Select cluster [PLACEHOLDER]</option>
                    </select>
                </div>
                <div style="margin-bottom: 16px;">
                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Type <span style="color: #ef4444;">*</span></label>
                    <select style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; background: white; outline: none;">
                        <option value="">Select report type [PLACEHOLDER]</option>
                    </select>
                </div>
                <div style="margin-bottom: 16px;">
                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Data range <span style="color: #ef4444;">*</span></label>
                    <div style="display: flex; gap: 10px;">
                        <div style="padding: 10px; border: 1px solid var(--border); border-radius: 6px; background: #f9fafb; font-size: 0.9rem; color: #6b7280; width: 80px; text-align: center;">Days</div>
                        <input type="number" value="7" style="flex: 1; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">
                    </div>
                </div>
                <div style="margin-bottom: 24px;">
                    <label style="display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: #374151;">Recipients</label>
                    <input type="text" placeholder="Enter email recipients [PLACEHOLDER]" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 12px;">
                    <button class="btn-secondary" onclick="document.getElementById('modal-create-report').style.display='none'">Cancel</button>
                    <button class="btn-primary" onclick="document.getElementById('modal-create-report').style.display='none'">Create <span style="font-size: 0.65rem; color: #ef4444; font-weight: bold; margin-left: 5px;">[PLACEHOLDER]</span></button>
                </div>
            </div>
        </div>
    </div>
"""

# Insert modal right before </body>
content = content.replace("</body>", modal_html + "\n</body>")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added report modal")
