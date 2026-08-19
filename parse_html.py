from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        if tag in ['div', 'section', 'main']:
            self.stack.append((tag, self.getpos()))
            attrs_dict = dict(attrs)
            if 'id' in attrs_dict:
                print(f"Start: {tag} id={attrs_dict['id']} at {self.getpos()} stack_len={len(self.stack)}")
            elif 'class' in attrs_dict and 'main-content' in attrs_dict['class']:
                print(f"Start: {tag} class={attrs_dict['class']} at {self.getpos()} stack_len={len(self.stack)}")

    def handle_endtag(self, tag):
        if tag in ['div', 'section', 'main']:
            if not self.stack:
                self.errors.append(f"Unexpected end tag {tag} at {self.getpos()}")
                return
            last_tag, _ = self.stack.pop()
            if last_tag != tag:
                self.errors.append(f"Mismatched end tag {tag} at {self.getpos()}, expected {last_tag}")

parser = MyHTMLParser()
with open('fastapi_app/templates/index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())
print("Errors:")
for e in parser.errors[:10]: print(e)
