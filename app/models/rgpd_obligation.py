# app/models/rgpd_obligation.py
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.db.base_class import Base

class RgpdObligation(Base):
    __tablename__ = "rgpd_obligation"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    label = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    last_update = Column(Date, nullable=True)
