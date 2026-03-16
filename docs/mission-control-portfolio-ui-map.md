<!-- Copyright (c) Dario Pizzolante -->
# Mission Control Portfolio UI Map

## Purpose
Define the next operator-facing Mission Control surfaces for managing clients, engagements, missions, and mission-level delivery control in Track A.

This document turns the portfolio cockpit direction in the existing governance docs into a concrete frontend implementation map that can guide API design, TypeScript contracts, and React page construction without inventing a separate product model.

## Scope
This UI map covers the next portfolio-focused Mission Control screens:

- `Clients`
- `Engagements`
- `Missions`
- `Mission Detail`

It assumes the existing Mission Control shell, `shadcn/ui` + Tailwind component foundation, and the current page pattern of:

- hero header
- KPI strip
- list or table surface
- right-side or lower detail panel
- status pills and compact callouts for risk, approvals, and readiness

## Operating Fit
This UI map is grounded in the current operating model:

- `client -> engagement -> mission -> agent_instance`
- Track A Mission Control acts as the portfolio control tower
- Track B or tenant-scoped runtimes remain the source of mutable client-delivery state
- Track A consumes bounded portfolio summaries rather than shared tenant-local state

The screen set should feel like a CEO or operator supervising a fleet of consultant-agents across the portfolio rather than editing raw tenant-local delivery records directly.

## Navigation Placement
Mission Control should add a new top-level navigation group:

- `Portfolio`

Recommended views inside that group:

- `clients`
- `engagements`
- `missions`

`Mission Detail` should normally open from mission selection or deep-link routing rather than appearing as a permanent top-level navigation item.

## Proposed View Keys
Recommended additions to the frontend view-key set:

- `clients`
- `engagements`
- `missions`
- `mission-detail`

Recommended routing behavior:

- `mission-detail` should accept a selected `mission_id`
- the app can initially keep this as in-memory page state
- later it should move to URL-backed routing when broader Mission Control navigation matures

## Shared Portfolio Page Pattern
Each new portfolio page should follow a consistent structure:

### Header
- page eyebrow
- page title
- one-sentence operator-oriented description
- optional context breadcrumb when opened inside a client or engagement drill-down

### KPI Strip
- 3 to 6 compact KPI cards
- counts and health posture first
- avoid dense financial detail unless the page is specifically commercial

### Filters
- search input
- status filters
- risk filter
- approval-state filter where relevant
- client or engagement selectors on deeper views

### Main List Surface
- table on desktop
- stacked list cards on narrower widths
- one selected item at a time

### Detail Surface
- summary of selected row
- priority actions and health indicators
- linked objects and recent activity

## Screen 1: Clients

### Goal
Give the operator a portfolio-wide view of all client accounts and their current operating posture.

### Header
- eyebrow: `Portfolio`
- title: `Client Portfolio`
- copy: supervise active clients, delivery load, approvals, and risk across the portfolio

### KPI Cards
- `total_clients`
- `active_engagements`
- `active_missions`
- `pending_approvals`
- `escalated_missions`

### Filters
- search by client name or tenant
- client status
- risk level
- active-only toggle

### Main Table Columns
- `client_name`
- `tenant_id`
- `active_engagements`
- `active_missions`
- `agents_dispatched`
- `pending_approvals`
- `risk_level`
- `last_activity_at`
- `health_status`

### Detail Panel
- client identity block
- active engagements list
- mission count by status
- dispatched consultant count by family
- unresolved risk and escalation summary
- last activity feed

### Primary Actions
- `View engagements`
- `Open active missions`
- later: `Open dispatch plans`
- later: `Seed or inspect runtime`

## Screen 2: Engagements

### Goal
Show the commercial and operational containers that sit between clients and missions.

### Header
- breadcrumb example: `Clients / Acme / Engagements`
- title: `Engagements`
- copy: inspect signed scope, dispatch readiness, roster status, and mission progress

### KPI Cards
- `total_engagements`
- `active_engagements`
- `awaiting_dispatch_approval`
- `in_delivery`
- `nearing_closeout`

### Filters
- search by engagement or client
- client selector
- stage selector
- roster status selector
- billing method selector

### Main Table Columns
- `engagement_name`
- `client_name`
- `stage`
- `signed_scope_status`
- `missions_count`
- `approved_roster_status`
- `billing_method`
- `last_activity_at`

