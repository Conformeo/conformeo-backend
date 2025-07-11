# app/routers/rgpd_procedure.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.dpo import DPORead, DPOCreate
from app.schemas.rgpd_obligation import RgpdObligationRead
from app.crud import crud_dpo, crud_rgpd_obligation
from app.db.session import get_db

router = APIRouter(prefix="/rgpd/procedure", tags=["RGPD"])

@router.get("/dpo", response_model=DPORead)
def get_dpo(user_id: int, db: Session = Depends(get_db)):
    dpo = crud_dpo.get_dpo_by_user(db, user_id)
    if not dpo:
        raise HTTPException(404, "DPO non trouvé")
    return dpo

@router.post("/dpo", response_model=DPORead)
def set_dpo(user_id: int, dpo: DPOCreate, db: Session = Depends(get_db)):
    return crud_dpo.create_or_update_dpo(db, user_id, dpo)

@router.get("/obligations", response_model=list[RgpdObligationRead])
def get_obligations(user_id: int, db: Session = Depends(get_db)):
    return crud_rgpd_obligation.get_obligations_by_user(db, user_id)
