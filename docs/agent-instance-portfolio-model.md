# Agent Instance and Portfolio Model

## Purpose
Define how reusable agent families become client-scoped runtime instances, and how Track A Mission Control can oversee the portfolio of client missions without breaking tenant isolation.

## Compatibility Summary
This model is compatible with the current architecture and the enterprise blueprint in `AI-Business_IDE_Handoff.md`.

- It extends the existing `family -> mode -> instance` rule instead of replacing it.
- It preserves Track A and Track B isolation by keeping mutable state, memory, credentials, and approvals inside each tenant-scoped runtime.
- It fits the existing Mission Control role as an operating supervisor and visibility layer.
- It does not require a free-form autonomous agent mesh; workflow control remains primary.

## Core Principle
Client-facing consulting capability is reusable at the family level, but instantiated at the mission level.

- `family`: reusable capability pattern such as `CTO/CIO Agent`
- `mode`: operating context such as `internal_operating`, `client_delivery`, or `client_facing_service`
- `instance`: concrete runtime identity with isolated tools, memory, approvals, and tenant scope

For customer-facing work, the instance should be bound to a specific client context rather than existing as one global consultant.

## Client-Facing Instance Binding
A client-facing agent instance should be scoped by:

- `tenant_id`
- `client_id`
- `engagement_id`
- `mission_id`
- `family_id`
- `mode`
- `tool_profile_id`
- `approval_policy_ref`
- `memory_scope_refs`
- `runtime_env_ref`

Example:

- `family_id`: `cto_cio_agent`
- `mode`: `client_delivery`
- `tenant_id`: `acme`
- `client_id`: `acme`
- `engagement_id`: `acme-erp-modernization`
- `mission_id`: `acme-erp-discovery`
- `instance_id`: `acme-erp-discovery-cto-cio-01`

This keeps one reusable consulting family available across the portfolio while ensuring every real runtime is attached to one bounded mission.

## Portfolio Objects
The portfolio operating view should distinguish the following objects:

- `client`: the account or tenant being served
- `engagement`: the commercial container for a body of work, such as a project, advisory retainer, or assessment
- `mission`: the bounded objective or workstream inside an engagement
- `agent_instance`: one runtime consultant identity attached to one mission
- `agent_assignment`: the link between an `agent_instance` and the mission or workflow scope it is serving

Suggested relationship:

- one `client` can have many `engagements`
- one `engagement` can have many `missions`
- one `mission` can have many `agent_instances`
- one `agent_instance` can participate in many workflow runs, but only inside its approved mission scope

## Track A Portfolio Cockpit
Track A Mission Control should act as the internal control tower for the client portfolio.

It should be able to show:

- all clients
- active engagements per client
- active missions per engagement
- number of dispatched agent instances per mission
- active runs per mission
- pending approvals
- escalation or risk signals
- last activity and health posture

This should feel like a CEO viewing a swarm of consultant-agents deployed across the portfolio, while still respecting client isolation.

## Isolation Rule for Portfolio Visibility
Track A portfolio visibility must not rely on shared mutable business state across clients.

Instead, each client runtime should expose or publish bounded operational summaries such as:

- instance identity metadata
- mission and engagement labels
- run counts and run status
- approval counts
- risk or escalation flags
- last-seen heartbeat

Track A Mission Control may aggregate those summaries into one portfolio dashboard, but it should not become the shared source of truth for client delivery state.

## Dashboard Shape
The target portfolio dashboard should center on:

- `client`
- `engagement`
- `mission`
- `agents_dispatched`
- `active_runs`
- `pending_approvals`
- `risk_level`
- `last_activity_at`

Useful example views:

- client portfolio table
- engagement or mission drill-down
- dispatched consultant count by family
- active agent-instance roster
- blocked or escalated missions

## Agent Family Examples
Likely client-scoped consultant instances include:

- `Client CTO/CIO Agent - Acme ERP Discovery`
- `Client Chief AI Agent - Beta Data Platform Strategy`
- `Client PMO Agent - Gamma Rollout`
- `Client Architect Agent - Delta Integration Workstream`
- `Client QA / Review Agent - Epsilon Delivery Gate`

The same family may also exist as an internal Track A instance, but that is a separate runtime identity with different state and memory.

## Workflow and Review Compatibility
This model is compatible with the current workflow-first and bounded-review architecture.

- workflows still assign and coordinate work
- agent instances execute bounded steps
- hybrid retrieval can remain mission-scoped
- review or gate agents still operate as explicit workflow steps
- Mission Control still supervises rather than replacing workflow control

## Planned Implementation Direction
This model implies later implementation work for:

- an agent-instance registry keyed by client, engagement, and mission
- mission-scoped assignment metadata for workflow runs and later `agent_runs`
- a Track A portfolio summary feed that reads client-runtime telemetry without violating isolation
- a Mission Control portfolio dashboard showing clients, missions, dispatched consultants, and operating health
