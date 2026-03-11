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


class KnowledgeQueryRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=8)


class KnowledgeCitation(BaseModel):
    title: str
    source_path: str
    snippet: str
    score: float


class KnowledgeQueryResponse(BaseModel):
    question: str
    answer: str
    citations: list[KnowledgeCitation] = Field(default_factory=list)
    grounded: bool
    provider_used: str
    model_used: str


class ProposalGenerationRequest(BaseModel):
    client_name: str = Field(min_length=1)
    opportunity_summary: str = Field(min_length=1)
    desired_outcomes: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class ProposalGenerationResponse(BaseModel):
    workflow_id: str
    status: Literal["completed"] = "completed"
    title: str
    executive_summary: str
    proposal_draft: str
    next_steps: list[str] = Field(default_factory=list)
    provider_used: str
    model_used: str


KpiTone = Literal["neutral", "success", "warning", "critical"]


class DashboardKpi(BaseModel):
    id: str
    label: str
    value: str
    tone: KpiTone = "neutral"
    context: str
    footnote: Optional[str] = None


class PersonalAssistantPriority(BaseModel):
    title: str
    reason: str
    urgency: Literal["low", "medium", "high"]


class ScheduleConflict(BaseModel):
    title: str
    detail: str
    severity: Literal["info", "warning", "critical"]


class PersonalAssistantQuickAction(BaseModel):
    label: str
    target_view: str
    reason: str


class PersonalAssistantBriefResponse(BaseModel):
    priorities: list[PersonalAssistantPriority] = Field(default_factory=list)
    schedule_conflicts: list[ScheduleConflict] = Field(default_factory=list)
    quick_actions: list[PersonalAssistantQuickAction] = Field(default_factory=list)
    inbox_status: str
    calendar_status: str


class DashboardSummaryResponse(BaseModel):
    kpis: list[DashboardKpi] = Field(default_factory=list)
    personal_assistant: PersonalAssistantBriefResponse
