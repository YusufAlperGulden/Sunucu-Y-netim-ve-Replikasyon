from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, BackgroundTasks, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from models import SessionLocal, Project, DatabaseNode
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ha_manager import test_connection, setup_replication, check_and_protect_wal_bloat, cleanup_node_replication, cleanup_project_replication
from deploy_worker import run_deploy_job
from backup_worker import run_backup_job
import traceback
import asyncio
import secrets
from contextlib import asynccontextmanager

security = HTTPBasic(auto_error=False)

import os
import secrets
import hashlib

ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS = os.environ.get("ADMIN_PASS")

if not ADMIN_USER or not ADMIN_PASS:
    raise RuntimeError("CRITICAL: ADMIN_USER or ADMIN_PASS environment variables are missing.")


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "crm_sec_salt_2026_"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify password against database hash or plain match."""
    if not stored_hash:
        return False
    if plain_password == stored_hash:
        return True
    return hash_password(plain_password) == stored_hash


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    
    # 1. Check database first
    from models import SessionLocal, User
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == credentials.username).first()
        if user and user.password_hash:
            if verify_password(credentials.password, user.password_hash):
                return credentials
    except Exception:
        pass
    finally:
        db.close()

    # 2. Fallback to environment variables
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER) if ADMIN_USER else False
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS) if ADMIN_PASS else False
    if correct_username and correct_password:
        return credentials

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials", headers={"WWW-Authenticate": "Bearer"})

def run_background_db_init():
    """Run table creation, schema migrations, and sync in a background thread without blocking port binding."""
    try:
        from sqlalchemy import text
        from models import engine, Base, SessionLocal, Project, DatabaseNode
        import os as _os

        _reports_dir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "reports")
        _os.makedirs(_reports_dir, exist_ok=True)

        Base.metadata.create_all(bind=engine)

        for stmt in [
            "ALTER TABLE nodes ADD COLUMN IF NOT EXISTS ssh_host VARCHAR(255)",
            "ALTER TABLE nodes ADD COLUMN IF NOT EXISTS ssh_port INTEGER DEFAULT 22",
            "ALTER TABLE nodes ADD COLUMN IF NOT EXISTS ssh_username VARCHAR(255) DEFAULT 'root'",
            "ALTER TABLE nodes ADD COLUMN IF NOT EXISTS encrypted_ssh_credential VARCHAR",
            "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS username VARCHAR(50) DEFAULT 'system'",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name VARCHAR(100)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name VARCHAR(100)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC'",
            "ALTER TABLE deploy_jobs ADD COLUMN IF NOT EXISTS log_output TEXT",
            """CREATE TABLE IF NOT EXISTS cloud_credentials (
                id SERIAL PRIMARY KEY,
                provider VARCHAR(50) NOT NULL,
                label VARCHAR(100) NOT NULL,
                encrypted_key_id VARCHAR(500),
                encrypted_secret VARCHAR(500),
                bucket VARCHAR(255),
                region VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS notification_services (
                id SERIAL PRIMARY KEY,
                service_type VARCHAR(50) NOT NULL,
                label VARCHAR(100) NOT NULL,
                encrypted_settings VARCHAR(2000),
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS certificates (
                id SERIAL PRIMARY KEY,
                node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
                cert_type VARCHAR(50) DEFAULT 'TLS',
                common_name VARCHAR(255),
                subject_alt_names VARCHAR(500),
                expires_at TIMESTAMP,
                issuer VARCHAR(255),
                file_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS ldap_configs (
                id SERIAL PRIMARY KEY,
                label VARCHAR(100) NOT NULL,
                server_url VARCHAR(255) NOT NULL,
                base_dn VARCHAR(255) NOT NULL,
                bind_user VARCHAR(255),
                encrypted_bind_pass VARCHAR(500),
                user_filter VARCHAR(255) DEFAULT '(objectClass=person)',
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS addon_settings (
                id SERIAL PRIMARY KEY,
                addon_key VARCHAR(100) UNIQUE NOT NULL,
                enabled BOOLEAN DEFAULT FALSE,
                api_url VARCHAR(500),
                extra_json VARCHAR(1000),
                updated_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS ops_controllers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                url VARCHAR(255) NOT NULL,
                encrypted_api_token VARCHAR(500),
                status VARCHAR(50) DEFAULT 'ONLINE',
                is_primary BOOLEAN DEFAULT FALSE,
                version VARCHAR(50) DEFAULT '2.5.0',
                cluster_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )""",
            """CREATE TABLE IF NOT EXISTS kube_clusters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                encrypted_kubeconfig TEXT NOT NULL,
                api_server_url VARCHAR(255),
                status VARCHAR(50) DEFAULT 'CONNECTED',
                namespace VARCHAR(100) DEFAULT 'default',
                nodes_count INTEGER DEFAULT 1,
                pods_count INTEGER DEFAULT 0,
                operator_installed VARCHAR(100) DEFAULT 'CloudNativePG',
                last_synced_at TIMESTAMP DEFAULT NOW(),
                created_at TIMESTAMP DEFAULT NOW()
            )""",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS node_id INTEGER REFERENCES nodes(id) ON DELETE SET NULL",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS db_type VARCHAR(50) DEFAULT 'postgresql'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS backup_host VARCHAR(255)",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS backup_method VARCHAR(50) DEFAULT 'pgdumpall'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS dump_type VARCHAR(50) DEFAULT 'Schema And Data'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS compression BOOLEAN DEFAULT TRUE",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS compression_level INTEGER DEFAULT 6",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS retention_days INTEGER DEFAULT 31",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS enable_encryption BOOLEAN DEFAULT FALSE",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS enable_partial BOOLEAN DEFAULT FALSE",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS storage_location VARCHAR(100) DEFAULT 'Store on controller'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS storage_directory VARCHAR(500) DEFAULT '/var/lib/backups'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS backup_subdirectory VARCHAR(255) DEFAULT 'BACKUP-%i'",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS cloud_credential_id INTEGER REFERENCES cloud_credentials(id) ON DELETE SET NULL",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS file_path VARCHAR(1000)",
            "ALTER TABLE backup_jobs ADD COLUMN IF NOT EXISTS error_msg TEXT",
            """CREATE TABLE IF NOT EXISTS alarm_records (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                severity VARCHAR(50) DEFAULT 'WARNING',
                category VARCHAR(100) DEFAULT 'Cluster',
                cluster_name VARCHAR(255),
                hostname VARCHAR(255),
                message TEXT,
                is_muted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )""",
        ]:
            try:
                with engine.begin() as conn:
                    conn.execute(text(stmt))
            except Exception:
                pass

        # Auto-sync Neon URLs
        try:
            from vault import encrypt, decrypt
            db = SessionLocal()
            try:
                projects = db.query(Project).all()
                for proj in projects:
                    p_name = (proj.name or '').lower()
                    if 'email' in p_name or 'e-mail' in p_name:
                        proj.metric_table = 'emails'
                    elif 'plaka' in p_name or 'araç' in p_name:
                        proj.metric_table = 'vehicles'
                        
                    nodes = proj.nodes
                    if len(nodes) >= 2:
                        primary_nodes = [n for n in nodes if n.role and n.role.lower() == 'primary']
                        standby_nodes = [n for n in nodes if n.role and n.role.lower() == 'standby']
                        
                        FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
                        YEDEK_URL = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
                        
                        for node in primary_nodes:
                            current = decrypt(node.encrypted_url) if node.encrypted_url else None
                            if current != FRANKFURT_URL:
                                node.encrypted_url = encrypt(FRANKFURT_URL)
                        
                        for node in standby_nodes:
                            current = decrypt(node.encrypted_url) if node.encrypted_url else None
                            if current != YEDEK_URL:
                                node.encrypted_url = encrypt(YEDEK_URL)
                                
                db.commit()
            finally:
                db.close()
        except Exception as e:
            print(f"Neon URL sync error: {e}")
        print("Database background migrations and initialization complete.")
    except Exception as e:
        print(f"Background DB init warning: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Immediate yield so uvicorn binds port instantly for Render port scanning
    print("Application starting up — port binding enabled immediately.")
    import asyncio
    asyncio.create_task(asyncio.to_thread(run_background_db_init))
    yield
    print("Application shutting down.")


app = FastAPI(title="Sunucu Yönetim ve Replikasyon", lifespan=lifespan)

@app.get("/health")
@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "universal-server-manager"}

# Mount static files and templates with absolute paths
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_STATIC_DIR = os.path.join(_BASE_DIR, "static")
_TEMPLATES_DIR = os.path.join(_BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
@app.get("/api/auth/verify", dependencies=[Depends(verify_credentials)])
def verify_auth():
    return {"status": "ok"}

class InitialNodeCreate(BaseModel):
    url: str | None = None
    ssh_host: str | None = None
    ssh_port: int = 22
    ssh_username: str = "root"
    ssh_password: str | None = None

class ProjectCreate(BaseModel):
    name: str
    description: str
    initial_node: InitialNodeCreate | None = None

class NodeCreate(BaseModel):
    role: str
    name: str
    url: str
    # SSH Credentials (opsiyonel — sağlanırsa gerçek pg_dump çalışır)
    ssh_host: str | None = None
    ssh_port: int = 22
    ssh_username: str = "root"
    ssh_password: str | None = None   # Şifre veya key içeriği; AES-256 şifreli saklanır

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/projects", dependencies=[Depends(verify_credentials)])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{"id": p.id, "name": p.name, "description": p.description, "nodesCount": len(p.nodes), "nodes": [{"id": n.id, "name": n.name, "role": n.role} for n in p.nodes]} for p in projects]

@app.post("/api/projects", dependencies=[Depends(verify_credentials)])
def add_project(project: ProjectCreate, db: Session = Depends(get_db)):
    name = (project.name or "").strip()
    desc = (project.description or "").strip()
    if not name:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Cluster adı boş bırakılamaz. Lütfen bir cluster adı giriniz."})
    
    # Check if a project with the same name already exists
    existing = db.query(Project).filter(Project.name.ilike(name)).first()
    if existing:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"'{name}' isminde bir cluster zaten mevcut. Lütfen farklı bir isim deneyiniz."})
        
    try:
        db_proj = Project(name=name, description=desc)
        db.add(db_proj)
        db.flush()

        # Handle initial node if provided (URL or SSH)
        if project.initial_node:
            init_url = (project.initial_node.url or "").strip()
            init_ssh_host = (project.initial_node.ssh_host or "").strip()
            if init_url or init_ssh_host:
                final_url = init_url if init_url else f"postgresql://root@{init_ssh_host}:5432/{name}"
                db_node = DatabaseNode(
                    project_id=db_proj.id,
                    role="primary",
                    name=f"{name} Primary",
                    ssh_host=init_ssh_host if init_ssh_host else None,
                    ssh_port=project.initial_node.ssh_port or 22,
                    ssh_username=project.initial_node.ssh_username or "root"
                )
                db_node.set_url(final_url)
                if project.initial_node.ssh_password and project.initial_node.ssh_password.strip():
                    from vault import encrypt as _enc
                    db_node.encrypted_ssh_credential = _enc(project.initial_node.ssh_password.strip())
                db.add(db_node)
        
        db.commit()
        db.refresh(db_proj)
        
        from models import AuditLog
        audit = AuditLog(project_id=db_proj.id, action="Project Created", details=f"Name: {name}")
        db.add(audit)
        db.commit()
        return {"success": True, "id": db_proj.id, "name": db_proj.name, "description": db_proj.description}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"success": False, "detail": f"Cluster oluşturulamadı: {str(e)}"})

@app.put("/api/projects/{project_id}", dependencies=[Depends(verify_credentials)])
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"success": False, "detail": "Belirtilen cluster bulunamadı."})
    
    name = (project.name or "").strip()
    desc = (project.description or "").strip()
    if not name:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Cluster adı boş bırakılamaz."})
        
    existing = db.query(Project).filter(Project.name.ilike(name), Project.id != project_id).first()
    if existing:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"'{name}' ismi başka bir cluster tarafından kullanılmaktadır. Lütfen farklı bir isim deneyiniz."})
        
    proj.name = name
    proj.description = desc
    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": new_node.id, "encrypted_url": new_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True}


@app.delete("/api/nodes/{node_id}", dependencies=[Depends(verify_credentials)])
async def delete_node(node_id: int, db: Session = Depends(get_db)):
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={"message": "Node not found"})
    
    from vault import decrypt
    proj = node.project
    if proj:
        primary = next((n for n in proj.nodes if n.role.lower() == 'primary' and n.id != node_id), None)
        if primary and node.role.lower() == 'standby':
            p_url = decrypt(primary.encrypted_url)
            s_url = decrypt(node.encrypted_url)
            if p_url:
                try:
                    await cleanup_node_replication(proj.id, node_id, p_url, s_url)
                except Exception as e:
                    return JSONResponse(status_code=500, content={"message": f"Failed to clean up PostgreSQL logical replication: {e}"})
                
    db.delete(node)
    
    from models import AuditLog
    audit = AuditLog(project_id=node.project_id, action="Node Deleted", details=f"ID: {node_id}, Name: {node.name}")
    db.add(audit)
    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": new_node.id, "encrypted_url": new_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True}

@app.delete("/api/projects/{project_id}", dependencies=[Depends(verify_credentials)])
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    
    from vault import decrypt
    primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
    if primary:
        p_url = decrypt(primary.encrypted_url)
        if p_url:
            s_urls = []
            for n in proj.nodes:
                if n.role.lower() == 'standby':
                    dec = decrypt(n.encrypted_url)
                    if dec: s_urls.append(dec)
            try:
                await cleanup_project_replication(project_id, p_url, s_urls)
            except Exception as e:
                return JSONResponse(status_code=500, content={"message": f"Failed to clean up PostgreSQL logical replication: {e}"})

    db.delete(proj)
    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": new_node.id, "encrypted_url": new_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True}

@app.get("/api/projects/{project_id}", dependencies=[Depends(verify_credentials)])
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    from models import SyncJob
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    
    latest_job = db.query(SyncJob).filter(SyncJob.project_id == project_id).order_by(SyncJob.id.desc()).first()
    sync_status = latest_job.status if latest_job else "IDLE"
    sync_error = latest_job.error_message if latest_job else None

    from vault import decrypt
    from urllib.parse import urlparse
    nodes = []
    for n in proj.nodes:
        ip = "Unknown"
        port = "Unknown"
        db_type = "Unknown"
        try:
            if n.encrypted_url:
                url = decrypt(n.encrypted_url)
                parsed = urlparse(url)
                ip = parsed.hostname or "Unknown"
                port = str(parsed.port) if parsed.port else ("5432" if parsed.scheme == "postgresql" else "Unknown")
                db_type = "PostgreSQL" if parsed.scheme == "postgresql" else (parsed.scheme or "Unknown")
        except Exception:
            pass
        nodes.append({
            "id": n.id, 
            "role": n.role, 
            "name": n.name,
            "ip": ip,
            "port": port,
            "type": db_type,
            "status": "Operational",
            "version": "16.4", # Or fetch from DB if available
            "ssh_host": n.ssh_host,
            "ssh_port": n.ssh_port,
            "ssh_username": n.ssh_username,
            "has_ssh_credential": bool(n.encrypted_ssh_credential)
        })
    return {
        "id": proj.id, 
        "name": proj.name, 
        "description": proj.description, 
        "sync_status": sync_status,
        "sync_error": sync_error,
        "replication_health": proj.replication_health,
        "nodes": nodes
    }

@app.post("/api/projects/{project_id}/nodes", dependencies=[Depends(verify_credentials)])
async def add_node(project_id: int, node: NodeCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    name = (node.name or "").strip()
    if not name:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Sunucu adı boş bırakılamaz.", "message": "Sunucu adı boş bırakılamaz."})

    if node.role.lower() not in ['primary', 'standby']:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Geçersiz rol. Sadece Primary veya Standby eklenebilir.", "message": "Geçersiz rol. Sadece Primary veya Standby eklenebilir."})

    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"success": False, "detail": "Belirtilen cluster bulunamadı.", "message": "Belirtilen cluster bulunamadı."})
        
    # Check duplicate node name in the project
    existing_node_name = next((n for n in proj.nodes if n.name and n.name.lower() == name.lower()), None)
    if existing_node_name:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"Bu cluster altında '{name}' isminde bir sunucu zaten mevcut.", "message": f"Bu cluster altında '{name}' isminde bir sunucu zaten mevcut."})

    if node.role.lower() == 'primary':
        existing_primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
        if existing_primary:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Bu cluster'da zaten 1 adet Primary (Ana) sunucu bulunmaktadır. İkinci bir Primary eklenemez.", "message": "Bu cluster'da zaten 1 adet Primary (Ana) sunucu bulunmaktadır. İkinci bir Primary eklenemez."})
    
    from vault import decrypt
    for n in db.query(DatabaseNode).all():
        if decrypt(n.encrypted_url) == node.url:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Bu sunucu bağlantı URL'si sistemde zaten kayıtlı. Aynı veritabanı birden fazla node olarak eklenemez.", "message": "Bu sunucu bağlantı URL'si sistemde zaten kayıtlı. Aynı veritabanı birden fazla node olarak eklenemez."})

    # 1. PING (Test Connection)
    is_alive = await test_connection(node.url)
    if not is_alive:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Bağlantı testi başarısız oldu. Sunucuya ulaşılamıyor veya URL hatalı.", "message": "Bağlantı testi başarısız oldu. Sunucuya ulaşılamıyor veya URL hatalı."})
    
    # 2. SAVE (Vault Encryption)
    db_node = DatabaseNode(project_id=proj.id, role=node.role, name=node.name)
    db_node.set_url(node.url) # AES-256 encrypts the url

    # SSH Credentials (opsiyonel)
    if node.ssh_host and node.ssh_host.strip():
        db_node.ssh_host = node.ssh_host.strip()
        db_node.ssh_port = node.ssh_port or 22
        db_node.ssh_username = node.ssh_username or "root"
        if node.ssh_password and node.ssh_password.strip():
            from vault import encrypt as _enc
            db_node.encrypted_ssh_credential = _enc(node.ssh_password)
    
    db.add(db_node)
    
    from models import AuditLog
    audit = AuditLog(project_id=proj.id, action="Node Added", details=f"Role: {node.role}, Name: {node.name}")
    db.add(audit)
    db.commit()
    
    # Check if there are project settings and apply them to the new node
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if ps:
        try:
            settings_data = json.loads(ps.settings_json)
            safe_node = [{"id": db_node.id, "encrypted_url": db_node.encrypted_url}]
            background_tasks.add_task(apply_postgres_settings, safe_node, settings_data)
        except Exception as e:
            print("Failed to dispatch settings apply for new node:", e)

    return {"success": True, "message": "Node added securely."}

@app.post("/api/projects/{project_id}/sync", status_code=202, dependencies=[Depends(verify_credentials)])
async def sync_replication(project_id: int, db: Session = Depends(get_db)):
    from models import SyncJob
    
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    # 1. Distributed Lock Control
    active_job = db.query(SyncJob).filter(SyncJob.project_id == project_id, SyncJob.status.notin_(["SUCCESS", "FAILED"])).first()
    if active_job:
        return JSONResponse(status_code=409, content={"success": False, "message": "A sync process is already running for this project."})
    
    primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
    standbys = [n for n in proj.nodes if n.role.lower() == 'standby']
    
    if not primary or not standbys:
        return JSONResponse(status_code=400, content={"success": False, "message": "Projenizde senkronizasyon için en az 1 Primary ve 1 Standby node bulunmalıdır."})
    
    # 2. Enqueue the job
    new_job = SyncJob(project_id=proj.id, status="QUEUED")
    db.add(new_job)
    
    from sqlalchemy.exc import IntegrityError
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return JSONResponse(status_code=409, content={"success": False, "message": "A sync process is already running for this project."})
    
    # Return 202 Accepted immediately
    return {
        "success": True, 
        "message": "Sync job has been queued and is processing in the background.",
        "job_id": new_job.id,
        "status_url": f"/api/projects/{proj.id}"
    }

@app.get('/api/audit-logs', dependencies=[Depends(verify_credentials)])
def get_audit_logs(db: Session = Depends(get_db)):
    from models import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.strftime("%Y-%m-%d %H:%M:%S") if l.timestamp else "-", 'action': l.action, 'details': l.details, 'user': l.username or "System"} for l in logs]

# ─── Watchlists ────────────────────────────────────────────────────────────────

class WatchListCreate(BaseModel):
    name: str
    topics: list = []
    cluster_ids: list = []
    page_by: str = 'Topic'
    grid: str = '2x2'
    page_speed: int = 5

@app.get('/api/watchlists', dependencies=[Depends(verify_credentials)])
def get_watchlists(db: Session = Depends(get_db)):
    import json
    from models import WatchList, Project
    wls = db.query(WatchList).order_by(WatchList.created_at.desc()).all()
    result = []
    for w in wls:
        try:
            topics = json.loads(w.topics or '[]')
        except Exception:
            topics = []
        try:
            cids = json.loads(w.cluster_ids or '[]')
        except Exception:
            cids = []
        # Resolve cluster names
        clusters = []
        for cid in cids:
            proj = db.query(Project).filter(Project.id == cid).first()
            if proj:
                clusters.append({'id': proj.id, 'name': proj.name})
        result.append({
            'id': w.id,
            'name': w.name,
            'topics': topics,
            'clusters': clusters,
            'page_by': w.page_by,
            'grid': w.grid,
            'page_speed': w.page_speed,
            'created_at': w.created_at.strftime('%Y-%m-%d %H:%M:%S') if w.created_at else ''
        })
    return result

@app.post('/api/watchlists', dependencies=[Depends(verify_credentials)])
def create_watchlist(data: WatchListCreate, db: Session = Depends(get_db)):
    import json
    from models import WatchList
    if not data.name.strip():
        return JSONResponse(status_code=400, content={'detail': 'Name is required.'})
    if not data.topics:
        return JSONResponse(status_code=400, content={'detail': 'At least one topic is required.'})
    wl = WatchList(
        name=data.name.strip(),
        topics=json.dumps(data.topics),
        cluster_ids=json.dumps([int(c) for c in data.cluster_ids]),
        page_by=data.page_by,
        grid=data.grid,
        page_speed=max(3, min(180, data.page_speed))
    )
    db.add(wl)
    db.commit()
    db.refresh(wl)
    return {'success': True, 'id': wl.id}

@app.delete('/api/watchlists/{wl_id}', dependencies=[Depends(verify_credentials)])
def delete_watchlist(wl_id: int, db: Session = Depends(get_db)):
    from models import WatchList
    wl = db.query(WatchList).filter(WatchList.id == wl_id).first()
    if not wl:
        return JSONResponse(status_code=404, content={'detail': 'Watchlist not found.'})
    db.delete(wl)
    db.commit()
    return {'success': True}

class SettingsUpdate(BaseModel):
    max_wal_lag_mb: int
    metric_table: str = None
    replication_tables: str = None

@app.get('/api/settings/{project_id}', dependencies=[Depends(verify_credentials)])
def get_settings(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
    return {
        'max_wal_lag_mb': proj.max_wal_lag_mb,
        'metric_table': proj.metric_table or '',
        'replication_tables': proj.replication_tables or ''
    }

@app.post('/api/settings/{project_id}', dependencies=[Depends(verify_credentials)])
def update_settings(project_id: int, settings: SettingsUpdate, db: Session = Depends(get_db)):
    if settings.max_wal_lag_mb < 50:
        return JSONResponse(status_code=400, content={'message': 'WAL limit must be at least 50 MB to prevent premature slot dropping'})
        
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
    proj.max_wal_lag_mb = settings.max_wal_lag_mb
    proj.metric_table = settings.metric_table
    proj.replication_tables = settings.replication_tables
    db.commit()
    return {'success': True}

@app.get('/api/projects/{project_id}/metrics', dependencies=[Depends(verify_credentials)])
async def get_project_metrics(project_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    import asyncio
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
    
    # Concurrently fetch metrics from all servers
    tasks = []
    for node in proj.nodes:
        node_dict = {
              'id': node.id,
              'name': node.name,
              'role': node.role,
              'encrypted_url': node.encrypted_url,
              'ssh_host': node.ssh_host,
              'ssh_port': node.ssh_port,
              'ssh_username': node.ssh_username,
              'encrypted_ssh_credential': node.encrypted_ssh_credential,
              'metric_table': proj.metric_table
          }
        tasks.append(get_server_metrics(node_dict, project_id=proj.id))
        
    results = await asyncio.gather(*tasks)
    
    # Map results back to node definitions
    metrics_list = []
    for i, node in enumerate(proj.nodes):
        metrics_list.append({
            'id': node.id,
            'name': node.name,
            'role': node.role,
            'metrics': results[i]
        })
        
    return metrics_list

class NodeUpdate(BaseModel):
    url: str
    # SSH Credentials (opsiyonel)
    ssh_host: str | None = None
    ssh_port: int = 22
    ssh_username: str = "root"
    ssh_password: str | None = None

@app.get('/api/nodes/{node_id}/url', dependencies=[Depends(verify_credentials)])
def get_node_url(node_id: int, db: Session = Depends(get_db)):
    from vault import decrypt
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
    try:
        raw_url = decrypt(node.encrypted_url)
        return {'success': True, 'url': raw_url}
    except:
        return JSONResponse(status_code=500, content={'message': 'Failed to decrypt URL'})

@app.put('/api/nodes/{node_id}', dependencies=[Depends(verify_credentials)])
async def update_node_url(node_id: int, update: NodeUpdate, db: Session = Depends(get_db)):
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
        
    from vault import decrypt
    for n in db.query(DatabaseNode).all():
        if n.id != node_id and decrypt(n.encrypted_url) == update.url:
            return JSONResponse(status_code=400, content={"success": False, "message": "Bu veritabanı URL'si sistemde zaten kayıtlı."})
    
    is_alive = await test_connection(update.url)
    if not is_alive:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'Connection test failed. Sunucuya ulaşılamıyor.'})
    
    node.set_url(update.url)

    # SSH Credentials güncelle (opsiyonel — boş gönderilirse silinmez)
    if update.ssh_host and update.ssh_host.strip():
        node.ssh_host = update.ssh_host.strip()
        node.ssh_port = update.ssh_port or 22
        node.ssh_username = update.ssh_username or "root"
        if update.ssh_password and update.ssh_password.strip():
            from vault import encrypt as _enc2
            node.encrypted_ssh_credential = _enc2(update.ssh_password)
    elif update.ssh_host == "":
        # Açıkça boş gönderilirse SSH bilgilerini temizle
        node.ssh_host = None
        node.encrypted_ssh_credential = None

    db.commit()
    return {'success': True, 'message': 'Node updated securely.'}

@app.get('/api/nodes/{node_id}/metrics', dependencies=[Depends(verify_credentials)])
async def get_single_node_metrics(node_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
    
    node_dict = {
        'id': node.id,
        'name': node.name,
        'role': node.role,
        'encrypted_url': node.encrypted_url,
        'ssh_host': node.ssh_host,
        'ssh_port': node.ssh_port,
        'ssh_username': node.ssh_username,
        'encrypted_ssh_credential': node.encrypted_ssh_credential,
        'metric_table': node.project.metric_table if node.project else None
    }
    metrics = await get_server_metrics(node_dict, project_id=node.project_id)
    return metrics


@app.post("/api/projects/{project_id}/cleanup-slots", dependencies=[Depends(verify_credentials)])
async def cleanup_orphaned_slots(project_id: int, db: Session = Depends(get_db)):
    from vault import decrypt
    import asyncpg
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
    if not primary:
        return JSONResponse(status_code=400, content={"message": "No primary node found in this project."})
        
    p_url = decrypt(primary.encrypted_url)
    if not p_url:
        return JSONResponse(status_code=500, content={"message": "Failed to decrypt primary URL"})
        
    valid_sub_names = [f"univ_sub_{project_id}_{n.id}" for n in proj.nodes if n.role.lower() == 'standby']
    
    dropped = []
    try:
        p_conn = await asyncpg.connect(p_url, timeout=10.0)
        # Fetch all our slots
        slots = await p_conn.fetch(f"SELECT slot_name, active_pid FROM pg_replication_slots WHERE slot_name LIKE 'univ_sub_{project_id}_%';")
        for slot in slots:
            slot_name = slot['slot_name']
            if slot_name not in valid_sub_names:
                # Orphaned slot! Drop it.
                active_pid = slot['active_pid']
                if active_pid:
                    await p_conn.execute(f"SELECT pg_terminate_backend({active_pid});")
                await p_conn.execute(f"SELECT pg_drop_replication_slot('{slot_name}');")
                dropped.append(slot_name)
        await p_conn.close()
        
        # Log it
        if dropped:
            from models import AuditLog
            audit = AuditLog(project_id=project_id, action="Orphaned Slots Cleaned", details=f"Dropped: {', '.join(dropped)}")
            db.add(audit)
            db.commit()
            
        return {"success": True, "message": f"Successfully dropped {len(dropped)} orphaned slots.", "dropped": dropped}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Cleanup failed: {e}"})


@app.get("/api/projects/{project_id}/settings")
def get_project_settings(project_id: int, db: Session = Depends(get_db)):
    from models import ProjectSettings
    import json
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if not ps:
        # Default settings if none exist
        default_settings = {
            "backup_cloud_retention": "180",
            "backup_retention": "31",
            "backupdir": "/home/cmon/backups",
            "pgbackrest_cipher_pass": "********",
            "pgbackrest_cipher_type": "none",
            "pgbackrest_repo_hostname": "",
            "pgbackrest_repo_path": "",
            "pgbackrest_stanza_name": "",
            "pitr_retention_hours": ""
        }
        return default_settings
    try:
        data = json.loads(ps.settings_json)
        return data
    except:
        return {}


async def apply_postgres_settings(nodes, settings_data):
    import asyncpg
    from vault import decrypt
    
    # Define which settings map to actual PostgreSQL parameters
    pg_params = [
        'log_min_duration_statement',
        'wal_level',
        'max_replication_slots',
        'max_wal_senders',
        'shared_buffers',
        'work_mem',
        'max_connections'
    ]
    
    for node in nodes:
        db_url = decrypt(node['encrypted_url'])
        try:
            conn = await asyncpg.connect(db_url, timeout=5.0)
            
            for param in pg_params:
                if param in settings_data and settings_data[param]:
                    # Prevent SQL injection loosely by removing quotes
                    safe_val = str(settings_data[param]).replace("'", "").strip()
                    try:
                        await conn.execute(f"ALTER SYSTEM SET {param} = '{safe_val}';")
                    except Exception as e:
                        print(f"Error setting {param} on node {node['id']}: {e}")
                        
            # Reload configuration (Note: some settings like shared_buffers require a full restart to take effect,
            # but pg_reload_conf() is safe to call and applies dynamic ones immediately).
            await conn.execute("SELECT pg_reload_conf();")
            await conn.close()
            print(f"Successfully applied settings to node {node['id']}")
        except Exception as e:
            print(f"Failed to connect and apply settings to node {node['id']}: {e}")


@app.put("/api/projects/{project_id}/settings")
async def update_project_settings(project_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from models import ProjectSettings, DatabaseNode
    import json
    data = await request.json()
    
    ps = db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).first()
    if not ps:
        current_data = {}
        current_data.update(data)
        ps = ProjectSettings(project_id=project_id, settings_json=json.dumps(current_data))
        db.add(ps)
    else:
        # Merge settings
        try:
            current_data = json.loads(ps.settings_json)
        except:
            current_data = {}
        current_data.update(data)
        ps.settings_json = json.dumps(current_data)
        
    db.commit()
    
    # Fetch all nodes and apply PostgreSQL parameters asynchronously
    nodes = db.query(DatabaseNode).filter(DatabaseNode.project_id == project_id).all()
    if nodes:
        # Pass a list of dicts to avoid DetachedInstanceError in background task
        safe_nodes = [{"id": n.id, "encrypted_url": n.encrypted_url} for n in nodes]
        background_tasks.add_task(apply_postgres_settings, safe_nodes, current_data)
        
    return {"status": "ok"}


class ReportCreate(BaseModel):
    project_id: int
    report_type: str
    data_range_days: int
    recipients: str

@app.post("/api/reports", dependencies=[Depends(verify_credentials)])
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    from models import OperationalReport
    import datetime
    
    # Generate a dummy filename based on type and time
    safe_type = report.report_type.replace(" ", "_").lower()
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{safe_type}_{ts}.pdf"
    
    new_report = OperationalReport(
        project_id=report.project_id,
        report_type=report.report_type,
        data_range_days=report.data_range_days,
        recipients=report.recipients,
        file_name=filename,
        created_by="admin"
    )
    db.add(new_report)
    db.commit()
    return {"success": True, "message": "Report created"}

@app.get("/api/reports", dependencies=[Depends(verify_credentials)])
def get_reports(db: Session = Depends(get_db)):
    from models import OperationalReport, Project
    reports = db.query(OperationalReport).order_by(OperationalReport.created_at.desc()).all()
    
    result = []
    for r in reports:
        # Get cluster name
        proj = db.query(Project).filter(Project.id == r.project_id).first()
        cluster_name = proj.name if proj else "Unknown Cluster"
        
        result.append({
            "id": r.id,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
            "file_name": r.file_name,
            "report_type": r.report_type,
            "cluster": cluster_name,
            "created_by": r.created_by,
            "data_range": f"Last {r.data_range_days} days",
            "recipients": r.recipients or "-"
        })
    return result


@app.post("/api/nodes/{node_id}/test-ssh", dependencies=[Depends(verify_credentials)])
def test_ssh_connection(node_id: int, db: Session = Depends(get_db)):
    from models import DatabaseNode
    from vault import decrypt
    from ssh_worker import SSHManager
    
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={"message": "Node not found"})
        
    if not node.ssh_host:
        return JSONResponse(status_code=400, content={"message": "SSH Host is not configured for this node."})
        
    credential = decrypt(node.encrypted_ssh_credential) if node.encrypted_ssh_credential else ""
    
    try:
        with SSHManager(node.ssh_host, node.ssh_port, node.ssh_username, credential) as ssh:
            stdout, stderr, code = ssh.execute_command("whoami")
            if code == 0:
                return {"success": True, "message": f"Successfully connected to SSH as {stdout.strip()}"}
            else:
                return {"success": False, "message": f"Connected, but command failed: {stderr}"}
    except Exception as e:
        return {"success": False, "message": f"SSH Connection failed: {str(e)}"}


@app.get("/api/debug-db")
def debug_db(db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        res = db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='nodes';"))
        columns = [row[0] for row in res.fetchall()]
        
        # Test project 2 query directly
        proj = db.query(Project).filter(Project.id == 2).first()
        node_count = len(proj.nodes) if proj else -1
        
        return {"columns": columns, "proj_2_nodes": node_count}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BackupWizardCreate(BaseModel):
    project_id: Optional[int] = None
    cluster_name: Optional[str] = None
    db_type: str = "postgresql" # "postgresql", "mssql"
    node_id: Optional[int] = None
    backup_host: Optional[str] = None
    backup_method: str = "pgdumpall" # pgdumpall, pg_basebackup, Full, Differential, Transaction Log
    dump_type: str = "Schema And Data" # Schema And Data, Schema Only, Data Only
    backup_type: str = "FULL"
    compression: bool = True
    compression_level: int = 6
    retention_days: int = 31
    enable_encryption: bool = False
    enable_partial: bool = False
    storage_location: str = "Store on controller" # Store on controller, Cloud storage
    storage_directory: str = "/var/lib/backups"
    backup_subdirectory: str = "BACKUP-%i"
    cloud_credential_id: Optional[int] = None

@app.post("/api/backups/create", dependencies=[Depends(verify_credentials)])
@app.post("/api/backups", dependencies=[Depends(verify_credentials)])
def create_backup(payload: BackupWizardCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from models import BackupJob, Project, DatabaseNode, AuditLog

    # Resolve project if project_id or cluster_name provided
    proj = None
    if payload.project_id:
        proj = db.query(Project).filter(Project.id == payload.project_id).first()
    elif payload.cluster_name:
        proj = db.query(Project).filter(Project.name.ilike(f"%{payload.cluster_name}%")).first()

    cluster_title = payload.cluster_name or (proj.name if proj else f"{payload.db_type.upper()} Cluster")

    # If node_id not specified, pick primary node of the cluster
    target_node_id = payload.node_id
    host_str = payload.backup_host
    if not target_node_id and proj and proj.nodes:
        pri = next((n for n in proj.nodes if n.role and n.role.lower() == 'primary'), proj.nodes[0])
        target_node_id = pri.id
        if not host_str:
            host_str = f"{pri.host}:{pri.port or (1433 if payload.db_type == 'mssql' else 5432)}"

    if not host_str:
        host_str = "localhost:5432" if payload.db_type == 'postgresql' else "localhost:1433"

    job = BackupJob(
        project_id=proj.id if proj else None,
        node_id=target_node_id,
        cluster_name=cluster_title,
        db_type=payload.db_type,
        backup_host=host_str,
        backup_method=payload.backup_method,
        dump_type=payload.dump_type,
        backup_type=payload.backup_type or "FULL",
        compression=payload.compression,
        compression_level=payload.compression_level,
        retention_days=payload.retention_days,
        enable_encryption=payload.enable_encryption,
        enable_partial=payload.enable_partial,
        storage_location=payload.storage_location,
        storage_directory=payload.storage_directory,
        backup_subdirectory=payload.backup_subdirectory,
        cloud_credential_id=payload.cloud_credential_id,
        status="PENDING"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Launch real background backup runner
    background_tasks.add_task(run_backup_job, job.id)

    audit = AuditLog(
        project_id=proj.id if proj else None,
        action="BACKUP_INITIATED",
        user="admin",
        details=f"Backup #{job.id} ({job.backup_method}) started for {cluster_title} on host {host_str}."
    )
    db.add(audit)
    db.commit()

    return {
        "success": True,
        "job_id": job.id,
        "cluster_name": cluster_title,
        "message": f"✓ Backup job #{job.id} initiated successfully."
    }

@app.get("/api/backups", dependencies=[Depends(verify_credentials)])
def get_backups(db: Session = Depends(get_db)):
    from models import BackupJob
    jobs = db.query(BackupJob).order_by(BackupJob.id.desc()).all()
    results = []
    for j in jobs:
        is_cloud = bool(j.cloud_credential_id or (j.storage_location and 'cloud' in j.storage_location.lower()))
        results.append({
            "id": j.id,
            "project_id": j.project_id,
            "cluster_name": j.cluster_name or "PostgreSQL",
            "db_type": j.db_type or "postgresql",
            "backup_host": j.backup_host or "localhost:5432",
            "backup_method": j.backup_method or "pgdumpall",
            "dump_type": j.dump_type or "Schema And Data",
            "backup_type": j.backup_type or "FULL",
            "title": f"BACKUP-{j.id}",
            "status": j.status,
            "size_mb": j.size_mb or 0.0,
            "size_display": f"{j.size_mb} MB" if j.size_mb and j.size_mb >= 1.0 else (f"{int((j.size_mb or 0)*1024)} KB" if j.size_mb else "0 KB"),
            "storage_location": j.storage_location or "Store on controller",
            "is_cloud": is_cloud,
            "file_path": j.file_path or "",
            "error_msg": j.error_msg or "",
            "created_at": j.created_at.strftime("%Y-%m-%d %H:%M:%S") if j.created_at else "",
            "created_human": j.created_at.strftime("%b %d, %H:%M") if j.created_at else "Just now",
            "completed_at": j.completed_at.strftime("%Y-%m-%d %H:%M:%S") if j.completed_at else ""
        })
    return results

# ── Alarms & Activity Quick Panel Endpoints ─────────────────────────────────

@app.get("/api/alarms", dependencies=[Depends(verify_credentials)])
def get_alarms(db: Session = Depends(get_db)):
    from models import AlarmRecord, DatabaseNode
    # Auto-generate dynamic alarms from offline database nodes
    try:
        nodes = db.query(DatabaseNode).all()
        for n in nodes:
            if n.status and n.status.upper() in ('DOWN', 'FAILED', 'ERROR'):
                existing = db.query(AlarmRecord).filter(
                    AlarmRecord.hostname.like(f"%{n.host}%"),
                    AlarmRecord.title.like('%Unreachable%')
                ).first()
                if not existing:
                    db.add(AlarmRecord(
                        title=f"Node Unreachable: {n.name or n.host}",
                        severity="CRITICAL",
                        category="Node",
                        cluster_name=n.project.name if n.project else "PostgreSQL",
                        hostname=f"{n.host}:{n.port or 5432}",
                        message=f"Node {n.name or n.host} is currently down or unreachable."
                    ))
        db.commit()
    except Exception:
        pass

    all_alarms = db.query(AlarmRecord).order_by(AlarmRecord.id.desc()).all()
    unmuted = [a for a in all_alarms if not a.is_muted]

    return {
        "total_count": len(all_alarms),
        "unmuted_count": len(unmuted),
        "alarms": [{
            "id": a.id,
            "title": a.title,
            "severity": a.severity,
            "category": a.category,
            "cluster_name": a.cluster_name or "PostgreSQL",
            "hostname": a.hostname or "localhost",
            "message": a.message or "",
            "is_muted": a.is_muted,
            "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else "",
            "when_human": a.created_at.strftime("%b %d, %H:%M") if a.created_at else "Just now"
        } for a in all_alarms]
    }

@app.post("/api/alarms/{alarm_id}/mute", dependencies=[Depends(verify_credentials)])
def mute_alarm(alarm_id: int, db: Session = Depends(get_db)):
    from models import AlarmRecord
    a = db.query(AlarmRecord).filter(AlarmRecord.id == alarm_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alarm not found")
    a.is_muted = True
    db.commit()
    return {"success": True, "message": "Alarm muted"}

@app.post("/api/alarms/{alarm_id}/unmute", dependencies=[Depends(verify_credentials)])
def unmute_alarm(alarm_id: int, db: Session = Depends(get_db)):
    from models import AlarmRecord
    a = db.query(AlarmRecord).filter(AlarmRecord.id == alarm_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alarm not found")
    a.is_muted = False
    db.commit()
    return {"success": True, "message": "Alarm unmuted"}

@app.post("/api/alarms/clear-all", dependencies=[Depends(verify_credentials)])
def clear_all_alarms(db: Session = Depends(get_db)):
    from models import AlarmRecord
    db.query(AlarmRecord).delete()
    db.commit()
    return {"success": True, "message": "All alarms cleared"}

class ScheduleCreate(BaseModel):
    project_id: int
    schedule_expression: str
    backup_type: str
    retention_days: int

@app.post("/api/backups/schedules", dependencies=[Depends(verify_credentials)])
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)):
    from models import BackupSchedule
    proj = db.query(Project).filter(Project.id == payload.project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    sched = BackupSchedule(
        project_id=proj.id,
        cluster_name=proj.name,
        schedule_expression=payload.schedule_expression,
        backup_type=payload.backup_type,
        retention_days=payload.retention_days
    )
    db.add(sched)
    db.commit()
    return {"success": True, "message": "Schedule created"}

@app.get("/api/backups/schedules", dependencies=[Depends(verify_credentials)])
def get_schedules(db: Session = Depends(get_db)):
    from models import BackupSchedule
    scheds = db.query(BackupSchedule).order_by(BackupSchedule.id.desc()).all()
    results = []
    for s in scheds:
        results.append({
            "id": s.id,
            "project_id": s.project_id,
            "cluster_name": s.cluster_name,
            "schedule_expression": s.schedule_expression,
            "backup_type": s.backup_type,
            "retention_days": s.retention_days,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else ""
        })
    return results


class UserCreate(BaseModel):
    username: str
    password: str
    role: str

@app.get("/api/users", dependencies=[Depends(verify_credentials)])
def get_users(db: Session = Depends(get_db)):
    from models import User
    db_users = db.query(User).order_by(User.id.asc()).all()

    result = []
    admin_username = ADMIN_USER or ""
    admin_in_db = any(u.username == admin_username for u in db_users)

    # Always include the env-var admin user first (even if not in DB)
    if not admin_in_db and admin_username:
        result.append({
            "id": 0,
            "username": admin_username,
            "email": f"{admin_username}@localhost",
            "first_name": admin_username.capitalize(),
            "last_name": "",
            "role": "admin",
            "team": "admins",
            "timezone": "UTC",
            "origin": "cmon",
            "status": "Enabled",
            "created_at": ""
        })

    for u in db_users:
        result.append({
            "id": u.id,
            "username": u.username,
            "email": u.email or f"{u.username}@localhost",
            "first_name": u.first_name or u.username.capitalize(),
            "last_name": u.last_name or "",
            "role": u.role,
            "team": "admins" if u.role == "admin" else "viewers",
            "timezone": u.timezone or "UTC",
            "origin": "cmon",
            "status": "Enabled",
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else ""
        })
    return result

@app.post("/api/users", dependencies=[Depends(verify_credentials)])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    from models import User
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        return JSONResponse(status_code=400, content={"message": "Username already exists"})
    new_user = User(username=payload.username, password_hash=hash_password(payload.password), role=payload.role)
    db.add(new_user)
    db.commit()
    return {"success": True}

@app.delete("/api/users/{user_id}", dependencies=[Depends(verify_credentials)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    from models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    if db.query(User).count() == 1:
        return JSONResponse(status_code=400, content={"message": "Cannot delete the last user"})
    db.delete(user)
    db.commit()
    return {"success": True}


@app.get("/api/users/me", dependencies=[Depends(verify_credentials)])
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    from models import User
    username = credentials.username
    user = db.query(User).filter(User.username == username).first()
    role = user.role if user else ("admin" if username == os.environ.get("ADMIN_USER") else "viewer")
    
    email = (user.email if user and user.email else f"{username}@localhost")
    first_name = (user.first_name if user and user.first_name else username.capitalize())
    last_name = (user.last_name if user and user.last_name else "")
    timezone = (user.timezone if user and user.timezone else "UTC")
    
    return {
        "username": username,
        "role": role,
        "team": "admins" if role == "admin" else "viewers",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "timezone": timezone
    }


class ProfileUpdateModel(BaseModel):
    email: str
    first_name: str = ""
    last_name: str = ""
    timezone: str = "UTC"


@app.put("/api/users/profile", dependencies=[Depends(verify_credentials)])
def update_profile(data: ProfileUpdateModel, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    from models import User
    import secrets
    username = credentials.username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(
            username=username,
            password_hash=hash_password(ADMIN_PASS) if username == ADMIN_USER else secrets.token_hex(16),
            role="admin" if username == os.environ.get("ADMIN_USER") else "viewer"
        )
        db.add(user)
    
    user.email = data.email.strip()
    user.first_name = data.first_name.strip()
    user.last_name = data.last_name.strip()
    user.timezone = data.timezone.strip() or "UTC"
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "username": user.username,
        "role": user.role,
        "team": "admins" if user.role == "admin" else "viewers",
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "timezone": user.timezone
    }


class ChangePasswordModel(BaseModel):
    current_password: str
    new_password: str
    repeat_password: str


@app.post("/api/users/change-password", dependencies=[Depends(verify_credentials)])
def change_password(data: ChangePasswordModel, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    from models import User
    username = credentials.username
    user = db.query(User).filter(User.username == username).first()

    # 1. Verify current password
    current_valid = False
    if user and user.password_hash:
        current_valid = verify_password(data.current_password, user.password_hash)
    if not current_valid and username == ADMIN_USER and data.current_password == ADMIN_PASS:
        current_valid = True

    if not current_valid:
        return JSONResponse(status_code=400, content={"message": "Please enter correct current password", "field": "current"})

    if data.current_password == data.new_password:
        return JSONResponse(status_code=400, content={"message": "Current and new password should not be the same!", "field": "new"})

    if data.new_password != data.repeat_password:
        return JSONResponse(status_code=400, content={"message": "Passwords do not match!", "field": "repeat"})

    if len(data.new_password.strip()) < 4:
        return JSONResponse(status_code=400, content={"message": "Password must be at least 4 characters", "field": "new"})

    if not user:
        user = User(
            username=username,
            role="admin" if username == ADMIN_USER else "viewer"
        )
        db.add(user)

    user.password_hash = hash_password(data.new_password)
    db.commit()
    db.refresh(user)

    return {"success": True, "message": "Password changed successfully"}


# ----------------------------------------------------
# ADDONS & INTEGRATIONS (Ops-Center & Kubernetes)
# ----------------------------------------------------

class EnableOpsCenterModel(BaseModel):
    root_username: str
    email: str = ""
    root_password: str
    confirm_root_password: str


class EnableK8sModel(BaseModel):
    enabled: bool = True


class ControllerCreateModel(BaseModel):
    name: str
    url: str
    api_token: str = ""


class KubeClusterCreateModel(BaseModel):
    name: str
    kubeconfig_yaml: str
    namespace: str = "default"


@app.get("/api/addons", dependencies=[Depends(verify_credentials)])
def get_addons(db: Session = Depends(get_db)):
    from models import AddonSetting, OpsController, KubeCluster
    import json
    
    ops_setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "ops_center").first()
    k8s_setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "kubernetes").first()
    
    ops_data = {}
    if ops_setting and ops_setting.extra_json:
        try:
            ops_data = json.loads(ops_setting.extra_json)
        except Exception:
            pass

    ops_controllers_count = db.query(OpsController).count()
    k8s_clusters_count = db.query(KubeCluster).count()

    return {
        "ops_center": {
            "enabled": bool(ops_setting.enabled) if ops_setting else False,
            "root_username": ops_data.get("root_username", "root"),
            "email": ops_data.get("email", ""),
            "controllers_count": ops_controllers_count,
            "mode": "multi-controller" if (ops_setting and ops_setting.enabled) else "single-controller"
        },
        "kubernetes": {
            "enabled": bool(k8s_setting.enabled) if k8s_setting else False,
            "clusters_count": k8s_clusters_count
        }
    }


@app.post("/api/addons/ops-center/enable", dependencies=[Depends(verify_credentials)])
def enable_ops_center(data: EnableOpsCenterModel, db: Session = Depends(get_db)):
    from models import AddonSetting, OpsController, Project
    import json
    
    if not data.root_username.strip():
        return JSONResponse(status_code=400, content={"message": "Root username is required"})
    if not data.root_password:
        return JSONResponse(status_code=400, content={"message": "Root password is required"})
    if data.root_password != data.confirm_root_password:
        return JSONResponse(status_code=400, content={"message": "Root passwords do not match"})

    setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "ops_center").first()
    if not setting:
        setting = AddonSetting(addon_key="ops_center")
        db.add(setting)

    setting.enabled = True
    setting.extra_json = json.dumps({
        "root_username": data.root_username.strip(),
        "email": data.email.strip(),
        "root_password_hash": hash_password(data.root_password)
    })
    
    # Ensure a local controller entry exists
    primary_ctrl = db.query(OpsController).filter(OpsController.is_primary == True).first()
    if not primary_ctrl:
        local_ctrl = OpsController(
            name="Primary Controller (Local)",
            url="http://127.0.0.1:8000",
            status="ONLINE",
            is_primary=True,
            version="2.5.0",
            cluster_count=db.query(Project).count()
        )
        db.add(local_ctrl)

    db.commit()
    return {"success": True, "message": "Ops-Center enabled successfully"}


@app.post("/api/addons/ops-center/disable", dependencies=[Depends(verify_credentials)])
def disable_ops_center(db: Session = Depends(get_db)):
    from models import AddonSetting
    setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "ops_center").first()
    if setting:
        setting.enabled = False
        db.commit()
    return {"success": True, "message": "Ops-Center disabled (Switched to Single-Controller mode)"}


@app.post("/api/addons/kubernetes/enable", dependencies=[Depends(verify_credentials)])
def enable_kubernetes(db: Session = Depends(get_db)):
    from models import AddonSetting
    setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "kubernetes").first()
    if not setting:
        setting = AddonSetting(addon_key="kubernetes")
        db.add(setting)
    setting.enabled = True
    db.commit()
    return {"success": True, "message": "Kubernetes integration enabled"}


@app.post("/api/addons/kubernetes/disable", dependencies=[Depends(verify_credentials)])
def disable_kubernetes(db: Session = Depends(get_db)):
    from models import AddonSetting
    setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "kubernetes").first()
    if setting:
        setting.enabled = False
        db.commit()
    return {"success": True, "message": "Kubernetes integration disabled"}


# --- Ops-Center Controller Endpoints ---

@app.get("/api/ops-center/controllers", dependencies=[Depends(verify_credentials)])
def get_ops_controllers(db: Session = Depends(get_db)):
    from ops_center_worker import sync_all_controllers
    return sync_all_controllers(db)


@app.post("/api/ops-center/controllers", dependencies=[Depends(verify_credentials)])
def add_ops_controller(data: ControllerCreateModel, db: Session = Depends(get_db)):
    from models import OpsController
    from vault import encrypt
    from ops_center_worker import ping_controller
    
    if not data.name.strip() or not data.url.strip():
        return JSONResponse(status_code=400, content={"message": "Name and URL are required"})

    ping_res = ping_controller(data.url, data.api_token)
    ctrl = OpsController(
        name=data.name.strip(),
        url=data.url.strip(),
        encrypted_api_token=encrypt(data.api_token) if data.api_token else None,
        status="ONLINE" if ping_res.get("online") else "OFFLINE",
        is_primary=False,
        version="2.5.0",
        cluster_count=0
    )
    db.add(ctrl)
    db.commit()
    db.refresh(ctrl)
    return {"success": True, "id": ctrl.id, "name": ctrl.name, "status": ctrl.status, "ping": ping_res}


@app.delete("/api/ops-center/controllers/{ctrl_id}", dependencies=[Depends(verify_credentials)])
def delete_ops_controller(ctrl_id: int, db: Session = Depends(get_db)):
    from models import OpsController
    ctrl = db.query(OpsController).filter(OpsController.id == ctrl_id).first()
    if not ctrl:
        return JSONResponse(status_code=404, content={"message": "Controller not found"})
    if ctrl.is_primary:
        return JSONResponse(status_code=400, content={"message": "Cannot delete the primary local controller"})
    db.delete(ctrl)
    db.commit()
    return {"success": True}


# --- Kubernetes Clusters Endpoints ---

@app.get("/api/k8s/clusters", dependencies=[Depends(verify_credentials)])
def get_k8s_clusters(db: Session = Depends(get_db)):
    from models import KubeCluster
    clusters = db.query(KubeCluster).order_by(KubeCluster.id.asc()).all()
    return [{
        "id": c.id,
        "name": c.name,
        "api_server_url": c.api_server_url or "-",
        "status": c.status,
        "namespace": c.namespace,
        "nodes_count": c.nodes_count,
        "pods_count": c.pods_count,
        "operator_installed": c.operator_installed,
        "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else ""
    } for c in clusters]


@app.post("/api/k8s/clusters", dependencies=[Depends(verify_credentials)])
def add_k8s_cluster(data: KubeClusterCreateModel, db: Session = Depends(get_db)):
    from models import KubeCluster
    from vault import encrypt
    from k8s_worker import validate_k8s_connection
    
    if not data.name.strip():
        return JSONResponse(status_code=400, content={"message": "Cluster name is required"})
    if not data.kubeconfig_yaml.strip():
        return JSONResponse(status_code=400, content={"message": "Kubeconfig YAML content is required"})

    val_res = validate_k8s_connection(data.kubeconfig_yaml)
    if not val_res.get("success"):
        return JSONResponse(status_code=400, content={"message": val_res.get("error", "Kubeconfig validation failed")})

    cluster = KubeCluster(
        name=data.name.strip(),
        encrypted_kubeconfig=encrypt(data.kubeconfig_yaml),
        api_server_url=val_res.get("api_server", ""),
        status="CONNECTED",
        namespace=data.namespace.strip() or "default",
        nodes_count=val_res.get("nodes_count", 1),
        operator_installed=val_res.get("operator", "CloudNativePG")
    )
    db.add(cluster)
    db.commit()
    db.refresh(cluster)
    return {"success": True, "id": cluster.id, "name": cluster.name, "message": val_res.get("message")}


@app.get("/api/k8s/clusters/{cluster_id}/pods", dependencies=[Depends(verify_credentials)])
def get_k8s_cluster_pods(cluster_id: int, db: Session = Depends(get_db)):
    from models import KubeCluster
    from vault import decrypt
    from k8s_worker import list_k8s_pods
    
    cluster = db.query(KubeCluster).filter(KubeCluster.id == cluster_id).first()
    if not cluster:
        return JSONResponse(status_code=404, content={"message": "Kubernetes cluster not found"})

    kubeconfig = decrypt(cluster.encrypted_kubeconfig)
    pods = list_k8s_pods(kubeconfig, cluster.namespace)
    return {"cluster_id": cluster.id, "namespace": cluster.namespace, "pods": pods}


class K8sDeployDbModel(BaseModel):
    db_name: str
    replicas: int = 2
    db_pass: str = "postgres123"


@app.post("/api/k8s/clusters/{cluster_id}/deploy-db", dependencies=[Depends(verify_credentials)])
def deploy_k8s_database(cluster_id: int, data: K8sDeployDbModel, db: Session = Depends(get_db)):
    from models import KubeCluster
    from vault import decrypt
    from k8s_worker import deploy_k8s_postgres
    
    cluster = db.query(KubeCluster).filter(KubeCluster.id == cluster_id).first()
    if not cluster:
        return JSONResponse(status_code=404, content={"message": "Kubernetes cluster not found"})

    kubeconfig = decrypt(cluster.encrypted_kubeconfig)
    res = deploy_k8s_postgres(
        kubeconfig_str=kubeconfig,
        namespace=cluster.namespace,
        cluster_name=data.db_name.strip().lower().replace(" ", "-"),
        replicas=data.replicas,
        db_pass=data.db_pass
    )
    if not res.get("success"):
        return JSONResponse(status_code=400, content={"message": res.get("error", "Deployment failed")})
    return res


@app.delete("/api/k8s/clusters/{cluster_id}", dependencies=[Depends(verify_credentials)])
def delete_k8s_cluster(cluster_id: int, db: Session = Depends(get_db)):
    from models import KubeCluster
    cluster = db.query(KubeCluster).filter(KubeCluster.id == cluster_id).first()
    if not cluster:
        return JSONResponse(status_code=404, content={"message": "Cluster not found"})
    db.delete(cluster)
    db.commit()
    return {"success": True}


@app.get("/api/debug/metrics/{project_id}", dependencies=[Depends(verify_credentials)])
async def debug_metrics(project_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    from vault import decrypt
    import asyncio
    
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return {"error": "Project not found"}
    
    results = []
    for node in proj.nodes:
        url = decrypt(node.encrypted_url) if node.encrypted_url else None
        node_dict = {
            'id': node.id, 'name': node.name, 'role': node.role,
            'encrypted_url': node.encrypted_url,
            'ssh_host': node.ssh_host, 'ssh_port': node.ssh_port,
            'ssh_username': node.ssh_username,
            'encrypted_ssh_credential': node.encrypted_ssh_credential,
            'metric_table': proj.metric_table
        }
        metrics = await get_server_metrics(node_dict, project_id=proj.id)
        results.append({
            "node_id": node.id,
            "node_name": node.name,
            "has_url": bool(node.encrypted_url),
            "decrypted_url_preview": url[:30] + "..." if url and len(url) > 30 else url,
            "metrics": metrics
        })
    return results
@app.get('/api/projects/{project_id}/performance')
async def get_project_performance(project_id: int, db: Session = Depends(get_db)):
    from vault import decrypt
    import asyncpg
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
        
    primary_node = next((n for n in proj.nodes if n.role and n.role.lower() == 'primary'), None)
    standby_node = next((n for n in proj.nodes if n.role and n.role.lower() == 'standby'), None)
    
    data = {
        'variables': [],
        'queries': [],
        'schema': [],
        'deadlocks': 0,
        'nodes': [{'id': n.id, 'name': n.name, 'role': n.role} for n in proj.nodes]
    }
    
    target_node = primary_node or (proj.nodes[0] if proj.nodes else None)
    if target_node and target_node.encrypted_url:
        db_url = decrypt(target_node.encrypted_url)
        if db_url:
            try:
                conn = await asyncpg.connect(db_url, timeout=10)
                
                # Fetch settings variables
                vars_rows = await conn.fetch("SELECT name, setting, COALESCE(unit, '') as unit, short_desc FROM pg_settings ORDER BY name LIMIT 100")
                data['variables'] = [{
                    'name': r['name'],
                    'setting': r['setting'],
                    'unit': r['unit'],
                    'desc': r['short_desc']
                } for r in vars_rows]
                
                # Fetch active queries
                query_rows = await conn.fetch("SELECT pid, usename, COALESCE(client_addr::text, 'local') as client, state, query, COALESCE(age(clock_timestamp(), query_start)::text, '0s') as duration FROM pg_stat_activity WHERE state != 'idle' AND query NOT LIKE '%pg_stat_activity%' LIMIT 20")
                data['queries'] = [{
                    'pid': r['pid'],
                    'user': r['usename'],
                    'client': r['client'],
                    'state': r['state'],
                    'query': r['query'],
                    'duration': r['duration']
                } for r in query_rows]
                
                # Fetch schema tables
                schema_rows = await conn.fetch("SELECT table_name, (SELECT count(*) FROM information_schema.columns WHERE table_name = t.table_name) as col_count FROM information_schema.tables t WHERE table_schema='public' ORDER BY table_name")
                for r in schema_rows:
                    t_name = r['table_name']
                    try:
                        row_count = await conn.fetchval(f'SELECT count(*) FROM "{t_name}"')
                    except Exception:
                        row_count = 0
                    data['schema'].append({
                        'table_name': t_name,
                        'col_count': r['col_count'],
                        'row_count': row_count
                    })
                    
                # Fetch deadlocks count
                deadlocks_val = await conn.fetchval("SELECT deadlocks FROM pg_stat_database WHERE datname=current_database()")
                data['deadlocks'] = deadlocks_val or 0
                
                await conn.close()
            except Exception as e:
                print(f"Performance API DB error: {e}")
                
    return data


# ─────────────────────────────────────────────────────────────────────────────
# JOBS — Activity Center Jobs tab (real SyncJob data)
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/jobs", dependencies=[Depends(verify_credentials)])
def get_jobs(project_id: int = None, db: Session = Depends(get_db)):
    """Return all SyncJobs, optionally filtered by project_id."""
    from models import SyncJob, Project
    q = db.query(SyncJob)
    if project_id:
        q = q.filter(SyncJob.project_id == project_id)
    jobs = q.order_by(SyncJob.id.desc()).limit(100).all()
    results = []
    for j in jobs:
        proj = db.query(Project).filter(Project.id == j.project_id).first()
        started = j.created_at.strftime("%Y-%m-%d %H:%M:%S") if j.created_at else ""
        completed = j.completed_at.strftime("%Y-%m-%d %H:%M:%S") if j.completed_at else ""
        duration = ""
        if j.created_at and j.completed_at:
            secs = int((j.completed_at - j.created_at).total_seconds())
            duration = f"{secs}s"
        elif j.created_at and j.status not in ("SUCCESS", "FAILED"):
            import datetime as _dt
            secs = int((_dt.datetime.utcnow() - j.created_at).total_seconds())
            duration = f"{secs}s (running)"
        results.append({
            "id": j.id,
            "project_id": j.project_id,
            "cluster": proj.name if proj else "Unknown",
            "status": j.status,
            "started": started,
            "completed": completed,
            "duration": duration,
            "message": j.error_message or "",
        })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# REPORTS — Real HTML report generation + download
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/reports/{report_id}/download", dependencies=[Depends(verify_credentials)])
@app.get("/api/reports/{report_id}/download", dependencies=[Depends(verify_credentials)])
async def download_report(report_id: int, db: Session = Depends(get_db)):
    """Generate (or retrieve) and stream an HTML operational report."""
    from fastapi.responses import FileResponse, HTMLResponse as _HTMLResponse
    from models import OperationalReport, AuditLog, BackupJob, SyncJob
    import os as _os, datetime as _dt

    rep = db.query(OperationalReport).filter(OperationalReport.id == report_id).first()
    if not rep:
        return JSONResponse(status_code=404, content={"message": "Report not found"})

    reports_dir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "reports")
    _os.makedirs(reports_dir, exist_ok=True)
    file_path = _os.path.join(reports_dir, rep.file_name.replace(".pdf", ".html"))

    # Always regenerate so the data is fresh
    proj = db.query(Project).filter(Project.id == rep.project_id).first()
    proj_name = proj.name if proj else "Unknown Cluster"

    cutoff = _dt.datetime.utcnow() - _dt.timedelta(days=rep.data_range_days)
    audit_logs = db.query(AuditLog).filter(
        AuditLog.project_id == rep.project_id,
        AuditLog.timestamp >= cutoff
    ).order_by(AuditLog.timestamp.desc()).limit(100).all()

    backup_jobs = db.query(BackupJob).filter(
        BackupJob.project_id == rep.project_id,
        BackupJob.created_at >= cutoff
    ).order_by(BackupJob.id.desc()).limit(50).all()

    sync_jobs = db.query(SyncJob).filter(
        SyncJob.project_id == rep.project_id,
        SyncJob.created_at >= cutoff
    ).order_by(SyncJob.id.desc()).limit(20).all()

    now_str = _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    def _row_color(status):
        return {"SUCCESS": "#d1fae5", "COMPLETED": "#d1fae5",
                "FAILED": "#fee2e2", "IN_PROGRESS": "#fef3c7"}.get(status, "#f9fafb")

    audit_rows = "".join(
        f"<tr style='background:{_row_color(l.action)}'><td>{l.timestamp.strftime('%Y-%m-%d %H:%M') if l.timestamp else ''}</td>"
        f"<td>{l.action}</td><td>{l.details or ''}</td><td>{l.username or 'system'}</td></tr>"
        for l in audit_logs
    )
    backup_rows = "".join(
        f"<tr style='background:{_row_color(b.status)}'><td>{b.id}</td><td>{b.backup_type}</td>"
        f"<td>{b.status}</td><td>{b.size_mb:.1f} MB</td>"
        f"<td>{b.created_at.strftime('%Y-%m-%d %H:%M') if b.created_at else ''}</td></tr>"
        for b in backup_jobs
    )
    sync_rows = "".join(
        f"<tr style='background:{_row_color(j.status)}'><td>{j.id}</td><td>{j.status}</td>"
        f"<td>{j.created_at.strftime('%Y-%m-%d %H:%M') if j.created_at else ''}</td>"
        f"<td>{j.error_message or '-'}</td></tr>"
        for j in sync_jobs
    )

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><title>Operational Report — {proj_name}</title>
<style>
  body{{font-family:Inter,sans-serif;margin:40px;color:#111827;background:#f9fafb}}
  h1{{color:#3a1c94;border-bottom:3px solid #3a1c94;padding-bottom:8px}}
  h2{{color:#374151;margin-top:32px}}
  table{{width:100%;border-collapse:collapse;margin-top:12px;font-size:13px}}
  th{{background:#3a1c94;color:#fff;padding:10px 12px;text-align:left}}
  td{{padding:8px 12px;border-bottom:1px solid #e5e7eb}}
  .meta{{display:flex;gap:32px;margin-bottom:24px;background:#fff;padding:16px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
  .meta div{{display:flex;flex-direction:column;gap:4px}}
  .meta label{{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.05em}}
  .meta span{{font-weight:600;color:#111827}}
  .badge{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:700}}
</style>
</head>
<body>
<h1>📊 Operational Report</h1>
<div class="meta">
  <div><label>Cluster</label><span>{proj_name}</span></div>
  <div><label>Report Type</label><span>{rep.report_type}</span></div>
  <div><label>Data Range</label><span>Last {rep.data_range_days} days</span></div>
  <div><label>Generated</label><span>{now_str}</span></div>
  <div><label>Created By</label><span>{rep.created_by}</span></div>
</div>

<h2>Activity Log ({len(audit_logs)} events)</h2>
<table>
  <thead><tr><th>Timestamp</th><th>Action</th><th>Details</th><th>User</th></tr></thead>
  <tbody>{audit_rows if audit_rows else '<tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:20px">No activity in this period</td></tr>'}</tbody>
</table>

<h2>Backup Jobs ({len(backup_jobs)} jobs)</h2>
<table>
  <thead><tr><th>ID</th><th>Type</th><th>Status</th><th>Size</th><th>Started</th></tr></thead>
  <tbody>{backup_rows if backup_rows else '<tr><td colspan="5" style="text-align:center;color:#9ca3af;padding:20px">No backups in this period</td></tr>'}</tbody>
</table>

<h2>Replication Jobs ({len(sync_jobs)} jobs)</h2>
<table>
  <thead><tr><th>ID</th><th>Status</th><th>Started</th><th>Error</th></tr></thead>
  <tbody>{sync_rows if sync_rows else '<tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:20px">No sync jobs in this period</td></tr>'}</tbody>
</table>

<p style="margin-top:40px;font-size:11px;color:#9ca3af">Generated by ClusterControl Universal Server Manager · {now_str}</p>
</body></html>"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    return FileResponse(file_path, media_type="text/html",
                        filename=rep.file_name.replace(".pdf", ".html"))


@app.delete("/api/reports/{report_id}", dependencies=[Depends(verify_credentials)])
def delete_report(report_id: int, db: Session = Depends(get_db)):
    from models import OperationalReport
    import os as _os
    rep = db.query(OperationalReport).filter(OperationalReport.id == report_id).first()
    if not rep:
        return JSONResponse(status_code=404, content={"message": "Report not found"})
    # Try to delete file
    reports_dir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "reports")
    for ext in [".html", ".pdf"]:
        fp = _os.path.join(reports_dir, rep.file_name.replace(".pdf", ext))
        try:
            if _os.path.exists(fp):
                _os.remove(fp)
        except Exception:
            pass
    db.delete(rep)
    db.commit()
    return {"success": True}


# ─────────────────────────────────────────────────────────────────────────────
# CLOUD CREDENTIALS
# ─────────────────────────────────────────────────────────────────────────────

class CloudCredCreate(BaseModel):
    provider: str
    label: str
    key_id: str = ""
    secret: str = ""
    bucket: str = ""
    region: str = ""

@app.get("/api/cloud-credentials", dependencies=[Depends(verify_credentials)])
def get_cloud_credentials(db: Session = Depends(get_db)):
    from models import CloudCredential
    creds = db.query(CloudCredential).order_by(CloudCredential.id.desc()).all()
    return [{
        "id": c.id,
        "provider": c.provider,
        "label": c.label,
        "bucket": c.bucket or "",
        "region": c.region or "",
        "created_at": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
    } for c in creds]

@app.post("/api/cloud-credentials", dependencies=[Depends(verify_credentials)])
def create_cloud_credential(payload: CloudCredCreate, db: Session = Depends(get_db)):
    from models import CloudCredential
    from vault import encrypt as _enc
    if not payload.label.strip():
        return JSONResponse(status_code=400, content={"message": "Label is required"})
    cred = CloudCredential(
        provider=payload.provider,
        label=payload.label.strip(),
        encrypted_key_id=_enc(payload.key_id) if payload.key_id else None,
        encrypted_secret=_enc(payload.secret) if payload.secret else None,
        bucket=payload.bucket or None,
        region=payload.region or None,
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)
    return {"success": True, "id": cred.id}

@app.delete("/api/cloud-credentials/{cred_id}", dependencies=[Depends(verify_credentials)])
def delete_cloud_credential(cred_id: int, db: Session = Depends(get_db)):
    from models import CloudCredential
    c = db.query(CloudCredential).filter(CloudCredential.id == cred_id).first()
    if not c:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(c)
    db.commit()
    return {"success": True}

@app.post("/api/cloud-credentials/{cred_id}/test", dependencies=[Depends(verify_credentials)])
def test_cloud_credential(cred_id: int, db: Session = Depends(get_db)):
    from models import CloudCredential
    from vault import decrypt as _dec
    c = db.query(CloudCredential).filter(CloudCredential.id == cred_id).first()
    if not c:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    key_id = _dec(c.encrypted_key_id) if c.encrypted_key_id else ""
    secret = _dec(c.encrypted_secret) if c.encrypted_secret else ""
    provider = (c.provider or "").upper()
    try:
        if "AWS" in provider or "S3" in provider:
            import boto3
            from botocore.exceptions import BotoCoreError, ClientError
            s3 = boto3.client(
                "s3",
                aws_access_key_id=key_id,
                aws_secret_access_key=secret,
                region_name=c.region or "us-east-1"
            )
            if c.bucket:
                s3.head_bucket(Bucket=c.bucket)
                return {"success": True, "message": f"AWS S3 bucket '{c.bucket}' is accessible."}
            else:
                s3.list_buckets()
                return {"success": True, "message": "AWS S3 credentials are valid."}
        else:
            return {"success": False, "message": f"Connection test not yet implemented for provider: {c.provider}. Credentials saved successfully."}
    except Exception as e:
        return {"success": False, "message": f"Connection test failed: {str(e)}"}


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATION SERVICES
# ─────────────────────────────────────────────────────────────────────────────

class NotificationCreate(BaseModel):
    service_type: str
    label: str
    settings: dict = {}

@app.get("/api/notifications", dependencies=[Depends(verify_credentials)])
def get_notifications(db: Session = Depends(get_db)):
    from models import NotificationService
    svcs = db.query(NotificationService).order_by(NotificationService.id.desc()).all()
    result = []
    for s in svcs:
        import json as _json
        try:
            from vault import decrypt as _dec
            raw = _dec(s.encrypted_settings) if s.encrypted_settings else "{}"
            settings = _json.loads(raw)
        except Exception:
            settings = {}
        result.append({
            "id": s.id,
            "service_type": s.service_type,
            "label": s.label,
            "active": s.active,
            "host": settings.get("host", ""),
            "webhook_url": settings.get("webhook_url", ""),
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M") if s.created_at else ""
        })
    return result

@app.post("/api/notifications", dependencies=[Depends(verify_credentials)])
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    from models import NotificationService
    from vault import encrypt as _enc
    import json as _json
    if not payload.label.strip():
        return JSONResponse(status_code=400, content={"message": "Label is required"})
    enc = _enc(_json.dumps(payload.settings))
    svc = NotificationService(
        service_type=payload.service_type,
        label=payload.label.strip(),
        encrypted_settings=enc,
        active=True,
    )
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return {"success": True, "id": svc.id}

@app.delete("/api/notifications/{svc_id}", dependencies=[Depends(verify_credentials)])
def delete_notification(svc_id: int, db: Session = Depends(get_db)):
    from models import NotificationService
    s = db.query(NotificationService).filter(NotificationService.id == svc_id).first()
    if not s:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(s)
    db.commit()
    return {"success": True}

@app.post("/api/notifications/{svc_id}/test", dependencies=[Depends(verify_credentials)])
def test_notification(svc_id: int, db: Session = Depends(get_db)):
    from models import NotificationService
    from vault import decrypt as _dec
    import json as _json, smtplib, socket
    s = db.query(NotificationService).filter(NotificationService.id == svc_id).first()
    if not s:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    try:
        raw = _dec(s.encrypted_settings) if s.encrypted_settings else "{}"
        cfg = _json.loads(raw)
    except Exception:
        cfg = {}

    stype = (s.service_type or "").upper()
    try:
        if stype == "SMTP":
            host = cfg.get("host", "")
            port = int(cfg.get("port", 587))
            user = cfg.get("user", "")
            password = cfg.get("password", "")
            if not host:
                return {"success": False, "message": "SMTP host is not configured"}
            with smtplib.SMTP(host, port, timeout=10) as smtp:
                smtp.ehlo()
                if port in (587, 465):
                    try:
                        smtp.starttls()
                        smtp.ehlo()
                    except Exception:
                        pass
                if user and password:
                    smtp.login(user, password)
            return {"success": True, "message": f"SMTP connection to {host}:{port} successful."}
        elif stype == "SLACK":
            webhook = cfg.get("webhook_url", "")
            if not webhook:
                return {"success": False, "message": "Slack Webhook URL is not configured"}
            import urllib.request as _req, urllib.error as _uerr
            data = '{"text":"✅ ClusterControl notification test — connection successful!"}'.encode()
            req = _req.Request(webhook, data=data, headers={"Content-Type": "application/json"})
            with _req.urlopen(req, timeout=10) as resp:
                body = resp.read().decode()
            return {"success": True, "message": f"Slack webhook responded: {body}"}
        else:
            return {"success": False, "message": f"Test not implemented for {s.service_type}. Settings saved."}
    except Exception as e:
        return {"success": False, "message": f"Connection test failed: {str(e)}"}


def send_email_via_smtp(host: str, port: int, user: str, password: str, from_addr: str, to_addr: str, subject: str, body_html: str, tls_ssl: bool = True):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formatdate

    msg = MIMEMultipart("alternative")
    msg["From"] = from_addr or user or "ClusterControl <noreply@localhost>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    text_part = MIMEText("This is an automated notification from ClusterControl.", "plain", "utf-8")
    html_part = MIMEText(body_html, "html", "utf-8")
    msg.attach(text_part)
    msg.attach(html_part)

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.ehlo()
        if tls_ssl or port in (587, 465):
            try:
                server.starttls()
                server.ehlo()
            except Exception:
                pass
        if user and password:
            server.login(user, password)
        server.sendmail(msg["From"], [to_addr], msg.as_string())
    return True


class MailServerConfig(BaseModel):
    mail_type: str = "SMTP"
    server: str = ""
    port: int = 587
    username: str = ""
    password: str = ""
    reply_to: str = ""
    tls_ssl: bool = False
    frontend_url: str = ""
    send_test: bool = False
    sendmail_config: dict = {}

@app.get("/api/settings/mail-server", dependencies=[Depends(verify_credentials)])
def get_mail_server(db: Session = Depends(get_db)):
    from models import NotificationService
    from vault import decrypt as _dec
    import json as _json
    s = db.query(NotificationService).filter(NotificationService.service_type.in_(["SMTP", "SENDMAIL"])).first()
    if not s:
        return {"configured": False, "mail_type": None, "settings": {}}
    try:
        raw = _dec(s.encrypted_settings) if s.encrypted_settings else "{}"
        settings = _json.loads(raw)
    except Exception:
        settings = {}
    return {
        "configured": True,
        "id": s.id,
        "mail_type": s.service_type,
        "label": s.label,
        "settings": settings
    }

@app.post("/api/settings/mail-server", dependencies=[Depends(verify_credentials)])
def save_mail_server(payload: MailServerConfig, db: Session = Depends(get_db)):
    from models import NotificationService
    from vault import encrypt as _enc
    import json as _json
    
    s = db.query(NotificationService).filter(NotificationService.service_type.in_(["SMTP", "SENDMAIL"])).first()
    if not s:
        s = NotificationService(service_type=payload.mail_type.upper(), label=f"Mail Server ({payload.mail_type.upper()})", active=True)
        db.add(s)
    
    s.service_type = payload.mail_type.upper()
    s.label = f"Mail Server ({payload.mail_type.upper()})"
    
    settings_data = {
        "host": payload.server,
        "port": payload.port,
        "user": payload.username,
        "password": payload.password,
        "from_address": payload.reply_to,
        "reply_to": payload.reply_to,
        "tls_ssl": payload.tls_ssl,
        "frontend_url": payload.frontend_url,
        "sendmail_config": payload.sendmail_config
    }
    s.encrypted_settings = _enc(_json.dumps(settings_data))
    s.active = True
    db.commit()

    test_msg = ""
    if payload.send_test and payload.mail_type.upper() == "SMTP":
        try:
            target_to = payload.reply_to
            test_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
                <div style="background: #3a1c94; color: white; padding: 18px 24px; font-size: 18px; font-weight: bold;">
                    ClusterControl — Mail Server Test
                </div>
                <div style="padding: 24px; color: #374151; font-size: 14px; line-height: 1.6;">
                    <p>Hello,</p>
                    <p>This is a confirmation that your mail server configuration on <strong>ClusterControl</strong> is active and working properly.</p>
                    <p style="background: #f3f4f6; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 13px;">
                        <strong>SMTP Host:</strong> {payload.server}:{payload.port}<br>
                        <strong>Sender / Reply-To:</strong> {payload.reply_to}<br>
                        <strong>TLS/SSL:</strong> {'Enabled' if payload.tls_ssl else 'Disabled'}
                    </p>
                    <p style="color: #6b7280; font-size: 12px; margin-top: 24px;">Sent by ClusterControl Notification System</p>
                </div>
            </div>
            """
            send_email_via_smtp(
                host=payload.server,
                port=payload.port,
                user=payload.username,
                password=payload.password,
                from_addr=payload.reply_to,
                to_addr=target_to,
                subject="ClusterControl Mail Server Test",
                body_html=test_html,
                tls_ssl=payload.tls_ssl
            )
            test_msg = f" Test email successfully delivered to {target_to}."
        except Exception as e:
            test_msg = f" Note: Test email delivery attempted but failed: {str(e)}"

    return {"success": True, "message": f"Mail server configuration saved.{test_msg}"}


# ─────────────────────────────────────────────────────────────────────────────
# CERTIFICATE MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/certificates", dependencies=[Depends(verify_credentials)])
def get_certificates(node_id: int = None, db: Session = Depends(get_db)):
    from models import CertificateRecord, DatabaseNode
    q = db.query(CertificateRecord)
    if node_id:
        q = q.filter(CertificateRecord.node_id == node_id)
    certs = q.order_by(CertificateRecord.id.desc()).all()
    result = []
    for c in certs:
        node = db.query(DatabaseNode).filter(DatabaseNode.id == c.node_id).first() if c.node_id else None
        result.append({
            "id": c.id,
            "node_id": c.node_id,
            "node_name": node.name if node else "Unknown",
            "cert_type": c.cert_type,
            "common_name": c.common_name or "",
            "subject_alt_names": c.subject_alt_names or "",
            "expires_at": c.expires_at.strftime("%Y-%m-%d") if c.expires_at else "",
            "issuer": c.issuer or "",
            "file_path": c.file_path or "",
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
        })
    return result

@app.post("/api/certificates/scan/{node_id}", dependencies=[Depends(verify_credentials)])
def scan_node_certificates(node_id: int, db: Session = Depends(get_db)):
    """Scan a node's filesystem for TLS certificates via SSH, store results."""
    from models import DatabaseNode, CertificateRecord
    from vault import decrypt as _dec
    from ssh_worker import SSHManager
    import datetime as _dt, re as _re

    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={"message": "Node not found"})
    if not node.ssh_host:
        return JSONResponse(status_code=400, content={"message": "SSH not configured for this node"})

    credential = _dec(node.encrypted_ssh_credential) if node.encrypted_ssh_credential else ""
    found = []
    try:
        with SSHManager(node.ssh_host, node.ssh_port, node.ssh_username, credential) as ssh:
            # Find .crt files in common locations
            stdout, _, _ = ssh.execute_command(
                "find /etc/ssl /etc/postgresql /etc/pki /var/lib/ssl 2>/dev/null -name '*.crt' -o -name '*.pem' 2>/dev/null | head -30"
            )
            cert_files = [f.strip() for f in stdout.splitlines() if f.strip()]

            for fpath in cert_files:
                try:
                    out, _, code = ssh.execute_command(
                        f"openssl x509 -in '{fpath}' -noout -subject -issuer -dates -ext subjectAltName 2>/dev/null"
                    )
                    if code != 0:
                        continue
                    cn_match = _re.search(r'CN\s*=\s*([^\n,/]+)', out)
                    issuer_match = _re.search(r'issuer=([^\n]+)', out)
                    exp_match = _re.search(r'notAfter=(.*)', out)
                    san_match = _re.search(r'DNS:[^\n]+', out)

                    cn = cn_match.group(1).strip() if cn_match else fpath.split("/")[-1]
                    issuer = issuer_match.group(1).strip()[:255] if issuer_match else ""
                    san = san_match.group(0).strip()[:500] if san_match else ""
                    expires_at = None
                    if exp_match:
                        try:
                            expires_at = _dt.datetime.strptime(exp_match.group(1).strip(), "%b %d %H:%M:%S %Y %Z")
                        except Exception:
                            pass

                    # Upsert: delete old record for same node+file, insert new
                    db.query(CertificateRecord).filter(
                        CertificateRecord.node_id == node_id,
                        CertificateRecord.file_path == fpath
                    ).delete()
                    rec = CertificateRecord(
                        node_id=node_id,
                        cert_type="TLS",
                        common_name=cn[:255],
                        subject_alt_names=san,
                        expires_at=expires_at,
                        issuer=issuer,
                        file_path=fpath
                    )
                    db.add(rec)
                    found.append(cn)
                except Exception:
                    continue

        db.commit()
        return {"success": True, "found": len(found), "certificates": found}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"SSH scan failed: {str(e)}"})

