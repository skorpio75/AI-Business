# Copyright (c) Dario Pizzolante
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, String, Text
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
    local_llm_invoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cloud_llm_invoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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


class AgentRunORM(Base):
    __tablename__ = "agent_runs"

    agent_run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    track: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    agent_family: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    step_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    parent_agent_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trigger_event_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    input_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    output_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    autonomy_class: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    approval_class: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    provider_used: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    routing_path: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    fallback_mode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    trace_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    error_code: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    error_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AuditEventORM(Base):
    __tablename__ = "audit_events"

    audit_event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    track: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    event_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    actor_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    step_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    agent_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    approval_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    approval_class: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    autonomy_class: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    tool_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    provider_used: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    routing_path: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    fallback_mode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trace_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    payload_ref_or_inline: Mapped[Optional[dict | str]] = mapped_column(JSON, nullable=True)
    state_diff_ref: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    error_code: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    error_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
