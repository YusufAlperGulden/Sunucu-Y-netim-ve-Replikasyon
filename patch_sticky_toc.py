with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build the new Changelog section with sticky/fixed sidebars and new v1.4.4 release block
NEW_CHANGELOG_SECTION = """        <!-- CHANGELOG VIEW -->
        <section id="changelog-view" class="view-section" style="display: none; height: calc(100vh - 110px); min-height: 600px;">
            <div style="display: flex; height: 100%; max-height: 100%; background: #ffffff; border: 1px solid var(--glass-border); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); overflow: hidden; position: relative;">
                <!-- Left Sidebar (Fixed / Non-scrolling) -->
                <div style="width: 250px; flex-shrink: 0; border-right: 1px solid #e5e7eb; padding: 32px 24px; display: flex; flex-direction: column; gap: 16px; font-size: 0.9rem; background: #fafafa; position: sticky; top: 0; align-self: flex-start; height: 100%; overflow-y: auto; user-select: none;">
                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.4.4 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.3</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.2</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.4.1</a>
                    <a href="#changelog-view" onclick="event.preventDefault();" style="color: #9ca3af; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px; cursor: default;" title="Archived versions coming soon">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>
                </div>
                
                <!-- Middle Content (The ONLY scrolling container) -->
                <div id="changelog-middle-content" style="flex: 1; padding: 32px 48px; overflow-y: auto; height: 100%; scroll-behavior: smooth;">
                    <div style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 24px;">Home &gt; Release Notes</div>
                    <h1 style="color: #4b5563; font-weight: 300; font-size: 2.2rem; margin-bottom: 24px;">Release Notes</h1>
                    <p style="color: #4b5563; line-height: 1.6; margin-bottom: 40px; font-size: 1.05rem;">Use this page as your guide to stay up to date on the latest enhancements and changes, ensuring you can make the most of ClusterControl's powerful capabilities.</p>
                    
                    <h2 id="v1-4-4" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.4</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">UI/UX (Fixed Table of Contents):</span> Changelog sayfasındaki sağ <b>İçindekiler (Table of Contents)</b> ve sol Release Notes menüleri, sayfa aşağı kaydırıldığında pozisyonunu kaybetmeyecek şekilde sabitlendi (`position: sticky; top: 0`). Yalnızca orta içerik alanı bağımsız kaydırılarak menülerin her zaman ekranda görünür kalması sağlandı.</li>
                        <li><span style="font-weight: 600;">Rules &amp; Standards:</span> Her commit ve güncellemede semantik sürüm numaralandırmasının (`v1.4.3` &rarr; `v1.4.4` &rarr; `v1.4.5`) otomatik artırılması kuralı devreye alındı.</li>
                    </ul>

                    <h2 id="v1-4-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.3</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Fix (Nodes View):</span> Nodes sayfasında düğümlerin listelenmesini engelleyen çift döngü ve eski closure referansı temizlendi. Tüm cluster'lardaki sunucular (Primary &amp; Standby) anında stat kartlarına (Operational, Failed, Offline vb.) ve envanter tablosuna gerçek zamanlı olarak bağlandı.</li>
                        <li><span style="font-weight: 600;">Feature (Audit Log Search &amp; Export):</span> Audit Log sekmesine anlık <b>Arama Çubuğu (Search Bar)</b>, <b>Filtre Sıfırlama ("Clear all filters")</b>, <b>Yenileme (Refresh)</b> ve ClusterControl formatında birebir uyumlu <b>CSV Dışa Aktarma ("Export CSV")</b> özelliği eklendi.</li>
                        <li><span style="font-weight: 600;">UI/UX (Loading Animation):</span> ClusterControl tasarımı ile birebir uyumlu <b>Circular Loading Spinner (Dönen Dairesel Animasyon)</b> tüm tablolara, kartlara ve yükleme durumlarına eklendi. Ham metin ("Yükleniyor...") yerine zarif dönen çember animasyonu gösterilmektedir.</li>
                        <li><span style="font-weight: 600;">Feature (Activity Center):</span> Activity Center ekranı orijinal ClusterControl yapısına uygun olarak 4 sekmeye ayrıldı: <b>Alarms</b>, <b>Jobs</b> (Yedekleme ve sistem işleri), <b>Audit Log</b> (Kullanıcı eylem ve denetim kayıtları) ve <b>Watchlists (Beta)</b>.</li>
                        <li><span style="font-weight: 600;">Fix (Replication &amp; Metrics):</span> Frankfurt (Ana Sunucu) ve Londra (Yedek Sunucu) Neon PostgreSQL veritabanı bağlantı şifreleri ve SSL parametreleri otomatik senkronize edilerek TPS, Ping, Storage ve Ana Tablo (vehicles) kayıt sayısı canlı metrikleri bağlandı.</li>
                    </ul>

                    <h2 id="v1-4-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.2</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Özellik 4:</span> <b>User Management (Kullanıcı Yönetimi)</b> motoru aktif edildi. Veritabanı destekli <code>User</code> modeli oluşturuldu, şifreler bcrypt ile hash'lendi ve kullanıcı silme/ekleme işlemleri yapıldı.</li>
                        <li><span style="font-weight: 600;">Hotfix 3 (Final):</span> Python <code>AttributeError</code> hatası çözüldü. "models.py" içerisindeki sınıf tanımına eklenmesi unutulan sütun değişkenleri (ssh_host) koda dahil edildi. Tüm özellikler %100 istikrarlı çalışıyor.</li>
                        <li><span style="font-weight: 600;">Hotfix 2:</span> Internal Server Error (500) tam olarak çözüldü! Bir önceki güncellemede manuel veritabanı göçlerini yaparken tablonun adını yanlışlıkla "database_nodes" yerine "nodes" olarak sorgulayan kod düzeltildi.</li>
                        <li><span style="font-weight: 600;">Hotfix (500 Internal Server Error):</span> "DatabaseNode" ve "AuditLog" tablolarındaki eksik sütunlar için otomatik SQLite / PostgreSQL şema göçü (Schema Migration) eklendi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> Uygulamaya yapılan önceki güncellemeler sırasında meydana gelen küçük bir yazım hatasından dolayı tüm etkileşimlerin bozulması (Syntax Error) sorunu düzeltildi.</li>
                        <li><span style="font-weight: 600;">Feature:</span> "Settings" ekranında artık gerçekten var olan PostgreSQL ayarları için API bağlantıları kuruldu.</li>
                    </ul>

                    <h2 id="v1-4-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.1</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature:</span> Veritabanı gecikme (lag) ve senkronizasyon metriklerini gösteren detaylı "Sunucu Yönetim Dashboard" eklendi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Uygulama giriş (Login) ekranı kurumsal tasarıma uygun hale getirildi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> Uzun sayfalarda kaydırma çubuğunun (scrollbar) menülerle çakışması sorunu düzeltildi.</li>
                    </ul>
                </div>
                
                <!-- Right Sidebar (TOC - Strictly Fixed / Non-scrolling) -->
                <div style="width: 250px; flex-shrink: 0; border-left: 1px solid #e5e7eb; padding: 32px 24px; font-size: 0.85rem; background: #fafafa; position: sticky; top: 0; align-self: flex-start; height: 100%; overflow-y: auto; user-select: none;">
                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.4.4 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.3 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-4-1').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>
                </div>
            </div>
        </section>"""

# Replace in index.html
start_idx = html.find('<!-- CHANGELOG VIEW -->')
end_idx = html.find('<!-- Add Project Modal -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + NEW_CHANGELOG_SECTION + "\n\n        </main>\n        </div>\n    </div>\n\n    " + html[end_idx:]
    print("Replaced Changelog view with strictly pinned Table of Contents and v1.4.4")

# Bump asset version to v=51
html = html.replace('v=50', 'v=51')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("changelogAnchors = ['v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];", "changelogAnchors = ['v1-4-4', 'v1-4-3', 'v1-4-2', 'v1-4-1', 'release-cycle', 'whats-new'];")
js = js.replace('v=50', 'v=51')

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated main.js with v1.4.4 anchor and v=51")
