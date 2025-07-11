# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.models.tenant import Tenant

from app.schemas.user import UserCreate, UserRead
from app.core.config import Settings

from app.crud.crud_user import create as create_user_crud, get_by_email

settings = Settings()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Vérifier l'existence d'un tenant "default"
    tenant = db.query(Tenant).filter_by(name="default").first()
    if not tenant:
        tenant = Tenant(name="default")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    # Vérifier que l'email n'existe pas déjà
    if get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Utiliser le CRUD user pour créer (le CRUD se charge du hash du mot de passe)
    user = create_user_crud(db, user_in, tenant_id=tenant.id)
    return user  # renvoie un modèle User (sera transformé en UserRead par FastAPI)

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
    # 1) Récupérer l'utilisateur par email via le CRUD
    user = get_by_email(db, form_data.username)
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
