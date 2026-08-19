# -*- coding: utf-8 -*-
with open('fastapi_app/static/style.css', 'a', encoding='utf-8') as f:
    f.write("\n.sidebar-nav a.submenu-item { background: transparent !important; color: #d1d5db !important; border-left: none !important; padding: 8px 16px 8px 32px !important; font-size: 0.85rem; }\n")
    f.write(".sidebar-nav a.submenu-item:hover { color: #ffffff !important; background: rgba(255,255,255,0.05) !important; }\n")
