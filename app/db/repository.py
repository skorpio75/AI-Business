from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.db.models import ApprovalORM, WorkflowRunORM, WorkflowStateSnapshotORM
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


def list_workflow_runs(db: Session) -> list[EmailWorkflowResponse]:
    rows = db.execute(select(WorkflowRunORM)).scalars().all()
    return [EmailWorkflowResponse.model_validate(row) for row in rows]


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
