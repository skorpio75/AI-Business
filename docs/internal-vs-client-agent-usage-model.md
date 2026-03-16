<!-- Copyright (c) Dario Pizzolante -->
# Internal vs Client Agent Usage Model

## Purpose
Clarify the difference between internal agents and client-facing or client-delivery agents, and define when each should be used during the consulting lifecycle.

## Core Rule
The same family may exist in multiple modes, but the platform must choose the mode based on business purpose and state ownership.

- `internal_operating`: use when the consulting firm is running its own business or making internal decisions
- `client_delivery`: use when executing a mission inside a tenant-scoped client delivery context
- `client_facing_service`: use when producing a bounded client-facing advisory or service output, still as a separate client-scoped runtime

## Track Mapping
- Track A is where `internal_operating` agents live
- Track B is where `client_delivery` and most `client_facing_service` instances live once a mission exists
- Track A may host internal pre-sales advisory work about a client opportunity, but that is still an internal agent using internal state

## Internal Agent Use Cases
Use `internal_operating` agents for:

- lead spotting and materialization
- qualification and account research
- proposal and SOW shaping
- internal CTO/CIO or Chief AI advisory support for sales and delivery strategy
- contract and mission approval
- dispatch candidate planning
- billing, receivables, and mission closeout governance
- portfolio oversight across all clients

These agents work over the consulting firm's own commercial and operating state.

## Client Agent Use Cases
Use `client_delivery` agents for:

- project planning inside an approved mission
- requirements, architecture, build, QA, and documentation work for that mission
- mission-scoped retrieval over client documents and delivery evidence
- milestone readiness, quality-gate execution, and handoff preparation

Use `client_facing_service` when the output is a client-scoped advisory or service surface rather than internal company control work.

## Decision Rule
Ask one question first:

Is the agent acting on the consulting firm's internal business process, or on the client's mission execution context?

- if internal business process: `internal_operating`
- if client mission execution: `client_delivery`
- if client-scoped advisory/service output: `client_facing_service`

## Lifecycle Usage by Stage

### Lead to qualified opportunity
- use Track A `internal_operating`
- no Track B mission instances yet

### Proposal, SOW, and contract shaping
- use Track A `internal_operating`
- advisory families may reason about the client, but they still use internal opportunity context

### Signed scope to mission startup
- use Track A `internal_operating`
- create `dispatch_candidate_plan`
- approve `approved_consultant_roster`
- seed or activate Track B only after mission approval

### Active delivery
- use Track B `client_delivery`
- this includes PM, BA, Architect, Build, QA, Documentation, and mission-scoped specialist instances

### Milestone acceptance and billing
- Track B prepares delivery evidence
- Track A internal agents own billing control, invoice release, and receivables

### Portfolio oversight
- use Track A `internal_operating`
- Mission Control reads bounded portfolio summaries from client runtimes

## Same Family, Different Use
Example with `CTO/CIO Agent`:

- Track A internal CTO/CIO: internal counselor for solution shaping, proposal support, architecture positioning, and internal platform improvement
- Track B client CTO/CIO: client-scoped advisor embedded in one mission with tenant-scoped context and evidence

Example with `Project Management / Delivery Coordination Agent`:

- Track A internal PM coordination: internal planning around staffing, commercial readiness, and delivery oversight
- Track B client PM coordination: actual mission plan, checkpoints, deliverables, follow-ups, and milestone readiness

## Non-Negotiable Boundaries
- internal agents must not directly become the client runtime instance
- client-delivery agents must not own internal billing or portfolio control
- Track A may observe client activity, but not absorb tenant-local mutable state
- final client-facing commitments remain approval-bound under policy

## Practical Recommendation
Default to Track A first.

Only move to Track B when all of the following are true:

- a real client or engagement exists
- scope has been accepted or approved enough to justify mission startup
- an approved consultant roster exists
- tenant-scoped context, tools, and runtime boundaries are ready

That gives a clean operating rule:

- Track A decides, shapes, approves, bills, and oversees
- Track B executes, evidences, and delivers
