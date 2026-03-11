from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkflowRunORM(Base):
    __tablename__ = "workflow_runs"

    workflow_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    approval_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    intent: Mapped[str] = mapped_column(String(128), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    draft_reply: Mapped[str] = mapped_column(Text, nullable=False)
    provider_used: Mapped[str] = mapped_column(String(32), nullable=False)
    model_used: Mapped[str] = mapped_column(String(128), nullable=False)
    escalation_reason: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    approval_status: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    send_status: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    source_provider: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    source_message_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)


class ApprovalORM(Base):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    workflow_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sender: Mapped[str] = mapped_column(String(320), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    draft_reply: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    decision_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_account_id: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    source_message_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    source_thread_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    source_provider: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    send_status: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    send_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkflowStateSnapshotORM(Base):
    __tablename__ = "workflow_state_snapshots"

    workflow_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    workflow_type: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    state_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
