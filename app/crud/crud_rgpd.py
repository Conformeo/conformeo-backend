from sqlalchemy.orm import Session
from app.models.rgpd_audit import RgpdAudit
from app.models.rgpd_exigence import RgpdExigence
from app.models.rgpd_audit_exigence import RgpdAuditExigence

def get_audit_by_id(db: Session, audit_id: int):
    return db.query(RgpdAudit).filter(RgpdAudit.id == audit_id).first()

def list_audits(db: Session, user_id: int):
    return db.query(RgpdAudit).filter(RgpdAudit.user_id == user_id).all()

def create_audit(db: Session, audit: dict):
    db_audit = RgpdAudit(**audit)
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit
# … autres CRUD selon besoin
