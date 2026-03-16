from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.repository import insert_approval, insert_workflow_run, upsert_workflow_state
from app.models.schemas import (
    ApprovalItem,
    EmailDraftResult,
    EmailWorkflowRequest,
    EmailWorkflowResponse,
)
from app.models.workflow_state import (
    EmailWorkflowState,
    WorkflowContextSnapshot,
    WorkflowStepState,
    mark_step_completed,
    mark_step_running,
)
from app.orchestration.langgraph_runner import (
    BaseLangGraphRunner,
    END,
    START,
    StateGraph,
    WorkflowGraphState,
)
from app.services.agent_run_logger import record_agent_run, subject_from_identity
from app.services.audit_event_logger import actor, record_audit_event
from app.services.model_gateway import GenerationResult, ModelGateway
from app.services.observability import NullObservabilityService

EMAIL_AGENT_SUBJECT = subject_from_identity(
    agent_id="email-agent",
    agent_family="email-agent",
    mode="internal_operating",
    autonomy_class="assistant",
    approval_class="ceo_required",
)


class EmailWorkflowRunner(BaseLangGraphRunner):
    def __init__(self, model_gateway: ModelGateway) -> None:
        self.model_gateway = model_gateway
        super().__init__()

    def register_nodes(self, graph: StateGraph) -> None:
        graph.add_node("draft_email", self._draft_email)
        graph.add_node("route_approval", self._route_approval)

    def register_edges(self, graph: StateGraph) -> None:
        graph.add_edge(START, "draft_email")
        graph.add_edge("draft_email", "route_approval")
        graph.add_edge("route_approval", END)

    def _draft_email(self, state: WorkflowGraphState) -> WorkflowGraphState:
        workflow = state["workflow"]
        payload = state["payload"]

        mark_step_running(workflow, "draft_email")
        result = self.model_gateway.draft_email(
            sender=payload.sender,
            subject=payload.subject,
            body=payload.body,
            thread_context=payload.thread_context,
            risk_level=payload.risk_level,
        )
        workflow.outputs["intent"] = result.intent
        workflow.outputs["confidence"] = result.confidence
        workflow.outputs["provider_used"] = result.provider_used
        workflow.outputs["model_used"] = result.model_used
        workflow.outputs["local_llm_invoked"] = result.local_llm_invoked
        workflow.outputs["cloud_llm_invoked"] = result.cloud_llm_invoked
        workflow.outputs["llm_diagnostic_code"] = result.llm_diagnostic_code
        workflow.outputs["llm_diagnostic_detail"] = result.llm_diagnostic_detail
        mark_step_completed(
            workflow,
            "draft_email",
            output_summary=f"Intent={result.intent}, confidence={result.confidence:.2f}",
        )
        return {"workflow": workflow, "payload": payload, "result": result}

    def _route_approval(self, state: WorkflowGraphState) -> WorkflowGraphState:
        workflow = state["workflow"]
        workflow.status = "pending_approval"
        mark_step_running(workflow, "route_approval")
        mark_step_completed(workflow, "route_approval", output_summary="Approval queued")
        return state


