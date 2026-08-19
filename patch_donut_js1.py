import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the line that accesses cc-donut-center-text
content = content.replace("document.getElementById('cc-donut-center-text').style.color = donutCircle.style.stroke;", "// removed center text")

# Add hover listeners to cc-donut-progress
hover_logic = """
            // Donut hover logic
            const donutCircle = document.getElementById('cc-donut-progress');
            const donutTooltip = document.getElementById('donut-hover-tooltip');
            const donutText = document.getElementById('donut-hover-text');
            
            if (donutCircle && donutTooltip) {
                donutCircle.addEventListener('mouseenter', (e) => {
                    donutText.innerText = `${operationalCount} Operational`;
                    donutTooltip.style.display = 'block';
                });
                donutCircle.addEventListener('mousemove', (e) => {
                    donutTooltip.style.left = (e.clientX + 10) + 'px';
                    donutTooltip.style.top = (e.clientY + 10) + 'px';
                });
                donutCircle.addEventListener('mouseleave', () => {
                    donutTooltip.style.display = 'none';
                });
            }
"""

# Insert it around where the data is fetched and operationalCount is calculated.
# In main.js, this happens in the '/api/clusters' fetch then block. Let's find it.
