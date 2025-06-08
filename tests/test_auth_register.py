# backend/tests/test_auth_register.py

import pytest


def test_register_user_success(client):
    """
    Teste qu'un POST /auth/register avec un nouvel email fonctionne bien.
    """
    response = client.post(
        "/auth/register",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True
    assert "id" in data


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
