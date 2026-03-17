# Copyright (c) Dario Pizzolante
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.control_plane import ApprovalClass, AutonomyClass
from app.models.governed_metadata import GovernedMetadataSummary, build_governed_metadata_summary
from app.models.tool_profiles import TOOL_PROFILE_BINDING_MAP

AgentDomain = Literal["corporate", "delivery", "platform"]
AgentStatus = Literal["idle", "running", "waiting", "blocked", "disabled"]
PrimaryTrack = Literal["track_a_internal", "track_b_client"]
ReplicationMode = Literal["none", "replicate_later"]
AgentPod = Literal["growth", "delivery", "ops", "executive", "specialist_overlay"]
OperatingMode = Literal["internal_operating", "client_delivery", "client_facing_service"]

INTERNAL_ONLY_MODES = ["internal_operating"]
INTERNAL_AND_CLIENT_MODES = ["internal_operating", "client_delivery"]
INTERNAL_CLIENT_SERVICE_MODES = [
    "internal_operating",
    "client_delivery",
    "client_facing_service",
]


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
    pod: Optional[AgentPod] = None
    family_id: Optional[str] = None
    operating_modes: list[OperatingMode] = Field(default_factory=list)
    role_summary: str
    approval_class: ApprovalClass
    autonomy_class: AutonomyClass = "assistant"
    tool_profile_by_mode: dict[str, str] = Field(default_factory=dict)
    deployment: AgentDeploymentPolicy = Field(default_factory=AgentDeploymentPolicy)
    capabilities: list[AgentCapability] = Field(default_factory=list)
    kpis: list[AgentKPI] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    runtime: AgentRuntimeState = Field(default_factory=AgentRuntimeState)
    governed_metadata: Optional[GovernedMetadataSummary] = None


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
            role_summary=(
                "Acts like a client-facing technology consultant: analyzes the active mission, client context, "
                "and history to produce strategy options, architecture advice, service recommendations, and account-growth opportunities."
            ),
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
            inputs=[
                "problem statement",
                "client context/history",
                "current stack",
                "constraints",
                "architecture state",
            ],
            outputs=[
                "mission assessment",
                "context assessment",
                "service recommendations",
                "upsell opportunities",
                "strategy options",
                "architecture advice",
                "risk assessment",
            ],
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
            role_summary=(
                "Acts like a client-facing AI consultant: analyzes client missions, context, and history to build "
                "AI opportunity maps, delivery blueprints, maturity guidance, service recommendations, and account-growth opportunities."
            ),
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
            inputs=[
                "problem statement",
                "client context/history",
                "process context",
                "data landscape",
                "delivery constraints",
            ],
            outputs=[
                "mission assessment",
                "context assessment",
                "service recommendations",
                "upsell opportunities",
                "opportunity map",
                "AI/data blueprint",
                "maturity assessment",
                "delivery roadmap",
            ],
            constraints=[
                "no client-facing commitment without CEO approval",
                "replicate for Track 2 later instead of sharing Track 1 runtime state",
            ],
        ),
        AgentContract(
            agent_id="billing-agent",
            display_name="Billing Agent",
            domain="corporate",
            role_summary="Generates invoice packages from approved work and tracks collections follow-up.",
            approval_class="ceo_required",
            tools=["billing-records", "workspace", "reporting"],
            inputs=["approved timesheets", "deliverable records", "rate cards"],
            outputs=["invoice package", "reminder draft", "billing exception"],
            constraints=["no invoice release without CEO approval"],
        ),
        AgentContract(
            agent_id="finance-agent",
            display_name="Finance Agent",
            domain="corporate",
            role_summary="Produces cashflow snapshots and flags revenue, expense, or runway anomalies.",
            approval_class="bounded",
            tools=["finance-snapshots", "workspace"],
            inputs=["receivables", "payables", "cash position"],
            outputs=["finance snapshot", "risk flag", "runway note"],
            constraints=["no autonomous financial commitment"],
        ),
        AgentContract(
            agent_id="procurement-agent",
            display_name="Procurement Agent",
            domain="corporate",
            role_summary="Drafts purchase orders and validates budget thresholds before approval routing.",
            approval_class="ceo_required",
            tools=["budget-tracker", "workspace", "supplier-records"],
            inputs=["purchase request", "supplier details", "budget code"],
            outputs=["PO draft", "budget check", "policy exception"],
            constraints=["no external commitment without CEO approval"],
        ),
        AgentContract(
            agent_id="reporting-agent",
            display_name="Reporting Agent",
            domain="corporate",
            role_summary="Consolidates operational and delivery KPIs into weekly and monthly reports.",
            approval_class="bounded",
            tools=["reporting", "workspace", "dashboard"],
            inputs=["workflow metrics", "delivery KPIs", "finance KPIs"],
            outputs=["weekly report", "monthly report", "exception summary"],
            constraints=["reports are internal until approved for distribution"],
        ),
        AgentContract(
            agent_id="compliance-contract-agent",
            display_name="Compliance / Contract Agent",
            domain="corporate",
            role_summary="Tracks obligations, milestones, and legal/compliance deadlines for CEO review.",
            approval_class="ceo_required",
            tools=["contract-repository", "workspace", "calendar"],
            inputs=["contract terms", "milestones", "deadline trackers"],
            outputs=["obligation summary", "deadline alert", "review note"],
            constraints=["no legal commitment without CEO approval"],
        ),
        AgentContract(
            agent_id="document-agent",
            display_name="Document Agent",
            domain="corporate",
            role_summary="Classifies documents, extracts structured data, and routes them for processing.",
            approval_class="bounded",
            tools=["document-store", "classification", "workspace"],
            inputs=["document files", "metadata", "workflow context"],
            outputs=["document class", "extracted fields", "routing decision"],
            constraints=["escalate low-confidence extraction"],
        ),
        AgentContract(
            agent_id="knowledge-agent",
            display_name="Knowledge Agent",
            domain="delivery",
            role_summary="Answers grounded questions from internal documents with source evidence.",
            approval_class="bounded",
            tools=["knowledge-base", "retrieval", "workspace"],
            inputs=["question", "retrieved chunks", "business context"],
            outputs=["grounded answer", "citations", "knowledge gap"],
            constraints=["never invent facts outside retrieved evidence"],
        ),
        AgentContract(
            agent_id="pmo-project-control-agent",
            display_name="PMO / Project Control Agent",
            domain="delivery",
            pod="delivery",
            family_id="pmo-project-control",
            operating_modes=["internal_operating", "client_delivery", "client_facing_service"],
            role_summary=(
                "Acts as the project governance and control-tower role for milestones, RAID, "
                "steering summaries, slippage detection, and portfolio visibility."
            ),
            approval_class="bounded",
            deployment=AgentDeploymentPolicy(
                primary_track="track_a_internal",
                replication_mode="replicate_later",
                replication_notes=(
                    "Use a separate client-delivery instance for Track 2 or client-facing PMO "
                    "support rather than sharing the internal PMO runtime state."
                ),
            ),
            capabilities=[
                AgentCapability(
                    id="milestone-governance",
                    name="Milestone Governance",
                    description="Track milestones, dependencies, and slippage against the control plan.",
                ),
                AgentCapability(
                    id="raid-management",
                    name="RAID Management",
                    description="Maintain RAID signals, steering summaries, and escalation views.",
                ),
                AgentCapability(
                    id="portfolio-visibility",
                    name="Portfolio Visibility",
                    description="Summarize project health, action backlog, and capacity pressure.",
                ),
            ],
            kpis=[
                AgentKPI(
                    id="slippage-detection-lag",
                    name="Slippage Detection Lag",
                    unit="days",
                    description="Average time between a delivery slip emerging and being surfaced.",
                )
            ],
            tools=["project-plan", "calendar", "reporting", "workspace"],
            inputs=["milestones", "dependencies", "task state", "meeting notes", "timesheet data"],
            outputs=["steering summary", "RAID update", "escalation list", "portfolio dashboard"],
            constraints=[
                "escalate material delivery risk instead of committing externally",
                "client-facing commitments still require approval through workflow policy",
            ],
        ),
        AgentContract(
            agent_id="project-management-agent",
            display_name="Project Management / Delivery Coordination Agent",
            domain="delivery",
            pod="delivery",
            family_id="project-management-delivery-coordination",
            operating_modes=["internal_operating", "client_delivery", "client_facing_service"],
            role_summary=(
                "Keeps day-to-day execution moving by turning plans, meeting notes, and milestone "
                "decisions into active tasks, checkpoints, and follow-ups."
            ),
            approval_class="bounded",
            deployment=AgentDeploymentPolicy(
                primary_track="track_a_internal",
                replication_mode="replicate_later",
                replication_notes=(
                    "Track 1 may use an internal coordination instance, while Track 2 delivery work "
                    "uses a separate client-specific coordination instance."
                ),
            ),
            capabilities=[
                AgentCapability(
                    id="checkpoint-coordination",
                    name="Checkpoint Coordination",
                    description="Turn plans and meetings into next checkpoints, follow-ups, and reminders.",
                ),
                AgentCapability(
                    id="work-package-followup",
                    name="Work Package Follow-Up",
                    description="Track work-package readiness, pending actions, and stakeholder follow-up.",
                ),
            ],
            tools=["project-plan", "task-system", "calendar", "workspace"],
            inputs=["tasks", "milestones", "dependencies", "meeting notes"],
            outputs=["delivery forecast", "checkpoint plan", "action list", "readiness alert"],
            constraints=[
                "material plan changes require CEO review",
                "day-to-day coordination does not replace PMO governance or steering oversight",
            ],
        ),
        AgentContract(
            agent_id="delivery-agent",
            display_name="Delivery Agent",
            domain="delivery",
            role_summary="Tracks milestone readiness and orchestrates engagement delivery checklists.",
            approval_class="bounded",
            tools=["delivery-checklists", "workspace"],
            inputs=["milestones", "handoff state", "readiness signals"],
            outputs=["delivery checklist", "handoff status", "readiness alert"],
            constraints=["client-facing release requires approval"],
        ),
        AgentContract(
            agent_id="quality-management-agent",
            display_name="Quality Management Agent",
            domain="delivery",
            role_summary="Runs quality gates and enforces definition-of-done checks before release.",
            approval_class="ceo_required",
            tools=["quality-gates", "test-results", "workspace"],
            inputs=["acceptance criteria", "test evidence", "release candidate data"],
            outputs=["gate decision", "risk summary", "release note"],
            constraints=["failed gates block release"],
        ),
        AgentContract(
            agent_id="consulting-support-agent",
            display_name="Consulting Support Agent",
            domain="delivery",
            role_summary="Supports consulting engagements with research-backed recommendations, mission framing, and account-growth hypotheses.",
            approval_class="bounded",
            tools=["knowledge-base", "research", "workspace"],
            inputs=["customer scope", "internal context", "external research"],
            outputs=["recommendation draft", "evidence pack", "open questions"],
            constraints=["final client recommendations require review"],
        ),
        AgentContract(
            agent_id="documentation-agent",
            display_name="Documentation Agent",
            domain="delivery",
            role_summary="Generates and maintains versioned project documentation and handover packs.",
            approval_class="bounded",
            tools=["document-store", "templates", "workspace"],
            inputs=["project artifacts", "versions", "handover requirements"],
            outputs=["documentation pack", "gap list", "handover summary"],
            constraints=["client-facing handover requires approval"],
        ),
        AgentContract(
            agent_id="testing-qa-agent",
            display_name="Testing / QA Agent",
            domain="delivery",
            role_summary="Generates test plans, summarizes defects, and reports release readiness.",
            approval_class="bounded",
            tools=["test-results", "quality-gates", "workspace"],
            inputs=["test scope", "defects", "release candidate"],
            outputs=["test plan", "defect summary", "readiness signal"],
            constraints=["critical defects escalate immediately"],
        ),
        AgentContract(
            agent_id="ops-agent",
            display_name="Ops Agent",
            domain="delivery",
            role_summary="Supports runbooks, release execution hygiene, and internal operational checklists.",
            approval_class="bounded",
            tools=["runbooks", "deployment-checklists", "workspace"],
            inputs=["release plan", "runbook state", "ops tasks"],
            outputs=["ops checklist", "release note", "execution alert"],
            constraints=["no destructive production action without explicit approval"],
            runtime=AgentRuntimeState(status="disabled"),
        ),
    ]
)

