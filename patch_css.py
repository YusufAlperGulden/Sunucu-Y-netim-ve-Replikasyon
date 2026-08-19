css_path = 'fastapi_app/static/style.css'
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("""
.cluster-tab {
    text-decoration: none;
    color: #6b7280;
    padding-bottom: 12px;
    margin-bottom: -1px;
    font-weight: 500;
}
.cluster-tab:hover {
    color: #374151;
}
.cluster-tab.active {
    color: #6366f1;
    border-bottom: 2px solid #6366f1;
}
.cluster-subtab {
    text-decoration: none;
    color: #6b7280;
    font-weight: 500;
}
.cluster-subtab:hover {
    color: #374151;
}
""")
print("Updated style.css")
