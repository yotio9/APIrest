"""set_task_creation_date_default

Revision ID: 91c3e28a74bd
Revises: 6f72d9b341a8
Create Date: 2026-10-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "91c3e28a74bd"
down_revision: Union[str, Sequence[str], None] = "6f72d9b341a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE task SET created = CURRENT_DATE WHERE created IS NULL")
    op.alter_column(
        "task",
        "created",
        existing_type=sa.Date(),
        nullable=False,
        server_default=sa.text("CURRENT_DATE"),
    )


def downgrade() -> None:
    op.alter_column(
        "task",
        "created",
        existing_type=sa.Date(),
        nullable=True,
        server_default=None,
    )
