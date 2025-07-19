# app/schemas/rgpd_audit_exigence.py  ──────────────────────────────────────────
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.enums import AnswerEnum
from app.schemas.rgpd_exigence import RgpdExigenceRead


class RgpdAuditExigenceBase(BaseModel):
    answer: Optional[AnswerEnum] = None
    critical: bool = False
    advice: Optional[str] = None


class RgpdAuditExigenceCreate(BaseModel):
    exigence_id: int = Field(..., ge=1)
    answer: AnswerEnum            # ← accepte minuscules grâce au _missing_
    comment: str | None = ""
    proof: str | None = ""


class RgpdAuditExigenceRead(BaseModel):
    id: int
    exigence: RgpdExigenceRead
    answer: AnswerEnum | None
    comment: str | None = None

    model_config = {"from_attributes": True}
