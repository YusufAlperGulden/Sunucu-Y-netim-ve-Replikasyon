import re
html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_changelog_item = """<li><span style="font-weight: 600;">Feature:</span> Cluster detay sayfas&#305; tamamen yenilenerek orjinal sisteme benzer sekilde "Dashboards", "Nodes", "Performance", "Alarms" gibi sekmeli (tab) yap&#305;ya ge&#231;irildi. Sahte OS verileri (CPU/RAM/Network) kullan&#305;lmay&#305;p "Veri Al&#305;nam&#305;yor" (Unavailable) mesaj&#305; eklendi. TPS, Cache Hit ve ba&#287;lant&#305; metrikleri gibi al&#305;nabilen veriler GER&#199;EK sunuculardan saniyede bir canl&#305; okunan verilerle ger&#231;ek&#231;i olarak eklendi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> "Home" """

content = content.replace('<li><span style="font-weight: 600;">Fix:</span> "Home" ', new_changelog_item)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Changelog updated.")
