# Copyright (c) Dario Pizzolante
from typing import Literal

from pydantic import BaseModel, Field


OperatingMode = Literal["internal_operating", "client_delivery", "client_facing_service"]
NormalizedToolId = Literal[
    "email.read",
    "email.draft",
    "email.send_internal",
    "email.send_external",
    "calendar.read",
    "calendar.write",
    "meetings.ingest_transcript",
    "crm.read",
    "crm.write",
    "contacts.read",
    "proposals.read_template",
    "pricing.read_rules",
    "pricing.run_estimate",
    "research.web_search",
    "pm.read",
    "pm.write",
    "tasks.read",
    "tasks.write",
    "docs.read",
    "docs.write",
    "repo.read",
    "repo.write",
    "code.run_sandbox",
    "workflow.deploy_nonprod",
    "finance.read",
    "finance.write_draft",
    "invoices.generate_draft",
    "payments.read",
    "vendors.read",
    "vendors.write",
    "hr.read",
    "hr.write_limited",
    "memory.search",
    "memory.write",
    "state.read",
    "state.write",
    "approval.request",
    "reporting.generate",
    "audit.log",
]


class ToolPermissionProfile(BaseModel):
    profile_id: str
    allowed_tools: list[NormalizedToolId] = Field(default_factory=list)
    approval_gated_tools: list[NormalizedToolId] = Field(default_factory=list)
    notes: str


class ToolProfileBinding(BaseModel):
    family_id: str
    operating_mode: OperatingMode
    profile_id: str


class ToolProfileRegistry(BaseModel):
    profiles: list[ToolPermissionProfile] = Field(default_factory=list)
    bindings: list[ToolProfileBinding] = Field(default_factory=list)


def _profile(
    profile_id: str,
    *,
    allowed: list[NormalizedToolId],
    gated: list[NormalizedToolId] | None = None,
    notes: str,
) -> ToolPermissionProfile:
    return ToolPermissionProfile(
        profile_id=profile_id,
        allowed_tools=allowed,
        approval_gated_tools=gated or [],
        notes=notes,
    )


def _bind(
    family_ids: list[str],
    operating_modes: list[OperatingMode],
    profile_id: str,
) -> list[ToolProfileBinding]:
    bindings: list[ToolProfileBinding] = []
    for family_id in family_ids:
        for operating_mode in operating_modes:
            bindings.append(
                ToolProfileBinding(
                    family_id=family_id,
                    operating_mode=operating_mode,
                    profile_id=profile_id,
                )
            )
    return bindings


