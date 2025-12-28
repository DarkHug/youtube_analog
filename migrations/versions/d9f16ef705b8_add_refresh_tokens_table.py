"""add refresh tokens table

Revision ID: d9f16ef705b8
Revises: 1c5a3787216c
Create Date: 2025-12-24 16:40:18.518654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd9f16ef705b8'
down_revision: Union[str, Sequence[str], None] = '1c5a3787216c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "revoked",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.create_index(
        "ix_refresh_tokens_token_hash",
        "refresh_tokens",
        ["token_hash"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_refresh_tokens_token_hash",
        table_name="refresh_tokens",
    )
    op.drop_table("refresh_tokens")
