from app.models.checklist import Checklist


def get_checklist_by_id(db, checklist_id):
    return db.query(Checklist).filter(Checklist.id == checklist_id).first()


def create_checklist(db, checklist_in):
    checklist = Checklist(**checklist_in.dict())
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    return checklist


def update_checklist(db, checklist, checklist_in):
    for attr, value in checklist_in.dict(exclude_unset=True).items():
        setattr(checklist, attr, value)  # description sera bien copiée
    db.commit()
    db.refresh(checklist)
    return checklist


def delete_checklist(db, checklist):
    db.delete(checklist)
    db.commit()
