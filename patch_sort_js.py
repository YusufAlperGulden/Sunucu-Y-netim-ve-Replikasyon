import re

with open('fastapi_app/static/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

sort_logic = """
    let currentSortCol = null;
    let currentSortDir = null; // 'asc', 'desc', null

    window.sortNodes = function(col) {
        if (currentSortCol !== col) {
            currentSortCol = col;
            currentSortDir = 'asc';
        } else {
            if (currentSortDir === 'asc') currentSortDir = 'desc';
            else if (currentSortDir === 'desc') currentSortDir = null;
            else currentSortDir = 'asc';
        }
        
        // Reset all tooltips and arrows
        ['host', 'port', 'status', 'type', 'role', 'cluster', 'seen'].forEach(c => {
            const arr = document.getElementById('nodes-sort-arrows-' + c);
            const txt = document.getElementById('nodes-sort-text-' + c);
            if(arr) arr.innerHTML = '&#9650;&#9660;';
            if(txt) txt.innerText = 'Click to sort ascending';
        });
        
        // Update current
        if (currentSortDir) {
            const arr = document.getElementById('nodes-sort-arrows-' + col);
            const txt = document.getElementById('nodes-sort-text-' + col);
            if (currentSortDir === 'asc') {
                if(arr) arr.innerHTML = '&#9650;';
                if(txt) txt.innerText = 'Click to sort descending';
            } else {
                if(arr) arr.innerHTML = '&#9660;';
                if(txt) txt.innerText = 'Click to Cancel Sorting';
            }
        }
        
        renderNodesPage();
    };

    function renderNodesPage() {
        const tbody = document.getElementById('nodes-page-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';
        
        let filteredData = nodesPageData.filter(n => currentFilter === 'All' || n.status === currentFilter);
        
        if (currentSortDir) {
            filteredData.sort((a, b) => {
                let valA = a[currentSortCol];
                let valB = b[currentSortCol];
                
                // For nested fields like cluster, sort by name
                if (currentSortCol === 'cluster') {
                    // Extract text before (ID:xx) if needed, but string comparison works fine
                }
                
                if (valA < valB) return currentSortDir === 'asc' ? -1 : 1;
                if (valA > valB) return currentSortDir === 'asc' ? 1 : -1;
                return 0;
            });
        }
"""

content = content.replace('    function renderNodesPage() {\n        const tbody = document.getElementById(\'nodes-page-tbody\');\n        if(!tbody) return;\n        tbody.innerHTML = \'\';\n        \n        const filteredData = nodesPageData.filter(n => currentFilter === \'All\' || n.status === currentFilter);', sort_logic.strip())

with open('fastapi_app/static/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS sorting logic patched")
