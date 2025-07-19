# app/crud/crud_rgpd_exigence.py

from sqlalchemy.orm import Session
from app.models.rgpd_exigence import RgpdExigence
from app.schemas.rgpd_exigence import RgpdExigenceCreate, RgpdExigenceRead

def get_all(db: Session):
    return db.query(RgpdExigence).all()

def get(db: Session, exigence_id: int):
    return db.query(RgpdExigence).filter(RgpdExigence.id == exigence_id).first()

def create(db: Session, exigence_in: RgpdExigenceCreate):
    db_obj = RgpdExigence(**exigence_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, exigence_id: int, data: dict):
    exigence = get(db, exigence_id)
    if not exigence:
        return None
    for k, v in data.items():
        setattr(exigence, k, v)
    db.commit()
    db.refresh(exigence)
    return exigence

def delete(db: Session, exigence_id: int):
    exigence = get(db, exigence_id)
    if not exigence:
        return False
    db.delete(exigence)
    db.commit()
    return True
