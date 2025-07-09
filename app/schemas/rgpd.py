from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel
from app.models.gdpr_action import ActionScope  # selon ton modèle, adapte le nom

class GdprActionBase(BaseModel):
    label: str
    article: Optional[str] = None
    scope: ActionScope

class GdprActionRead(GdprActionBase):
    id: int

    model_config = {"from_attributes": True}  # Pydantic V2

class RgpdExigenceBase(BaseModel):
    label: str
    article: Optional[str] = None
    critical: Optional[bool] = False
    advice: Optional[str] = None

class RgpdExigenceRead(RgpdExigenceBase):
    id: int
    class Config:
        orm_mode = True

class RgpdAuditExigenceBase(BaseModel):
    exigence_id: int
    answer: str
    critical: Optional[bool] = False
    advice: Optional[str] = None

class RgpdAuditExigenceRead(RgpdAuditExigenceBase):
    id: int
    exigence: RgpdExigenceRead

    class Config:
        orm_mode = True

class RgpdAuditBase(BaseModel):
    user_id: int
    company_id: Optional[int]
    statut: Optional[str] = "EN_COURS"

class RgpdAuditCreate(RgpdAuditBase):
    exigences: List[RgpdAuditExigenceBase]

class RgpdAuditRead(RgpdAuditBase):
    id: int
    created_at: Optional[str]
    score: Optional[int]
    exigences: List[RgpdAuditExigenceRead]
    class Config:
        orm_mode = True
