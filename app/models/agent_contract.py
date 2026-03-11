from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


AgentDomain = Literal["corporate", "delivery", "platform"]
ApprovalClass = Literal["none", "bounded", "ceo_required"]
AgentStatus = Literal["idle", "running", "waiting", "blocked", "disabled"]
PrimaryTrack = Literal["track_a_internal", "track_b_client"]
ReplicationMode = Literal["none", "replicate_later"]


class AgentCapability(BaseModel):
    id: str
    name: str
    description: str


class AgentKPI(BaseModel):
    id: str
    name: str
    unit: str
    description: str


class AgentRuntimeState(BaseModel):
    status: AgentStatus = "idle"
    last_run_at: Optional[datetime] = None
    current_task: Optional[str] = None
    last_error: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentDeploymentPolicy(BaseModel):
    primary_track: PrimaryTrack = "track_a_internal"
    replication_mode: ReplicationMode = "none"
    replication_notes: Optional[str] = None


class AgentContract(BaseModel):
    agent_id: str
    display_name: str
    domain: AgentDomain
    role_summary: str
    approval_class: ApprovalClass
    deployment: AgentDeploymentPolicy = Field(default_factory=AgentDeploymentPolicy)
    capabilities: list[AgentCapability] = Field(default_factory=list)
    kpis: list[AgentKPI] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    runtime: AgentRuntimeState = Field(default_factory=AgentRuntimeState)


class AgentRegistry(BaseModel):
    agents: list[AgentContract] = Field(default_factory=list)


