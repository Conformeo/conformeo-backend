# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.tenants import router as tenants_router


from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title="Mon App MVP", description="API FastAPI - Sprint 1…", version="0.1.0"
)

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
