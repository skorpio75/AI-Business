# Copyright (c) Dario Pizzolante
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from app.models.control_plane import TrackId
from app.models.tool_profiles import OperatingMode

DeliveryLabScopeKind = Literal["ad_hoc_session", "saved_lab_mission", "engagement_bound_run"]
DeliveryLabStatus = Literal["draft", "active", "completed", "archived", "blocked"]
ArtifactApprovalStatus = Literal["draft", "reviewed", "approved_for_handover", "rejected"]
ReadinessStatus = Literal["not_started", "in_review", "ready", "revise", "blocked", "exec_review"]
ActivationStatus = Literal["queued", "seeding", "ready_to_start", "activated", "failed", "cancelled"]
ActivationMode = Literal["seed_only", "seed_and_start", "attach_existing"]


class AgentInvokeRequest(BaseModel):
    request_id: Optional[str] = None
    tenant_id: str = "internal"
    family_id: str
    mode: OperatingMode = "internal_operating"
    scope_kind: DeliveryLabScopeKind
    scope_id: Optional[str] = None
    task_template_id: str
    title: str
    goal: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    context_pack_refs: list[str] = Field(default_factory=list)
    output_schema_id: str
    requested_by: str = "ceo"
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    opportunity_id: Optional[str] = None
    engagement_id: Optional[str] = None


class AgentInvokeRouting(BaseModel):
    provider_used: str
    model_used: str
    strategy_used: str


class AgentInvokeResponse(BaseModel):
    session_id: str
    run_id: str
    family_id: str
    scope_kind: DeliveryLabScopeKind
    status: Literal["completed", "pending_approval", "failed"]
    output_ref: str
    routing: AgentInvokeRouting


class AdHocSession(BaseModel):
    session_id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    family_id: str
    mode: OperatingMode = "internal_operating"
    title: str
    goal: str
    status: DeliveryLabStatus = "draft"
    task_template_id: str
    output_schema_id: str
    opportunity_id: Optional[str] = None
    engagement_id: Optional[str] = None
    created_by: str = "ceo"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    latest_output_ref: Optional[str] = None
    context_pack_refs: list[str] = Field(default_factory=list)


class SaveSessionAsLabMissionRequest(BaseModel):
    title: str
    goal: str
    mission_brief: Optional[str] = None
    owner_role: str = "CEO"
    engagement_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    assigned_family_ids: list[str] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    quality_gate_plan_ref: Optional[str] = None


class LabMissionArtifact(BaseModel):
    artifact_id: str
    artifact_type: str
    title: str
    storage_ref: str
    version: int = 1
    produced_by_family_id: str
    produced_by_agent_run_id: Optional[str] = None
    approval_status: ArtifactApprovalStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LabMission(BaseModel):
    lab_mission_id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    title: str
    status: DeliveryLabStatus = "draft"
    goal: str
    mission_brief: str
    owner_role: str
    opportunity_id: Optional[str] = None
    engagement_id: Optional[str] = None
    source_session_id: Optional[str] = None
    assigned_family_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quality_gate_plan_ref: Optional[str] = None
    last_readiness_posture: ReadinessStatus = "not_started"
    context_pack_refs: list[str] = Field(default_factory=list)
    artifacts: list[LabMissionArtifact] = Field(default_factory=list)
    linked_handover_pack_ids: list[str] = Field(default_factory=list)


class HandoverPackItem(BaseModel):
    item_id: str
    item_type: str
    title: str
    storage_ref: str
    source_artifact_ref: Optional[str] = None
    required_for_activation: bool = True
    approval_status: ArtifactApprovalStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CreateHandoverPackRequest(BaseModel):
    target_client_id: str
    target_engagement_id: str
    target_mission_name: str
    artifact_refs: list[str] = Field(default_factory=list)
    approved_roster_ref: str
    context_pack_refs: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)


class HandoverPack(BaseModel):
    handover_pack_id: str
    tenant_id: str
    source_lab_mission_id: str
    source_engagement_id: Optional[str] = None
    status: Literal["draft", "approved", "superseded", "activated"] = "draft"
    target_client_id: str
    target_engagement_id: str
    target_mission_name: str
    mission_brief_ref: str
    approved_roster_ref: str
    project_plan_ref: Optional[str] = None
    raid_log_ref: Optional[str] = None
    quality_gate_plan_ref: Optional[str] = None
    context_pack_refs: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    items: list[HandoverPackItem] = Field(default_factory=list)
    created_by: str = "ceo"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None
    readiness_status: ReadinessStatus = "not_started"


