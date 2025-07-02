# ────────────────────────────────────────────────────────────────────────────────
# RGPD – Traitements & catalogue d’actions
# ────────────────────────────────────────────────────────────────────────────────
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.processing import Processing
from app.models.tenant import Tenant
from app.models.gdpr_action import GdprAction

from app.schemas.processing import (
    ProcessingCreate,
    ProcessingUpdate,
    ProcessingOut,
)
from app.schemas.gdpr_action import GdprActionRead
from app.crud import crud_processing, crud_gdpr_action

router = APIRouter(
    prefix="/rgpd/processings",
    tags=["rgpd"],
)

# ─────────────────────────── L I S T  &  C R E A T E ────────────────────────────
@router.get("/", response_model=List[ProcessingOut])
def list_processings(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Processing).offset(skip).limit(limit).all()


@router.post(
    "",
    response_model=ProcessingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_processing(dto: ProcessingCreate, db: Session = Depends(get_db)):
    if not db.get(Tenant, dto.tenant_id):
        raise HTTPException(status_code=404, detail="Tenant not found")

    proc = Processing(**dto.model_dump())
    db.add(proc)
    db.commit()
    db.refresh(proc)
    return proc


# (URL avec « / » final – masquée de la doc)
@router.post(
    "/",
    response_model=ProcessingOut,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_processing_slash(dto: ProcessingCreate, db: Session = Depends(get_db)):
    return create_processing(dto, db)

# ─────────────────────────── U P D A T E  &  D E L E T E ────────────────────────
@router.put("/{proc_id}", response_model=ProcessingOut)
def update_processing(proc_id: int, dto: ProcessingUpdate, db: Session = Depends(get_db)):
    proc = db.get(Processing, proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Processing not found")

    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(proc, field, value)

    db.commit()
    db.refresh(proc)
    return proc


@router.delete("/{proc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_processing(proc_id: int, db: Session = Depends(get_db)):
    proc = db.get(Processing, proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Processing not found")

    db.delete(proc)
    db.commit()

# ─────────────────────────── A C T I O N S  R G P D ─────────────────────────────
@router.get(
    "/actions/",
    response_model=List[GdprActionRead],
    summary="Catalogue complet des actions RGPD",
)
def list_actions(db: Session = Depends(get_db)):
    return crud_gdpr_action.get_all(db)


@router.get(
    "/{processing_id}/actions",
    response_model=List[GdprActionRead],
    summary="Actions recommandées pour un traitement",
)
def recommended_actions(processing_id: int, db: Session = Depends(get_db)):
    processing = crud_processing.get(db, processing_id)
    if not processing:
        raise HTTPException(status_code=404, detail="Processing not found")

    return crud_gdpr_action.get_recommended(db, processing)

# ────────────────── A J O U T / S U P P R E S S I O N  d’une action ─────────────
@router.post(
    "/{proc_id}/actions/{action_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Associe une action RGPD au traitement",
)
def add_action_to_processing(proc_id: int, action_id: int, db: Session = Depends(get_db)):
    proc   = db.get(Processing,  proc_id)
    action = db.get(GdprAction, action_id)
    if not (proc and action):
        raise HTTPException(status_code=404, detail="Processing ou action introuvable")

    if action not in proc.actions:
        proc.actions.append(action)
        db.commit()
    return Response(status_code=204)


@router.delete(
    "/{proc_id}/actions/{action_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Dissocie l’action RGPD du traitement",
)
def remove_action_from_processing(proc_id: int, action_id: int, db: Session = Depends(get_db)):
    proc   = db.get(Processing,  proc_id)
    action = db.get(GdprAction, action_id)
    if not (proc and action):
        raise HTTPException(status_code=404, detail="Processing ou action introuvable")

    if action in proc.actions:
        proc.actions.remove(action)
        db.commit()
    return Response(status_code=204)
