<!-- Copyright (c) Dario Pizzolante -->
# Audit Model

## Purpose
Define the canonical audit and execution-trace model for workflows, agents, approvals, tool usage, and outbound actions.

## Audit Rules
- Audit records are authoritative only when emitted through platform-controlled workflow, API, or policy paths.
- Audit data is tenant-scoped, track-scoped, and time-ordered.
- Sensitive actions must be traceable from trigger through approval, execution, and outcome.
- Audit detail is append-oriented: corrections should supersede prior records rather than silently rewriting history.
- External observability tools may mirror trace data, but this platform remains the system of record for auditability.

## Audit Objectives
The audit layer must let an operator answer:
- what happened
- who or what initiated it
- which workflow, run, step, or agent was involved
- which model route, tool, and approval path were used
- what changed as a result
- whether the action completed, failed, was rejected, or was escalated

## Core Audit Objects

### `agent_run`
Represents one bounded agent execution inside a workflow step, supervisor action, or later direct agent runtime surface.

#### Required fields
- `agent_run_id`
- `tenant_id`
- `track`
- `agent_id`
- `agent_family`
- `mode`
- `status`
- `started_at`

#### Optional fields
- `ended_at`
- `workflow_id`
- `run_id`
- `step_id`
- `parent_agent_run_id`
- `trigger_event_name`
- `input_ref`
- `output_ref`
- `autonomy_class`
- `approval_class`
- `provider_used`
- `model_used`
- `routing_path`
- `fallback_mode`
- `confidence`
- `trace_ref`
- `error_code`
- `error_detail`

#### Purpose
- summarize one agent execution window
- support persisted `agent_runs` history
- link higher-level workflow visibility to finer-grained execution history

### `audit_event`
Represents one append-oriented trace event for workflow progression, tool use, approval handling, routing, or external action.

#### Required fields
- `audit_event_id`
- `tenant_id`
- `track`
- `occurred_at`
- `event_name`
- `entity_type`
- `entity_id`
- `actor_type`
- `actor_id`
- `status`

#### Optional fields
- `workflow_id`
- `run_id`
- `step_id`
- `agent_run_id`
- `approval_id`
- `approval_class`
- `autonomy_class`
- `tool_id`
- `provider_used`
- `model_used`
- `routing_path`
- `fallback_mode`
- `trace_ref`
- `payload_ref_or_inline`
- `state_diff_ref`
- `error_code`
- `error_detail`

#### Purpose
- provide step-level traceability
- support persisted `audit_events` history
- create one normalized audit language across workflows, approvals, tools, and routing decisions

## Minimum Audit Envelope
Every persisted audit record should be linkable through this minimum envelope:
- `tenant_id`
- `track`
- `workflow_id` or `entity_type + entity_id`
- `run_id` where a workflow run exists
- `occurred_at`
- `actor_type`
- `actor_id`
- `status`

## Audit Event Families

### Workflow
- `workflow.run.started`
- `workflow.run.completed`
- `workflow.run.failed`
- `workflow.step.started`
- `workflow.step.completed`
- `workflow.step.failed`
- `workflow.step.escalated`

### Agent Execution
- `agent.run.started`
- `agent.run.completed`
- `agent.run.failed`
- `agent.run.handoff_requested`
- `agent.run.handoff_completed`

### Model and Routing
- `model.route.selected`
- `model.route.escalated`
- `model.route.fallback_applied`
- `model.output.validated`
- `model.output.validation_failed`

### Tools and Actions
- `tool.call.started`
- `tool.call.completed`
- `tool.call.failed`
- `outbound.action.requested`
- `outbound.action.executed`
- `outbound.action.blocked`

### Approval
- `approval.requested`
- `approval.reminded`
- `approval.decided`
- `approval.rejected`
- `approval.edited`
- `approval.expired`

### Connector and Runtime
- `connector.bootstrap.updated`
- `connector.refresh.failed`
- `runtime.config.loaded`
- `runtime.policy.blocked`

## Actor Model
Audit records must distinguish who or what acted.

### `actor_type` examples
- `human_operator`
- `workflow_system`
- `agent`
- `policy_layer`
- `connector`
- `external_runtime`

### `actor_id` examples
- operator username or approver role
- `Mission Control Agent`
- a workflow service name
- connector provider ID

## Linkage Rules
The audit model should join cleanly with the existing control models.

### Workflow and state linkage
- `run_state.run_id` is the primary workflow-level join key
- `approval_state.approval_id` is the primary approval-level join key
- `audit_ref` on `run_state` should point to the canonical audit aggregate for that run when persistence lands

### Event linkage
- `event_name` should align with the normalized event vocabulary in `EVENT_MODEL.md` where possible
- audit-only lifecycle detail may use the more specific audit event families defined here

### Tool linkage
- `tool_id` must use normalized tool IDs from `TOOLS.md`
- raw connector capability names should not be used as the canonical audit key

### Autonomy and approval linkage
- `autonomy_class` should align with `AUTONOMY_MODEL.md`
- `approval_class` should align with the normalized approval-class contract already used in workflow config and approval state

### Trace linkage
- `trace_ref` may point to Langfuse trace/span identifiers or later internal trace IDs
- external observability references support debugging, but they do not replace platform audit records

## Persistence Intent

### `agent_runs`
- persistence status: `implemented`
- intended role: summary table for per-agent execution history
- expected grain: one row per bounded agent execution
- likely joins: `workflow_runs`, `workflow_state_snapshots`, later `audit_events`

### `audit_events`
- persistence status: `implemented`
- intended role: append-oriented event table for fine-grained traceability
- expected grain: one row per auditable action, transition, tool call, routing choice, or approval event
- likely joins: `workflow_runs`, `approvals`, later `agent_runs`

## Mission Control Intent
Mission Control should expose audit views that let an operator inspect:
- source event and trigger path
- workflow and step progression
- agent execution history
- model/provider/routing decisions
- tool invocation history
- approval request and decision timeline
- outbound action outcomes

## MVP Boundary
This document defines the canonical audit model before full persistence and UI exposure exist.

Current reality:
- workflow runs and snapshots already provide partial traceability
- `agent_runs` now persist bounded execution history for the current workflow and specialist-analysis seams
- approvals already provide partial decision traceability
- `audit_events` now persist append-oriented workflow-step, model-route, tool-call, approval, and outbound-action history for the current implemented seams
- audit contracts now validate normalized trigger-event names, explicit audit-event-family names, normalized `tool_id` values, and governed approval/autonomy literals at the Pydantic contract layer
- aggregated API inspection endpoints now expose workflow, approval, and agent trace bundles over those persisted audit records
- Langfuse already provides optional workflow/model traces
- richer Mission Control audit presentation remains roadmap work

## Related Docs
- `STATE_MODEL.md`
- `EVENT_MODEL.md`
- `TOOLS.md`
- `AUTONOMY_MODEL.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `ROADMAP.md`
