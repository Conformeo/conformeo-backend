from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Site(Base):
    __tablename__ = "sites"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    city    = Column(String, nullable=True)
    zipCode = Column(String, nullable=True)
    score   = Column(Integer, nullable=True)

    # One-to-Many vers contrôles, photos, documents
    controles = relationship(
        "SecuriteControle",
        back_populates="site",
        cascade="all, delete-orphan",
    )
    photos = relationship(
        "SitePhoto",
        back_populates="site",
        cascade="all, delete-orphan",
    )
    documents = relationship(
        "SiteDocument",
        back_populates="site",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pour le debug sympa
        return f"<Site id={self.id} name={self.name!r} score={self.score}>"


class SitePhoto(Base):
    __tablename__ = "site_photos"

    id      = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    url     = Column(String, nullable=False)

    site = relationship("Site", back_populates="photos")


class SiteDocument(Base):
    __tablename__ = "site_documents"

    id      = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    url     = Column(String, nullable=False)

    site = relationship("Site", back_populates="documents")
