"""
Initialisation du layer d’accès BD.
Exporte :

- `Base`          : la classe de base SQLAlchemy pour les modèles.
- `engine`        : l’Engine partagé.
- `SessionLocal`  : factory de sessions.
- `get_db()`      : dépendance FastAPI pour fournir/fermer une session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# ❶ ——————————————————————
DATABASE_URL = "sqlite:///./dev.db"  # <- adapte (env var, psql, etc.)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# ❷ ——————————————————————
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ❸ ——————————————————————
def get_db():
    """
    Dépendance FastAPI : ouvre une session, la ferme après la requête.
    Usage : `db: Session = Depends(get_db)`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
