# backend/app/main.py

from fastapi import FastAPI, Request, Response  # <--- AJOUT ICI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.tenants import router as tenants_router
from app.routers.checklists import router as checklist_router
from app.routers.checklist_items import router as items_router
from app.routers.extinguishers import router as extinguishers
from app.routers.camera import router as camera_router
from app.routers.kits import router as kits_router
from app.routers.certification import router as certification_router
from app.routers.insurance import router as insurance_router
from app.routers import documents
from app.core.config import Settings
from fastapi.staticfiles import StaticFiles
from app.routers.sites import router as sites_router 

settings = Settings()

app = FastAPI(
    title="Conformeo", description="API FastAPI - Sprint 1…", version="0.1.0"
)
app.mount("/static", StaticFiles(directory="app/uploads", html=True), name="static")
# app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Middleware d'upload max size (juste ici)
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    max_body_size = 10 * 1024 * 1024  # Limite à 10 Mo
    if request.headers.get("content-length") and int(request.headers["content-length"]) > max_body_size:
        return Response("Fichier trop gros", status_code=413)
    return await call_next(request)

origins = ["http://localhost", "http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello FastAPI - Backend Initialisé"}


# Inclusion des routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tenants_router)
app.include_router(users_router)
app.include_router(checklist_router)
app.include_router(items_router)
app.include_router(extinguishers)
app.include_router(camera_router)
app.include_router(kits_router)
app.include_router(certification_router)
app.include_router(insurance_router)
app.include_router(documents.router)
app.include_router(sites_router, prefix="/api")
