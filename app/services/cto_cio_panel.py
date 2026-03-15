from app.models.agent_contract import AgentContract
from app.models.schemas import CTOCIOPanelResponse, CTOCIOScopeInsight
from app.models.specialist_contracts import (
    ArchitectureAdvice,
    CTOCIOCounselOutput,
    ImprovementBacklogItem,
    StrategyOption,
)


class CTOCIOPanelService:
    def build_panel(self, *, agent: AgentContract) -> CTOCIOPanelResponse:
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
            scope_insights=scope_insights,
            strategy_options=counsel.strategy_options,
            architecture_advice=counsel.architecture_advice,
            internal_improvement_backlog=counsel.internal_improvement_backlog,
            approval_required=counsel.approval_required,
        )
