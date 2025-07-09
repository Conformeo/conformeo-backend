from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.gdpr_action_answer import GdprActionAnswerCreate, GdprActionAnswerRead
from app.crud import crud_gdpr_action_answer

router = APIRouter(prefix="/gdpr/answers", tags=["GDPR Answers"])

@router.post("/", response_model=GdprActionAnswerRead)
def submit_answer(answer_in: GdprActionAnswerCreate, db: Session = Depends(get_db)):
    return crud_gdpr_action_answer.create_answer(db, answer_in)

@router.get("/user/{user_id}", response_model=List[GdprActionAnswerRead])
def get_user_answers(user_id: int, db: Session = Depends(get_db)):
    return crud_gdpr_action_answer.get_answers_for_user(db, user_id)
