from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.control_plane import ApprovalClass, AutonomyClass, TrackId

AgentRunStatus = str
AgentRunMode = str


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
    trigger_event_name: Optional[str] = None
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
