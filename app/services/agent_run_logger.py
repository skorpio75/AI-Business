# Copyright (c) Dario Pizzolante
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.db.repository import insert_agent_run
from app.models.agent_contract import AgentContract
from app.models.audit import AgentRunMode, AgentRunRecord, AgentRunStatus
from app.models.control_plane import ApprovalClass, AutonomyClass, NormalizedEventName


@dataclass(frozen=True)
class AgentRunSubject:
    agent_id: str
    agent_family: str
    mode: AgentRunMode
    autonomy_class: AutonomyClass | None = None
    approval_class: ApprovalClass | None = None


def subject_from_agent(agent: AgentContract, *, mode: AgentRunMode) -> AgentRunSubject:
    return AgentRunSubject(
        agent_id=agent.agent_id,
        agent_family=agent.family_id or agent.agent_id,
        mode=mode,
        autonomy_class=agent.autonomy_class,
        approval_class=agent.approval_class,
    )


def subject_from_identity(
    *,
    agent_id: str,
    agent_family: str,
    mode: AgentRunMode,
    autonomy_class: AutonomyClass | None = None,
    approval_class: ApprovalClass | None = None,
) -> AgentRunSubject:
    return AgentRunSubject(
        agent_id=agent_id,
        agent_family=agent_family,
        mode=mode,
        autonomy_class=autonomy_class,
        approval_class=approval_class,
    )


def record_agent_run(
    db: Session,
    *,
    subject: AgentRunSubject,
    status: AgentRunStatus,
    started_at: datetime,
    ended_at: datetime | None = None,
    workflow_id: str | None = None,
    run_id: str | None = None,
    step_id: str | None = None,
    trigger_event_name: NormalizedEventName | None = None,
    input_ref: str | None = None,
    output_ref: str | None = None,
    provider_used: str | None = None,
    model_used: str | None = None,
    routing_path: str | None = None,
    fallback_mode: str | None = None,
    confidence: float | None = None,
    trace_ref: str | None = None,
    error_code: str | None = None,
    error_detail: str | None = None,
) -> AgentRunRecord:
    settings = get_settings()
    record = AgentRunRecord(
        agent_run_id=str(uuid4()),
        tenant_id=settings.tenant_id,
        track=settings.primary_track,
        agent_id=subject.agent_id,
        agent_family=subject.agent_family,
        mode=subject.mode,
        status=status,
        started_at=started_at,
        ended_at=ended_at,
        workflow_id=workflow_id,
        run_id=run_id,
        step_id=step_id,
        trigger_event_name=trigger_event_name,
        input_ref=input_ref,
        output_ref=output_ref,
        autonomy_class=subject.autonomy_class,
        approval_class=subject.approval_class,
        provider_used=provider_used,
        model_used=model_used,
        routing_path=routing_path or provider_used,
        fallback_mode=fallback_mode or _infer_fallback_mode(provider_used),
        confidence=confidence,
        trace_ref=trace_ref,
        error_code=error_code,
        error_detail=_clean_detail(error_detail),
    )
    insert_agent_run(db, record)
    return record


def _infer_fallback_mode(provider_used: str | None) -> str | None:
    if provider_used == "fallback-rule":
        return "rule_based"
    return None


def _clean_detail(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split())[:400]
