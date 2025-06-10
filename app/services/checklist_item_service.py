from sqlalchemy.orm import Session
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist_item import ChecklistItemCreate, ChecklistItemUpdate


def get_items_by_checklist(db: Session, checklist_id: int):
    return (
        db.query(ChecklistItem).filter(ChecklistItem.checklist_id == checklist_id).all()
    )


def create_item(db: Session, checklist_id: int, data: ChecklistItemCreate):
    item = ChecklistItem(checklist_id=checklist_id, **data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: ChecklistItem, data: ChecklistItemUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: ChecklistItem):
    db.delete(item)
    db.commit()
