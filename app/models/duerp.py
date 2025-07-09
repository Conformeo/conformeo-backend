# app/models/duerp.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base

class DuerpEvaluation(Base):
    __tablename__ = "duerp_evaluations"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    title = Column(String, nullable=False)
    description = Column(String)
    statut = Column(String, default="EN_COURS")
    # autres champs utiles...
