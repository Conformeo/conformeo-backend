from __future__ import annotations

"""
app.core.security
=================
Utilitaires centralisés :

- Hash / vérification de mot de passe
- Création / décodage de JWT
- Dépendances FastAPI pour récupérer l’utilisateur courant

Import :

    from app.core.security import (
        verify_password,
        get_password_hash,
        create_access_token,
        get_current_active_user,
    )
"""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

# ---------------------------------------------------------------------------#
#  Constantes                                                                #
# ---------------------------------------------------------------------------#

ALGORITHM: str = settings.ALGORITHM or "HS256"  # sécurité : garde-fou

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Argon2 (fort) + bcrypt (pour une transition douce si besoin)
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# ---------------------------------------------------------------------------#
#  Mot de passe                                                              #
# ---------------------------------------------------------------------------#


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Retourne **True** si le mot de passe en clair correspond au hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Retourne le hash du mot de passe (argon2 par défaut)."""
    return pwd_context.hash(password)


# ---------------------------------------------------------------------------#
#  JWT                                                                       #
# ---------------------------------------------------------------------------#


def _build_claims(data: Dict[str, Any], expires_delta: timedelta | None) -> Dict[str, Any]:
    now = datetime.now(UTC)
    exp_delta = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = data.copy()
    claims.update({"iat": now, "exp": now + exp_delta})
    return claims


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Encode *data* + claims standard dans un JWT signé."""
    to_encode = _build_claims(data, expires_delta)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------------------------#
#  Dépendances FastAPI                                                       #
# ---------------------------------------------------------------------------#

_credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Impossible de valider les identifiants",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    """Décodage du JWT et récupération de l’utilisateur."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("user_id")
        if user_id is None:
            raise _credentials_exc
    except JWTError:
        raise _credentials_exc from None

    user: User | None = db.query(User).get(user_id)
    if user is None:
        raise _credentials_exc
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Vérifie également que l’utilisateur est marqué actif."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_user
