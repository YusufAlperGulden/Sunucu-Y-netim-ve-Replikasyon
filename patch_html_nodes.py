import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the hardcoded stat values in nodes-view section
replacements = [
    # Operational card - has hardcoded 4
    ('filterNodes(\'Operational\', this)', 'stat-operational', '>4<', '" id="stat-operational">-<'),
    # All card - has hardcoded 4
    ('filterNodes(\'All\', this)', 'stat-all', '>4<', '" id="stat-all">-<'),
]

# Find and fix the nodes view status cards
# Operational card
if 'id="stat-operational"' not in content:
    # Pattern: inside filterNodes('Operational', this) card, has value "4"
    content = re.sub(
        r'(onclick="filterNodes\(\'Operational\', this\)"[^>]*>.*?font-size: 1\.5rem; font-weight: 500;"\s*>)4(<)',
        r'\g<1><span id="stat-operational">-</span>\2',
        content,
        flags=re.DOTALL
    )

# All card
if 'id="stat-all"' not in content:
    content = re.sub(
        r'(onclick="filterNodes\(\'All\', this\)"[^>]*>.*?font-size: 1\.5rem; font-weight: 500;"\s*>)4(<)',
        r'\g<1><span id="stat-all">-</span>\2',
        content,
        flags=re.DOTALL
    )

# Failed card
if 'id="stat-failed"' not in content:
    content = re.sub(
        r'(onclick="filterNodes\(\'Failed\', this\)"[^>]*>.*?font-size: 1\.5rem; font-weight: 500;"\s*>)0(<)',
        r'\g<1><span id="stat-failed">0</span>\2',
        content,
        flags=re.DOTALL
    )

# Offline card
if 'id="stat-offline"' not in content:
    content = re.sub(
        r'(onclick="filterNodes\(\'Offline\', this\)"[^>]*>.*?font-size: 1\.5rem; font-weight: 500;"\s*>)0(<)',
        r'\g<1><span id="stat-offline">0</span>\2',
        content,
        flags=re.DOTALL
    )

# Check tbody
if 'nodes-page-tbody' not in content:
    content = re.sub(
        r'(<table[^>]*>.*?<tbody>)',
        r'<table style="width: 100%; border-collapse: collapse; text-align: left;"><tbody id="nodes-page-tbody">',
        content,
        count=1,
        flags=re.DOTALL
    )
    print("Added nodes-page-tbody id")
else:
    print("nodes-page-tbody already exists")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching HTML nodes view")
