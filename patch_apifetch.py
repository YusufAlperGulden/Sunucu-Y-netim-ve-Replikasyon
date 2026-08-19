import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace apiFetch
old_api = """async function apiFetch(url, options = {}) {
    options.headers = options.headers || {};
    if (globalAuthToken) {
        options.headers['Authorization'] = 'Basic ' + globalAuthToken;
    }
    return fetch(url, options);
}"""

new_api = """async function apiFetch(url, options = {}) {
    options.headers = options.headers || {};
    if (globalAuthToken) {
        options.headers['Authorization'] = 'Basic ' + globalAuthToken;
    }
    const res = await fetch(url, options);
    if (res.status === 401) {
        // Show login screen if unauthorized
        const loginScreen = document.getElementById('login-screen');
        if(loginScreen) {
            loginScreen.style.display = 'flex';
        }
        localStorage.removeItem('auth_token');
        globalAuthToken = null;
    }
    return res;
}"""

content = content.replace(old_api, new_api)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed apiFetch to handle 401")
