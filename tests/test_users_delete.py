import pytest
from app.models.user import User as UserModel
from app.core.security import get_password_hash


def create_user(db_session, email, password, is_admin=False, tenant_id=1):
    user = UserModel(
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
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_delete_user(client, db_session):
    tenant_id = 1
    admin = create_user(
        db_session, "admin@del.com", "adminpass", is_admin=True, tenant_id=tenant_id
    )
    user = create_user(
        db_session, "todelete@del.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )

    headers = get_auth_headers(client, admin.email, "adminpass")
    # On delete
    resp = client.delete(f"/users/{user.id}", headers=headers)
    assert resp.status_code == 204

    # Vérifie que le user est bien supprimé
    assert db_session.query(UserModel).filter_by(id=user.id).first() is None


def test_non_admin_cannot_delete_user(client, db_session):
    tenant_id = 1
    user = create_user(
        db_session, "user@del.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )
    user2 = create_user(
        db_session, "other@del.com", "pass12345", is_admin=False, tenant_id=tenant_id
    )
    headers = get_auth_headers(client, user.email, "pass12345")
    resp = client.delete(f"/users/{user2.id}", headers=headers)
    assert resp.status_code == 403
