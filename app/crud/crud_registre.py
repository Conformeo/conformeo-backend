from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.registre import Registre
from app.schemas.registre import RegistreCreate

def create(db: Session, obj: RegistreCreate, user_id: int) -> Registre:
    """Crée un nouveau registre RGPD, lié à l'utilisateur courant."""
    db_obj = Registre(**obj.dict(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_by_user(db: Session, user_id: int) -> List[Registre]:
    """Retourne tous les registres du user courant."""
    return db.query(Registre).filter(Registre.user_id == user_id).all()

def update(db: Session, registre_id: int, data: dict, user_id: int) -> Optional[Registre]:
    """Met à jour un registre, mais uniquement s'il appartient à l'utilisateur courant."""
    obj = db.query(Registre).filter(
        Registre.id == registre_id, Registre.user_id == user_id
    ).first()
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, registre_id: int, user_id: int) -> bool:
    """Supprime un registre RGPD, uniquement s'il appartient à l'utilisateur courant."""
    obj = db.query(Registre).filter(
        Registre.id == registre_id, Registre.user_id == user_id
    ).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
