from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.gdpr_action_answer import GdprActionAnswer
from app.services.rgpd_scoring import compute_rgpd_score
from app.schemas.rgpd_score import ScoreResponse

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

@router.get("/audit/{audit_id}/score", response_model=ScoreResponse)
def get_rgpd_audit_score(audit_id: int, db: Session = Depends(get_db)):
    answers = db.query(GdprActionAnswer).filter(GdprActionAnswer.user_id == audit_id).all()
    result = compute_rgpd_score(db, answers)
    return result
