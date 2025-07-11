from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Routers importés
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.tenants import router as tenants_router
from app.routers.checklists import router as checklist_router
from app.routers.checklist_items import router as items_router
from app.routers.extinguishers import router as extinguishers_router
from app.routers.camera import router as camera_router
from app.routers.kits import router as kits_router
# from app.routers.certification import router as certification_router
from app.routers.certif import router as certif_router
from app.routers.insurance import router as insurance_router
from app.routers.sites import router as sites_router
from app.routers.workers import router as workers_router
from app.routers.duerp import router as duerp_router
from app.routers.securite import router as securite_router
from app.routers.obligation import router as obligation_router
from app.routers.rgpd_export import router as rgpd_export_router


# RGPD Routers – NOUVEAU (utilise tes nouveaux fichiers)
from app.routers.rgpd import router as rgpd_router      # ← Ton endpoint principal RGPD (audit, exigences, réponses, etc.)
# (si besoin, adapte ici selon le nom de ton router principal)
# from app.routers.rgpd_exigences import router as rgpd_exigences_router
# from app.routers.rgpd_audit import router as rgpd_audit_router
# from app.routers.rgpd_audit_exigence import router as rgpd_audit_exigence_router

from app.routers import documents
from app.core.config import Settings

# ─── App & Config ───────────────────────────────────────────────────────────────
settings = Settings()

app = FastAPI(
    title="Conforméo",
    description="API FastAPI – Sprint 1",
    version="0.1.0",
)

# Fichiers statiques (photos, docs…)
app.mount("/static", StaticFiles(directory="app/uploads"), name="static")

# Limite de taille d’upload (10 Mo)
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    max_body_size = 10 * 1024 * 1024  # 10 Mo
    if request.headers.get("content-length") and int(request.headers["content-length"]) > max_body_size:
        return Response("Fichier trop gros", status_code=413)
    return await call_next(request)

# CORS pour le front Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello FastAPI – Backend initialisé"}

# Préfixe commun à toutes les routes d’API
API_PREFIX = "/api"

# Ensemble de tous les routers à exposer sous /api
_API_ROUTERS = [
    documents.router,
    sites_router,
    workers_router,
    rgpd_router,
    rgpd_export_router,                 # Nouveau router RGPD principal !
    duerp_router,
    items_router,
    securite_router,
    checklist_router,
    extinguishers_router,
    obligation_router,
    # certification_router,
    certif_router,
    insurance_router,
    camera_router,
    kits_router,
]

_API_ROUTERS.extend([auth_router, users_router, tenants_router])

for rtr in _API_ROUTERS:
    app.include_router(rtr, prefix=API_PREFIX)

# Routes racine (hors préfixe /api, pour certains cas)
_ROOT_ROUTERS = [
    health_router,
    auth_router,
    users_router,
    tenants_router,
    checklist_router,
    items_router,
    extinguishers_router,
    certif_router,
    # certification_router,
    camera_router,
    kits_router,
    insurance_router,
]

for rtr in _ROOT_ROUTERS:
    app.include_router(rtr)

# --------  Debugging routes
# @app.on_event("startup")
# async def _debug_routes() -> None:
#     print("\n─── Routes déclarées ───")
#     for r in app.router.routes:
#         if hasattr(r, "methods"):
#             methods = ",".join(r.methods or [])
#             path = getattr(r, "path", getattr(r, "path_format", ""))
#             print(f"{path:40s}  [{methods}]")
#         else:
#             print(f"{getattr(r, 'path', r.name):40s}  [MOUNT]")
#     print("────────────────────────\n")
