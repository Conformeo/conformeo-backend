# tests/test_checklist_items.py
import pytest
from starlette.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.checklist import Checklist  # ✅ modèle
from tests.conftest import create_user_and_token, auth_headers  # ✅ helpers


def test_item_crud(client, db_session):
    # create tenant + user + checklist (helpers déjà dispos)
    user, tenant, token = create_user_and_token(client, db_session, "it@x.com", "pass")
    cl = Checklist(name="CL", tenant_id=tenant.id)
    db_session.add(cl)
    db_session.commit()
    db_session.refresh(cl)

    headers = auth_headers(token)

    # create
    r = client.post(
        f"/checklists/{cl.id}/items", json={"label": "Extincteur OK"}, headers=headers
    )
    assert r.status_code == 201
    item_id = r.json()["id"]

    # list
    r = client.get(f"/checklists/{cl.id}/items", headers=headers)
    assert len(r.json()) == 1

    # update
    r = client.put(
        f"/checklists/{cl.id}/items/{item_id}",
        json={"label": "Extincteur vérifié", "is_done": True},
        headers=headers,
    )
    assert r.json()["is_done"] is True

    # delete
    r = client.delete(f"/checklists/{cl.id}/items/{item_id}", headers=headers)
    assert r.status_code == 204