@app.delete("/api/certificates/{cert_id}", dependencies=[Depends(verify_credentials)])
def delete_certificate(cert_id: int, db: Session = Depends(get_db)):
    from models import CertificateRecord
    c = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
    if not c:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(c)
    db.commit()
    return {"success": True}


# ─────────────────────────────────────────────────────────────────────────────
# LICENSE — Dynamic node count from DB
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/license", dependencies=[Depends(verify_credentials)])
def get_license(db: Session = Depends(get_db)):
    from models import DatabaseNode
    total_nodes = db.query(DatabaseNode).count()
    node_limit = int(os.environ.get("LICENSE_NODE_LIMIT", "25"))
    owner = os.environ.get("LICENSE_OWNER", "ClusterControl Enterprise")
    expires = os.environ.get("LICENSE_EXPIRES", "2027-12-31")
    license_type = os.environ.get("LICENSE_TYPE", "Enterprise")
    return {
        "owner": owner,
        "type": license_type,
        "expires": expires,
        "total_nodes": total_nodes,
        "node_limit": node_limit,
        "nodes_available": max(0, node_limit - total_nodes),
        "percent_used": round((total_nodes / node_limit) * 100, 1) if node_limit > 0 else 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# ADDONS — Kubernetes & Ops-Center toggle + health check
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/addons", dependencies=[Depends(verify_credentials)])
def get_addons(db: Session = Depends(get_db)):
    from models import AddonSetting
    import json as _json
    def _addon(key, default_url=""):
        rec = db.query(AddonSetting).filter(AddonSetting.addon_key == key).first()
        if rec:
            return {"key": key, "enabled": rec.enabled, "api_url": rec.api_url or ""}
        return {"key": key, "enabled": False, "api_url": default_url}
    return {
        "kubernetes": _addon("kubernetes", os.environ.get("KUBERNETES_API_URL", "")),
        "ops_center": _addon("ops_center", os.environ.get("OPS_CENTER_URL", "")),
    }

class AddonUpdate(BaseModel):
    enabled: bool
    api_url: str = ""

@app.put("/api/addons/{addon_key}", dependencies=[Depends(verify_credentials)])
def update_addon(addon_key: str, payload: AddonUpdate, db: Session = Depends(get_db)):
    from models import AddonSetting
    import datetime as _dt
    allowed = {"kubernetes", "ops_center"}
    if addon_key not in allowed:
        return JSONResponse(status_code=400, content={"message": "Unknown addon"})
    rec = db.query(AddonSetting).filter(AddonSetting.addon_key == addon_key).first()
    if rec:
        rec.enabled = payload.enabled
        rec.api_url = payload.api_url
        rec.updated_at = _dt.datetime.utcnow()
    else:
        rec = AddonSetting(addon_key=addon_key, enabled=payload.enabled, api_url=payload.api_url)
        db.add(rec)
    db.commit()
    return {"success": True}

@app.post("/api/addons/{addon_key}/test", dependencies=[Depends(verify_credentials)])
def test_addon(addon_key: str, db: Session = Depends(get_db)):
    from models import AddonSetting
    import urllib.request as _req
    rec = db.query(AddonSetting).filter(AddonSetting.addon_key == addon_key).first()
    api_url = (rec.api_url if rec else "") or ""
    if not api_url:
        env_key = "KUBERNETES_API_URL" if addon_key == "kubernetes" else "OPS_CENTER_URL"
        api_url = os.environ.get(env_key, "")
    if not api_url:
        return {"success": False, "message": "API URL is not configured"}
    endpoint_map = {"kubernetes": "/healthz", "ops_center": "/status"}
    endpoint = endpoint_map.get(addon_key, "/health")
    full_url = api_url.rstrip("/") + endpoint
    try:
        req = _req.Request(full_url, headers={"Accept": "application/json"})
        with _req.urlopen(req, timeout=8) as resp:
            body = resp.read().decode()[:200]
        return {"success": True, "message": f"Connected: {full_url} → {body}"}
    except Exception as e:
        return {"success": False, "message": f"Connection failed: {str(e)}"}


# ─────────────────────────────────────────────────────────────────────────────
# LDAP CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

class LDAPCreate(BaseModel):
    label: str
    server_url: str
    base_dn: str
    bind_user: str = ""
    bind_pass: str = ""
    user_filter: str = "(objectClass=person)"

@app.get("/api/ldap", dependencies=[Depends(verify_credentials)])
def get_ldap_configs(db: Session = Depends(get_db)):
    from models import LDAPConfig
    configs = db.query(LDAPConfig).order_by(LDAPConfig.id.desc()).all()
    return [{
        "id": c.id,
        "label": c.label,
        "server_url": c.server_url,
        "base_dn": c.base_dn,
        "bind_user": c.bind_user or "",
        "user_filter": c.user_filter or "(objectClass=person)",
        "active": c.active,
        "created_at": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
    } for c in configs]

@app.post("/api/ldap", dependencies=[Depends(verify_credentials)])
def create_ldap_config(payload: LDAPCreate, db: Session = Depends(get_db)):
    from models import LDAPConfig
    from vault import encrypt as _enc
    if not payload.label.strip() or not payload.server_url.strip() or not payload.base_dn.strip():
        return JSONResponse(status_code=400, content={"message": "Label, server URL and Base DN are required"})
    cfg = LDAPConfig(
        label=payload.label.strip(),
        server_url=payload.server_url.strip(),
        base_dn=payload.base_dn.strip(),
        bind_user=payload.bind_user or None,
        encrypted_bind_pass=_enc(payload.bind_pass) if payload.bind_pass else None,
        user_filter=payload.user_filter or "(objectClass=person)",
        active=True,
    )
    db.add(cfg)
    db.commit()
    db.refresh(cfg)
    return {"success": True, "id": cfg.id}

@app.delete("/api/ldap/{config_id}", dependencies=[Depends(verify_credentials)])
def delete_ldap_config(config_id: int, db: Session = Depends(get_db)):
    from models import LDAPConfig
    c = db.query(LDAPConfig).filter(LDAPConfig.id == config_id).first()
    if not c:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(c)
    db.commit()
    return {"success": True}

@app.post("/api/ldap/{config_id}/test", dependencies=[Depends(verify_credentials)])
def test_ldap_config(config_id: int, db: Session = Depends(get_db)):
    from models import LDAPConfig
    from vault import decrypt as _dec
    c = db.query(LDAPConfig).filter(LDAPConfig.id == config_id).first()
    if not c:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    try:
        import ldap3
        server = ldap3.Server(c.server_url, get_info=ldap3.ALL, connect_timeout=10)
        bind_user = c.bind_user or ""
        bind_pass = _dec(c.encrypted_bind_pass) if c.encrypted_bind_pass else ""
        conn = ldap3.Connection(server, user=bind_user or None, password=bind_pass or None,
                                auto_bind=ldap3.AUTO_BIND_NO_TLS)
        result = conn.bind()
        if result:
            conn.unbind()
            return {"success": True, "message": f"LDAP bind successful to {c.server_url}"}
        else:
            return {"success": False, "message": f"LDAP bind failed: {conn.result}"}
    except Exception as e:
        return {"success": False, "message": f"LDAP connection failed: {str(e)}"}


# ─────────────────────────────────────────────────────────────────────────────
# BACKUPS — Real pg_dump via SSH
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/backups/run/{backup_job_id}", dependencies=[Depends(verify_credentials)])
async def run_backup_via_ssh(backup_job_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Trigger actual pg_dump on the primary node's server via SSH (runs in background)."""
    from models import BackupJob, DatabaseNode
    from vault import decrypt as _dec

    job = db.query(BackupJob).filter(BackupJob.id == backup_job_id).first()
    if not job:
        return JSONResponse(status_code=404, content={"message": "Backup job not found"})

    proj = db.query(Project).filter(Project.id == job.project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})

    primary = next((n for n in proj.nodes if n.role and n.role.lower() == "primary"), None)
    if not primary:
        return JSONResponse(status_code=400, content={"message": "No primary node configured"})

    if not primary.ssh_host:
        return JSONResponse(status_code=400, content={"message": "Primary node has no SSH configured. Cannot run pg_dump remotely."})

    # Kick off in background
    async def _run_dump():
        import datetime as _dt
        from models import SessionLocal as _SL, BackupJob as _BJ, AuditLog as _AL
        from vault import decrypt as _d
        from ssh_worker import SSHManager
        _db = _SL()
        try:
            _job = _db.query(_BJ).filter(_BJ.id == backup_job_id).first()
            if not _job:
                return
            node = _db.query(DatabaseNode).filter(DatabaseNode.id == primary.id).first()
            credential = _d(node.encrypted_ssh_credential) if node.encrypted_ssh_credential else ""
            db_url = _d(node.encrypted_url) if node.encrypted_url else ""
            # Extract DB name from URL
            db_name = db_url.split("/")[-1].split("?")[0] if db_url else "postgres"
            ts = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            dump_file = f"/tmp/ccweb_backup_{_job.project_id}_{ts}.dump"

            with SSHManager(node.ssh_host, node.ssh_port or 22, node.ssh_username or "root", credential) as ssh:
                cmd = f"pg_dump -Fc --dbname='{db_url}' -f '{dump_file}' 2>&1"
                stdout, stderr, code = ssh.execute_command(cmd)
                if code == 0:
                    # Get file size
                    sz_out, _, _ = ssh.execute_command(f"stat -c%s '{dump_file}' 2>/dev/null || echo 0")
                    size_bytes = int((sz_out.strip() or "0"))
                    _job.status = "COMPLETED"
                    _job.size_mb = round(size_bytes / (1024 * 1024), 2)
                    _job.completed_at = _dt.datetime.utcnow()
                    audit = _AL(project_id=_job.project_id, action="Backup Completed",
                                details=f"File: {dump_file}, Size: {_job.size_mb} MB")
                else:
                    _job.status = "FAILED"
                    _job.completed_at = _dt.datetime.utcnow()
                    audit = _AL(project_id=_job.project_id, action="Backup Failed",
                                details=f"pg_dump error: {stderr[:300]}")
            _db.add(audit)
            _db.commit()
        except Exception as ex:
            try:
                _job2 = _db.query(_BJ).filter(_BJ.id == backup_job_id).first()
                if _job2:
                    _job2.status = "FAILED"
                    _job2.completed_at = _dt.datetime.utcnow()
                    _db.commit()
            except Exception:
                pass
            print(f"SSH backup error for job {backup_job_id}: {ex}")
        finally:
            _db.close()

    background_tasks.add_task(_run_dump)
    return {"success": True, "message": "Backup started via SSH in background", "job_id": backup_job_id}


@app.delete("/api/backups/{backup_id}", dependencies=[Depends(verify_credentials)])
def delete_backup(backup_id: int, db: Session = Depends(get_db)):
    from models import BackupJob
    job = db.query(BackupJob).filter(BackupJob.id == backup_id).first()
    if not job:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(job)
    db.commit()
    return {"success": True}

@app.delete("/api/backups/schedules/{sched_id}", dependencies=[Depends(verify_credentials)])
def delete_schedule(sched_id: int, db: Session = Depends(get_db)):
    from models import BackupSchedule
    s = db.query(BackupSchedule).filter(BackupSchedule.id == sched_id).first()
    if not s:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    db.delete(s)
    db.commit()
    return {"success": True}


# ── Deploy a Cluster ──────────────────────────────────────────────────────────

@app.post("/api/deploy/validate-ssh", dependencies=[Depends(verify_credentials)])
def deploy_validate_ssh(body: dict = Body(...)):
    """
    Test SSH connectivity to a host before committing to deployment.
    Accepts password auth or PEM private key (detected automatically).
    Returns {ok, hostname, os} on success or {ok: false, error} on failure.
    """
    import paramiko, io, socket
    host     = body.get("host", "").strip()
    port     = int(body.get("port", 22))
    username = body.get("username", "root").strip()
    cred     = body.get("credential", "").strip()   # PEM key text or password

    if not host or not username:
        return JSONResponse(status_code=400, content={"ok": False, "error": "Host ve kullanıcı adı zorunludur"})

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if cred and "-----BEGIN" in cred:
            # PEM key — try RSA, Ed25519, ECDSA in order
            pkey = None
            for KeyClass in [paramiko.RSAKey, paramiko.Ed25519Key, paramiko.ECDSAKey]:
                try:
                    pkey = KeyClass.from_private_key(io.StringIO(cred))
                    break
                except Exception:
                    continue
            if pkey is None:
                return JSONResponse(content={"ok": False, "error": "Geçersiz PEM anahtarı"})
            client.connect(hostname=host, port=port, username=username, pkey=pkey, timeout=10)
        elif cred:
            client.connect(hostname=host, port=port, username=username, password=cred, timeout=10)
        else:
            # Try passwordless key-based auth
            client.connect(hostname=host, port=port, username=username, timeout=10)

        # Gather basic host info
        _, stdout, _ = client.exec_command("hostname && cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"' || echo 'Unknown OS'")
        lines = stdout.read().decode("utf-8", errors="ignore").strip().splitlines()
        hostname_str = lines[0] if lines else host
        os_str       = lines[1] if len(lines) > 1 else "Unknown OS"
        client.close()
        return {"ok": True, "hostname": hostname_str, "os": os_str}

    except socket.timeout:
        return JSONResponse(content={"ok": False, "error": f"Bağlantı zaman aşımı: {host}:{port}"})
    except paramiko.AuthenticationException:
        return JSONResponse(content={"ok": False, "error": "Kimlik doğrulama başarısız — kullanıcı adı/şifre/anahtar hatalı"})
    except paramiko.SSHException as e:
        return JSONResponse(content={"ok": False, "error": f"SSH hatası: {str(e)}"})
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)})


