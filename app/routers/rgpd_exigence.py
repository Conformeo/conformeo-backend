from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.rgpd_exigence import RgpdExigenceCreate, RgpdExigenceRead
from app.crud import crud_rgpd_exigence

router = APIRouter(prefix="/rgpd", tags=["rgpd"])

# === Liste toutes les exigences ===
@router.get("/exigences", response_model=List[RgpdExigenceRead])
def list_exigences(db: Session = Depends(get_db)):
    exigences = crud_rgpd_exigence.get_all(db)
    return [RgpdExigenceRead.from_orm(e) for e in exigences]

# === Détail d'une exigence ===
@router.get("/exigences/{exigence_id}", response_model=RgpdExigenceRead)
def get_exigence(exigence_id: int, db: Session = Depends(get_db)):
    exigence = crud_rgpd_exigence.get(db, exigence_id)
    if not exigence:
        raise HTTPException(404, detail="Exigence non trouvée")
    return RgpdExigenceRead.from_orm(exigence)

# === Création d'une exigence ===
@router.post("/exigences", response_model=RgpdExigenceRead, status_code=201)
def create_exigence(exigence_in: RgpdExigenceCreate, db: Session = Depends(get_db)):
    exigence = crud_rgpd_exigence.create(db, exigence_in)
    return RgpdExigenceRead.from_orm(exigence)

# === Mise à jour d'une exigence ===
@router.put("/exigences/{exigence_id}", response_model=RgpdExigenceRead)
def update_exigence(exigence_id: int, exigence_in: RgpdExigenceCreate, db: Session = Depends(get_db)):
    exigence = crud_rgpd_exigence.update(db, exigence_id, exigence_in)
    if not exigence:
        raise HTTPException(404, detail="Exigence non trouvée")
    return RgpdExigenceRead.from_orm(exigence)

# === Suppression d'une exigence ===
@router.delete("/exigences/{exigence_id}", status_code=204)
def delete_exigence(exigence_id: int, db: Session = Depends(get_db)):
    ok = crud_rgpd_exigence.delete(db, exigence_id)
    if not ok:
        raise HTTPException(404, detail="Exigence non trouvée")
    return None  # 204 No Content = pas de retour
