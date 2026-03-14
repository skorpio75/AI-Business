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
from app.services.model_gateway import GenerationResult, ModelGateway


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
    def __init__(self, model_gateway: ModelGateway):
        self.model_gateway = model_gateway
        self.runner = EmailWorkflowRunner(model_gateway=model_gateway)

    def run(self, payload: EmailWorkflowRequest, db: Session) -> EmailWorkflowResponse:
        workflow_id = str(uuid4())
        approval_id = str(uuid4())

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
        db.commit()
        return run
