import re

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a polling interval for cluster detail view
if 'let detailMetricsInterval = null;' not in content:
    content = content.replace('let previousMetrics = {};', 'let previousMetrics = {};\n    let detailMetricsInterval = null;\n    let currentDetailProj = null;')
    
    # In showDetailView, set currentDetailProj and start polling
    old_show = "refreshClusterDetailMetrics(proj);"
    new_show = """currentDetailProj = proj;
            refreshClusterDetailMetrics(proj);
            clearInterval(detailMetricsInterval);
            detailMetricsInterval = setInterval(() => {
                if (document.getElementById('project-detail-view').style.display !== 'none' && currentDetailProj) {
                    refreshClusterDetailMetrics(currentDetailProj);
                }
            }, 5000);"""
    content = content.replace(old_show, new_show)
    
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added polling to main.js")
