from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ───── Relations ────────────────────────────────────────────
    users      = relationship(
        "User",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    checklists = relationship(
        "Checklist",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # app/models/tenant.py
    processings = relationship(
        "Processing",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    securite_controles = relationship("SecuriteControle", back_populates="societe", lazy="dynamic")



