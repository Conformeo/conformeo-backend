# tests/test_actions_catalog.py
"""
Vérifie que le catalogue d’actions RGPD est bien exposé et non-vide.
"""

import pytest


def test_list_actions(client):
    """
    - L’endpoint `/api/rgpd/actions/` doit répondre 200.
    - Le JSON retourné doit être une liste contenant au moins 5 actions
      (les seeds créés au démarrage).
    """
    response = client.get("/api/rgpd/actions/")
    assert response.status_code == 200, response.text

    data = response.json()
    assert isinstance(data, list), "La réponse doit être une liste"
    assert len(data) >= 5, "Le catalogue devrait contenir ≥ 5 actions"

    # Sanity-check rapide sur la structure des items
    sample = data[0]
    for field in ("id", "label", "scope"):
        assert field in sample, f"Champ manquant : {field}"
