"""
Table d’association many-to-many entre Processing et GdprAction.
Aucune classe déclarative nécessaire.
"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base_class import Base

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
)
