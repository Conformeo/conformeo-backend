from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.duerp import DuerpEvaluationCreate, DuerpEvaluationRead
from app.crud import crud_duerp
from app.db.session import get_db

router = APIRouter(prefix="/duerp", tags=["DUERP"])

# 1. Liste toutes les évaluations DUERP
@router.get("/", response_model=List[DuerpEvaluationRead])
def list_evaluations(db: Session = Depends(get_db)):
    return crud_duerp.get_evaluations(db)

# 2. Ajoute une nouvelle évaluation DUERP
@router.post("/", response_model=DuerpEvaluationRead)
def add_evaluation(evaluation: DuerpEvaluationCreate, db: Session = Depends(get_db)):
    return crud_duerp.create_evaluation(db, evaluation)

# 3. Synthèse DUERP (données globales d'un utilisateur)
@router.get("/synthese")
def duerp_synthese(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud_duerp.get_synthese(db, user_id)

# 4. Timeline des audits DUERP (évolution graphique)
@router.get("/audits")
def duerp_audits(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud_duerp.get_timeline(db, user_id)

# 5. Types de risques DUERP
@router.get("/risques-types")
def duerp_risques_types(user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud_duerp.get_risques_types(db, user_id)
