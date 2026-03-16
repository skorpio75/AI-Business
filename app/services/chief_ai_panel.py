from dataclasses import dataclass

from app.core.prompt_loader import PromptLoader
from app.core.settings import Settings
from app.models.agent_contract import AgentContract
from app.models.schemas import ChiefAIAnalysisResponse, ChiefAIPanelResponse, ChiefAIScopeSignal
from app.models.specialist_contracts import (
    ChiefAIDigitalStrategyOutput,
    ChiefAIDigitalStrategyInput,
    ContextSignal,
    DeliveryBlueprintPhase,
    MaturityDimension,
    MissionAssessment,
    OpportunityMapItem,
    RecommendedService,
    UpsellOpportunity,
)
from app.services.model_gateway import ModelGateway


@dataclass
class PanelSectionRoute:
    section_name: str
    provider_used: str
    model_used: str
    local_llm_invoked: bool
    cloud_llm_invoked: bool
    llm_diagnostic_code: str | None = None
    llm_diagnostic_detail: str | None = None


class ChiefAIPanelService:
    PANEL_LOCAL_MODEL = "qwen2.5:1.5b-instruct-q4_K_M"

    def __init__(self, model_gateway: ModelGateway | None = None) -> None:
        self.model_gateway = model_gateway or ModelGateway(settings=Settings())
        self.prompt_loader = PromptLoader()

    def build_panel(self, *, agent: AgentContract) -> ChiefAIPanelResponse:
        fallback_response = self._build_fallback_panel(agent)
        summary_generation = self.model_gateway.generate_text(
            prompt=self._render_delimited_panel_prompt(
                agent=agent,
                section_name="executive_summary",
                section_focus="Return one concise executive summary under 18 words.",
                line_format="executive_summary",
            ),
            fallback_content=fallback_response.executive_summary,
            local_num_predict=45,
            local_timeout_seconds=15,
            local_model_override=self.PANEL_LOCAL_MODEL,
        )
        signal_generation = self.model_gateway.generate_text(
            prompt=self._render_delimited_panel_prompt(
                agent=agent,
                section_name="scope_signals",
                section_focus="Return 1 or 2 AI strategy scope signals with short titles and summaries.",
                line_format="signal_id||title||summary||focus_area",
            ),
            fallback_content=self._serialize_scope_signals(fallback_response.scope_signals),
            local_num_predict=90,
            local_timeout_seconds=15,
            local_model_override=self.PANEL_LOCAL_MODEL,
        )
        opportunity_generation = self.model_gateway.generate_text(
            prompt=self._render_delimited_panel_prompt(
                agent=agent,
                section_name="opportunity_map",
                section_focus="Return 1 or 2 opportunity items with short fields.",
                line_format="opportunity_id||title||problem_statement||expected_value||priority||dependency",
            ),
            fallback_content=self._serialize_opportunity_map(fallback_response.opportunity_map),
            local_num_predict=90,
            local_timeout_seconds=15,
            local_model_override=self.PANEL_LOCAL_MODEL,
        )
        blueprint_generation = self.model_gateway.generate_text(
            prompt=self._render_delimited_panel_prompt(
                agent=agent,
                section_name="delivery_blueprint",
                section_focus="Return 1 or 2 blueprint phases with short objectives, deliverables, and risks.",
                line_format="phase_id||title||objective||deliverable||risk",
            ),
            fallback_content=self._serialize_delivery_blueprint(fallback_response.delivery_blueprint),
            local_num_predict=110,
            local_timeout_seconds=15,
            local_model_override=self.PANEL_LOCAL_MODEL,
        )
        maturity_generation = self.model_gateway.generate_text(
            prompt=self._render_delimited_panel_prompt(
                agent=agent,
                section_name="maturity_model",
                section_focus="Return 1 or 2 maturity dimensions with brief gap summary and actions.",
                line_format="dimension||current_level||target_level||gap_summary||next_action",
            ),
            fallback_content=self._serialize_maturity_model(fallback_response.maturity_model),
            local_num_predict=95,
            local_timeout_seconds=15,
            local_model_override=self.PANEL_LOCAL_MODEL,
        )

        executive_summary, summary_route = self._resolve_summary_section(
            section_name="executive_summary",
            generation=summary_generation,
            fallback_value=fallback_response.executive_summary,
            validation_detail="The executive summary section did not match the expected schema, so the fallback summary was used.",
        )
        scope_signals, signal_route = self._resolve_scope_signals_section(
            section_name="scope_signals",
            generation=signal_generation,
            fallback_items=fallback_response.scope_signals,
            validation_detail="The scope signals section did not match the expected schema, so fallback signals were used.",
        )
        opportunity_map, opportunity_route = self._resolve_opportunity_map_section(
            section_name="opportunity_map",
            generation=opportunity_generation,
            fallback_items=fallback_response.opportunity_map,
            validation_detail="The opportunity map section did not match the expected schema, so fallback opportunities were used.",
        )
        delivery_blueprint, blueprint_route = self._resolve_delivery_blueprint_section(
            section_name="delivery_blueprint",
            generation=blueprint_generation,
            fallback_items=fallback_response.delivery_blueprint,
            validation_detail="The delivery blueprint section did not match the expected schema, so the fallback blueprint was used.",
        )
        maturity_model, maturity_route = self._resolve_maturity_model_section(
            section_name="maturity_model",
            generation=maturity_generation,
            fallback_items=fallback_response.maturity_model,
            validation_detail="The maturity model section did not match the expected schema, so the fallback maturity model was used.",
        )
        route_summary = self._summarize_panel_routes(
            panel_name="Chief AI panel",
            routes=[summary_route, signal_route, opportunity_route, blueprint_route, maturity_route],
        )

        return ChiefAIPanelResponse(
            agent_id=agent.agent_id,
            display_name=agent.display_name,
            role_summary=agent.role_summary,
            primary_track=agent.deployment.primary_track,
            operating_modes=agent.operating_modes,
            tool_profile_by_mode=agent.tool_profile_by_mode,
            provider_used=route_summary["provider_used"],
            model_used=route_summary["model_used"],
            local_llm_invoked=route_summary["local_llm_invoked"],
            cloud_llm_invoked=route_summary["cloud_llm_invoked"],
            llm_diagnostic_code=route_summary["llm_diagnostic_code"],
            llm_diagnostic_detail=route_summary["llm_diagnostic_detail"],
            executive_summary=executive_summary,
            scope_signals=scope_signals,
            opportunity_map=opportunity_map,
            delivery_blueprint=delivery_blueprint,
            maturity_model=maturity_model,
            approval_required=fallback_response.approval_required,
        )

    def _render_delimited_panel_prompt(
        self,
        *,
        agent: AgentContract,
        section_name: str,
        section_focus: str,
        line_format: str,
    ) -> str:
        section_rules = {
            "scope_signals": "Use focus_area=offer_design|delivery_controls|commercialization and tone=neutral|success|warning|critical.",
            "opportunity_map": "Use priority=now|next|later.",
            "maturity_model": "Use maturity levels ad_hoc|emerging|repeatable|managed|optimized.",
        }
        return (
            "Chief AI panel. "
            "Context: AI advisory packaging, delivery controls, commercialization pressure. "
            f"{section_focus} "
            f"Format: {line_format}. "
            f"{section_rules.get(section_name, '')} "
            f"Example: {self._section_example(section_name)} "
            "Return only the line or lines."
        )

    def _resolve_summary_section(
        self,
        *,
        section_name: str,
        generation,
        fallback_value: str,
        validation_detail: str,
    ) -> tuple[str, PanelSectionRoute]:
        if isinstance(generation.content, str) and generation.content.strip():
            summary = self._clean_delimited_field(generation.content.strip().splitlines()[0])
            if summary:
                return summary, self._route_from_generation(section_name=section_name, generation=generation)
        return fallback_value, self._validation_fallback_route(
            section_name=section_name,
            generation=generation,
            validation_detail=validation_detail,
        )

    def _serialize_scope_signals(self, items: list[ChiefAIScopeSignal]) -> str:
        return "\n".join(
            f"{item.signal_id}||{item.title}||{item.summary}||{item.focus_area}||{item.tone}" for item in items
        )

    def _serialize_opportunity_map(self, items: list[OpportunityMapItem]) -> str:
        return "\n".join(
            "||".join(
                [
                    item.opportunity_id,
                    item.title,
                    item.problem_statement,
                    item.expected_value,
                    item.priority,
                    ";".join(item.dependencies[:2]),
                ]
            )
            for item in items
        )

    def _serialize_delivery_blueprint(self, items: list[DeliveryBlueprintPhase]) -> str:
        return "\n".join(
            "||".join(
                [
                    item.phase_id,
                    item.title,
                    ";".join(item.objectives[:2]),
                    ";".join(item.deliverables[:2]),
                    ";".join(item.risks[:2]),
                ]
            )
            for item in items
        )

    def _serialize_maturity_model(self, items: list[MaturityDimension]) -> str:
        return "\n".join(
            "||".join(
                [
                    item.dimension,
                    item.current_level,
                    item.target_level,
                    item.gap_summary,
                    ";".join(item.next_actions[:2]),
                ]
            )
            for item in items
        )

    def _section_example(self, section_name: str) -> str:
        examples = {
            "executive_summary": "Advisory packaging is improving but still needs faster, trustable local outputs",
            "scope_signals": "signal_01||Offer packaging gap||Capabilities are ahead of packaging||commercialization",
            "opportunity_map": "opp_01||AI delivery offer||Packaging is still unclear||Clearer offer narrative||now||proposal_assets",
            "delivery_blueprint": "phase_01||Discovery slice||map pain points||use-case shortlist||weak sponsorship",
            "maturity_model": "Operating model||repeatable||managed||Controls exist but packaging lags||package offers",
        }
        return examples.get(section_name, "signal_01||Short title||Short summary||offer_design||neutral")

    def _resolve_scope_signals_section(
        self,
        *,
        section_name: str,
        generation,
        fallback_items: list[ChiefAIScopeSignal],
        validation_detail: str,
    ) -> tuple[list[ChiefAIScopeSignal], PanelSectionRoute]:
        try:
            items = []
            for raw_line in generation.content.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = [self._clean_delimited_field(part) for part in line.split("||")]
                if len(parts) not in {4, 5}:
                    raise ValueError("scope_signal_parts_invalid")
                focus_area = parts[3]
                tone = "neutral"
                if len(parts) == 5:
                    tone = parts[4]
                elif "|" in parts[3]:
                    signal_parts = [self._clean_delimited_field(item) for item in parts[3].split("|") if self._clean_delimited_field(item)]
                    if signal_parts:
                        focus_area = signal_parts[-1]
                items.append(
                    ChiefAIScopeSignal.model_validate(
                        {
                            "signal_id": parts[0],
                            "title": parts[1],
                            "summary": parts[2],
                            "focus_area": self._normalize_chief_focus_area(focus_area),
                            "tone": self._normalize_tone(tone),
                        }
                    )
                )
            if items:
                return items, self._route_from_generation(section_name=section_name, generation=generation)
        except Exception:
            pass
        return fallback_items, self._validation_fallback_route(
            section_name=section_name,
            generation=generation,
            validation_detail=validation_detail,
        )

    def _resolve_opportunity_map_section(
        self,
        *,
        section_name: str,
        generation,
        fallback_items: list[OpportunityMapItem],
        validation_detail: str,
    ) -> tuple[list[OpportunityMapItem], PanelSectionRoute]:
        try:
            items = []
            for raw_line in generation.content.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = [self._clean_delimited_field(part) for part in line.split("||")]
                if len(parts) != 6:
                    raise ValueError("opportunity_parts_invalid")
                items.append(
                    OpportunityMapItem.model_validate(
                        {
                            "opportunity_id": parts[0],
                            "title": parts[1],
                            "problem_statement": parts[2],
                            "expected_value": parts[3],
                            "priority": self._normalize_priority(parts[4]),
                            "dependencies": self._split_delimited_list(parts[5]),
                        }
                    )
                )
            if items:
                return items, self._route_from_generation(section_name=section_name, generation=generation)
        except Exception:
            pass
        return fallback_items, self._validation_fallback_route(
            section_name=section_name,
            generation=generation,
            validation_detail=validation_detail,
        )

    def _resolve_delivery_blueprint_section(
        self,
        *,
        section_name: str,
        generation,
        fallback_items: list[DeliveryBlueprintPhase],
        validation_detail: str,
    ) -> tuple[list[DeliveryBlueprintPhase], PanelSectionRoute]:
        try:
            items = []
            for raw_line in generation.content.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = [self._clean_delimited_field(part) for part in line.split("||")]
                if len(parts) != 5:
                    raise ValueError("blueprint_parts_invalid")
                items.append(
                    DeliveryBlueprintPhase.model_validate(
                        {
                            "phase_id": parts[0],
                            "title": parts[1],
                            "objectives": self._split_delimited_list(parts[2]),
                            "deliverables": self._split_delimited_list(parts[3]),
                            "risks": self._split_delimited_list(parts[4]),
                        }
                    )
                )
            if items:
                return items, self._route_from_generation(section_name=section_name, generation=generation)
        except Exception:
            pass
        return fallback_items, self._validation_fallback_route(
            section_name=section_name,
            generation=generation,
            validation_detail=validation_detail,
        )

    def _resolve_maturity_model_section(
        self,
        *,
        section_name: str,
        generation,
        fallback_items: list[MaturityDimension],
        validation_detail: str,
    ) -> tuple[list[MaturityDimension], PanelSectionRoute]:
        try:
            items = []
            for raw_line in generation.content.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = [self._clean_delimited_field(part) for part in line.split("||")]
                if len(parts) != 5:
                    raise ValueError("maturity_parts_invalid")
                items.append(
                    MaturityDimension.model_validate(
                        {
                            "dimension": parts[0],
                            "current_level": self._normalize_maturity_level(parts[1]),
                            "target_level": self._normalize_maturity_level(parts[2]),
                            "gap_summary": parts[3],
                            "next_actions": self._split_delimited_list(parts[4]),
                        }
                    )
                )
            if items:
                return items, self._route_from_generation(section_name=section_name, generation=generation)
        except Exception:
            pass
        return fallback_items, self._validation_fallback_route(
            section_name=section_name,
            generation=generation,
            validation_detail=validation_detail,
        )

    def _clean_delimited_field(self, value: str) -> str:
        return value.strip().strip('"').strip("'")

    def _split_delimited_list(self, value: str) -> list[str]:
        return [self._clean_delimited_field(item) for item in value.split(";") if self._clean_delimited_field(item)]

    def _normalize_tone(self, value: str) -> str:
        normalized = self._clean_delimited_field(value).lower().replace(" ", "_")
        mapping = {
            "positive": "success",
            "negative": "critical",
            "informational": "neutral",
            "info": "neutral",
            "caution": "warning",
        }
        normalized = mapping.get(normalized, normalized)
        return normalized if normalized in {"neutral", "success", "warning", "critical"} else "neutral"

    def _normalize_chief_focus_area(self, value: str) -> str:
        normalized = self._clean_delimited_field(value).lower().replace(" ", "_")
        if normalized in {"offer_design", "delivery_controls", "commercialization"}:
            return normalized
        if "offer" in normalized or "service" in normalized or "packag" in normalized:
            return "offer_design"
        if "control" in normalized or "govern" in normalized or "delivery" in normalized:
            return "delivery_controls"
        return "commercialization"

    def _normalize_priority(self, value: str) -> str:
        normalized = self._clean_delimited_field(value).lower().replace(" ", "_")
        mapping = {
            "immediate": "now",
            "current": "now",
            "high": "now",
            "soon": "next",
            "medium": "next",
            "future": "later",
            "longer_term": "later",
            "long_term": "later",
            "low": "later",
        }
        normalized = mapping.get(normalized, normalized)
        return normalized if normalized in {"now", "next", "later"} else "next"

    def _normalize_maturity_level(self, value: str) -> str:
        normalized = self._clean_delimited_field(value).lower().replace(" ", "_").replace("-", "_")
        mapping = {
            "adhoc": "ad_hoc",
            "ad-hoc": "ad_hoc",
            "early": "emerging",
            "defined": "repeatable",
            "advanced": "managed",
            "leading": "optimized",
        }
        normalized = mapping.get(normalized, normalized)
        return normalized if normalized in {"ad_hoc", "emerging", "repeatable", "managed", "optimized"} else "repeatable"

    def _route_from_generation(self, *, section_name: str, generation) -> PanelSectionRoute:
        return PanelSectionRoute(
            section_name=section_name,
            provider_used=generation.provider_used,
            model_used=generation.model_used,
            local_llm_invoked=generation.local_llm_invoked,
            cloud_llm_invoked=generation.cloud_llm_invoked,
            llm_diagnostic_code=generation.llm_diagnostic_code,
            llm_diagnostic_detail=generation.llm_diagnostic_detail,
        )

    def _validation_fallback_route(
        self,
        *,
        section_name: str,
        generation,
        validation_detail: str,
    ) -> PanelSectionRoute:
        return PanelSectionRoute(
            section_name=section_name,
            provider_used="fallback-rule",
            model_used="rules-v1",
            local_llm_invoked=generation.local_llm_invoked,
            cloud_llm_invoked=generation.cloud_llm_invoked,
            llm_diagnostic_code=self._combine_diagnostic_code(
                generation.llm_diagnostic_code,
                "structured_response_validation_failed",
            ),
            llm_diagnostic_detail=self._combine_diagnostic_detail(
                generation.llm_diagnostic_detail,
                validation_detail,
            ),
        )

    def _summarize_panel_routes(
        self,
        *,
        panel_name: str,
        routes: list[PanelSectionRoute],
    ) -> dict[str, str | bool | None]:
        provider_used = "local"
        if any(route.provider_used == "fallback-rule" for route in routes):
            provider_used = "fallback-rule"
        elif any(route.provider_used == "cloud" for route in routes):
            provider_used = "cloud"

        concrete_models = {
            route.model_used
            for route in routes
            if route.model_used not in {"rules-v1", "section-assembled"}
        }
        if provider_used == "fallback-rule" and not concrete_models:
            model_used = "rules-v1"
        elif len(concrete_models) == 1 and len({route.provider_used for route in routes}) == 1:
            model_used = next(iter(concrete_models))
        else:
            model_used = "section-assembled"

        route_notes = []
        for route in routes:
            note = f"{route.section_name}={route.provider_used}"
            if route.llm_diagnostic_detail:
                note = f"{note} ({route.llm_diagnostic_detail})"
            route_notes.append(note)

        return {
            "provider_used": provider_used,
            "model_used": model_used,
            "local_llm_invoked": any(route.local_llm_invoked for route in routes),
            "cloud_llm_invoked": any(route.cloud_llm_invoked for route in routes),
            "llm_diagnostic_code": self._combine_diagnostic_code(
                *[route.llm_diagnostic_code for route in routes]
            ),
            "llm_diagnostic_detail": (
                f"{panel_name} was assembled from {len(routes)} smaller section calls. "
                f"Section routes: {'; '.join(route_notes)}."
            ),
        }

    def _build_fallback_panel(self, agent: AgentContract) -> ChiefAIPanelResponse:
        strategy_output = ChiefAIDigitalStrategyOutput(
            mission_assessment=MissionAssessment(
                mission_id="internal-ai-panel-posture",
                consulting_motion="mixed",
                title="Internal AI strategy operating posture",
                summary="The Chief AI panel summarizes offer design, productization, and delivery-shaping opportunities.",
                client_need="Internal visibility over AI advisory packaging and strategic direction.",
                success_definition="Operators can turn AI strategy thinking into clearer consulting offers and delivery motions.",
                why_now="This panel is still an internal advisory surface rather than a client mission output.",
            ),
            opportunity_map=[
                OpportunityMapItem(
                    opportunity_id="opp-agent-ops",
                    title="Productize the agentic operating model as an advisory offer",
                    problem_statement=(
                        "The repo now contains a strong operating model, but customer-facing packaging "
                        "for AI operating-system advisory work is still emerging."
                    ),
                    expected_value="Creates a repeatable high-trust AI strategy offer anchored in real platform practice.",
                    priority="now",
                    dependencies=["CTO/CIO panel", "Finance cockpit", "proposal/SOW packaging"],
                ),
                OpportunityMapItem(
                    opportunity_id="opp-delivery-copilot",
                    title="Package AI-assisted delivery governance and documentation support",
                    problem_statement=(
                        "PMO, BA, architect, QA, and documentation families are reusable, but the offer mix "
                        "still needs sharper AI-service framing."
                    ),
                    expected_value="Turns internal delivery leverage into client-visible value with better margins.",
                    priority="next",
                    dependencies=["delivery templates", "reporting surfaces", "client-safe prompt assets"],
                ),
                OpportunityMapItem(
                    opportunity_id="opp-knowledge-rag",
                    title="Offer AI knowledge assistant and document operations services",
                    problem_statement=(
                        "Knowledge and document families are strong candidates for productized client services, "
                        "but need clearer packaging and maturity signaling."
                    ),
                    expected_value="Extends the firm toward AI-enabled managed services with reusable assets.",
                    priority="next",
                    dependencies=["knowledge workflow polish", "document intake coverage", "client deployment template"],
                ),
            ],
            delivery_blueprint=[
                DeliveryBlueprintPhase(
                    phase_id="phase-discovery",
                    title="Discovery and opportunity shaping",
                    objectives=[
                        "Map business pain points, process friction, and available data assets",
                        "Identify the smallest useful AI or automation outcome worth piloting",
                    ],
                    deliverables=[
                        "opportunity portfolio",
                        "prioritized use-case shortlist",
                        "delivery assumptions and constraints",
                    ],
                    risks=[
                        "AI ambition may outrun data/process readiness",
                    ],
                ),
                DeliveryBlueprintPhase(
                    phase_id="phase-foundation",
                    title="Foundation and control setup",
                    objectives=[
                        "Define architecture, controls, and approval boundaries before scaling automation",
                        "Prepare prompt, tool, and observability conventions for safe execution",
                    ],
                    deliverables=[
                        "target operating model",
                        "tool and prompt control profile",
                        "delivery guardrails",
                    ],
                    risks=[
                        "Skipping controls early creates hidden operational risk later",
                    ],
                ),
                DeliveryBlueprintPhase(
                    phase_id="phase-pilot",
                    title="Pilot and measured rollout",
                    objectives=[
                        "Launch a bounded AI-enabled workflow or assistant with clear success metrics",
                        "Capture lessons learned before wider rollout or productization",
                    ],
                    deliverables=[
                        "pilot implementation slice",
                        "operator playbook",
                        "scale-or-stop recommendation",
                    ],
                    risks=[
                        "Weak success criteria can make a pilot look better than it really is",
                    ],
                ),
            ],
            maturity_model=[
                MaturityDimension(
                    dimension="Operating model",
                    current_level="repeatable",
                    target_level="managed",
                    gap_summary="The agent operating model is strong, but specialist AI strategy surfacing is only now landing in Mission Control.",
                    next_actions=[
                        "Finish specialist advisory surfaces",
                        "Connect advisory outputs to repeatable commercial packaging",
                    ],
                ),
                MaturityDimension(
                    dimension="Prompt and control layer",
                    current_level="repeatable",
                    target_level="managed",
                    gap_summary="Prompt composition and tool/state controls are formalized, but broad evaluation and version governance remain future work.",
                    next_actions=[
                        "Add prompt/version governance processes",
                        "Expand audit and evaluation coverage before deeper automation",
                    ],
                ),
                MaturityDimension(
                    dimension="Delivery productization",
                    current_level="emerging",
                    target_level="repeatable",
                    gap_summary="Reusable agent families are defined, but client-facing AI service packages still need stronger templates and delivery evidence.",
                    next_actions=[
                        "Package a few repeatable AI-assisted offers",
                        "Tie opportunity maps to proposal and reporting assets",
                    ],
                ),
            ],
            executive_summary=(
                "The platform is now strong enough to support credible AI strategy guidance, but the next gain comes from "
                "turning reusable internal capabilities into clearer productized offers with visible control and maturity signals."
            ),
            approval_required=True,
        )

        scope_signals = [
            ChiefAIScopeSignal(
                signal_id="signal-reuse",
                title="Reusable delivery families create real AI-service leverage",
                summary=(
                    "The repo now has a documented and runtime-aware family/mode/instance model, which is a strong base "
                    "for packaging AI-enabled services without mixing internal and client state."
                ),
                focus_area="offer_design",
                tone="success",
            ),
            ChiefAIScopeSignal(
                signal_id="signal-controls",
                title="Control foundations are in place before broader AI autonomy",
                summary=(
                    "Events, state, tools, autonomy, and prompt-layer conventions are now explicit, which makes AI strategy "
                    "recommendations more credible and safer to operationalize."
                ),
                focus_area="delivery_controls",
                tone="success",
            ),
            ChiefAIScopeSignal(
                signal_id="signal-productization",
                title="Productization is the next commercial bottleneck",
                summary=(
                    "The operating model is stronger than the current offer packaging, so the next value comes from turning "
                    "capabilities into repeatable client-facing AI and automation services."
                ),
                focus_area="commercialization",
                tone="warning",
            ),
        ]

        return ChiefAIPanelResponse(
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
            executive_summary=strategy_output.executive_summary,
            scope_signals=scope_signals,
            opportunity_map=strategy_output.opportunity_map,
            delivery_blueprint=strategy_output.delivery_blueprint,
            maturity_model=strategy_output.maturity_model,
            approval_required=strategy_output.approval_required,
        )

    def analyze_client_context(
        self,
        *,
        agent: AgentContract,
        payload: ChiefAIDigitalStrategyInput,
    ) -> ChiefAIAnalysisResponse:
        combined_text = self._combine_text(payload)
        fallback_output = self._build_fallback_output(payload, combined_text)
        prompt = self.prompt_loader.render_composition(
            "specialist-advisory.chief-ai-analyze",
            template_context={
                "engagement_name": payload.engagement_name,
                "problem_statement": payload.problem_statement,
                "business_context": payload.business_context,
                "client_context": payload.client_context or "none",
                "engagement_history": self._format_list(payload.engagement_history),
                "process_areas": self._format_list(payload.process_areas),
                "data_assets": self._format_list(payload.data_assets),
                "current_stack": self._format_list(payload.current_stack),
                "delivery_constraints": self._format_list(payload.delivery_constraints),
                "desired_outcomes": self._format_list(payload.desired_outcomes),
            },
            injected_context={
                "approval_policy": (
                    "Advisory output only. No delivery commitment, spend commitment, or client promise is final "
                    "without explicit CEO review and approval."
                ),
                "autonomy_policy": (
                    "Use LLM reasoning for consulting judgment, but stay within bounded AI advisory guidance. "
                    "Do not invent capabilities, approvals, budgets, or implementation facts."
                ),
                "tool_profile": "specialist-advisory profile; client brief interpretation only in this endpoint.",
                "state_summary": (
                    "Client-scoped advisory instance. Track A and Track B context must stay isolated. "
                    "Use only the supplied brief plus injected runtime policy."
                ),
                "output_schema": (
                    '{"executive_summary":"string","mission_assessment":{"mission_id":"string","consulting_motion":"problem_solving|opportunity_discovery|account_growth|mixed","title":"string","summary":"string","client_need":"string","success_definition":"string","why_now":"string"},'
                    '"context_signals":[{"signal_id":"string","category":"problem|history|constraint|readiness|risk|opportunity","title":"string","summary":"string","implication":"string"}],'
                    '"recommended_services":[{"service_id":"string","name":"string","summary":"string","fit_reason":"string","suggested_outcomes":["string"],"delivery_mode":"client_delivery|client_facing_service","priority":"now|next|later"}],'
                    '"upsell_opportunities":[{"opportunity_id":"string","title":"string","summary":"string","rationale":"string","suggested_service":"string","expansion_trigger":"string","priority":"now|next|later"}],'
                    '"opportunity_map":[{"opportunity_id":"string","title":"string","problem_statement":"string","expected_value":"string","priority":"now|next|later","dependencies":["string"]}],'
                    '"delivery_blueprint":[{"phase_id":"string","title":"string","objectives":["string"],"deliverables":["string"],"risks":["string"]}],'
                    '"maturity_model":[{"dimension":"string","current_level":"ad_hoc|emerging|repeatable|managed|optimized","target_level":"ad_hoc|emerging|repeatable|managed|optimized","gap_summary":"string","next_actions":["string"]}],"approval_required":true}'
                ),
            },
        )
        generation = self.model_gateway.generate_structured_json(
            prompt=prompt,
            fallback_payload=fallback_output.model_dump(),
        )
        response_provider_used = generation.provider_used
        response_model_used = generation.model_used
        response_diagnostic_code = generation.llm_diagnostic_code
        response_diagnostic_detail = generation.llm_diagnostic_detail
        try:
            strategy_output = ChiefAIDigitalStrategyOutput.model_validate(generation.content)
        except Exception:
            strategy_output = fallback_output
            response_provider_used = "fallback-rule"
            response_model_used = "rules-v1"
            response_diagnostic_code = self._combine_diagnostic_code(
                generation.llm_diagnostic_code,
                "structured_response_validation_failed",
            )
            response_diagnostic_detail = self._combine_diagnostic_detail(
                generation.llm_diagnostic_detail,
                "The structured Chief AI analysis response did not match the expected schema, so the rule-based advisory output was returned.",
            )

        return ChiefAIAnalysisResponse(
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
            executive_summary=strategy_output.executive_summary,
            mission_assessment=strategy_output.mission_assessment,
            context_signals=strategy_output.context_signals,
            recommended_services=strategy_output.recommended_services,
            upsell_opportunities=strategy_output.upsell_opportunities,
            opportunity_map=strategy_output.opportunity_map,
            delivery_blueprint=strategy_output.delivery_blueprint,
            maturity_model=strategy_output.maturity_model,
            approval_required=strategy_output.approval_required,
        )

    def _build_fallback_output(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> ChiefAIDigitalStrategyOutput:
        return ChiefAIDigitalStrategyOutput(
            mission_assessment=self._build_mission_assessment(payload, combined_text),
            context_signals=self._build_context_signals(payload, combined_text),
            recommended_services=self._build_recommended_services(payload, combined_text),
            upsell_opportunities=self._build_upsell_opportunities(payload, combined_text),
            opportunity_map=self._build_opportunity_map(payload, combined_text),
            delivery_blueprint=self._build_delivery_blueprint(payload, combined_text),
            maturity_model=self._build_maturity_model(payload, combined_text),
            executive_summary=(
                f"{payload.engagement_name} should be handled like a consulting account: solve the active AI mission, "
                "ground the recommendation in real context and history, and identify adjacent AI or data opportunities "
                "that can expand the relationship responsibly."
            ),
            approval_required=True,
        )

    def _combine_text(self, payload: ChiefAIDigitalStrategyInput) -> str:
        return " ".join(
            [
                payload.problem_statement,
                payload.business_context,
                payload.client_context,
                " ".join(payload.engagement_history),
                " ".join(payload.process_areas),
                " ".join(payload.data_assets),
                " ".join(payload.current_stack),
                " ".join(payload.delivery_constraints),
                " ".join(payload.desired_outcomes),
            ]
        ).lower()

    def _build_context_signals(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[ContextSignal]:
        signals = [
            ContextSignal(
                signal_id="client-problem",
                category="problem",
                title="Problem statement should drive AI scope",
                summary=payload.problem_statement,
                implication=(
                    "The AI strategy should stay anchored to the business problem and avoid generic tool-led recommendations."
                ),
            )
        ]

        if payload.engagement_history:
            signals.append(
                ContextSignal(
                    signal_id="engagement-history",
                    category="history",
                    title="Client history matters for advisory fit",
                    summary=" | ".join(payload.engagement_history[:3]),
                    implication=(
                        "Past attempts, constraints, or stakeholder feedback should shape the recommendation."
                    ),
                )
            )

        if payload.delivery_constraints:
            signals.append(
                ContextSignal(
                    signal_id="delivery-constraints",
                    category="constraint",
                    title="Delivery constraints limit the first AI move",
                    summary=", ".join(payload.delivery_constraints[:4]),
                    implication=(
                        "The first service should be sized to fit governance, budget, timing, and change capacity."
                    ),
                )
            )

        if self._contains_any(
            combined_text,
            "manual",
            "repetitive",
            "copy",
            "email",
            "intake",
            "triage",
            "backlog",
        ):
            signals.append(
                ContextSignal(
                    signal_id="workflow-friction",
                    category="opportunity",
                    title="Manual workflow friction is a strong AI candidate",
                    summary=(
                        "The brief highlights repetitive work, which is usually a better early AI target than a broad transformation program."
                    ),
                    implication=(
                        "Recommend a bounded workflow pilot with clear operator review and success metrics."
                    ),
                )
            )

        if self._contains_any(
            combined_text,
            "document",
            "knowledge",
            "search",
            "support",
            "policy",
            "faq",
        ):
            signals.append(
                ContextSignal(
                    signal_id="knowledge-gap",
                    category="opportunity",
                    title="Knowledge access appears to be a reusable use-case",
                    summary=(
                        "The client context points to people losing time finding or interpreting information."
                    ),
                    implication=(
                        "A knowledge assistant or document-operations service may be a higher-confidence offer than a custom model build."
                    ),
                )
            )

        if self._contains_any(
            combined_text,
            "governance",
            "compliance",
            "security",
            "approval",
            "privacy",
            "risk",
        ):
            signals.append(
                ContextSignal(
                    signal_id="governance-readiness",
                    category="risk",
                    title="AI governance needs to be part of the offer",
                    summary=(
                        "The client context includes explicit risk, approval, or compliance signals."
                    ),
                    implication=(
                        "Pair AI opportunity work with policy, review, and operating-boundary guidance."
                    ),
                )
            )

        return signals[:5]

    def _build_mission_assessment(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> MissionAssessment:
        consulting_motion = "problem_solving"
        if self._contains_any(
            combined_text,
            "portfolio",
            "roadmap",
            "opportunity",
            "growth",
            "scale",
            "productize",
        ):
            consulting_motion = "mixed"

        return MissionAssessment(
            mission_id="chief-ai-client-mission",
            consulting_motion=consulting_motion,
            title=f"AI consulting mission for {payload.engagement_name}",
            summary=(
                "Frame the immediate AI or digital problem like a consultant on the account, then connect it "
                "to the strongest next service and a few high-fit expansion paths."
            ),
            client_need=payload.problem_statement,
            success_definition=(
                "The client gets a practical AI mission, a realistic first engagement, and a shortlist of "
                "follow-on opportunities that make commercial sense."
            ),
            why_now=(
                "The brief already contains enough business and delivery context to recommend both a first move "
                "and adjacent consulting opportunities."
            ),
        )

    def _build_recommended_services(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[RecommendedService]:
        recommendations: list[RecommendedService] = [
            RecommendedService(
                service_id="ai-opportunity-assessment",
                name="AI Opportunity Assessment",
                summary="Translate the problem statement, process context, and delivery constraints into a ranked AI use-case portfolio.",
                fit_reason=(
                    "This is the safest first move when a client needs advisory direction rather than an immediate build."
                ),
                suggested_outcomes=[
                    "prioritized use-case map",
                    "business case hypotheses",
                    "pilot recommendation",
                ],
                delivery_mode="client_facing_service",
                priority="now",
            )
        ]

        if self._contains_any(
            combined_text,
            "document",
            "knowledge",
            "search",
            "support",
            "faq",
            "policy",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="knowledge-assistant-pilot",
                    name="Knowledge Assistant Pilot",
                    summary="Design a grounded assistant for internal documents, support knowledge, or policy retrieval.",
                    fit_reason=(
                        "The problem statement suggests information friction that is a strong fit for retrieval-backed assistance."
                    ),
                    suggested_outcomes=[
                        "use-case scope",
                        "retrieval and guardrail design",
                        "pilot evaluation plan",
                    ],
                    delivery_mode="client_delivery",
                    priority="now",
                )
            )

        if self._contains_any(
            combined_text,
            "manual",
            "repetitive",
            "email",
            "intake",
            "triage",
            "workflow",
            "backlog",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="workflow-automation-pilot",
                    name="AI Workflow Automation Pilot",
                    summary="Pilot a bounded workflow copilot or agent around a repetitive business process with human review.",
                    fit_reason=(
                        "Manual process friction is one of the clearest early wins for practical AI consulting work."
                    ),
                    suggested_outcomes=[
                        "pilot workflow design",
                        "operator approval points",
                        "success and rollback metrics",
                    ],
                    delivery_mode="client_delivery",
                    priority="now",
                )
            )

        if len(payload.data_assets) < 2 or self._contains_any(
            combined_text,
            "fragmented",
            "quality",
            "spreadsheet",
            "silo",
            "missing data",
            "inconsistent",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="data-readiness-sprint",
                    name="Data Readiness Sprint",
                    summary="Assess data availability, ownership, and quality before committing to a heavier AI roadmap.",
                    fit_reason=(
                        "The available context suggests data readiness could limit value unless addressed early."
                    ),
                    suggested_outcomes=[
                        "data asset inventory",
                        "readiness risks",
                        "minimum viable data plan",
                    ],
                    delivery_mode="client_facing_service",
                    priority="next",
                )
            )

        if self._contains_any(
            combined_text,
            "governance",
            "compliance",
            "security",
            "approval",
            "privacy",
            "risk",
        ):
            recommendations.append(
                RecommendedService(
                    service_id="ai-governance-setup",
                    name="AI Governance and Adoption Setup",
                    summary="Define review boundaries, usage policy, and operating controls for the proposed AI services.",
                    fit_reason=(
                        "The client context already signals that risk and adoption controls will shape what can be deployed."
                    ),
                    suggested_outcomes=[
                        "governance starter pack",
                        "human review policy",
                        "risk and escalation model",
                    ],
                    delivery_mode="client_facing_service",
                    priority="next",
                )
            )

        return recommendations[:5]

    def _build_upsell_opportunities(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[UpsellOpportunity]:
        opportunities: list[UpsellOpportunity] = []

        if self._contains_any(combined_text, "document", "knowledge", "policy", "support", "faq", "search"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-knowledge-ops",
                    title="Extend the mission into knowledge operations and grounded assistants",
                    summary="The current problem may open a broader document and knowledge-services engagement.",
                    rationale=(
                        "Information friction often leads naturally from one pilot into retrieval, document operations, "
                        "and support-enablement work."
                    ),
                    suggested_service="Knowledge Assistant Pilot",
                    expansion_trigger="The client already struggles with knowledge access or policy interpretation.",
                    priority="now",
                )
            )

        if self._contains_any(combined_text, "manual", "workflow", "triage", "email", "intake", "repetitive"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-workflow-suite",
                    title="Grow from one AI pilot into a broader workflow automation roadmap",
                    summary="A single manual-process pilot can often expand into a portfolio of supervised automations.",
                    rationale=(
                        "Clients rarely have only one repetitive workflow, so a successful pilot can become a larger consulting program."
                    ),
                    suggested_service="AI Workflow Automation Pilot",
                    expansion_trigger="The brief already shows recurring process friction beyond a single task.",
                    priority="now",
                )
            )

        if len(payload.data_assets) < 2 or self._contains_any(combined_text, "quality", "fragmented", "silo", "spreadsheet"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-data-foundation",
                    title="Add a follow-on data foundation engagement",
                    summary="Weak data readiness creates a natural next consulting motion after the first AI assessment.",
                    rationale=(
                        "Many AI missions stall on data quality, ownership, or structure, which creates demand for a practical data-readiness sprint."
                    ),
                    suggested_service="Data Readiness Sprint",
                    expansion_trigger="The brief shows limited or inconsistent data foundations.",
                    priority="next",
                )
            )

        if self._contains_any(combined_text, "governance", "compliance", "security", "approval", "privacy", "risk"):
            opportunities.append(
                UpsellOpportunity(
                    opportunity_id="expand-ai-governance",
                    title="Turn the pilot into a wider AI governance and adoption program",
                    summary="Risk and control concerns create room for a broader governance and enablement engagement.",
                    rationale=(
                        "Clients often need policy, operating guardrails, and adoption support once AI use cases start gaining traction."
                    ),
                    suggested_service="AI Governance and Adoption Setup",
                    expansion_trigger="The current mission already includes review, compliance, or risk signals.",
                    priority="next",
                )
            )

        return opportunities[:4]

    def _build_opportunity_map(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[OpportunityMapItem]:
        opportunities = [
            OpportunityMapItem(
                opportunity_id="opp-primary",
                title=f"Address {payload.engagement_name}'s core problem with a bounded AI advisory brief",
                problem_statement=payload.problem_statement,
                expected_value="Turns a broad AI conversation into a specific shortlist of realistic interventions.",
                priority="now",
                dependencies=["stakeholder alignment", "success criteria"],
            )
        ]

        if self._contains_any(combined_text, "document", "knowledge", "support", "faq", "policy"):
            opportunities.append(
                OpportunityMapItem(
                    opportunity_id="opp-knowledge",
                    title="Improve knowledge access and document response quality",
                    problem_statement=(
                        "Teams appear to be losing time finding or reusing information across documents or support knowledge."
                    ),
                    expected_value="Reduces search friction while keeping answers grounded in approved sources.",
                    priority="now",
                    dependencies=["content inventory", "retrieval guardrails"],
                )
            )

        if self._contains_any(combined_text, "manual", "repetitive", "triage", "intake", "email", "workflow"):
            opportunities.append(
                OpportunityMapItem(
                    opportunity_id="opp-automation",
                    title="Automate high-volume manual workflow steps with approval gates",
                    problem_statement=(
                        "The client context suggests repetitive process load that could be reduced with a supervised workflow copilot."
                    ),
                    expected_value="Creates measurable time savings without removing human control from sensitive decisions.",
                    priority="next",
                    dependencies=["workflow mapping", "operator review points"],
                )
            )

        if len(payload.data_assets) < 2 or self._contains_any(combined_text, "quality", "fragmented", "silo", "spreadsheet"):
            opportunities.append(
                OpportunityMapItem(
                    opportunity_id="opp-data-foundation",
                    title="Strengthen the data foundation before broader AI rollout",
                    problem_statement=(
                        "AI value may be capped by weak data availability, ownership, or consistency."
                    ),
                    expected_value="Prevents low-trust pilots and gives the client a credible path to scale later.",
                    priority="next",
                    dependencies=["data ownership", "minimum dataset definition"],
                )
            )

        return opportunities[:3]

    def _build_delivery_blueprint(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[DeliveryBlueprintPhase]:
        phase_one_deliverables = [
            "problem framing pack",
            "use-case shortlist",
            "constraints and guardrails",
        ]
        if payload.engagement_history:
            phase_one_deliverables.append("history-informed lessons learned")

        foundation_objectives = [
            "Confirm data, tooling, and review boundaries before implementation",
            "Define evaluation criteria and operator ownership",
        ]
        if self._contains_any(combined_text, "governance", "compliance", "security", "privacy", "approval"):
            foundation_objectives.append("Document approval, policy, and evidence expectations early")

        return [
            DeliveryBlueprintPhase(
                phase_id="phase-discovery",
                title="Client context and use-case framing",
                objectives=[
                    "Turn the problem statement and history into a small set of decision-ready use cases",
                    "Separate attractive ideas from feasible first moves",
                ],
                deliverables=phase_one_deliverables,
                risks=["Discovery can become too broad if the initial pilot boundary is not enforced."],
            ),
            DeliveryBlueprintPhase(
                phase_id="phase-foundation",
                title="Data, controls, and pilot design",
                objectives=foundation_objectives,
                deliverables=[
                    "data and tool readiness view",
                    "pilot architecture",
                    "governance and review setup",
                ],
                risks=["Weak controls or weak data can both undermine confidence in the pilot."],
            ),
            DeliveryBlueprintPhase(
                phase_id="phase-pilot",
                title="Bounded pilot and adoption decision",
                objectives=[
                    "Launch one supervised AI workflow or assistant tied to the stated problem",
                    "Measure whether the pilot deserves rollout, redesign, or stop",
                ],
                deliverables=[
                    "pilot implementation slice",
                    "operator playbook",
                    "scale, iterate, or stop recommendation",
                ],
                risks=["A pilot without clear success criteria can create false confidence."],
            ),
        ]

    def _build_maturity_model(
        self,
        payload: ChiefAIDigitalStrategyInput,
        combined_text: str,
    ) -> list[MaturityDimension]:
        data_level = "repeatable" if len(payload.data_assets) >= 2 else "emerging"
        governance_level = (
            "emerging"
            if self._contains_any(combined_text, "governance", "compliance", "security", "approval", "privacy", "risk")
            else "repeatable"
        )
        process_level = "repeatable" if len(payload.process_areas) >= 2 else "emerging"

        return [
            MaturityDimension(
                dimension="Use-case shaping",
                current_level="repeatable",
                target_level="managed",
                gap_summary=(
                    "The client has enough context to define practical AI use cases, but still needs prioritization discipline."
                ),
                next_actions=[
                    "Rank use cases by feasibility and business value",
                    "Lock the first pilot to one measurable workflow",
                ],
            ),
            MaturityDimension(
                dimension="Data readiness",
                current_level=data_level,
                target_level="managed",
                gap_summary=(
                    "Data readiness will need explicit attention before the client can scale beyond a narrow pilot."
                ),
                next_actions=[
                    "Clarify data ownership and availability",
                    "Define the minimum viable dataset for the first pilot",
                ],
            ),
            MaturityDimension(
                dimension="Governance and adoption",
                current_level=governance_level,
                target_level="managed",
                gap_summary=(
                    "Human review, policy, and adoption routines should be designed alongside the AI service, not after it."
                ),
                next_actions=[
                    "Set approval and escalation boundaries",
                    "Define operator training and review expectations",
                ],
            ),
            MaturityDimension(
                dimension="Process instrumentation",
                current_level=process_level,
                target_level="managed",
                gap_summary=(
                    "The best AI pilots depend on a clear understanding of the target workflow and how success will be measured."
                ),
                next_actions=[
                    "Map the target process baseline",
                    "Instrument time, quality, or throughput before the pilot starts",
                ],
            ),
        ]

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
            "The platform now supports workflow-first operations, prompt-layer contracts, client-facing advisory analysis, "
            "and reusable specialist families. The current internal AI strategy question is how to turn those capabilities "
            "into repeatable AI consulting offers, stronger delivery guidance, and visible maturity signals without "
            "compromising governance or overextending productization."
        )
