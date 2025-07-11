# app/models/obligation.py

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.db.base_class import Base

class Obligation(Base):
    __tablename__ = "obligation"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    last_update = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
