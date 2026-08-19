import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

demo_banner = """
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #b45309; background: #fef3c7; padding: 6px 16px; border-radius: 4px; border: 1px solid #fcd34d; margin-right: auto; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    This is a demo environment. Any changes made to the nodes and clusters will be reset daily.
                </div>"""

# Ensure exact match by using a regex just in case spaces differ slightly
content = re.sub(
    r'<div style="display: flex; align-items: center; gap: 8px; font-size: 0\.85rem; color: #b45309; background: #fef3c7; padding: 6px 16px; border-radius: 4px; border: 1px solid #fcd34d; margin-right: auto; box-shadow: 0 1px 2px rgba\(0,0,0,0\.05\);">\s*<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2\.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12\.01" y2="16"></line></svg>\s*This is a demo environment\. Any changes made to the nodes and clusters will be reset daily\.\s*</div>',
    '',
    content
)

# Also let's update changelog
changelog_entry = """
                    <div style="margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--glass-border);">
                        <h3 style="margin-top: 0; color: var(--primary);">v1.4.3 - Demo Uyarısının Kaldırılması</h3>
                        <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 12px;">19 Ağustos 2026</div>
                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6; color: var(--text-main);">
                            <li><strong>UI:</strong> Üst menüde yer alan "This is a demo environment" şeklindeki sarı uyarı banner'ı kaldırıldı.</li>
                        </ul>
                    </div>
"""
content = content.replace(
    '<div style="background: var(--glass-bg); padding: 32px; border-radius: 8px; border: 1px solid var(--glass-border); box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 500px;">',
    '<div style="background: var(--glass-bg); padding: 32px; border-radius: 8px; border: 1px solid var(--glass-border); box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 500px;">\n' + changelog_entry
)


with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed banner and updated changelog")
