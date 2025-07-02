# backend/conftest.py
import os
import pytest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Project imports
from app.db.base_class import Base
from app.db.session import get_db, engine, engine_test, SessionLocalTest
from app.main import app as fastapi_app
from app.models.tenant import Tenant
# Import models to register their tables in Base.metadata
from app.models.gdpr_action import GdprAction
from app.models.processing_action import processing_actions

# ──────────────────────────────────────────────
#  PostgreSQL base – created once per test run
# ──────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """Create / drop all PostgreSQL tables for the integration test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ──────────────────────────────────────────────
#  In‑memory SQLite – fast unit tests layer
# ──────────────────────────────────────────────
@pytest.fixture(scope="module")
def setup_test_db():
    """Create the whole schema in the ephemeral SQLite DB then clean it up."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """Provide a SQLite session bound to a SAVEPOINT and roll it back afterwards."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = SessionLocalTest(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Return a FastAPI TestClient wired to the in‑memory SQLite session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as c:
        yield c

    fastapi_app.dependency_overrides.clear()


# ──────────────────────────────────────────────
#  Helper – auth headers (public routes for now)
# ──────────────────────────────────────────────
@pytest.fixture
def auth_headers():
    return {}


# ──────────────────────────────────────────────
#  Tenant factory for tests
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def tenant(db_session):
    """Create a dummy Tenant in the test database and return it."""
    t = Tenant(name="Tenant-test")
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)
    return t
