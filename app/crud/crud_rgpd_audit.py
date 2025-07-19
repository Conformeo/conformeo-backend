from sqlalchemy.orm import Session, joinedload
from app.models.rgpd_audit import RgpdAudit, RgpdAuditExigence
from app.schemas.rgpd_audit import RgpdAuditCreate, RgpdAuditExigenceCreate

# -----------------------------
# AUDIT CRUD
# -----------------------------

def create_audit(
    db: Session,
    audit_in: RgpdAuditCreate,
    exigences_in: list[RgpdAuditExigenceCreate] = None
):
    audit = RgpdAudit(
        user_id=audit_in.user_id,
        company_id=audit_in.company_id,
        statut=audit_in.statut,
    )
    # Ajoute les exigences si fournies (trame CNIL)
    if exigences_in:
        audit.exigences = [
            RgpdAuditExigence(**ex.dict()) for ex in exigences_in
        ]
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit

def get_audit(db: Session, audit_id: int):
    # Charge aussi les exigences avec la relation (joinedload)
    return (
        db.query(RgpdAudit)
        .options(joinedload(RgpdAudit.exigences))
        .filter(RgpdAudit.id == audit_id)
        .first()
    )

def get_audits_by_user(db: Session, user_id: int):
    return (
        db.query(RgpdAudit)
        .options(joinedload(RgpdAudit.exigences))
        .filter(RgpdAudit.user_id == user_id)
        .order_by(RgpdAudit.created_at.desc())
        .all()
    )

def update_audit(db: Session, audit_id: int, data: dict):
    audit = db.query(RgpdAudit).filter(RgpdAudit.id == audit_id).first()
    if not audit:
        return None
    for k, v in data.items():
        setattr(audit, k, v)
    db.commit()
    db.refresh(audit)
    return audit

def delete_audit(db: Session, audit_id: int):
    audit = db.query(RgpdAudit).filter(RgpdAudit.id == audit_id).first()
    if not audit:
        return False
    db.delete(audit)
    db.commit()
    return True

# -----------------------------
# EXIGENCE CRUD
# -----------------------------

def add_exigence(db: Session, audit_id: int, exigence_in: RgpdAuditExigenceCreate):
    exigence = RgpdAuditExigence(**exigence_in.dict(), audit_id=audit_id)
    db.add(exigence)
    db.commit()
    db.refresh(exigence)
    return exigence

def update_exigence(db: Session, exigence_id: int, data: dict):
    exigence = db.query(RgpdAuditExigence).filter(RgpdAuditExigence.id == exigence_id).first()
    if not exigence:
        return None
    for k, v in data.items():
        setattr(exigence, k, v)
    db.commit()
    db.refresh(exigence)
    return exigence

def delete_exigence(db: Session, exigence_id: int):
    exigence = db.query(RgpdAuditExigence).filter(RgpdAuditExigence.id == exigence_id).first()
    if not exigence:
        return False
    db.delete(exigence)
    db.commit()
    return True

# -----------------------------
# BONUS : Générer un audit à partir de la trame CNIL
# -----------------------------

def create_audit_with_cnilexigences(db: Session, user_id: int, company_id: int):
    """
    Crée un audit et pré-remplit avec toutes les exigences (questions) du référentiel CNIL.
    """
    from app.models.rgpd_exigence import RgpdExigence  # À placer en haut si circulaire OK

    exigences = db.query(RgpdExigence).all()
    audit = RgpdAudit(
        user_id=user_id,
        company_id=company_id,
        statut="EN_COURS"
    )
    db.add(audit)
    db.flush()  # Pour obtenir audit.id

    audit_exigences = [
        RgpdAuditExigence(
            audit_id=audit.id,
            exigence_id=exigence.id
        )
        for exigence in exigences
    ]
    db.add_all(audit_exigences)
    db.commit()
    db.refresh(audit)
    return audit
