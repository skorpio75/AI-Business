# Copyright (c) Dario Pizzolante
"""workflow state snapshots

Revision ID: 20260310_0004
Revises: 20260310_0003
Create Date: 2026-03-10 00:20:00
"""

from typing import Sequence, Union

from alembic import op


revision: str = "20260310_0004"
down_revision: Union[str, Sequence[str], None] = "20260310_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE workflow_state_snapshots (
            workflow_id VARCHAR(64) PRIMARY KEY,
            workflow_type VARCHAR(128) NOT NULL,
            status VARCHAR(32) NOT NULL,
            state_json JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS workflow_state_snapshots")
