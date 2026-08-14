from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Project, DatabaseNode, AuditLog
import vault
import ha_manager
import threading

app = Flask(__name__)
CORS(app) # Allow CORS for frontend

SQLALCHEMY_DATABASE_URL = "sqlite:///./universal_manager.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from flask import render_template

@app.route("/", methods=["GET"])
def read_root():
    return render_template("index.html")

@app.route("/api/projects", methods=["GET"])
def get_projects():
    db = next(get_db())
    projects = db.query(Project).all()
    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "created_at": p.created_at
        })
    return jsonify(result)

@app.route("/api/projects", methods=["POST"])
def create_project():
    data = request.json
    db = next(get_db())
    new_project = Project(name=data.get('name'), description=data.get('description'))
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return jsonify({"id": new_project.id, "name": new_project.name})

@app.route("/api/projects/<int:project_id>/nodes", methods=["POST"])
def add_node(project_id):
    data = request.json
    db = next(get_db())
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    encrypted_url = vault.encrypt(data.get('db_url'))
    new_node = DatabaseNode(
        project_id=project_id,
        name=data.get('name'),
        role=data.get('role', 'PRIMARY'),
        db_url_encrypted=encrypted_url
    )
    db.add(new_node)
    
    log = AuditLog(project_id=project_id, action="ADD_NODE", details=f"Node {new_node.name} added as {new_node.role}.")
    db.add(log)
    
    db.commit()
    return jsonify({"status": "success", "node_id": new_node.id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
