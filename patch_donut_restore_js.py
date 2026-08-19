import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "// center text removed",
    "document.getElementById('cc-donut-center-text').innerText = operationalCount;"
)

# Insert the color update logic back
color_update = """
                if (donutTooltip && donutText) {
                    donutCircle.addEventListener('mouseenter', (e) => {
"""

color_update_replacement = """
                document.getElementById('cc-donut-center-text').style.color = donutCircle.style.stroke;
                if (donutTooltip && donutText) {
                    donutCircle.addEventListener('mouseenter', (e) => {
"""

content = content.replace(color_update.strip(), color_update_replacement.strip())

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS center text restored")
