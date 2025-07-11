from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, func
from app.db.base_class import Base

class Dpo(Base):
    __tablename__ = "rgpd_dpo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False, unique=True)  # 1 seul DPO par user/tenant
    nom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
    designation_date = Column(Date, nullable=True)
    is_external = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
