# backend/tests/test_users_update.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserUpdate


def create_user_and_token(client, db_session, email, password, is_admin=False):
    # Créer directement le user en base
    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed, is_active=True, is_admin=is_admin)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # Récupérer le token
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    return user, response.json()["access_token"]


def test_user_can_update_own_profile(client, db_session):
    user, token = create_user_and_token(
        client, db_session, "u1@example.com", "secret123"
    )
    response = client.put(
        f"/users/{user.id}",
        json={"email": "nouvel@example.com", "password": "newsecret123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "nouvel@example.com"


def test_user_cannot_update_other_profile(client, db_session):
    u1, token1 = create_user_and_token(
        client, db_session, "u1@example.com", "secret123"
    )
    u2, _ = create_user_and_token(client, db_session, "u2@example.com", "secret123")
    response = client.put(
        f"/users/{u2.id}",
        json={"email": "hack@example.com"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response.status_code == 403


def test_admin_can_update_any_profile(client, db_session):
    admin, token_admin = create_user_and_token(
        client, db_session, "admin@example.com", "adminpass", is_admin=True
    )
    u, _ = create_user_and_token(client, db_session, "u@example.com", "userpass")
    response = client.put(
        f"/users/{u.id}",
        json={"email": "adminmodif@example.com"},
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "adminmodif@example.com"
