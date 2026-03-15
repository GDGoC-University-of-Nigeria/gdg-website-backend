"""add is_active column to users

Revision ID: c8f4a1d2e3ab
Revises: b3d2f9a4c512
Create Date: 2026-03-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c8f4a1d2e3ab"
down_revision: Union[str, Sequence[str], None] = "b3d2f9a4c512"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.add_column(
    "users",
    sa.Column(
      "is_active",
      sa.Boolean(),
      nullable=False,
      server_default=sa.text("true"),
    ),
  )


def downgrade() -> None:
  op.drop_column("users", "is_active")

