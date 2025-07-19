# app/models/registre.py  ─────────────────────────────────────────────────────
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Registre(Base):
    __tablename__ = "registres"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    nom_traitement       = Column(String(255), nullable=False)
    finalite             = Column(Text,        nullable=False)
    personnes_concernees = Column(Text,        nullable=True)
    categorie_donnees    = Column(Text,        nullable=True)
    base_legale          = Column(String(255), nullable=False)
    duree_conservation   = Column(String(255), nullable=False)
    mesures_securite     = Column(Text,        nullable=True)
    commentaire          = Column(Text,        nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="registres")
