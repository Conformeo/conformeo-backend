# backend/tests/test_users_update.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

# 1. Crée un tenant pour associer le user (sinon tenant_id NOT NULL)
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash


hashed = get_password_hash("mon_mdp")


def create_user_and_token(client, db_session, email, password, is_admin=False):

    # 1. Cherche le tenant, ou crée-le si besoin
    tenant = db_session.query(Tenant).filter_by(name="test-tenant").first()
    if not tenant:
        tenant = Tenant(name="test-tenant")
        db_session.add(tenant)
        db_session.commit()
        db_session.refresh(tenant)

    # 2. Crée le user lié au tenant
    hashed = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed,
        is_active=True,
        is_admin=is_admin,  # <==== Ici !
        tenant_id=tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 3. Auth (login) pour obtenir le token
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]

    return user, token


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
