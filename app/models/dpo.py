from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship


class Dpo(Base):
    __tablename__ = "dpo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
    designation_date = Column(Date, nullable=True)
    is_external = Column(Boolean, default=False)

    registers = relationship("Register", back_populates="dpo")

