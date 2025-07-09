# … imports …
from sqlalchemy.orm import relationship

class Certification(Base):
    __tablename__ = "certifications"

    id      = Column(Integer, primary_key=True)
    name    = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # back-ref vers l’utilisateur
    user = relationship("User", back_populates="certifs")
