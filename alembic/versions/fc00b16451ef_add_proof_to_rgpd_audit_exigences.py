"""add proof to rgpd_audit_exigences

Revision ID: fc00b16451ef
Revises: 682a5ec9e01a
Create Date: 2025-07-18 18:35:53.471472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc00b16451ef'
down_revision: Union[str, None] = '682a5ec9e01a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "rgpd_audit_exigences",
        sa.Column("proof", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
