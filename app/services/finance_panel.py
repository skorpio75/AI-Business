# Copyright (c) Dario Pizzolante
from app.models.agent_contract import AgentContract
from app.models.schemas import FinancePanelAgentSummary, FinancePanelResponse
from app.models.specialist_contracts import (
    AccountantContractOutput,
    CFOContractOutput,
    CloseChecklistItem,
    FinancialScenario,
    ReconciliationException,
    ReconciliationRule,
)


class FinancePanelService:
    def build_panel(
        self,
        *,
        accountant_agent: AgentContract,
        cfo_agent: AgentContract,
        finance_ops_agent: AgentContract,
    ) -> FinancePanelResponse:
        accountant_output = AccountantContractOutput(
            reconciliation_rules=[
                ReconciliationRule(
                    rule_id="rule-billing-evidence",
                    description="Every invoice draft should trace back to an approved milestone or delivery artifact.",
                    severity="blocking",
                ),
                ReconciliationRule(
                    rule_id="rule-receivable-followup",
                    description="Overdue receivables older than 14 days should be surfaced in the weekly finance pack.",
                    severity="warning",
                ),
            ],
            exceptions=[
                ReconciliationException(
                    exception_id="recon-margin-gap",
                    summary="Forecasted margin visibility is weaker than proposal and delivery visibility.",
                    impacted_records=["finance-review workflow", "company reporting pack"],
                    severity="material",
                    recommended_action=(
                        "Expose finance exceptions and forecast-vs-actual drift in the cockpit so weekly review can close the gap."
                    ),
                ),
                ReconciliationException(
                    exception_id="recon-ui-gap",
                    summary="Finance specialist outputs exist in contracts but are only partially surfaced in Mission Control.",
                    impacted_records=["accountant-agent", "cfo-agent", "finance-ops-agent"],
                    severity="warning",
                    recommended_action=(
                        "Complete the finance cockpit and then wire future finance workflows to richer live metrics."
                    ),
                ),
            ],
            close_checklist=[
                CloseChecklistItem(
                    item_id="close-reporting",
                    title="Prepare recurring finance cockpit pack",
                    owner="Finance Ops Agent",
                    status="in_progress",
                    notes="Panel is now live; richer live signals still need workflow-backed metrics.",
                ),
                CloseChecklistItem(
                    item_id="close-receivables",
                    title="Review receivables aging and reminder readiness",
                    owner="Accountant Agent",
                    status="pending",
                    notes="Invoice and receivables automation exists, but cockpit review should make exceptions clearer.",
                ),
                CloseChecklistItem(
                    item_id="close-scenarios",
                    title="Refresh CFO scenario deck for pricing and runway tradeoffs",
                    owner="CFO Agent",
                    status="pending",
                ),
            ],
            accounting_ready_exports=[
                "weekly-finance-pack",
                "receivables-aging-summary",
                "scenario-review-inputs",
            ],
        )

        cfo_output = CFOContractOutput(
            scenarios=[
                FinancialScenario(
                    scenario_id="scenario-utilization",
                    title="Protect margin by prioritizing repeatable advisory work",
                    horizon="90_days",
                    assumptions=[
                        "CTO/CIO and architecture work continue to convert into scoped delivery work",
                        "Operator time remains the main capacity constraint",
                    ],
                    projected_outcomes=[
                        "Higher-value work is easier to package and price",
                        "Less context switching across small custom tasks",
                    ],
                    risks=[
                        "Pipeline may narrow if packaged offers are not communicated clearly",
                        "Advisory work still depends on strong follow-on delivery positioning",
                    ],
                ),
                FinancialScenario(
                    scenario_id="scenario-cashflow",
                    title="Improve cash discipline through tighter milestone billing review",
                    horizon="30_days",
                    assumptions=[
                        "Billing triggers and receivables follow-up stay policy-bound",
                        "Mission Control surfaces exceptions before invoices age too far",
                    ],
                    projected_outcomes=[
                        "Lower receivables lag",
                        "Better visibility into near-term cash constraints",
                    ],
                    risks=[
                        "Without live finance workflow metrics, the cockpit is still partly proxy-based",
                    ],
                ),
                FinancialScenario(
                    scenario_id="scenario-platform-investment",
                    title="Invest in observability before deeper multi-agent finance automation",
                    horizon="12_months",
                    assumptions=[
                        "Audit and trace work remains ahead of broader autonomous execution",
                    ],
                    projected_outcomes=[
                        "Safer runtime expansion into finance-support workflows",
                        "Clearer decision history for future delegated approvals",
                    ],
                    risks=[
                        "UI and control work may slow near-term visible feature delivery",
                    ],
                ),
            ],
            cashflow_risks=[
                "Receivables visibility is improving, but still depends on partial proxy data rather than full live workflow metrics.",
                "Margin drift can hide inside delivery work unless finance review and reporting surfaces stay visible to the operator.",
            ],
            recommendations=[
                "Use the finance cockpit in weekly review to close the loop between approvals, billing, and delivery readiness.",
                "Prioritize finance exceptions that affect cash timing before expanding lower-signal admin automation.",
                "Treat live finance workflow metrics as the next maturity step after this cockpit layer.",
            ],
            executive_summary=(
                "Finance controls are now modeled and visible enough to support operator review, but richer live finance signals "
                "should come next before deeper finance-runtime automation."
            ),
            approval_required=True,
        )

        return FinancePanelResponse(
            agents=[
                self._agent_summary(accountant_agent),
                self._agent_summary(cfo_agent),
                self._agent_summary(finance_ops_agent),
            ],
            reconciliation_rules=accountant_output.reconciliation_rules,
            accounting_exceptions=accountant_output.exceptions,
            close_checklist=accountant_output.close_checklist,
            accounting_ready_exports=accountant_output.accounting_ready_exports,
            scenarios=cfo_output.scenarios,
            cashflow_risks=cfo_output.cashflow_risks,
            recommendations=cfo_output.recommendations,
            executive_summary=cfo_output.executive_summary,
            approval_required=cfo_output.approval_required,
        )

    def _agent_summary(self, agent: AgentContract) -> FinancePanelAgentSummary:
        return FinancePanelAgentSummary(
            agent_id=agent.agent_id,
            display_name=agent.display_name,
            role_summary=agent.role_summary,
            primary_track=agent.deployment.primary_track,
            operating_modes=agent.operating_modes,
            tool_profile_by_mode=agent.tool_profile_by_mode,
            approval_class=agent.approval_class,
            autonomy_class=agent.autonomy_class,
        )
