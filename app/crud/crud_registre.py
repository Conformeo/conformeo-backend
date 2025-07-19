# app/crud/crud_registre.py
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.registre import Registre
from app.schemas.registre import RegistreCreate, RegistreUpdate


# --------------------------------------------------------------------------- #
# CREATE
# --------------------------------------------------------------------------- #
def create(db: Session, payload: RegistreCreate, user_id: int) -> Registre:
    data = payload.model_dump()
    data["user_id"] = user_id

    obj = Registre(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# --------------------------------------------------------------------------- #
# READ
# --------------------------------------------------------------------------- #
def get_by_user(db: Session, user_id: int) -> List[Registre]:
    """Renvoie les registres de l’utilisateur, triés du plus récent au plus ancien."""
    return (
        db.query(Registre)
        .filter(Registre.user_id == user_id)
        .order_by(Registre.created_at.desc())
        .all()
    )


# --------------------------------------------------------------------------- #
# UPDATE
# --------------------------------------------------------------------------- #
def update(
    db: Session,
    registre_id: int,
    payload: RegistreUpdate,
    user_id: int,
) -> Optional[Registre]:
    """Met à jour un registre si, et seulement si, il appartient à l’utilisateur."""
    obj = (
        db.query(Registre)
        .filter(Registre.id == registre_id, Registre.user_id == user_id)
        .first()
    )
    if not obj:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(obj)
    return obj


# --------------------------------------------------------------------------- #
# DELETE
# --------------------------------------------------------------------------- #
def delete(db: Session, registre_id: int, user_id: int) -> bool:
    """Supprime un registre appartenant à l’utilisateur ; retourne `True` si OK."""
    obj = (
        db.query(Registre)
        .filter(Registre.id == registre_id, Registre.user_id == user_id)
        .first()
    )
    if not obj:
        return False

    db.delete(obj)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return True
