from pydantic import BaseModel
from typing import Optional

class RgpdAuditExigenceBase(BaseModel):
    audit_id: int
    exigence_id: int
    answer: Optional[str]
    critical: bool = False
    advice: Optional[str]

class RgpdAuditExigenceCreate(RgpdAuditExigenceBase):
    pass

class RgpdAuditExigenceRead(RgpdAuditExigenceBase):
    id: int
    class Config:
        from_attributes = True
