def test_create_tenant(client):
    response = client.post("/tenants/", json={"name": "Conforméo"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Conforméo"
