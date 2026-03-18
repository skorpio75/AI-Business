# Copyright (c) Dario Pizzolante
from app.models.agent_contract import AgentContract
from app.models.connectors import PersonalAssistantContext
from app.models.schemas import (
    ApprovalItem,
    DashboardKpi,
    DashboardSummaryResponse,
    PersonalAssistantBriefResponse,
    PersonalAssistantPriority,
    PersonalAssistantQuickAction,
    ScheduleConflict,
)


class DashboardSummaryService:
    def build_summary(
        self,
        *,
        agents: list[AgentContract],
        approvals: list[ApprovalItem],
        workflow_runs_count: int,
        personal_context: PersonalAssistantContext,
    ) -> DashboardSummaryResponse:
        blocked_agents = [agent for agent in agents if agent.runtime.status == "blocked"]
        waiting_agents = [agent for agent in agents if agent.runtime.status == "waiting"]
        delivery_agents = [agent for agent in agents if agent.domain == "delivery"]
        commercial_workload = sum(
            1 for approval in approvals if any(term in approval.subject.lower() for term in ("invoice", "quote", "proposal", "payment"))
        )
        kpis = [
            DashboardKpi(
                id="billing",
                label="Billing",
                value=str(commercial_workload),
                tone="warning" if commercial_workload else "neutral",
                context="commercial approvals in queue",
                footnote="Derived from pending approvals that look commercial.",
            ),
            DashboardKpi(
                id="cashflow",
                label="Cashflow",
                value="Watch" if len(approvals) >= 3 else "Stable",
                tone="warning" if len(approvals) >= 3 else "success",
                context=f"{len(approvals)} approvals pending",
                footnote="Finance workflows are not live yet, so this is an operational proxy.",
            ),
            DashboardKpi(
                id="delivery-health",
                label="Delivery Health",
                value=f"{max(len(delivery_agents) - len(blocked_agents), 0)}/{len(delivery_agents) or 1}",
                tone="critical" if blocked_agents else ("warning" if waiting_agents else "success"),
                context="delivery agents available vs blocked",
            ),
            DashboardKpi(
                id="quality-gate",
                label="Quality Gate",
                value="No failures" if not blocked_agents else "Attention",
                tone="critical" if blocked_agents else "success",
                context="based on current agent runtime state",
                footnote="Dedicated quality workflow metrics will improve this widget later.",
            ),
        ]

        priorities: list[PersonalAssistantPriority] = []
        if approvals:
            priorities.append(
                PersonalAssistantPriority(
                    title="Clear pending approvals",
                    reason=f"{len(approvals)} CEO decisions are waiting in the approval queue.",
                    urgency="high" if len(approvals) >= 3 else "medium",
                )
            )
        if workflow_runs_count:
            priorities.append(
                PersonalAssistantPriority(
                    title="Review latest workflow throughput",
                    reason=f"{workflow_runs_count} workflow runs are now visible in mission control.",
                    urgency="medium",
                )
            )
        if personal_context.inbox_health and personal_context.inbox_health.status != "ok":
            priorities.append(
                PersonalAssistantPriority(
                    title="Reconnect inbox integration",
                    reason=personal_context.inbox_health.detail or "Inbox connector is degraded.",
                    urgency="medium",
                )
            )
        if personal_context.calendar_health and personal_context.calendar_health.status != "ok":
            priorities.append(
                PersonalAssistantPriority(
                    title="Check calendar integration",
                    reason=personal_context.calendar_health.detail or "Calendar connector is degraded.",
                    urgency="low",
                )
            )
        if personal_context.tasks_health and personal_context.tasks_health.status != "ok":
            priorities.append(
                PersonalAssistantPriority(
                    title="Reconnect task integration",
                    reason=personal_context.tasks_health.detail or "Task connector is degraded.",
                    urgency="low",
                )
            )

        conflicts: list[ScheduleConflict] = []
        events = sorted(personal_context.calendar_events, key=lambda item: item.start_at)
        for previous, current in zip(events, events[1:]):
            if previous.end_at > current.start_at:
                conflicts.append(
                    ScheduleConflict(
                        title=f"Overlap: {previous.title} / {current.title}",
                        detail="Two calendar events overlap in the assistant window.",
                        severity="warning",
                    )
                )
        if personal_context.calendar_health and personal_context.calendar_health.status != "ok":
            conflicts.append(
                ScheduleConflict(
                    title="Calendar connector degraded",
                    detail=personal_context.calendar_health.detail or "Calendar integration is not configured.",
                    severity="info",
                )
            )

        quick_actions = [
            PersonalAssistantQuickAction(
                label="Open approvals",
                target_view="approval-queue",
                reason="CEO review work is best cleared first.",
            ),
            PersonalAssistantQuickAction(
                label="Run email workflow",
                target_view="email-operations",
                reason="Create and route a new draft reply when the inbox needs attention.",
            ),
            PersonalAssistantQuickAction(
                label="Check agents org",
                target_view="agents-org",
                reason="Review availability across corporate and delivery functions.",
            ),
        ]

        return DashboardSummaryResponse(
            kpis=kpis,
            personal_assistant=PersonalAssistantBriefResponse(
                priorities=priorities[:3],
                schedule_conflicts=conflicts[:3],
                quick_actions=quick_actions,
                inbox_status=personal_context.inbox_health.status if personal_context.inbox_health else "error",
                calendar_status=personal_context.calendar_health.status if personal_context.calendar_health else "error",
            ),
        )
