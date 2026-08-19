import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
"""        for (let i = 0; i < 250; i++) {
            particles.push(new Particle());
            // Fast forward initial particles slightly so it's not starting from absolute center
            particles[i].x = width / 2 + Math.cos(particles[i].angle) * particles[i].radius;
            particles[i].y = height / 2 + Math.sin(particles[i].angle) * particles[i].radius;
        }""",
"""        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
            // Fast forward a little bit
            for(let j=0; j<Math.random()*100; j++) particles[i].update();
        }"""
)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Loop patched")
