# models/rgpd_audit.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class RgpdAudit(Base):
    __tablename__ = "rgpd_audits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    company_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer)
    statut = Column(String, default="EN_COURS")
    exigences = relationship("RgpdAuditExigence", back_populates="audit", cascade="all, delete-orphan")
