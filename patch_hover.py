import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Make sure clusterHoverTimeout is declared
if 'let clusterHoverTimeout' not in js_content:
    js_content = js_content.replace('let currentProjectId = null;', 'let currentProjectId = null;\n    let clusterHoverTimeout = null;')

# The old tr.onmouseenter and onmouseleave logic:
old_mouseleave = """                tr.onmouseleave = (e) => { 
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

new_mouseleave = """                tr.onmouseleave = (e) => { 
                    tr.style.backgroundColor = 'transparent'; 
                    clearTimeout(clusterHoverTimeout);
                    const ct = document.getElementById('cluster-hover-tooltip'); 
                    if (ct) { 
                        // Start hide timeout
                        clusterHoverTimeout = setTimeout(() => {
                            ct.style.opacity = '0'; 
                            ct.style.transform = 'translateY(10px)';
                            setTimeout(() => {
                                if(ct.style.opacity === '0') ct.style.display = 'none';
                            }, 200);
                        }, 50); // small delay to allow mouse to enter the tooltip
                    } 
                };"""

js_content = js_content.replace(old_mouseleave, new_mouseleave)

# We also need to add ct.onmouseenter and ct.onmouseleave ONCE. We can put it right inside the API fetch response loop, or outside.
# Let's add it outside the fetchProjects function, or just globally.

global_ct_events = """
    // Global tooltip hover events
    const clusterTooltip = document.getElementById('cluster-hover-tooltip');
    if (clusterTooltip) {
        clusterTooltip.addEventListener('mouseenter', () => {
            clearTimeout(clusterHoverTimeout);
        });
        clusterTooltip.addEventListener('mouseleave', () => {
            clusterHoverTimeout = setTimeout(() => {
                clusterTooltip.style.opacity = '0';
                clusterTooltip.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    if(clusterTooltip.style.opacity === '0') clusterTooltip.style.display = 'none';
                }, 200);
            }, 100);
        });
    }
"""

if 'clusterTooltip.addEventListener' not in js_content:
    # insert it before fetchProjects
    js_content = js_content.replace('async function fetchProjects() {', global_ct_events + '\n    async function fetchProjects() {')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated hover logic.")
