import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the lines setting the center text
content = content.replace("document.getElementById('cc-donut-center-text').innerText = operationalCount;", "// center text removed")
content = content.replace("document.getElementById('cc-donut-center-text').style.color = donutCircle.style.stroke;", "// center text style removed")

# Add hover listeners inside the block where operationalCount is updated
hover_code = """
            if (donutCircle) {
                donutCircle.style.strokeDashoffset = offset;
                donutCircle.style.stroke = ratio === 1 ? 'var(--success)' : (ratio > 0 ? 'var(--warning)' : 'var(--danger)');
                
                // Add hover logic
                const donutTooltip = document.getElementById('donut-hover-tooltip');
                const donutText = document.getElementById('donut-hover-text');
                if (donutTooltip && donutText) {
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
            }
"""

content = content.replace("""            if (donutCircle) {
                donutCircle.style.strokeDashoffset = offset;
                donutCircle.style.stroke = ratio === 1 ? 'var(--success)' : (ratio > 0 ? 'var(--warning)' : 'var(--danger)');
                // center text style removed
            }""", hover_code.strip())

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS patched for donut tooltip")
