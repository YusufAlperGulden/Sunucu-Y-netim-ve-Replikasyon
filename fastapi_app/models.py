import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from vault import encrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fastapi_app.db")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("CRITICAL: DATABASE_URL environment variable is missing. Production systems must explicitly define a PostgreSQL connection string.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    metric_table = Column(String(100), nullable=True) # E.g., 'vehicles', 'email_records'
    replication_tables = Column(String(500), nullable=True) # E.g. 'vehicles, metadata'
    max_wal_lag_mb = Column(Integer, default=500) # Esnek limit ayar
    
    # Replication Health Status
    replication_health = Column(String(50), default="UNKNOWN") # HEALTHY, FAILED, UNKNOWN
    
    nodes = relationship("DatabaseNode", back_populates="project", cascade="all, delete-orphan")

class DatabaseNode(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    role = Column(String(20)) # "primary" or "standby"
    name = Column(String(100))
    # Şifrelenmiş veritabanı bağlantı metni
    encrypted_url = Column(String(500))
    
    project = relationship("Project", back_populates="nodes")

class SyncJob(Base):
    __tablename__ = "sync_jobs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    status = Column(String(50), default="QUEUED") # QUEUED, VALIDATING, BOOTSTRAPPING, CATCHING_UP, SUCCESS, FAILED, RECOVERING
    error_message = Column(String(1000), nullable=True)
    lease_owner = Column(String(255), nullable=True)
    lease_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    project = relationship("Project")
    
    def set_url(self, raw_url: str):
        self.encrypted_url = encrypt(raw_url)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(255))
    details = Column(String(500))

    project = relationship("Project")

