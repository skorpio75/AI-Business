<!-- Copyright (c) Dario Pizzolante -->
# Agent Workbench UI Map

## Purpose
Define the Mission Control screens and frontend contracts required for ad hoc Track A agent invocation, delivery-lab work, handover promotion, and activation oversight while keeping the UI readable and dashboard-oriented.

## Design Rule
Do not turn Mission Control into a raw prompt console.

Each page should keep the existing readable pattern:
- hero header
- compact KPI strip
- one main list or work surface
- one detail/output surface
- strong status chips for approvals, readiness, and routing

## New Navigation Group
Recommended new top-level group:

- `Delivery Lab`

Recommended views:
- `agent-workbench`
- `lab-missions`
- `handover-packs`
- `activation-queue`

## Screen 1: Agent Workbench

### Goal
Let an operator invoke any family on demand for bounded internal work.

### Layout
- left rail: family picker and task-template picker
- center pane: brief and inputs form
- right pane: output preview, routing metadata, and save/promote actions

### Header
- eyebrow: `Delivery Lab`
- title: `Agent Workbench`
- copy: run delivery and specialist families on demand for internal planning, review, and rehearsal

### Inputs Contract
```ts
type AgentWorkbenchRequest = {
  familyId: string;
  mode: "internal_operating";
  scopeKind: "ad_hoc_session" | "saved_lab_mission" | "engagement_bound_run";
  scopeId?: string | null;
  taskTemplateId: string;
  title: string;
  goal: string;
  inputs: Record<string, unknown>;
  contextPackRefs: string[];
  outputSchemaId?: string | null;
};
```

### Output Contract
```ts
type AgentWorkbenchResult = {
  sessionId: string;
  runId: string;
  status: "queued" | "running" | "completed" | "failed";
  outputRef?: string | null;
  renderedOutput?: string | null;
  routing: {
    strategyUsed?: string | null;
    providerUsed: string;
    modelUsed: string;
    fallbackMode?: string | null;
  };
};
```

### Primary Actions
- `Run`
- `Save as Lab Mission`
- `Link to Engagement`
- `Promote to Handover`

## Screen 2: Lab Missions

### Goal
Provide the internal portfolio view over saved rehearsal and dogfooding missions.

### KPI Cards
- `active_lab_missions`
- `recent_runs`
- `ready_for_handover`
- `blocked_readiness_reviews`

### Table Columns
- `lab_mission_name`
- `status`
- `linked_engagement`
- `assigned_families`
- `recent_run_count`
- `handover_status`
- `last_activity_at`

### Detail Panel
- mission summary
- artifacts
- recent runs
- readiness posture
- linked handover packs

## Screen 3: Handover Packs

### Goal
Show all draft and approved promotion artifacts between Track A and Track B.

### KPI Cards
- `draft_handover_packs`
- `approved_handover_packs`
- `ready_for_activation`
- `blocked_handover_packs`

### Table Columns
- `handover_pack_id`
- `source_lab_mission`
- `target_client`
- `status`
- `readiness_status`
- `approved_roster_status`
- `last_updated_at`

### Detail Panel
- mission brief summary
- artifact checklist
- readiness checks
- activation status

## Screen 4: Activation Queue

### Goal
Give operators a readable queue of Track B activation progress and failures.

### KPI Cards
- `pending_activation_requests`
- `running_activations`
- `failed_activations`
- `completed_activations`

### Table Columns
- `activation_request_id`
- `target_tenant_id`
- `target_mission_name`
- `status`
- `current_step`
- `started_at`
- `completed_at`

### Detail Panel
- linked handover pack
- target runtime info
- step timeline
- failure details
- retry action

## API Client Contracts
Recommended frontend client methods:

- `invokeAgent(request)`
- `getAgentSession(sessionId)`
- `saveAgentSessionAsLabMission(sessionId, payload)`
- `listLabMissions(filters)`
- `getLabMission(labMissionId)`
- `createHandoverPack(labMissionId, payload)`
- `listHandoverPacks(filters)`
- `runReadinessGate(handoverPackId, payload)`
- `createActivationRequest(payload)`
- `listActivationRequests(filters)`

## Local Development Rule
These pages must be usable locally against a local API before cloud rollout.

- local frontend should point to local API through `VITE_API_BASE_URL`
- local Track A should support Workbench and Lab flows
- local seeded Track B tenants should support activation testing
