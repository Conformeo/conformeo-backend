# app/models/processing_action.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import registry
from app.db.base_class import Base

mapper_registry = registry()

# 🔒 Protection contre redéfinition
if "processing_actions" not in Base.metadata.tables:
    processing_actions = Table(
        "processing_actions",
        Base.metadata,
        Column("processing_id", Integer, ForeignKey("processings.id", ondelete="CASCADE"), primary_key=True),
        Column("action_id", Integer, ForeignKey("gdpr_actions.id", ondelete="CASCADE"), primary_key=True),
        extend_existing=True,
    )
else:
    processing_actions = Base.metadata.tables["processing_actions"]

# ✅ Classe mappée (compatible avec les imports et ORM)
@mapper_registry.mapped
class ProcessingAction:
    __table__ = processing_actions
