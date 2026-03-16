# Copyright (c) Dario Pizzolante
"""add audit events table

Revision ID: 20260316_0008
Revises: 20260316_0007
Create Date: 2026-03-16 17:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260316_0008"
down_revision: Union[str, Sequence[str], None] = "20260316_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audit_events",
        sa.Column("audit_event_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=128), nullable=False),
        sa.Column("track", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_name", sa.String(length=128), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("workflow_id", sa.String(length=64), nullable=True),
        sa.Column("run_id", sa.String(length=64), nullable=True),
        sa.Column("step_id", sa.String(length=128), nullable=True),
        sa.Column("agent_run_id", sa.String(length=64), nullable=True),
        sa.Column("approval_id", sa.String(length=64), nullable=True),
        sa.Column("approval_class", sa.String(length=32), nullable=True),
        sa.Column("autonomy_class", sa.String(length=32), nullable=True),
        sa.Column("tool_id", sa.String(length=128), nullable=True),
        sa.Column("provider_used", sa.String(length=32), nullable=True),
        sa.Column("model_used", sa.String(length=128), nullable=True),
        sa.Column("routing_path", sa.String(length=128), nullable=True),
        sa.Column("fallback_mode", sa.String(length=64), nullable=True),
        sa.Column("trace_ref", sa.String(length=256), nullable=True),
        sa.Column("payload_ref_or_inline", sa.JSON(), nullable=True),
        sa.Column("state_diff_ref", sa.String(length=256), nullable=True),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("audit_event_id"),
    )
    op.create_index(op.f("ix_audit_events_actor_id"), "audit_events", ["actor_id"], unique=False)
    op.create_index(op.f("ix_audit_events_actor_type"), "audit_events", ["actor_type"], unique=False)
    op.create_index(op.f("ix_audit_events_agent_run_id"), "audit_events", ["agent_run_id"], unique=False)
    op.create_index(op.f("ix_audit_events_approval_id"), "audit_events", ["approval_id"], unique=False)
    op.create_index(op.f("ix_audit_events_entity_id"), "audit_events", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_events_entity_type"), "audit_events", ["entity_type"], unique=False)
    op.create_index(op.f("ix_audit_events_event_name"), "audit_events", ["event_name"], unique=False)
    op.create_index(op.f("ix_audit_events_occurred_at"), "audit_events", ["occurred_at"], unique=False)
    op.create_index(op.f("ix_audit_events_run_id"), "audit_events", ["run_id"], unique=False)
    op.create_index(op.f("ix_audit_events_status"), "audit_events", ["status"], unique=False)
    op.create_index(op.f("ix_audit_events_tenant_id"), "audit_events", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_audit_events_track"), "audit_events", ["track"], unique=False)
    op.create_index(op.f("ix_audit_events_workflow_id"), "audit_events", ["workflow_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_events_workflow_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_track"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_tenant_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_status"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_run_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_occurred_at"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_event_name"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_entity_type"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_entity_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_approval_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_agent_run_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_actor_type"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_actor_id"), table_name="audit_events")
    op.drop_table("audit_events")
