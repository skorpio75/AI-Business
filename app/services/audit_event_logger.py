from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.db.repository import insert_audit_event
from app.models.audit import AuditActorType, AuditEventName, AuditEventRecord, AuditEventStatus
from app.models.control_plane import ApprovalClass, AutonomyClass
from app.models.tool_profiles import NormalizedToolId


@dataclass(frozen=True)
class AuditActor:
    actor_type: AuditActorType
    actor_id: str


def actor(*, actor_type: AuditActorType, actor_id: str) -> AuditActor:
    return AuditActor(actor_type=actor_type, actor_id=actor_id)


def record_audit_event(
    db: Session,
    *,
    event_name: AuditEventName,
    entity_type: str,
    entity_id: str,
    event_actor: AuditActor,
    status: AuditEventStatus,
    occurred_at: datetime | None = None,
    workflow_id: str | None = None,
    run_id: str | None = None,
    step_id: str | None = None,
    agent_run_id: str | None = None,
    approval_id: str | None = None,
    approval_class: ApprovalClass | None = None,
    autonomy_class: AutonomyClass | None = None,
    tool_id: NormalizedToolId | None = None,
    provider_used: str | None = None,
    model_used: str | None = None,
    routing_path: str | None = None,
    fallback_mode: str | None = None,
    trace_ref: str | None = None,
    payload_ref_or_inline: dict | str | None = None,
    state_diff_ref: str | None = None,
    error_code: str | None = None,
    error_detail: str | None = None,
) -> AuditEventRecord:
    settings = get_settings()
    record = AuditEventRecord(
        audit_event_id=str(uuid4()),
        tenant_id=settings.tenant_id,
        track=settings.primary_track,
        occurred_at=occurred_at or datetime.now(timezone.utc),
        event_name=event_name,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_type=event_actor.actor_type,
        actor_id=event_actor.actor_id,
        status=status,
        workflow_id=workflow_id,
        run_id=run_id,
        step_id=step_id,
        agent_run_id=agent_run_id,
        approval_id=approval_id,
        approval_class=approval_class,
        autonomy_class=autonomy_class,
        tool_id=tool_id,
        provider_used=provider_used,
        model_used=model_used,
        routing_path=routing_path or provider_used,
        fallback_mode=fallback_mode or _infer_fallback_mode(provider_used),
        trace_ref=trace_ref,
        payload_ref_or_inline=payload_ref_or_inline,
        state_diff_ref=state_diff_ref,
        error_code=error_code,
        error_detail=_clean_detail(error_detail),
    )
    insert_audit_event(db, record)
    return record


def _infer_fallback_mode(provider_used: str | None) -> str | None:
    if provider_used == "fallback-rule":
        return "rule_based"
    return None


def _clean_detail(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split())[:400]
