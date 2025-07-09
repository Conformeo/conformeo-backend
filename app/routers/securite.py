from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.securite import SecuriteControleCreate, SecuriteControleRead
from app.crud import crud_securite
from app.db.session import get_db

router = APIRouter(prefix="/securite", tags=["Sécurité"])

@router.get("/", response_model=List[SecuriteControleRead])
def list_controles(user_id: int = Query(None), site_id: int = Query(None), societe_id: int = Query(None), db: Session = Depends(get_db)):
    """Lister tous les contrôles par user, site, ou société"""
    if user_id:
        return crud_securite.get_controles_by_user(db, user_id)
    if site_id:
        return crud_securite.get_controles_by_site(db, site_id)
    if societe_id:
        return crud_securite.get_controles_by_societe(db, societe_id)
    return []

@router.post("/", response_model=SecuriteControleRead)
def add_controle(controle_in: SecuriteControleCreate, db: Session = Depends(get_db)):
    """Ajouter un contrôle"""
    return crud_securite.create_controle(db, controle_in)

@router.get("/summary")
def summary(user_id: int = Query(...)):
    # Ex : retourne des stats fictives pour la démo
    return {"nb_alertes": 3, "nb_visites": 5}

@router.get("/nonconformites")
def nonconformites(user_id: int = Query(...)):
    # Ex : retourne une liste fictive
    return [{"id": 1, "label": "Porte coupe-feu bloquée"}]

@router.get("/timeline")
def timeline(user_id: int = Query(...)):
    # Ex : retourne un historique fictif
    return [
        {"date": "2024-07-01", "alertes": 2},
        {"date": "2024-07-02", "alertes": 3},
    ]