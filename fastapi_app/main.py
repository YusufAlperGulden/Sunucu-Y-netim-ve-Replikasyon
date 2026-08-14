from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import SessionLocal, Project, DatabaseNode
from pydantic import BaseModel
from ha_manager import test_connection, setup_replication, check_and_protect_wal_bloat
import traceback
import asyncio
from contextlib import asynccontextmanager

# Arka plan gÃ¶revi: Her 30 saniyede bir WAL Lag'i kontrol eder
async def wal_bloat_monitor():
    while True:
        await asyncio.sleep(30)
        db = SessionLocal()
        try:
            projects = db.query(Project).all()
            for proj in projects:
                primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
                if primary:
                    res = await check_and_protect_wal_bloat(primary.encrypted_url, proj.max_wal_lag_mb)
                    if res['dropped']:
                        print(f"[ALERT] Project {proj.name} - Slot DROPPED! {res['message']}")
                    elif res['lag_mb'] > 0:
                        print(f"[MONITOR] Project {proj.name} - {res['message']}")
        except Exception as e:
            print(f"Monitor error: {e}")
        finally:
            db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    monitor_task = asyncio.create_task(wal_bloat_monitor())
    yield
    # Shutdown
    monitor_task.cancel()

app = FastAPI(title="Sunucu YÃ¶netim ve Replikasyon", lifespan=lifespan)

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

@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{"id": p.id, "name": p.name, "description": p.description, "nodesCount": len(p.nodes)} for p in projects]

@app.post("/api/projects")
def add_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_proj = Project(name=project.name, description=project.description)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return {"success": True, "id": db_proj.id}

@app.put("/api/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    proj.name = project.name
    proj.description = project.description
    db.commit()
    return {"success": True}

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    db.delete(proj)
    db.commit()
    return {"success": True}

@app.get("/api/projects/{project_id}")
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    
    nodes = [{"id": n.id, "role": n.role, "name": n.name} for n in proj.nodes]
    return {"id": proj.id, "name": proj.name, "description": proj.description, "nodes": nodes}

@app.post("/api/projects/{project_id}/nodes")
async def add_node(project_id: int, node: NodeCreate, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    
    # 1. PING (Test Connection)
    is_alive = await test_connection(node.url)
    if not is_alive:
        return JSONResponse(status_code=400, content={"success": False, "message": "Connection test failed. Sunucuya ulaÅŸÄ±lamÄ±yor veya URL hatalÄ±."})
    
    # 2. SAVE (Vault Encryption)
    db_node = DatabaseNode(project_id=proj.id, role=node.role, name=node.name)
    db_node.set_url(node.url) # AES-256 encrypts the url
    db.add(db_node)
    db.commit()
    
    return {"success": True, "message": "Node added securely."}

@app.post("/api/projects/{project_id}/sync")
async def sync_replication(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={"message": "Project not found"})
    
    primary = next((n for n in proj.nodes if n.role.lower() == 'primary'), None)
    standby = next((n for n in proj.nodes if n.role.lower() == 'standby'), None)
    
    if not primary or not standby:
        return JSONResponse(status_code=400, content={"success": False, "message": "Projenizde senkronizasyon iÃ§in en az 1 Primary ve 1 Standby node bulunmalÄ±dÄ±r."})
    
    # 3. Setup Logical Replication
    result = await setup_replication(primary.encrypted_url, standby.encrypted_url)
    if not result['success']:
        return JSONResponse(status_code=500, content=result)
        
    return result

@app.get('/api/audit-logs')
def get_audit_logs(db: Session = Depends(get_db)):
    from models import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [{'id': l.id, 'project_id': l.project_id, 'timestamp': l.timestamp.isoformat(), 'action': l.action, 'details': l.details} for l in logs]

class SettingsUpdate(BaseModel):
    max_wal_lag_mb: int

@app.post('/api/settings/{project_id}')
def update_settings(project_id: int, settings: SettingsUpdate, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
    proj.max_wal_lag_mb = settings.max_wal_lag_mb
    db.commit()
    return {'success': True}

@app.get('/api/projects/{project_id}/metrics')
async def get_project_metrics(project_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    import asyncio
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        return JSONResponse(status_code=404, content={'message': 'Project not found'})
    
    # Concurrently fetch metrics from all servers
    tasks = []
    for node in proj.nodes:
        tasks.append(get_server_metrics(node.encrypted_url))
        
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

@app.get('/api/nodes/{node_id}/url')
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

@app.put('/api/nodes/{node_id}')
async def update_node_url(node_id: int, update: NodeUpdate, db: Session = Depends(get_db)):
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
    
    is_alive = await test_connection(update.url)
    if not is_alive:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'Connection test failed. Sunucuya ulaşılamıyor.'})
    
    node.set_url(update.url)
    db.commit()
    return {'success': True, 'message': 'Node updated securely.'}

@app.get('/api/nodes/{node_id}/metrics')
async def get_single_node_metrics(node_id: int, db: Session = Depends(get_db)):
    from ha_manager import get_server_metrics
    node = db.query(DatabaseNode).filter(DatabaseNode.id == node_id).first()
    if not node:
        return JSONResponse(status_code=404, content={'message': 'Node not found'})
    
    metrics = await get_server_metrics(node.encrypted_url)
    return metrics
