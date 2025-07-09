# models/rgpd_audit_exigence.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class RgpdAuditExigence(Base):
    __tablename__ = "rgpd_audit_exigences"
    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("rgpd_audits.id", ondelete="CASCADE"))
    exigence_id = Column(Integer, ForeignKey("rgpd_exigences.id", ondelete="CASCADE"))
    answer = Column(String)
    critical = Column(Boolean, default=False)
    advice = Column(String)
    audit = relationship("RgpdAudit", back_populates="exigences")
    exigence = relationship("RgpdExigence")

