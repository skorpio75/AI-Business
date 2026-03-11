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
        )
        db.add(row)
    else:
        row.draft_reply = item.draft_reply
        row.status = item.status
        row.decision_note = item.decision_note
    return ApprovalItem.model_validate(row)


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
