from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class GdprActionAnswer(Base):
    __tablename__ = "gdpr_action_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    audit_id = Column(Integer, ForeignKey("rgpd_audits.id", ondelete="CASCADE"), nullable=False)   # <--- NOUVEAU LIEN
    action_id = Column(Integer, ForeignKey("gdpr_actions.id", ondelete="CASCADE"), nullable=False)
    answer = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    action = relationship("GdprAction")
    audit = relationship("RgpdAudit", back_populates="answers")
