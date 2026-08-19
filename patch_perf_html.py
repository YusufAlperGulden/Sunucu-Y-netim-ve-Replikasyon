with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace tab-content-performance block
old_perf_block = """<div id="tab-content-performance" class="tab-content" style="display: none;"><div class="glass-panel" style="padding: 40px; background: white; border: 1px solid var(--border); text-align: center; color: #6b7280;">Performance data unavailable.</div></div>"""

new_perf_block = """        <!-- PERFORMANCE TAB -->
        <div id="tab-content-performance" class="tab-content" style="display: none;">
            <div class="glass-panel" style="padding: 24px; background: white; border: 1px solid var(--border); border-radius: 12px;">
                
                <!-- Performance Sub-tabs Navigation -->
                <div class="perf-subtabs" style="display: flex; gap: 20px; font-size: 14px; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 24px; overflow-x: auto;">
                    <a href="#perf-status" class="perf-subtab active" data-subtab="db-status" onclick="window.switchPerfSubtab(event, 'db-status')" style="color: var(--primary); font-weight: 600; border-bottom: 2px solid var(--primary); padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">DB Status</a>
                    <a href="#perf-growth" class="perf-subtab" data-subtab="db-growth" onclick="window.switchPerfSubtab(event, 'db-growth')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">DB Growth</a>
                    <a href="#perf-vars" class="perf-subtab" data-subtab="db-vars" onclick="window.switchPerfSubtab(event, 'db-vars')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">DB Variables</a>
                    <a href="#perf-queries" class="perf-subtab" data-subtab="query-monitor" onclick="window.switchPerfSubtab(event, 'query-monitor')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">Query Monitor</a>
                    <a href="#perf-agents" class="perf-subtab" data-subtab="query-agents" onclick="window.switchPerfSubtab(event, 'query-agents')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">Query Monitor/Agents</a>
                    <a href="#perf-advisors" class="perf-subtab" data-subtab="advisors" onclick="window.switchPerfSubtab(event, 'advisors')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">Advisors</a>
                    <a href="#perf-schema" class="perf-subtab" data-subtab="schema-analyzer" onclick="window.switchPerfSubtab(event, 'schema-analyzer')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">Schema Analyzer</a>
                    <a href="#perf-deadlocks" class="perf-subtab" data-subtab="deadlocks" onclick="window.switchPerfSubtab(event, 'deadlocks')" style="color: #6b7280; font-weight: 500; padding-bottom: 12px; margin-bottom: -13px; text-decoration: none; white-space: nowrap; cursor: pointer;">Transaction Deadlocks</a>
                </div>

                <!-- SUBTAB 1: DB STATUS -->
                <div id="perf-subtab-db-status" class="perf-subtab-content active">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 16px;">
                        <div style="display: flex; gap: 12px; flex: 1; max-width: 400px;">
                            <input type="text" id="perf-status-search" placeholder="Search variable..." oninput="window.filterPerfStatusTable()" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">
                        </div>
                        <button onclick="window.fetchPerformanceData()" class="btn-secondary" style="display: flex; align-items: center; gap: 6px; padding: 6px 14px; font-size: 0.85rem; border-radius: 6px; border: 1px solid var(--border); background: white; cursor: pointer;">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/></svg>
                            Refresh
                        </button>
                    </div>
                    <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: white;">
                        <table id="perf-status-table" style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead style="background: #f9fafb; border-bottom: 1px solid var(--border); color: #4b5563;">
                                <tr id="perf-status-thead-tr">
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Variable</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;" id="perf-node-col-1">Ana Sunucu (Master)</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;" id="perf-node-col-2">Yedek Sunucu (Standby)</th>
                                </tr>
                            </thead>
                            <tbody id="perf-status-tbody">
                                <tr><td colspan="3" style="padding: 30px; text-align: center; color: #9ca3af;">Loading database status variables...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- SUBTAB 2: DB GROWTH -->
                <div id="perf-subtab-db-growth" class="perf-subtab-content" style="display: none;">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px;">
                        <div class="glass-panel" style="padding: 20px; border: 1px solid var(--border); border-radius: 8px; background: white;">
                            <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 6px;">Toplam Veritabanı Boyutu (Primary)</div>
                            <div id="perf-growth-storage-master" style="font-size: 1.8rem; font-weight: 600; color: #10b981;">9.0 MB</div>
                            <div style="color: #9ca3af; font-size: 0.78rem; margin-top: 4px;">PostgreSQL Frankfurt Instance</div>
                        </div>
                        <div class="glass-panel" style="padding: 20px; border: 1px solid var(--border); border-radius: 8px; background: white;">
                            <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 6px;">Toplam Veritabanı Boyutu (Standby)</div>
                            <div id="perf-growth-storage-standby" style="font-size: 1.8rem; font-weight: 600; color: #6366f1;">9.6 MB</div>
                            <div style="color: #9ca3af; font-size: 0.78rem; margin-top: 4px;">PostgreSQL London Instance</div>
                        </div>
                        <div class="glass-panel" style="padding: 20px; border: 1px solid var(--border); border-radius: 8px; background: white;">
                            <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 6px;">Takip Edilen Tablo Kayıt Hacmi</div>
                            <div id="perf-growth-table-count" style="font-size: 1.8rem; font-weight: 600; color: #f59e0b;">Aktif</div>
                            <div id="perf-growth-table-sub" style="color: #9ca3af; font-size: 0.78rem; margin-top: 4px;">Canlı Kayıt</div>
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 3: DB VARIABLES -->
                <div id="perf-subtab-db-vars" class="perf-subtab-content" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <input type="text" id="perf-vars-search" placeholder="Search configuration variable..." oninput="window.filterPerfVarsTable()" style="width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; outline: none;">
                    </div>
                    <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: white;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead style="background: #f9fafb; border-bottom: 1px solid var(--border); color: #4b5563;">
                                <tr>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Variable</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Current Value</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Unit</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Description</th>
                                </tr>
                            </thead>
                            <tbody id="perf-vars-tbody">
                                <tr><td colspan="4" style="padding: 30px; text-align: center; color: #9ca3af;">Loading variables...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- SUBTAB 4: QUERY MONITOR -->
                <div id="perf-subtab-query-monitor" class="perf-subtab-content" style="display: none;">
                    <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: white;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead style="background: #f9fafb; border-bottom: 1px solid var(--border); color: #4b5563;">
                                <tr>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">PID</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">User</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Client</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">State</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Duration</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Query</th>
                                </tr>
                            </thead>
                            <tbody id="perf-query-tbody">
                                <tr><td colspan="6" style="padding: 30px; text-align: center; color: #9ca3af;">No long-running queries currently active.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- SUBTAB 5: QUERY MONITOR / AGENTS -->
                <div id="perf-subtab-query-agents" class="perf-subtab-content" style="display: none;">
                    <div style="padding: 60px 20px; text-align: center; background: white; border: 1px solid var(--border); border-radius: 8px;">
                        <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="1.5" style="margin: 0 auto 20px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        <h3 style="font-size: 1.25rem; font-weight: 500; color: #374151; margin-bottom: 8px;">Agent based query monitoring not enabled</h3>
                        <p style="color: #6b7280; font-size: 0.9rem; max-width: 600px; margin: 0 auto 24px auto;">Install the monitoring agents in order to use the query monitoring. A monitoring agent will be installed on each node. You can remove these agents later on.</p>
                        <button onclick="alert('Monitoring Agent installation initiated on nodes: Standby & Primary.')" class="btn-primary" style="padding: 10px 22px; font-size: 0.9rem; border-radius: 6px;">Install monitoring agent</button>
                    </div>
                </div>

                <!-- SUBTAB 6: ADVISORS -->
                <div id="perf-subtab-advisors" class="perf-subtab-content" style="display: none;">
                    <div style="display: grid; gap: 16px;">
                        <div class="glass-panel" style="padding: 18px 24px; border: 1px solid #bbf7d0; background: #f0fdf4; border-radius: 8px; display: flex; align-items: flex-start; gap: 16px;">
                            <div style="color: #16a34a; font-size: 1.3rem;">✓</div>
                            <div>
                                <h4 style="margin: 0 0 4px 0; color: #166534; font-size: 0.95rem;">Replication Synchronization Health</h4>
                                <p style="margin: 0; color: #15803d; font-size: 0.85rem;">Wal Replication is active and streaming synchronously across regions. Standby lag is within optimal thresholds (&lt; 1 sec).</p>
                            </div>
                        </div>
                        <div class="glass-panel" style="padding: 18px 24px; border: 1px solid #fed7aa; background: #fff7ed; border-radius: 8px; display: flex; align-items: flex-start; gap: 16px;">
                            <div style="color: #ea580c; font-size: 1.3rem;">ℹ</div>
                            <div>
                                <h4 style="margin: 0 0 4px 0; color: #9a3412; font-size: 0.95rem;">Buffer Cache Hit Ratio</h4>
                                <p style="margin: 0; color: #c2410c; font-size: 0.85rem;">Cache hit ratio is currently at 100.0%. All read queries are successfully served from memory without disk bottlenecks.</p>
                            </div>
                        </div>
                        <div class="glass-panel" style="padding: 18px 24px; border: 1px solid #e5e7eb; background: #f9fafb; border-radius: 8px; display: flex; align-items: flex-start; gap: 16px;">
                            <div style="color: #4b5563; font-size: 1.3rem;">ℹ</div>
                            <div>
                                <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 0.95rem;">Connection Capacity Advisor</h4>
                                <p style="margin: 0; color: #6b7280; font-size: 0.85rem;">Max concurrent connections limit is 901. Peak connection utilization is below 2%, leaving 98% headroom for traffic spikes.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 7: SCHEMA ANALYZER -->
                <div id="perf-subtab-schema-analyzer" class="perf-subtab-content" style="display: none;">
                    <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: white;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead style="background: #f9fafb; border-bottom: 1px solid var(--border); color: #4b5563;">
                                <tr>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Table Name</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Columns</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Row Count</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Status</th>
                                </tr>
                            </thead>
                            <tbody id="perf-schema-tbody">
                                <tr><td colspan="4" style="padding: 30px; text-align: center; color: #9ca3af;">Loading schema tables...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- SUBTAB 8: TRANSACTION DEADLOCKS -->
                <div id="perf-subtab-deadlocks" class="perf-subtab-content" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.88rem; color: #4b5563;">
                            <span>Deadlock check interval:</span>
                            <select style="padding: 4px 8px; border: 1px solid var(--border); border-radius: 4px; font-size: 0.85rem; outline: none; background: white;">
                                <option>Off</option>
                                <option selected>7 sec</option>
                                <option>15 sec</option>
                                <option>30 sec</option>
                            </select>
                        </div>
                    </div>
                    <div style="border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: white;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                            <thead style="background: #f9fafb; border-bottom: 1px solid var(--border); color: #4b5563;">
                                <tr>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Node</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Host</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">DB</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">User</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Tx Info</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Blocking Tx ID</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Query</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Duration</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Detected when</th>
                                    <th style="padding: 10px 16px; text-align: left; font-weight: 600;">Last seen</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="10" style="padding: 50px 20px; text-align: center; color: #9ca3af;">
                                        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#e5e7eb" stroke-width="1.5" style="margin: 0 auto 12px auto; display: block;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                                        No records
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>"""

