# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import du router health
from app.routers.health import router as health_router

app = FastAPI(
    title="Mon App MVP",
    description="API FastAPI - Sprint 1: structure initiale et endpoint /health",
    version="0.1.0"
)

# --- Configuration CORS (exemple minimal) ---
origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Origines autorisées en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoint racine (facultatif, mais pratique pour tester) ---
@app.get("/")
def root():
    return {"message": "Hello FastAPI - Backend Initialisé"}

# --- Inclusion du router de santé ---
app.include_router(health_router, prefix="/health", tags=["health"])
