# DUERP – Module Backend

## Arborescence

- `models/duerp.py` – Table SQLAlchemy des DUERP
- `schemas/duerp.py` – Schémas Pydantic in/out
- `crud/crud_duerp.py` – Accès CRUD aux DUERP
- `routers/duerp.py` – Endpoints API (list, create…)
- `services/duerp_service.py` – Logique métier avancée (statuts, etc.)

## Endpoints principaux

- `GET /api/duerp/` : liste des DUERP
- `POST /api/duerp/` : création d’un nouveau DUERP

## Bonnes pratiques

- Toujours utiliser les schémas Pydantic pour la validation
- Factoriser la logique business dans `services/`
- Écrire les tests au fur et à mesure dans `/tests`

## Extension

- Ajouter scoring/exports, relances automatiques, liens avec d’autres modules (ex : audits sécurité)
