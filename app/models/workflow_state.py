from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


WorkflowStatus = Literal[
    "queued",
    "running",
    "pending_approval",
    "completed",
    "failed",
    "escalated",
]
WorkflowStepKind = Literal["deterministic", "ai", "approval", "integration"]
WorkflowStepStatus = Literal["pending", "running", "completed", "failed", "skipped"]
RiskLevel = Literal["low", "medium", "high"]


class WorkflowMemoryRefs(BaseModel):
    shared_workspace_ids: list[str] = Field(default_factory=list)
    semantic_refs: list[str] = Field(default_factory=list)
    episodic_refs: list[str] = Field(default_factory=list)


class WorkflowContextSnapshot(BaseModel):
    input_summary: Optional[str] = None
    company_context_id: Optional[str] = None
    client_context_id: Optional[str] = None
    project_context_id: Optional[str] = None
    memory_refs: WorkflowMemoryRefs = Field(default_factory=WorkflowMemoryRefs)


class WorkflowStepState(BaseModel):
    step_id: str
    name: str
    kind: WorkflowStepKind
    status: WorkflowStepStatus = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_summary: Optional[str] = None
    error_message: Optional[str] = None


class WorkflowState(BaseModel):
    workflow_id: str
    workflow_type: str
    status: WorkflowStatus
    risk_level: RiskLevel = "medium"
    approval_required: bool = False
    current_step_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    context: WorkflowContextSnapshot = Field(default_factory=WorkflowContextSnapshot)
    steps: list[WorkflowStepState] = Field(default_factory=list)
    outputs: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmailWorkflowState(WorkflowState):
    workflow_type: Literal["email-operations"] = "email-operations"
    sender: str
    subject: str
    thread_context_present: bool = False


def mark_step_running(state: WorkflowState, step_id: str) -> WorkflowState:
    now = datetime.now(timezone.utc)
    for step in state.steps:
        if step.step_id == step_id:
            step.status = "running"
            step.started_at = now
            state.current_step_id = step_id
            state.updated_at = now
            return state
    raise ValueError(f"step_not_found:{step_id}")


def mark_step_completed(
    state: WorkflowState, step_id: str, output_summary: Optional[str] = None
) -> WorkflowState:
    now = datetime.now(timezone.utc)
    for step in state.steps:
        if step.step_id == step_id:
            step.status = "completed"
            step.completed_at = now
            step.output_summary = output_summary
            state.updated_at = now
            return state
    raise ValueError(f"step_not_found:{step_id}")


def mark_step_failed(state: WorkflowState, step_id: str, error_message: str) -> WorkflowState:
    now = datetime.now(timezone.utc)
    for step in state.steps:
        if step.step_id == step_id:
            step.status = "failed"
            step.completed_at = now
            step.error_message = error_message
            state.status = "failed"
            state.updated_at = now
            return state
    raise ValueError(f"step_not_found:{step_id}")
