# Copyright (c) Dario Pizzolante
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.control_plane import ApprovalClass, AutonomyClass, NormalizedEventName, TrackId


StateId = Literal[
    "opportunity_state",
    "project_state",
    "run_state",
    "approval_state",
    "ad_hoc_session_state",
    "lab_mission_state",
    "handover_pack_state",
    "readiness_gate_result_state",
    "activation_request_state",
]
PersistenceStatus = Literal["active", "partial", "planned"]
CanonicalStoreKind = Literal["postgres_entity_table", "postgres_row_table", "json_snapshot", "policy_record"]
SerializationKind = Literal["structured_columns", "json_document", "hybrid_projection"]


class OpportunityState(BaseModel):
    id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    prospect_id: str
    owner_agent_or_role: str
    stage: str
    qualification_status: str
    service_type: str
    next_action: str
    lead_score: Optional[float] = None
    estimated_value: Optional[float] = None
    urgency: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    last_contact_at: Optional[datetime] = None
    risks: list[str] = Field(default_factory=list)
    memory_refs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class ProjectState(BaseModel):
    id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    client_id: str
    status: str
    project_manager: str
    current_phase: str
    risk_level: str
    milestone_health: Optional[str] = None
    budget_health: Optional[str] = None
    overdue_actions_count: int = 0
    next_steerco_date: Optional[datetime] = None
    deliverables: list[str] = Field(default_factory=list)
    quality_gate_plan_id: Optional[str] = None
    active_quality_gate_ids: list[str] = Field(default_factory=list)
    quality_gate_status: Optional[str] = None
    quality_gate_result_refs: list[str] = Field(default_factory=list)
    raid_log_ref: Optional[str] = None
    acceptance_refs: list[str] = Field(default_factory=list)
    memory_refs: list[str] = Field(default_factory=list)


class RunState(BaseModel):
    run_id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    workflow_id: str
    workflow_type: str
    agent_id: Optional[str] = None
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    step_id: Optional[str] = None
    event_source: Optional[NormalizedEventName] = None
    confidence: Optional[float] = None
    routing_path: Optional[str] = None
    fallback_mode: Optional[str] = None
    tool_calls: list[str] = Field(default_factory=list)
    output_ref: Optional[str] = None
    blocking_reason: Optional[str] = None
    approval_class: Optional[ApprovalClass] = None
    autonomy_class: Optional[AutonomyClass] = None
    audit_ref: Optional[str] = None


class ApprovalState(BaseModel):
    approval_id: str
    tenant_id: str
    track: TrackId = "track_a_internal"
    approval_class: ApprovalClass
    related_run_id: str
    requested_by_agent: str
    approver_role: str
    status: str
    requested_at: datetime
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    decided_at: Optional[datetime] = None
    decision: Optional[str] = None
    notes: Optional[str] = None
    policy_ref: Optional[str] = None


class StateOwnershipContract(BaseModel):
    state_id: StateId
    primary_owner: str
    steward: str
    typical_writers: list[str] = Field(default_factory=list)
    consuming_workflows: list[str] = Field(default_factory=list)


class StatePersistenceContract(BaseModel):
    state_id: StateId
    persistence_status: PersistenceStatus
    canonical_store_kind: CanonicalStoreKind
    serialization_kind: SerializationKind
    physical_target: str
    repository_functions: list[str] = Field(default_factory=list)
    notes: str


class StateRegistry(BaseModel):
    ownership: list[StateOwnershipContract] = Field(default_factory=list)
    persistence: list[StatePersistenceContract] = Field(default_factory=list)


