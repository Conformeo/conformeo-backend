from sqlalchemy.orm import Session
from app.models.rgpd_audit import RgpdAudit
from app.models.rgpd_exigence import RgpdExigence
from app.models.rgpd_audit_exigence import RgpdAuditExigence
from app.schemas.rgpd_audit import RgpdAuditCreate

def create_audit(db: Session, audit_in: RgpdAuditCreate) -> RgpdAudit:
    db_audit = RgpdAudit(**audit_in.dict())
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit

def get_audit_history(db: Session, user_id: int):
    return db.query(RgpdAudit).filter(RgpdAudit.user_id == user_id).order_by(RgpdAudit.created_at.desc()).all()