@app.post("/api/deploy/start", dependencies=[Depends(verify_credentials)])
def deploy_start(background_tasks: BackgroundTasks, body: dict = Body(...), db: Session = Depends(get_db)):
    """
    Save wizard data and create the cluster record.
    Creates: Project + DatabaseNode rows + DeployJob.
    The actual remote installation is deferred (status = PENDING).
    """
    from models import DeployJob
    from vault import encrypt

    db_type      = body.get("db_type", "postgresql")
    cluster_name = body.get("cluster_name", "").strip()
    if not cluster_name:
        import random, string
        cluster_name = db_type.upper() + "-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    ssh_cred_raw = body.get("ssh_credential", "")
    db_pass_raw  = body.get("db_admin_pass", "")
    nodes_list   = body.get("nodes", [])   # [{"role": "primary"|"replica", "ip": "..."}]

    # Create Project
    proj = Project(
        name=cluster_name,
        description=f"{db_type.upper()} cluster deployed via wizard"
    )
    db.add(proj)
    db.flush()  # get proj.id

    # Create DatabaseNode rows for each node
    db_port_default = 5432 if db_type == "postgresql" else 1433
    db_port = int(body.get("db_port", db_port_default))
    root_conn_url = body.get("connection_url", "").strip()

    for node_entry in nodes_list:
        ip = node_entry.get("ip", "").strip()
        role = node_entry.get("role", "replica")
        raw_url = node_entry.get("url", "").strip()
        if not ip and not raw_url:
            continue

        if raw_url:
            conn_url = raw_url
        elif root_conn_url and role == "primary":
            conn_url = root_conn_url
        else:
            db_pass = body.get('db_admin_pass', '')
            user_auth = f"{body.get('db_admin_user','postgres')}:{db_pass}" if db_pass else f"{body.get('db_admin_user','postgres')}"
            conn_url = f"postgresql://{user_auth}@{ip}:{db_port}/{cluster_name}" \
                       if db_type == "postgresql" \
                       else f"mssql+pyodbc://{user_auth}@{ip}:{db_port}/{cluster_name}"

        node = DatabaseNode(
            project_id=proj.id,
            role=role,
            name=f"{ip or 'Node'}",
            ssh_host=ip if ip else None,
            ssh_port=int(body.get("ssh_port", 22)),
            ssh_username=body.get("ssh_user", "root"),
            encrypted_ssh_credential=encrypt(ssh_cred_raw) if ssh_cred_raw else None,
        )
        node.set_url(conn_url)
        db.add(node)

    # Create DeployJob record
    job = DeployJob(
        project_id      = proj.id,
        db_type         = db_type,
        cluster_name    = cluster_name,
        status          = "PENDING",
        step            = "wizard_complete",
        ssh_host        = (nodes_list[0].get("ip") if nodes_list else None),
        ssh_port        = int(body.get("ssh_port", 22)),
        ssh_user        = body.get("ssh_user", "root"),
        encrypted_ssh_cred = encrypt(ssh_cred_raw) if ssh_cred_raw else None,
        sudo_method     = body.get("sudo_method", "sudo"),
        disable_fw      = bool(body.get("disable_fw", True)),
        disable_selinux = bool(body.get("disable_selinux", True)),
        install_software= bool(body.get("install_software", True)),
        db_version      = body.get("db_version", ""),
        db_port         = db_port,
        db_admin_user   = body.get("db_admin_user", ""),
        encrypted_db_pass = encrypt(db_pass_raw) if db_pass_raw else None,
        db_data_dir     = body.get("db_data_dir", ""),
        nodes_json      = str(nodes_list),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(run_deploy_job, job.id)
    return {"success": True, "job_id": job.id, "project_id": proj.id, "cluster_name": cluster_name}


@app.get("/api/deploy/{job_id}", dependencies=[Depends(verify_credentials)])
def deploy_get_job(job_id: int, db: Session = Depends(get_db)):
    """Return the current status of a deploy job."""
    from models import DeployJob
    job = db.query(DeployJob).filter(DeployJob.id == job_id).first()
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job bulunamadı"})
    return {
        "id": job.id, "project_id": job.project_id,
        "db_type": job.db_type, "cluster_name": job.cluster_name,
        "status": job.status, "step": job.step, "error_msg": job.error_msg,
        "log_output": job.log_output or "",
        "created_at": str(job.created_at), "updated_at": str(job.updated_at),
    }


@app.get("/api/deploy", dependencies=[Depends(verify_credentials)])
def deploy_list(db: Session = Depends(get_db)):
    """List all deploy jobs (most recent first)."""
    from models import DeployJob
    jobs = db.query(DeployJob).order_by(DeployJob.created_at.desc()).limit(50).all()
    return [
        {
            "id": j.id, "project_id": j.project_id,
            "db_type": j.db_type, "cluster_name": j.cluster_name,
            "status": j.status, "step": j.step,
            "created_at": str(j.created_at),
        }
        for j in jobs
    ]