class ReadinessGateCheck(BaseModel):
    check_id: str
    checkpoint_id: str
    family_id: str
    outcome: ReadinessStatus
    notes: Optional[str] = None
    artifact_refs: list[str] = Field(default_factory=list)


class RunReadinessGateRequest(BaseModel):
    rubric_id: str
    required_families: list[str] = Field(default_factory=list)


class ReadinessGateResult(BaseModel):
    readiness_gate_result_id: str
    handover_pack_id: str
    status: ReadinessStatus
    review_summary: str
    reviewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_by_role: str = "CEO"
    blocking_reason: Optional[str] = None
    rubric_version: str
    checks: list[ReadinessGateCheck] = Field(default_factory=list)


class CreateActivationRequest(BaseModel):
    target_tenant_id: str
    runtime_env_ref: str
    activation_mode: ActivationMode


class ActivationRequest(BaseModel):
    activation_request_id: str
    handover_pack_id: str
    tenant_id: str
    target_tenant_id: str
    runtime_env_ref: str
    activation_mode: ActivationMode
    status: ActivationStatus = "queued"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status_detail: Optional[str] = None


class DeliveryLabRegistryEntry(BaseModel):
    object_id: str
    display_name: str
    scope_kind: Optional[DeliveryLabScopeKind] = None
    track: TrackId
    persistence_target: str
    status_values: list[str] = Field(default_factory=list)
    required_refs: list[str] = Field(default_factory=list)
    notes: str


class DeliveryLabContractRegistry(BaseModel):
    objects: list[DeliveryLabRegistryEntry] = Field(default_factory=list)


DEFAULT_DELIVERY_LAB_CONTRACT_REGISTRY = DeliveryLabContractRegistry(
    objects=[
        DeliveryLabRegistryEntry(
            object_id="ad_hoc_session",
            display_name="Ad Hoc Session",
            scope_kind="ad_hoc_session",
            track="track_a_internal",
            persistence_target="planned ad_hoc_sessions table or json_snapshot store",
            status_values=["draft", "active", "completed", "archived", "blocked"],
            required_refs=["family_id", "task_template_id", "output_schema_id"],
            notes="Lightweight Track A invocation session for immediate bounded internal work.",
        ),
        DeliveryLabRegistryEntry(
            object_id="lab_mission",
            display_name="Lab Mission",
            scope_kind="saved_lab_mission",
            track="track_a_internal",
            persistence_target="planned lab_missions and lab_mission_artifacts tables",
            status_values=["draft", "active", "completed", "archived", "blocked"],
            required_refs=["mission_brief", "assigned_family_ids"],
            notes="Durable Track A rehearsal mission with artifacts and readiness posture.",
        ),
        DeliveryLabRegistryEntry(
            object_id="handover_pack",
            display_name="Handover Pack",
            track="track_a_internal",
            persistence_target="planned handover_packs and handover_pack_items tables",
            status_values=["draft", "approved", "superseded", "activated"],
            required_refs=["mission_brief_ref", "approved_roster_ref", "context_pack_refs"],
            notes="Approved artifact bundle promoted from Track A into Track B activation.",
        ),
        DeliveryLabRegistryEntry(
            object_id="readiness_gate_result",
            display_name="Readiness Gate Result",
            track="track_a_internal",
            persistence_target="planned readiness_gate_results and readiness_gate_checks tables",
            status_values=["not_started", "in_review", "ready", "revise", "blocked", "exec_review"],
            required_refs=["handover_pack_id", "rubric_version"],
            notes="Explicit Track A readiness decision before Track B activation can start.",
        ),
        DeliveryLabRegistryEntry(
            object_id="activation_request",
            display_name="Activation Request",
            track="track_a_internal",
            persistence_target="planned activation_requests table",
            status_values=["queued", "seeding", "ready_to_start", "activated", "failed", "cancelled"],
            required_refs=["handover_pack_id", "runtime_env_ref", "activation_mode"],
            notes="Request to seed or activate the target Track B tenant runtime from an approved handover pack.",
        ),
    ]
)
