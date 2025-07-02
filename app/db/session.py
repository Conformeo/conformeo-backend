# backend/app/db/session.py
"""Session & engines
- `engine`         : connexion PostgreSQL (prod/dev)
- `engine_test`    : SQLite in-memory (tests unitaires, pool StaticPool)
- `get_db`         : dépendance FastAPI → SessionLocal (PostgreSQL)
- `SessionLocalTest`: session factory pour SQLite
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool                 # ← NEW

from app.core.config import Settings
from app.db.base_class import Base                     # Base unique

settings = Settings()

# ──────────────────────────────
#  PostgreSQL – env. dev / prod
# ──────────────────────────────
engine = create_engine(
    str(settings.DATABASE_URL),   # AnyUrl → str
    future=True,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ──────────────────────────────
#  SQLite in-memory – tests
#   (une seule connexion partagée)
# ──────────────────────────────
engine_test = create_engine(
    "sqlite://",                                  # URI vide ⇒ in-memory
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,                         # ← connexion unique
    future=True,
)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# ──────────────────────────────
#  Dépendance FastAPI
# ──────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = [
    "engine",
    "SessionLocal",
    "engine_test",
    "SessionLocalTest",
    "get_db",
]
