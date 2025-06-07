# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session                       # <-- importer Session
from app.db.session import get_db                        # <-- importer get_db
from app.dependencies.auth import get_current_active_user
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import get_user_by_id, update_user
from app.models.user import User as UserModel
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Renvoie le profil de l’utilisateur courant (JWT).
    """
    return current_user



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
