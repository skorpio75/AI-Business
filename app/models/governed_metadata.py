# Copyright (c) Dario Pizzolante
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.control_plane import ApprovalClass, AutonomyClass, TrackId
from app.models.tool_profiles import DEFAULT_TOOL_PROFILE_REGISTRY, OperatingMode

RoutingPosture = Literal["DO-C", "DO-G", "GW-R", "DT-H", "UNSPECIFIED"]
ReplicationMode = Literal["none", "replicate_later"]
AgentPod = Literal["growth", "delivery", "ops", "executive", "specialist_overlay"]

MODE_LABELS: dict[OperatingMode, str] = {
    "internal_operating": "Internal operating",
    "client_delivery": "Client delivery",
    "client_facing_service": "Client-facing service",
}
TRACK_LABELS: dict[TrackId, str] = {
    "track_a_internal": "Track A internal",
    "track_b_client": "Track B client",
}
APPROVAL_LABELS: dict[ApprovalClass, str] = {
    "none": "No approval gate",
    "bounded": "Bounded approval",
    "ceo_required": "CEO approval required",
}
AUTONOMY_LABELS: dict[AutonomyClass, str] = {
    "assistant": "Assistant",
    "supervised_executor": "Supervised executor",
    "bounded_autonomous": "Bounded autonomous",
    "approval_gated": "Approval gated",
}
REPLICATION_LABELS: dict[ReplicationMode, str] = {
    "none": "No replication",
    "replicate_later": "Replicate later",
}
POD_LABELS: dict[AgentPod, str] = {
    "growth": "Growth",
    "delivery": "Delivery",
    "ops": "Ops",
    "executive": "Executive",
    "specialist_overlay": "Specialist overlay",
}
ROUTING_POSTURE_LABELS: dict[RoutingPosture, str] = {
    "DO-C": "Direct Ollama / compact local-first",
    "DO-G": "Direct Ollama with guarded drafting",
    "GW-R": "Governed LiteLLM / ModelGateway reasoning",
    "DT-H": "Deterministic or tool-first hybrid",
    "UNSPECIFIED": "Routing posture not yet governed",
}
ROUTING_POSTURE_SUMMARIES: dict[RoutingPosture, str] = {
    "DO-C": "Best for bounded internal reasoning, grounded answers, and compact local-first execution.",
    "DO-G": "Best for approval-sensitive drafting where local-first speed still needs stronger output guardrails.",
    "GW-R": "Best for richer client or cross-domain reasoning routed through the governed gateway.",
    "DT-H": "Best when rules, retrieval, validation, or operational tools should dominate over free-form generation.",
    "UNSPECIFIED": "This family does not yet have a governed routing posture mapped in the planning matrix.",
}
ROUTING_POSTURE_BY_FAMILY: dict[str, RoutingPosture] = {
    "lead-intake": "DT-H",
    "account-research": "DO-C",
    "qualification": "DO-C",
    "outreach-draft": "DO-G",
    "proposal-sow": "DO-G",
    "crm-hygiene": "DT-H",
    "pmo-project-control": "DO-C",
    "project-management-delivery-coordination": "DO-C",
    "ba-requirements": "DO-C",
    "architect": "DO-C",
    "build-automation": "DT-H",
    "qa-review": "DT-H",
    "documentation": "DO-C",
    "finance-ops": "DT-H",
    "invoice-receivables": "DT-H",
    "vendor-procurement": "DT-H",
    "admin-hr-ops": "DT-H",
    "company-reporting": "DO-C",
    "ceo-briefing": "DO-C",
    "strategy-opportunity": "DO-C",
    "risk-watchdog": "DT-H",
    "mission-control": "DT-H",
    "email": "DO-G",
    "personal-assistant": "DO-C",
    "cto-cio-advisory": "DO-C",
    "accountant": "DT-H",
    "cfo": "DO-C",
    "chief-ai-digital-strategy": "DO-C",
    "billing": "DT-H",
    "finance": "DO-C",
    "procurement": "DT-H",
    "reporting": "DO-C",
    "compliance-contract": "DO-G",
    "document": "DT-H",
    "knowledge": "DO-C",
    "delivery": "DT-H",
    "quality-management": "DT-H",
    "consulting-support": "DO-C",
    "testing-qa": "DT-H",
    "ops-runbook": "DT-H",
}
TOOL_PROFILE_NOTES = {profile.profile_id: profile.notes for profile in DEFAULT_TOOL_PROFILE_REGISTRY.profiles}


