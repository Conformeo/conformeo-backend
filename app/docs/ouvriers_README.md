# Module Ouvriers (backend)

- `models/ouvrier.py` : modèle SQLAlchemy Ouvrier
- `schemas/ouvrier.py` : schémas Pydantic
- `crud/crud_ouvrier.py` : fonctions CRUD
- `routers/ouvrier.py` : endpoints API
    - `/ouvriers/summary`
    - `/ouvriers/` (GET/POST)

À brancher dans `main.py` :
```python
from app.routers.ouvrier import router as ouvrier_router
app.include_router(ouvrier_router, prefix="/api")
