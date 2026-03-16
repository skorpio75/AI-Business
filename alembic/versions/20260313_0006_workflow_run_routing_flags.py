# Copyright (c) Dario Pizzolante
"""add workflow run routing invocation flags

Revision ID: 20260313_0006
Revises: 20260311_0005
Create Date: 2026-03-13 11:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260313_0006"
down_revision: Union[str, Sequence[str], None] = "20260311_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workflow_runs",
        sa.Column("local_llm_invoked", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "workflow_runs",
        sa.Column("cloud_llm_invoked", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.execute(
        """
        UPDATE workflow_runs
        SET
            local_llm_invoked = CASE
                WHEN provider_used IN ('local', 'cloud') THEN TRUE
                ELSE FALSE
            END,
            cloud_llm_invoked = CASE
                WHEN provider_used = 'cloud' THEN TRUE
                ELSE FALSE
            END
        """
    )

    op.alter_column("workflow_runs", "local_llm_invoked", server_default=None)
    op.alter_column("workflow_runs", "cloud_llm_invoked", server_default=None)


def downgrade() -> None:
    op.drop_column("workflow_runs", "cloud_llm_invoked")
    op.drop_column("workflow_runs", "local_llm_invoked")
