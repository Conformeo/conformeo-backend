from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class SecuriteControle(Base):
    __tablename__ = "securite_controles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="SET NULL"), nullable=True, index=True)
    societe_id = Column(Integer, ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True, index=True)  # société/tenant

    date_controle = Column(Date, nullable=True)
    type = Column(String, nullable=False)
    nb_nc = Column(Integer, default=0)
    rapport = Column(String, nullable=True)

    # Utilise le chemin sous forme de **string** pour éviter les problèmes de cycle d'import
    user = relationship("User", back_populates="securite_controles", lazy="joined")
    site = relationship("Site", back_populates="controles", lazy="joined")
    societe = relationship("Tenant", back_populates="securite_controles", lazy="joined")
