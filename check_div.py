import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def check_div(view_id):
    match = re.search(f'(<div id="{view_id}".*?)<!-- End {view_id} -->', content, re.DOTALL)
    # wait, there's no end comment. Let's find the closing div of the view.
    # Actually, let's just parse the DOM or just count the entire html file BEFORE users-view!
