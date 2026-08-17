from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from models import SessionLocal, Project, DatabaseNode
from pydantic import BaseModel
from ha_manager import test_connection, setup_replication, check_and_protect_wal_bloat, cleanup_node_replication, cleanup_project_replication
import traceback
import asyncio
import secrets
from contextlib import asynccontextmanager

security = HTTPBasic(auto_error=False)

import os
import secrets

ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS = os.environ.get("ADMIN_PASS")

if not ADMIN_USER or not ADMIN_PASS:
    raise RuntimeError("CRITICAL: ADMIN_USER or ADMIN_PASS environment variables are missing.")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return credentials

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "alembic.ini"))
        # Run migrations on startup to prevent 500 errors if user forgets to run them
        command.upgrade(alembic_cfg, "head")
        print("Alembic migrations ran successfully.")
    except Exception as e:
        print(f"Migration error: {e}")
        # Uygulamanın başlatılmasını durdurmak (fail-closed)
        raise RuntimeError(f"Database migration check failed: {e}")
        
    yield
    # Shutdown

app = FastAPI(title="Sunucu Yönetim ve Replikasyon", lifespan=lifespan)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

class ProjectCreate(BaseModel):
    name: str
    description: str

class NodeCreate(BaseModel):
    role: str
    name: str
    url: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/projects", dependencies=[Depends(verify_credentials)])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{"id": p.id, "name": p.name, "description": p.description, "nodesCount": len(p.nodes)} for p in projects]

@app.post("/api/projects", dependencies=[Depends(verify_credentials)])
def add_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_proj = Project(name=project.name, description=project.description)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    
    from models import AuditLog
    audit = AuditLog(project_id=db_proj.id, action="Project Created", details=f"Name: {project.name}")
    db.add(audit)
    db.commit()
    return {"success": True, "id": db_proj.id}

@app.put("/api/projects/{project_id}", dependencies=[Depends(verify_credentials)])
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    proj.name = project.name
    proj.description = project.description
    db.commit()
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

    nodes = [{"id": n.id, "role": n.role, "name": n.name} for n in proj.nodes]
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
async def add_node(project_id: int, node: NodeCreate, db: Session = Depends(get_db)):
    if node.role.lower() not in ['primary', 'standby']:
        return JSONResponse(status_code=400, content={"success": False, "message": "Geçersiz rol. Sadece Primary veya Standby eklenebilir."})

    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
        
    if node.role.lower() == 'primary':
        existing_primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
        if existing_primary:
            return JSONResponse(status_code=400, content={"success": False, "message": "Bir projede sadece 1 adet Primary (Ana) sunucu bulunabilir."})
    
    from vault import decrypt
    for n in db.query(DatabaseNode).all():
        if decrypt(n.encrypted_url) == node.url:
            return JSONResponse(status_code=400, content={"success": False, "message": "Bu sunucu bağlantı URL'si zaten başka bir projede veya rolde kayıtlı. Sistem güvenliği için aynı veritabanı birden fazla node olarak eklenemez."})

    # 1. PING (Test Connection)
    is_alive = await test_connection(node.url)
    if not is_alive:
        return JSONResponse(status_code=400, content={"success": False, "message": "Connection test failed. Sunucuya ulaşılamıyor veya URL hatalı."})
    
    # 2. SAVE (Vault Encryption)
    db_node = DatabaseNode(project_id=proj.id, role=node.role, name=node.name)
    db_node.set_url(node.url) # AES-256 encrypts the url
    db.add(db_node)
    
    from models import AuditLog
    audit = AuditLog(project_id=proj.id, action="Node Added", details=f"Role: {node.role}, Name: {node.name}")
    db.add(audit)
    db.commit()
    
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
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.isoformat(), 'action': l.action, 'details': l.details} for l in logs]

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
        tasks.append(get_server_metrics(node.encrypted_url, project_id=proj.id, role=node.role, metric_table=proj.metric_table))
        
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
    db.commit()
    return {'success': True, 'message': 'Node updated securely.'}

@app.get('/api/nodes/{node_id}/metrics', dependencies=[Depends(verify_credentials)])
async def get_single_node_metrics(node_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
    
    metrics = await get_server_metrics(
        node.encrypted_url,
        project_id=node.project_id,
        role=node.role,
        metric_table=node.project.metric_table if node.project else None
    )
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
