from enum import Enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

from app.schemas.gdpr_action import GdprActionRead  # 👈 nouvel import


# ────────────────────────────
#  Enums
# ────────────────────────────
class LegalBasisEnum(str, Enum):
    CONSENT             = "Consentement"
    CONTRACT            = "Contrat"
    LEGAL_OBLIGATION    = "Obligation légale"
    LEGITIMATE_INTEREST = "Intérêt légitime"


# ────────────────────────────
#  Schémas de base
# ────────────────────────────
class ProcessingBase(BaseModel):
    name            : str               = Field(..., example="Gestion RH")
    purpose         : str               = Field(..., example="Gestion des salariés")
    legal_basis     : LegalBasisEnum    = Field(..., example="Contrat")
    data_subjects   : List[str]         = Field(default_factory=lambda: ["Salariés"])
    data_categories : List[str]         = Field(..., example=["Nom", "Adresse", "IBAN"])
    retention_period: Optional[int]     = Field(None, description="Durée (mois)", ge=0)
    dpo_contact     : Optional[EmailStr] = None

# ⚙️  accepte 'contrat', 'Contrat', 'CONTRAT', etc.
    @field_validator("legal_basis", mode="before")
    @classmethod
    def normalize_legal_basis(cls, v):
        if isinstance(v, str):
            v_norm = v.strip().lower()
            mapping = {
                "consentement": LegalBasisEnum.CONSENT,
                "contrat": LegalBasisEnum.CONTRACT,
                "obligation légale": LegalBasisEnum.LEGAL_OBLIGATION,
                "obligation legale": LegalBasisEnum.LEGAL_OBLIGATION,
                "intérêt légitime": LegalBasisEnum.LEGITIMATE_INTEREST,
                "interet legitime": LegalBasisEnum.LEGITIMATE_INTEREST,
            }
            if v_norm in mapping:
                return mapping[v_norm]
        return v  # laisser Pydantic gérer sinon
# ────────────────────────────
#  Création
# ────────────────────────────
class ProcessingCreate(ProcessingBase):
    tenant_id: int = Field(..., ge=1, example=1)


# ────────────────────────────
#  Mise à jour partielle
# ────────────────────────────
class ProcessingUpdate(BaseModel):
    name            : Optional[str]            = None
    purpose         : Optional[str]            = None
    legal_basis     : Optional[LegalBasisEnum] = None
    data_subjects   : Optional[List[str]]      = None
    data_categories : Optional[List[str]]      = None
    retention_period: Optional[int]            = Field(None, ge=0)
    dpo_contact     : Optional[EmailStr]       = None


# ────────────────────────────
#  Retour API
# ────────────────────────────
class ProcessingOut(ProcessingBase):
    id         : int
    tenant_id  : int
    created_at : datetime
    actions    : list[GdprActionRead] = []          # 👈

    model_config = ConfigDict(from_attributes=True)



