from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Certif(Base):
    __tablename__ = "certifs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    label = Column(String, nullable=False)
    date_obtention = Column(Date, nullable=True)
    date_expiration = Column(Date, nullable=True)
    organisme = Column(String, nullable=True)

    user = relationship("User", back_populates="certifs")
