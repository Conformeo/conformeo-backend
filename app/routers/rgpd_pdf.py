from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.gdpr_action_answer import GdprActionAnswer
from app.services.rgpd_scoring import compute_rgpd_score
from app.services.rgpd_pdf import build_rgpd_pdf

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

@router.get("/audit/{audit_id}/rapport", response_class=Response)
def download_rgpd_pdf(audit_id: int, db: Session = Depends(get_db)):
    answers = db.query(GdprActionAnswer).filter(GdprActionAnswer.user_id == audit_id).all()
    report_data = compute_rgpd_score(db, answers)
    pdf_bytes = build_rgpd_pdf(report_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename=rapport_rgpd_{audit_id}.pdf"})
