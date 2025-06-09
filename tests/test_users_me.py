from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import get_password_hash


def get_auth_headers(client, email, password):
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_read_users_me_success(client, db_session):
    # 1. Crée un tenant
    tenant = Tenant(name="test-tenant")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    # 2. Crée un user lié à ce tenant
    hashed = get_password_hash("mypassword")
    user = User(
        email="me@example.com",
        hashed_password=hashed,
        is_active=True,
        is_admin=False,
        tenant_id=tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 3. Authentifie et vérifie l'accès à /users/me
    headers = get_auth_headers(client, "me@example.com", "mypassword")
    resp = client.get("/users/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "me@example.com"
