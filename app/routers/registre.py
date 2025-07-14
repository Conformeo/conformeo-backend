# backend/app/routers/registre.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.registre import RegistreCreate, RegistreRead
from app.crud import crud_registre, crud_audit_log
from app.schemas.audit_log import AuditLogCreate
from app.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/rgpd/registre", tags=["registres"])

@router.post("/", response_model=RegistreRead)
def create_registre(
    registre_in: RegistreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    print(f"USER AUTH: {current_user.email}")  # <-- tu devrais voir ce print
    print("DEBUG TOKEN PAYLOAD:", payload)
    print("DEBUG USER_ID:", user_id)
    print("DEBUG USER:", user)

    new_registre = crud_registre.create(db, registre_in, user_id=current_user.id)
    crud_audit_log.create(db, AuditLogCreate(
        user_id=current_user.id,
        action='create',
        object_type='registre',
        object_id=new_registre.id,
        details="Création registre RGPD"
    ))
    return new_registre

@router.get("/", response_model=list[RegistreRead])
def list_registres(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    print("USER AUTH:", current_user.email)  # doit s’afficher si ça marche

    return crud_registre.get_by_user(db, current_user.id)

@router.put("/{registre_id}", response_model=RegistreRead)
def update_registre(
    registre_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    reg = crud_registre.update(db, registre_id, data, user_id=current_user.id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registre non trouvé ou non autorisé")
    return reg

@router.delete("/{registre_id}", status_code=204)
def delete_registre(
    registre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    success = crud_registre.delete(db, registre_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Registre non trouvé ou non autorisé")
