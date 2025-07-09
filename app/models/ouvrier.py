from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Ouvrier(Base):
    __tablename__ = "ouvriers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    date_embauche = Column(Date, nullable=True)
    poste = Column(String, nullable=True)
    formation_a_jour = Column(String, nullable=True)

    user = relationship("User", back_populates="ouvriers")
