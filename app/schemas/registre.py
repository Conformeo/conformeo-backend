from pydantic import BaseModel
from typing import Optional
from datetime import date

class RegistreBase(BaseModel):
    nom_traitement: str
    finalite: str
    categorie_donnees: Optional[str] = None
    categorie_personnes: Optional[str] = None
    base_legale: Optional[str] = None
    duree_conservation: Optional[str] = None
    mesures_securite: Optional[str] = None
    date_creation: Optional[date] = None
    commentaire: Optional[str] = None

class RegistreCreate(RegistreBase):
    user_id: int

class RegistreRead(RegistreBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
