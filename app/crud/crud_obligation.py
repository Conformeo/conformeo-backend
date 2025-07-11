from sqlalchemy.orm import Session
from app.models.obligation import Obligation
from app.schemas.obligation import ObligationCreate, ObligationUpdate
from app.constants.obligation import OBLIGATIONS_DEFAULT  # <-- décommente bien !
from datetime import date
from app.crud import crud_audit_log
from app.schemas.audit_log import AuditLogCreate

def create_defaults_for_user(db: Session, user_id: int):
    # ... Création des obligations ...
    for obligation in obligations_created:
        from app.crud import crud_audit_log
        from app.schemas.audit_log import AuditLogCreate
        crud_audit_log.create(db, AuditLogCreate(
            user_id=user_id,
            action='create',
            object_type='obligation',
            object_id=obligation.id,
            details="Création par défaut"
        ))


def get_all_by_user(db: Session, user_id: int):
    """Récupère toutes les obligations RGPD d'un utilisateur donné."""
    return db.query(Obligation).filter(Obligation.user_id == user_id).all()

def get(db: Session, obligation_id: int):
    return db.query(Obligation).filter(Obligation.id == obligation_id).first()


def create(db: Session, obj: ObligationCreate):
    """Crée une nouvelle obligation RGPD pour un utilisateur."""
    db_obj = Obligation(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Obligation, obj_in: ObligationUpdate):
    """Met à jour une obligation RGPD existante."""
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def create_defaults_for_user(db: Session, user_id: int):
    """
    Initialise les obligations RGPD par défaut pour un nouvel utilisateur.
    """
    for label in OBLIGATIONS_DEFAULT:
        db_obj = Obligation(
            label=label,
            status=False,
            last_update=None,
            user_id=user_id
        )
        db.add(db_obj)
    db.commit()

def delete(db: Session, obligation_id: int) -> bool:
    obj = db.query(Obligation).filter(Obligation.id == obligation_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
