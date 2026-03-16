from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


TrackId = Literal["track_a_internal", "track_b_client"]
TriggerKind = Literal["event", "schedule", "operator", "approval_resolution"]
ApprovalClass = Literal["none", "bounded", "ceo_required"]
AutonomyClass = Literal["assistant", "supervised_executor", "bounded_autonomous", "approval_gated"]
NormalizedEventName = Literal[
    "lead.signal.detected",
    "lead.candidate.created",
    "lead.review.requested",
    "lead.materialized",
    "lead.received",
    "lead.enriched",
    "lead.qualified",
    "meeting.discovery.completed",
    "proposal.requested",
    "proposal.submitted",
    "deal.won",
    "deal.lost",
    "contract.signed",
    "dispatch.plan.proposed",
    "dispatch.plan.approved",
    "mission.approved",
    "project.created",
    "workshop.completed",
    "requirements.updated",
    "design.requested",
    "design.completed",
    "build.requested",
    "build.completed",
    "qa.failed",
    "qa.passed",
    "milestone.completed",
    "milestone.acceptance.requested",
    "milestone.accepted",
    "project.risk.detected",
    "invoice.triggered",
    "invoice.sent",
    "invoice.overdue",
    "vendor.renewal_approaching",
    "month_end.started",
    "timesheet.missing",
    "risk.alert",
    "approval.pending",
    "run.failed",
    "schedule.daily_brief",
    "schedule.weekly_review",
    "schedule.monthly_strategy",
    "document.ingested",
    "meeting.summary.created",
    "project.closed",
    "mission.closeout.requested",
    "mission.closed",
    "lessons_learned.created",
    "email.received",
    "email.classified",
    "knowledge.retrieved",
    "approval.approved",
    "approval.rejected",
    "email.sent",
    "billing.exception_detected",
    "invoice.drafted",
    "invoice.released",
    "finance.review.scheduled",
    "finance.snapshot.completed",
    "reporting.refresh_requested",
    "purchase.requested",
    "procurement.validated",
    "procurement.exception_detected",
    "po.issued",
    "project.control.updated",
    "release.candidate_ready",
    "release.blocked",
    "documentation.packaged",
    "handover.ready",
    "handover.released",
]

NORMALIZED_EVENT_NAMES: tuple[NormalizedEventName, ...] = (
    "lead.signal.detected",
    "lead.candidate.created",
    "lead.review.requested",
    "lead.materialized",
    "lead.received",
    "lead.enriched",
    "lead.qualified",
    "meeting.discovery.completed",
    "proposal.requested",
    "proposal.submitted",
    "deal.won",
    "deal.lost",
    "contract.signed",
    "dispatch.plan.proposed",
    "dispatch.plan.approved",
    "mission.approved",
    "project.created",
    "workshop.completed",
    "requirements.updated",
    "design.requested",
    "design.completed",
    "build.requested",
    "build.completed",
    "qa.failed",
    "qa.passed",
    "milestone.completed",
    "milestone.acceptance.requested",
    "milestone.accepted",
    "project.risk.detected",
    "invoice.triggered",
    "invoice.sent",
    "invoice.overdue",
    "vendor.renewal_approaching",
    "month_end.started",
    "timesheet.missing",
    "risk.alert",
    "approval.pending",
    "run.failed",
    "schedule.daily_brief",
    "schedule.weekly_review",
    "schedule.monthly_strategy",
    "document.ingested",
    "meeting.summary.created",
    "project.closed",
    "mission.closeout.requested",
    "mission.closed",
    "lessons_learned.created",
    "email.received",
    "email.classified",
    "knowledge.retrieved",
    "approval.approved",
    "approval.rejected",
    "email.sent",
    "billing.exception_detected",
    "invoice.drafted",
    "invoice.released",
    "finance.review.scheduled",
    "finance.snapshot.completed",
    "reporting.refresh_requested",
    "purchase.requested",
    "procurement.validated",
    "procurement.exception_detected",
    "po.issued",
    "project.control.updated",
    "release.candidate_ready",
    "release.blocked",
    "documentation.packaged",
    "handover.ready",
    "handover.released",
)
APPROVAL_CLASSES: tuple[ApprovalClass, ...] = ("none", "bounded", "ceo_required")
AUTONOMY_CLASSES: tuple[AutonomyClass, ...] = (
    "assistant",
    "supervised_executor",
    "bounded_autonomous",
    "approval_gated",
)


class EventEnvelope(BaseModel):
    event_id: str
    event_name: NormalizedEventName
    tenant_id: str
    track: TrackId
    source: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    entity_type: str
    entity_id: str
    payload: dict[str, Any] = Field(default_factory=dict)


class WorkflowTrigger(BaseModel):
    kind: TriggerKind
    event_name: Optional[NormalizedEventName] = None
    schedule: Optional[str] = None
    operator_action: Optional[str] = None


class WorkflowControlPolicy(BaseModel):
    start_trigger: WorkflowTrigger
    emitted_events: list[NormalizedEventName] = Field(default_factory=list)
    approval_class: ApprovalClass = "none"
    autonomy_class: AutonomyClass = "assistant"
