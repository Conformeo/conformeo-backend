from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(db: Session, user_in: UserCreate, tenant_id: int = None):
    hashed_password = pwd_context.hash(user_in.password)
    db_obj = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow(),
        tenant_id=tenant_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update(db: Session, db_obj: User, user_in: UserUpdate):
    update_data = user_in.dict(exclude_unset=True)
    if update_data.get("password"):
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, user_id: int):
    obj = get(db, user_id)
    if obj:
        db.delete(obj)
        db.commit()

def get_all_by_tenant(db: Session, tenant_id: int):
    return db.query(User).filter(User.tenant_id == tenant_id).all()

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()