AGENT_METADATA_OVERRIDES: dict[str, dict[str, object]] = {
    "email-agent": {
        "pod": "specialist_overlay",
        "family_id": "email",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "personal-assistant-agent": {
        "pod": "executive",
        "family_id": "personal-assistant",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "cto-cio-agent": {
        "pod": "specialist_overlay",
        "family_id": "cto-cio-advisory",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
    },
    "accountant-agent": {
        "pod": "specialist_overlay",
        "family_id": "accountant",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "cfo-agent": {
        "pod": "specialist_overlay",
        "family_id": "cfo",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "chief-ai-digital-strategy-agent": {
        "pod": "specialist_overlay",
        "family_id": "chief-ai-digital-strategy",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
    },
    "billing-agent": {
        "pod": "specialist_overlay",
        "family_id": "billing",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "finance-agent": {
        "pod": "specialist_overlay",
        "family_id": "finance",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "procurement-agent": {
        "pod": "specialist_overlay",
        "family_id": "procurement",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "reporting-agent": {
        "pod": "specialist_overlay",
        "family_id": "reporting",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
        "deployment": AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Internal reporting remains Track 1-owned. Client reporting support should run as a "
                "separate replicated instance with isolated tenant, delivery, and audit context."
            ),
        ),
    },
    "compliance-contract-agent": {
        "pod": "specialist_overlay",
        "family_id": "compliance-contract",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
    "document-agent": {
        "pod": "specialist_overlay",
        "family_id": "document",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
        "deployment": AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Document processing patterns may be reused for client work, but each client deployment "
                "must use a separate document-processing instance and isolated document store."
            ),
        ),
    },
    "knowledge-agent": {
        "pod": "specialist_overlay",
        "family_id": "knowledge",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
        "deployment": AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Knowledge retrieval may be reused for client delivery or client-facing services only "
                "through separate client-scoped instances with isolated retrieval stores."
            ),
        ),
    },
    "pmo-project-control-agent": {
        "pod": "delivery",
        "family_id": "pmo-project-control",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
    },
    "project-management-agent": {
        "pod": "delivery",
        "family_id": "project-management-delivery-coordination",
        "operating_modes": INTERNAL_CLIENT_SERVICE_MODES,
    },
    "delivery-agent": {
        "pod": "specialist_overlay",
        "family_id": "delivery",
        "operating_modes": INTERNAL_AND_CLIENT_MODES,
    },
    "quality-management-agent": {
        "pod": "specialist_overlay",
        "family_id": "quality-management",
        "operating_modes": INTERNAL_AND_CLIENT_MODES,
    },
    "consulting-support-agent": {
        "pod": "specialist_overlay",
        "family_id": "consulting-support",
        "operating_modes": INTERNAL_AND_CLIENT_MODES,
    },
    "documentation-agent": {
        "pod": "delivery",
        "family_id": "documentation",
        "operating_modes": INTERNAL_AND_CLIENT_MODES,
        "deployment": AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Documentation capability may be reused in client delivery, but each engagement must "
                "use its own scoped documentation instance and artifact boundary."
            ),
        ),
    },
    "testing-qa-agent": {
        "pod": "specialist_overlay",
        "family_id": "testing-qa",
        "operating_modes": INTERNAL_AND_CLIENT_MODES,
    },
    "ops-agent": {
        "pod": "specialist_overlay",
        "family_id": "ops-runbook",
        "operating_modes": INTERNAL_ONLY_MODES,
    },
}

