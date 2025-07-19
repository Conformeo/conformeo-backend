from sqlalchemy.orm import Session
from app.models.rgpd_audit import RgpdAudit
from app.models.rgpd_exigence import RgpdExigence
from app.models.rgpd_audit_exigence import RgpdAuditExigence

def get_audit_by_id(db: Session, audit_id: int):
    return db.query(RgpdAudit).filter(RgpdAudit.id == audit_id).first()

def list_audits(db: Session, user_id: int):
    return db.query(RgpdAudit).filter(RgpdAudit.user_id == user_id).all()

def create_audit(db: Session, audit: dict):
    """audit['exigences'] est une liste de dict provenant du front"""
    children = []
    for item in audit.pop("exigences", []):
        children.append(
            RgpdAuditExigence(
                exigence_id=item["exigence_id"],
                answer=item["answer"],
                comment=item.get("comment", ""),
                proof=item.get("proof", "")
            )
        )

    db_audit = RgpdAudit(**audit)
    db_audit.exigences.extend(children)

    db.add(db_audit)
    db.flush()        # pour obtenir l’ID si besoin
    db.commit()
    db.refresh(db_audit)
    return db_audit

