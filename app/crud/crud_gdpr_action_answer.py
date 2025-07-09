from sqlalchemy.orm import Session
from app.models.gdpr_action_answer import GdprActionAnswer
from app.schemas.gdpr_action_answer import GdprActionAnswerCreate

def create_answer(db: Session, answer_in: GdprActionAnswerCreate) -> GdprActionAnswer:
    answer = GdprActionAnswer(**answer_in.dict())
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer

def get_answers_for_user(db: Session, user_id: int) -> list[GdprActionAnswer]:
    return db.query(GdprActionAnswer).filter(GdprActionAnswer.user_id == user_id).all()

def get_answers_for_audit(db: Session, audit_id: int) -> list[GdprActionAnswer]:
    return db.query(GdprActionAnswer).filter(GdprActionAnswer.audit_id == audit_id).all()