AGENT_AUTONOMY_BY_ID: dict[str, AutonomyClass] = {
    "email-agent": "approval_gated",
    "personal-assistant-agent": "supervised_executor",
    "cto-cio-agent": "assistant",
    "accountant-agent": "supervised_executor",
    "cfo-agent": "assistant",
    "chief-ai-digital-strategy-agent": "assistant",
    "billing-agent": "approval_gated",
    "finance-agent": "assistant",
    "procurement-agent": "approval_gated",
    "reporting-agent": "assistant",
    "compliance-contract-agent": "approval_gated",
    "document-agent": "supervised_executor",
    "knowledge-agent": "assistant",
    "pmo-project-control-agent": "supervised_executor",
    "project-management-agent": "supervised_executor",
    "delivery-agent": "supervised_executor",
    "quality-management-agent": "approval_gated",
    "consulting-support-agent": "assistant",
    "documentation-agent": "supervised_executor",
    "testing-qa-agent": "supervised_executor",
    "ops-agent": "supervised_executor",
    "lead-intake-agent": "supervised_executor",
    "account-research-agent": "assistant",
    "qualification-agent": "assistant",
    "outreach-draft-agent": "assistant",
    "proposal-sow-agent": "approval_gated",
    "crm-hygiene-agent": "supervised_executor",
    "ba-requirements-agent": "assistant",
    "architect-agent": "assistant",
    "build-automation-agent": "supervised_executor",
    "qa-review-agent": "assistant",
    "finance-ops-agent": "supervised_executor",
    "invoice-receivables-agent": "supervised_executor",
    "vendor-procurement-agent": "approval_gated",
    "admin-hr-ops-agent": "supervised_executor",
    "company-reporting-agent": "supervised_executor",
    "ceo-briefing-agent": "assistant",
    "strategy-opportunity-agent": "assistant",
    "risk-watchdog-agent": "supervised_executor",
    "mission-control-agent": "supervised_executor",
}

