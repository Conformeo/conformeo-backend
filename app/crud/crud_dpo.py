# app/crud/crud_dpo.py

from sqlalchemy.orm import Session
from app.models.dpo import Dpo
from app.schemas.dpo import DpoCreate, DpoBase
from app.crud import crud_audit_log
from app.schemas.audit_log import AuditLogCreate

crud_audit_log.create(db, AuditLogCreate(
    user_id=current_user.id,
    action='create',
    object_type='register',
    object_id=new_register.id,
    details="Création d'un DPO"
))

def get_dpo_by_user(db: Session, user_id: int):
    return db.query(Dpo).filter(Dpo.user_id == user_id).first()

def get_dpo_by_id(db: Session, dpo_id: int):
    return db.query(Dpo).filter(Dpo.id == dpo_id).first()

def create_or_update_dpo(db: Session, user_id: int, dpo_data: DpoCreate):
    dpo = get_dpo_by_user(db, user_id)
    if dpo:
        # Mise à jour des champs existants (hors id/user_id)
        for key, value in dpo_data.dict(exclude={"user_id"}).items():
            setattr(dpo, key, value)
    else:
        dpo = Dpo(user_id=user_id, **dpo_data.dict(exclude={"user_id"}))
        db.add(dpo)
    db.commit()
    db.refresh(dpo)
    return dpo

def update_dpo(db: Session, dpo_id: int, dpo_data: DpoBase):
    dpo = get_dpo_by_id(db, dpo_id)
    if not dpo:
        return None
    for key, value in dpo_data.dict(exclude_unset=True).items():
        setattr(dpo, key, value)
    db.commit()
    db.refresh(dpo)
    return dpo

def delete_dpo(db: Session, dpo_id: int):
    dpo = get_dpo_by_id(db, dpo_id)
    if dpo:
        db.delete(dpo)
        db.commit()
        return True
    return False
