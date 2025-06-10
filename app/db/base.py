from app.db.session import Base  # <- c'est là que tu déclares Base = declarative_base()
from app.models.user import User
from app.models.tenant import Tenant
from app.models.checklist import Checklist


# Base = declarative_base()

# Forcer l'import des modèles ici (sinon Alembic ne les voit PAS !)
