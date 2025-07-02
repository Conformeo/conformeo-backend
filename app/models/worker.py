from pydantic import BaseModel
from typing import Optional

class Worker(BaseModel):
    id: str
    nom: str
    prenom: str
    poste: str
    telephone: Optional[str] = None
    email: Optional[str] = None
    siteId: Optional[str] = None
    equipe: str
