# app/api/v1/endpoints/rgpd_registre.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.registre import Registre
from app.schemas.registre import RegistreCreate, RegistreRead
from app.core.security import get_current_active_user
from app.models.user import User
from app.crud import crud_registre  # à créer si besoin

router = APIRouter(prefix="/rgpd", tags=["RGPD – Registre"])

@router.post(
    "/registre",
    response_model=RegistreRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une entrée de registre",
)
def create_registre(
    *,
    entry_in: RegistreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # on transmet directement l’objet Pydantic + l’ID utilisateur
    return crud_registre.create(db, entry_in, current_user.id)


@router.get(
    "/registre",
    response_model=List[RegistreRead],
    summary="Lister le registre de l’utilisateur courant",
)
def list_registre(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(Registre)
        .filter(Registre.user_id == current_user.id)
        .order_by(Registre.created_at.asc())
        .all()
    )
