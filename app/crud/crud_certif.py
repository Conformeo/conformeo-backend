from sqlalchemy.orm import Session
from app.models.certif import Certif
from app.schemas.certif import CertifCreate

def get_certifs_by_user(db: Session, user_id: int):
    return db.query(Certif).filter_by(user_id=user_id).all()

def create_certif(db: Session, user_id: int, certif_in: CertifCreate):
    db_certif = Certif(**certif_in.model_dump(), user_id=user_id)
    db.add(db_certif)
    db.commit()
    db.refresh(db_certif)
    return db_certif

def get_certif_stats(db: Session, user_id: int):
    from sqlalchemy import func
    nb_certifs = db.query(Certif).filter_by(user_id=user_id).count()
    expireSous30j = db.query(Certif).filter(
        Certif.user_id == user_id,
        Certif.date_expiration != None,
        Certif.date_expiration <= func.current_date() + func.cast(30, Integer)
    ).count()
    return {
        "nb_certifs": nb_certifs,
        "expireSous30j": expireSous30j,
    }
