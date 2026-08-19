js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Add changelog anchor protection at the start of handleRouting
old_routing_start = """function handleRouting() {
        let hash = window.location.hash.substring(1) || 'projects-view';
        
        sidebarLinks.forEach(l => l.classList.remove('active'));"""

new_routing_start = """function handleRouting() {
        let hash = window.location.hash.substring(1) || 'projects-view';
        
        // If hash is a changelog section anchor (e.g. v1-4-2), show changelog-view and scroll
        const changelogAnchors = ['v1-4-2', 'v1-4-1', 'v1-4-0', 'v1-3-0'];
        if (changelogAnchors.includes(hash)) {
            document.querySelectorAll('.view-section').forEach(s => s.style.display = 'none');
            const cv = document.getElementById('changelog-view');
            if (cv) { cv.style.display = 'block'; }
            setTimeout(() => {
                const el = document.getElementById(hash);
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            }, 100);
            const cl = document.querySelector('a[data-view="changelog-view"]');
            if (cl) { sidebarLinks.forEach(l => l.classList.remove('active')); cl.classList.add('active'); }
            return;
        }
        
        sidebarLinks.forEach(l => l.classList.remove('active'));"""

if "changelogAnchors" not in js:
    js = js.replace(old_routing_start, new_routing_start)
    print("Added changelog anchor protection")
else:
    print("Already exists")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
