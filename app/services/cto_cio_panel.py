from app.core.prompt_loader import PromptLoader
from app.core.settings import Settings
from app.models.agent_contract import AgentContract
from app.models.schemas import CTOCIOAnalysisResponse, CTOCIOPanelResponse, CTOCIOScopeInsight
from app.models.specialist_contracts import (
    ArchitectureAdvice,
    ContextSignal,
    CTOCIOCounselInput,
    CTOCIOCounselOutput,
    ImprovementBacklogItem,
    MissionAssessment,
    RecommendedService,
    StrategyOption,
    UpsellOpportunity,
)
from app.services.model_gateway import ModelGateway


class CTOCIOPanelService:
    def __init__(self, model_gateway: ModelGateway | None = None) -> None:
        self.model_gateway = model_gateway or ModelGateway(settings=Settings())
        self.prompt_loader = PromptLoader()

    def build_panel(self, *, agent: AgentContract) -> CTOCIOPanelResponse:
        fallback_response = self._build_fallback_panel(agent)
        prompt = self.prompt_loader.render_composition(
            "specialist-advisory.cto-cio-panel",
            template_context={
                "display_name": agent.display_name,
                "role_summary": agent.role_summary,
                "operating_modes": self._format_list(agent.operating_modes),
                "platform_context": self._panel_platform_context(),
            },
            injected_context={
                "approval_policy": (
                    "Internal advisory output only. This panel does not bypass approval policy or authorize delivery commitments."
                ),
                "tool_profile": "specialist-advisory profile with internal platform and roadmap context only.",
                "state_summary": (
                    "Current internal state includes workflow-first orchestration, prompt-layer contracts, "
                    "typed specialist panels, client advisory endpoints, and pending multi-agent runtime evolution."
                ),
                "output_schema": (
                    '{"scope_insights":[{"insight_id":"string","title":"string","summary":"string","focus_area":"customer_scope|architecture|internal_platform","tone":"neutral|success|warning|critical"}],'
                    '"strategy_options":[{"option_id":"string","title":"string","summary":"string","benefits":["string"],"tradeoffs":["string"],"recommended_when":"string"}],'
                    '"architecture_advice":{"current_state":"string","target_state":"string","key_constraints":["string"],"proposed_changes":["string"],"risks":["string"]},'
                    '"internal_improvement_backlog":[{"item_id":"string","title":"string","rationale":"string","priority":"now|next|later","impact":"low|medium|high","effort":"small|medium|large","owner_hint":"string"}],"approval_required":true}'
                ),
            },
        )
        generation = self.model_gateway.generate_structured_json(
            prompt=prompt,
            fallback_payload={
                "scope_insights": [item.model_dump() for item in fallback_response.scope_insights],
                "strategy_options": [item.model_dump() for item in fallback_response.strategy_options],
                "architecture_advice": fallback_response.architecture_advice.model_dump(),
                "internal_improvement_backlog": [
                    item.model_dump() for item in fallback_response.internal_improvement_backlog
                ],
                "approval_required": fallback_response.approval_required,
            },
        )

        try:
            return CTOCIOPanelResponse.model_validate(
                {
                    "agent_id": agent.agent_id,
                    "display_name": agent.display_name,
                    "role_summary": agent.role_summary,
                    "primary_track": agent.deployment.primary_track,
                    "operating_modes": agent.operating_modes,
                    "tool_profile_by_mode": agent.tool_profile_by_mode,
                    "provider_used": generation.provider_used,
                    "model_used": generation.model_used,
                    "local_llm_invoked": generation.local_llm_invoked,
                    "cloud_llm_invoked": generation.cloud_llm_invoked,
                    "llm_diagnostic_code": generation.llm_diagnostic_code,
                    "llm_diagnostic_detail": generation.llm_diagnostic_detail,
                    **generation.content,
                }
            )
        except Exception:
            return fallback_response.model_copy(
                update=self._fallback_generation_metadata(
                    generation.provider_used,
                    generation.model_used,
                    generation.local_llm_invoked,
                    generation.cloud_llm_invoked,
                    generation.llm_diagnostic_code,
                    generation.llm_diagnostic_detail,
                    "The structured CTO/CIO panel response did not match the expected schema, so the rule-based panel was returned.",
                )
            )

    def _build_fallback_panel(self, agent: AgentContract) -> CTOCIOPanelResponse:
        scope_insights = [
            CTOCIOScopeInsight(
                insight_id="scope-signal-delivery",
                title="Delivery system is ready for advisory packaging",
                summary=(
                    "The platform already has distinct BA, architect, build, QA, PMO, and documentation "
                    "families, which makes it viable to shape advisory recommendations into repeatable "
                    "delivery offers."
                ),
                focus_area="customer_scope",
                tone="success",
            ),
            CTOCIOScopeInsight(
                insight_id="scope-signal-controls",
                title="Control-plane foundations reduce architecture risk",
                summary=(
                    "State, events, autonomy, tool profiles, and prompt composition are now modeled in "
                    "contracts, so solution guidance can reference real operating controls rather than "
                    "only markdown intent."
                ),
                focus_area="architecture",
                tone="success",
            ),
            CTOCIOScopeInsight(
                insight_id="scope-signal-ui",
                title="Executive advisory surfaces still need operator panels",
                summary=(
                    "The React cockpit now has CTO/CIO, finance, and AI strategy specialist surfaces, so "
                    "the next gap is turning those advisory views into repeatable operator routines and offer packaging."
                ),
                focus_area="internal_platform",
                tone="warning",
            ),
        ]

        counsel = CTOCIOCounselOutput(
            analysis_summary=(
                "The current CTO/CIO panel remains an internal summary surface. Client-specific analysis "
                "is available through the dedicated advisory analysis endpoint."
            ),
            mission_assessment=MissionAssessment(
                mission_id="internal-panel-posture",
                consulting_motion="mixed",
                title="Internal advisory operating posture",
                summary="The CTO/CIO panel summarizes strategy, architecture, and offer-packaging priorities.",
                client_need="Internal operator visibility over advisory packaging and platform direction.",
                success_definition="Operators can turn advisory thinking into repeatable offerings and safer execution.",
                why_now="The panel is an internal operating surface rather than a client-engagement output.",
            ),
            strategy_options=[
                StrategyOption(
                    option_id="stabilize-and-package",
                    title="Stabilize and package the advisory operating layer",
                    summary=(
                        "Prioritize specialist cockpit surfaces and reusable advisory outputs before "
                        "introducing deeper runtime dynamism."
                    ),
                    benefits=[
                        "Makes the internal advisory model visible and saleable",
                        "Improves operator trust before more autonomy is introduced",
                        "Turns existing architecture work into customer-facing leverage",
                    ],
                    tradeoffs=[
                        "Delays deeper runtime-splitting work for some delivery specialists",
                        "Adds UI work before richer operational analytics exist",
                    ],
                    recommended_when="Use this when the immediate priority is to operationalize advisory value.",
                ),
                StrategyOption(
                    option_id="advance-multi-agent-foundations",
                    title="Advance multi-agent delivery foundations next",
                    summary=(
                        "Invest in step identity, agent execution logs, and handoff metadata so Delivery "
                        "can evolve into the flagship multi-agent runtime."
                    ),
                    benefits=[
                        "Strengthens the future delivery pod runtime model",
                        "Improves observability for agent-to-agent handoffs",
                    ],
                    tradeoffs=[
                        "Near-term advisory UX remains lighter",
                        "Customer-facing CTO/CIO output stays less polished in the cockpit",
                    ],
                    recommended_when="Use this when delivery-runtime maturity is more urgent than advisory packaging.",
                ),
                StrategyOption(
                    option_id="productize-selected-advisory-offers",
                    title="Productize selected advisory offers",
                    summary=(
                        "Package CTO/CIO guidance, architecture reviews, and internal platform audits into "
                        "repeatable offer structures with bounded templates."
                    ),
                    benefits=[
                        "Creates clearer sales positioning for high-value advisory work",
                        "Leverages internal-first agent families for billable client delivery",
                    ],
                    tradeoffs=[
                        "Needs more template and evidence curation",
                        "Requires stronger reporting and presentation surfaces",
                    ],
                    recommended_when="Use this when commercial packaging becomes the priority.",
                ),
            ],
            architecture_advice=ArchitectureAdvice(
                current_state=(
                    "The platform is workflow-first, approval-bound, and now has normalized contracts for "
                    "state, events, tool profiles, and prompt composition."
                ),
                target_state=(
                    "Mission Control should expose specialist advisory views while the backend grows into a "
                    "more observable, workflow-mediated multi-agent operating system."
                ),
                key_constraints=[
                    "Keep the MVP workflow-first and avoid uncontrolled peer-agent behavior",
                    "Do not force full prompt authoring before more delivery surfaces are live",
                    "Preserve Track A and Track B isolation even for reusable advisory families",
                ],
                proposed_changes=[
                    "Add specialist cockpit panels for CTO/CIO, finance, and Chief AI / Digital Strategy",
                    "Continue with step-level metadata before deeper runtime promotion",
                    "Gradually migrate prompt assets into the canonical prompt filesystem layout",
                ],
                risks=[
                    "Advisory outputs may stay too abstract if they are not tied to live operator surfaces",
                    "Runtime complexity could outpace observability if multi-agent features are rushed",
                ],
            ),
            internal_improvement_backlog=[
                ImprovementBacklogItem(
                    item_id="cto-panel",
                    title="Finish specialist advisory cockpit surfaces",
                    rationale="The advisory model is defined, but mission control still needs dedicated panels for operators.",
                    priority="now",
                    impact="high",
                    effort="medium",
                    owner_hint="frontend + api",
                ),
                ImprovementBacklogItem(
                    item_id="step-agent-identity",
                    title="Persist per-step agent identity and handoff metadata",
                    rationale="This is the control boundary needed before broader multi-agent runtime promotion.",
                    priority="next",
                    impact="high",
                    effort="medium",
                    owner_hint="backend orchestration",
                ),
                ImprovementBacklogItem(
                    item_id="prompt-migration",
                    title="Migrate new prompt assets into canonical `agents/` and `workflows/` layout",
                    rationale="The convention is now defined; new prompt authoring should stop adding drift.",
                    priority="next",
                    impact="medium",
                    effort="small",
                    owner_hint="runtime prompt layer",
                ),
            ],
            approval_required=True,
        )

        return CTOCIOPanelResponse(
            agent_id=agent.agent_id,
            display_name=agent.display_name,
            role_summary=agent.role_summary,
            primary_track=agent.deployment.primary_track,
            operating_modes=agent.operating_modes,
            tool_profile_by_mode=agent.tool_profile_by_mode,
            provider_used="fallback-rule",
            model_used="rules-v1",
            local_llm_invoked=False,
            cloud_llm_invoked=False,
            llm_diagnostic_code=None,
            llm_diagnostic_detail=None,
            scope_insights=scope_insights,
            strategy_options=counsel.strategy_options,
            architecture_advice=counsel.architecture_advice,
            internal_improvement_backlog=counsel.internal_improvement_backlog,
            approval_required=counsel.approval_required,
        )

    def analyze_client_context(
        self,
        *,
        agent: AgentContract,
        payload: CTOCIOCounselInput,
    ) -> CTOCIOAnalysisResponse:
        combined_text = self._combine_text(payload)
        fallback_counsel = self._build_fallback_output(payload, combined_text)
        prompt = self.prompt_loader.render_composition(
            "specialist-advisory.cto-cio-analyze",
            template_context={
                "engagement_name": payload.engagement_name,
                "problem_statement": payload.problem_statement,
                "business_goal": payload.business_goal,
                "client_context": payload.client_context or "none",
                "engagement_history": self._format_list(payload.engagement_history),
                "current_stack": self._format_list(payload.current_stack),
                "constraints": self._format_list(payload.constraints),
                "desired_outcomes": self._format_list(payload.desired_outcomes),
                "internal_platform_needs": self._format_list(payload.internal_platform_needs),
            },
            injected_context={
                "approval_policy": (
                    "Advisory output only. No roadmap commitment, commercial commitment, or client promise is final "
                    "without explicit CEO review and approval."
                ),
                "autonomy_policy": (
                    "Use LLM reasoning for consulting judgment, but stay within bounded consulting advice. "
                    "Do not invent facts, commitments, budgets, or approvals."
                ),
                "tool_profile": "specialist-advisory profile; client brief interpretation only in this endpoint.",
                "state_summary": (
                    "Client-scoped advisory instance. Track A and Track B context must stay isolated. "
                    "Use only the supplied brief plus injected runtime policy."
                ),
                "output_schema": (
                    '{"analysis_summary":"string","mission_assessment":{"mission_id":"string","consulting_motion":"problem_solving|opportunity_discovery|account_growth|mixed","title":"string","summary":"string","client_need":"string","success_definition":"string","why_now":"string"},'
                    '"context_signals":[{"signal_id":"string","category":"problem|history|constraint|readiness|risk|opportunity","title":"string","summary":"string","implication":"string"}],'
                    '"recommended_services":[{"service_id":"string","name":"string","summary":"string","fit_reason":"string","suggested_outcomes":["string"],"delivery_mode":"client_delivery|client_facing_service","priority":"now|next|later"}],'
                    '"upsell_opportunities":[{"opportunity_id":"string","title":"string","summary":"string","rationale":"string","suggested_service":"string","expansion_trigger":"string","priority":"now|next|later"}],'
                    '"strategy_options":[{"option_id":"string","title":"string","summary":"string","benefits":["string"],"tradeoffs":["string"],"recommended_when":"string"}],'
                    '"architecture_advice":{"current_state":"string","target_state":"string","key_constraints":["string"],"proposed_changes":["string"],"risks":["string"]},"approval_required":true}'
                ),
            },
        )
        generation = self.model_gateway.generate_structured_json(
            prompt=prompt,
            fallback_payload=fallback_counsel.model_dump(),
        )
        response_provider_used = generation.provider_used
        response_model_used = generation.model_used
        response_diagnostic_code = generation.llm_diagnostic_code
        response_diagnostic_detail = generation.llm_diagnostic_detail
        try:
            counsel = CTOCIOCounselOutput.model_validate(generation.content)
        except Exception:
            counsel = fallback_counsel
            response_provider_used = "fallback-rule"
            response_model_used = "rules-v1"
            response_diagnostic_code = self._combine_diagnostic_code(
                generation.llm_diagnostic_code,
                "structured_response_validation_failed",
            )
            response_diagnostic_detail = self._combine_diagnostic_detail(
                generation.llm_diagnostic_detail,
                "The structured CTO/CIO analysis response did not match the expected schema, so the rule-based advisory output was returned.",
            )

        return CTOCIOAnalysisResponse(
            agent_id=agent.agent_id,
            display_name=agent.display_name,
            role_summary=agent.role_summary,
            primary_track=agent.deployment.primary_track,
            operating_modes=agent.operating_modes,
            tool_profile_by_mode=agent.tool_profile_by_mode,
            provider_used=response_provider_used,
            model_used=response_model_used,
            local_llm_invoked=generation.local_llm_invoked,
            cloud_llm_invoked=generation.cloud_llm_invoked,
            llm_diagnostic_code=response_diagnostic_code,
            llm_diagnostic_detail=response_diagnostic_detail,
            analysis_summary=counsel.analysis_summary,
            mission_assessment=counsel.mission_assessment,
            context_signals=counsel.context_signals,
            recommended_services=counsel.recommended_services,
            upsell_opportunities=counsel.upsell_opportunities,
            strategy_options=counsel.strategy_options,
            architecture_advice=counsel.architecture_advice,
            approval_required=counsel.approval_required,
        )

    def _build_fallback_output(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> CTOCIOCounselOutput:
        return CTOCIOCounselOutput(
            analysis_summary=(
                f"{payload.engagement_name} should be handled like a consulting engagement: solve the active "
                "technology mission, use the client context and history to shape delivery, and surface adjacent "
                "opportunities that can grow the account without losing focus."
            ),
            mission_assessment=self._build_mission_assessment(payload, combined_text),
            context_signals=self._build_context_signals(payload, combined_text),
            recommended_services=self._build_recommended_services(payload, combined_text),
            upsell_opportunities=self._build_upsell_opportunities(payload, combined_text),
            strategy_options=self._build_strategy_options(payload, combined_text),
            architecture_advice=self._build_architecture_advice(payload, combined_text),
            internal_improvement_backlog=[],
            approval_required=True,
        )

    def _combine_text(self, payload: CTOCIOCounselInput) -> str:
        return " ".join(
            [
                payload.problem_statement,
                payload.business_goal,
                payload.client_context,
                " ".join(payload.engagement_history),
                " ".join(payload.current_stack),
                " ".join(payload.constraints),
                " ".join(payload.desired_outcomes),
                " ".join(payload.internal_platform_needs),
            ]
        ).lower()

    def _build_context_signals(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> list[ContextSignal]:
        signals = [
            ContextSignal(
                signal_id="core-need",
                category="problem",
                title="Problem statement anchors the advisory brief",
                summary=payload.problem_statement,
                implication=(
                    "Recommendations should stay tied to this business problem instead of jumping straight "
                    "into tools or platform choices."
                ),
            )
        ]

        if payload.engagement_history:
            signals.append(
                ContextSignal(
                    signal_id="history-pattern",
                    category="history",
                    title="Prior context should shape the next move",
                    summary=" | ".join(payload.engagement_history[:3]),
                    implication=(
                        "The advisory path should reuse known lessons and avoid proposing a reset that "
                        "ignores what the client has already tried."
                    ),
                )
            )

        if payload.constraints:
            signals.append(
                ContextSignal(
                    signal_id="delivery-constraints",
                    category="constraint",
                    title="Constraints narrow the feasible architecture path",
                    summary=", ".join(payload.constraints[:4]),
                    implication=(
                        "The recommended services need to fit real delivery, budget, compliance, or timing boundaries."
                    ),
                )
            )

        if self._contains_any(
            combined_text,
            "legacy",
            "integration",
            "api",
            "spreadsheet",
            "manual handoff",
            "silo",
            "erp",
            "crm",
        ):
            signals.append(
                ContextSignal(
                    signal_id="integration-friction",
                    category="risk",
                    title="Architecture friction is likely coming from system sprawl",
                    summary=(
                        "The brief points to fragmented systems or brittle handoffs, which usually means "
                        "the highest-value advisory work starts with integration and target-state simplification."
                    ),
                    implication=(
                        "Lead with architecture review and phased modernization rather than a full replacement recommendation."
                    ),
                )
            )

        if self._contains_any(
            combined_text,
            "security",
            "compliance",
            "audit",
            "privacy",
            "risk",
            "gdpr",
        ):
            signals.append(
                ContextSignal(
                    signal_id="control-pressure",
                    category="risk",
                    title="Control and assurance requirements are material",
                    summary=(
                        "The client context includes explicit risk or compliance pressure, so advisory work "
                        "has to include governance, approval, and evidence concerns."
                    ),
                    implication=(
                        "Any target architecture should include control points, traceability, and human approval boundaries."
                    ),
                )
            )

        if not payload.constraints and not payload.engagement_history:
            signals.append(
                ContextSignal(
                    signal_id="discovery-gap",
                    category="readiness",
                    title="Discovery detail is still light",
                    summary=(
                        "The brief includes a clear problem statement, but history and constraints are still thin."
                    ),
                    implication=(
                        "Start with a short assessment sprint before locking a larger delivery recommendation."
                    ),
                )
            )

        return signals[:5]

    def _build_mission_assessment(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> MissionAssessment:
        consulting_motion = "problem_solving"
        if self._contains_any(
            combined_text,
            "strategy",
            "roadmap",
            "growth",
            "new market",
            "productize",
            "scale",
        ):
            consulting_motion = "mixed"

        return MissionAssessment(
            mission_id="cto-cio-client-mission",
            consulting_motion=consulting_motion,
            title=f"Technology consulting mission for {payload.engagement_name}",
            summary=(
                "Interpret the stated business problem like a consultant on the account: define the mission, "
                "recommend the most relevant service path, and keep an eye on follow-on opportunities."
            ),
            client_need=payload.business_goal,
            success_definition=(
                "The client gets a credible technology direction, a scoped next move, and a short list of "
                "adjacent consulting opportunities worth discussing."
            ),
            why_now=(
                "The combination of problem statement, client context, and engagement history is strong enough "
                "to move beyond generic advice into a consulting recommendation."
            ),
        )

    def _build_recommended_services(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> list[RecommendedService]:
        recommendations: list[RecommendedService] = [
            RecommendedService(
                service_id="technology-strategy-assessment",
                name="Technology Strategy Assessment",
                summary=(
                    "Frame the problem, review the existing landscape, and produce a bounded target-state recommendation."
                ),
                fit_reason=(
                    "The client is asking for direction, so the first service should turn problem context and "
                    "history into a practical decision pack."
                ),
                suggested_outcomes=[
                    "current-state diagnosis",
                    "target-state options",
                    "sequenced decision memo",
                ],
                delivery_mode="client_facing_service",
                priority="now",
            )
        ]

        if self._contains_any(
            combined_text,
            "legacy",
            "integration",
            "api",
            "erp",
            "crm",
            "spreadsheet",
            "manual",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="architecture-modernization-review",
                    name="Architecture Review and Modernization Plan",
                    summary="Map the current stack, identify failure points, and define a phased integration or modernization plan.",
                    fit_reason=(
                        "The client context suggests system sprawl or brittle handoffs that need architecture-level simplification."
                    ),
                    suggested_outcomes=[
                        "integration risk map",
                        "phased modernization roadmap",
                        "priority architecture decisions",
                    ],
                    delivery_mode="client_delivery",
                    priority="now",
                )
            )

        if self._contains_any(
            combined_text,
            "security",
            "compliance",
            "audit",
            "privacy",
            "approval",
            "risk",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="governance-controls-review",
                    name="Governance and Control Review",
                    summary="Define approval boundaries, control points, and evidence requirements around the target solution.",
                    fit_reason=(
                        "Risk and compliance signals are strong enough that architecture advice alone would be incomplete."
                    ),
                    suggested_outcomes=[
                        "control-boundary map",
                        "approval policy outline",
                        "risk register starter",
                    ],
                    delivery_mode="client_facing_service",
                    priority="now",
                )
            )

        if self._contains_any(
            combined_text,
            "delivery",
            "handoff",
            "project",
            "roadmap",
            "deadline",
            "governance",
            "portfolio",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="delivery-governance-reset",
                    name="Delivery Governance Reset",
                    summary="Tighten milestones, ownership, and steering routines so delivery can support the target architecture.",
                    fit_reason=(
                        "The brief points to execution friction, so the client likely needs operating-model help alongside technical advice."
                    ),
                    suggested_outcomes=[
                        "governance cadence",
                        "checkpoint model",
                        "decision ownership map",
                    ],
                    delivery_mode="client_delivery",
                    priority="next",
                )
            )

        return recommendations[:4]

    def _build_upsell_opportunities(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> list[UpsellOpportunity]:
        opportunities: list[UpsellOpportunity] = []

        if self._contains_any(combined_text, "legacy", "integration", "erp", "crm", "manual", "spreadsheet"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-integration-governance",
                    title="Expand from architecture advice into integration governance support",
                    summary="The current problem likely sits on top of broader integration and operating-model issues.",
                    rationale=(
                        "Once the immediate mission is framed, the same client may need phased governance, "
                        "decision support, and modernization oversight."
                    ),
                    suggested_service="Architecture Review and Modernization Plan",
                    expansion_trigger="Multiple systems and brittle handoffs are already visible in the brief.",
                    priority="now",
                )
            )

        if self._contains_any(combined_text, "security", "compliance", "audit", "privacy", "risk"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-controls",
                    title="Extend the mission into governance and control advisory",
                    summary="Risk and compliance pressure creates room for a follow-on control-design engagement.",
                    rationale=(
                        "A technology recommendation will be easier to buy and implement if it is paired with "
                        "approval, auditability, and operating-control guidance."
                    ),
                    suggested_service="Governance and Control Review",
                    expansion_trigger="The client already signals assurance or compliance pressure.",
                    priority="now",
                )
            )

        if self._contains_any(combined_text, "delivery", "project", "deadline", "portfolio", "handoff", "governance"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-delivery-oversight",
                    title="Add delivery coordination or PMO support around the technical mission",
                    summary="Execution friction suggests the account could benefit from consulting support beyond architecture.",
                    rationale=(
                        "Clients often need help turning strategy into checkpoints, steering, and accountable follow-through."
                    ),
                    suggested_service="Delivery Governance Reset",
                    expansion_trigger="The brief points to slippage, weak checkpoints, or ownership ambiguity.",
                    priority="next",
                )
            )

        if payload.internal_platform_needs:
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-platform-improvement",
                    title="Package a follow-on internal platform improvement roadmap",
                    summary="The account may grow from one mission into a broader improvement portfolio.",
                    rationale=(
                        "The current ask includes platform improvement needs that could become a structured advisory retainer."
                    ),
                    suggested_service="Technology Strategy Assessment",
                    expansion_trigger="The brief includes multiple internal platform needs beyond the immediate issue.",
                    priority="next",
                )
            )

        return opportunities[:4]

    def _build_strategy_options(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> list[StrategyOption]:
        options = [
            StrategyOption(
                option_id="stabilize-current-state",
                title=f"Stabilize the current estate around {payload.engagement_name}",
                summary=(
                    "Reduce the most immediate delivery or architecture friction first, then sequence deeper change."
                ),
                benefits=[
                    "Creates a lower-risk starting point",
                    "Builds trust with visible early control improvements",
                ],
                tradeoffs=[
                    "Some structural problems remain in place longer",
                    "Longer path to a cleaner target architecture",
                ],
                recommended_when="Use this when delivery risk or stakeholder confidence is the immediate issue.",
            ),
            StrategyOption(
                option_id="modernize-high-friction-slice",
                title="Modernize the highest-friction slice first",
                summary=(
                    "Pick the system boundary causing the most pain and redesign that slice with clear interfaces and controls."
                ),
                benefits=[
                    "Targets business pain directly",
                    "Produces an architecture proof point without a full-program commitment",
                ],
                tradeoffs=[
                    "Requires careful scoping to avoid local optimization",
                ],
                recommended_when="Use this when one workflow or integration seam is clearly driving the problem.",
            ),
        ]

        if self._contains_any(combined_text, "security", "compliance", "audit", "privacy"):
            options.append(
                StrategyOption(
                    option_id="control-led-transformation",
                    title="Lead the transformation through control design",
                    summary=(
                        "Use governance, traceability, and approval boundaries as the frame for the architecture roadmap."
                    ),
                    benefits=[
                        "Matches regulated or high-risk environments",
                        "Makes implementation decisions easier to defend",
                    ],
                    tradeoffs=[
                        "Adds design overhead early",
                        "Can feel slower without disciplined scope control",
                    ],
                    recommended_when="Use this when assurance and auditability are part of the buying criteria.",
                )
            )

        return options

    def _build_architecture_advice(
        self,
        payload: CTOCIOCounselInput,
        combined_text: str,
    ) -> ArchitectureAdvice:
        key_constraints = payload.constraints[:]
        if not key_constraints:
            key_constraints.append("Discovery constraints still need confirmation with the client sponsor.")

        proposed_changes = [
            "Translate the problem statement into a bounded current-state and target-state architecture brief.",
            "Prioritize one or two decision points that unblock the stated business goal fastest.",
        ]
        if payload.current_stack:
            proposed_changes.append(
                f"Review the current stack boundary across {', '.join(payload.current_stack[:4])} before proposing replacement or migration."
            )
        if payload.desired_outcomes:
            proposed_changes.append(
                f"Use desired outcomes such as {', '.join(payload.desired_outcomes[:3])} to sequence the roadmap."
            )

        risks = []
        if self._contains_any(combined_text, "legacy", "integration", "spreadsheet", "manual"):
            risks.append("Integration debt may hide more delivery effort than the brief first suggests.")
        if self._contains_any(combined_text, "security", "compliance", "audit", "privacy"):
            risks.append("Control gaps could block implementation if governance is left for later.")
        if not risks:
            risks.append("Discovery assumptions may drift unless the current-state assessment is evidence-backed.")

        return ArchitectureAdvice(
            current_state=(
                f"{payload.engagement_name} presents a technology problem that should be interpreted in light of "
                "existing context, delivery history, and real operating constraints."
            ),
            target_state=(
                "A sequenced target architecture with explicit control boundaries, clear ownership, and a small set "
                "of high-confidence delivery moves tied directly to the business goal."
            ),
            key_constraints=key_constraints,
            proposed_changes=proposed_changes,
            risks=risks,
        )

    def _contains_any(self, text: str, *keywords: str) -> bool:
        return any(keyword in text for keyword in keywords)

    def _combine_diagnostic_code(self, *codes: str | None) -> str | None:
        unique_codes = []
        for code in codes:
            if code and code not in unique_codes:
                unique_codes.append(code)
        if not unique_codes:
            return None
        if len(unique_codes) == 1:
            return unique_codes[0]
        return "multiple_llm_failures"

    def _combine_diagnostic_detail(self, *details: str | None) -> str | None:
        unique_details = []
        for detail in details:
            if detail and detail not in unique_details:
                unique_details.append(detail)
        if not unique_details:
            return None
        return " ".join(unique_details)

    def _fallback_generation_metadata(
        self,
        provider_used: str,
        model_used: str,
        local_llm_invoked: bool,
        cloud_llm_invoked: bool,
        llm_diagnostic_code: str | None,
        llm_diagnostic_detail: str | None,
        validation_detail: str,
    ) -> dict[str, str | bool | None]:
        attempted_path = None
        if provider_used != "fallback-rule":
            attempted_path = f"Attempted model path before fallback: {provider_used} / {model_used}."
        return {
            "provider_used": "fallback-rule",
            "model_used": "rules-v1",
            "local_llm_invoked": local_llm_invoked,
            "cloud_llm_invoked": cloud_llm_invoked,
            "llm_diagnostic_code": self._combine_diagnostic_code(
                llm_diagnostic_code,
                "structured_response_validation_failed",
            ),
            "llm_diagnostic_detail": self._combine_diagnostic_detail(
                llm_diagnostic_detail,
                validation_detail,
                attempted_path,
            ),
        }

    def _format_list(self, items: list[str]) -> str:
        if not items:
            return "- none"
        return "\n".join(f"- {item}" for item in items)

    def _panel_platform_context(self) -> str:
        return (
            "The platform is workflow-first and approval-bound. Mission Control exposes specialist panels for CTO/CIO, "
            "finance, and Chief AI. Prompt-layer contracts, tool profiles, autonomy classes, and client-facing advisory "
            "analysis endpoints now exist. The next challenge is to convert this capability into stronger internal "
            "counsel, operator trust, and repeatable consulting offers without outrunning observability or governance."
        )
