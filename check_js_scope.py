content = open('fastapi_app/static/main.js', encoding='utf-8').read()

# Check exact placement of fetchNodesPage - is it inside a DOMContentLoaded or outside?
idx = content.find('async function fetchNodesPage()')
surrounding = content[max(0,idx-200):idx+50]
print("Context before fetchNodesPage:")
print(repr(surrounding))
print()

# Count DOMContentLoaded openings and closings before fetchNodesPage
chunk_before = content[:idx]
opens = chunk_before.count("document.addEventListener('DOMContentLoaded'")
# Count });  that close DOMContentLoaded blocks
# Count how many DOMContentLoaded blocks have been fully closed
print(f"DOMContentLoaded opens before fetchNodesPage: {opens}")

# Check the handleRouting function to see if nodes-view is there
hr_idx = content.find('function handleRouting()')
hr_chunk = content[hr_idx:hr_idx+1000]
print("\nhandleRouting content:")
print(hr_chunk)
