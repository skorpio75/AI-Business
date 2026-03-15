from app.models.agent_contract import AgentContract
from app.models.schemas import ChiefAIPanelResponse, ChiefAIScopeSignal
from app.models.specialist_contracts import (
    ChiefAIDigitalStrategyOutput,
    DeliveryBlueprintPhase,
    MaturityDimension,
    OpportunityMapItem,
)


class ChiefAIPanelService:
    def build_panel(self, *, agent: AgentContract) -> ChiefAIPanelResponse:
        strategy_output = ChiefAIDigitalStrategyOutput(
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
            executive_summary=strategy_output.executive_summary,
            scope_signals=scope_signals,
            opportunity_map=strategy_output.opportunity_map,
            delivery_blueprint=strategy_output.delivery_blueprint,
            maturity_model=strategy_output.maturity_model,
            approval_required=strategy_output.approval_required,
        )
