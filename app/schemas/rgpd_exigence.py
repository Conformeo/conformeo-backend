# app/schemas/rgpd_exigence.py

from pydantic import BaseModel
from typing import Optional

class RgpdExigenceBase(BaseModel):
    label: str
    question: Optional[str] = None
    description: Optional[str] = None

class RgpdExigenceCreate(RgpdExigenceBase):
    pass

class RgpdExigenceRead(BaseModel):
    id: int
    label: str
    article: Optional[str] = None
    critical: Optional[bool] = None
    advice: Optional[str] = None
    question: Optional[str] = None

    class Config:
        from_attributes = True  # ou orm_mode = True si Pydantic V1