ADDITIONAL_AGENT_CONTRACTS = [
    AgentContract(
        agent_id="lead-intake-agent",
        display_name="Lead Intake Agent",
        domain="corporate",
        pod="growth",
        family_id="lead-intake",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Ingests inbound lead signals, structures opportunity records, and starts the growth workflow.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="lead-capture",
                name="Lead Capture",
                description="Convert inbound lead signals into structured opportunity records.",
            ),
            AgentCapability(
                id="signal-extraction",
                name="Signal Extraction",
                description="Extract company, contact, urgency, and probable need signals from inbound requests.",
            ),
        ],
        tools=["mailbox", "forms", "crm", "workspace"],
        inputs=["lead email", "web form", "manual intake"],
        outputs=["opportunity card", "missing-info list", "confidence score"],
        constraints=["no autonomous external commitment", "unclear lead data should be flagged for review"],
    ),
    AgentContract(
        agent_id="account-research-agent",
        display_name="Account Research Agent",
        domain="corporate",
        pod="growth",
        family_id="account-research",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Enriches opportunities with account, market, and historical context before qualification or proposal work.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="account-enrichment",
                name="Account Enrichment",
                description="Build a concise account brief from external and internal context.",
            )
        ],
        tools=["research", "crm", "knowledge-base", "workspace"],
        inputs=["opportunity card", "company name", "prior interactions"],
        outputs=["account brief", "opportunity hypotheses", "research notes"],
        constraints=["research only; no autonomous outbound contact"],
    ),
    AgentContract(
        agent_id="qualification-agent",
        display_name="Qualification Agent",
        domain="corporate",
        pod="growth",
        family_id="qualification",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Scores fit, identifies commercial red flags, and recommends the next growth path.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="fit-scoring",
                name="Fit Scoring",
                description="Score leads against service fit, urgency, and likely value.",
            )
        ],
        tools=["crm", "service-catalog", "pricing-rules", "workspace"],
        inputs=["opportunity card", "account brief", "service catalog"],
        outputs=["qualification outcome", "red flags", "next-step recommendation"],
        constraints=["routing recommendations remain reviewable by the CEO"],
    ),
    AgentContract(
        agent_id="outreach-draft-agent",
        display_name="Outreach Draft Agent",
        domain="corporate",
        pod="growth",
        family_id="outreach-draft",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Drafts first responses and bounded follow-up messaging after qualification or stale-opportunity review.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="outreach-drafting",
                name="Outreach Drafting",
                description="Prepare personalized follow-up, discovery, and meeting request drafts.",
            )
        ],
        tools=["mailbox", "crm", "templates", "workspace"],
        inputs=["qualified opportunity", "account brief", "prior correspondence"],
        outputs=["reply draft", "follow-up sequence", "meeting-request draft"],
        constraints=["draft only by default", "sending remains approval-gated"],
    ),
    AgentContract(
        agent_id="proposal-sow-agent",
        display_name="Proposal / SOW Agent",
        domain="corporate",
        pod="growth",
        family_id="proposal-sow",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Turns discovery and pricing context into proposal, scope, and SOW drafts.",
        approval_class="ceo_required",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Proposal patterns may be reused in client-delivery or partner contexts only through "
                "separate scoped instances with isolated opportunity and pricing state."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="scope-drafting",
                name="Scope Drafting",
                description="Draft scope, assumptions, and exclusions from discovery context.",
            ),
            AgentCapability(
                id="sow-generation",
                name="SOW Generation",
                description="Prepare proposal and SOW drafts with explicit next steps and assumptions.",
            ),
        ],
        tools=["proposal-templates", "pricing-rules", "service-catalog", "workspace"],
        inputs=["discovery notes", "account brief", "pricing context", "desired outcomes"],
        outputs=["proposal draft", "sow draft", "effort estimate", "assumption list"],
        constraints=["pricing and external commitment require CEO approval"],
    ),
    AgentContract(
        agent_id="crm-hygiene-agent",
        display_name="CRM Hygiene Agent",
        domain="corporate",
        pod="growth",
        family_id="crm-hygiene",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Keeps pipeline records current, complete, and deduplicated so growth workflows stay trustworthy.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="crm-maintenance",
                name="CRM Maintenance",
                description="Detect stale, incomplete, or duplicated CRM records and correct them.",
            )
        ],
        tools=["crm", "mailbox", "calendar", "workspace"],
        inputs=["crm records", "email metadata", "meeting activity"],
        outputs=["updated record", "stale-lead alert", "missing-data reminder"],
        constraints=["no stage progression without sufficient source evidence"],
    ),
    AgentContract(
        agent_id="ba-requirements-agent",
        display_name="BA / Requirements Agent",
        domain="delivery",
        pod="delivery",
        family_id="ba-requirements",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Turns workshops, notes, and documents into structured requirements, acceptance criteria, and process understanding.",
        approval_class="bounded",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Requirements work may be reused for client delivery, but each project needs a separate "
                "requirements instance with isolated engagement context."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="requirements-structuring",
                name="Requirements Structuring",
                description="Organize raw needs into epics, stories, and acceptance criteria.",
            )
        ],
        tools=["transcripts", "document-store", "templates", "workspace"],
        inputs=["workshop notes", "client documents", "scope changes"],
        outputs=["requirements pack", "acceptance criteria", "open questions"],
        constraints=["surface ambiguity instead of inventing requirements"],
    ),
    AgentContract(
        agent_id="architect-agent",
        display_name="Architect Agent",
        domain="delivery",
        pod="delivery",
        family_id="architect",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Defines solution structure, options, and implementation design from requirements and delivery constraints.",
        approval_class="bounded",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Architecture work may be reused for client delivery or advisory services only through "
                "separate scoped instances with isolated project and tenant context."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="solution-design",
                name="Solution Design",
                description="Produce target architecture, option comparisons, and dependency mapping.",
            )
        ],
        tools=["architecture-docs", "diagrams", "standards-library", "workspace"],
        inputs=["requirements pack", "environment constraints", "existing-system context"],
        outputs=["architecture note", "option analysis", "dependency map", "risk note"],
        constraints=["major design choices require review before commitment"],
    ),
    AgentContract(
        agent_id="build-automation-agent",
        display_name="Build / Automation Agent",
        domain="delivery",
        pod="delivery",
        family_id="build-automation",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Implements code, scripts, automations, and configuration assets from approved design and work packages.",
        approval_class="bounded",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Implementation work may be reused across internal and client delivery, but each runtime "
                "must stay isolated by tenant, repository, secrets, and project state."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="automation-implementation",
                name="Automation Implementation",
                description="Create automation artifacts, connectors, and technical delivery assets.",
            )
        ],
        tools=["repository", "code-runtime", "workflow-engine", "workspace"],
        inputs=["approved work package", "architecture note", "requirements pack"],
        outputs=["code artifact", "automation asset", "implementation note"],
        constraints=["deployment remains separately gated", "production-impacting actions require approval"],
    ),
    AgentContract(
        agent_id="qa-review-agent",
        display_name="QA / Review Agent",
        domain="delivery",
        pod="delivery",
        family_id="qa-review",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Validates completeness, traceability, and release-readiness before milestone close or release.",
        approval_class="bounded",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "QA review may be reused for client delivery, but each engagement requires a separate "
                "review instance tied to that project's evidence and approval boundary."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="deliverable-review",
                name="Deliverable Review",
                description="Check deliverables against requirements, design, and quality expectations.",
            )
        ],
        tools=["quality-gates", "requirements", "design-docs", "workspace"],
        inputs=["release candidate", "requirements pack", "test evidence"],
        outputs=["review findings", "pass-fail summary", "remediation tasks"],
        constraints=["cannot independently approve commercial or legal commitments"],
    ),
    AgentContract(
        agent_id="finance-ops-agent",
        display_name="Finance Ops Agent",
        domain="corporate",
        pod="ops",
        family_id="finance-ops",
        operating_modes=INTERNAL_ONLY_MODES,
        role_summary="Runs internal finance control, margin analysis, and forecast-versus-actual review for company operations.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="margin-monitoring",
                name="Margin Monitoring",
                description="Track project margin drift, missing billable items, and finance-control exceptions.",
            )
        ],
        tools=["accounting-ledger", "crm", "reporting", "workspace"],
        inputs=["timesheets", "project plans", "invoices", "pricing context"],
        outputs=["margin report", "forecast update", "pricing sanity check"],
        constraints=["analysis only; no autonomous financial commitment"],
    ),
    AgentContract(
        agent_id="invoice-receivables-agent",
        display_name="Invoice / Receivables Agent",
        domain="corporate",
        pod="ops",
        family_id="invoice-receivables",
        operating_modes=INTERNAL_ONLY_MODES,
        role_summary="Prepares invoice packets, tracks receivables aging, and drafts payment follow-up actions.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="receivables-tracking",
                name="Receivables Tracking",
                description="Monitor overdue invoices and prepare payment reminder actions.",
            )
        ],
        tools=["accounting-ledger", "mailbox", "contracts", "workspace"],
        inputs=["billing milestones", "invoice records", "payment status"],
        outputs=["invoice packet", "aging report", "reminder draft"],
        constraints=["release of invoices or reminders remains policy-bound"],
    ),
    AgentContract(
        agent_id="vendor-procurement-agent",
        display_name="Vendor / Procurement Agent",
        domain="corporate",
        pod="ops",
        family_id="vendor-procurement",
        operating_modes=INTERNAL_ONLY_MODES,
        role_summary="Tracks vendors, renewals, procurement requests, and supporting approval data for internal operations.",
        approval_class="ceo_required",
        capabilities=[
            AgentCapability(
                id="vendor-control",
                name="Vendor Control",
                description="Track procurement requests, renewals, and supplier comparison notes.",
            )
        ],
        tools=["supplier-records", "budget-tracker", "contracts", "workspace"],
        inputs=["procurement request", "vendor profile", "budget context"],
        outputs=["vendor summary", "renewal alert", "approval packet"],
        constraints=["no external vendor commitment without approval"],
    ),
    AgentContract(
        agent_id="admin-hr-ops-agent",
        display_name="Admin / HR Ops Agent",
        domain="corporate",
        pod="ops",
        family_id="admin-hr-ops",
        operating_modes=INTERNAL_ONLY_MODES,
        role_summary="Supports bounded admin, onboarding, access, and people-ops workflows as the company scales.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="admin-task-packs",
                name="Admin Task Packs",
                description="Prepare onboarding, offboarding, and access-control task packs.",
            )
        ],
        tools=["directory", "task-system", "templates", "workspace"],
        inputs=["person-event", "role change", "access request"],
        outputs=["onboarding pack", "admin checklist", "access reminder"],
        constraints=["sensitive identity changes remain approval-bound"],
    ),
    AgentContract(
        agent_id="company-reporting-agent",
        display_name="Company Reporting Agent",
        domain="corporate",
        pod="ops",
        family_id="company-reporting",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Consolidates company KPIs across growth, delivery, finance, and receivables into management reporting packs.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="company-kpi-reporting",
                name="Company KPI Reporting",
                description="Build company-level dashboards and recurring executive KPI packs.",
            )
        ],
        tools=["reporting", "crm", "dashboard", "workspace"],
        inputs=["pipeline metrics", "delivery health", "receivables data", "finance signals"],
        outputs=["executive dashboard", "weekly pack", "risk summary"],
        constraints=["external distribution remains approval-bound"],
    ),
    AgentContract(
        agent_id="ceo-briefing-agent",
        display_name="CEO Briefing Agent",
        domain="platform",
        pod="executive",
        family_id="ceo-briefing",
        operating_modes=INTERNAL_ONLY_MODES,
        role_summary="Synthesizes what matters now across pods into a concise executive brief for the CEO.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="executive-synthesis",
                name="Executive Synthesis",
                description="Merge signals across growth, delivery, and ops into a concise leadership brief.",
            )
        ],
        tools=["dashboard", "workspace", "reporting", "run-state"],
        inputs=["growth summary", "delivery summary", "ops summary", "risk alerts"],
        outputs=["executive brief", "decision queue", "priority list"],
        constraints=["briefing only; no autonomous decisions"],
    ),
    AgentContract(
        agent_id="strategy-opportunity-agent",
        display_name="Strategy / Opportunity Agent",
        domain="platform",
        pod="executive",
        family_id="strategy-opportunity",
        operating_modes=["internal_operating", "client_facing_service"],
        role_summary="Looks for productization, repeatability, and strategic growth opportunities across the business.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="strategic-pattern-detection",
                name="Strategic Pattern Detection",
                description="Identify repeatable offers, productization patterns, and growth bets.",
            )
        ],
        tools=["roadmap", "reporting", "workspace", "knowledge-base"],
        inputs=["deal history", "margin data", "delivery patterns", "market notes"],
        outputs=["opportunity memo", "productization ideas", "strategy recommendation"],
        constraints=["recommendation only; no autonomous strategic commitment"],
    ),
    AgentContract(
        agent_id="risk-watchdog-agent",
        display_name="Risk / Watchdog Agent",
        domain="platform",
        pod="executive",
        family_id="risk-watchdog",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Detects, summarizes, and escalates operational, delivery, commercial, or runtime risks across pods.",
        approval_class="bounded",
        capabilities=[
            AgentCapability(
                id="risk-detection",
                name="Risk Detection",
                description="Monitor for slippage, missing approvals, weak documentation, and anomalous signals.",
            )
        ],
        tools=["reporting", "workspace", "run-state", "approval-state"],
        inputs=["delivery signals", "finance signals", "approval queue", "workflow logs"],
        outputs=["risk alert", "escalation recommendation", "risk-register entry"],
        constraints=["alerts only; never executes punitive or irreversible action"],
    ),
    AgentContract(
        agent_id="mission-control-agent",
        display_name="Mission Control Agent",
        domain="platform",
        pod="executive",
        family_id="mission-control",
        operating_modes=INTERNAL_AND_CLIENT_MODES,
        role_summary="Supervises runs, approvals, escalations, and runtime visibility across the operating model.",
        approval_class="bounded",
        deployment=AgentDeploymentPolicy(
            primary_track="track_a_internal",
            replication_mode="replicate_later",
            replication_notes=(
                "Mission Control may supervise Track 1 and later Track 2 environments, but client "
                "supervision must run as a separate tenant-scoped supervisor instance."
            ),
        ),
        capabilities=[
            AgentCapability(
                id="run-supervision",
                name="Run Supervision",
                description="Track workflow status, approval bottlenecks, and escalations across pods.",
            )
        ],
        tools=["workflow-engine", "dashboard", "approval-state", "run-state"],
        inputs=["workflow run status", "approval queue", "exception events"],
        outputs=["mission-control view", "escalation list", "approval backlog"],
        constraints=["operational supervision only; subordinate to workflow and approval policy"],
    ),
]

