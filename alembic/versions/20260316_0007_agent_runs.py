# Copyright (c) Dario Pizzolante
"""add agent run execution history table

Revision ID: 20260316_0007
Revises: 20260313_0006
Create Date: 2026-03-16 15:30:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260316_0007"
down_revision: Union[str, Sequence[str], None] = "20260313_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_runs",
        sa.Column("agent_run_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=128), nullable=False),
        sa.Column("track", sa.String(length=32), nullable=False),
        sa.Column("agent_id", sa.String(length=128), nullable=False),
        sa.Column("agent_family", sa.String(length=128), nullable=False),
        sa.Column("mode", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("workflow_id", sa.String(length=64), nullable=True),
        sa.Column("run_id", sa.String(length=64), nullable=True),
        sa.Column("step_id", sa.String(length=128), nullable=True),
        sa.Column("parent_agent_run_id", sa.String(length=64), nullable=True),
        sa.Column("trigger_event_name", sa.String(length=128), nullable=True),
        sa.Column("input_ref", sa.String(length=256), nullable=True),
        sa.Column("output_ref", sa.String(length=256), nullable=True),
        sa.Column("autonomy_class", sa.String(length=32), nullable=True),
        sa.Column("approval_class", sa.String(length=32), nullable=True),
        sa.Column("provider_used", sa.String(length=32), nullable=True),
        sa.Column("model_used", sa.String(length=128), nullable=True),
        sa.Column("routing_path", sa.String(length=128), nullable=True),
        sa.Column("fallback_mode", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("trace_ref", sa.String(length=256), nullable=True),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("agent_run_id"),
    )
    op.create_index(op.f("ix_agent_runs_agent_family"), "agent_runs", ["agent_family"], unique=False)
    op.create_index(op.f("ix_agent_runs_agent_id"), "agent_runs", ["agent_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_run_id"), "agent_runs", ["run_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_started_at"), "agent_runs", ["started_at"], unique=False)
    op.create_index(op.f("ix_agent_runs_status"), "agent_runs", ["status"], unique=False)
    op.create_index(op.f("ix_agent_runs_tenant_id"), "agent_runs", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_track"), "agent_runs", ["track"], unique=False)
    op.create_index(op.f("ix_agent_runs_workflow_id"), "agent_runs", ["workflow_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_agent_runs_workflow_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_track"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_tenant_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_status"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_started_at"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_run_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_agent_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_agent_family"), table_name="agent_runs")
    op.drop_table("agent_runs")
