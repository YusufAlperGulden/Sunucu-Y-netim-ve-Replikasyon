import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

tooltip_logic = """
                let hoverTimeout;
                document.querySelectorAll('.node-hex-hover').forEach(el => {
                    el.onmouseenter = (e) => {
                        clearTimeout(hoverTimeout);
                        hoverTimeout = setTimeout(() => {
                            const ntt = document.getElementById('node-hover-tooltip');
                            const data = window['nodeData_' + el.getAttribute('data-idx')];
                            if (ntt && data) {
                                const header = document.getElementById('ntt-header');
                                const msgBox = document.getElementById('ntt-message');
                                const stat = document.getElementById('ntt-status');
                                
                                document.getElementById('ntt-hostname').innerText = data.hostname;
                                document.getElementById('ntt-port').innerText = data.port;
                                document.getElementById('ntt-role').innerText = data.role;
                                document.getElementById('ntt-type').innerText = data.type;
                                document.getElementById('ntt-cluster').innerText = data.cluster;
                                document.getElementById('ntt-badge').innerHTML = data.badge;
                                
                                // Update Logo
                                let logoHtml = '';
                                if (data.vendorType === 'mariadb') {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"></path></svg>`; // Mock Bird logo
                                } else if (data.vendorType === 'postgres') {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path></svg>`; // Mock Elephant logo
                                } else {
                                    logoHtml = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2"><rect x="10" y="3" width="4" height="4" rx="1"></rect><rect x="3" y="17" width="4" height="4" rx="1"></rect><rect x="10" y="17" width="4" height="4" rx="1"></rect><rect x="17" y="17" width="4" height="4" rx="1"></rect><line x1="12" y1="7" x2="12" y2="12"></line><line x1="5" y1="12" x2="19" y2="12"></line><line x1="5" y1="12" x2="5" y2="17"></line><line x1="12" y1="12" x2="12" y2="17"></line><line x1="19" y1="12" x2="19" y2="17"></line></svg>`;
                                }
                                const clusterLogoContainer = document.getElementById('ntt-cluster').previousElementSibling;
                                if (clusterLogoContainer && clusterLogoContainer.tagName === 'svg') {
                                    clusterLogoContainer.outerHTML = logoHtml;
                                }
                                
                                if (data.status === 'Shut Down') {
                                    header.style.background = '#3b82f6';
                                    msgBox.style.display = 'flex';
                                    stat.innerHTML = '<span style="color:#3b82f6;">? Shut Down</span>';
                                    document.getElementById('ntt-repl-col').style.display = 'block';
                                } else {
                                    header.style.background = 'var(--success)';
                                    msgBox.style.display = 'none';
                                    stat.innerHTML = '<span style="color:var(--success);">? Operational</span>';
                                    document.getElementById('ntt-repl-col').style.display = 'none';
                                }
                                
                                // Reset display and opacity to allow animation
                                ntt.style.display = 'block';
                                ntt.style.opacity = '0';
                                ntt.style.transform = 'translateY(10px)';
                                ntt.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                                
                                const rect = el.getBoundingClientRect();
                                const tooltipRect = ntt.getBoundingClientRect();
                                
                                // Center horizontally above the node
                                let leftPos = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
                                // Prevent going off-screen
                                leftPos = Math.max(10, Math.min(window.innerWidth - tooltipRect.width - 10, leftPos));
                                
                                // Place right above the node
                                let topPos = rect.top - tooltipRect.height - 15;
                                if (topPos < 0) {
                                    // If no space above, put below
                                    topPos = rect.bottom + 15;
                                }
                                
                                ntt.style.top = topPos + 'px';
                                ntt.style.left = leftPos + 'px';
                                
                                // Trigger animation
                                requestAnimationFrame(() => {
                                    ntt.style.opacity = '1';
                                    ntt.style.transform = 'translateY(0)';
                                });
                            }
                        }, 1000); // 1 second delay
                    };
                    el.onmouseleave = (e) => {
                        clearTimeout(hoverTimeout);
                        const ntt = document.getElementById('node-hover-tooltip');
                        if (ntt) {
                            ntt.style.opacity = '0';
                            ntt.style.transform = 'translateY(10px)';
                            setTimeout(() => {
                                if (ntt.style.opacity === '0') {
                                    ntt.style.display = 'none';
                                }
                            }, 200);
                        }
                    };
                });
"""

old_logic = r"document\.querySelectorAll\('\.node-hex-hover'\)\.forEach\(el => \{.*?(?=\s+document\.getElementById\('cc-total-nodes'\)\.innerText)/s"
# Actually, re.sub with complex logic might fail. I'll just find the exact block and replace it.
