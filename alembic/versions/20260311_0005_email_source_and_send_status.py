# Copyright (c) Dario Pizzolante
"""add email source metadata and send status tracking

Revision ID: 20260311_0005
Revises: 20260310_0004
Create Date: 2026-03-11 00:05:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260311_0005"
down_revision: Union[str, Sequence[str], None] = "20260310_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("approvals", sa.Column("source_account_id", sa.String(length=320), nullable=True))
    op.add_column("approvals", sa.Column("source_message_id", sa.String(length=256), nullable=True))
    op.add_column("approvals", sa.Column("source_thread_id", sa.String(length=256), nullable=True))
    op.add_column("approvals", sa.Column("source_provider", sa.String(length=64), nullable=True))
    op.add_column("approvals", sa.Column("send_status", sa.String(length=32), nullable=True))
    op.add_column("approvals", sa.Column("send_detail", sa.Text(), nullable=True))
    op.add_column("approvals", sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True))

    op.add_column("workflow_runs", sa.Column("approval_status", sa.String(length=32), nullable=True))
    op.add_column("workflow_runs", sa.Column("send_status", sa.String(length=32), nullable=True))
    op.add_column("workflow_runs", sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("workflow_runs", sa.Column("source_provider", sa.String(length=64), nullable=True))
    op.add_column("workflow_runs", sa.Column("source_message_id", sa.String(length=256), nullable=True))


def downgrade() -> None:
    op.drop_column("workflow_runs", "source_message_id")
    op.drop_column("workflow_runs", "source_provider")
    op.drop_column("workflow_runs", "sent_at")
    op.drop_column("workflow_runs", "send_status")
    op.drop_column("workflow_runs", "approval_status")

    op.drop_column("approvals", "sent_at")
    op.drop_column("approvals", "send_detail")
    op.drop_column("approvals", "send_status")
    op.drop_column("approvals", "source_provider")
    op.drop_column("approvals", "source_thread_id")
    op.drop_column("approvals", "source_message_id")
    op.drop_column("approvals", "source_account_id")
