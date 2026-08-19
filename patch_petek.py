import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the positions
old_positions = """const positions = [
                    {x:20, y:20}, {x:76, y:20}, {x:132, y:20}, {x:188, y:20},
                    {x:48, y:68}, {x:104, y:68}, {x:160, y:68},
                    {x:20, y:116}, {x:76, y:116}, {x:132, y:116}, {x:188, y:116}
                ];"""
new_positions = """const positions = [
                    {x:20, y:20}, {x:62, y:20}, {x:104, y:20}, {x:146, y:20},
                    {x:41, y:54}, {x:83, y:54}, {x:125, y:54},
                    {x:20, y:88}, {x:62, y:88}, {x:104, y:88}, {x:146, y:88}
                ];"""
content = content.replace(old_positions, new_positions)

# Replace the polyPoints and polygon group
old_poly = """const polyPoints = "32,0 60,16 60,48 32,65 4,48 4,16";
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})">
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" />
                    </g>`;"""

new_poly = """const polyPoints = "22,0 42,11 42,34 22,46 3,34 3,11";
                    
                    hexHtml += `<g class="node-hex-hover" data-idx="${idx}" style="cursor:pointer;" transform="translate(${pos.x}, ${pos.y})"
                        onmouseover="let p = this.querySelector('polygon'); p.setAttribute('data-orig-fill', p.getAttribute('fill')); p.setAttribute('fill', 'white'); p.setAttribute('stroke', '${node.color}');"
                        onmouseout="let p = this.querySelector('polygon'); p.setAttribute('fill', p.getAttribute('data-orig-fill')); p.setAttribute('stroke', 'var(--glass-bg)');"
                    >
                        <polygon class="node-petek" points="${polyPoints}" fill="${node.color}" stroke="var(--glass-bg)" stroke-width="3" style="transition: all 0.2s ease;" />
                    </g>`;"""
content = content.replace(old_poly, new_poly)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated petek UI in JS.")
