# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old hardcoded nodesSvg tooltip
old_hover = """// Nodes Donut Tooltip
const nodesSvg = document.getElementById('nodes-donut-svg');
const tooltip = document.getElementById('custom-tooltip');
if (nodesSvg && tooltip) {
    nodesSvg.addEventListener('mousemove', (e) => {
        tooltip.style.display = 'block';
        tooltip.innerHTML = '4 Operational';
        tooltip.style.left = (e.pageX + 10) + 'px';
        tooltip.style.top = (e.pageY + 10) + 'px';
    });
    nodesSvg.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
    });
}"""

content = content.replace(old_hover, "")

# Add logic to fetch function
nodes_logic = """
                document.getElementById('cc-total-nodes').innerText = allNodes.length + ' Nodes';
                
                const dnCenter = document.getElementById('nodes-donut-center-num');
                if (dnCenter) dnCenter.innerText = allNodes.length;

                const dnSlice = document.getElementById('nodes-donut-slice');
                if (dnSlice) {
                   if (allNodes.length === 0) dnSlice.style.strokeDashoffset = '439.8';
                   else {
                       const ratio = (allNodes.length - shutDownCount) / allNodes.length;
                       dnSlice.style.strokeDashoffset = 439.8 * (1 - ratio);
                       
                       const donutTooltip = document.getElementById('donut-hover-tooltip');
                       const donutText = document.getElementById('donut-hover-text');
                       if (donutTooltip && donutText) {
                           dnSlice.addEventListener('mouseenter', (e) => {
                               donutText.innerText = `${allNodes.length - shutDownCount} Operational`;
                               donutTooltip.style.display = 'block';
                           });
                           dnSlice.addEventListener('mousemove', (e) => {
                               donutTooltip.style.left = (e.clientX + 10) + 'px';
                               donutTooltip.style.top = (e.clientY + 10) + 'px';
                           });
                           dnSlice.addEventListener('mouseleave', () => {
                               donutTooltip.style.display = 'none';
                           });
                       }
                   }
                }
"""

content = re.sub(r"document\.getElementById\('cc-total-nodes'\)\.innerText = allNodes\.length \+ ' Nodes';\s*const dnSlice = document\.getElementById\('nodes-donut-slice'\);\s*if \(dnSlice\) \{\s*if \(allNodes\.length === 0\) dnSlice\.style\.strokeDashoffset = '439\.8';\s*else \{\s*const ratio = \(allNodes\.length - shutDownCount\) / allNodes\.length;\s*dnSlice\.style\.strokeDashoffset = 439\.8 \* \(1 - ratio\);\s*\}\s*\}", nodes_logic.strip().replace('\\', '\\\\'), content)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS nodes donut patched")
