from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # user relation
    users = relationship("User", back_populates="tenant")
    # checklist relation
    checklists = relationship(
        "Checklist", back_populates="tenant", cascade="all, delete-orphan"
    )
