from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.request import RgpdRequestCreate, RgpdRequestRead, RgpdRequestUpdate
from app.crud import crud_request

router = APIRouter(prefix="/rgpd/requests", tags=["rgpd_requests"])

@router.post("/", response_model=RgpdRequestRead)
def create_request(data: RgpdRequestCreate, db: Session = Depends(get_db)):
    return crud_request.create(db, data)

@router.get("/", response_model=list[RgpdRequestRead])
def list_requests(user_id: int, db: Session = Depends(get_db)):
    return crud_request.list_by_user(db, user_id)

@router.put("/{req_id}", response_model=RgpdRequestRead)
def update_request(req_id: int, data: RgpdRequestUpdate, db: Session = Depends(get_db)):
    req = crud_request.update(db, req_id, data)
    if not req:
        raise HTTPException(404, detail="Demande non trouvée")
    return req
