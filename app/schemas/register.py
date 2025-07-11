from pydantic import BaseModel
from typing import Optional
from datetime import date

class RegisterBase(BaseModel):
    nom_traitement: str
    finalite: Optional[str] = None
    base_legale: Optional[str] = None
    personnes_concernees: Optional[str] = None
    duree_conservation: Optional[str] = None
    dpo_id: Optional[int] = None
    date_creation: Optional[date] = None

class RegisterCreate(RegisterBase):
    user_id: int

class RegisterRead(RegisterBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2
