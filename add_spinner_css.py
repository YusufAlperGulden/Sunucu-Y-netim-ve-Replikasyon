content = open('fastapi_app/templates/index.html', encoding='utf-8').read()

# Find where to insert CSS - before </style> in head
SPINNER_CSS = """
/* ---- LOADING SPINNER ---- */
@keyframes cc-spin {
    to { transform: rotate(360deg); }
}
.cc-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top-color: var(--primary, #6366f1);
    border-radius: 50%;
    animation: cc-spin 0.8s linear infinite;
    display: inline-block;
}
.cc-spinner-sm {
    width: 18px;
    height: 18px;
    border-width: 2px;
}
.cc-spinner-lg {
    width: 48px;
    height: 48px;
    border-width: 4px;
}
.cc-loading-row td {
    text-align: center;
    padding: 60px 20px !important;
}
"""

if 'cc-spinner' not in content:
    content = content.replace('</style>', SPINNER_CSS + '\n</style>', 1)
    print("Added spinner CSS")
else:
    print("Already exists")

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
