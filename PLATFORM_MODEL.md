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
- `Tool`: bounded action or retrieval capability exposed through a normalized tool ID
- `Workflow`: deterministic coordination logic that sequences steps, applies policies, and records outcomes
- `Trigger`: condition that starts a workflow or subflow, often driven by an event
- `Event`: normalized signal that something happened and may require processing
- `Run`: a single execution instance of a workflow or agent step
- `Approval`: a policy-gated human decision checkpoint tied to a run or business entity
- `Task`: a unit of follow-up work created inside or outside a workflow
- `MemorySource`: document, record, trace, or connector source contributing to memory
- `Client`: isolated business entity with its own state, storage, credentials, and runtime instances
- `Opportunity`: pre-sale entity representing lead, qualification, and proposal context
- `Project`: post-sale entity representing scoped work, milestones, risks, and outcomes
- `Policy`: rule constraining actions, approvals, autonomy, and tool use

## Family, Mode, Instance Model
Agent reuse is modeled through three levels:

- `family`: reusable capability pattern
- `mode`: internal operating, client delivery, or client-facing service mode
- `instance`: concrete runtime identity with isolated state and memory

This allows the same family to exist in both internal and client-facing forms without violating Track A and Track B isolation.

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

## Scaling Model
The platform is intended to support:

- solo operator use
- solo plus subcontractor support
- micro-firm operations
- boutique multi-role delivery teams
- later agent-augmented teams with delegated authority and richer policy enforcement
