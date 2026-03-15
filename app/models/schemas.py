from datetime import datetime
from typing import Literal, Optional

from pydantic import ConfigDict
from pydantic import BaseModel, Field
from pydantic import field_validator

from app.models.specialist_contracts import (
    ArchitectureAdvice,
    CloseChecklistItem,
    ContextSignal,
    DeliveryBlueprintPhase,
    FinancialScenario,
    ImprovementBacklogItem,
    MaturityDimension,
    MissionAssessment,
    OpportunityMapItem,
    ReconciliationException,
    ReconciliationRule,
    RecommendedService,
    StrategyOption,
    UpsellOpportunity,
)

DecisionType = Literal["approve", "reject", "edit"]
ApprovalStatus = Literal["pending", "approved", "rejected", "edited"]
WorkflowRunStatus = Literal["pending_approval", "completed"]
SendStatus = Literal["pending", "sent", "not_applicable"]


class EmailWorkflowRequest(BaseModel):
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)
    sender: str = Field(min_length=1)
    thread_context: Optional[str] = None
    risk_level: Literal["low", "medium", "high"] = "medium"
    source_account_id: Optional[str] = None
    source_message_id: Optional[str] = None
    source_thread_id: Optional[str] = None
    source_provider: Optional[str] = None


class EmailDraftResult(BaseModel):
    intent: str
    confidence: float
    draft_reply: str
    provider_used: Literal["local", "cloud", "fallback-rule"]
    model_used: str
    escalation_reason: Optional[str] = None
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


class EmailWorkflowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: str
    status: WorkflowRunStatus
    approval_id: str
    intent: str
    confidence: float
    draft_reply: str
    provider_used: str
    model_used: str
    escalation_reason: Optional[str] = None
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None
    approval_status: ApprovalStatus = "pending"
    send_status: SendStatus = "not_applicable"
    sent_at: Optional[datetime] = None
    source_provider: Optional[str] = None
    source_message_id: Optional[str] = None

    @field_validator("approval_status", mode="before")
    @classmethod
    def default_approval_status(cls, value: str | None) -> str:
        return value or "pending"

    @field_validator("send_status", mode="before")
    @classmethod
    def default_send_status(cls, value: str | None) -> str:
        return value or "not_applicable"


class ApprovalItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_id: str
    created_at: datetime
    sender: str
    subject: str
    draft_reply: str
    status: ApprovalStatus
    decision_note: Optional[str] = None
    source_account_id: Optional[str] = None
    source_message_id: Optional[str] = None
    source_thread_id: Optional[str] = None
    source_provider: Optional[str] = None
    send_status: SendStatus = "not_applicable"
    send_detail: Optional[str] = None
    sent_at: Optional[datetime] = None

    @field_validator("send_status", mode="before")
    @classmethod
    def default_send_status(cls, value: str | None) -> str:
        return value or "not_applicable"


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
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


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
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


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


class CTOCIOScopeInsight(BaseModel):
    insight_id: str
    title: str
    summary: str
    focus_area: Literal["customer_scope", "architecture", "internal_platform"]
    tone: KpiTone = "neutral"


class CTOCIOPanelResponse(BaseModel):
    agent_id: str
    display_name: str
    role_summary: str
    primary_track: Literal["track_a_internal", "track_b_client"]
    operating_modes: list[str] = Field(default_factory=list)
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None
    scope_insights: list[CTOCIOScopeInsight] = Field(default_factory=list)
    strategy_options: list[StrategyOption] = Field(default_factory=list)
    architecture_advice: ArchitectureAdvice
    internal_improvement_backlog: list[ImprovementBacklogItem] = Field(default_factory=list)
    approval_required: bool = True


class CTOCIOAnalysisResponse(BaseModel):
    agent_id: str
    display_name: str
    role_summary: str
    primary_track: Literal["track_a_internal", "track_b_client"]
    operating_modes: list[str] = Field(default_factory=list)
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None
    analysis_summary: str
    mission_assessment: MissionAssessment
    context_signals: list[ContextSignal] = Field(default_factory=list)
    recommended_services: list[RecommendedService] = Field(default_factory=list)
    upsell_opportunities: list[UpsellOpportunity] = Field(default_factory=list)
    strategy_options: list[StrategyOption] = Field(default_factory=list)
    architecture_advice: ArchitectureAdvice
    approval_required: bool = True


class FinancePanelAgentSummary(BaseModel):
    agent_id: str
    display_name: str
    role_summary: str
    primary_track: Literal["track_a_internal", "track_b_client"]
    operating_modes: list[str] = Field(default_factory=list)
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    approval_class: Literal["none", "bounded", "ceo_required"]
    autonomy_class: Literal["assistant", "supervised_executor", "bounded_autonomous", "approval_gated"]


class FinancePanelResponse(BaseModel):
    agents: list[FinancePanelAgentSummary] = Field(default_factory=list)
    reconciliation_rules: list[ReconciliationRule] = Field(default_factory=list)
    accounting_exceptions: list[ReconciliationException] = Field(default_factory=list)
    close_checklist: list[CloseChecklistItem] = Field(default_factory=list)
    accounting_ready_exports: list[str] = Field(default_factory=list)
    scenarios: list[FinancialScenario] = Field(default_factory=list)
    cashflow_risks: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    executive_summary: str
    approval_required: bool = True


class ChiefAIScopeSignal(BaseModel):
    signal_id: str
    title: str
    summary: str
    focus_area: Literal["offer_design", "delivery_controls", "commercialization"]
    tone: KpiTone = "neutral"


class ChiefAIPanelResponse(BaseModel):
    agent_id: str
    display_name: str
    role_summary: str
    primary_track: Literal["track_a_internal", "track_b_client"]
    operating_modes: list[str] = Field(default_factory=list)
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None
    executive_summary: str
    scope_signals: list[ChiefAIScopeSignal] = Field(default_factory=list)
    opportunity_map: list[OpportunityMapItem] = Field(default_factory=list)
    delivery_blueprint: list[DeliveryBlueprintPhase] = Field(default_factory=list)
    maturity_model: list[MaturityDimension] = Field(default_factory=list)
    approval_required: bool = True


class ChiefAIAnalysisResponse(BaseModel):
    agent_id: str
    display_name: str
    role_summary: str
    primary_track: Literal["track_a_internal", "track_b_client"]
    operating_modes: list[str] = Field(default_factory=list)
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None
    executive_summary: str
    mission_assessment: MissionAssessment
    context_signals: list[ContextSignal] = Field(default_factory=list)
    recommended_services: list[RecommendedService] = Field(default_factory=list)
    upsell_opportunities: list[UpsellOpportunity] = Field(default_factory=list)
    opportunity_map: list[OpportunityMapItem] = Field(default_factory=list)
    delivery_blueprint: list[DeliveryBlueprintPhase] = Field(default_factory=list)
    maturity_model: list[MaturityDimension] = Field(default_factory=list)
    approval_required: bool = True
