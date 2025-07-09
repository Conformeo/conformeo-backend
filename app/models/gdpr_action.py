from __future__ import annotations

from enum import Enum as PyEnum
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, UniqueConstraint, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ActionScope(str, PyEnum):
    ALL         = "ALL"
    LEGAL_BASIS = "LEGAL_BASIS"

class GdprAction(Base):
    __tablename__ = "gdpr_actions"
    __table_args__ = (
        UniqueConstraint("label", "scope", name="uq_action_label_scope"),
    )

    id      = Column(Integer, primary_key=True, index=True)
    label   = Column(String,  nullable=False)
    article = Column(String,  nullable=True)
    scope   = Column(sa.Enum(ActionScope, name="actionscope"), nullable=False)
    advice  = Column(Text,    nullable=True)       # <--- NOUVEAU
    critical= Column(Boolean, default=False)       # <--- NOUVEAU

    # Traitements liés (relation inverse)
    processings = relationship(
        "Processing",
        secondary="processing_actions",
        back_populates="actions",
    )
