from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class RgpdRequest(Base):
    __tablename__ = "rgpd_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    type = Column(String, nullable=False)  # ex: "Accès", "Effacement", "Rectification", etc.
    message = Column(String, nullable=True)
    status = Column(String, default="Nouveau")  # "Nouveau", "En cours", "Traité", "Refusé"
    date_submitted = Column(DateTime, default=datetime.utcnow)
    date_closed = Column(DateTime, nullable=True)
    note = Column(String, nullable=True)  # Note du DPO

    user = relationship("User")
