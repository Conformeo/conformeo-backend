# backend/tests/test_users_delete.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_password_hash
from app.models.user import User


def create_user(client, db_session, email, password, is_admin=False):
    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed, is_active=True, is_admin=is_admin)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_token_for(client, email, password):
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_admin_can_delete_user(client, db_session):
    # Préparer un admin et un utilisateur à supprimer
    admin = create_user(client, db_session, "admin@ex.com", "adminpass", is_admin=True)
    target = create_user(
        client, db_session, "victim@ex.com", "userpass", is_admin=False
    )

    token = get_token_for(client, admin.email, "adminpass")
    response = client.delete(
        f"/users/{target.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Vérifier que l'utilisateur n'existe plus
    resp = client.get(
        f"/users/{target.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 404


def test_non_admin_cannot_delete(client, db_session):
    user1 = create_user(client, db_session, "u1@ex.com", "pass1", is_admin=False)
    user2 = create_user(client, db_session, "u2@ex.com", "pass2", is_admin=False)

    token = get_token_for(client, user1.email, "pass1")
    response = client.delete(
        f"/users/{user2.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_cannot_delete_self_even_admin(client, db_session):
    admin = create_user(client, db_session, "admin2@ex.com", "adminpass", is_admin=True)
    token = get_token_for(client, admin.email, "adminpass")
    response = client.delete(
        f"/users/{admin.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
