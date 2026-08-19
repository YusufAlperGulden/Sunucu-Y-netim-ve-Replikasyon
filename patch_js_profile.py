import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

profile_js = """
async function fetchProfile() {
    try {
        const res = await apiFetch('/api/users/me');
        if (res.ok) {
            const data = await res.json();
            const avatar = document.getElementById('profile-avatar');
            const fullname = document.getElementById('profile-fullname');
            const role = document.getElementById('profile-role');
            const username = document.getElementById('profile-username');
            const team = document.getElementById('profile-team');
            
            if (avatar) avatar.innerText = data.username.substring(0, 2);
            if (fullname) fullname.innerText = data.username;
            if (role) role.innerText = data.role;
            if (username) username.innerText = data.username;
            if (team) team.innerText = data.team;
        }
    } catch (e) {
        console.error("Failed to fetch profile", e);
    }
}
"""

if "fetchProfile" not in content:
    content += "\n" + profile_js
    
    # inject into Settings view routing
    if "else if (hash === 'settings-view') {" in content:
        content = content.replace("else if (hash === 'settings-view') {\n            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();", "else if (hash === 'settings-view') {\n            if(typeof stopDashboardInterval === 'function') stopDashboardInterval();\n            if(typeof fetchProfile === 'function') fetchProfile();")
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added fetchProfile")
else:
    print("fetchProfile already exists")
