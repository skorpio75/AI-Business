<!-- Copyright (c) Dario Pizzolante -->
# Consulting Engagement Lifecycle Model

## Purpose
Define the end-to-end operating model for a real consulting engagement, from spotted lead through signed scope, mission startup, delivery, milestone billing, and mission closeout.

## Recommended Operating Split
The recommended architecture is a linked two-environment model:

- Track A is the control plane for commercial progression, approvals, dispatch planning, billing, and portfolio oversight
- Track B is the delivery plane for tenant-scoped execution, client context, deliverables, and dispatched consultant instances

This preserves client isolation while keeping the consulting firm's commercial and financial control in Track A.

## Agent Usage Rule
The lifecycle should also make the internal-vs-client agent switch explicit.

- before mission approval, default to Track A `internal_operating`
- after roster activation, use Track B `client_delivery` for mission execution
- keep client-scoped advisory or service outputs in separate client runtimes rather than reusing the internal agent directly

## Lifecycle Stages
The target lifecycle should follow these stages:

1. lead spotting
2. lead normalization and materialization
3. qualification and proposal/SOW shaping
4. contract and signed scope
5. mission approval and consultant dispatch planning
6. approved consultant roster activation
7. delivery planning and execution
8. milestone acceptance
9. billing and receivables
10. mission closeout

## Lead Intake Rule
Lead intake follows the upstream rule defined in `docs/lead-intake-materialization-model.md`:

- spotting can come from manual and non-manual sources
- non-manual sources should normalize into candidates first
- only then should the platform materialize a real lead and emit `lead.received`

## Commercial Progression in Track A
Track A should own the commercial progression from spotted lead to mission startup.

Core commercial objects:

- `lead_signal`
- `lead_candidate`
- `opportunity`
- `commercial_scope`
- `proposal`
- `sow`
- `contract`
- `engagement`
- `mission`

Typical flow:

1. `lead_signal` is spotted
2. `lead_candidate` is normalized and deduplicated
3. a real `opportunity` is created
4. Growth agents qualify and shape the opportunity
5. `proposal` and `sow` drafts are prepared
6. once commercial terms are accepted, `contract` and signed scope are recorded

## Agent Dispatch Candidate Plan
Between signed scope and mission startup, the platform should create a `dispatch_candidate_plan`.

This is the proposal for the to-be consultant swarm attached to the mission.

It should contain:

- `engagement_id`
- `mission_id`
- mission statement
- agreed deliverables from the SOW
- candidate agent families
- candidate internal owners or operator roles where relevant
- expected effort or staffing hints
- expected timeline or phase coverage
- required tools and connector profile
- required RAG/context packs
- approval gates
- delivery assumptions and exclusions
- estimated billing implications

## Why Dispatch Planning Exists
The dispatch candidate plan is useful before delivery starts because it:

- makes the swarm explicit before activation
- supports scope validation
- supports budgeting and pricing review
- makes capacity and tool needs visible
- gives the CEO something concrete to approve before consultant instances are created

## Approved Consultant Roster
Once the dispatch candidate plan is approved, it should become the `approved_consultant_roster`.

The roster is the approved consultant lineup for the mission and should contain:

- approved agent families
- approved mission-bound instance count
- mission ownership roles such as PMO or PM lead
- approved context and tool boundaries
- approved delivery start conditions

The approved roster should then be visible:

- in Track A as part of engagement oversight
- in Track B as the `agents dispatched` view for that client mission

## Mission Startup Trigger
The preferred trigger sequence is:

1. `contract.signed`
2. `dispatch.plan.proposed`
3. `dispatch.plan.approved`
4. `mission.approved`
5. Track B tenant is seeded or activated if needed
6. approved consultant roster is instantiated as mission-bound client instances
7. delivery planning begins

This keeps signed commercial scope separate from operational startup approval.

## Delivery Startup
After roster activation, the Delivery pod should start the mission in Track B.

Typical startup flow:

1. create or activate `project_state`
2. PMO / Project Control Agent establishes governance baseline
3. Project Management / Delivery Coordination Agent creates the project plan
4. deliverables from the SOW are mapped into milestones, work packages, checkpoints, and acceptance criteria
5. a mission-specific `quality_gate_plan` is created from the SOW, project plan, deliverable classes, and acceptance criteria
6. BA, Architect, Build, QA, Documentation, and specialist advisory families are activated as needed from the approved roster

## Deliverables and SOW Alignment
Deliverables should remain first-class mission objects and stay linked to:

- the SOW
- the project plan
- milestones
- acceptance criteria
- quality gates
- later billing triggers

This avoids a gap between commercial promises and delivery execution.

## Delivery Quality Gates
Delivery quality should be treated as a mission mechanism, not only as one generic QA step.

The mission should carry a `quality_gate_plan` that defines:

- which gate checkpoints apply in planning, design, implementation, milestone release, and handoff phases
- which agent families review each deliverable class
- which gates must pass before milestone acceptance or handoff routing can proceed

Typical gate families:

- `QA / Review Agent`
- `Testing / QA Agent`
- `Documentation Agent`
- `Risk / Watchdog Agent` where escalation sensitivity is higher

This lets the platform review documents, code, automation flows, testing evidence, and handover packs in a way that reflects the actual mission shape.

## Billing Plan
The mission should also carry a `billing_plan` in Track A.

Suggested fields:

- `billing_method`
- `billing_schedule`
- `milestone_billing_rules`
- `time_and_material_rules`
- `fixed_fee_rules`
- invoice release conditions
- approver policy
- receivables follow-up policy

Supported billing methods may include:

- fixed fee by milestone
- time and materials
- retainer
- mixed model

## Milestone Acceptance and Billing Trigger
Billing should not start merely because work looks done internally.

Recommended flow:

1. Track B delivery agents prepare milestone evidence
2. required quality gates pass or are escalated and resolved
3. client acceptance is recorded
4. `milestone.accepted` is emitted
5. Track A internal billing agents create the invoice package according to the `billing_plan`
6. invoice release remains approval-bound under policy
7. receivables follow-up remains in Track A

This keeps billing under internal control while still depending on client-approved delivery evidence.

## Mission Closeout
Mission closeout should also be explicit.

Suggested closeout conditions:

- final deliverables accepted
- final handoff-readiness gate passed
- final invoice state resolved or intentionally open under policy
- remaining approvals resolved
- lessons learned captured
- final status and handover archived
- consultant roster marked inactive

Useful closeout objects:

- `mission_closeout`
- final delivery summary
- final commercial summary
- lessons learned pack

## Internal Agent Ownership
This lifecycle should remain owned by internal agents for commercial and financial control.

- Track A internal agents handle lead intake, qualification, proposal, SOW, contract progression, dispatch planning, billing, receivables, and closeout governance
- Track B client-scoped agents handle mission execution and delivery evidence inside the tenant boundary

## Key Planned Objects
The biggest missing operating objects are:

- `dispatch_candidate_plan`
- `approved_consultant_roster`
- `billing_plan`
- `milestone_acceptance`
- `mission_closeout`

## Recommended Next Implementation Sequence
1. formalize `dispatch_candidate_plan`
2. formalize `approved_consultant_roster`
3. formalize `billing_plan`
4. add the signed-scope to mission-start workflow
5. add milestone-acceptance to billing workflow
6. add mission closeout workflow
