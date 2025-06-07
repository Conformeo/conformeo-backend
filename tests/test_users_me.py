import pytest
from app.core.security import get_password_hash
from app.models.user import User

def test_read_users_me_success(client, db_session):
    # 1) Créer un user actif via db_session (SQLite in-memory)
    hashed = get_password_hash("mypassword")
    user = User(email="me@example.com", hashed_password=hashed, is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 2) Récupérer un token via l’endpoint /auth/login (utilise la fixture client)
    response = client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "mypassword"}
    )
    assert response.status_code == 200, f"Login a renvoyé {response.status_code}"
    token = response.json()["access_token"]

    # 3) Appeler GET /users/me avec le token obtenu
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"/users/me a renvoyé {response.status_code}"
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["is_active"] is True
    assert "id" in data
