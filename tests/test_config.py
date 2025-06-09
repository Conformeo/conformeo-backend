# backend/tests/test_config.py

import os
import pytest
from app.core.config import Settings


def test_settings_load(tmp_path, monkeypatch):
    # Supprime toute env var héritée du runner CI
    os.environ.pop("DATABASE_URL", None)

    # Crée un .env temporaire
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DATABASE_URL=postgresql://localhost:5432/db_test\n"
        "SECRET_KEY=testsecret\n"
        "ACCESS_TOKEN_EXPIRE_MINUTES=120\n"
        "FEATURE_X_ENABLED=True\n"
        "LOG_LEVEL=debug"
    )

    # Patch le CWD et la variable d'env
    monkeypatch.chdir(tmp_path)
    os.environ["DATABASE_URL"] = "postgresql://localhost:5432/db_test"

    settings = Settings()
    assert settings.DATABASE_URL is not None
