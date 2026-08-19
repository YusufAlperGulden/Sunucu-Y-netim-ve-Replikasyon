import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire changelog-view section
pattern = r'<!-- CHANGELOG VIEW -->\s*<section id="changelog-view".*?</section>'
new_changelog = """<!-- CHANGELOG VIEW -->
        <section id="changelog-view" class="view-section" style="display: none; height: 100%;">
            <div style="display: flex; height: 100%; min-height: 800px; background: #ffffff; border: 1px solid var(--glass-border); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); overflow: hidden;">
                <!-- Left Sidebar -->
                <div style="width: 250px; border-right: 1px solid #e5e7eb; padding: 32px 24px; display: flex; flex-direction: column; gap: 16px; font-size: 0.9rem; background: #fafafa;">
                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#v1-4-2" style="color: #4b5563; text-decoration: none;">v1.4.2 (Latest)</a>
                    <a href="#v1-4-1" style="color: #4b5563; text-decoration: none;">v1.4.1</a>
                    <a href="#v1-4-0" style="color: #4b5563; text-decoration: none;">v1.4.0</a>
                    <a href="#v1-3-0" style="color: #4b5563; text-decoration: none;">v1.3.0</a>
                    <a href="#" style="color: #4b5563; text-decoration: none; display: flex; justify-content: space-between; margin-top: 12px;">Archived <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></a>
                </div>
                
                <!-- Middle Content -->
                <div style="flex: 1; padding: 32px 48px; overflow-y: auto; scroll-behavior: smooth;">
                    <div style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 24px;">Home &gt; Release Notes</div>
                    <h1 style="color: #4b5563; font-weight: 300; font-size: 2.2rem; margin-bottom: 24px;">Release Notes</h1>
                    <p style="color: #4b5563; line-height: 1.6; margin-bottom: 40px; font-size: 1.05rem;">Use this page as your guide to stay up to date on the latest enhancements and changes, ensuring you can make the most of ClusterControl's powerful capabilities.</p>
                    
                    <h2 id="v1-4-2" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.2</h2>
                    
                    <h3 style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature:</span> Sayfalardan ba&#287;&#305;ms&#305;z her zaman ekranda kalan Global Top Bar ve h&#305;zl&#305; "Deploy a Cluster" butonu eklendi.</li>
                        <li><span style="font-weight: 600;">Feature:</span> Sol men&#252;ye (Sidebar) k&#252;melere (Ara&#231; Plaka Takip Sistemi &amp; E-mail Okuma) an&#305;nda eri&#351;im sa&#287;layan a&#231;&#305;l&#305;r-kapan&#305;r "Clusters" alt men&#252;s&#252; eklendi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Geli&#351;mi&#351; Ayarlar (Settings) men&#252;s&#252; 7 farkl&#305; sekmeye b&#246;l&#252;nerek daha d&#252;zenli hale getirildi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Men&#252;lerde dola&#351;&#305;rken Cluster detaylar&#305;n&#305;n (tooltip) an&#305;nda a&#231;&#305;l&#305;p ekran&#305; kaplamas&#305;n&#305; &#246;nlemek i&#231;in 0.2 saniyelik hover gecikmesi eklendi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> "Nodes" sayfas&#305;ndaki Donut grafi&#287;inin animasyonlar&#305;n&#305;n &#231;al&#305;&#351;mamas&#305; ve merkezine toplam node say&#305;s&#305;n&#305; yazmamas&#305; sorunu giderildi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> Sunucu listesindeki veritaban&#305; s&#252;r&#252;m metriklerinin canl&#305; PostgreSQL s&#252;r&#252;m&#252;yle (18.4) senkronize olmamas&#305; sorunu giderildi.</li>
                    </ul>

                    <h2 id="v1-4-1" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.4.1</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Feature:</span> Veritaban&#305; gecikme (lag) ve senkronizasyon metriklerini g&#246;steren detayl&#305; "Sunucu Y&#246;netim Dashboard" eklendi.</li>
                        <li><span style="font-weight: 600;">Improvement:</span> Uygulama giri&#351; (Login) ekran&#305; kurumsal tasar&#305;ma uygun hale getirildi.</li>
                        <li><span style="font-weight: 600;">Fix:</span> Uzun sayfalarda kayd&#305;rma &#231;ubu&#287;unun (scrollbar) men&#252;lerle &#231;ak&#305;&#351;mas&#305; sorunu d&#252;zeltildi.</li>
                    </ul>
                </div>
                
                <!-- Right Sidebar (TOC) -->
                <div style="width: 250px; border-left: 1px solid #e5e7eb; padding: 32px 24px; font-size: 0.85rem; background: #fafafa;">
                    <div style="color: #9ca3af; margin-bottom: 16px;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#v1-4-2" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.2 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#v1-4-2" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#v1-4-2" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#v1-4-1" style="color: inherit; text-decoration: none; font-weight: 500;">v1.4.1 Release</a>
                    </div>
                </div>
            </div>
        </section>"""

content_new = re.sub(pattern, new_changelog, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content_new)
print("Replaced changelog view.")
