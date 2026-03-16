import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.connectors.factory import build_calendar_connector, build_inbox_connector
from app.connectors.http import ConnectorHttpError
from app.core.settings import Settings, build_settings, ensure_runtime_directories, get_settings
from app.knowledge.pgvector_store import PgVectorRetrievalService
from app.db.repository import (
    get_approval,
    list_pending_approvals,
    list_workflow_runs,
    resolve_workflow_state,
    update_workflow_run_resolution,
    upsert_approval,
)
from app.db.session import get_db
from app.models.agent_contract import AgentContract
from app.models.connectors import ConnectorBootstrapStatusResponse, PersonalAssistantContext
from app.models.schemas import (
    ApprovalDecisionRequest,
    ApprovalItem,
    ChiefAIAnalysisResponse,
    ChiefAIPanelResponse,
    CTOCIOAnalysisResponse,
    CTOCIOPanelResponse,
    DashboardSummaryResponse,
    EmailWorkflowRequest,
    EmailWorkflowResponse,
    FinancePanelResponse,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    ProposalGenerationRequest,
    ProposalGenerationResponse,
)
from app.models.specialist_contracts import ChiefAIDigitalStrategyInput, CTOCIOCounselInput
from app.services.dashboard_summary import DashboardSummaryService
from app.services.agent_registry import AgentRegistryService
from app.services.chief_ai_panel import ChiefAIPanelService
from app.services.cto_cio_panel import CTOCIOPanelService
from app.services.email_workflow import EmailWorkflowService
from app.services.finance_panel import FinancePanelService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import ModelGateway
from app.services.personal_assistant_context import PersonalAssistantContextService
from app.services.provider_auth import (
    ProviderAuthError,
    describe_provider_bootstrap,
    ensure_provider_tokens,
    hydrate_provider_settings,
)
from app.services.proposal_workflow import ProposalWorkflowService

logger = logging.getLogger(__name__)
settings = get_settings()
gateway = ModelGateway(settings=settings)
email_workflow = EmailWorkflowService(model_gateway=gateway)
agent_registry = AgentRegistryService()
knowledge_qna = KnowledgeQnAService(retrieval_service=PgVectorRetrievalService(), model_gateway=gateway)
proposal_workflow = ProposalWorkflowService(model_gateway=gateway)
dashboard_summary = DashboardSummaryService()
cto_cio_panel = CTOCIOPanelService(model_gateway=gateway)
finance_panel = FinancePanelService()
chief_ai_panel = ChiefAIPanelService(model_gateway=gateway)


def get_runtime_settings() -> Settings:
    return build_settings()


def build_personal_assistant_context_service(current_settings: Settings) -> PersonalAssistantContextService:
    prepared_settings = hydrate_provider_settings(current_settings)
    try:
        prepared_settings = ensure_provider_tokens(prepared_settings)
    except ProviderAuthError as exc:
        logger.warning("Provider token bootstrap failed while building connector context: %s", exc)
    return PersonalAssistantContextService(
        inbox_connector=build_inbox_connector(prepared_settings),
        calendar_connector=build_calendar_connector(prepared_settings),
    )


def bootstrap_provider_tokens_on_startup() -> None:
    current_settings = get_runtime_settings()
    try:
        ensure_provider_tokens(current_settings, force_refresh=True)
        logger.info("Completed provider token bootstrap during startup.")
    except ProviderAuthError as exc:
        logger.warning("Provider token bootstrap failed during startup: %s", exc)


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_runtime_directories(get_runtime_settings())
    bootstrap_provider_tokens_on_startup()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
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
    current_settings = get_runtime_settings()
    personal_assistant_context = build_personal_assistant_context_service(current_settings)
    approvals = list_pending_approvals(db)
    workflow_runs = list_workflow_runs(db)
    assistant_context = personal_assistant_context.build_context(
        account_id=current_settings.personal_assistant_account_id,
        calendar_id=current_settings.personal_assistant_calendar_id,
        window_hours=current_settings.personal_assistant_window_hours,
        inbox_lookback_hours=current_settings.personal_assistant_inbox_lookback_hours,
    )
    return dashboard_summary.build_summary(
        agents=agent_registry.list_agents(),
        approvals=approvals,
        workflow_runs_count=len(workflow_runs),
        personal_context=assistant_context,
    )


@app.get("/specialists/cto-cio/panel", response_model=CTOCIOPanelResponse)
def get_cto_cio_panel() -> CTOCIOPanelResponse:
    agent = agent_registry.get_agent("cto-cio-agent")
    if agent is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return cto_cio_panel.build_panel(agent=agent)


@app.post("/specialists/cto-cio/analyze", response_model=CTOCIOAnalysisResponse)
def analyze_cto_cio_client_context(payload: CTOCIOCounselInput) -> CTOCIOAnalysisResponse:
    agent = agent_registry.get_agent("cto-cio-agent")
    if agent is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return cto_cio_panel.analyze_client_context(agent=agent, payload=payload)


