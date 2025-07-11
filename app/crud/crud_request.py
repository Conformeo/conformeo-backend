from sqlalchemy.orm import Session
from app.models.request import RgpdRequest
from app.schemas.request import RgpdRequestCreate, RgpdRequestUpdate

def create(db: Session, obj_in: RgpdRequestCreate):
    db_obj = RgpdRequest(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def list_by_user(db: Session, user_id: int):
    return db.query(RgpdRequest).filter(RgpdRequest.user_id == user_id).order_by(RgpdRequest.date_submitted.desc()).all()

def update(db: Session, req_id: int, obj_in: RgpdRequestUpdate):
    db_obj = db.query(RgpdRequest).filter(RgpdRequest.id == req_id).first()
    if not db_obj:
        return None
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get(db: Session, req_id: int):
    return db.query(RgpdRequest).filter(RgpdRequest.id == req_id).first()
