# backend/app/routers/health.py

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Statut de santé de l'API")
def ping():
    """
    Endpoint de santé :
    - Renvoie {"status": "OK"} si l'API est opérationnelle.
    """
    return {"status": "OK"}
