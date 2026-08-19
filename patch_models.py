import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# read existing to check
with open('fastapi_app/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

if "class OperationalReport" not in content:
    with open('fastapi_app/models.py', 'a', encoding='utf-8') as f:
        f.write("\nclass OperationalReport(Base):\n")
        f.write("    __tablename__ = 'operational_reports'\n")
        f.write("    id = Column(Integer, primary_key=True, index=True)\n")
        f.write("    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))\n")
        f.write("    report_type = Column(String(255))\n")
        f.write("    data_range_days = Column(Integer, default=7)\n")
        f.write("    recipients = Column(String(500))\n")
        f.write("    file_name = Column(String(255))\n")
        f.write("    created_by = Column(String(100), default='admin')\n")
        f.write("    created_at = Column(DateTime, default=datetime.datetime.utcnow)\n")
        f.write("\n    project = relationship('Project')\n")
    print("Added OperationalReport model")
else:
    print("Already exists")
