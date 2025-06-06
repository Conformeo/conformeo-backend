# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import du router health
from app.routers.health import router as health_router
from app.core.config import settings  # <-- Import des settings


app = FastAPI(
    title="Mon App MVP",
    description="API FastAPI - Sprint 1: structure initiale et endpoint /health",
    version="0.1.0"
)

# Exemple d’utilisation : afficher dans la console la DATABASE_URL lors du démarrage
print(f"[CONFIG] DATABASE_URL = {settings.DATABASE_URL}")
print(f"[CONFIG] ACCESS_TOKEN_EXPIRE_MINUTES = {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")


# --- Configuration CORS (exemple minimal) ---
origins = [
    "http://localhost",
    "http://localhost:4200",
    # si besoin, ajouter d’autres domaines de dev ou staging :
    # "http://127.0.0.1:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # origines autorisées
    allow_credentials=True,       # autoriser l’envoi de cookies / credentials
    allow_methods=["*"],          # autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],          # autoriser tous les headers
)

# --- Endpoint racine (facultatif, mais pratique pour tester) ---
@app.get("/")
def root():
    return {"message": "Hello FastAPI - Backend Initialisé"}

# --- Inclusion du router de santé ---
app.include_router(health_router, prefix="/health", tags=["health"])
