"""add default now() to users.created_at

Revision ID: 1c5a3787216c
Revises: c265007153aa
Create Date: 2025-12-19 22:16:21.989680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c5a3787216c'
down_revision: Union[str, Sequence[str], None] = 'c265007153aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.text("now()"),
        nullable=False,
        existing_type=sa.DateTime(timezone=True),
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