class EmailWorkflowService:
    def __init__(self, model_gateway: ModelGateway, observability: NullObservabilityService | None = None):
        self.model_gateway = model_gateway
        self.runner = EmailWorkflowRunner(model_gateway=model_gateway)
        self.observability = observability or getattr(model_gateway, "observability", NullObservabilityService())

    def run(self, payload: EmailWorkflowRequest, db: Session) -> EmailWorkflowResponse:
        workflow_id = str(uuid4())
        approval_id = str(uuid4())
        started_at = datetime.now(timezone.utc)
        try:
            with self.observability.start_span(
                name="workflow.email-operations.run",
                input={
                    "workflow_id": workflow_id,
                    "approval_id": approval_id,
                    "sender": payload.sender,
                    "subject": payload.subject,
                    "risk_level": payload.risk_level,
                    "thread_context_present": payload.thread_context is not None,
                    "source_provider": payload.source_provider,
                },
                metadata={"workflow_type": "email-operations"},
            ) as observation:
                state = EmailWorkflowState(
                    workflow_id=workflow_id,
                    status="running",
                    risk_level=payload.risk_level,
                    approval_required=True,
                    sender=payload.sender,
                    subject=payload.subject,
                    thread_context_present=payload.thread_context is not None,
                    context=WorkflowContextSnapshot(
                        input_summary=f"Email from {payload.sender}: {payload.subject}"
                    ),
                    metadata={
                        "source_account_id": payload.source_account_id,
                        "source_message_id": payload.source_message_id,
                        "source_thread_id": payload.source_thread_id,
                        "source_provider": payload.source_provider,
                    },
                    steps=[
                        WorkflowStepState(
                            step_id="draft_email",
                            name="Draft email response",
                            kind="ai",
                        ),
                        WorkflowStepState(
                            step_id="route_approval",
                            name="Route approval",
                            kind="approval",
                        ),
                    ],
                )
                final_state = self.runner.invoke({"workflow": state, "payload": payload, "approval_id": approval_id})
                workflow_state = final_state["workflow"]
                result = final_state["result"]
                if isinstance(result, GenerationResult):
                    result = EmailDraftResult.model_validate(result.__dict__)
                elif isinstance(result, dict):
                    result = EmailDraftResult.model_validate(result)
                if not isinstance(result, EmailDraftResult):
                    raise TypeError("email_workflow_result_invalid")

                run = EmailWorkflowResponse(
                    workflow_id=workflow_id,
                    status=workflow_state.status,
                    approval_id=approval_id,
                    intent=result.intent,
                    confidence=result.confidence,
                    draft_reply=result.draft_reply,
                    provider_used=result.provider_used,
                    model_used=result.model_used,
                    escalation_reason=result.escalation_reason,
                    local_llm_invoked=result.local_llm_invoked,
                    cloud_llm_invoked=result.cloud_llm_invoked,
                    llm_diagnostic_code=result.llm_diagnostic_code,
                    llm_diagnostic_detail=result.llm_diagnostic_detail,
                    approval_status="pending",
                    send_status="pending" if payload.source_message_id and payload.source_provider else "not_applicable",
                    source_provider=payload.source_provider,
                    source_message_id=payload.source_message_id,
                )

                approval = ApprovalItem(
                    id=approval_id,
                    workflow_id=workflow_id,
                    created_at=datetime.now(timezone.utc),
                    sender=payload.sender,
                    subject=payload.subject,
                    draft_reply=result.draft_reply,
                    status="pending",
                    source_account_id=payload.source_account_id,
                    source_message_id=payload.source_message_id,
                    source_thread_id=payload.source_thread_id,
                    source_provider=payload.source_provider,
                    send_status="pending" if payload.source_message_id and payload.source_provider else "not_applicable",
                )
                upsert_workflow_state(db, workflow_state)
                insert_workflow_run(db, run)
                insert_approval(db, approval)
                agent_run = record_agent_run(
                    db,
                    subject=EMAIL_AGENT_SUBJECT,
                    status="completed",
                    started_at=started_at,
                    ended_at=datetime.now(timezone.utc),
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="draft_email",
                    trigger_event_name="email.received",
                    provider_used=run.provider_used,
                    model_used=run.model_used,
                    confidence=run.confidence,
                )
                record_audit_event(
                    db,
                    event_name="workflow.step.completed",
                    entity_type="workflow_step",
                    entity_id=f"{workflow_id}:draft_email",
                    event_actor=actor(actor_type="agent", actor_id=EMAIL_AGENT_SUBJECT.agent_id),
                    status="completed",
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="draft_email",
                    agent_run_id=agent_run.agent_run_id,
                    approval_class=EMAIL_AGENT_SUBJECT.approval_class,
                    autonomy_class=EMAIL_AGENT_SUBJECT.autonomy_class,
                    provider_used=run.provider_used,
                    model_used=run.model_used,
                    payload_ref_or_inline={"intent": run.intent, "confidence": run.confidence},
                )
                record_audit_event(
                    db,
                    event_name="model.route.selected",
                    entity_type="agent_run",
                    entity_id=agent_run.agent_run_id,
                    event_actor=actor(actor_type="agent", actor_id=EMAIL_AGENT_SUBJECT.agent_id),
                    status="completed",
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="draft_email",
                    agent_run_id=agent_run.agent_run_id,
                    approval_class=EMAIL_AGENT_SUBJECT.approval_class,
                    autonomy_class=EMAIL_AGENT_SUBJECT.autonomy_class,
                    provider_used=run.provider_used,
                    model_used=run.model_used,
                    payload_ref_or_inline={"local_llm_invoked": run.local_llm_invoked, "cloud_llm_invoked": run.cloud_llm_invoked},
                )
                record_audit_event(
                    db,
                    event_name="workflow.step.completed",
                    entity_type="workflow_step",
                    entity_id=f"{workflow_id}:route_approval",
                    event_actor=actor(actor_type="workflow_system", actor_id="email-workflow-service"),
                    status="completed",
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="route_approval",
                    approval_id=approval_id,
                    approval_class=EMAIL_AGENT_SUBJECT.approval_class,
                    payload_ref_or_inline={"approval_status": "pending"},
                )
                record_audit_event(
                    db,
                    event_name="approval.requested",
                    entity_type="approval",
                    entity_id=approval_id,
                    event_actor=actor(actor_type="workflow_system", actor_id="email-workflow-service"),
                    status="pending",
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="route_approval",
                    approval_id=approval_id,
                    approval_class=EMAIL_AGENT_SUBJECT.approval_class,
                    tool_id="approval.request",
                    payload_ref_or_inline={"sender": payload.sender, "subject": payload.subject},
                )
                db.commit()
                observation.update(
                    output=run.model_dump(mode="json"),
                    metadata={
                        "workflow_status": workflow_state.status,
                        "approval_required": workflow_state.approval_required,
                        "provider_used": run.provider_used,
                        "model_used": run.model_used,
                    },
                )
                return run
        except Exception as exc:
            db.rollback()
            try:
                agent_run = record_agent_run(
                    db,
                    subject=EMAIL_AGENT_SUBJECT,
                    status="failed",
                    started_at=started_at,
                    ended_at=datetime.now(timezone.utc),
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="draft_email",
                    trigger_event_name="email.received",
                    error_code=exc.__class__.__name__,
                    error_detail=str(exc),
                )
                record_audit_event(
                    db,
                    event_name="workflow.step.failed",
                    entity_type="workflow_step",
                    entity_id=f"{workflow_id}:draft_email",
                    event_actor=actor(actor_type="agent", actor_id=EMAIL_AGENT_SUBJECT.agent_id),
                    status="failed",
                    workflow_id=workflow_id,
                    run_id=workflow_id,
                    step_id="draft_email",
                    agent_run_id=agent_run.agent_run_id,
                    approval_class=EMAIL_AGENT_SUBJECT.approval_class,
                    autonomy_class=EMAIL_AGENT_SUBJECT.autonomy_class,
                    error_code=exc.__class__.__name__,
                    error_detail=str(exc),
                )
                db.commit()
            except Exception:
                db.rollback()
            raise
