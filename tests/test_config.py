# backend/tests/test_config.py

import os
import pytest
from app.core.config import Settings


def test_settings_load(tmp_path, monkeypatch):
    """
    Vérifie que Settings lit correctement les variables d'environnement depuis un fichier .env.
    """
    import os

    # 0. Supprime toute env var héritée du runner CI
    os.environ.pop("DATABASE_URL", None)

    # 1. Créer un fichier .env temporaire
    env_file = tmp_path / ".env"
    env_content = "\n".join(
        [
            "DATABASE_URL=***localhost:5432/db_test",
            "SECRET_KEY=testsecret",
            "ACCESS_TOKEN_EXPIRE_MINUTES=120",
            "FEATURE_X_ENABLED=True",
            "LOG_LEVEL=debug",
        ]
    )
    env_file.write_text(env_content)

    # 2. Forcer Pydantic à utiliser ce dossier temporaire comme CWD
    monkeypatch.chdir(tmp_path)

    # 3. Instancier Settings : il doit lire le .env que l'on vient de créer
    settings = Settings()

    # 4. Assertions (on compare str() pour DATABASE_URL)
    assert str(settings.DATABASE_URL) == "***localhost:5432/db_test"

