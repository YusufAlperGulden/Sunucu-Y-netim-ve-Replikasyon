import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.html', '.js', '.css', '.py')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'Giriş' in content or 'Giris' in content or 'bubble' in content or 'circle' in content:
                        if 'node_modules' not in path and '.git' not in path:
                            print(path)
            except Exception:
                pass
