from pydantic import BaseModel
from typing import Optional
from datetime import date

class Certification(BaseModel):
    id: str
    name: str
    validUntil: str
    status: str  # Ou Literal['OK', 'DUE', 'TO_SCHEDULE'] si tu veux

class CertifBase(BaseModel):
    label: str
    date_obtention: Optional[date] = None
    date_expiration: Optional[date] = None
    organisme: Optional[str] = None

class CertifCreate(CertifBase):
    pass

class CertifRead(CertifBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
