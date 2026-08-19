import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'this\.speed = Math\.random\(\) \* 0\.4 \+ 0\.1;',
    'this.speed = Math.random() * 0.15 + 0.05;',
    content
)

content = re.sub(
    r'this\.swirl = \(Math\.random\(\) - 0\.5\) \* 0\.02;',
    'this.swirl = (Math.random() - 0.5) * 0.005;',
    content
)

content = re.sub(
    r'this\.size = Math\.random\(\) \* 20 \+ 8;',
    'this.size = Math.random() * 80 + 30;',
    content
)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
