<!-- Copyright (c) Dario Pizzolante -->
# Delivery Lab Operating Model

## Purpose
Define how Track A can invoke delivery-family capabilities on demand for internal rehearsal, dogfooding, service design, and pre-delivery preparation before a real Track B client mission exists.

## Core Rule
Track A may use any delivery-capable family in `internal_operating` mode as long as the work remains bounded, auditable, and internal.

- ad hoc drafting, planning, review, synthesis, and artifact generation are allowed
- authoritative client delivery still begins only after Track B activation
- promotion into Track B happens through explicit artifacts, not shared mutable state

## Activation Shapes

### `ad_hoc_session`
Use when an operator wants to invoke a family immediately without first creating a lead, engagement, or mission.

Examples:
- "PM, generate a project plan for a CRM rollout"
- "QA, review this draft requirements pack"
- "Documentation, create a handover outline for an AI support pilot"

Characteristics:
- lightweight
- session-scoped
- may remain ephemeral
- can later be saved into a lab mission

### `saved_lab_mission`
Use when the internal work should become a durable rehearsal or dogfooding mission.

Examples:
- internal ERP discovery rehearsal
- productized PMO pack rehearsal
- AI strategy pilot runbook rehearsal

Characteristics:
- mission-scoped
- durable artifacts
- can have assigned families
- can produce a `handover_pack`

### `engagement_bound_run`
Use when the run belongs to a real internal opportunity or engagement in Track A, but Track B has not started yet.

Examples:
- BA drafting for an accepted discovery proposal
- Architect scoping for an engagement awaiting activation
- PM creating a draft delivery plan before client runtime startup

Characteristics:
- linked to `opportunity_id` or `engagement_id`
- stronger traceability and commercial linkage
- can also feed a `handover_pack`

## Recommended Lifecycle
1. operator launches an `ad_hoc_session`, `saved_lab_mission`, or `engagement_bound_run`
2. platform assembles the internal context pack
3. selected family runs in Track A `internal_operating`
4. output is returned and traced
5. operator optionally saves the work into `lab_mission`
6. approved artifacts can later promote into `handover_pack`

## Backend Contracts and Tables

### `agent_invoke_request`
Suggested fields:

- `request_id`
- `tenant_id`
- `family_id`
- `mode`
- `scope_kind`: `ad_hoc_session`, `saved_lab_mission`, `engagement_bound_run`
- `scope_id`
- `task_template_id`
- `goal`
- `input_payload_json`
- `context_pack_refs_json`
- `output_schema_id`
- `requested_by`
- `requested_at`

### `ad_hoc_sessions`
Suggested columns:

- `session_id`
- `tenant_id`
- `family_id`
- `mode`
- `title`
- `goal`
- `status`
- `task_template_id`
- `opportunity_id` nullable
- `engagement_id` nullable
- `created_by`
- `created_at`
- `last_activity_at`
- `latest_output_ref`

### `lab_missions`
Suggested columns:

- `lab_mission_id`
- `tenant_id`
- `title`
- `status`
- `goal`
- `mission_brief`
- `opportunity_id` nullable
- `engagement_id` nullable
- `source_session_id` nullable
- `owner_role`
- `created_at`
- `updated_at`
- `quality_gate_plan_ref` nullable
- `last_readiness_posture`

### `lab_mission_artifacts`
Suggested columns:

- `artifact_id`
- `lab_mission_id`
- `artifact_type`
- `title`
- `storage_ref`
- `version`
- `produced_by_family_id`
- `produced_by_agent_run_id`
- `approved_for_handover`
- `created_at`

### `agent_instances`
This table should support both Track A and Track B runtime identities.

Suggested columns:

- `instance_id`
- `family_id`
- `mode`
- `tenant_id`
- `client_id` nullable
- `engagement_id` nullable
- `mission_id` nullable
- `lab_mission_id` nullable
- `scope_kind`
- `tool_profile_id`
- `approval_policy_ref`
- `runtime_env_ref`
- `status`
- `created_at`
- `last_heartbeat_at`

### `agent_assignments`
Suggested columns:

- `assignment_id`
- `instance_id`
- `scope_kind`
- `scope_id`
- `workflow_id` nullable
- `run_id` nullable
- `assignment_role`
- `assigned_at`
- `released_at` nullable

## Recommended Extensions to Existing Tables

### `agent_runs`
Add optional linkage fields:

- `scope_kind`
- `scope_id`
- `lab_mission_id`
- `opportunity_id`
- `engagement_id`
- `handover_pack_id`

### `audit_events`
Add optional linkage fields:

- `scope_kind`
- `scope_id`
- `lab_mission_id`
- `handover_pack_id`

## API Payloads

### `POST /agents/invoke`
Request:

```json
{
  "family_id": "project-management-delivery-coordination",
  "mode": "internal_operating",
  "scope_kind": "ad_hoc_session",
  "scope_id": null,
  "task_template_id": "generate-project-plan",
  "title": "CRM rollout planning draft",
  "goal": "Draft a practical first-pass project plan for a CRM rollout.",
  "inputs": {
    "project_name": "CRM rollout",
    "deliverables": ["project plan", "milestones", "RAID log"],
    "constraints": ["12 weeks", "small team"]
  },
  "context_pack_refs": [],
  "output_schema_id": "project-plan-v1"
}
```

Response:

```json
{
  "session_id": "lab-session-001",
  "run_id": "run-001",
  "family_id": "project-management-delivery-coordination",
  "scope_kind": "ad_hoc_session",
  "status": "completed",
  "output_ref": "artifact://lab-session-001/project-plan-v1",
  "routing": {
    "provider_used": "local",
    "model_used": "ollama/qwen2.5:1.5b",
    "strategy_used": "local_first"
  }
}
```

### `POST /agent-sessions/{session_id}/save-as-lab-mission`
Request:

```json
{
  "title": "Internal CRM rollout rehearsal",
  "goal": "Rehearse the CRM rollout delivery motion before client activation.",
  "engagement_id": "eng-internal-crm-rollout",
  "artifact_refs": ["artifact://lab-session-001/project-plan-v1"]
}
```

### `GET /lab-missions/{lab_mission_id}`
Response should include:

- mission metadata
- assigned families
- artifacts
- recent runs
- readiness posture
- linked handover packs

## Local Development Rule
Everything in the delivery-lab model must work locally first.

- run the same repo locally
- use local PostgreSQL and local or desktop `Ollama`
- develop and test the API and UI locally
- commit and push to Git from local
- cloud instances should pull approved changes rather than being edited directly

This keeps local development and cloud deployment aligned instead of creating two different operating models.