for agent in DEFAULT_AGENT_REGISTRY.agents:
    override = AGENT_METADATA_OVERRIDES.get(agent.agent_id)
    if override is None:
        continue
    agent.pod = override.get("pod", agent.pod)
    agent.family_id = override.get("family_id", agent.family_id)
    agent.operating_modes = list(override.get("operating_modes", agent.operating_modes))
    if "deployment" in override:
        agent.deployment = override["deployment"]  # type: ignore[assignment]

existing_agent_ids = {agent.agent_id for agent in DEFAULT_AGENT_REGISTRY.agents}
for agent in ADDITIONAL_AGENT_CONTRACTS:
    if agent.agent_id not in existing_agent_ids:
        DEFAULT_AGENT_REGISTRY.agents.append(agent)

for agent in DEFAULT_AGENT_REGISTRY.agents:
    autonomy_class = AGENT_AUTONOMY_BY_ID.get(agent.agent_id)
    if autonomy_class is not None:
        agent.autonomy_class = autonomy_class
    if agent.family_id:
        tool_profile_by_mode: dict[str, str] = {}
        for operating_mode in agent.operating_modes:
            profile_id = TOOL_PROFILE_BINDING_MAP.get((agent.family_id, operating_mode))
            if profile_id:
                tool_profile_by_mode[operating_mode] = profile_id
        if tool_profile_by_mode:
            agent.tool_profile_by_mode = tool_profile_by_mode
    agent.governed_metadata = build_governed_metadata_summary(
        pod=agent.pod,
        family_id=agent.family_id,
        primary_track=agent.deployment.primary_track,
        operating_modes=agent.operating_modes,
        approval_class=agent.approval_class,
        autonomy_class=agent.autonomy_class,
        replication_mode=agent.deployment.replication_mode,
        tool_profile_by_mode=agent.tool_profile_by_mode,
    )
