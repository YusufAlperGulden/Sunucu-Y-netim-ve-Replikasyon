import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

changelog_entry = """
                    <div style="margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--glass-border);">
                        <h3 style="margin-top: 0; color: var(--primary);">v1.4.1 - Backup Modals UI Eklenmesi</h3>
                        <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 12px;">19 Ağustos 2026</div>
                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6; color: var(--text-main);">
                            <li><strong>UI/UX:</strong> "Backups" menüsündeki "Create backup" butonu aktif edildi.</li>
                            <li><strong>UI/UX:</strong> "Backup on Demand" ve "Schedule a Backup" seçeneklerini sunan ClusterControl tasarımlı yeni modal eklendi.</li>
                            <li><strong>UI/UX:</strong> Backup konfigürasyon (Configuration) adımı kodlandı. Gerçek Cluster'lar ve bu cluster'lara ait aktif sunucular (Host) otomatik olarak listelenmektedir.</li>
                            <li><strong>System:</strong> "Sahte veri yok" kuralı gereğince, S3 Cloud Storage entegrasyonu tamamlanmadığı için yedekleme işlemi başlatıldığında şeffaf ve dürüst bir "Cloud Storage (AWS S3) is not configured" hatası gösterilmesi sağlandı.</li>
                        </ul>
                    </div>
"""

# Insert the new changelog entry right after the changelog container div
content = content.replace(
    '<div style="background: var(--glass-bg); padding: 32px; border-radius: 8px; border: 1px solid var(--glass-border); box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 500px;">',
    '<div style="background: var(--glass-bg); padding: 32px; border-radius: 8px; border: 1px solid var(--glass-border); box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 500px;">\n' + changelog_entry
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated changelog in index.html")
