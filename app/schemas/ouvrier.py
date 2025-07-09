from pydantic import BaseModel
from typing import Optional
from datetime import date

class OuvrierBase(BaseModel):
    nom: str
    prenom: str
    date_embauche: Optional[date] = None
    poste: Optional[str] = None
    formation_a_jour: Optional[str] = None

class OuvrierCreate(OuvrierBase):
    pass

class OuvrierRead(OuvrierBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
