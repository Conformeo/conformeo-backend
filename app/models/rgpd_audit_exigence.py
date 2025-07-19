# app/models/rgpd_audit_exigence.py
from sqlalchemy import (
    Column,
    Integer,
    Text,          # ←  ICI : l’import manquant
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.rgpd_audit_exigence import AnswerEnum   # adapte le chemin si besoin


class RgpdAuditExigence(Base):
    __tablename__ = "rgpd_audit_exigences"

    id           = Column(Integer, primary_key=True, index=True)
    audit_id     = Column(Integer, ForeignKey("rgpd_audits.id"), nullable=False)
    exigence_id  = Column(Integer, ForeignKey("rgpd_exigences.id"), nullable=False)
    label        = Column(Text, nullable=False)
    answer       = Column(Enum(AnswerEnum), nullable=False)
    comment      = Column(Text)
    proof        = Column(Text)          # ← nouvelle colonne optionnelle

    audit    = relationship("RgpdAudit", back_populates="exigences")
    exigence = relationship("RgpdExigence")
