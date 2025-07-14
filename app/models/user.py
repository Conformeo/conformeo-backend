from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
# from app.models.registre import Registre  # Tu peux garder ou commenter si tu as des imports circulaires

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    tenant = relationship("Tenant", back_populates="users")
    certifs = relationship("Certif", back_populates="user")
    ouvriers = relationship("Ouvrier", back_populates="user")
    securite_controles = relationship("SecuriteControle", back_populates="user", lazy="dynamic")
    registres = relationship("Registre", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