@app.get("/specialists/finance/panel", response_model=FinancePanelResponse)
def get_finance_panel() -> FinancePanelResponse:
    accountant_agent = agent_registry.get_agent("accountant-agent")
    cfo_agent = agent_registry.get_agent("cfo-agent")
    finance_ops_agent = agent_registry.get_agent("finance-ops-agent")
    if accountant_agent is None or cfo_agent is None or finance_ops_agent is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return finance_panel.build_panel(
        accountant_agent=accountant_agent,
        cfo_agent=cfo_agent,
        finance_ops_agent=finance_ops_agent,
    )


@app.get("/specialists/chief-ai-digital-strategy/panel", response_model=ChiefAIPanelResponse)
def get_chief_ai_panel() -> ChiefAIPanelResponse:
    agent = agent_registry.get_agent("chief-ai-digital-strategy-agent")
    if agent is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return chief_ai_panel.build_panel(agent=agent)


@app.post("/specialists/chief-ai-digital-strategy/analyze", response_model=ChiefAIAnalysisResponse)
def analyze_chief_ai_client_context(
    payload: ChiefAIDigitalStrategyInput,
) -> ChiefAIAnalysisResponse:
    agent = agent_registry.get_agent("chief-ai-digital-strategy-agent")
    if agent is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return chief_ai_panel.analyze_client_context(agent=agent, payload=payload)


@app.get("/personal-assistant/context", response_model=PersonalAssistantContext)
def get_personal_assistant_context(
    window_hours: int = Query(default=settings.personal_assistant_window_hours, ge=1, le=336),
    inbox_lookback_hours: int = Query(default=settings.personal_assistant_inbox_lookback_hours, ge=1, le=720),
    inbox_limit: int = Query(default=25, ge=1, le=100),
) -> PersonalAssistantContext:
    current_settings = get_runtime_settings()
    personal_assistant_context = build_personal_assistant_context_service(current_settings)
    return personal_assistant_context.build_context(
        account_id=current_settings.personal_assistant_account_id,
        calendar_id=current_settings.personal_assistant_calendar_id,
        window_hours=window_hours,
        inbox_lookback_hours=inbox_lookback_hours,
        inbox_limit=inbox_limit,
    )


@app.get("/connectors/bootstrap-status", response_model=ConnectorBootstrapStatusResponse)
def get_connector_bootstrap_status() -> ConnectorBootstrapStatusResponse:
    return describe_provider_bootstrap(get_runtime_settings())


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
    current_settings = get_runtime_settings()
    personal_assistant_context = build_personal_assistant_context_service(current_settings)
    item = get_approval(db, approval_id)
    if item is None:
        raise HTTPException(status_code=404, detail="approval_not_found")

    if item.status != "pending":
        raise HTTPException(status_code=409, detail="approval_already_resolved")

    if payload.edited_reply:
        item.draft_reply = payload.edited_reply

    if payload.decision == "approve":
        if item.source_message_id and item.source_account_id:
            try:
                personal_assistant_context.inbox_connector.reply_to_message(
                    account_id=item.source_account_id,
                    message_id=item.source_message_id,
                    reply_body=item.draft_reply,
                )
            except (ConnectorHttpError, NotImplementedError) as exc:
                raise HTTPException(status_code=502, detail=f"email_send_failed:{exc}") from exc
            item.send_status = "sent"
            item.send_detail = "Reply sent through configured inbox connector."
            item.sent_at = datetime.now(timezone.utc)
        else:
            item.send_status = "not_applicable"
            item.send_detail = "No source message metadata was attached to this approval."
        item.status = "approved"
        update_workflow_run_resolution(
            db,
            workflow_id=item.workflow_id,
            status="completed",
            approval_status="approved",
            send_status=item.send_status,
            sent_at=item.sent_at,
        )
        resolve_workflow_state(
            db,
            workflow_id=item.workflow_id,
            status="completed",
            approval_status="approved",
            send_status=item.send_status,
            decision_note=payload.note,
        )
    elif payload.decision == "reject":
        item.status = "rejected"
        item.send_status = "not_applicable"
        item.send_detail = "Approval rejected before outbound send."
        update_workflow_run_resolution(
            db,
            workflow_id=item.workflow_id,
            status="completed",
            approval_status="rejected",
            send_status=item.send_status,
        )
        resolve_workflow_state(
            db,
            workflow_id=item.workflow_id,
            status="completed",
            approval_status="rejected",
            send_status=item.send_status,
            decision_note=payload.note,
        )
    else:
        if not payload.edited_reply:
            raise HTTPException(status_code=400, detail="edited_reply_required")
        item.status = "pending"
        item.send_status = "pending" if item.source_message_id else "not_applicable"
        item.send_detail = "Draft updated and left pending for approval."
        update_workflow_run_resolution(
            db,
            workflow_id=item.workflow_id,
            status="pending_approval",
            approval_status="pending",
            send_status=item.send_status,
        )
        resolve_workflow_state(
            db,
            workflow_id=item.workflow_id,
            status="pending_approval",
            approval_status="pending",
            send_status=item.send_status,
            decision_note=payload.note,
        )

    item.decision_note = payload.note
    updated = upsert_approval(db, item)
    db.commit()
    return updated
