# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.config import Settings

settings = Settings()

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur.
    - Vérifie si l'email existe déjà.
    - Hash le mot de passe, crée l'utilisateur en base.
    - Retourne l'objet UserRead.
    """
    # 1) Vérifier si l'email est déjà utilisé
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà utilisé"
        )

    # 2) Créer l'utilisateur
    hashed_pwd = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Connexion d'un utilisateur :
    - Reçoit form-data avec "username" (email) et "password".
    - Vérifie l'existence de l'utilisateur et le mot de passe.
    - Génère un JWT (access_token) si OK.
    """
    # 1) Récupérer l'utilisateur par email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2) Vérifier le mot de passe
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3) Générer le token
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
