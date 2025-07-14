# backend/app/dependencies/auth.py

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings         # IMPORTE BIEN *l'instance* settings, PAS la classe Settings !
from app.core.security import oauth2_scheme  # doit être importé, ne pas redéfinir dans ce fichier

# NE PAS refaire settings = Settings() ici ! On utilise celui déjà importé

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # DEBUG pour t'assurer que la clé est bien la même partout :
        print("DEBUG SECRET_KEY DECODE:", settings.SECRET_KEY)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif",
        )
    return current_user

def get_current_active_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (admin only)",
        )
    return current_user

# (Optionnel) Pour debug ou support API externe : extraire le token d'une requête manuellement
def get_token_from_request(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):]
    return None
