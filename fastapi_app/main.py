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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials", headers={"WWW-Authenticate": "Bearer"})
    return credentials

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup complete.")
        
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
    return [{"id": p.id, "name": p.name, "description": p.description, "nodesCount": len(p.nodes), "nodes": [{"id": n.id, "name": n.name, "role": n.role} for n in p.nodes]} for p in projects]

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
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.isoformat() if l.timestamp else None, 'action': l.action, 'details': l.details} for l in logs]

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
            'id': node['id'],
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
