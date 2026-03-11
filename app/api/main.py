from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.knowledge.pgvector_store import PgVectorRetrievalService
from app.db.repository import get_approval, list_pending_approvals, list_workflow_runs, upsert_approval
from app.db.session import get_db
from app.models.agent_contract import AgentContract
from app.models.schemas import (
    ApprovalDecisionRequest,
    ApprovalItem,
    DashboardSummaryResponse,
    EmailWorkflowRequest,
    EmailWorkflowResponse,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    ProposalGenerationRequest,
    ProposalGenerationResponse,
)
from app.services.dashboard_summary import DashboardSummaryService
from app.services.agent_registry import AgentRegistryService
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import ModelGateway
from app.services.personal_assistant_context import PersonalAssistantContextService
from app.services.proposal_workflow import ProposalWorkflowService

settings = get_settings()
gateway = ModelGateway(settings=settings)
email_workflow = EmailWorkflowService(model_gateway=gateway)
agent_registry = AgentRegistryService()
knowledge_qna = KnowledgeQnAService(retrieval_service=PgVectorRetrievalService(), model_gateway=gateway)
proposal_workflow = ProposalWorkflowService(model_gateway=gateway)
personal_assistant_context = PersonalAssistantContextService()
dashboard_summary = DashboardSummaryService()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/agents", response_model=list[AgentContract])
def list_agents_endpoint() -> list[AgentContract]:
    return agent_registry.list_agents()


@app.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    approvals = list_pending_approvals(db)
    workflow_runs = list_workflow_runs(db)
    assistant_context = personal_assistant_context.build_context(
        account_id="ceo-inbox",
        calendar_id="primary-calendar",
    )
    return dashboard_summary.build_summary(
        agents=agent_registry.list_agents(),
        approvals=approvals,
        workflow_runs_count=len(workflow_runs),
        personal_context=assistant_context,
    )


@app.post("/knowledge/qna", response_model=KnowledgeQueryResponse)
def run_knowledge_qna(payload: KnowledgeQueryRequest) -> KnowledgeQueryResponse:
    return knowledge_qna.answer(payload)


@app.post("/workflows/proposal-generation/run", response_model=ProposalGenerationResponse)
def run_proposal_generation(
    payload: ProposalGenerationRequest,
) -> ProposalGenerationResponse:
    return proposal_workflow.run(payload)


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
