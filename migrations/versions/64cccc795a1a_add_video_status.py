"""add video status

Revision ID: 64cccc795a1a
Revises: 9fee34d2a6e6
Create Date: 2026-02-19
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "64cccc795a1a"
down_revision: Union[str, Sequence[str], None] = "9fee34d2a6e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Создаём enum тип в БД
    video_status_enum = sa.Enum(
        "draft",
        "published",
        name="video_status",
    )
    video_status_enum.create(op.get_bind(), checkfirst=True)

    # 2. Добавляем колонку
    op.add_column(
        "videos",
        sa.Column(
            "status",
            video_status_enum,
            nullable=False,
            server_default="draft",
        ),
    )

    # 3. (Опционально) можно убрать server_default после заполнения
    # op.alter_column("videos", "status", server_default=None)


def downgrade() -> None:
    # 1. Удаляем колонку
    op.drop_column("videos", "status")

    # 2. Удаляем enum тип
    video_status_enum = sa.Enum(
        "draft",
        "published",
        name="video_status",
    )
    video_status_enum.drop(op.get_bind(), checkfirst=True)
