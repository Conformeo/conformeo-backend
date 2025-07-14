from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Registre(Base):
    __tablename__ = "registres"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    nom_traitement = Column(String, nullable=False)
    finalite = Column(Text, nullable=False)
    categorie_donnees = Column(Text)
    categorie_personnes = Column(Text)
    base_legale = Column(String)
    duree_conservation = Column(String)
    mesures_securite = Column(Text)
    date_creation = Column(Date)
    commentaire = Column(Text)

    # Relation vers User (back_populates)
    user = relationship("User", back_populates="registres")
