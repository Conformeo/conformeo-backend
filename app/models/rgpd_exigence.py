# models/rgpd_exigence.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class RgpdExigence(Base):
    __tablename__ = "rgpd_exigences"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    article = Column(String)
    critical = Column(Boolean, default=False)
    advice = Column(String)
