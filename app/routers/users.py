# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Path, Response, Body
from sqlalchemy.orm import Session

from app.schemas.user import UserRead, UserUpdate
from app.dependencies.auth import get_current_active_user
from app.db.session import get_db
from app.services.user_service import get_user_by_id, update_user, delete_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Renvoie le profil de l’utilisateur courant (JWT).
    """
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Lire le profil d'un utilisateur par son ID"
)
def read_user_by_id(
    user_id: int = Path(..., ge=1),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    - Un utilisateur peut lire son propre profil.
    - Un admin peut lire n'importe quel profil.
    """
    target = get_user_by_id(db, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    if target.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pas autorisé")

    return target




@router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Mettre à jour un profil utilisateur"
)
def modify_user(
    user_id: int = Path(..., ge=1),
    user_in: UserUpdate = Body(),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    - Un utilisateur peut modifier son propre profil.
    - Un admin peut modifier n’importe quel profil.
    """
    target = get_user_by_id(db, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    # Vérifier les droits
    if target.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pas autorisé")

    updated = update_user(db, target, user_in)
    return updated


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un utilisateur (admin only)"
)
def remove_user(
    user_id: int = Path(..., ge=1),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    - Seul un admin (`current_user.is_admin == True`) peut supprimer un compte.
    - Renvoie 204 No Content si l’opération réussit.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pas autorisé")

    target = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    # On ne peut pas supprimer soi-même, éventuellement
    if target.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impossible de supprimer son propre compte")

    delete_user(db, target)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
