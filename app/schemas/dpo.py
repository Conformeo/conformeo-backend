from pydantic import ConfigDict
from pydantic import BaseModel
from datetime import date
from typing import Optional

class DpoBase(BaseModel):
    user_id: int
    nom: str
    email: str
    telephone: Optional[str] = None
    designation_date: Optional[date] = None
    is_external: Optional[bool] = False
    model_config = ConfigDict(from_attributes=True)

class DpoCreate(DpoBase):
    pass

class DpoRead(DpoBase):
    id: int

    class Config:
        orm_mode = True
