from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.db.repository import get_approval, list_pending_approvals, list_workflow_runs, upsert_approval
from app.db.session import get_db
from app.models.schemas import (
    ApprovalDecisionRequest,
    ApprovalItem,
    EmailWorkflowRequest,
    EmailWorkflowResponse,
)
from app.services.email_workflow import EmailWorkflowService
from app.services.model_gateway import ModelGateway

settings = get_settings()
gateway = ModelGateway(settings=settings)
email_workflow = EmailWorkflowService(model_gateway=gateway)

app = FastAPI(title=settings.app_name)


@app.get("/healthz")
def healthz() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.env,
        "local_model": settings.local_model,
        "cloud_model": settings.cloud_model,
    }


@app.post("/workflows/email-operations/run", response_model=EmailWorkflowResponse)
def run_email_operations(
    payload: EmailWorkflowRequest, db: Session = Depends(get_db)
) -> EmailWorkflowResponse:
    return email_workflow.run(payload, db=db)


@app.get("/workflows/runs")
def list_workflow_runs_endpoint(db: Session = Depends(get_db)) -> list[EmailWorkflowResponse]:
    return list_workflow_runs(db)


@app.get("/approvals/pending")
def list_pending_approvals_endpoint(db: Session = Depends(get_db)) -> list[ApprovalItem]:
    return list_pending_approvals(db)


@app.post("/approvals/{approval_id}/decision", response_model=ApprovalItem)
def decide_approval(
    approval_id: str, payload: ApprovalDecisionRequest, db: Session = Depends(get_db)
) -> ApprovalItem:
    item = get_approval(db, approval_id)
    if item is None:
        raise HTTPException(status_code=404, detail="approval_not_found")

    if item.status != "pending":
        raise HTTPException(status_code=409, detail="approval_already_resolved")

    if payload.decision == "approve":
        item.status = "approved"
    elif payload.decision == "reject":
        item.status = "rejected"
    else:
        if not payload.edited_reply:
            raise HTTPException(status_code=400, detail="edited_reply_required")
        item.status = "edited"
        item.draft_reply = payload.edited_reply

    item.decision_note = payload.note
    updated = upsert_approval(db, item)
    db.commit()
    return updated
