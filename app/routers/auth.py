# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.user import UserCreate, UserRead
from app.crud.crud_user import create as create_user_crud, get_by_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter_by(name="default").first()
    if not tenant:
        tenant = Tenant(name="default")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    if get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user = create_user_crud(db, user_in, tenant_id=tenant.id)
    return user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None
):
    user = get_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # DEBUG: Vérifie bien la clé utilisée pour signer
    from app.core.config import settings as _settings
    print("DEBUG SECRET_KEY LOGIN:", _settings.SECRET_KEY)

    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