DEFAULT_TOOL_PROFILE_REGISTRY = ToolProfileRegistry(
    profiles=[
        _profile(
            "email-internal",
            allowed=["email.read", "email.draft", "memory.search", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["email.send_external"],
            notes="Email drafting and approval preparation for internal operator workflows.",
        ),
        _profile(
            "personal-assistant-internal",
            allowed=["email.read", "calendar.read", "memory.search", "state.read", "reporting.generate", "audit.log"],
            gated=["calendar.write", "email.send_external"],
            notes="Read-heavy daily coordination profile for the CEO assistant.",
        ),
        _profile(
            "growth-intake",
            allowed=["email.read", "crm.read", "crm.write", "contacts.read", "state.read", "state.write", "audit.log"],
            gated=["crm.write"],
            notes="Lead capture and CRM structuring for growth intake.",
        ),
        _profile(
            "growth-research",
            allowed=["crm.read", "contacts.read", "research.web_search", "memory.search", "state.read", "audit.log"],
            notes="Research and enrichment profile without outbound action rights.",
        ),
        _profile(
            "growth-qualification",
            allowed=["crm.read", "crm.write", "pricing.read_rules", "state.read", "state.write", "audit.log"],
            gated=["crm.write"],
            notes="Qualification profile for fit scoring and next-step routing.",
        ),
        _profile(
            "growth-outreach",
            allowed=["email.read", "email.draft", "crm.read", "crm.write", "contacts.read", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["email.send_external", "crm.write"],
            notes="Outreach drafting profile with approval-gated outbound commitments.",
        ),
        _profile(
            "growth-proposal",
            allowed=["proposals.read_template", "pricing.read_rules", "pricing.run_estimate", "docs.read", "docs.write", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["docs.write"],
            notes="Proposal and SOW preparation profile with pricing and document-authoring access.",
        ),
        _profile(
            "delivery-governance-internal",
            allowed=["pm.read", "pm.write", "tasks.read", "tasks.write", "docs.read", "docs.write", "finance.read", "reporting.generate", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["pm.write", "docs.write"],
            notes="Internal PMO profile with delivery governance and company-level finance visibility.",
        ),
        _profile(
            "delivery-governance-client",
            allowed=["pm.read", "pm.write", "tasks.read", "tasks.write", "docs.read", "docs.write", "reporting.generate", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["pm.write", "docs.write"],
            notes="Client-delivery PMO profile without company finance visibility.",
        ),
        _profile(
            "delivery-coordination",
            allowed=["pm.read", "tasks.read", "tasks.write", "docs.read", "docs.write", "calendar.read", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["tasks.write", "docs.write", "calendar.write"],
            notes="Execution-follow-up profile for delivery coordination and checkpoints.",
        ),
        _profile(
            "delivery-analysis",
            allowed=["meetings.ingest_transcript", "docs.read", "docs.write", "pm.read", "state.read", "state.write", "memory.search", "approval.request", "audit.log"],
            gated=["docs.write"],
            notes="Requirements and architecture analysis profile for delivery specialists.",
        ),
        _profile(
            "delivery-build",
            allowed=["repo.read", "repo.write", "docs.read", "docs.write", "code.run_sandbox", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["repo.write", "workflow.deploy_nonprod"],
            notes="Implementation profile for build and automation work with approval-gated writes and deployments.",
        ),
        _profile(
            "delivery-qa",
            allowed=["docs.read", "pm.read", "tasks.read", "repo.read", "reporting.generate", "state.read", "approval.request", "audit.log"],
            notes="Validation and release-readiness profile for QA and quality review roles.",
        ),
        _profile(
            "delivery-documentation",
            allowed=["docs.read", "docs.write", "pm.read", "tasks.read", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["docs.write"],
            notes="Documentation and handover packaging profile for delivery teams.",
        ),
        _profile(
            "ops-finance",
            allowed=["finance.read", "finance.write_draft", "invoices.generate_draft", "payments.read", "reporting.generate", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["finance.write_draft", "invoices.generate_draft"],
            notes="Internal finance operations profile for billing, forecasting, and receivables support.",
        ),
        _profile(
            "ops-vendor-admin",
            allowed=["vendors.read", "vendors.write", "finance.read", "hr.read", "hr.write_limited", "docs.read", "docs.write", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["vendors.write", "hr.write_limited", "docs.write"],
            notes="Internal vendor, procurement, admin, and HR operations profile.",
        ),
        _profile(
            "ops-reporting-internal",
            allowed=["crm.read", "pm.read", "finance.read", "reporting.generate", "memory.search", "state.read", "audit.log"],
            notes="Internal company reporting profile across growth, delivery, and finance inputs.",
        ),
        _profile(
            "ops-reporting-client",
            allowed=["pm.read", "reporting.generate", "memory.search", "state.read", "audit.log"],
            notes="Client reporting profile constrained to delivery-side context.",
        ),
        _profile(
            "executive-briefing",
            allowed=["reporting.generate", "memory.search", "state.read", "audit.log"],
            notes="Executive synthesis profile for briefing and leadership visibility.",
        ),
        _profile(
            "executive-strategy",
            allowed=["crm.read", "pm.read", "finance.read", "reporting.generate", "research.web_search", "memory.search", "state.read", "approval.request", "audit.log"],
            notes="Strategy and opportunity profile across growth, delivery, and financial context.",
        ),
        _profile(
            "executive-risk",
            allowed=["pm.read", "finance.read", "reporting.generate", "state.read", "approval.request", "audit.log"],
            notes="Risk detection and escalation profile across workflow, delivery, and finance signals.",
        ),
        _profile(
            "mission-control",
            allowed=["state.read", "approval.request", "reporting.generate", "audit.log"],
            notes="Supervision profile for run visibility, escalations, and approval backlog monitoring.",
        ),
        _profile(
            "specialist-accounting",
            allowed=["finance.read", "finance.write_draft", "payments.read", "reporting.generate", "state.read", "approval.request", "audit.log"],
            gated=["finance.write_draft"],
            notes="Accounting and reconciliation profile for internal specialist overlays.",
        ),
        _profile(
            "specialist-finance",
            allowed=["finance.read", "payments.read", "reporting.generate", "memory.search", "state.read", "approval.request", "audit.log"],
            notes="Finance analysis profile for CFO and finance specialist roles.",
        ),
        _profile(
            "specialist-reporting-internal",
            allowed=["crm.read", "pm.read", "finance.read", "reporting.generate", "memory.search", "state.read", "audit.log"],
            notes="Internal reporting specialist profile.",
        ),
        _profile(
            "specialist-reporting-client",
            allowed=["pm.read", "reporting.generate", "memory.search", "state.read", "audit.log"],
            notes="Client-facing reporting specialist profile with delivery-only scope.",
        ),
        _profile(
            "specialist-compliance",
            allowed=["docs.read", "calendar.read", "state.read", "approval.request", "audit.log"],
            notes="Compliance and contract-monitoring profile for internal obligations and deadlines.",
        ),
        _profile(
            "specialist-knowledge-internal",
            allowed=["docs.read", "memory.search", "state.read", "audit.log"],
            notes="Internal knowledge retrieval profile.",
        ),
        _profile(
            "specialist-knowledge-client",
            allowed=["docs.read", "memory.search", "state.read", "audit.log"],
            notes="Client-delivery knowledge retrieval profile over isolated client corpora.",
        ),
        _profile(
            "specialist-knowledge-service",
            allowed=["docs.read", "memory.search", "state.read", "approval.request", "audit.log"],
            notes="Client-facing knowledge-assistant profile with bounded service outputs.",
        ),
        _profile(
            "specialist-document-internal",
            allowed=["docs.read", "docs.write", "state.read", "state.write", "audit.log"],
            gated=["docs.write"],
            notes="Internal document processing profile.",
        ),
        _profile(
            "specialist-document-client",
            allowed=["docs.read", "docs.write", "state.read", "state.write", "audit.log"],
            gated=["docs.write"],
            notes="Client document processing profile with isolated tenant boundaries.",
        ),
        _profile(
            "specialist-document-service",
            allowed=["docs.read", "docs.write", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["docs.write"],
            notes="Client-facing document operations profile for bounded service execution.",
        ),
        _profile(
            "specialist-advisory",
            allowed=["docs.read", "repo.read", "reporting.generate", "research.web_search", "memory.search", "state.read", "approval.request", "audit.log"],
            notes="Advisory specialist profile for CTO/CIO, Chief AI, and consulting-support roles.",
        ),
        _profile(
            "specialist-delivery",
            allowed=["pm.read", "tasks.read", "docs.read", "docs.write", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["docs.write"],
            notes="Delivery specialist overlay profile for generic delivery coordination wrappers.",
        ),
        _profile(
            "specialist-quality",
            allowed=["docs.read", "pm.read", "tasks.read", "reporting.generate", "state.read", "approval.request", "audit.log"],
            notes="Quality-management gating profile for specialist overlay roles.",
        ),
        _profile(
            "specialist-testing",
            allowed=["docs.read", "repo.read", "reporting.generate", "state.read", "approval.request", "audit.log"],
            notes="Testing and QA specialist profile for evidence review and release readiness.",
        ),
        _profile(
            "ops-runbook",
            allowed=["docs.read", "docs.write", "repo.read", "state.read", "state.write", "approval.request", "audit.log"],
            gated=["workflow.deploy_nonprod", "docs.write"],
            notes="Runbook and operational hygiene profile for internal ops support.",
        ),
    ],
    bindings=(
        _bind(["email"], ["internal_operating"], "email-internal")
        + _bind(["personal-assistant"], ["internal_operating"], "personal-assistant-internal")
        + _bind(["lead-intake"], ["internal_operating", "client_delivery"], "growth-intake")
        + _bind(["account-research"], ["internal_operating", "client_delivery"], "growth-research")
        + _bind(["qualification"], ["internal_operating", "client_delivery"], "growth-qualification")
        + _bind(["outreach-draft"], ["internal_operating", "client_delivery"], "growth-outreach")
        + _bind(["proposal-sow"], ["internal_operating", "client_delivery"], "growth-proposal")
        + _bind(["crm-hygiene"], ["internal_operating", "client_delivery"], "growth-qualification")
        + _bind(["pmo-project-control"], ["internal_operating"], "delivery-governance-internal")
        + _bind(["pmo-project-control"], ["client_delivery", "client_facing_service"], "delivery-governance-client")
        + _bind(["project-management-delivery-coordination"], ["internal_operating", "client_delivery", "client_facing_service"], "delivery-coordination")
        + _bind(["ba-requirements", "architect"], ["internal_operating", "client_delivery"], "delivery-analysis")
        + _bind(["build-automation"], ["internal_operating", "client_delivery"], "delivery-build")
        + _bind(["qa-review"], ["internal_operating", "client_delivery"], "delivery-qa")
        + _bind(["documentation"], ["internal_operating", "client_delivery"], "delivery-documentation")
        + _bind(["finance-ops", "invoice-receivables"], ["internal_operating"], "ops-finance")
        + _bind(["vendor-procurement", "admin-hr-ops"], ["internal_operating"], "ops-vendor-admin")
        + _bind(["company-reporting"], ["internal_operating"], "ops-reporting-internal")
        + _bind(["company-reporting"], ["client_delivery"], "ops-reporting-client")
        + _bind(["ceo-briefing"], ["internal_operating"], "executive-briefing")
        + _bind(["strategy-opportunity"], ["internal_operating", "client_facing_service"], "executive-strategy")
        + _bind(["risk-watchdog"], ["internal_operating", "client_delivery"], "executive-risk")
        + _bind(["mission-control"], ["internal_operating", "client_delivery"], "mission-control")
        + _bind(["accountant"], ["internal_operating"], "specialist-accounting")
        + _bind(["cfo", "finance"], ["internal_operating"], "specialist-finance")
        + _bind(["reporting"], ["internal_operating"], "specialist-reporting-internal")
        + _bind(["reporting"], ["client_delivery", "client_facing_service"], "specialist-reporting-client")
        + _bind(["compliance-contract"], ["internal_operating"], "specialist-compliance")
        + _bind(["knowledge"], ["internal_operating"], "specialist-knowledge-internal")
        + _bind(["knowledge"], ["client_delivery"], "specialist-knowledge-client")
        + _bind(["knowledge"], ["client_facing_service"], "specialist-knowledge-service")
        + _bind(["document"], ["internal_operating"], "specialist-document-internal")
        + _bind(["document"], ["client_delivery"], "specialist-document-client")
        + _bind(["document"], ["client_facing_service"], "specialist-document-service")
        + _bind(["cto-cio-advisory", "chief-ai-digital-strategy", "consulting-support"], ["internal_operating", "client_delivery", "client_facing_service"], "specialist-advisory")
        + _bind(["delivery"], ["internal_operating", "client_delivery"], "specialist-delivery")
        + _bind(["quality-management"], ["internal_operating", "client_delivery"], "specialist-quality")
        + _bind(["testing-qa"], ["internal_operating", "client_delivery"], "specialist-testing")
        + _bind(["billing"], ["internal_operating"], "ops-finance")
        + _bind(["procurement"], ["internal_operating"], "ops-vendor-admin")
        + _bind(["ops-runbook"], ["internal_operating"], "ops-runbook")
    ),
)

TOOL_PROFILE_BY_ID = {profile.profile_id: profile for profile in DEFAULT_TOOL_PROFILE_REGISTRY.profiles}
TOOL_PROFILE_BINDING_MAP = {
    (binding.family_id, binding.operating_mode): binding.profile_id
    for binding in DEFAULT_TOOL_PROFILE_REGISTRY.bindings
}
