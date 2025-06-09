import pytest
from app.models.user import User
from app.core.security import get_password_hash


def create_user(db_session, email, password, is_admin=False, tenant_id=1):
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_admin=is_admin,
        tenant_id=tenant_id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_auth_headers(client, email, password):
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_list_users(client, db_session):
    # Création du tenant fictif (si nécessaire dans ta config)
    tenant_id = 1

    # Création d'un admin et deux users dans le même tenant
    admin = create_user(
        db_session, "admin@org.com", "adminpass", is_admin=True, tenant_id=tenant_id
    )
    _ = create_user(
        db_session, "user1@org.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )
    _ = create_user(
        db_session, "user2@org.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )

    # Authentifie l’admin pour récupérer un token JWT
    headers = get_auth_headers(client, admin.email, "adminpass")

    # Requête GET /users (avec token d’admin)
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    users_list = response.json()
    emails = [u["email"] for u in users_list]

    # L’admin doit voir tous les users de SON tenant
    assert set(emails) == {"admin@org.com", "user1@org.com", "user2@org.com"}


def test_non_admin_cannot_list_users(client, db_session):
    # Création du tenant fictif
    tenant_id = 2

    # Crée un user non-admin
    user = create_user(
        db_session, "user@org2.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )
    headers = get_auth_headers(client, user.email, "pass12345")

    # Tente GET /users (doit renvoyer 403)
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403
