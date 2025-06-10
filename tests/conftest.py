from typing import Tuple  # pour le type de retour
from starlette.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.models.tenant import Tenant
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # ← override pour pytest


def create_user_and_token(
    client: TestClient,
    db_session: Session,
    email: str,
    password: str,
    *,
    is_admin: bool = False,
) -> Tuple[User, Tenant, str]:
    tenant = Tenant(name="test-tenant")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    user = User(
        email=email,
        hashed_password=get_password_hash(password),  # ← utilise la fonction importée
        is_active=True,
        is_admin=is_admin,
        tenant_id=tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return user, tenant, token


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
