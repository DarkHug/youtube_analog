"""add server default to created_at

Revision ID: c265007153aa
Revises: c16e36407055
Create Date: 2025-12-19 22:12:08.932322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c265007153aa'
down_revision: Union[str, Sequence[str], None] = 'c16e36407055'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.func.now(),
        nullable=False,
        existing_type=sa.DateTime(timezone=True),
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
        nullable=True,
        existing_type=sa.DateTime(timezone=True),
    )
