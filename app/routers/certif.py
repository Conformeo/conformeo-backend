from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.certif import CertifCreate, CertifRead
from app.crud import crud_certif
from app.api.deps import get_db

router = APIRouter(prefix="/certif", tags=["Certifications"])

@router.get("/summary", response_model=dict)
def summary(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Synthèse des certifications pour un utilisateur (nombre total, à renouveler…)
    """
    return crud_certif.get_certif_stats(db, user_id)

@router.get("/", response_model=List[CertifRead])
def list_certifs(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Liste complète des certifications pour un utilisateur.
    """
    return crud_certif.get_certifs_by_user(db, user_id)

@router.post("/", response_model=CertifRead)
def create_certif(
    user_id: int = Query(...),
    certif_in: CertifCreate = ...,
    db: Session = Depends(get_db)
):
    """
    Création d’une nouvelle certification.
    """
    return crud_certif.create_certif(db, user_id, certif_in)


@router.get("/expiring", response_model=List[CertifRead])
def expiring_certifs(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud_certif.get_certifs_expiring(db, user_id)
