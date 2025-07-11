from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.rgpd import GdprActionRead
from app.schemas.rgpd_audit import RgpdAuditRead, RgpdAuditCreate
from app.schemas.dpo import DpoRead, DpoCreate

from app.crud import crud_rgpd
from app.db.session import get_db

from app.models.rgpd_audit import RgpdAudit
from app.models.dpo import Dpo

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

# --- Détail d'un audit
@router.get("/audits/{audit_id}", response_model=RgpdAuditRead)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = crud_rgpd.get_audit_by_id(db, audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

# --- Création d'un audit
@router.post("/audits", response_model=RgpdAuditRead)
def create_audit(audit: RgpdAuditCreate, db: Session = Depends(get_db)):
    return crud_rgpd.create_audit(db, audit.model_dump())

# --- Dernier audit RGPD pour un user_id (user_id en query param)
@router.get("/audits/last")
def get_last_audit(user_id: int = Query(...), db: Session = Depends(get_db)):
    audit = db.query(RgpdAudit).filter_by(user_id=user_id).order_by(RgpdAudit.created_at.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Aucun audit trouvé")
    return {
        "id": audit.id,
        "score": audit.score,
        "conforme": audit.nb_conforme,
        "non_conforme": audit.nb_non_conforme,
        "critical_ko": audit.critical_ko,
    }

# --- Timeline des audits pour un user_id
@router.get("/audits", response_model=List[RgpdAuditRead])
def get_audit_timeline(
    user_id: int = Query(..., description="ID utilisateur"),
    db: Session = Depends(get_db)
):
    audits = db.query(RgpdAudit).filter_by(user_id=user_id).order_by(RgpdAudit.created_at.asc()).all()
    return audits or []

# --- Répartition des exigences par domaine pour un audit donné
@router.get("/audits/{audit_id}/domains")
def get_domain_stats(audit_id: int, db: Session = Depends(get_db)):
    # À compléter selon ta logique d’audit
    # Ex : [{"name": "Base légale", "value": 2}, ...]
    return []

# --- Liste actions RGPD (optionnel)
@router.get("/actions/", response_model=List[GdprActionRead])
def list_actions(db: Session = Depends(get_db)):
    actions = crud_rgpd.get_all(db)
    return actions or []

# --- DPO - lecture
@router.get("/dpo", response_model=DpoRead)
def get_dpo(user_id: int = Query(...), db: Session = Depends(get_db)):
    dpo = db.query(Dpo).filter_by(user_id=user_id).first()
    if not dpo:
        raise HTTPException(404, "DPO non trouvé")
    return dpo

# --- DPO - création ou mise à jour (upsert)
@router.post("/dpo", response_model=DpoRead)
def create_or_update_dpo(dpo: DpoCreate, db: Session = Depends(get_db)):
    dpo_obj = db.query(Dpo).filter_by(user_id=dpo.user_id).first()
    if dpo_obj:
        # Update (patch tous les champs)
        for field, value in dpo.dict().items():
            setattr(dpo_obj, field, value)
    else:
        dpo_obj = Dpo(**dpo.dict())
        db.add(dpo_obj)
    db.commit()
    db.refresh(dpo_obj)
    return dpo_obj
