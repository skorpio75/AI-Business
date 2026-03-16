from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from app.models.control_plane import ApprovalClass, AutonomyClass, NormalizedEventName, TrackId
from app.models.tool_profiles import NormalizedToolId, OperatingMode

AgentRunStatus = Literal["started", "completed", "failed", "waiting", "blocked"]
AgentRunMode = OperatingMode
AuditEventStatus = Literal[
    "started",
    "completed",
    "failed",
    "requested",
    "approved",
    "rejected",
    "pending",
    "blocked",
    "edited",
    "escalated",
    "validated",
]
AuditActorType = Literal[
    "human_operator",
    "workflow_system",
    "agent",
    "policy_layer",
    "connector",
    "external_runtime",
]
AuditEventName = Literal[
    "workflow.run.started",
    "workflow.run.completed",
    "workflow.run.failed",
    "workflow.step.started",
    "workflow.step.completed",
    "workflow.step.failed",
    "workflow.step.escalated",
    "agent.run.started",
    "agent.run.completed",
    "agent.run.failed",
    "agent.run.handoff_requested",
    "agent.run.handoff_completed",
    "model.route.selected",
    "model.route.escalated",
    "model.route.fallback_applied",
    "model.output.validated",
    "model.output.validation_failed",
    "tool.call.started",
    "tool.call.completed",
    "tool.call.failed",
    "outbound.action.requested",
    "outbound.action.executed",
    "outbound.action.blocked",
    "approval.requested",
    "approval.reminded",
    "approval.decided",
    "approval.rejected",
    "approval.edited",
    "approval.expired",
    "connector.bootstrap.updated",
    "connector.refresh.failed",
    "runtime.config.loaded",
    "runtime.policy.blocked",
]


class AgentRunRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    agent_run_id: str
    tenant_id: str
    track: TrackId
    agent_id: str
    agent_family: str
    mode: AgentRunMode
    status: AgentRunStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    workflow_id: Optional[str] = None
    run_id: Optional[str] = None
    step_id: Optional[str] = None
    parent_agent_run_id: Optional[str] = None
    trigger_event_name: Optional[NormalizedEventName] = None
    input_ref: Optional[str] = None
    output_ref: Optional[str] = None
    autonomy_class: Optional[AutonomyClass] = None
    approval_class: Optional[ApprovalClass] = None
    provider_used: Optional[str] = None
    model_used: Optional[str] = None
    routing_path: Optional[str] = None
    fallback_mode: Optional[str] = None
    confidence: Optional[float] = None
    trace_ref: Optional[str] = None
    error_code: Optional[str] = None
    error_detail: Optional[str] = None


class AuditEventRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    audit_event_id: str
    tenant_id: str
    track: TrackId
    occurred_at: datetime
    event_name: AuditEventName
    entity_type: str
    entity_id: str
    actor_type: AuditActorType
    actor_id: str
    status: AuditEventStatus
    workflow_id: Optional[str] = None
    run_id: Optional[str] = None
    step_id: Optional[str] = None
    agent_run_id: Optional[str] = None
    approval_id: Optional[str] = None
    approval_class: Optional[ApprovalClass] = None
    autonomy_class: Optional[AutonomyClass] = None
    tool_id: Optional[NormalizedToolId] = None
    provider_used: Optional[str] = None
    model_used: Optional[str] = None
    routing_path: Optional[str] = None
    fallback_mode: Optional[str] = None
    trace_ref: Optional[str] = None
    payload_ref_or_inline: Optional[dict | str] = None
    state_diff_ref: Optional[str] = None
    error_code: Optional[str] = None
    error_detail: Optional[str] = None
