# app/crud/crud_duerp.py
from sqlalchemy.orm import Session
from app.models.duerp import DuerpEvaluation
from app.schemas.duerp import DuerpEvaluationCreate



def create_evaluation(db: Session, evaluation: DuerpEvaluationCreate):
    db_obj = DuerpEvaluation(**evaluation.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_synthese(db, user_id):
    return {"nb_risques": 10, "sites": 2, "plans_action": 1}

def get_evaluations(db: Session, skip=0, limit=20):
    return db.query(DuerpEvaluation).offset(skip).limit(limit).all()

def create_evaluation(db, user_id, eval_in):
    return {}

def get_timeline(db, user_id):
    return []

def get_risques_types(db, user_id):
    return [{"type": "Chute", "nb": 4}]
