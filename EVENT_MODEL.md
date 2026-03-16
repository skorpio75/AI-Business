<!-- Copyright (c) Dario Pizzolante -->
# Event Model

## Purpose
Define the normalized event families and trigger patterns used across workflows, approvals, and Mission Control.

## Event Rules
- Events describe something that happened.
- Triggers start workflows in response to events, schedules, or operator actions.
- Event names use lowercase dotted identifiers.
- Events are tenant-scoped and track-scoped.

## Minimum Event Envelope
- `event_id`
- `event_name`
- `tenant_id`
- `track`
- `source`
- `occurred_at`
- `entity_type`
- `entity_id`
- `payload_ref_or_inline`

## Sales Events
- `lead.signal.detected`
- `lead.candidate.created`
- `lead.review.requested`
- `lead.materialized`
- `lead.received`
- `lead.enriched`
- `lead.qualified`
- `meeting.discovery.completed`
- `proposal.requested`
- `proposal.submitted`
- `deal.won`
- `deal.lost`
- `contract.signed`
- `dispatch.plan.proposed`
- `dispatch.plan.approved`
- `mission.approved`

## Delivery Events
- `project.created`
- `workshop.completed`
- `requirements.updated`
- `design.requested`
- `design.completed`
- `build.requested`
- `build.completed`
- `qa.failed`
- `qa.passed`
- `milestone.completed`
- `milestone.acceptance.requested`
- `milestone.accepted`
- `project.risk.detected`
- `mission.closeout.requested`
- `mission.closed`

## Operations Events
- `invoice.triggered`
- `invoice.sent`
- `invoice.overdue`
- `vendor.renewal_approaching`
- `month_end.started`
- `timesheet.missing`

## Executive Events
- `risk.alert`
- `approval.pending`
- `run.failed`
- `schedule.daily_brief`
- `schedule.weekly_review`
- `schedule.monthly_strategy`

## Knowledge Events
- `document.ingested`
- `meeting.summary.created`
- `project.closed`
- `lessons_learned.created`

## Trigger Patterns
- event triggers
- schedule triggers
- operator triggers
- approval-resolution triggers
