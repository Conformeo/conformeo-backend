from fastapi import APIRouter, Depends, HTTPException, status, Path, Response, Body
from sqlalchemy.orm import Session

from app.schemas.user import UserRead, UserUpdate, UserCreate
from app.dependencies.auth import get_current_active_user, get_current_active_admin
from app.db.session import get_db
from app.models.user import User as UserModel

# Import direct des CRUDs
from app.crud.crud_obligation import create_defaults_for_user
from app.crud.crud_user import (
    create as create_user_crud,
    get as get_user_crud,
    update as update_user_crud,
    delete as delete_user_crud,
    get_all_by_tenant,
)


# Import direct des CRUDs
from app.crud.crud_obligation import create_defaults_for_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate = Body(...),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(get_current_active_admin),
):
    """
    Crée un nouvel utilisateur dans le tenant de l'admin courant.
    Initialise ses obligations RGPD par défaut.
    """
    new_user = create_user_crud(db, user_in, tenant_id=admin.tenant_id)
    create_defaults_for_user(db, new_user.id)
    return new_user

@router.get("/", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    admin: UserModel = Depends(get_current_active_admin),
):
    """
    Liste tous les utilisateurs du tenant de l'admin courant.
    """
    return get_all_by_tenant(db, admin.tenant_id)

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_user_by_id(
    user_id: int = Path(..., ge=1),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    target = get_user_crud(db, user_id)
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )
    if target.id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Pas autorisé"
        )
    return target

@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def modify_user(
    user_id: int = Path(..., ge=1),
    user_in: UserUpdate = Body(),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    target = get_user_crud(db, user_id)
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )
    if target.id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Pas autorisé"
        )
    updated = update_user_crud(db, target, user_in)
    return updated

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un utilisateur (admin only)",
)
def remove_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(get_current_active_admin),
):
    user = get_user_crud(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if user.id == admin.id:
        raise HTTPException(
            status_code=400, detail="Impossible de supprimer son propre compte"
        )
    delete_user_crud(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
