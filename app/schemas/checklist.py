from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime  # si tu as created_at


class ChecklistBase(BaseModel):
    name: str
    description: Optional[str] = None  # ←  Clé présente partout


class ChecklistCreate(ChecklistBase):
    tenant_id: int


class ChecklistUpdate(ChecklistBase):  # ←  On peut tout modifier
    pass


class ChecklistRead(ChecklistBase):
    id: int
    tenant_id: int
    created_at: datetime  # si tu l’as ajouté

    model_config = ConfigDict(from_attributes=True)
