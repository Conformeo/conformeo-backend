# backend/app/routers/users.py

from fastapi import APIRouter, Depends
from app.schemas.user import UserRead
from app.dependencies.auth import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Renvoie le profil de l’utilisateur courant (JWT).
    """
    return current_user