DEFAULT_AGENT_REGISTRY = AgentRegistry(
    agents=[
        AgentContract(
            agent_id="email-agent",
            display_name="Email Agent",
            domain="corporate",
            role_summary="Classifies inbound emails, drafts replies, and routes approvals.",
            approval_class="ceo_required",
            capabilities=[
                AgentCapability(
                    id="classify-email",
                    name="Classify Email",
                    description="Classify inbound email intent and urgency.",
                ),
                AgentCapability(
                    id="draft-reply",
                    name="Draft Reply",
                    description="Draft a grounded response for review.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="email-turnaround",
                    name="Email Turnaround",
                    unit="minutes",
                    description="Average time to produce an approval-ready draft.",
                )
            ],
            tools=["mailbox", "retrieval", "logging"],
            inputs=["email subject", "email body", "thread context"],
            outputs=["intent", "confidence", "draft reply", "approval request"],
            constraints=["no autonomous sending", "escalate low-confidence cases"],
        ),
        AgentContract(
            agent_id="personal-assistant-agent",
            display_name="Personal Assistant Agent",
            domain="corporate",
            role_summary="Builds a prioritized daily list from inbox and calendar context.",
            approval_class="bounded",
            capabilities=[
                AgentCapability(
                    id="daily-prioritization",
                    name="Daily Prioritization",
                    description="Create a ranked action list for the CEO.",
                ),
                AgentCapability(
                    id="schedule-conflict-detection",
                    name="Schedule Conflict Detection",
                    description="Find deadline and calendar conflicts.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="priority-accuracy",
                    name="Priority Accuracy",
                    unit="percent",
                    description="Share of daily priorities accepted without manual reshuffling.",
                )
            ],
            tools=["mailbox", "calendar", "workspace"],
            inputs=["calendar events", "inbox metadata", "task state"],
            outputs=["daily action list", "conflict alerts", "prep notes"],
            constraints=["no external commitments without CEO approval"],
        ),
        AgentContract(
            agent_id="cto-cio-agent",
            display_name="CTO/CIO Agent",
            domain="platform",
            role_summary="Produces strategy options, architecture advice, and internal improvement backlog items.",
            approval_class="ceo_required",
            deployment=AgentDeploymentPolicy(
                primary_track="track_a_internal",
                replication_mode="replicate_later",
                replication_notes=(
                    "Track 1 owns the live internal instance. A separate Track 2 variant may be "
                    "replicated later for client-facing CIO/CTO advisory services without sharing state."
                ),
            ),
            capabilities=[
                AgentCapability(
                    id="architecture-counsel",
                    name="Architecture Counsel",
                    description="Produce architecture options and trade-offs.",
                ),
                AgentCapability(
                    id="platform-improvement",
                    name="Platform Improvement",
                    description="Recommend improvements to the internal platform.",
                ),
                AgentCapability(
                    id="strategy-options",
                    name="Strategy Options",
                    description="Compare technology strategy paths, constraints, and sequencing.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="improvement-throughput",
                    name="Improvement Throughput",
                    unit="items/month",
                    description="Number of accepted platform improvement items per month.",
                )
            ],
            tools=["knowledge-base", "roadmap", "architecture-docs"],
            inputs=["client scope", "platform telemetry", "architecture state"],
            outputs=["strategy options", "architecture advice", "improvement backlog", "risk assessment"],
            constraints=["no direct production changes", "CEO approval for roadmap commitments"],
        ),
        AgentContract(
            agent_id="accountant-agent",
            display_name="Accountant Agent",
            domain="corporate",
            role_summary="Enforces bookkeeping consistency, reconciliation rules, and close-readiness controls.",
            approval_class="bounded",
            capabilities=[
                AgentCapability(
                    id="ledger-reconciliation",
                    name="Ledger Reconciliation",
                    description="Detect mismatches between invoices, payments, expenses, and journal records.",
                ),
                AgentCapability(
                    id="close-checklist",
                    name="Close Checklist",
                    description="Generate accounting close tasks, blockers, and accounting-ready exports.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="reconciliation-lag",
                    name="Reconciliation Lag",
                    unit="days",
                    description="Average age of unresolved reconciliation exceptions.",
                )
            ],
            tools=["accounting-ledger", "workspace", "reporting"],
            inputs=["ledger entries", "invoice records", "payment records", "expense records"],
            outputs=["reconciliation exceptions", "close checklist", "export package"],
            constraints=[
                "no autonomous money movement",
                "CEO review required for material unresolved exceptions",
            ],
        ),
        AgentContract(
            agent_id="cfo-agent",
            display_name="CFO Agent",
            domain="corporate",
            role_summary="Produces scenario planning, cashflow risk analysis, and financial decision options for the CEO.",
            approval_class="ceo_required",
            capabilities=[
                AgentCapability(
                    id="scenario-planning",
                    name="Scenario Planning",
                    description="Model pricing, cost, hiring, and investment scenarios.",
                ),
                AgentCapability(
                    id="cashflow-risk",
                    name="Cashflow Risk",
                    description="Interpret runway pressure, profitability drift, and mitigation options.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="decision-readiness",
                    name="Decision Readiness",
                    unit="reviews/month",
                    description="Number of CEO-ready finance decision packs produced per month.",
                )
            ],
            tools=["finance-snapshots", "billing", "reporting"],
            inputs=["financial KPIs", "forecast assumptions", "delivery pipeline"],
            outputs=["scenario options", "cashflow recommendations", "decision memo"],
            constraints=[
                "recommendations only, no autonomous commitments",
                "CEO approval required for pricing, hiring, and investment decisions",
            ],
        ),
        AgentContract(
            agent_id="chief-ai-digital-strategy-agent",
            display_name="Chief AI / Digital Strategy Agent",
            domain="platform",
            role_summary="Builds AI opportunity maps, delivery blueprints, and maturity improvement plans.",
            approval_class="ceo_required",
            deployment=AgentDeploymentPolicy(
                primary_track="track_a_internal",
                replication_mode="replicate_later",
                replication_notes=(
                    "Track 1 owns the internal advisory pattern. A separate Track 2 variant may be "
                    "replicated later for client consulting offers without sharing company memory or context."
                ),
            ),
            capabilities=[
                AgentCapability(
                    id="ai-opportunity-mapping",
                    name="AI Opportunity Mapping",
                    description="Identify and prioritize AI, data, and digitalization opportunities.",
                ),
                AgentCapability(
                    id="delivery-blueprint",
                    name="Delivery Blueprint",
                    description="Translate scope into phased AI/data implementation plans.",
                ),
                AgentCapability(
                    id="maturity-assessment",
                    name="Maturity Assessment",
                    description="Assess AI and digital capability maturity and recommend next steps.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="opportunity-conversion",
                    name="Opportunity Conversion",
                    unit="percent",
                    description="Share of high-priority AI opportunities that progress into approved delivery plans.",
                )
            ],
            tools=["knowledge-base", "delivery-roadmap", "architecture-docs", "workspace"],
            inputs=["customer scope", "process context", "data landscape", "delivery constraints"],
            outputs=["opportunity map", "AI/data blueprint", "maturity assessment", "delivery roadmap"],
            constraints=[
                "no client-facing commitment without CEO approval",
                "replicate for Track 2 later instead of sharing Track 1 runtime state",
            ],
        ),
    ]
)