class ToolProfileSummary(BaseModel):
    operating_mode: OperatingMode
    operating_mode_label: str
    profile_id: str
    profile_summary: str


class GovernedMetadataSummary(BaseModel):
    pod_label: Optional[str] = None
    family_id: Optional[str] = None
    family_label: Optional[str] = None
    primary_track_label: str
    operating_mode_labels: list[str] = Field(default_factory=list)
    approval_label: str
    autonomy_label: str
    replication_label: str
    routing_posture: RoutingPosture = "UNSPECIFIED"
    routing_posture_label: str
    routing_posture_summary: str
    operating_model_label: str
    operating_model_summary: str
    tool_profiles: list[ToolProfileSummary] = Field(default_factory=list)


def build_governed_metadata_summary(
    *,
    pod: AgentPod | None,
    family_id: str | None,
    primary_track: TrackId,
    operating_modes: list[OperatingMode],
    approval_class: ApprovalClass,
    autonomy_class: AutonomyClass,
    replication_mode: ReplicationMode,
    tool_profile_by_mode: dict[str, str],
) -> GovernedMetadataSummary:
    routing_posture = ROUTING_POSTURE_BY_FAMILY.get(family_id or "", "UNSPECIFIED")
    operating_mode_labels = [MODE_LABELS.get(mode, _humanize_identifier(mode)) for mode in operating_modes]
    tool_profiles = [
        ToolProfileSummary(
            operating_mode=mode,
            operating_mode_label=MODE_LABELS.get(mode, _humanize_identifier(mode)),
            profile_id=profile_id,
            profile_summary=TOOL_PROFILE_NOTES.get(profile_id, "Tool profile note not yet documented."),
        )
        for mode, profile_id in tool_profile_by_mode.items()
    ]
    track_label = TRACK_LABELS.get(primary_track, _humanize_identifier(primary_track))
    approval_label = APPROVAL_LABELS.get(approval_class, _humanize_identifier(approval_class))
    autonomy_label = AUTONOMY_LABELS.get(autonomy_class, _humanize_identifier(autonomy_class))
    replication_label = REPLICATION_LABELS.get(replication_mode, _humanize_identifier(replication_mode))
    family_label = _humanize_identifier(family_id) if family_id else None
    pod_label = POD_LABELS.get(pod) if pod else None
    mode_scope_label = _mode_scope_label(operating_modes)
    operating_model_label = f"{mode_scope_label} / {autonomy_label} / {approval_label}"
    operating_model_summary = (
        f"Primary home: {track_label}. "
        f"Modes: {', '.join(operating_mode_labels) if operating_mode_labels else 'Not declared'}. "
        f"Autonomy: {autonomy_label}. Approval: {approval_label}. Replication: {replication_label}."
    )
    return GovernedMetadataSummary(
        pod_label=pod_label,
        family_id=family_id,
        family_label=family_label,
        primary_track_label=track_label,
        operating_mode_labels=operating_mode_labels,
        approval_label=approval_label,
        autonomy_label=autonomy_label,
        replication_label=replication_label,
        routing_posture=routing_posture,
        routing_posture_label=ROUTING_POSTURE_LABELS[routing_posture],
        routing_posture_summary=ROUTING_POSTURE_SUMMARIES[routing_posture],
        operating_model_label=operating_model_label,
        operating_model_summary=operating_model_summary,
        tool_profiles=tool_profiles,
    )


def _mode_scope_label(operating_modes: list[OperatingMode]) -> str:
    modes = set(operating_modes)
    if not modes:
        return "Mode pending"
    if modes == {"internal_operating"}:
        return "Internal operating"
    if modes == {"internal_operating", "client_delivery"}:
        return "Internal + client delivery"
    if modes == {"internal_operating", "client_delivery", "client_facing_service"}:
        return "Internal + client service reusable"
    return "Multi-mode governed"


def _humanize_identifier(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").strip().title()
