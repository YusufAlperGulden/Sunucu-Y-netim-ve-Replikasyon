import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from vault import encrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fastapi_app.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    max_wal_lag_mb = Column(Integer, default=500) # Esnek limit ayarı
    nodes = relationship("DatabaseNode", back_populates="project", cascade="all, delete-orphan")

class DatabaseNode(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(String(20)) # "primary" or "standby"
    name = Column(String(100))
    # Şifrelenmiş veritabanı bağlantı metni
    encrypted_url = Column(String(500))
    
    project = relationship("Project", back_populates="nodes")
    
    def set_url(self, raw_url: str):
        self.encrypted_url = encrypt(raw_url)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(255))
    details = Column(String(500))

    project = relationship("Project")

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)
