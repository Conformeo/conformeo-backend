# backend/tests/test_health.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Hello FastAPI" in data["message"]
