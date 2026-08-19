import re

models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

user_model = """
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="viewer") # "admin" or "viewer"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""

if "class User(Base)" not in content:
    content += "\n" + user_model
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added User model to models.py")
else:
    print("User model already exists")
