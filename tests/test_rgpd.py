from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_audit():
    response = client.get("/api/rgpd/audits/1")
    assert response.status_code in (200, 404)  # selon si audit existe

def test_create_audit():
    payload = {"user_id": 1, "company_id": 1}
    response = client.post("/api/rgpd/audits", json=payload)
    assert response.status_code == 200
