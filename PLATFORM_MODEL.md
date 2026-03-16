<!-- Copyright (c) Dario Pizzolante -->
# Platform Model

## Purpose
Define the formal operating meta-model of the platform so implementation, documentation, and workflow design use the same concepts.

## Governing Principle
- Agents think
- Tools act
- Workflows coordinate
- Policies constrain
- Mission Control observes
- Humans approve key commitments

## Layer Model

```text
Interfaces
  ->
Workflows
  ->
Agents
  ->
Tools and Actions
  ->
Policies and Approvals
  ->
State and Events
  ->
Memory
  ->
Infrastructure
```

## Core Objects
- `Pod`: ownership layer for Growth, Delivery, Ops, and Executive responsibilities
- `Agent`: reasoning unit with bounded responsibility, tool profile, autonomy class, and state scope
- `AgentInstance`: concrete runtime identity for one family and mode inside one tenant or mission scope
- `AgentAssignment`: binding between an agent instance and a client, engagement, mission, workflow, or run scope
- `Tool`: bounded action or retrieval capability exposed through a normalized tool ID
- `Workflow`: deterministic coordination logic that sequences steps, applies policies, and records outcomes
- `Trigger`: condition that starts a workflow or subflow, often driven by an event
- `Event`: normalized signal that something happened and may require processing
- `Run`: a single execution instance of a workflow or agent step
- `Approval`: a policy-gated human decision checkpoint tied to a run or business entity
- `Task`: a unit of follow-up work created inside or outside a workflow
- `MemorySource`: document, record, trace, or connector source contributing to memory
- `Client`: isolated business entity with its own state, storage, credentials, and runtime instances
- `Engagement`: commercial container for a body of client work, such as a project, assessment, or advisory retainer
- `Mission`: bounded objective or workstream inside an engagement
- `DispatchCandidatePlan`: proposed consultant swarm, tool boundary, and delivery assumptions for a mission before approval
- `ApprovedConsultantRoster`: approved mission-bound consultant lineup that becomes eligible for runtime instantiation
- `BillingPlan`: approved commercial billing method and trigger rules for a mission or engagement
- `Opportunity`: pre-sale entity representing lead, qualification, and proposal context
- `Project`: post-sale entity representing scoped work, milestones, risks, and outcomes
- `Policy`: rule constraining actions, approvals, autonomy, and tool use

## Family, Mode, Instance Model
Agent reuse is modeled through three levels:

- `family`: reusable capability pattern
- `mode`: internal operating, client delivery, or client-facing service mode
- `instance`: concrete runtime identity with isolated state and memory

This allows the same family to exist in both internal and client-facing forms without violating Track A and Track B isolation.

For client-facing consulting and delivery work, the concrete runtime should also be mission-bound:

- one family can have many client-scoped instances
- each client-scoped instance should bind to one `tenant_id`, `client_id`, `engagement_id`, and `mission_id`
- Mission Control should supervise those instances as a portfolio rather than flattening them into one shared consultant identity

## Mode Usage Rule
Mode selection should follow business purpose, not only family identity.

- `internal_operating` is for the consulting firm's own commercial, approval, billing, and portfolio-control processes
- `client_delivery` is for tenant-scoped mission execution
- `client_facing_service` is for bounded client-scoped advisory or service outputs

The same family may appear in more than one mode, but those are separate runtime instances with different state and authority boundaries.

## Reasoning, Execution, Orchestration, Oversight
- Reasoning is handled by agents.
- Execution is handled by tools.
- Orchestration is handled by workflows.
- Oversight is handled by Mission Control plus human approvers.

## Workflow Governance Rule
- Workflows remain the process owner.
- Agents do not become free-roaming autonomous orchestrators.
- External systems do not become the source of truth for approvals, shared state, or memory promotion.

## Track Model

### Track A
- internal instance used to run the consulting firm

### Track B
- isolated client instance or replicated client-facing service deployment

Shared patterns:
- codebase
- templates
- contracts
- configuration schema

Isolated runtime assets:
- database
- vector index
- credentials
- logs
- documents
- client and project state
- runtime agent instances

## Portfolio Visibility Model
Track A Mission Control is intended to operate as a portfolio control tower over internal and client-delivery activity.

- Track B or client-delivery runtimes keep their own mutable state, memory, and approvals
- Track A may aggregate bounded portfolio summaries such as mission labels, dispatched agent counts, run status, pending approvals, and risk flags
- portfolio visibility must not become a shared mutable state layer across clients

This supports a CEO-style operating view over clients, engagements, missions, and dispatched consultant agents while preserving tenant isolation.

## Scaling Model
The platform is intended to support:

- solo operator use
- solo plus subcontractor support
- micro-firm operations
- boutique multi-role delivery teams
- later agent-augmented teams with delegated authority and richer policy enforcement