DEFAULT_STATE_REGISTRY = StateRegistry(
    ownership=[
        StateOwnershipContract(
            state_id="opportunity_state",
            primary_owner="growth_pod",
            steward="Lead Intake Agent",
            typical_writers=[
                "Lead Intake Agent",
                "Account Research Agent",
                "Qualification Agent",
                "Proposal / SOW Agent",
            ],
            consuming_workflows=["proposal-generation", "growth qualification", "account research"],
        ),
        StateOwnershipContract(
            state_id="project_state",
            primary_owner="delivery_pod",
            steward="PMO / Project Control Agent",
            typical_writers=[
                "PMO / Project Control Agent",
                "Project Management / Delivery Coordination Agent",
                "BA / Requirements Agent",
                "Architect Agent",
                "Build / Automation Agent",
                "QA / Review Agent",
                "Documentation Agent",
            ],
            consuming_workflows=[
                "project-management",
                "quality-testing-gate",
                "documentation-handover",
                "delivery quality gates",
            ],
        ),
        StateOwnershipContract(
            state_id="run_state",
            primary_owner="workflow_orchestration_layer",
            steward="Mission Control Agent",
            typical_writers=[
                "LangGraph workflow runner",
                "workflow services",
                "approval resolution path",
            ],
            consuming_workflows=[
                "email-operations",
                "knowledge-qna",
                "proposal-generation",
                "project-management",
            ],
        ),
        StateOwnershipContract(
            state_id="approval_state",
            primary_owner="policy_and_approval_layer",
            steward="CEO approval control",
            typical_writers=["approval queue", "workflow approval steps", "approval decision API"],
            consuming_workflows=[
                "email-operations",
                "billing-operations",
                "procurement-po",
                "documentation-handover",
            ],
        ),
        StateOwnershipContract(
            state_id="ad_hoc_session_state",
            primary_owner="delivery_lab_control_plane",
            steward="Mission Control Agent",
            typical_writers=[
                "future agent invocation API",
                "delivery-lab orchestration layer",
                "Track A operator actions",
            ],
            consuming_workflows=["delivery-lab invoke", "agent workbench", "internal rehearsal"],
        ),
        StateOwnershipContract(
            state_id="lab_mission_state",
            primary_owner="delivery_pod",
            steward="PMO / Project Control Agent",
            typical_writers=[
                "delivery-lab orchestration layer",
                "PMO / Project Control Agent",
                "Project Management / Delivery Coordination Agent",
            ],
            consuming_workflows=["delivery-lab mission", "readiness review", "handover assembly"],
        ),
        StateOwnershipContract(
            state_id="handover_pack_state",
            primary_owner="promotion_and_activation_layer",
            steward="Documentation Agent",
            typical_writers=[
                "future handover-pack API",
                "Documentation Agent",
                "PMO / Project Control Agent",
            ],
            consuming_workflows=["handover assembly", "readiness review", "track-b activation"],
        ),
        StateOwnershipContract(
            state_id="readiness_gate_result_state",
            primary_owner="quality_and_gate_layer",
            steward="QA / Review Agent",
            typical_writers=[
                "future readiness-gate API",
                "QA / Review Agent",
                "Risk / Watchdog Agent",
                "Mission Control Agent",
            ],
            consuming_workflows=["readiness review", "activation queue"],
        ),
        StateOwnershipContract(
            state_id="activation_request_state",
            primary_owner="track_b_activation_layer",
            steward="Mission Control Agent",
            typical_writers=[
                "future activation API",
                "tenant bootstrap automation",
                "Mission Control Agent",
            ],
            consuming_workflows=["track-b activation", "activation queue"],
        ),
    ],
    persistence=[
        StatePersistenceContract(
            state_id="opportunity_state",
            persistence_status="planned",
            canonical_store_kind="postgres_entity_table",
            serialization_kind="structured_columns",
            physical_target="future opportunity_state table or shared-workspace entity store",
            repository_functions=[],
            notes=(
                "Opportunity ownership is defined, but the current MVP does not yet persist a canonical "
                "opportunity entity in the backend."
            ),
        ),
        StatePersistenceContract(
            state_id="project_state",
            persistence_status="planned",
            canonical_store_kind="postgres_entity_table",
            serialization_kind="structured_columns",
            physical_target="future project_state table or shared-workspace entity store",
            repository_functions=[],
            notes=(
                "Project ownership is defined, but the current MVP does not yet persist a canonical "
                "project entity in the backend."
            ),
        ),
        StatePersistenceContract(
            state_id="run_state",
            persistence_status="active",
            canonical_store_kind="json_snapshot",
            serialization_kind="hybrid_projection",
            physical_target="workflow_state_snapshots.state_json plus workflow_runs operational projection",
            repository_functions=[
                "upsert_workflow_state",
                "resolve_workflow_state",
                "insert_workflow_run",
                "update_workflow_run_resolution",
            ],
            notes=(
                "Run state is persisted today through workflow snapshots and a workflow-runs projection "
                "used by Mission Control surfaces."
            ),
        ),
        StatePersistenceContract(
            state_id="approval_state",
            persistence_status="active",
            canonical_store_kind="policy_record",
            serialization_kind="structured_columns",
            physical_target="approvals table",
            repository_functions=[
                "insert_approval",
                "upsert_approval",
                "get_approval",
                "list_pending_approvals",
            ],
            notes=(
                "Approval state is persisted today as first-class approval records, with workflow-state "
                "snapshots carrying approval outcome echoes for run visibility."
            ),
        ),
        StatePersistenceContract(
            state_id="ad_hoc_session_state",
            persistence_status="planned",
            canonical_store_kind="postgres_entity_table",
            serialization_kind="structured_columns",
            physical_target="future ad_hoc_sessions table or delivery-lab json snapshot store",
            repository_functions=[],
            notes=(
                "Ad hoc Track A delivery-lab sessions are now governed as first-class state, but no backend "
                "persistence layer has been implemented yet."
            ),
        ),
        StatePersistenceContract(
            state_id="lab_mission_state",
            persistence_status="planned",
            canonical_store_kind="postgres_entity_table",
            serialization_kind="hybrid_projection",
            physical_target="future lab_missions and lab_mission_artifacts tables",
            repository_functions=[],
            notes=(
                "Durable Track A rehearsal missions and artifacts are modeled, but the canonical persistence "
                "tables and repository functions are still upcoming."
            ),
        ),
        StatePersistenceContract(
            state_id="handover_pack_state",
            persistence_status="planned",
            canonical_store_kind="postgres_entity_table",
            serialization_kind="hybrid_projection",
            physical_target="future handover_packs and handover_pack_items tables",
            repository_functions=[],
            notes=(
                "Promotion from Track A to Track B should pass through a handover-pack contract rather than "
                "shared mutable runtime state, but persistence is not yet implemented."
            ),
        ),
        StatePersistenceContract(
            state_id="readiness_gate_result_state",
            persistence_status="planned",
            canonical_store_kind="policy_record",
            serialization_kind="structured_columns",
            physical_target="future readiness_gate_results and readiness_gate_checks tables",
            repository_functions=[],
            notes=(
                "Readiness gate results will record explicit activation decisions for handover packs once the "
                "review runtime is implemented."
            ),
        ),
        StatePersistenceContract(
            state_id="activation_request_state",
            persistence_status="planned",
            canonical_store_kind="policy_record",
            serialization_kind="structured_columns",
            physical_target="future activation_requests table",
            repository_functions=[],
            notes=(
                "Track B activation requests are modeled now so later bootstrap automation can depend on a "
                "stable contract."
            ),
        ),
    ],
)
