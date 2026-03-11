from datetime import datetime
from typing import Literal, Optional

from pydantic import ConfigDict
from pydantic import BaseModel, Field


DecisionType = Literal["approve", "reject", "edit"]


class EmailWorkflowRequest(BaseModel):
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)
    sender: str = Field(min_length=1)
    thread_context: Optional[str] = None
    risk_level: Literal["low", "medium", "high"] = "medium"


class EmailDraftResult(BaseModel):
    intent: str
    confidence: float
    draft_reply: str
    provider_used: Literal["local", "cloud", "fallback-rule"]
    model_used: str
    escalation_reason: Optional[str] = None


class EmailWorkflowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: str
    status: Literal["pending_approval"]
    approval_id: str
    intent: str
    confidence: float
    draft_reply: str
    provider_used: str
    model_used: str
    escalation_reason: Optional[str] = None


class ApprovalItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_id: str
    created_at: datetime
    sender: str
    subject: str
    draft_reply: str
    status: Literal["pending", "approved", "rejected", "edited"]
    decision_note: Optional[str] = None


class ApprovalDecisionRequest(BaseModel):
    decision: DecisionType
    edited_reply: Optional[str] = None
    note: Optional[str] = None
