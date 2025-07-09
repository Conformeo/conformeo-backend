# Module Certifications (backend)

- `models/certif.py` : modèle SQLAlchemy Certification
- `schemas/certif.py` : schémas Pydantic (lecture, création)
- `crud/crud_certif.py` : fonctions de base CRUD + stats
- `routers/certif.py` : endpoints API
    - `/certif/summary` : stats synthèse
    - `/certif/` : liste
    - `/certif/` (POST) : ajout

À brancher dans `main.py` :
```python
from app.routers.certif import router as certif_router
app.include_router(certif_router, prefix="/api")
