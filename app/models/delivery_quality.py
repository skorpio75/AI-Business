# Copyright (c) Dario Pizzolante
from typing import Literal

from pydantic import BaseModel, Field

from app.models.control_plane import TrackId


MissionPhase = Literal[
    "planning",
    "analysis_design",
    "implementation",
    "pre_milestone",
    "handover",
]
DeliverableClass = Literal[
    "document_deliverable",
    "requirements_deliverable",
    "architecture_deliverable",
    "code_deliverable",
    "configuration_deliverable",
    "analysis_deliverable",
    "test_evidence_deliverable",
    "handover_deliverable",
]
QualityGateType = Literal[
    "document_review_gate",
    "requirements_traceability_gate",
    "architecture_review_gate",
    "implementation_review_gate",
    "test_readiness_gate",
    "milestone_release_gate",
    "handover_readiness_gate",
]
QualityGateOutcome = Literal["approve", "revise", "escalate", "human_review", "blocked"]
QualityGateAgentFamily = Literal[
    "qa-review",
    "testing-qa",
    "documentation",
    "risk-watchdog",
    "mission-control",
]
GateRubricInput = Literal[
    "mission_statement",
    "sow_excerpt",
    "project_plan",
    "deliverable_artifact",
    "acceptance_criteria",
    "test_evidence",
    "prior_gate_results",
    "internal_retrieval",
    "client_retrieval",
]
QualityGateTemplateId = Literal["advisory_light", "delivery_standard", "implementation_heavy"]


class QualityGateCheckpoint(BaseModel):
    checkpoint_id: str
    phase: MissionPhase
    gate_type: QualityGateType
    deliverable_classes: list[DeliverableClass] = Field(default_factory=list)
    required_agent_families: list[QualityGateAgentFamily] = Field(default_factory=list)
    rubric_inputs: list[GateRubricInput] = Field(default_factory=list)
    release_blocking: bool = True
    pass_condition_summary: str
    escalation_conditions: list[str] = Field(default_factory=list)


class QualityGatePlan(BaseModel):
    plan_id: str
    mission_id: str
    engagement_id: str
    tenant_id: str
    track: TrackId = "track_b_client"
    template_id: QualityGateTemplateId = "delivery_standard"
    deliverable_classes: list[DeliverableClass] = Field(default_factory=list)
    checkpoints: list[QualityGateCheckpoint] = Field(default_factory=list)
    milestone_release_gate_required: bool = True
    handover_gate_required: bool = True
    release_policy_notes: list[str] = Field(default_factory=list)


class QualityGateTemplate(BaseModel):
    template_id: QualityGateTemplateId
    description: str
    recommended_for: list[str] = Field(default_factory=list)
    deliverable_classes: list[DeliverableClass] = Field(default_factory=list)
    checkpoints: list[QualityGateCheckpoint] = Field(default_factory=list)


class QualityGateRegistry(BaseModel):
    templates: list[QualityGateTemplate] = Field(default_factory=list)


def _checkpoint(
    checkpoint_id: str,
    *,
    phase: MissionPhase,
    gate_type: QualityGateType,
    deliverable_classes: list[DeliverableClass],
    required_agent_families: list[QualityGateAgentFamily],
    rubric_inputs: list[GateRubricInput],
    pass_condition_summary: str,
    escalation_conditions: list[str],
    release_blocking: bool = True,
) -> QualityGateCheckpoint:
    return QualityGateCheckpoint(
        checkpoint_id=checkpoint_id,
        phase=phase,
        gate_type=gate_type,
        deliverable_classes=deliverable_classes,
        required_agent_families=required_agent_families,
        rubric_inputs=rubric_inputs,
        release_blocking=release_blocking,
        pass_condition_summary=pass_condition_summary,
        escalation_conditions=escalation_conditions,
    )


