# -*- coding: utf-8 -*-
with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix login
login_bad = '''    // Login Logic
    const attemptLogin = () => {
        const u = loginUsername.value.trim();
        const p = loginPassword.value.trim();
        if (u === 'admin' && p === 'admin123') {
            globalAuthToken = btoa(u + ':' + p);
            loginScreen.style.transition = 'opacity 0.3s ease';
            loginScreen.style.opacity = '0';
            setTimeout(() => {
                loginScreen.style.display = 'none';
            }, 300);
            
            // Only fetch initial data after successful login
            fetchProjects();
        } else {
            loginError.style.display = 'block';
            setTimeout(() => loginError.style.display = 'none', 3000);
        }
    };'''

login_good = '''    // Login Logic
    const attemptLogin = async () => {
        const u = loginUsername.value.trim();
        const p = loginPassword.value.trim();
        const token = btoa(u + ':' + p);
        try {
            const res = await fetch('/api/auth/verify', {
                headers: { 'Authorization': 'Basic ' + token }
            });
            if (res.ok) {
                globalAuthToken = token;
                loginScreen.style.transition = 'opacity 0.3s ease';
                loginScreen.style.opacity = '0';
                setTimeout(() => {
                    loginScreen.style.display = 'none';
                }, 300);
                
                // Only fetch initial data after successful login
                fetchProjects();
            } else {
                loginError.style.display = 'block';
                loginError.innerText = 'Invalid username or password';
                setTimeout(() => loginError.style.display = 'none', 3000);
            }
        } catch (err) {
            loginError.style.display = 'block';
            loginError.innerText = 'Connection to server failed';
            setTimeout(() => loginError.style.display = 'none', 3000);
        }
    };'''
text = text.replace(login_bad, login_good)

# Escape node name and role in projects view (around line 122)
text = text.replace(
    '<h3></h3>',
    '<h3></h3>'
)
text = text.replace(
    '',
    ''
)

# Fix currentProjectId in Settings
text = text.replace(
    'const settingsProject = currentProjectId || 1;',
    'const settingsProject = currentProjectId;'
)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done modifying main.js')
