<!-- Copyright (c) Dario Pizzolante -->
# Track B Activation Runbook

## Purpose
Define the implementation and operator sequence for activating a Track B tenant runtime from an approved Track A handover pack.

## Scope
This runbook covers:

- preconditions in Track A
- activation request creation
- tenant bootstrap or reuse
- artifact ingestion into Track B
- initial roster instantiation
- local and cloud deployment behavior

## Preconditions
Before activation, all of the following should be true:

- `handover_pack` is approved
- `readiness_gate_result` is `ready`
- target tenant identity exists or has been approved for creation
- target runtime config path is known
- approved consultant roster exists
- starter context pack exists

## Backend Contracts and Tables

### `activation_requests`
Suggested columns:

- `activation_request_id`
- `handover_pack_id`
- `target_tenant_id`
- `target_client_id`
- `target_engagement_id`
- `target_mission_id`
- `runtime_env_ref`
- `activation_mode`
- `status`
- `created_by`
- `created_at`
- `started_at` nullable
- `completed_at` nullable
- `failure_reason` nullable

### `activation_steps`
Suggested columns:

- `step_id`
- `activation_request_id`
- `step_name`
- `status`
- `started_at`
- `completed_at` nullable
- `detail`

## Activation Flow
1. create `activation_request`
2. validate target tenant contract and env file
3. seed tenant if missing
4. ensure DB and storage are ready
5. ingest approved handover artifacts into tenant-local storage
6. instantiate approved consultant roster as Track B `client_delivery` instances
7. initialize Track B project state and quality gates
8. emit `mission.delivery.started`

## API Payloads

### `POST /activation-requests`
```json
{
  "handover_pack_id": "hp-acme-discovery-001",
  "target_tenant_id": "acme",
  "target_client_id": "acme",
  "target_engagement_id": "acme-erp-modernization",
  "target_mission_id": "acme-erp-discovery",
  "runtime_env_ref": "config/clients/acme.env",
  "activation_mode": "seed_and_start"
}
```

### `GET /activation-requests/{activation_request_id}`
Response should include:

- high-level status
- current step
- step timeline
- target tenant metadata
- linked handover pack
- linked Track B mission identifiers

## Local Activation Path
Local activation is required for developer rehearsal and testing.

Recommended local flow:
1. run Track A locally
2. create a `handover_pack`
3. seed a local Track B tenant env under `config/clients/`
4. activate Track B locally from the approved pack
5. smoke-test the tenant API and roster

This should reuse the same repo, same workflow logic, and same activation contract as production.

## Cloud Activation Path
Production cloud activation should follow the same contracts, but with separate deployed runtimes.

Recommended deployment rule:
- code is developed locally
- changes are committed and pushed to Git
- cloud hosts pull approved merged changes
- do not maintain cloud-only code paths

That keeps local and cloud behavior aligned and makes activation reproducible.

## Failure Handling
Typical failure states:

- `blocked_config`
- `blocked_storage`
- `blocked_database`
- `blocked_artifact_ingest`
- `blocked_roster_instantiation`

Recommended response:
- persist failure in `activation_steps`
- show status in Mission Control `Activation Queue`
- allow operator retry once the blocking issue is fixed
