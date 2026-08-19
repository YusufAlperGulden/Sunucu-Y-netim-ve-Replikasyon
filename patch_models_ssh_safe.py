models_path = 'fastapi_app/models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    encrypted_url = Column(String(500))
    
    project = relationship("Project", back_populates="nodes")"""

replacement = """    encrypted_url = Column(String(500))
    
    ssh_host = Column(String(255), nullable=True)
    ssh_port = Column(Integer, default=22)
    ssh_username = Column(String(255), default="root")
    encrypted_ssh_credential = Column(String, nullable=True)
    
    project = relationship("Project", back_populates="nodes")"""

if target in content:
    content = content.replace(target, replacement)
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added SSH columns")
else:
    print("Target not found")
