# -*- coding: utf-8 -*-
with open('fastapi_app/static/style.css', 'a', encoding='utf-8') as f:
    f.write("\n.sidebar.collapsed #clusters-chevron { display: none !important; }\n")
    f.write(".sidebar.collapsed #clusters-submenu { display: none !important; }\n")
