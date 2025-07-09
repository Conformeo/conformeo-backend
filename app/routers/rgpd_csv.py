import csv
from io import StringIO
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.gdpr_action_answer import GdprActionAnswer
from app.services.rgpd_scoring import compute_rgpd_score

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

@router.get("/audit/{audit_id}/export", response_class=Response)
def export_csv(audit_id: int, db: Session = Depends(get_db)):
    answers = db.query(GdprActionAnswer).filter(GdprActionAnswer.user_id == audit_id).all()
    report_data = compute_rgpd_score(db, answers)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Exigence", "Réponse", "Critique", "Conseil", "Commentaire"])
    for detail in report_data["details"]:
        writer.writerow([
            detail["action_id"],
            detail["label"],
            detail["answer"],
            "Oui" if detail["critical"] else "Non",
            detail.get("advice", ""),
            detail.get("comment", "")
        ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=rgpd_export_{audit_id}.csv"}
    )
