from sqlalchemy.orm import Session
from app.models.ouvrier import Ouvrier
from app.schemas.ouvrier import OuvrierCreate

def get_ouvriers_by_user(db: Session, user_id: int):
    return db.query(Ouvrier).filter_by(user_id=user_id).all()

def create_ouvrier(db: Session, user_id: int, ouvrier_in: OuvrierCreate):
    db_ouvrier = Ouvrier(**ouvrier_in.model_dump(), user_id=user_id)
    db.add(db_ouvrier)
    db.commit()
    db.refresh(db_ouvrier)
    return db_ouvrier

def get_ouvriers_stats(db: Session, user_id: int):
    from sqlalchemy import func
    nb_ouvriers = db.query(Ouvrier).filter_by(user_id=user_id).count()
    # Exemples à compléter selon tes champs réels
    return {
        "nb_ouvriers": nb_ouvriers,
        "formations_a_faire": 2,
        "last_hire": "2024-06-28"  # à remplacer par une vraie requête SQL
    }
