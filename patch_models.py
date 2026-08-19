import re

model_path = 'fastapi_app/models.py'
with open(model_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_model = """class ProjectSettings(Base):
    __tablename__ = "project_settings"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), unique=True)
    settings_json = Column(String(5000), default="{}")
    
    project = relationship("Project")

class SyncJob"""

if "class ProjectSettings" not in content:
    content = content.replace("class SyncJob", new_model)
    with open(model_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added ProjectSettings model")
else:
    print("ProjectSettings model already exists")
