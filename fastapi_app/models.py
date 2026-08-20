import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text, Index, Float, Boolean
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
    username = Column(String(50), nullable=True, default="system")

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


class BackupJob(Base):
    __tablename__ = 'backup_jobs'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cluster_name = Column(String(255))
    backup_type = Column(String(50)) # FULL, INCR, DIFF
    status = Column(String(50), default="IN_PROGRESS") # COMPLETED, FAILED, IN_PROGRESS
    size_mb = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
class BackupSchedule(Base):
    __tablename__ = 'backup_schedules'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    cluster_name = Column(String(255))
    schedule_expression = Column(String(100)) # e.g. "Daily at 02:00 AM"
    backup_type = Column(String(50))
    retention_days = Column(Integer, default=7)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="viewer") # "admin" or "viewer"
    email = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CloudCredential(Base):
    """Cloud storage provider credentials (AWS S3, GCS, Azure Blob)."""
    __tablename__ = 'cloud_credentials'
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False)          # 'AWS S3', 'GCS', 'Azure'
    label = Column(String(100), nullable=False)
    encrypted_key_id = Column(String(500), nullable=True)  # Access key / Client ID
    encrypted_secret = Column(String(500), nullable=True)  # Secret / credentials JSON
    bucket = Column(String(255), nullable=True)
    region = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class NotificationService(Base):
    """SMTP / Slack / PagerDuty notification configurations."""
    __tablename__ = 'notification_services'
    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String(50), nullable=False)  # 'SMTP', 'Slack', 'PagerDuty'
    label = Column(String(100), nullable=False)
    # Stored as encrypted JSON string containing all settings
    encrypted_settings = Column(String(2000), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CertificateRecord(Base):
    """TLS/CA certificate records scanned from nodes via SSH."""
    __tablename__ = 'certificates'
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, ForeignKey('nodes.id', ondelete='CASCADE'), nullable=True)
    cert_type = Column(String(50), default='TLS')  # 'TLS', 'CA', 'Client'
    common_name = Column(String(255), nullable=True)
    subject_alt_names = Column(String(500), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    issuer = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    node = relationship('DatabaseNode')


class LDAPConfig(Base):
    """LDAP / Active Directory server configurations."""
    __tablename__ = 'ldap_configs'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)
    server_url = Column(String(255), nullable=False)     # e.g. ldap://dc.company.com:389
    base_dn = Column(String(255), nullable=False)        # e.g. DC=company,DC=com
    bind_user = Column(String(255), nullable=True)
    encrypted_bind_pass = Column(String(500), nullable=True)
    user_filter = Column(String(255), default='(objectClass=person)')
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AddonSetting(Base):
    """Addon configuration (Kubernetes, Ops-Center)."""
    __tablename__ = 'addon_settings'
    id = Column(Integer, primary_key=True, index=True)
    addon_key = Column(String(100), unique=True, nullable=False)  # 'kubernetes', 'ops_center'
    enabled = Column(Boolean, default=False)
    api_url = Column(String(500), nullable=True)
    extra_json = Column(String(1000), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class DeployJob(Base):
    """Tracks a cluster deployment wizard session and its execution state."""
    __tablename__ = 'deploy_jobs'
    id                  = Column(Integer, primary_key=True, index=True)
    project_id          = Column(Integer, ForeignKey('projects.id', ondelete='SET NULL'), nullable=True)
    db_type             = Column(String(50), nullable=False)   # 'postgresql', 'mssql'
    cluster_name        = Column(String(255), nullable=False)
    # Status: PENDING → CONNECTING → SSH_OK → INSTALLING → CONFIGURING_PRIMARY
    #         → STARTING_PRIMARY → CONFIGURING_REPLICA → VERIFYING → SUCCESS | FAILED
    status              = Column(String(50), default='PENDING', nullable=False)
    step                = Column(String(100), nullable=True)
    error_msg           = Column(String(1000), nullable=True)
    log_output          = Column(Text, nullable=True)   # Live SSH command output for frontend polling

    # SSH configuration
    ssh_host            = Column(String(255), nullable=True)
    ssh_port            = Column(Integer, default=22)
    ssh_user            = Column(String(255), nullable=True)
    encrypted_ssh_cred  = Column(String(2000), nullable=True)  # PEM key or password (encrypted)
    sudo_method         = Column(String(20), default='sudo')   # sudo | doas | pbrun
    disable_fw          = Column(Boolean, default=True)
    disable_selinux     = Column(Boolean, default=True)
    install_software    = Column(Boolean, default=True)

    # Database configuration
    db_version          = Column(String(20), nullable=True)
    db_port             = Column(Integer, nullable=True)
    db_admin_user       = Column(String(100), nullable=True)
    encrypted_db_pass   = Column(String(500), nullable=True)
    db_data_dir         = Column(String(500), nullable=True)

    # Nodes: '[{"role":"primary","ip":"10.0.0.1"},{"role":"replica","ip":"10.0.0.2"}]'
    nodes_json          = Column(String(2000), nullable=True)

    created_at          = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.datetime.utcnow,
                                  onupdate=datetime.datetime.utcnow)

    project = relationship('Project')
