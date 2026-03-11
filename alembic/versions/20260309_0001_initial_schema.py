"""initial schema

Revision ID: 20260309_0001
Revises:
Create Date: 2026-03-09 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260309_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "approvals",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workflow_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sender", sa.String(length=320), nullable=False),
        sa.Column("subject", sa.String(length=500), nullable=False),
        sa.Column("draft_reply", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_approvals_status", "approvals", ["status"], unique=False)
    op.create_index("ix_approvals_workflow_id", "approvals", ["workflow_id"], unique=False)

    op.create_table(
        "workflow_runs",
        sa.Column("workflow_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("approval_id", sa.String(length=64), nullable=False),
        sa.Column("intent", sa.String(length=128), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("draft_reply", sa.Text(), nullable=False),
        sa.Column("provider_used", sa.String(length=32), nullable=False),
        sa.Column("model_used", sa.String(length=128), nullable=False),
        sa.Column("escalation_reason", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("workflow_id"),
    )
    op.create_index("ix_workflow_runs_approval_id", "workflow_runs", ["approval_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_workflow_runs_approval_id", table_name="workflow_runs")
    op.drop_table("workflow_runs")
    op.drop_index("ix_approvals_workflow_id", table_name="approvals")
    op.drop_index("ix_approvals_status", table_name="approvals")
    op.drop_table("approvals")
