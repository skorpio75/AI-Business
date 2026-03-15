from typing import Literal, Optional

from pydantic import BaseModel, Field


PriorityBand = Literal["now", "next", "later"]
ImpactLevel = Literal["low", "medium", "high"]
EffortBand = Literal["small", "medium", "large"]
DecisionHorizon = Literal["30_days", "90_days", "12_months"]
MaturityLevel = Literal["ad_hoc", "emerging", "repeatable", "managed", "optimized"]
ContextSignalCategory = Literal["problem", "history", "constraint", "readiness", "risk", "opportunity"]
ServiceDeliveryMode = Literal["client_delivery", "client_facing_service"]
ConsultingMotion = Literal["problem_solving", "opportunity_discovery", "account_growth", "mixed"]


class ContextSignal(BaseModel):
    signal_id: str
    category: ContextSignalCategory
    title: str
    summary: str
    implication: str


class RecommendedService(BaseModel):
    service_id: str
    name: str
    summary: str
    fit_reason: str
    suggested_outcomes: list[str] = Field(default_factory=list)
    delivery_mode: ServiceDeliveryMode = "client_facing_service"
    priority: PriorityBand


class MissionAssessment(BaseModel):
    mission_id: str
    consulting_motion: ConsultingMotion
    title: str
    summary: str
    client_need: str
    success_definition: str
    why_now: str


class UpsellOpportunity(BaseModel):
    opportunity_id: str
    title: str
    summary: str
    rationale: str
    suggested_service: str
    expansion_trigger: str
    priority: PriorityBand


class StrategyOption(BaseModel):
    option_id: str
    title: str
    summary: str
    benefits: list[str] = Field(default_factory=list)
    tradeoffs: list[str] = Field(default_factory=list)
    recommended_when: str


class ArchitectureAdvice(BaseModel):
    current_state: str
    target_state: str
    key_constraints: list[str] = Field(default_factory=list)
    proposed_changes: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class ImprovementBacklogItem(BaseModel):
    item_id: str
    title: str
    rationale: str
    priority: PriorityBand
    impact: ImpactLevel
    effort: EffortBand
    owner_hint: Optional[str] = None


class CTOCIOCounselInput(BaseModel):
    engagement_name: str
    problem_statement: str
    business_goal: str
    client_context: str = ""
    engagement_history: list[str] = Field(default_factory=list)
    current_stack: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    desired_outcomes: list[str] = Field(default_factory=list)
    internal_platform_needs: list[str] = Field(default_factory=list)


class CTOCIOCounselOutput(BaseModel):
    analysis_summary: str
    mission_assessment: MissionAssessment
    context_signals: list[ContextSignal] = Field(default_factory=list)
    recommended_services: list[RecommendedService] = Field(default_factory=list)
    upsell_opportunities: list[UpsellOpportunity] = Field(default_factory=list)
    strategy_options: list[StrategyOption] = Field(default_factory=list)
    architecture_advice: ArchitectureAdvice
    internal_improvement_backlog: list[ImprovementBacklogItem] = Field(default_factory=list)
    approval_required: bool = True


class ReconciliationRule(BaseModel):
    rule_id: str
    description: str
    severity: Literal["warning", "blocking"]


class ReconciliationException(BaseModel):
    exception_id: str
    summary: str
    impacted_records: list[str] = Field(default_factory=list)
    severity: Literal["warning", "material", "critical"]
    recommended_action: str


class CloseChecklistItem(BaseModel):
    item_id: str
    title: str
    owner: str
    status: Literal["pending", "in_progress", "completed", "blocked"]
    notes: Optional[str] = None


class AccountantContractInput(BaseModel):
    period_label: str
    invoices: list[str] = Field(default_factory=list)
    payments: list[str] = Field(default_factory=list)
    expenses: list[str] = Field(default_factory=list)
    journal_entries: list[str] = Field(default_factory=list)


class AccountantContractOutput(BaseModel):
    reconciliation_rules: list[ReconciliationRule] = Field(default_factory=list)
    exceptions: list[ReconciliationException] = Field(default_factory=list)
    close_checklist: list[CloseChecklistItem] = Field(default_factory=list)
    accounting_ready_exports: list[str] = Field(default_factory=list)


class FinancialScenario(BaseModel):
    scenario_id: str
    title: str
    horizon: DecisionHorizon
    assumptions: list[str] = Field(default_factory=list)
    projected_outcomes: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class CFOContractInput(BaseModel):
    period_label: str
    baseline_kpis: list[str] = Field(default_factory=list)
    known_risks: list[str] = Field(default_factory=list)
    decision_topics: list[str] = Field(default_factory=list)


class CFOContractOutput(BaseModel):
    scenarios: list[FinancialScenario] = Field(default_factory=list)
    cashflow_risks: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    executive_summary: str
    approval_required: bool = True


class OpportunityMapItem(BaseModel):
    opportunity_id: str
    title: str
    problem_statement: str
    expected_value: str
    priority: PriorityBand
    dependencies: list[str] = Field(default_factory=list)


class DeliveryBlueprintPhase(BaseModel):
    phase_id: str
    title: str
    objectives: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class MaturityDimension(BaseModel):
    dimension: str
    current_level: MaturityLevel
    target_level: MaturityLevel
    gap_summary: str
    next_actions: list[str] = Field(default_factory=list)


class ChiefAIDigitalStrategyInput(BaseModel):
    engagement_name: str
    problem_statement: str
    business_context: str
    client_context: str = ""
    engagement_history: list[str] = Field(default_factory=list)
    process_areas: list[str] = Field(default_factory=list)
    data_assets: list[str] = Field(default_factory=list)
    current_stack: list[str] = Field(default_factory=list)
    delivery_constraints: list[str] = Field(default_factory=list)
    desired_outcomes: list[str] = Field(default_factory=list)


class ChiefAIDigitalStrategyOutput(BaseModel):
    mission_assessment: MissionAssessment
    context_signals: list[ContextSignal] = Field(default_factory=list)
    recommended_services: list[RecommendedService] = Field(default_factory=list)
    upsell_opportunities: list[UpsellOpportunity] = Field(default_factory=list)
    opportunity_map: list[OpportunityMapItem] = Field(default_factory=list)
    delivery_blueprint: list[DeliveryBlueprintPhase] = Field(default_factory=list)
    maturity_model: list[MaturityDimension] = Field(default_factory=list)
    executive_summary: str
    approval_required: bool = True
