from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    nodes = relationship("DatabaseNode", back_populates="project", cascade="all, delete-orphan")

class DatabaseNode(Base):
    """
    Represents a database node within a project (e.g. Primary, Standby).
    The db_url_encrypted stores the actual connection string securely.
    """
    __tablename__ = "database_nodes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(120), nullable=False) # e.g., 'Frankfurt Primary'
    role = Column(String(50), nullable=False, default="PRIMARY") # PRIMARY, STANDBY, READ_REPLICA
    db_url_encrypted = Column(Text, nullable=False)
    
    # Health and Sync Status
    is_healthy = Column(Boolean, default=False)
    last_health_check = Column(DateTime, nullable=True)
    replication_lag_bytes = Column(Integer, default=0)
    
    # Logical Replication Tracking
    is_replication_active = Column(Boolean, default=False)
    sync_status = Column(String(50), default="UNKNOWN") # PENDING, SYNCING, READY, FAILED
    
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="nodes")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    action = Column(String(120), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
