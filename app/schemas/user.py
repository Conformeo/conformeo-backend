# backend/app/schemas/user.py

from typing import Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schéma pour l'inscription :
    - email : doit être une adresse valide
    - password : au moins 8 caractères
    """
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserRead(BaseModel):
    """
    Schéma pour renvoyer un utilisateur en réponse :
    - id, email, is_active, date_created
    """
    id: int
    email: EmailStr
    is_active: bool
    date_created: datetime

    class Config:
        orm_mode = True
