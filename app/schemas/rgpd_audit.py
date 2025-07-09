from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RgpdAuditBase(BaseModel):
    user_id: int
    company_id: int
    statut: str = "EN_COURS"

class RgpdAuditCreate(RgpdAuditBase):
    pass

class RgpdAuditRead(RgpdAuditBase):
    id: int
    created_at: datetime
    score: Optional[int]
    class Config:
        from_attributes = True
