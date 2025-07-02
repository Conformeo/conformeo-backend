from app.models.processing import Processing

def test_create_and_list_processing(client, db_session, auth_headers, tenant):
    # Création
    dto = {
        "name": "Gestion RH",
        "purpose": "Paie",
        "legal_basis": "contrat",
        "data_subjects": ["Salariés"],
        "data_categories": ["Nom", "IBAN"],
        "tenant_id": tenant.id,
    }
    r = client.post("/rgpd/processings/", json=dto, headers=auth_headers)
    assert r.status_code == 201
    proc_id = r.json()["id"]

    # Liste
    r2 = client.get("/rgpd/processings/", headers=auth_headers)
    assert r2.status_code == 200
    assert any(p["id"] == proc_id for p in r2.json())
