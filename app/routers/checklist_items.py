from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_active_user
from app.db.session import get_db
from app.models.checklist import Checklist
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist_item import (
    ChecklistItemCreate,
    ChecklistItemRead,
    ChecklistItemUpdate,
)
from app.services.checklist_item_service import (
    get_items_by_checklist,
    create_item,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/checklists/{checklist_id}/items", tags=["Checklist Items"])


@router.get("/", response_model=list[ChecklistItemRead])
def list_items(
    checklist_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    checklist = (
        db.query(Checklist).filter_by(id=checklist_id, tenant_id=user.tenant_id).first()
    )
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    return get_items_by_checklist(db, checklist_id)


@router.post("/", response_model=ChecklistItemRead, status_code=status.HTTP_201_CREATED)
def add_item(
    checklist_id: int = Path(..., ge=1),
    data: ChecklistItemCreate = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    checklist = (
        db.query(Checklist).filter_by(id=checklist_id, tenant_id=user.tenant_id).first()
    )
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    return create_item(db, checklist_id, data)


@router.put("/{item_id}", response_model=ChecklistItemRead)
def update_item_api(
    checklist_id: int = Path(..., ge=1),
    item_id: int = Path(..., ge=1),
    data: ChecklistItemUpdate = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    item = (
        db.query(ChecklistItem)
        .join(Checklist)
        .filter(
            ChecklistItem.id == item_id,
            ChecklistItem.checklist_id == checklist_id,
            Checklist.tenant_id == user.tenant_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(404, "Item not found")
    return update_item(db, item, data)


@router.delete("/{item_id}", status_code=204)
def remove_item(
    checklist_id: int = Path(..., ge=1),
    item_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    item = (
        db.query(ChecklistItem)
        .join(Checklist)
        .filter(
            ChecklistItem.id == item_id,
            ChecklistItem.checklist_id == checklist_id,
            Checklist.tenant_id == user.tenant_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(404, "Item not found")
    delete_item(db, item)
    return {}
