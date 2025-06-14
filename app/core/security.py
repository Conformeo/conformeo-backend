# backend/app/core/security.py

from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import Settings

settings = Settings()
# Indique l’URL où l’on récupère le token (login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Contexte de hachage pour bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Génère un JWT à partir d’un dict `data` (par exemple {"sub": email, "user_id": id}).
    Le token expirera selon `expires_delta` ou selon ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
