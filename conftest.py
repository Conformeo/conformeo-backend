# backend/conftest.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Importer les objets du projet
from app.db.session import Base, get_db
from app.models.user import User
from app.main import app  # L'instance FastAPI

# 1) On crée un engine "in-memory" pour SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# echo=False pour ne pas spammer la console pendant les tests
engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

# SessionLocalTest :
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# 2) Fixture qui crée la table "users" en mémoire AVANT chaque test de module
#    et détruit la table APRES
@pytest.fixture(scope="module")
def setup_test_db():
    # Crée toutes les tables (User + futures tables) dans la DB SQLite en mémoire
    Base.metadata.create_all(bind=engine_test)
    yield  # Après le yield, le teardown pourra se faire
    Base.metadata.drop_all(bind=engine_test)  # Nettoyage


# 3) Fixture pour obtenir une session SQLAlchemy "test"
@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """
    Cette fixture fournit une session liée à SQLite in-memory,
    et rollback automatiquement à la fin de chaque function-test.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = SessionLocalTest(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# 4) Override de la dépendance get_db pour qu’elle utilise sqlite-test au lieu de PostgreSQL
@pytest.fixture(scope="function")
def client(db_session):
    """
    Cette fixture démarre un TestClient FastAPI dont la dépendance get_db()
    renverra toujours une session SQLite in-memory (via db_session).
    """

    # Fonction qui remplace get_db()
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Pas besoin de fermer ici car db_session fixture s'en charge

    # Remplacement dans FastAPI
    app.dependency_overrides[get_db] = override_get_db

    # On crée un client TestClient pour appeler l’API
    client = TestClient(app)
    yield client

    # Après tous les tests, on peut enlever l’override si besoin
    app.dependency_overrides.clear()
