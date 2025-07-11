from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.register import RegisterCreate, RegisterRead
from app.crud import crud_register

router = APIRouter(prefix="/registers", tags=["registers"])

@router.post("/", response_model=RegisterRead)
def create_register(register: RegisterCreate, db: Session = Depends(get_db)):
    return crud_register.create(db, register)

@router.get("/", response_model=list[RegisterRead])
def list_registers(user_id: int, db: Session = Depends(get_db)):
    return crud_register.get_by_user(db, user_id)

@router.put("/{register_id}", response_model=RegisterRead)
def update_register(register_id: int, data: dict, db: Session = Depends(get_db)):
    reg = crud_register.update(db, register_id, data)
    if not reg:
        raise HTTPException(status_code=404, detail="Registre non trouvé")
    return reg

@router.delete("/{register_id}", status_code=204)
def delete_register(register_id: int, db: Session = Depends(get_db)):
    success = crud_register.delete(db, register_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registre non trouvé")
