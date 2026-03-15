from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


PromptAssetKind = Literal["family_base", "workflow_step"]
PromptAssetStatus = Literal["planned", "implemented"]
PromptContextKey = Literal[
    "tenant_context",
    "track",
    "operating_mode",
    "approval_policy",
    "autonomy_policy",
    "tool_profile",
    "state_summary",
    "memory_context",
    "handoff_payload",
    "output_schema",
]
PromptContextSource = Literal[
    "tenant",
    "policy",
    "tools",
    "state",
    "memory",
    "handoff",
    "schema",
]


class PromptAsset(BaseModel):
    asset_id: str
    asset_kind: PromptAssetKind
    status: PromptAssetStatus = "planned"
    relative_path: Optional[str] = None
    description: str


class PromptContextRule(BaseModel):
    key: PromptContextKey
    source: PromptContextSource
    required: bool = False
    description: str


class PromptCompositionContract(BaseModel):
    composition_id: str
    workflow_id: str
    step_id: str
    agent_family_id: Optional[str] = None
    base_prompt_asset_id: Optional[str] = None
    step_prompt_asset_id: str
    template_fields: list[str] = Field(default_factory=list)
    context_injection: list[PromptContextRule] = Field(default_factory=list)
    notes: Optional[str] = None


class PromptRenderRequest(BaseModel):
    composition_id: str
    template_context: dict[str, Any] = Field(default_factory=dict)
    injected_context: dict[PromptContextKey, str] = Field(default_factory=dict)


class PromptLayerRegistry(BaseModel):
    assets: list[PromptAsset] = Field(default_factory=list)
    compositions: list[PromptCompositionContract] = Field(default_factory=list)


def _asset(
    asset_id: str,
    *,
    asset_kind: PromptAssetKind,
    description: str,
    status: PromptAssetStatus = "planned",
    relative_path: Optional[str] = None,
) -> PromptAsset:
    return PromptAsset(
        asset_id=asset_id,
        asset_kind=asset_kind,
        description=description,
        status=status,
        relative_path=relative_path,
    )


def _context(
    key: PromptContextKey,
    *,
    source: PromptContextSource,
    description: str,
    required: bool = False,
) -> PromptContextRule:
    return PromptContextRule(
        key=key,
        source=source,
        description=description,
        required=required,
    )


DEFAULT_PROMPT_LAYER_REGISTRY = PromptLayerRegistry(
    assets=[
        _asset(
            "email.family.base",
            asset_kind="family_base",
            description="Durable email-agent behavior instructions shared across email workflow steps.",
        ),
        _asset(
            "email.workflow.classify-email",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="email/email_operations_prompt.txt",
            description="Classify inbound email and return the structured response payload.",
        ),
        _asset(
            "email.workflow.draft-reply",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="email/email_draft_prompt.txt",
            description="Draft a bounded reply body for the current email workflow step.",
        ),
        _asset(
            "knowledge.family.base",
            asset_kind="family_base",
            description="Durable grounded-answer behavior for the knowledge family.",
        ),
        _asset(
            "knowledge.workflow.answer-question",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="knowledge/knowledge_qna_prompt.txt",
            description="Answer a knowledge question using retrieved evidence only.",
        ),
        _asset(
            "proposal-sow.family.base",
            asset_kind="family_base",
            description="Durable proposal-drafting behavior for the proposal/SOW family.",
        ),
        _asset(
            "proposal-sow.workflow.generate-draft",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="proposal/proposal_generation_prompt.txt",
            description="Generate a baseline proposal draft from the current opportunity context.",
        ),
    ],
    compositions=[
        PromptCompositionContract(
            composition_id="email-operations.classify-email",
            workflow_id="email-operations",
            step_id="classify-email",
            agent_family_id="email",
            base_prompt_asset_id="email.family.base",
            step_prompt_asset_id="email.workflow.classify-email",
            template_fields=["sender", "subject", "body", "thread_context"],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Explain outbound-review rules for the current email workflow.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the required structured output shape for the classification step.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    description="Describe the bounded email tools available to the step.",
                ),
            ],
            notes="Base prompt asset is planned; current runtime composes step prompt plus injected operating context.",
        ),
        PromptCompositionContract(
            composition_id="email-operations.draft-reply",
            workflow_id="email-operations",
            step_id="draft-reply",
            agent_family_id="email",
            base_prompt_asset_id="email.family.base",
            step_prompt_asset_id="email.workflow.draft-reply",
            template_fields=["subject", "body"],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Explain approval boundaries for the outbound reply draft.",
                ),
                _context(
                    "autonomy_policy",
                    source="policy",
                    description="Clarify any additional bounded-autonomy notes for the draft step.",
                ),
            ],
            notes="This prompt remains step-scoped; family-level prompt authoring is intentionally deferred.",
        ),
        PromptCompositionContract(
            composition_id="knowledge-qna.answer-question",
            workflow_id="knowledge-qna",
            step_id="answer-question",
            agent_family_id="knowledge",
            base_prompt_asset_id="knowledge.family.base",
            step_prompt_asset_id="knowledge.workflow.answer-question",
            template_fields=["question", "context"],
            context_injection=[
                _context(
                    "memory_context",
                    source="memory",
                    required=True,
                    description="Clarify that only retrieved internal knowledge may ground the answer.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the expected grounded-answer output format.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    description="Describe bounded retrieval and memory-search permissions.",
                ),
            ],
        ),
        PromptCompositionContract(
            composition_id="proposal-generation.generate-draft",
            workflow_id="proposal-generation",
            step_id="generate-draft",
            agent_family_id="proposal-sow",
            base_prompt_asset_id="proposal-sow.family.base",
            step_prompt_asset_id="proposal-sow.workflow.generate-draft",
            template_fields=[
                "client_name",
                "opportunity_summary",
                "desired_outcomes",
                "constraints",
            ],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Clarify that proposal text is draft-only until reviewed and approved.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the expected proposal-draft structure for the workflow step.",
                ),
                _context(
                    "state_summary",
                    source="state",
                    description="Summarize relevant opportunity-state assumptions if available.",
                ),
            ],
        ),
    ],
)

PROMPT_ASSET_BY_ID = {
    asset.asset_id: asset for asset in DEFAULT_PROMPT_LAYER_REGISTRY.assets
}
PROMPT_COMPOSITION_BY_ID = {
    composition.composition_id: composition
    for composition in DEFAULT_PROMPT_LAYER_REGISTRY.compositions
}
