# backend/tests/test_db.py

import pytest
from sqlalchemy import inspect
from app.db.session import engine


@pytest.fixture(scope="module")
def connection():
    # On se connecte directement à la base configurée via DATABASE_URL
    conn = engine.connect()
    yield conn
    conn.close()


def test_users_table_exists(connection):
    inspector = inspect(connection)
    tables = inspector.get_table_names()
    assert "users" in tables
