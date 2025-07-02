from sqlalchemy.orm import Session
from app.models.gdpr_action import GdprAction, ActionScope


# --------------------------------------------------------------------------- #
# Catalogue complet (seed auto si vide)                                       #
# --------------------------------------------------------------------------- #
def get_all(db: Session) -> list[GdprAction]:
    actions = db.query(GdprAction).all()
    if actions:
        return actions

    seed = [
        ("Tenir un registre des traitements",     "Art. 30",     ActionScope.ALL),
        ("Informer les personnes concernées",     "Art. 13-14",  ActionScope.ALL),
        ("Limiter la conservation des données",   "Art. 5-1-e)", ActionScope.ALL),
        ("Mettre en place une AIPD au besoin",    "Art. 35",     ActionScope.ALL),
        ("Documenter une procédure de violation", "Art. 33-34",  ActionScope.ALL),
        ("Nommer un DPO (si requis)",             "Art. 37",     ActionScope.ALL),
    ]
    for label, article, scope in seed:
        db.add(GdprAction(label=label, article=article, scope=scope))
    db.commit()
    return db.query(GdprAction).all()


# --------------------------------------------------------------------------- #
# Recommandations basiques (v1 : tout renvoyer)                               #
# --------------------------------------------------------------------------- #
def get_recommended(db: Session, processing) -> list[GdprAction]:
    # plus tard : filtrer selon processing.legal_basis, etc.
    return get_all(db)
