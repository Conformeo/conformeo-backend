# app/models/checklist_item.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.session import Base  # ← change ici (plus depuis app.db.base)


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(
        Integer,
        ForeignKey("checklists.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    label = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
