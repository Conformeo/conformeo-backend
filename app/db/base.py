from sqlalchemy.orm import declarative_base
from app.models.tenant import Tenant
from app.models.user import User

Base = declarative_base()

# Forcer l'import des modèles ici (sinon Alembic ne les voit PAS !)
