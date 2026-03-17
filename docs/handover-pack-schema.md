<!-- Copyright (c) Dario Pizzolante -->
# Handover Pack Schema

## Purpose
Define the promotion artifact that moves approved rehearsal output from Track A into Track B activation without sharing mutable runtime state.

## Core Rule
`handover_pack` is an explicit, approved artifact set.

- it is not a direct database copy
- it is not a live shared memory bridge
- it is the promotion contract between Track A and Track B

## Required Contents
- mission brief
- approved deliverables from SOW or internal scope
- approved consultant roster assumptions
- project-plan baseline
- RAID baseline
- acceptance-criteria summary
- quality-gate baseline
- starter context pack references
- assumptions, exclusions, and risks

## Backend Contracts and Tables

### `handover_packs`
Suggested columns:

- `handover_pack_id`
- `tenant_id`
- `source_lab_mission_id`
- `source_engagement_id` nullable
- `target_client_id`
- `target_engagement_id`
- `target_mission_name`
- `status`
- `mission_brief_ref`
- `approved_roster_ref`
- `project_plan_ref`
- `raid_log_ref`
- `quality_gate_plan_ref`
- `created_by`
- `created_at`
- `approved_at` nullable
- `readiness_status`

### `handover_pack_items`
Suggested columns:

- `item_id`
- `handover_pack_id`
- `item_type`
- `title`
- `storage_ref`
- `source_artifact_ref`
- `required_for_activation`
- `approval_status`
- `created_at`

### `readiness_gate_results`
Suggested columns:

- `readiness_gate_result_id`
- `handover_pack_id`
- `status`
- `review_summary`
- `reviewed_at`
- `reviewed_by_role`
- `blocking_reason` nullable
- `rubric_version`

### `readiness_gate_checks`
Suggested columns:

- `check_id`
- `readiness_gate_result_id`
- `checkpoint_id`
- `family_id`
- `outcome`
- `notes`
- `artifact_refs_json`

## Canonical Payload Shape

### `handover_pack`
```json
{
  "handover_pack_id": "hp-acme-discovery-001",
  "tenant_id": "internal",
  "source_lab_mission_id": "lab-acme-discovery-001",
  "target_client_id": "acme",
  "target_engagement_id": "acme-erp-modernization",
  "target_mission_name": "Discovery Mission",
  "status": "approved",
  "mission_brief_ref": "artifact://handover/hp-acme-discovery-001/mission-brief.md",
  "project_plan_ref": "artifact://handover/hp-acme-discovery-001/project-plan.md",
  "raid_log_ref": "artifact://handover/hp-acme-discovery-001/raid-log.md",
  "quality_gate_plan_ref": "artifact://handover/hp-acme-discovery-001/quality-gates.json",
  "approved_roster_ref": "artifact://handover/hp-acme-discovery-001/roster.json",
  "context_pack_refs": [
    "artifact://handover/hp-acme-discovery-001/context-pack/index.json"
  ],
  "assumptions": [
    "Client discovery workshops will occur weekly."
  ],
  "exclusions": [
    "Production rollout is out of scope for this mission."
  ]
}
```

## API Payloads

### `POST /lab-missions/{lab_mission_id}/handover-pack`
Request:

```json
{
  "target_client_id": "acme",
  "target_engagement_id": "acme-erp-modernization",
  "target_mission_name": "Discovery Mission",
  "artifact_refs": [
    "artifact://lab/lab-acme-discovery-001/project-plan.md",
    "artifact://lab/lab-acme-discovery-001/raid-log.md"
  ],
  "approved_roster_ref": "artifact://roster/acme-discovery-roster.json",
  "context_pack_refs": [
    "artifact://lab/lab-acme-discovery-001/context-pack/index.json"
  ]
}
```

### `POST /handover-packs/{handover_pack_id}/readiness-gate`
Request:

```json
{
  "rubric_id": "track-b-activation-readiness-v1",
  "required_families": [
    "pmo-project-control",
    "project-management-delivery-coordination",
    "qa-review",
    "documentation",
    "risk-watchdog"
  ]
}
```

Response:

```json
{
  "readiness_gate_result_id": "rg-001",
  "handover_pack_id": "hp-acme-discovery-001",
  "status": "ready",
  "checks": [
    {"family_id": "pmo-project-control", "outcome": "ready"},
    {"family_id": "qa-review", "outcome": "ready"}
  ]
}
```

### `POST /handover-packs/{handover_pack_id}/activate-track-b`
Request:

```json
{
  "target_tenant_id": "acme",
  "runtime_env_ref": "config/clients/acme.env",
  "activation_mode": "seed_and_start"
}
```

## Promotion Rules
- only approved artifacts should enter the handover pack
- readiness gate must be explicit
- Track B startup must reference the pack, not the original Track A live session
- Track B may copy or ingest the pack's approved artifact set into tenant-local storage

## Local Development Rule
The same handover model must work locally.

- Track A local lab missions can create handover packs
- local Track B seeded tenants can activate from those packs
- no separate cloud-only handover semantics should exist
