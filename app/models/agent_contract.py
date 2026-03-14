from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


AgentDomain = Literal["corporate", "delivery", "platform"]
ApprovalClass = Literal["none", "bounded", "ceo_required"]
AgentStatus = Literal["idle", "running", "waiting", "blocked", "disabled"]
PrimaryTrack = Literal["track_a_internal", "track_b_client"]
ReplicationMode = Literal["none", "replicate_later"]
AgentPod = Literal["growth", "delivery", "ops", "executive", "specialist_overlay"]
OperatingMode = Literal["internal_operating", "client_delivery", "client_facing_service"]


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
            role_summary="Prepares research-backed draft recommendations for consulting engagements.",
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
