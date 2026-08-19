import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace hexHtml generation
old_hexHtml_block = r'// Draw Honeycomb.*?hcContainer\.innerHTML = hexHtml;'

new_hexHtml_block = """// Draw Honeycomb
            const hcContainer = document.getElementById('nodes-honeycomb');
            if (hcContainer) {
                // Made smaller, scaled down by ~0.65
                let hexHtml = '<svg width="100%" height="200" viewBox="0 0 240 200">';
                
                // New positions for smaller hexagons
                // width ~56, height ~65
                const positions = [
                    {x:20, y:20}, {x:76, y:20}, {x:132, y:20}, {x:188, y:20},
                    {x:48, y:68}, {x:104, y:68}, {x:160, y:68},
                    {x:20, y:116}, {x:76, y:116}, {x:132, y:116}, {x:188, y:116}
                ];
                
                let shutDownCount = 0;
                
                allNodes.forEach((node, idx) => {
                    if (node.status === 'Shut Down') shutDownCount++;
                    
                    const pos = positions[idx % positions.length];
                    
                    let nodeType = 'PostgreSQL';
                    if (node.vendorType === 'mariadb') nodeType = 'MariaDB';
                    if (node.vendorType === 'percona_mysql') nodeType = 'Percona';
                    if (node.vendorType === 'mongo') nodeType = 'MongoDB';
                    if (node.vendorType === 'timescale') nodeType = 'TimescaleDB';
                    
                    let roleBadge = '';
                    if (node.role && node.role.toLowerCase() === 'primary') roleBadge = '<span style="background: rgba(34,197,94,0.1); color: var(--success); border: 1px solid var(--success);">Writable</span>';
                    else if (node.role && node.role.toLowerCase() === 'replica') roleBadge = '<span style="background: rgba(107,114,128,0.1); color: #6b7280; border: 1px solid #d1d5db;">Readonly</span>';
                    
                    // The smaller polygon points (scaled from original)
                    const polyPoints = "32,0 60,16 60,48 32,65 4,48 4,16";
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})">
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" />
                    </g>`;
                    
                    window['nodeData_' + idx] = {
                        hostname: node.name,
                        port: node.role === 'ProxySQL' ? 6032 : (nodeType === 'PostgreSQL' ? 5432 : 3306),
                        status: node.status,
                        role: node.role ? (node.role.charAt(0).toUpperCase() + node.role.slice(1)) : 'None',
                        type: nodeType,
                        cluster: `${node.clusterName} (ID:${node.clusterId})`,
                        badge: roleBadge,
                        color: node.color
                    };
                });
                hexHtml += '</svg>';
                hcContainer.innerHTML = hexHtml;"""

js_content = re.sub(old_hexHtml_block, new_hexHtml_block, js_content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated main.js")
