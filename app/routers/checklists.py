from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.checklist import Checklist
from app.schemas.checklist import ChecklistCreate, ChecklistRead, ChecklistUpdate
from app.dependencies.auth import get_current_active_user
from app.models.user import User  # ou depuis schemas si tu utilises un schéma Pydantic


router = APIRouter(prefix="/checklists", tags=["checklists"])


@router.post("/", response_model=ChecklistRead, status_code=status.HTTP_201_CREATED)
def create_checklist(checklist_in: ChecklistCreate, db: Session = Depends(get_db)):
    checklist = Checklist(**checklist_in.dict())
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    return checklist


@router.get("/", response_model=List[ChecklistRead])  # ou Checklist si pas de schéma
def list_checklists(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return (
        db.query(Checklist).filter(Checklist.tenant_id == current_user.tenant_id).all()
    )


@router.get("/{checklist_id}", response_model=ChecklistRead)
def read_checklist(checklist_id: int, db: Session = Depends(get_db)):
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist


@router.put("/{checklist_id}", response_model=ChecklistRead)
def update_checklist(
    checklist_id: int, checklist_in: ChecklistUpdate, db: Session = Depends(get_db)
):
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    for attr, value in checklist_in.dict(exclude_unset=True).items():
        setattr(checklist, attr, value)
    db.commit()
    db.refresh(checklist)
    return checklist


@router.delete("/{checklist_id}", status_code=204)
def delete_checklist(checklist_id: int, db: Session = Depends(get_db)):
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    db.delete(checklist)
    db.commit()
    return None
