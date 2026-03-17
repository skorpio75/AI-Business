# Copyright (c) Dario Pizzolante
"""add public lead submissions table

Revision ID: 20260318_0009
Revises: 20260316_0008
Create Date: 2026-03-18 16:40:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260318_0009"
down_revision: Union[str, Sequence[str], None] = "20260316_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "public_lead_submissions",
        sa.Column("submission_id", sa.String(length=64), nullable=False),
        sa.Column("lead_id", sa.String(length=64), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_class", sa.String(length=32), nullable=False),
        sa.Column("submission_kind", sa.String(length=32), nullable=False),
        sa.Column("materialization_status", sa.String(length=32), nullable=False),
        sa.Column("lead_status", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("company", sa.String(length=200), nullable=True),
        sa.Column("role_title", sa.String(length=160), nullable=True),
        sa.Column("service_interest", sa.String(length=128), nullable=True),
        sa.Column("challenge_summary", sa.Text(), nullable=False),
        sa.Column("preferred_timing", sa.String(length=160), nullable=True),
        sa.Column("website_path", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("submission_id"),
    )
    op.create_index(op.f("ix_public_lead_submissions_company"), "public_lead_submissions", ["company"], unique=False)
    op.create_index(op.f("ix_public_lead_submissions_email"), "public_lead_submissions", ["email"], unique=False)
    op.create_index(op.f("ix_public_lead_submissions_lead_id"), "public_lead_submissions", ["lead_id"], unique=False)
    op.create_index(
        op.f("ix_public_lead_submissions_lead_status"),
        "public_lead_submissions",
        ["lead_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_public_lead_submissions_service_interest"),
        "public_lead_submissions",
        ["service_interest"],
        unique=False,
    )
    op.create_index(
        op.f("ix_public_lead_submissions_source_class"),
        "public_lead_submissions",
        ["source_class"],
        unique=False,
    )
    op.create_index(
        op.f("ix_public_lead_submissions_submission_kind"),
        "public_lead_submissions",
        ["submission_kind"],
        unique=False,
    )
    op.create_index(
        op.f("ix_public_lead_submissions_submitted_at"),
        "public_lead_submissions",
        ["submitted_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_public_lead_submissions_submitted_at"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_submission_kind"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_source_class"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_service_interest"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_lead_status"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_lead_id"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_email"), table_name="public_lead_submissions")
    op.drop_index(op.f("ix_public_lead_submissions_company"), table_name="public_lead_submissions")
    op.drop_table("public_lead_submissions")
