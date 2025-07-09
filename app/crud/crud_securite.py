from app.models.securite import SecuriteControle

def get_summary(db, user_id: int):
    controles = db.query(SecuriteControle).filter(SecuriteControle.user_id == user_id).all()
    nb_controles = len(controles)
    nb_nc_total = sum(c.nb_nc for c in controles)
    derniere = max((c.date_controle for c in controles if c.date_controle), default=None)
    return {
        "total_controles": nb_controles,
        "total_nc": nb_nc_total,
        "derniere_controle": derniere
    }

def get_nonconformes(db, user_id: int):
    return [
        {
            "id": c.id,
            "date_controle": c.date_controle,
            "type": c.type,
            "nb_nc": c.nb_nc,
            "rapport": c.rapport
        }
        for c in db.query(SecuriteControle)
                  .filter(SecuriteControle.user_id == user_id, SecuriteControle.nb_nc > 0)
                  .all()
    ]

def get_timeline(db, user_id: int):
    return [
        {
            "date": c.date_controle,
            "nb_nc": c.nb_nc
        }
        for c in db.query(SecuriteControle)
                  .filter(SecuriteControle.user_id == user_id)
                  .order_by(SecuriteControle.date_controle.asc())
                  .all()
    ]

def get_controles_by_user(db, user_id: int):
    return db.query(SecuriteControle).filter(SecuriteControle.user_id == user_id).all()

def get_controles_by_site(db, site_id: int):
    return db.query(SecuriteControle).filter(SecuriteControle.site_id == site_id).all()

def get_controles_by_societe(db, societe_id: int):
    return db.query(SecuriteControle).filter(SecuriteControle.societe_id == societe_id).all()

def create_controle(db, controle_in):
    controle = SecuriteControle(**controle_in.dict())
    db.add(controle)
    db.commit()
    db.refresh(controle)
    return controle
