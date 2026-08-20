"""
ops_center_worker.py -- ClusterControl Ops-Center Multi-Controller Management Worker
"""
import json
import requests
import datetime
from models import SessionLocal, OpsController, AddonSetting
from vault import encrypt, decrypt


def get_ops_center_config(db) -> dict:
    """Retrieves Ops-Center configuration from AddonSetting."""
    setting = db.query(AddonSetting).filter(AddonSetting.addon_key == "ops_center").first()
    if not setting or not setting.extra_json:
        return {"enabled": False, "root_user": None}
    try:
        data = json.loads(setting.extra_json)
        return {
            "enabled": bool(setting.enabled),
            "root_user": data.get("root_username"),
            "email": data.get("email"),
            "updated_at": str(setting.updated_at)
        }
    except Exception:
        return {"enabled": bool(setting.enabled), "root_user": None}


def ping_controller(url: str, api_token: str = None) -> dict:
    """Sends a health check ping to an external ClusterControl / Manager controller."""
    clean_url = url.rstrip('/')
    target_url = f"{clean_url}/api/users/me" if "/api" not in clean_url else clean_url
    
    headers = {"User-Agent": "ClusterControl-OpsCenter/2.5.0"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    try:
        resp = requests.get(target_url, headers=headers, timeout=5, verify=False)
        return {
            "online": resp.status_code in [200, 401], # 401 means server is up and responsive to auth
            "status_code": resp.status_code,
            "latency_ms": int(resp.elapsed.total_seconds() * 1000)
        }
    except Exception as e:
        return {"online": False, "error": str(e), "latency_ms": 0}


def sync_all_controllers(db) -> list:
    """Refreshes status and cluster counts for all registered controllers."""
    controllers = db.query(OpsController).all()
    results = []
    for c in controllers:
        token = decrypt(c.encrypted_api_token) if c.encrypted_api_token else None
        res = ping_controller(c.url, token)
        c.status = 'ONLINE' if res.get('online') else 'OFFLINE'
        c.updated_at = datetime.datetime.utcnow()
        db.commit()
        results.append({
            "id": c.id,
            "name": c.name,
            "url": c.url,
            "status": c.status,
            "is_primary": c.is_primary,
            "version": c.version,
            "cluster_count": c.cluster_count,
            "latency_ms": res.get("latency_ms", 0)
        })
    return results
