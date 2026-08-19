import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text, Index
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
    engine = create_engine(
        DATABASE_URL, 
        connect_args={
            "connect_timeout": 10,
            
        }
    )

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
    
    # Şifrelenmiş veritabanı bağlantı metni
    encrypted_url = Column(String(500))
    
    # SSH Credentials for OS-level access
    ssh_host = Column(String(255), nullable=True)
    ssh_port = Column(Integer, default=22)
    ssh_username = Column(String(255), default="root")
    encrypted_ssh_credential = Column(String, nullable=True)
    
    project = relationship("Project", back_populates="nodes")
    
    def set_url(self, raw_url: str):
        self.encrypted_url = encrypt(raw_url)

class ProjectSettings(Base):
    __tablename__ = "project_settings"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), unique=True)
    settings_json = Column(String(5000), default="{}")
    
    project = relationship("Project")

class SyncJob(Base):
    __tablename__ = "sync_jobs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(String(50), default="QUEUED", nullable=False) # QUEUED, VALIDATING, BOOTSTRAPPING, CATCHING_UP, SUCCESS, FAILED, RECOVERING
    error_message = Column(String(1000), nullable=True)
    lease_owner = Column(String(255), nullable=True)
    lease_token = Column(String(36), nullable=True)
    lease_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    project = relationship("Project")
    
    __table_args__ = (
        Index("ix_sync_jobs_claim", "status", "lease_expires_at", "created_at"),
        Index("ix_sync_jobs_active", "project_id", unique=True, postgresql_where=text("status NOT IN ('SUCCESS', 'FAILED')"), sqlite_where=text("status NOT IN ('SUCCESS', 'FAILED')")),
    )

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(255))
    details = Column(String(500))

    project = relationship("Project")


class OperationalReport(Base):
    __tablename__ = 'operational_reports'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    report_type = Column(String(255))
    data_range_days = Column(Integer, default=7)
    recipients = Column(String(500))
    file_name = Column(String(255))
    created_by = Column(String(100), default='admin')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship('Project')
