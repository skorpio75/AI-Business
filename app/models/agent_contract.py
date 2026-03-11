from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


AgentDomain = Literal["corporate", "delivery", "platform"]
ApprovalClass = Literal["none", "bounded", "ceo_required"]
AgentStatus = Literal["idle", "running", "waiting", "blocked", "disabled"]


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


class AgentContract(BaseModel):
    agent_id: str
    display_name: str
    domain: AgentDomain
    role_summary: str
    approval_class: ApprovalClass
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
            role_summary="Advises on technology architecture and internal platform improvement.",
            approval_class="ceo_required",
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
            outputs=["architecture advice", "improvement backlog", "risk assessment"],
            constraints=["no direct production changes", "CEO approval for roadmap commitments"],
        ),
    ]
)
