# 🚀 Onboarding Développeur – Backend Conforméo (FastAPI/PostgreSQL)

Bienvenue sur l’API Conforméo !

## 📦 Arborescence projet

# Conforméo – Backend

Ce backend utilise FastAPI, SQLAlchemy et Pydantic pour gérer la logique métier, la base de données et l'API REST.

## Arborescence
- `models/` : Modèles SQLAlchemy (DB)
- `schemas/` : Schémas Pydantic (entrée/sortie)
- `crud/` : Accès DB (CRUD)
- `routers/` : Routes FastAPI
- `services/` : Logique métier, scoring, PDF, etc.
- `tests/` : Tests unitaires
- `main.py` : Point d'entrée FastAPI

## Ajouter un module (exemple RGPD)
1. Crée le modèle (models/...)
2. Crée le schéma (schemas/...)
3. Crée les fonctions CRUD (crud/...)
4. Crée le router (routers/...)
5. Ajoute le router dans `main.py`
6. Ajoute des tests dans `tests/`


app/
core/ – config, middlewares, settings globaux
db/ – connexion BDD, models SQLAlchemy, base_class, session
crud/ – accès/modification données (repository + seed)
dependencies/ – dépendances FastAPI (auth, etc.)
models/ – models SQLAlchemy (1 fichier par entité métier)
routers/ – endpoints API (regroupés par module métier)
schemas/ – schémas Pydantic (requêtes/réponses, validation)
services/ – logique métier, intégration externe
uploads/ – fichiers importés (si besoin)
main.py – point d’entrée FastAPI


---

## ⚡ Premiers pas

- [ ] Python 3.10+ & [Poetry](https://python-poetry.org/) ou pip/venv
- [ ] Installer dépendances  
  `poetry install` **ou** `pip install -r requirements.txt`
- [ ] Configurer `.env` (copier `.env.example` et adapter BDD)
- [ ] Démarrer :  
  `uvicorn app.main:app --reload`
- [ ] Accéder à la doc OpenAPI : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Routine dev

- Modèles et schémas :  
  `app/models/`, `app/schemas/`
- Endpoints API :  
  `app/routers/`
- CRUD logique :  
  `app/crud/`
- Services spécialisés :  
  `app/services/`
- Tests unitaires (si activés) :  
  `tests/` (structure à compléter)

---

## 🏗️ Ajout d’une nouvelle entité/module

1. **Model** :  
   `app/models/monmodule.py`
2. **Schema** (Pydantic) :  
   `app/schemas/monmodule.py`
3. **CRUD** (méthodes de base + logiques avancées) :  
   `app/crud/crud_monmodule.py`
4. **Router** (endpoints API) :  
   `app/routers/monmodule.py`
5. **Service** (optionnel, logique complexe ou intégration externe) :  
   `app/services/monmodule_service.py`
6. **Mise à jour `main.py` pour ajouter le router**
7. **(Optionnel)** : seed/fixtures dans `crud/` ou script de migration

---

## 🗺️ Routing API

- Endpoints regroupés par “module métier” (ex: `/api/rgpd`, `/api/checklists`)
- Tous les routers importés dans `main.py`
- OpenAPI doc générée automatiquement

---

## ✅ Routines du quotidien

- Toujours lancer :  
  `uvicorn app.main:app --reload`
- **Format** : Black, isort (`black .`, `isort .`)
- **Tests** : pytest (`pytest tests/`)
- **Migration BDD** : alembic ou autres (si besoin)
- Toujours documenter tout nouveau endpoint dans le doc de la feature

---

## 📚 Onboarding rapide

- Lire ce README
- Lancer l’API en local
- Voir la doc auto (`/docs`)
- Regarder le README du module sur lequel tu bosses (ex : `app/routers/rgpd.py` → voir `app/features/rgpd/README.md`)
- Pour chaque nouvelle fonctionnalité, crée :
  - models, schemas, crud, routers, services, tests

---

## 🔗 Liens utiles

- [FastAPI doc](https://fastapi.tiangolo.com/)
- [SQLAlchemy doc](https://docs.sqlalchemy.org/)
- [Pydantic doc](https://docs.pydantic.dev/)


# ✅ Onboarding Backend FastAPI

- [ ] Cloner le repo, aller dans `/backend`
- [ ] Copier `.env.example` en `.env` et configurer la BDD
- [ ] Installer les deps (`poetry install` ou `pip install -r requirements.txt`)
- [ ] Lancer FastAPI (`uvicorn app.main:app --reload`)
- [ ] Créer un module : models + schemas + crud + routers (+ services si besoin)
- [ ] Tester endpoints dans `/docs`
- [ ] Commit, PR, mise à jour du README de la feature



# Conseils & routines backend

- 1 module métier = models + schemas + crud + routers (+ services)
- Factorise les dépendances globales dans /core et /dependencies
- Privilégie la clarté des schémas et l’auto-doc de l’API
- Toute nouvelle table → migration (alembic)
- Un README par dossier feature
- Gardez le code “stateless” : tout passe par la BDD, aucune variable globale non contrôlée

