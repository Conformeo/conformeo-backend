from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ouvrier import OuvrierCreate, OuvrierRead
from app.crud import crud_ouvrier
from app.api.deps import get_db

router = APIRouter(prefix="/ouvriers", tags=["Ouvriers"])

@router.get("/summary", response_model=dict)
def summary(user_id: int, db: Session = Depends(get_db)):
    return crud_ouvrier.get_ouvriers_stats(db, user_id)

@router.get("/", response_model=list[OuvrierRead])
def list_ouvriers(user_id: int, db: Session = Depends(get_db)):
    return crud_ouvrier.get_ouvriers_by_user(db, user_id)

@router.post("/", response_model=OuvrierRead)
def create_ouvrier(user_id: int, ouvrier_in: OuvrierCreate, db: Session = Depends(get_db)):
    return crud_ouvrier.create_ouvrier(db, user_id, ouvrier_in)
