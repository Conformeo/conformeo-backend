# backend/tests/test_auth_register.py

import pytest


from app.models.tenant import Tenant


def test_register_user_success(client, db_session):
    # Créer un tenant de test (avant le user)
    tenant = Tenant(name="test-tenant")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    # Ajouter le user en lui passant tenant_id=tenant.id si création directe,
    # ou si via l’API, assure-toi que la logique d’API prend le premier tenant.
    response = client.post(
        "/auth/register",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201  # <-- Correction ici
    data = response.json()
    assert data["email"] == "testuser@example.com"
    # Optionnel: vérifie le tenant_id renvoyé


def test_login_user_success(client):
    # Pour pouvoir se connecter, il faut d’abord créer un user "à la main"
    # On peut le faire en appelant directement l’endpoint /auth/register
    client.post(
        "/auth/register", json={"email": "john@example.com", "password": "secretpass"}
    )
    # Puis on teste le login
    response = client.post(
        "/auth/login", data={"username": "john@example.com", "password": "secretpass"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
