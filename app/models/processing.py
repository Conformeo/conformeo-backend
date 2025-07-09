import enum
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, func,
    Enum as SAEnum
)
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.m2m import processing_actions 

# ──────────────────────────────────────────────────────────
#  Enum RGPD – valeurs FR stockées en base
# ──────────────────────────────────────────────────────────
class LegalBasisEnum(str, enum.Enum):
    CONSENT             = "Consentement"
    CONTRACT            = "Contrat"
    LEGAL_OBLIGATION    = "Obligation légale"
    LEGITIMATE_INTEREST = "Intérêt légitime"


def _enum_values(enum_cls):
    """Renvoie la liste des .value pour la création du type ENUM SQL."""
    return [m.value for m in enum_cls]


class Processing(Base):
    """Modèle SQLAlchemy pour un traitement RGPD."""
    __tablename__ = "processings"

    # ─────── Clés
    id        = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ─────── Champs métier
    name        = Column(String, nullable=False)
    purpose     = Column(String, nullable=False)
    legal_basis = Column(
        SAEnum(
            LegalBasisEnum,
            name="legal_basis_enum",
            values_callable=_enum_values,   # stocke les libellés FR
            native_enum=True,
        ),
        nullable=False,
    )
    data_subjects    = Column(JSON, nullable=False, default=list)
    data_categories  = Column(JSON, nullable=False, default=list)
    retention_period = Column(Integer)        # durée en mois
    dpo_contact      = Column(String)

    # ─────── Méta
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ─────── Relations
    # Relations
    tenant = relationship("Tenant", back_populates="processings")

    actions = relationship(
        "GdprAction",
        secondary="processing_actions",   # ← chaîne, plus de variable Python
        back_populates="processings",
        cascade="all, delete",
    )