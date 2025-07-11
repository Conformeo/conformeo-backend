from sqlalchemy.orm import Session
from app.models.register import Register
from app.schemas.register import RegisterCreate
from app.crud import crud_audit_log
from app.schemas.audit_log import AuditLogCreate

crud_audit_log.create(db, AuditLogCreate(
    user_id=current_user.id,
    action='create',
    object_type='register',
    object_id=new_register.id,
    details="Création registre RGPD"
))

def create(db: Session, obj: RegisterCreate):
    db_obj = Register(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_by_user(db: Session, user_id: int):
    return db.query(Register).filter(Register.user_id == user_id).all()

def update(db: Session, register_id: int, data: dict):
    obj = db.query(Register).filter(Register.id == register_id).first()
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, register_id: int):
    obj = db.query(Register).filter(Register.id == register_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
