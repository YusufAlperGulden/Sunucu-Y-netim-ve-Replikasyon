import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "class Particle {"
end_marker = "const canvas = document.getElementById('login-canvas');"

start_idx = content.find(start_marker)

# To find where the class ends, let's find `draw() { ... }` then the end of the class.
# We will just replace from `class Particle {` to `particles.push(new Particle());`

replace_start = content.find("class Particle {")
replace_end = content.find("for (let i = 0; i < 40; i++) {")

new_particle_class = """class Particle {
            constructor() {
                this.size = Math.random() * 80 + 30;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                
                // Start them randomly around the edges
                if (Math.random() > 0.5) {
                    this.x = Math.random() > 0.5 ? -this.size : width + this.size;
                    this.y = Math.random() * height;
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() > 0.5 ? -this.size : height + this.size;
                }
                
                this.vx = (Math.random() - 0.5) * 1.0;
                this.vy = (Math.random() - 0.5) * 1.0;
                
                if (Math.abs(this.vx) < 0.2) this.vx = 0.5 * Math.sign(this.vx || 1);
                if (Math.abs(this.vy) < 0.2) this.vy = 0.5 * Math.sign(this.vy || 1);
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                
                // Exclusion zone for the Title and Login Box
                // Approximate size: 850px wide, 550px tall, centered
                const boxW = 850;
                const boxH = 550;
                const boxX = width / 2 - boxW / 2;
                const boxY = height / 2 - boxH / 2;
                
                let testX = this.x;
                let testY = this.y;
                
                if (this.x < boxX) testX = boxX;
                else if (this.x > boxX + boxW) testX = boxX + boxW;
                
                if (this.y < boxY) testY = boxY;
                else if (this.y > boxY + boxH) testY = boxY + boxH;
                
                let distX = this.x - testX;
                let distY = this.y - testY;
                let distance = Math.sqrt((distX*distX) + (distY*distY));
                
                if (distance <= this.size) {
                    // Collision! Bounce out smoothly
                    if (Math.abs(distX) > Math.abs(distY)) {
                        this.vx *= -1;
                        this.x += Math.sign(distX) * 2;
                    } else {
                        this.vy *= -1;
                        this.y += Math.sign(distY) * 2;
                    }
                }
                
                // Screen edges collision
                if (this.x - this.size > width) { this.x = width - this.size; this.vx *= -1; }
                if (this.x + this.size < 0) { this.x = -this.size; this.vx *= -1; }
                if (this.y - this.size > height) { this.y = height - this.size; this.vy *= -1; }
                if (this.y + this.size < 0) { this.y = -this.size; this.vy *= -1; }
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = 0.5;
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
        
        """

content = content[:replace_start] + new_particle_class + content[replace_end:]

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Particle patched")
