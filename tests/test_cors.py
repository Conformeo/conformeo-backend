# backend/tests/test_cors.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cors_allowed_origin():
    response = client.options(
        "/health/",  # on peut envoyer un OPTIONS pour tester CORS pré-vol
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Le status_code 200 signifie qu'on répond bien au pré-vol
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:4200"
    )


def test_cors_disallowed_origin():
    response = client.options(
        "/health/",
        headers={
            "Origin": "http://exemple.invalid",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Il n'y a pas d'en-tête access-control-allow-origin pour un domaine non autorisé
    assert response.headers.get("access-control-allow-origin") is None
