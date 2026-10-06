"""create_task_table

Revision ID: 6f72d9b341a8
Revises: 0d4beacbb911
Create Date: 2026-10-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f72d9b341a8"
down_revision: Union[str, Sequence[str], None] = "0d4beacbb911"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.Column("userID", sa.Integer(), nullable=False),
        sa.Column("created", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["userID"], ["users.id"]),
    )


def downgrade() -> None:
    op.drop_table("task")
