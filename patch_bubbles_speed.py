import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Make slower
content = content.replace(
    'this.vx = (Math.random() - 0.5) * 1.0;',
    'this.vx = (Math.random() - 0.5) * 0.4;'
)
content = content.replace(
    'this.vy = (Math.random() - 0.5) * 1.0;',
    'this.vy = (Math.random() - 0.5) * 0.4;'
)
content = content.replace(
    'if (Math.abs(this.vx) < 0.2) this.vx = 0.5 * Math.sign(this.vx || 1);',
    'if (Math.abs(this.vx) < 0.1) this.vx = 0.2 * Math.sign(this.vx || 1);'
)
content = content.replace(
    'if (Math.abs(this.vy) < 0.2) this.vy = 0.5 * Math.sign(this.vy || 1);',
    'if (Math.abs(this.vy) < 0.1) this.vy = 0.2 * Math.sign(this.vy || 1);'
)

# Shrink the box
content = content.replace(
    'const boxW = 850;',
    'const boxW = 500;'
)
content = content.replace(
    'const boxH = 550;',
    'const boxH = 500;'
)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS patched successfully")
