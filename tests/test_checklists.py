import pytest
from app.models.tenant import Tenant
from app.models.user import User
from app.models.checklist import Checklist
from app.core.security import get_password_hash


# Réutilise tes helpers pour login/token, par ex :
def create_user_and_token(client, db_session, email, password, is_admin=False):
    # 1. Crée un tenant unique à chaque test (évite les collisions)
    tenant = Tenant(name=f"tenant_{email}")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_admin=is_admin,
        tenant_id=tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Auth via login endpoint → récupère le token JWT
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return user, tenant, token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_checklist(client, db_session):
    user, tenant, token = create_user_and_token(
        client, db_session, "chk@a.com", "passpass"
    )
    data = {
        "name": "Sécurité chantier",
        "description": "Checklist sécurité BTP",
        "tenant_id": tenant.id,
    }
    resp = client.post("/checklists/", json=data, headers=auth_headers(token))
    assert resp.status_code == 201, resp.json()
    assert resp.json()["name"] == "Sécurité chantier"
    assert resp.json()["tenant_id"] == tenant.id


def test_list_checklists(client, db_session):
    user, tenant, token = create_user_and_token(
        client, db_session, "chk@b.com", "passpass"
    )
    # Ajout direct DB (rapide, pas d’API)
    c1 = Checklist(name="Checklist 1", tenant_id=tenant.id)
    c2 = Checklist(name="Checklist 2", tenant_id=tenant.id)
    db_session.add_all([c1, c2])
    db_session.commit()
    resp = client.get("/checklists/", headers=auth_headers(token))
    assert resp.status_code == 200
    names = [x["name"] for x in resp.json()]
    assert "Checklist 1" in names and "Checklist 2" in names


def test_update_checklist(client, db_session):
    user, tenant, token = create_user_and_token(
        client, db_session, "chk@c.com", "passpass"
    )
    checklist = Checklist(name="Initial", tenant_id=tenant.id)
    db_session.add(checklist)
    db_session.commit()
    db_session.refresh(checklist)

    data = {"name": "Modifié", "description": "Nouvelle desc"}
    resp = client.put(
        f"/checklists/{checklist.id}", json=data, headers=auth_headers(token)
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Modifié"
    assert resp.json()["description"] == "Nouvelle desc"


def test_delete_checklist(client, db_session):
    user, tenant, token = create_user_and_token(
        client, db_session, "chk@d.com", "passpass"
    )
    checklist = Checklist(name="ASUP", tenant_id=tenant.id)
    db_session.add(checklist)
    db_session.commit()
    db_session.refresh(checklist)

    resp = client.delete(f"/checklists/{checklist.id}", headers=auth_headers(token))
    assert resp.status_code == 204
    # Vérifie la suppression
    c = db_session.query(Checklist).filter_by(id=checklist.id).first()
    assert c is None