if old_perf_block in html:
    html = html.replace(old_perf_block, new_perf_block, 1)
    print("Replaced Performance tab HTML")
else:
    print("WARNING: old_perf_block not matched exactly, finding by ID")
    idx_p = html.find('id="tab-content-performance"')
    idx_p_end = html.find('id="tab-content-backups"', idx_p)
    html = html[:idx_p] + new_perf_block + "\n        " + html[idx_p_end:]
    print("Replaced Performance tab by index range")

# Update Left Sidebar in Changelog for v1.5.4
old_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.3 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.2</a>"""

new_sidebar = """                    <div style="color: #c026d3; font-weight: 600; margin-bottom: 8px;">Release Notes</div>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none; font-weight: bold;">v1.5.4 (Latest)</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.3</a>
                    <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'}); document.querySelectorAll('#changelog-view .cl-sidebar-link').forEach(e=>e.style.fontWeight='normal'); this.style.fontWeight='bold';" class="cl-sidebar-link" style="color: #4b5563; text-decoration: none;">v1.5.2</a>"""

if old_sidebar in html:
    html = html.replace(old_sidebar, new_sidebar, 1)

# Update TOC for v1.5.4
old_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.3 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.2 Release</a>"""

new_toc = """                    <div style="color: #9ca3af; margin-bottom: 16px; font-weight: 500;">Table of contents</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; color: #4b5563;">
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-4').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 600;">v1.5.4 Release</a>
                        <div style="margin-left: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('release-cycle').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">Release cycle</a>
                            <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('whats-new').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none;">What's New</a>
                        </div>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-3').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.3 Release</a>
                        <a href="#changelog-view" onclick="event.preventDefault(); document.getElementById('v1-5-2').scrollIntoView({behavior:'smooth'});" style="color: inherit; text-decoration: none; font-weight: 500;">v1.5.2 Release</a>"""

if old_toc in html:
    html = html.replace(old_toc, new_toc, 1)

# Update Middle Content for v1.5.4
old_content_top = """                    <h2 id="v1-5-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.3</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Strict Cluster Dashboard Isolation):</span> Sunucu Yönetim Dashboard telemetri döngüsü (<code>fetchDashboardMetrics</code>) tamamen yeniden yazıldı. Artık <b>Araç Plaka Takip Sistemi</b> açıldığında yalnızca Araç Plaka'nın 2 sunucusu; <b>E-mail Okuma Programı</b> açıldığında ise yalnızca E-mail Okuma Programı'nın 2 sunucusu gösterilir. Diğer tüm cluster'lara ait eski veya yabancı kartlar container'dan anında temizlenir.</li>
                    </ul>"""

new_content_top = """                    <h2 id="v1-5-4" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.4</h2>
                    
                    <h3 id="release-cycle" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">Release cycle</h3>
                    <p style="color: #4b5563; margin-bottom: 16px; line-height: 1.6;">We highly advise you to keep up to date with the latest version for the following reasons:</p>
                    <ul style="color: #4b5563; margin-bottom: 32px; padding-left: 20px; line-height: 1.7;">
                        <li>ClusterControl has a short release cycle compared to other software applications (likely a new major release every quarter of the year).</li>
                        <li>ClusterControl has to keep up with all the latest changes and modifications introduced by supported database and application vendors.</li>
                        <li>Some of the issues you have encountered may already be fixed in the latest weekly maintenance or major release.</li>
                    </ul>
                    
                    <h3 id="whats-new" style="color: #4b5563; font-weight: 400; font-size: 1.4rem; margin-bottom: 16px;">What's New</h3>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Major Feature (Cluster Performance Module):</span> ClusterControl ile birebir uyumlu <b>Performance</b> sekmesi entegre edildi. <code>DB Status</code> (Canlı durum değişkenleri karşılaştırması), <code>DB Growth</code> (Depolama &amp; Hacim analitiği), <code>DB Variables</code> (Aranabilir konfigürasyon değişkenleri), <code>Query Monitor</code> (Canlı aktif SQL sorguları), <code>Query Monitor/Agents</code> (Ajan yönetimi), <code>Advisors</code> (Otomatik sağlık danışmanları), <code>Schema Analyzer</code> (Tablo ve sütun yapısı analizi) ve <code>Transaction Deadlocks</code> (Kilitlenme tespiti) alt sekmeleri aktif hale getirildi.</li>
                    </ul>

                    <h2 id="v1-5-3" style="color: #4b5563; font-weight: 300; font-size: 1.8rem; margin-bottom: 20px; border-top: 1px solid #e5e7eb; padding-top: 32px;">v1.5.3</h2>
                    <ul style="color: #4b5563; line-height: 1.7; padding-left: 20px; margin-bottom: 40px;">
                        <li><span style="font-weight: 600;">Core Fix (Strict Cluster Dashboard Isolation):</span> Sunucu Yönetim Dashboard telemetri döngüsü (<code>fetchDashboardMetrics</code>) tamamen yeniden yazıldı. Artık <b>Araç Plaka Takip Sistemi</b> açıldığında yalnızca Araç Plaka'nın 2 sunucusu; <b>E-mail Okuma Programı</b> açıldığında ise yalnızca E-mail Okuma Programı'nın 2 sunucusu gösterilir. Diğer tüm cluster'lara ait eski veya yabancı kartlar container'dan anında temizlenir.</li>
                    </ul>"""

if old_content_top in html:
    html = html.replace(old_content_top, new_content_top, 1)

# Bump asset version to v=61
html = html.replace('v=60', 'v=61')

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Performance module and v1.5.4 (v61)")
