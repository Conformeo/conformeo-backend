"""add exigence_id to rgpd_audit_exigences

Revision ID: 682a5ec9e01a
Revises: 326b8132f1f3
Create Date: 2025-07-18 18:30:12.442895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '682a5ec9e01a'
down_revision: Union[str, None] = '326b8132f1f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Dans la révision générée
def upgrade():
    op.add_column(
        "rgpd_audit_exigences",
        sa.Column("exigence_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        "fk_rgae_exigence",
        "rgpd_audit_exigences",
        "rgpd_exigences",
        ["exigence_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
