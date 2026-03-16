# Copyright (c) Dario Pizzolante
"""knowledge documents with pgvector embeddings

Revision ID: 20260310_0003
Revises: 20260309_0002
Create Date: 2026-03-10 00:10:00
"""

from typing import Sequence, Union

from alembic import op


revision: str = "20260310_0003"
down_revision: Union[str, Sequence[str], None] = "20260309_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE knowledge_documents (
            id BIGSERIAL PRIMARY KEY,
            source_path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_length INTEGER NOT NULL,
            embedding VECTOR(8) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS knowledge_documents")
