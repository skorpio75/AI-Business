from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.db.models import AgentRunORM, ApprovalORM, AuditEventORM, WorkflowRunORM, WorkflowStateSnapshotORM
from app.models.audit import AgentRunRecord, AuditEventRecord
from app.models.schemas import ApprovalItem, EmailWorkflowResponse
from app.models.workflow_state import WorkflowState


def insert_workflow_run(db: Session, run: EmailWorkflowResponse) -> None:
    db.add(
        WorkflowRunORM(
            workflow_id=run.workflow_id,
            status=run.status,
            approval_id=run.approval_id,
            intent=run.intent,
            confidence=run.confidence,
            draft_reply=run.draft_reply,
            provider_used=run.provider_used,
            model_used=run.model_used,
            local_llm_invoked=run.local_llm_invoked,
            cloud_llm_invoked=run.cloud_llm_invoked,
            escalation_reason=run.escalation_reason,
            approval_status=run.approval_status,
            send_status=run.send_status,
            sent_at=run.sent_at,
            source_provider=run.source_provider,
            source_message_id=run.source_message_id,
        )
    )


def insert_approval(db: Session, item: ApprovalItem) -> None:
    db.add(
        ApprovalORM(
            id=item.id,
            workflow_id=item.workflow_id,
            created_at=item.created_at,
            sender=item.sender,
            subject=item.subject,
            draft_reply=item.draft_reply,
            status=item.status,
            decision_note=item.decision_note,
            source_account_id=item.source_account_id,
            source_message_id=item.source_message_id,
            source_thread_id=item.source_thread_id,
            source_provider=item.source_provider,
            send_status=item.send_status,
            send_detail=item.send_detail,
            sent_at=item.sent_at,
        )
    )


def insert_agent_run(db: Session, item: AgentRunRecord) -> None:
    db.add(
        AgentRunORM(
            agent_run_id=item.agent_run_id,
            tenant_id=item.tenant_id,
            track=item.track,
            agent_id=item.agent_id,
            agent_family=item.agent_family,
            mode=item.mode,
            status=item.status,
            started_at=item.started_at,
            ended_at=item.ended_at,
            workflow_id=item.workflow_id,
            run_id=item.run_id,
            step_id=item.step_id,
            parent_agent_run_id=item.parent_agent_run_id,
            trigger_event_name=item.trigger_event_name,
            input_ref=item.input_ref,
            output_ref=item.output_ref,
            autonomy_class=item.autonomy_class,
            approval_class=item.approval_class,
            provider_used=item.provider_used,
            model_used=item.model_used,
            routing_path=item.routing_path,
            fallback_mode=item.fallback_mode,
            confidence=item.confidence,
            trace_ref=item.trace_ref,
            error_code=item.error_code,
            error_detail=item.error_detail,
        )
    )


def insert_audit_event(db: Session, item: AuditEventRecord) -> None:
    db.add(
        AuditEventORM(
            audit_event_id=item.audit_event_id,
            tenant_id=item.tenant_id,
            track=item.track,
            occurred_at=item.occurred_at,
            event_name=item.event_name,
            entity_type=item.entity_type,
            entity_id=item.entity_id,
            actor_type=item.actor_type,
            actor_id=item.actor_id,
            status=item.status,
            workflow_id=item.workflow_id,
            run_id=item.run_id,
            step_id=item.step_id,
            agent_run_id=item.agent_run_id,
            approval_id=item.approval_id,
            approval_class=item.approval_class,
            autonomy_class=item.autonomy_class,
            tool_id=item.tool_id,
            provider_used=item.provider_used,
            model_used=item.model_used,
            routing_path=item.routing_path,
            fallback_mode=item.fallback_mode,
            trace_ref=item.trace_ref,
            payload_ref_or_inline=item.payload_ref_or_inline,
            state_diff_ref=item.state_diff_ref,
            error_code=item.error_code,
            error_detail=item.error_detail,
        )
    )


def list_workflow_runs(db: Session) -> list[EmailWorkflowResponse]:
    rows = db.execute(select(WorkflowRunORM)).scalars().all()
    snapshots = {
        snapshot.workflow_id: snapshot
        for snapshot in db.execute(select(WorkflowStateSnapshotORM)).scalars().all()
    }
    results: list[EmailWorkflowResponse] = []
    for row in rows:
        response = EmailWorkflowResponse.model_validate(row)
        snapshot = snapshots.get(row.workflow_id)
        outputs = snapshot.state_json.get("outputs") if snapshot and isinstance(snapshot.state_json, dict) else None
        if isinstance(outputs, dict):
            response = response.model_copy(
                update={
                    "llm_diagnostic_code": outputs.get("llm_diagnostic_code"),
                    "llm_diagnostic_detail": outputs.get("llm_diagnostic_detail"),
                }
            )
        results.append(response)
    return results


def list_agent_runs(db: Session, *, workflow_id: str | None = None) -> list[AgentRunRecord]:
    query = select(AgentRunORM).order_by(AgentRunORM.started_at, AgentRunORM.agent_run_id)
    if workflow_id is not None:
        query = query.where(AgentRunORM.workflow_id == workflow_id)
    rows = db.execute(query).scalars().all()
    return [AgentRunRecord.model_validate(row) for row in rows]