DEFAULT_QUALITY_GATE_REGISTRY = QualityGateRegistry(
    templates=[
        QualityGateTemplate(
            template_id="advisory_light",
            description="Lightweight quality gates for advisory and document-heavy missions.",
            recommended_for=["assessments", "advisory packs", "strategy deliverables"],
            deliverable_classes=[
                "document_deliverable",
                "analysis_deliverable",
                "handover_deliverable",
            ],
            checkpoints=[
                _checkpoint(
                    "planning-document-alignment",
                    phase="planning",
                    gate_type="document_review_gate",
                    deliverable_classes=["document_deliverable", "analysis_deliverable"],
                    required_agent_families=["qa-review"],
                    rubric_inputs=["mission_statement", "sow_excerpt", "project_plan", "acceptance_criteria"],
                    pass_condition_summary="The planned advisory deliverables align with the SOW and have clear acceptance criteria.",
                    escalation_conditions=["scope contradiction", "missing acceptance criteria"],
                ),
                _checkpoint(
                    "handover-advisory-readiness",
                    phase="handover",
                    gate_type="handover_readiness_gate",
                    deliverable_classes=["handover_deliverable", "document_deliverable"],
                    required_agent_families=["documentation", "qa-review"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "prior_gate_results"],
                    pass_condition_summary="The advisory package is complete, internally consistent, and ready for handoff.",
                    escalation_conditions=["missing sections", "unresolved contradictions"],
                ),
            ],
        ),
        QualityGateTemplate(
            template_id="delivery_standard",
            description="Default delivery gate pattern for mixed consulting and implementation work.",
            recommended_for=["standard delivery", "platform rollout", "automation projects"],
            deliverable_classes=[
                "requirements_deliverable",
                "architecture_deliverable",
                "document_deliverable",
                "analysis_deliverable",
                "test_evidence_deliverable",
                "handover_deliverable",
            ],
            checkpoints=[
                _checkpoint(
                    "planning-gate-plan-baseline",
                    phase="planning",
                    gate_type="requirements_traceability_gate",
                    deliverable_classes=["requirements_deliverable", "document_deliverable"],
                    required_agent_families=["qa-review", "mission-control"],
                    rubric_inputs=["mission_statement", "sow_excerpt", "project_plan", "acceptance_criteria"],
                    pass_condition_summary="The project plan reflects agreed deliverables, milestones, and acceptance criteria.",
                    escalation_conditions=["missing milestone coverage", "weak traceability to SOW"],
                ),
                _checkpoint(
                    "design-architecture-review",
                    phase="analysis_design",
                    gate_type="architecture_review_gate",
                    deliverable_classes=["architecture_deliverable", "analysis_deliverable"],
                    required_agent_families=["qa-review", "risk-watchdog"],
                    rubric_inputs=["sow_excerpt", "project_plan", "deliverable_artifact", "acceptance_criteria", "internal_retrieval"],
                    pass_condition_summary="Design artifacts are complete, feasible, and aligned with mission constraints.",
                    escalation_conditions=["unresolved design risk", "missing dependency treatment"],
                ),
                _checkpoint(
                    "milestone-release-readiness",
                    phase="pre_milestone",
                    gate_type="milestone_release_gate",
                    deliverable_classes=["document_deliverable", "test_evidence_deliverable", "handover_deliverable"],
                    required_agent_families=["qa-review", "testing-qa", "mission-control"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "test_evidence", "prior_gate_results"],
                    pass_condition_summary="Milestone evidence is complete and ready for client acceptance routing.",
                    escalation_conditions=["failing evidence", "missing required gate results", "open blocker defects"],
                ),
                _checkpoint(
                    "handover-final-readiness",
                    phase="handover",
                    gate_type="handover_readiness_gate",
                    deliverable_classes=["handover_deliverable", "document_deliverable"],
                    required_agent_families=["documentation", "qa-review"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "prior_gate_results"],
                    pass_condition_summary="Handover materials are complete, versioned, and operationally clear.",
                    escalation_conditions=["missing handover content", "unclear ownership after release"],
                ),
            ],
        ),
        QualityGateTemplate(
            template_id="implementation_heavy",
            description="Heavier gate pattern for code, automation, and implementation-intensive missions.",
            recommended_for=["software delivery", "automation buildout", "integration implementation"],
            deliverable_classes=[
                "requirements_deliverable",
                "architecture_deliverable",
                "code_deliverable",
                "configuration_deliverable",
                "test_evidence_deliverable",
                "handover_deliverable",
            ],
            checkpoints=[
                _checkpoint(
                    "implementation-traceability-baseline",
                    phase="planning",
                    gate_type="requirements_traceability_gate",
                    deliverable_classes=["requirements_deliverable", "architecture_deliverable"],
                    required_agent_families=["qa-review", "mission-control"],
                    rubric_inputs=["mission_statement", "sow_excerpt", "project_plan", "acceptance_criteria"],
                    pass_condition_summary="Implementation scope is traceable from SOW through plan and acceptance criteria.",
                    escalation_conditions=["requirements gaps", "missing implementation checkpoints"],
                ),
                _checkpoint(
                    "implementation-artifact-review",
                    phase="implementation",
                    gate_type="implementation_review_gate",
                    deliverable_classes=["code_deliverable", "configuration_deliverable"],
                    required_agent_families=["qa-review", "testing-qa"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "test_evidence", "prior_gate_results"],
                    pass_condition_summary="Implementation artifacts meet the agreed design intent and are supported by evidence.",
                    escalation_conditions=["untested changes", "implementation drift", "critical defects"],
                ),
                _checkpoint(
                    "test-readiness-check",
                    phase="implementation",
                    gate_type="test_readiness_gate",
                    deliverable_classes=["test_evidence_deliverable", "code_deliverable"],
                    required_agent_families=["testing-qa"],
                    rubric_inputs=["acceptance_criteria", "test_evidence", "prior_gate_results"],
                    pass_condition_summary="Testing evidence is sufficient for the current release or milestone decision.",
                    escalation_conditions=["missing test coverage", "high-severity unresolved defects"],
                ),
                _checkpoint(
                    "implementation-milestone-release",
                    phase="pre_milestone",
                    gate_type="milestone_release_gate",
                    deliverable_classes=["code_deliverable", "configuration_deliverable", "test_evidence_deliverable"],
                    required_agent_families=["qa-review", "testing-qa", "risk-watchdog"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "test_evidence", "prior_gate_results"],
                    pass_condition_summary="Implementation milestone is ready for client acceptance and release discussion.",
                    escalation_conditions=["release blocker", "security or risk concern", "insufficient evidence"],
                ),
                _checkpoint(
                    "implementation-handover-readiness",
                    phase="handover",
                    gate_type="handover_readiness_gate",
                    deliverable_classes=["handover_deliverable", "configuration_deliverable", "document_deliverable"],
                    required_agent_families=["documentation", "qa-review"],
                    rubric_inputs=["deliverable_artifact", "acceptance_criteria", "prior_gate_results"],
                    pass_condition_summary="Technical handover is complete enough for the client or downstream operator to run safely.",
                    escalation_conditions=["missing runbook", "missing environment notes", "open unresolved blocker"],
                ),
            ],
        ),
    ]
)


QUALITY_GATE_TEMPLATE_BY_ID = {
    template.template_id: template for template in DEFAULT_QUALITY_GATE_REGISTRY.templates
}