### Detail Panel
- engagement summary
- contract or SOW posture
- linked missions
- dispatch candidate plan summary
- approved consultant roster summary
- billing plan summary
- open approvals and escalations

### Primary Actions
- `View missions`
- `Open dispatch plan`
- `Open approved roster`
- later: `Start mission workflow`

## Screen 3: Missions

### Goal
Provide the operational fleet view over live and upcoming missions.

### Header
- eyebrow: `Portfolio`
- title: `Missions`
- copy: monitor mission phase, approvals, dispatched agents, and delivery readiness

### KPI Cards
- `active_missions`
- `blocked_missions`
- `pending_milestone_acceptance`
- `pending_approvals`
- `failing_quality_gates`

### Filters
- search by mission, client, or engagement
- client selector
- engagement selector
- mission status
- current phase
- risk level
- approval state
- quality-gate state
- dispatched family

### Main Table Columns
- `mission_name`
- `engagement_name`
- `client_name`
- `status`
- `current_phase`
- `agents_dispatched`
- `active_runs`
- `pending_approvals`
- `quality_gate_status`
- `risk_level`
- `last_activity_at`

### Detail Panel
- mission statement
- current phase
- roster summary by family
- active runs summary
- pending approvals
- current risks
- next checkpoint
- quality gate summary

### Primary Actions
- `Open mission detail`
- `View approvals`
- `View runs`
- `View quality gates`

## Screen 4: Mission Detail

### Goal
Act as the single mission operating cockpit.

### Header
- breadcrumb example: `Clients / Acme / ERP Modernization / Discovery Mission`
- title: mission name
- subheader chips:
  - mission status
  - current phase
  - risk level
  - quality gate status
  - approval state

### Header Actions
- `View approvals`
- `View runs`
- `View roster`
- later: `Request milestone acceptance`
- later: `Close mission`

### Layout
Recommended desktop layout:

- left column for mission context and delivery state
- right column for live control and activity state

### Left Column Sections
- `Mission Summary`
- `Approved Consultant Roster`
- `Project and Delivery`
- `Quality Gates`

### Right Column Sections
- `Run Activity`
- `Approval Queue`
- `Risks and Escalations`
- `Commercial Control`
- `Timeline`

### Mission Summary
Fields:

- `mission_name`
- `mission_statement`
- `success_definition`
- `client_name`
- `engagement_name`
- `status`
- `current_phase`
- `deliverables`
- `acceptance_criteria_summary`

### Approved Consultant Roster
Fields:

- `approved_roster_status`
- `agent_family`
- `instance_count`
- `operating_mode`
- `tool_profile`
- `last_heartbeat_at`
- `running_count`
- `waiting_count`
- `blocked_count`

### Project and Delivery
Fields:

- `milestones`
- `work_packages`
- `next_checkpoint_at`
- `project_manager_or_owner`
- `milestone_health`
- `budget_health`

### Quality Gates
Fields:

- `quality_gate_plan_id`
- `quality_gate_status`
- `active_gate_checkpoints`
- `failing_gate_count`
- `escalated_gate_count`
- `evidence_pack_refs`

### Run Activity
Fields:

- recent mission-linked workflow runs
- owning `agent_instance_id` when available
- route or provider metadata
- status and escalation flags

### Approval Queue
Fields:

- mission-linked pending approvals
- approval class
- requested by
- related entity
- created at

### Risks and Escalations
Fields:

- RAID-style risk list
- open escalations
- unresolved blockers
- watchdog summaries

### Commercial Control
Fields:

- `billing_plan_summary`
- `milestone_acceptance_status`
- `invoice_trigger_readiness`
- `closeout_readiness`

### Timeline
Unified event-style stream of:

- mission startup
- roster approval
- run activity
- quality gate outcomes
- milestone acceptance events
- billing readiness events
- closeout events

## Suggested Backend Read Models
These screens should prefer summary-oriented read models over raw entity dumps.

Recommended endpoints:

- `GET /portfolio/clients`
- `GET /portfolio/clients/{client_id}`
- `GET /portfolio/engagements`
- `GET /portfolio/engagements/{engagement_id}`
- `GET /portfolio/missions`
- `GET /portfolio/missions/{mission_id}`
- `GET /portfolio/missions/{mission_id}/roster`
- `GET /portfolio/missions/{mission_id}/quality-gates`
- `GET /portfolio/missions/{mission_id}/activity`

## Suggested TypeScript Contracts
Recommended frontend summary types:

