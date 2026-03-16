# Pods

## Purpose
Define the 4-pod operating structure for the agent-run consulting firm and show how reusable agent families operate across internal and client-delivery contexts.

## Core Rule
The platform reuses agent families, not shared runtime identities.

- `family`: the reusable capability pattern, such as `PMO / Project Control Agent`
- `mode`: the operating context for that family, such as `internal_operating` or `client_delivery`
- `instance`: the concrete runtime identity with its own memory, tools, approvals, and tenant scope

Example:
- `PMO / Project Control Agent` is the family
- `Internal PMO Agent` is one Track A instance
- `Client PMO Agent - Acme ERP rollout` is a separate Track B instance

For client-facing use, the instance should also bind to a concrete `client`, `engagement`, and `mission` so one reusable family can be dispatched across the portfolio without sharing runtime identity.

## Pod Definitions

### Pod A - Growth
Purpose:
- acquire, qualify, and convert business

Primary agents:
- Lead Intake Agent
- Account Research Agent
- Qualification Agent
- Outreach Draft Agent
- Proposal / SOW Agent
- CRM Hygiene Agent

### Pod B - Delivery
Purpose:
- execute consulting, IT, digital, data, and AI delivery work

Primary agents:
- PMO / Project Control Agent
- Project Management / Delivery Coordination Agent
- BA / Requirements Agent
- Architect Agent
- Build / Automation Agent
- QA / Review Agent
- Documentation Agent

### Pod C - Ops
Purpose:
- run the company as an operating business

Primary agents:
- Finance Ops Agent
- Invoice / Receivables Agent
- Vendor / Procurement Agent
- Admin / HR Ops Agent
- Company Reporting Agent

### Pod D - Executive
Purpose:
- maintain leadership visibility, prioritization, escalation, and control

Primary agents:
- CEO Briefing Agent
- Strategy / Opportunity Agent
- Risk / Watchdog Agent
- Mission Control Agent

## Specialist Overlays
The pod model does not replace specialist business agents. The following remain valid and can overlay pod workflows where needed:

- CFO Agent
- Accountant Agent
- Finance Agent
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent
- Compliance/Contract Agent
- Procurement Agent
- Knowledge Agent
- Document Agent
- Project Management Agent
- Delivery Agent
- Quality Management Agent
- Consulting Support Agent
- Testing/QA Agent
- Ops Agent

Suggested overlay mapping:

### Growth overlays
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent

### Delivery overlays
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent
- Compliance/Contract Agent
- Knowledge Agent

### Ops overlays
- CFO Agent
- Accountant Agent
- Finance Agent
- Procurement Agent
- Reporting Agent

### Executive overlays
- CFO Agent
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent
- Risk / Watchdog Agent

## Pod Boundaries
- Growth owns pre-sale opportunity progression.
- Delivery owns project execution artifacts and client-delivery coordination.
- Inside Delivery, `PMO / Project Control Agent` is the governance and control-tower role, while `Project Management / Delivery Coordination Agent` is the execution-follow-up role that keeps plans, checkpoints, and actions moving.
- Ops owns internal business operations and company records.
- Executive owns visibility, escalation, prioritization, and approval routing.

## Internal and Track B Replication Rules
- Track A internal pod instances own Track A state and memory only.
- Track B client pod instances must be replicated as separate instances per client deployment.
- Agent families may be reused across tracks, but state, memory, credentials, and approvals must remain isolated.
- A client-facing service offer may reuse a family contract without sharing operational runtime identity with the internal instance.

## Orchestrator Strategy
- Workflows remain the coordination backbone.
- Pods clarify operational ownership.
- Agents reason within pod-specific or overlay-specific responsibilities.
- Tools act through policy and approval constraints.
- Mission Control supervises cross-pod visibility, failed runs, and pending approvals.
- Track A Mission Control should eventually aggregate portfolio summaries across client engagements and dispatched consultant instances without becoming the shared mutable source of truth for those client runtimes.

## Operating Maturity
The pod model is designed to scale across these stages:

- solo operator
- solo operator plus subcontractors
- micro-firm of 2-4 people
- boutique firm of 5-7 people
- 10-person agent-augmented firm
