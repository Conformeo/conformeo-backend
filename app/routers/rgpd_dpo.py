# app/routers/rgpd_dpo.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.rgpd_dpo import Dpo
from app.schemas.rgpd_dpo import DpoRead, DpoCreate, DpoUpdate
from app.db.session import get_db

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

@router.get("/dpo/{user_id}", response_model=DpoRead)
def get_dpo(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère le DPO d'un utilisateur.
    - 404 si aucun DPO désigné.
    """
    dpo = db.query(Dpo).filter_by(user_id=user_id).first()
    if not dpo:
        raise HTTPException(status_code=404, detail="DPO non désigné")
    return dpo

@router.post("/dpo", response_model=DpoRead, status_code=status.HTTP_201_CREATED)
def create_dpo(dpo_in: DpoCreate, db: Session = Depends(get_db)):
    """
    Crée un DPO pour un utilisateur donné.
    - 400 si un DPO existe déjà.
    """
    exist = db.query(Dpo).filter_by(user_id=dpo_in.user_id).first()
    if exist:
        raise HTTPException(status_code=400, detail="Un DPO existe déjà pour cet utilisateur")
    dpo = Dpo(**dpo_in.dict())
    db.add(dpo)
    db.commit()
    db.refresh(dpo)
    return dpo

@router.put("/dpo/{user_id}", response_model=DpoRead)
def update_dpo(user_id: int, dpo_in: DpoUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations du DPO d'un utilisateur.
    - 404 si DPO non trouvé.
    """
    dpo = db.query(Dpo).filter_by(user_id=user_id).first()
    if not dpo:
        raise HTTPException(status_code=404, detail="DPO non désigné")
    # On n'écrase que les champs fournis
    for k, v in dpo_in.dict(exclude_unset=True).items():
        setattr(dpo, k, v)
    db.commit()
    db.refresh(dpo)
    return dpo

@router.delete("/dpo/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dpo(user_id: int, db: Session = Depends(get_db)):
    """
    Supprime le DPO d'un utilisateur.
    - 404 si DPO non trouvé.
    """
    dpo = db.query(Dpo).filter_by(user_id=user_id).first()
    if not dpo:
        raise HTTPException(status_code=404, detail="DPO non désigné")
    db.delete(dpo)
    db.commit()
    # Explicitement aucun retour
    return None
