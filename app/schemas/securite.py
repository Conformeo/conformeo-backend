from pydantic import BaseModel
from typing import Optional
from datetime import date

class SecuriteControleBase(BaseModel):
    type: str
    date_controle: Optional[date]
    nb_nc: int = 0
    rapport: Optional[str]
    site_id: Optional[int] = None
    societe_id: Optional[int] = None

class SecuriteControleCreate(SecuriteControleBase):
    user_id: int  # obligatoire à la création

class SecuriteControleRead(SecuriteControleBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
