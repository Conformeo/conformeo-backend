from pydantic import ConfigDict
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class DpoBase(BaseModel):
    """
    Schéma commun pour DPO (Délégué à la Protection des Données)
    """
    nom: str
    email: EmailStr
    telephone: Optional[str] = None
    designation_date: Optional[date] = None
    is_external: bool = False
    model_config = ConfigDict(from_attributes=True)

class DpoCreate(DpoBase):
    """
    Schéma pour création d’un DPO (POST)
    """
    user_id: int

class DpoUpdate(BaseModel):
    """
    Schéma pour mise à jour d’un DPO (PATCH/PUT)
    """
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    designation_date: Optional[date] = None
    is_external: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class DpoRead(DpoBase):
    """
    Schéma pour lecture d’un DPO (GET)
    """
    user_id: int

    class Config:
        orm_mode = True
