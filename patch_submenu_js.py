# -*- coding: utf-8 -*-
import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

submenu_logic = """
              const submenu = document.getElementById('clusters-submenu');
              if (submenu) {
                  submenu.innerHTML = '';
                  data.forEach(proj => {
                      let isOperational = proj.nodesCount > 0 && proj.sync_status !== 'FAILED';
                      let color = isOperational ? 'var(--success)' : 'var(--danger)';
                      
                      let a = document.createElement('a');
                      a.href = "#";
                      a.className = "submenu-item";
                      a.innerHTML = `<span style="color: ${color}; font-size: 1.2rem; line-height: 1;">&#8226;</span> <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px;">${proj.name}</span>`;
                      submenu.appendChild(a);
                  });
              }
"""

# Insert it around where data is looped, right after let allNodes = [];
content = content.replace("let allNodes = [];", "let allNodes = [];" + submenu_logic)

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS submenu logic added")
