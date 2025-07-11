# app/schemas/rgpd_obligation.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class RgpdObligationBase(BaseModel):
    label: str
    status: bool
    last_update: Optional[date]

class RgpdObligationCreate(RgpdObligationBase):
    pass

class RgpdObligationRead(RgpdObligationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
