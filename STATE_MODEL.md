# State Model

## Purpose
Define the canonical operating state objects that workflows, agents, approvals, and Mission Control rely on.

## State Rules
- State is authoritative only when persisted through platform-controlled workflows or API paths.
- Each state object must declare ownership, writers, and consuming workflows.
- Track A and Track B state remain isolated by tenant and deployment boundary.

## `opportunity_state`

### Required fields
- `id`
- `tenant_id`
- `prospect_id`
- `owner_agent_or_role`
- `stage`
- `qualification_status`
- `service_type`
- `next_action`

### Optional fields
- `lead_score`
- `estimated_value`
- `urgency`
- `expected_close_date`
- `last_contact_at`
- `risks`
- `memory_refs`
- `source_refs`

### Ownership
- primary owner: Growth pod workflows
- steward: Lead Intake Agent or delegated commercial controller

### Typical writers
- Lead Intake Agent
- Account Research Agent
- Qualification Agent
- Proposal / SOW Agent

## `project_state`

### Required fields
- `id`
- `tenant_id`
- `client_id`
- `status`
- `project_manager`
- `current_phase`
- `risk_level`

### Optional fields
- `milestone_health`
- `budget_health`
- `overdue_actions_count`
- `next_steerco_date`
- `deliverables`
- `raid_log_ref`
- `acceptance_refs`
- `memory_refs`

### Ownership
- primary owner: Delivery pod workflows
- steward: PMO / Project Control Agent

### Typical writers
- PMO / Project Control Agent
- BA / Requirements Agent
- Architect Agent
- Build / Automation Agent
- QA / Review Agent
- Documentation Agent

## `run_state`

### Required fields
- `run_id`
- `tenant_id`
- `workflow_id`
- `agent_id`
- `status`
- `started_at`

### Optional fields
- `ended_at`
- `step_id`
- `event_source`
- `confidence`
- `routing_path`
- `fallback_mode`
- `tool_calls`
- `output_ref`
- `blocking_reason`
- `approval_class`
- `autonomy_class`
- `audit_ref`

### Ownership
- primary owner: workflow orchestration layer

## `approval_state`

### Required fields
- `approval_id`
- `tenant_id`
- `approval_class`
- `related_run_id`
- `requested_by_agent`
- `approver_role`
- `status`
- `requested_at`

### Optional fields
- `related_entity_type`
- `related_entity_id`
- `decided_at`
- `decision`
- `notes`
- `policy_ref`

### Ownership
- primary owner: policy and approval layer

## State Ownership Summary
- Growth pod primarily owns `opportunity_state`
- Delivery pod primarily owns `project_state`
- workflow orchestration owns `run_state`
- policy and approval controls own `approval_state`
