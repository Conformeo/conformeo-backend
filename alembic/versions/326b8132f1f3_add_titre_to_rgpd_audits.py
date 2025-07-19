"""add titre to rgpd_audits

Revision ID: 326b8132f1f3
Revises: 9aacd3e34108
Create Date: 2025-07-18 18:10:36.212301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '326b8132f1f3'
down_revision: Union[str, None] = '9aacd3e34108'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "rgpd_audits",
        sa.Column("titre", sa.String(length=255), nullable=True),
    )

def downgrade() -> None:
    op.drop_column("rgpd_audits", "titre")