```ts
type RiskLevel = "low" | "medium" | "high" | "critical";
type HealthStatus = "ok" | "watch" | "at_risk" | "blocked";

type ClientPortfolioRow = {
  client_id: string;
  client_name: string;
  tenant_id: string;
  active_engagements: number;
  active_missions: number;
  agents_dispatched: number;
  pending_approvals: number;
  risk_level: RiskLevel;
  last_activity_at?: string | null;
  health_status: HealthStatus;
};

type EngagementPortfolioRow = {
  engagement_id: string;
  engagement_name: string;
  client_id: string;
  client_name: string;
  stage: string;
  signed_scope_status: string;
  missions_count: number;
  approved_roster_status: string;
  billing_method?: string | null;
  last_activity_at?: string | null;
};

type MissionPortfolioRow = {
  mission_id: string;
  mission_name: string;
  engagement_id: string;
  engagement_name: string;
  client_id: string;
  client_name: string;
  status: string;
  current_phase: string;
  agents_dispatched: number;
  active_runs: number;
  pending_approvals: number;
  quality_gate_status?: string | null;
  risk_level: RiskLevel;
  last_activity_at?: string | null;
};

type MissionRosterItem = {
  agent_family: string;
  instance_count: number;
  operating_mode: string;
  tool_profile?: string | null;
  running_count: number;
  waiting_count: number;
  blocked_count: number;
  last_heartbeat_at?: string | null;
};

type MissionGateSummary = {
  quality_gate_plan_id?: string | null;
  quality_gate_status?: string | null;
  active_gate_checkpoints: string[];
  failing_gate_count: number;
  escalated_gate_count: number;
  evidence_pack_refs: string[];
};

type MissionDetailView = {
  mission_id: string;
  mission_name: string;
  mission_statement: string;
  success_definition: string;
  client_id: string;
  client_name: string;
  engagement_id: string;
  engagement_name: string;
  status: string;
  current_phase: string;
  risk_level: RiskLevel;
  quality_gate_status?: string | null;
  approval_state?: string | null;
  deliverables: string[];
  acceptance_criteria_summary: string[];
  milestone_health?: string | null;
  budget_health?: string | null;
  next_checkpoint_at?: string | null;
  roster: MissionRosterItem[];
  quality_gates: MissionGateSummary;
};
```

## Suggested React Page Structure
Recommended frontend files:

- `frontend/src/pages/ClientsPage.tsx`
- `frontend/src/pages/EngagementsPage.tsx`
- `frontend/src/pages/MissionsPage.tsx`
- `frontend/src/pages/MissionDetailPage.tsx`

Recommended supporting types:

- `ClientPortfolioRow`
- `EngagementPortfolioRow`
- `MissionPortfolioRow`
- `MissionDetailView`
- `MissionRosterItem`
- `MissionGateSummary`

Recommended reusable components:

- `PortfolioKpiStrip`
- `PortfolioFilters`
- `PortfolioTable`
- `PortfolioDetailPanel`
- `MissionStatusHeader`
- `RosterSummaryCard`
- `QualityGateSummaryCard`
- `MissionTimelineCard`

## MVP Delivery Sequence
Recommended implementation order:

1. `Missions`
2. `Mission Detail`
3. `Clients`
4. `Engagements`

Reasoning:

- the current app already thinks in runs, approvals, agent visibility, and mission-scoped delivery health
- the mission view becomes the fastest path to operator value once portfolio summary feeds exist
- clients and engagements become stronger after the formal agent-instance registry and mission linkage are available

## Dependency Notes
These pages depend on later contract and backend work already present in the roadmap:

- formal agent-instance registry
- mission and engagement linkage in traces and run summaries
- Track A portfolio summary feed
- approved consultant roster contract
- billing plan contract
- mission quality-gate persistence and read models

## Non-Goals
This UI map does not imply:

- direct editing of tenant-local delivery state from Track A
- immediate full CRUD over client, engagement, or mission entities
- replacement of workflow-first control with free-form dashboard actions
- centralizing Track B mutable state in the Track A UI

## Review Notes
This document should stay aligned with:

- `ROADMAP.md`
- `TODO.md`
- `ARCHITECTURE.md`
- `EPICS.md`
- `docs/agent-instance-portfolio-model.md`
- `docs/consulting-engagement-lifecycle-model.md`
- `docs/delivery-quality-gate-model.md`
