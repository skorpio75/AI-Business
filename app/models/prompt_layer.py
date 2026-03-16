# Copyright (c) Dario Pizzolante
import re
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


class PromptNamingConvention(BaseModel):
    family_base_asset_pattern: str = "<family_id>.family.base"
    workflow_step_asset_pattern: str = "<family_id>.workflow.<step_id>"
    composition_pattern: str = "<workflow_id>.<step_id>"
    workflow_step_filename_style: Literal["snake_case"] = "snake_case"


class PromptStorageConvention(BaseModel):
    prompts_root: str = "prompts"
    family_base_directory: str = "agents/{agent_family_id}"
    family_base_filename: str = "system.txt"
    workflow_step_directory: str = "workflows/{workflow_id}"
    workflow_step_filename: str = "{step_file}.txt"


class PromptLoadingConvention(BaseModel):
    explicit_relative_path_override: bool = True
    family_base_optional: bool = True
    workflow_step_required: bool = True
    append_runtime_context: bool = True


class PromptConventionSet(BaseModel):
    naming: PromptNamingConvention = Field(default_factory=PromptNamingConvention)
    storage: PromptStorageConvention = Field(default_factory=PromptStorageConvention)
    loading: PromptLoadingConvention = Field(default_factory=PromptLoadingConvention)


class PromptLayerRegistry(BaseModel):
    conventions: PromptConventionSet = Field(default_factory=PromptConventionSet)
    assets: list[PromptAsset] = Field(default_factory=list)
    compositions: list[PromptCompositionContract] = Field(default_factory=list)


def normalize_prompt_file_segment(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return normalized or "prompt"


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
    conventions=PromptConventionSet(),
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
        _asset(
            "cto-cio-advisory.family.base",
            asset_kind="family_base",
            description="Durable consulting behavior for the CTO/CIO advisory family.",
        ),
        _asset(
            "cto-cio-advisory.workflow.analyze-client-context",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="specialists/cto_cio_analysis_prompt.txt",
            description="Analyze a client technology consulting brief and return structured advisory JSON.",
        ),
        _asset(
            "cto-cio-advisory.workflow.build-panel",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="specialists/cto_cio_panel_prompt.txt",
            description="Build the internal CTO/CIO specialist panel summary as structured JSON.",
        ),
        _asset(
            "chief-ai-digital-strategy.family.base",
            asset_kind="family_base",
            description="Durable consulting behavior for the Chief AI / Digital Strategy family.",
        ),
        _asset(
            "chief-ai-digital-strategy.workflow.analyze-client-context",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="specialists/chief_ai_analysis_prompt.txt",
            description="Analyze a client AI consulting brief and return structured advisory JSON.",
        ),
        _asset(
            "chief-ai-digital-strategy.workflow.build-panel",
            asset_kind="workflow_step",
            status="implemented",
            relative_path="specialists/chief_ai_panel_prompt.txt",
            description="Build the internal Chief AI / Digital Strategy panel summary as structured JSON.",
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
        PromptCompositionContract(
            composition_id="specialist-advisory.cto-cio-analyze",
            workflow_id="specialist-advisory",
            step_id="cto-cio-analyze",
            agent_family_id="cto-cio-advisory",
            base_prompt_asset_id="cto-cio-advisory.family.base",
            step_prompt_asset_id="cto-cio-advisory.workflow.analyze-client-context",
            template_fields=[
                "engagement_name",
                "problem_statement",
                "business_goal",
                "client_context",
                "engagement_history",
                "current_stack",
                "constraints",
                "desired_outcomes",
                "internal_platform_needs",
            ],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Clarify that the output is advisory only and cannot commit the company or client.",
                ),
                _context(
                    "autonomy_policy",
                    source="policy",
                    required=True,
                    description="Describe the bounded consulting posture and governance guardrails.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    required=True,
                    description="Describe the bounded tools and context available to the specialist.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the required JSON structure for the advisory response.",
                ),
                _context(
                    "state_summary",
                    source="state",
                    description="Summarize any relevant client, opportunity, or delivery-state assumptions.",
                ),
            ],
        ),
        PromptCompositionContract(
            composition_id="specialist-advisory.cto-cio-panel",
            workflow_id="specialist-advisory",
            step_id="cto-cio-panel",
            agent_family_id="cto-cio-advisory",
            base_prompt_asset_id="cto-cio-advisory.family.base",
            step_prompt_asset_id="cto-cio-advisory.workflow.build-panel",
            template_fields=[
                "display_name",
                "role_summary",
                "operating_modes",
                "platform_context",
            ],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Clarify that the panel is advisory only and not an approval bypass.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    required=True,
                    description="Describe the bounded tools and runtime context available to the specialist.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the required JSON structure for the panel response.",
                ),
                _context(
                    "state_summary",
                    source="state",
                    required=True,
                    description="Summarize the current internal platform state the panel should reason over.",
                ),
            ],
        ),
        PromptCompositionContract(
            composition_id="specialist-advisory.chief-ai-analyze",
            workflow_id="specialist-advisory",
            step_id="chief-ai-analyze",
            agent_family_id="chief-ai-digital-strategy",
            base_prompt_asset_id="chief-ai-digital-strategy.family.base",
            step_prompt_asset_id="chief-ai-digital-strategy.workflow.analyze-client-context",
            template_fields=[
                "engagement_name",
                "problem_statement",
                "business_context",
                "client_context",
                "engagement_history",
                "process_areas",
                "data_assets",
                "current_stack",
                "delivery_constraints",
                "desired_outcomes",
            ],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Clarify that the output is advisory only and cannot commit delivery or spend.",
                ),
                _context(
                    "autonomy_policy",
                    source="policy",
                    required=True,
                    description="Describe the bounded AI consulting posture and governance guardrails.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    required=True,
                    description="Describe the bounded tools and contextual sources available to the specialist.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the required JSON structure for the advisory response.",
                ),
                _context(
                    "state_summary",
                    source="state",
                    description="Summarize any relevant account, opportunity, or delivery-state assumptions.",
                ),
            ],
        ),
        PromptCompositionContract(
            composition_id="specialist-advisory.chief-ai-panel",
            workflow_id="specialist-advisory",
            step_id="chief-ai-panel",
            agent_family_id="chief-ai-digital-strategy",
            base_prompt_asset_id="chief-ai-digital-strategy.family.base",
            step_prompt_asset_id="chief-ai-digital-strategy.workflow.build-panel",
            template_fields=[
                "display_name",
                "role_summary",
                "operating_modes",
                "platform_context",
            ],
            context_injection=[
                _context(
                    "approval_policy",
                    source="policy",
                    required=True,
                    description="Clarify that the panel is advisory only and not an approval bypass.",
                ),
                _context(
                    "tool_profile",
                    source="tools",
                    required=True,
                    description="Describe the bounded tools and runtime context available to the specialist.",
                ),
                _context(
                    "output_schema",
                    source="schema",
                    required=True,
                    description="Describe the required JSON structure for the panel response.",
                ),
                _context(
                    "state_summary",
                    source="state",
                    required=True,
                    description="Summarize the current internal platform state the panel should reason over.",
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
