# app/schemas/rgpd_audit.py  ───────────────────────────────────────────────────
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.enums import AnswerEnum
from app.schemas.rgpd_audit_exigence import (
    RgpdAuditExigenceRead,
    RgpdAuditExigenceCreate,
)


# --------------------------------------------------------------------------- #
# READ                                                                        #
# --------------------------------------------------------------------------- #
class RgpdAuditRead(BaseModel):
    id: int
    user_id: int
    company_id: int | None = None
    titre: str
    statut: str
    created_at: datetime

    score: int | None = None
    conforme: int = 0
    non_conforme: int = 0
    critical_ko: list[str] = []

    exigences: list[RgpdAuditExigenceRead] = []

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------- #
# CREATE / UPDATE                                                              #
# --------------------------------------------------------------------------- #
class RgpdAuditCreate(BaseModel):
    # id utilisateur injecté par la dépendance de sécurité
    titre: str | None = None
    statut: str = "EN_COURS"
    exigences: list[RgpdAuditExigenceCreate]

    model_config = {"from_attributes": True}
