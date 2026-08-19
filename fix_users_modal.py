import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

modal_html = """
    <!-- Create User or Team Modal -->
    <div id="modal-create-user-team" class="modal-overlay" style="display: none; align-items: center; justify-content: center; z-index: 1000;">
        <div class="modal-content" style="max-width: 600px; padding: 32px; position: relative;">
            <button onclick="document.getElementById('modal-create-user-team').style.display='none'" style="position: absolute; right: 24px; top: 24px; background: none; border: 1px solid var(--border); border-radius: 4px; padding: 4px; cursor: pointer; color: var(--text-muted);"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>
            <h2 style="font-size: 1.5rem; font-weight: 500; text-align: center; margin-bottom: 8px;">Create user or team</h2>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 32px; font-size: 0.9rem;">Create new users and group them together for better management.</p>
            
            <div style="display: flex; flex-direction: column; gap: 16px;">
                <div style="border: 1px solid var(--border); border-radius: 12px; padding: 24px; display: flex; align-items: flex-start; gap: 20px; cursor: pointer; transition: border-color 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
                    <div style="color: var(--primary);">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
                    </div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 500;">Create user</h3>
                        <ul style="margin: 0; padding-left: 20px; color: var(--text-muted); font-size: 0.9rem;">
                            <li style="margin-bottom: 4px;">Create a new user</li>
                            <li>Assign it to a team</li>
                        </ul>
                    </div>
                </div>
                
                <div style="border: 1px solid var(--border); border-radius: 12px; padding: 24px; display: flex; align-items: flex-start; gap: 20px; cursor: pointer; transition: border-color 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
                    <div style="color: var(--primary);">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
                    </div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 500;">Create team</h3>
                        <ul style="margin: 0; padding-left: 20px; color: var(--text-muted); font-size: 0.9rem;">
                            <li style="margin-bottom: 4px;">Manage large amount of users at ones</li>
                            <li>Easily assign permissions for all users in the team</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

# Insert modal before closing </body>
pattern_body = r'(</body>)'
content = re.sub(pattern_body, modal_html + r'\n\1', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Modal added")
