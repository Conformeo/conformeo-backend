# backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Création de l'engine : il se connecte à PostgreSQL via la variable d'environnement DATABASE_URL
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=True,  # Affiche les requêtes SQL générées (utile en dev)
    future=True  # Active le style "2.0" si tu utilises SQLAlchemy >=1.4
)

# SessionLocal sera utilisée pour obtenir un objet Session par requête
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base est la classe mère pour tous les modèles déclaratifs
Base = declarative_base()

# Dépendance FastAPI : on pourra l’importer dans les routers pour obtenir une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
