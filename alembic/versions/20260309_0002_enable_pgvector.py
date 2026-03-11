"""enable pgvector extension

Revision ID: 20260309_0002
Revises: 20260309_0001
Create Date: 2026-03-09 00:10:00
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20260309_0002"
down_revision: Union[str, Sequence[str], None] = "20260309_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