def get_workflow_run(db: Session, workflow_id: str) -> EmailWorkflowResponse | None:
    row = db.get(WorkflowRunORM, workflow_id)
    if row is None:
        return None
    return EmailWorkflowResponse.model_validate(row)


def get_approval_by_workflow_id(db: Session, workflow_id: str) -> ApprovalItem | None:
    row = db.execute(select(ApprovalORM).where(ApprovalORM.workflow_id == workflow_id)).scalars().first()
    if row is None:
        return None
    return ApprovalItem.model_validate(row)


def list_agent_runs_for_agent(
    db: Session,
    *,
    agent_id: str,
    limit: int | None = None,
) -> list[AgentRunRecord]:
    query = select(AgentRunORM).where(AgentRunORM.agent_id == agent_id).order_by(AgentRunORM.started_at.desc())
    if limit is not None:
        query = query.limit(limit)
    rows = db.execute(query).scalars().all()
    return [AgentRunRecord.model_validate(row) for row in rows]


def list_audit_events(
    db: Session,
    *,
    workflow_id: str | None = None,
    approval_id: str | None = None,
    agent_run_ids: list[str] | None = None,
) -> list[AuditEventRecord]:
    query = select(AuditEventORM).order_by(AuditEventORM.occurred_at, AuditEventORM.audit_event_id)
    if workflow_id is not None:
        query = query.where(AuditEventORM.workflow_id == workflow_id)
    if approval_id is not None:
        query = query.where(AuditEventORM.approval_id == approval_id)
    if agent_run_ids is not None:
        if not agent_run_ids:
            return []
        query = query.where(AuditEventORM.agent_run_id.in_(agent_run_ids))
    rows = db.execute(query).scalars().all()
    return [AuditEventRecord.model_validate(row) for row in rows]


def list_pending_approvals(db: Session) -> list[ApprovalItem]:
    rows = db.execute(select(ApprovalORM).where(ApprovalORM.status == "pending")).scalars().all()
    return [ApprovalItem.model_validate(row) for row in rows]


def get_approval(db: Session, approval_id: str) -> Optional[ApprovalItem]:
    row = db.get(ApprovalORM, approval_id)
    if row is None:
        return None
    return ApprovalItem.model_validate(row)


def upsert_approval(db: Session, item: ApprovalItem) -> ApprovalItem:
    row = db.get(ApprovalORM, item.id)
    if row is None:
        row = ApprovalORM(
            id=item.id,
            workflow_id=item.workflow_id,
            created_at=item.created_at,
            sender=item.sender,
            subject=item.subject,
            draft_reply=item.draft_reply,
            status=item.status,
            decision_note=item.decision_note,
            source_account_id=item.source_account_id,
            source_message_id=item.source_message_id,
            source_thread_id=item.source_thread_id,
            source_provider=item.source_provider,
            send_status=item.send_status,
            send_detail=item.send_detail,
            sent_at=item.sent_at,
        )
        db.add(row)
    else:
        row.draft_reply = item.draft_reply
        row.status = item.status
        row.decision_note = item.decision_note
        row.source_account_id = item.source_account_id
        row.source_message_id = item.source_message_id
        row.source_thread_id = item.source_thread_id
        row.source_provider = item.source_provider
        row.send_status = item.send_status
        row.send_detail = item.send_detail
        row.sent_at = item.sent_at
    return ApprovalItem.model_validate(row)


def update_workflow_run_resolution(
    db: Session,
    *,
    workflow_id: str,
    status: str,
    approval_status: str,
    send_status: str,
    sent_at: datetime | None = None,
) -> EmailWorkflowResponse | None:
    row = db.get(WorkflowRunORM, workflow_id)
    if row is None:
        return None
    row.status = status
    row.approval_status = approval_status
    row.send_status = send_status
    row.sent_at = sent_at
    return EmailWorkflowResponse.model_validate(row)


def upsert_workflow_state(db: Session, state: WorkflowState) -> WorkflowState:
    row = db.get(WorkflowStateSnapshotORM, state.workflow_id)
    payload = state.model_dump(mode="json")
    now = datetime.now(timezone.utc)
    if row is None:
        row = WorkflowStateSnapshotORM(
            workflow_id=state.workflow_id,
            workflow_type=state.workflow_type,
            status=state.status,
            state_json=payload,
            updated_at=now,
        )
        db.add(row)
    else:
        row.workflow_type = state.workflow_type
        row.status = state.status
        row.state_json = payload
        row.updated_at = now
    return WorkflowState.model_validate(row.state_json)


def resolve_workflow_state(
    db: Session,
    *,
    workflow_id: str,
    status: str,
    approval_status: str,
    send_status: str,
    decision_note: str | None = None,
) -> WorkflowState | None:
    row = db.get(WorkflowStateSnapshotORM, workflow_id)
    if row is None:
        return None
    payload = dict(row.state_json)
    outputs = dict(payload.get("outputs") or {})
    outputs["approval_status"] = approval_status
    outputs["send_status"] = send_status
    if decision_note:
        outputs["decision_note"] = decision_note
    payload["outputs"] = outputs
    payload["status"] = status
    payload["current_step_id"] = None
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    row.status = status
    row.state_json = payload
    row.updated_at = datetime.now(timezone.utc)
    return WorkflowState.model_validate(row.state_json)
