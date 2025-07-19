from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class RgpdAudit(Base):
    __tablename__ = "rgpd_audits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    statut = Column(String, default="EN_COURS", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    score = Column(Integer, nullable=True)
    titre = Column(String(255), nullable=False)

    # Champs pour le dashboard
    conforme = Column(Integer, default=0, nullable=False)
    non_conforme = Column(Integer, default=0, nullable=False)
    critical_ko = Column(JSON, default=list, nullable=False)

    # Relation avec les exigences RGPD (One to Many)
    exigences = relationship(
        "RgpdAuditExigence",
        back_populates="audit",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self):
        return (
            f"<RgpdAudit id={self.id} user_id={self.user_id} "
            f"score={self.score} conforme={self.conforme} non_conforme={self.non_conforme}>"
        )
