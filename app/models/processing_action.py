# app/models/processing_action.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base_class import Base

if "processing_actions" not in Base.metadata.tables:   # ✅ protection idempotente
    processing_actions = Table(
        "processing_actions",
        Base.metadata,
        Column(
            "processing_id",
            Integer,
            ForeignKey("processings.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        Column(
            "action_id",
            Integer,
            ForeignKey("gdpr_actions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        extend_existing=True,   # ← tolère un 2ᵉ passage éventuel
    )
else:
    processing_actions = Base.metadata.tables["processing_actions"]
