# app/routers/rgpd_audit.py
from fastapi import APIRouter, Depends, Response, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.rgpd_audit import RgpdAudit
from app.models.gdpr_action_answer import GdprActionAnswer
from app.services.rgpd_scoring import compute_rgpd_score
from app.services.rgpd_pdf import build_rgpd_pdf
from app.schemas.rgpd_audit import AuditSummary, AuditList
from app.services.notification import send_alert_email

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

@router.get("/audits/{user_id}", response_model=AuditList)
def get_audit_history(user_id: int, db: Session = Depends(get_db)):
    audits = db.query(RgpdAudit).filter(RgpdAudit.user_id == user_id).order_by(RgpdAudit.created_at.desc()).all()
    return {"audits": [AuditSummary(**a.__dict__) for a in audits]}

@router.get("/audit/{audit_id}/score", summary="Score complet d'un audit RGPD")
def get_rgpd_audit_score(audit_id: int, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    answers = db.query(GdprActionAnswer).filter(GdprActionAnswer.audit_id == audit_id).all()
    result = compute_rgpd_score(db, answers)
    # MAJ score dans audit
    audit = db.query(RgpdAudit).get(audit_id)
    if audit:
        audit.score = result["score"]
        db.commit()
    # Notification auto si KO critique
    if result["critical_ko"]:
        # Mettre l’email du user à récupérer dans l’audit ou le user associé
        background_tasks.add_task(send_alert_email, "email@conformeo.fr", result)
    return result

@router.get("/audit/{audit_id}/rapport", response_class=Response)
def download_rgpd_pdf(audit_id: int, db: Session = Depends(get_db)):
    answers = db.query(GdprActionAnswer).filter(GdprActionAnswer.audit_id == audit_id).all()
    report_data = compute_rgpd_score(db, answers)
    pdf_bytes = build_rgpd_pdf(report_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename=rapport_rgpd_{audit_id}.pdf"})


@app.get("audits/last")
def get_last_audit(user_id: int, db: Session = Depends(get_db)):
    audit = db.query(RgpdAudit).filter_by(user_id=user_id).order_by(RgpdAudit.created_at.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Aucun audit trouvé")
    return {
        "id": audit.id,
        "score": audit.score,
        "conforme": audit.nb_conforme,
        "non_conforme": audit.nb_non_conforme,
        "critical_ko": audit.critical_ko,  # list des exigences critiques non conformes
        # ...
    }


@app.get("/audits")
def get_audit_timeline(user_id: int, db: Session = Depends(get_db)):
    audits = db.query(RgpdAudit).filter_by(user_id=user_id).order_by(RgpdAudit.created_at.asc()).all()
    return [
        {"created_at": a.created_at, "score": a.score}
        for a in audits
    ]

@app.get("/audits/{audit_id}/domains")
def get_domain_stats(audit_id: int, db: Session = Depends(get_db)):
    # Retourne la répartition des exigences par “domaine” pour le camembert/barres
    # Ex : [{name: "Base légale", value: 2}, ...]
    ...
