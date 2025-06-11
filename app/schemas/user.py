# backend/app/schemas/user.py

from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict, Field
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
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    # avant : class Config: orm_mode = True
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Schéma pour mettre à jour un utilisateur :
    - email : optionnel, doit être une adresse valide
    - password : optionnel, au moins 8 caractères
    """

    email: Annotated[EmailStr, Field(default=None)]
    password: Annotated[str, Field(default=None, min_length=8)]

    model_config = ConfigDict(from_attributes=True)
