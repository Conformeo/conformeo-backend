from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.rgpd_audit import RgpdAudit
from app.schemas.rgpd_audit import (
    RgpdAuditRead,
    RgpdAuditCreate,
    RgpdAuditExigenceCreate,
    RgpdAuditExigenceRead
)
from app.crud import crud_rgpd_audit
from app.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/rgpd/audits", tags=["RGPD_AUDITS"])

# -------------------- ROUTES "USER PAR TOKEN" --------------------------

# Dernier audit RGPD de l'utilisateur courant
@router.get("/last", response_model=RgpdAuditRead)
def get_last_audit(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit = db.query(RgpdAudit).filter_by(user_id=current_user.id).order_by(RgpdAudit.created_at.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Aucun audit trouvé")
    return RgpdAuditRead.from_orm(audit)

# Timeline des audits du user courant
@router.get("/timeline", response_model=List[RgpdAuditRead])
def get_audit_timeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audits = db.query(RgpdAudit).filter_by(user_id=current_user.id).order_by(RgpdAudit.created_at.asc()).all()
    return [RgpdAuditRead.from_orm(a) for a in audits]

# Détail d'un audit (par ID, mais vérifie l'utilisateur)
@router.get("/{audit_id}", response_model=RgpdAuditRead)
def get_audit(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit = db.query(RgpdAudit).filter_by(id=audit_id, user_id=current_user.id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    return RgpdAuditRead.from_orm(audit)

# Création d'un audit (user_id forcé côté back)
@router.post("/audits", response_model=RgpdAuditRead, status_code=201)
def create_audit(
    audit_in: RgpdAuditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # titre par défaut et owner forcé
    data = audit_in.model_dump()
    data["titre"] = data.get("titre") or f"Audit {datetime.utcnow():%Y-%m-%d}"
    data["user_id"] = current_user.id
    return crud_rgpd.create_audit(db, data)

# Update d'un audit (idem sécurité)
@router.put("/{audit_id}", response_model=RgpdAuditRead)
def update_audit(
    audit_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit = db.query(RgpdAudit).filter_by(id=audit_id, user_id=current_user.id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    updated = crud_rgpd_audit.update_audit(db, audit_id, data)
    return RgpdAuditRead.from_orm(updated)

# Suppression d'un audit (idem sécurité)
@router.delete("/{audit_id}", status_code=204)
def delete_audit(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit = db.query(RgpdAudit).filter_by(id=audit_id, user_id=current_user.id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    crud_rgpd_audit.delete_audit(db, audit_id)

# -------------------- EXIGENCES D'UN AUDIT --------------------------

@router.post("/{audit_id}/exigences", response_model=RgpdAuditExigenceRead)
def add_exigence(
    audit_id: int,
    exigence_in: RgpdAuditExigenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit = db.query(RgpdAudit).filter_by(id=audit_id, user_id=current_user.id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    exigence = crud_rgpd_audit.add_exigence(db, audit_id, exigence_in)
    return RgpdAuditExigenceRead.from_orm(exigence)

@router.put("/exigences/{exigence_id}", response_model=RgpdAuditExigenceRead)
def update_exigence(
    exigence_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    exigence = crud_rgpd_audit.get_exigence(db, exigence_id)
    if not exigence or exigence.audit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Exigence non trouvée")
    updated = crud_rgpd_audit.update_exigence(db, exigence_id, data)
    return RgpdAuditExigenceRead.from_orm(updated)

@router.delete("/exigences/{exigence_id}", status_code=204)
def delete_exigence(
    exigence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    exigence = crud_rgpd_audit.get_exigence(db, exigence_id)
    if not exigence or exigence.audit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Exigence non trouvée")
    crud_rgpd_audit.delete_exigence(db, exigence_id)
