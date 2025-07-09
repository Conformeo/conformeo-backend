# Module Sécurité (backend)

- `models/securite.py` : modèle SQLAlchemy SecuriteControle
- `schemas/securite.py` : schémas Pydantic
- `crud/crud_securite.py` : CRUD/services
- `routers/securite.py` : endpoints API
    - `/securite/summary`
    - `/securite/` (GET/POST)

À brancher dans `main.py` :
```python
from app.routers.securite import router as securite_router
app.include_router(securite_router, prefix="/api")

# Module Sécurité — Modèle multi-entité

Chaque contrôle de sécurité est rattaché à :
- un utilisateur (user_id)
- un site (site_id)
- une société/tenant (societe_id)

## Relations à ajouter sur User/Site/Tenant

# app/models/user.py
securite_controles = relationship("SecuriteControle", back_populates="user", cascade="all, delete-orphan")
# app/models/site.py
securite_controles = relationship("SecuriteControle", back_populates="site", cascade="all, delete-orphan")
# app/models/tenant.py
securite_controles = relationship("SecuriteControle", back_populates="societe", cascade="all, delete-orphan")

## Ajoute dans main.py :
from app.routers.securite import router as securite_router
app.include_router(securite_router, prefix="/api")


securite_controles
  id (PK)
  user_id (FK > users.id)
  site_id (FK > sites.id)
  societe_id (FK > tenants.id)
  type
  date_controle
  nb_nc
  rapport
