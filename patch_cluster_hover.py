# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I will add a global variable for the timeout
if 'let clusterHoverTimeout = null;' not in content:
    content = content.replace("let dashboardInterval = null;", "let dashboardInterval = null;\n    let clusterHoverTimeout = null;")

# Now replace tr.onmouseenter and tr.onmouseleave
# Note: since tr.onmouseenter is large, I'll use regex to match from `tr.onmouseenter = (e) => {` to `ct.style.left = (rect.left + 50) + 'px'; \n                    } \n                };`
# Actually, it's safer to just split and replace.

old_enter = """tr.onmouseenter = (e) => { 
                    tr.style.backgroundColor = 'rgba(0,0,0,0.02)'; 
                    const ct = document.getElementById('cluster-hover-tooltip');"""

new_enter = """tr.onmouseenter = (e) => { 
                    tr.style.backgroundColor = 'rgba(0,0,0,0.02)'; 
                    clearTimeout(clusterHoverTimeout);
                    clusterHoverTimeout = setTimeout(() => {
                    const ct = document.getElementById('cluster-hover-tooltip');"""

old_enter_end = """                        ct.style.display = 'block'; 
                        let topPos = rect.bottom + 5; 
                        if (topPos + 350 > window.innerHeight) topPos = rect.top - 350; 
                        ct.style.top = topPos + 'px'; 
                        ct.style.left = (rect.left + 50) + 'px'; 
                    } 
                };"""

new_enter_end = """                        ct.style.display = 'block'; 
                        ct.style.opacity = '0';
                        ct.style.transform = 'translateY(10px)';
                        
                        setTimeout(() => {
                            ct.style.opacity = '1';
                            ct.style.transform = 'translateY(0)';
                        }, 10);
                        
                        let topPos = rect.bottom + 5; 
                        if (topPos + 350 > window.innerHeight) topPos = rect.top - 350; 
                        ct.style.top = topPos + 'px'; 
                        ct.style.left = (rect.left + 50) + 'px'; 
                    } 
                    }, 200);
                };"""

old_leave = "tr.onmouseleave = (e) => { tr.style.backgroundColor = 'transparent'; const ct = document.getElementById('cluster-hover-tooltip'); if (ct) ct.style.display = 'none'; };"
new_leave = """tr.onmouseleave = (e) => { 
                    tr.style.backgroundColor = 'transparent'; 
                    clearTimeout(clusterHoverTimeout);
                    const ct = document.getElementById('cluster-hover-tooltip'); 
                    if (ct) { 
                        ct.style.opacity = '0'; 
                        ct.style.transform = 'translateY(10px)';
                        setTimeout(() => {
                            if(ct.style.opacity === '0') ct.style.display = 'none';
                        }, 200);
                    } 
                };"""

content = content.replace(old_enter, new_enter)
content = content.replace(old_enter_end, new_enter_end)
content = content.replace(old_leave, new_leave)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS cluster hover patched")
