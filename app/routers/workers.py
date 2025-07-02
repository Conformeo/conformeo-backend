from fastapi import APIRouter
from typing import List
from app.models.worker import Worker

router = APIRouter(prefix="/workers", tags=["workers"])

# Simule la “base” temporaire pour le MVP (à remplacer par ta vraie DB)
workers_db: List[Worker] = [
    Worker(id="1", nom="Macron", prenom="Emmanuel", poste="Président", telephone="0283948213", email="emmanuel@elysee.fr", siteId="1751017705531", equipe="Equipe Alpha"),
    Worker(id="2", nom="Macron", prenom="Brigitte", poste="Inutile", telephone="0987654P9087", email=None, siteId=None, equipe="Equipe Bravo"),
]

@router.get("/", response_model=List[Worker])
def list_workers():
    return workers_db

@router.post("/", response_model=Worker)
def add_worker(worker: Worker):
    workers_db.append(worker)
    return worker
