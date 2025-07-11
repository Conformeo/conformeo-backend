from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Register(Base):
    __tablename__ = "registers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nom_traitement = Column(String, nullable=False)
    finalite = Column(String)
    base_legale = Column(String)
    personnes_concernees = Column(String)
    duree_conservation = Column(String)
    dpo_id = Column(Integer, ForeignKey("dpo.id"), nullable=True)
    date_creation = Column(Date)

    user = relationship("User", back_populates="registers")
    # dpo = relationship("Dpo", back_populates="registers", foreign_keys=[dpo_id])  # <-- ENLÈVE-TEMPORAIREMENT

# ... ensuite, dans le même fichier OU dans register.py à la fin :
def setup_relationships():
    from app.models.dpo import Dpo  # Import local pour casser la boucle
    Register.dpo = relationship("Dpo", back_populates="registers", foreign_keys=[Register.dpo_id])

setup_relationships()
