import json, time

audit_sample = {
    "application": "ClusterControl Web UI",
    "exportDate": "2026-08-19T15:14:00.000Z",
    "totalEvents": 4,
    "events": [
        {"id": 1, "time": "2026-08-19T15:14:01.120Z", "route": "#settings-view", "eventType": "AUDIT_SESSION_STARTED", "details": {"userAgent": "Mozilla/5.0 Chrome/120.0"}},
        {"id": 2, "time": "2026-08-19T15:14:05.450Z", "route": "#settings-view", "eventType": "CLICK", "details": {"tagName": "BUTTON", "id": "btn-save-project-settings", "innerText": "Save Settings"}},
        {"id": 3, "time": "2026-08-19T15:14:06.100Z", "route": "#settings-view", "eventType": "API_RESPONSE", "details": {"endpoint": "/api/projects/2", "status": 200}},
        {"id": 4, "time": "2026-08-19T15:14:10.000Z", "route": "#settings-view", "eventType": "AUDIT_SESSION_STOPPED", "details": {}}
    ]
}

print("=== GENERATED AUDIT JSON FORMAT TEST ===")
print(json.dumps(audit_sample, indent=2))
