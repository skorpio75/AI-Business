# Workflows

## Purpose
This document lists reusable workflow templates across company operations and service delivery.

## Workflow Contract Pattern
Each workflow should increasingly specify:

- owning pod
- primary agent owner by step
- start event or trigger
- emitted events
- state objects read or written
- approval gates

## Cross-Agent Handoff Templates

### Opportunity to Proposal
- Start event: `lead.received`
- Pod owner: `Growth`
- State objects: `opportunity_state`, `run_state`, `approval_state`
- Handoff:
  1. Lead Intake Agent
  2. Account Research Agent
  3. Qualification Agent
  4. Outreach Draft Agent or discovery scheduling
  5. Proposal / SOW Agent
  6. Finance review when pricing implications exist
  7. CEO approval
  8. external send
- Emitted events:
  - `lead.enriched`
  - `lead.qualified`
  - `proposal.requested`
  - `proposal.submitted`
  - `approval.pending` when approval is required

### Delivery Flow
- Start event: `deal.won`
- Pod owner: `Delivery`
- State objects: `project_state`, `run_state`, `approval_state`
- Handoff:
  1. PMO / Project Control Agent opens project structure
  2. Project Management / Delivery Coordination Agent activates work packages, actions, and checkpoint cadence
  3. BA / Requirements Agent updates requirements
  4. Architect Agent produces design
  5. Build / Automation Agent implements
  6. QA / Review Agent validates
  7. Documentation Agent packages handover and working docs
  8. Project Management / Delivery Coordination Agent updates follow-ups and checkpoint readiness
  9. PMO / Project Control Agent updates steering status and escalations
  10. Finance trigger if milestone is reached
- Emitted events:
  - `project.created`
  - `requirements.updated`
  - `design.completed`
  - `build.completed`
  - `qa.passed` or `qa.failed`
  - `milestone.completed`

## Core MVP Workflows
### Workflow 1 - Email Operations
Start event:
- operator launch or inbox-originated message selection

State objects:
- `run_state`
- `approval_state` when outbound send requires approval

1. ingest email
2. classify intent
3. retrieve knowledge
4. draft reply
5. confidence check
6. approval
7. send

### Workflow 2 - Knowledge Q&A
Start event:
- operator question or knowledge query

State objects:
- `run_state`

1. receive question
2. retrieve relevant chunks
3. synthesize answer
4. return with evidence

### Workflow 3 - Document Intake
Start event:
- `document.ingested` trigger or operator upload

State objects:
- `run_state`

1. upload document
2. extract text
3. classify
4. extract fields
5. validate
6. store result

### Workflow 4 - Proposal Generation
Start event:
- `proposal.requested`

State objects:
- `opportunity_state`
- `run_state`
- `approval_state`

1. collect opportunity data
2. load reusable context
3. generate proposal draft
4. review and approve

### Workflow 5 - Personal Assistant Daily Triage
Start event:
- `schedule.daily_brief`

State objects:
- `run_state`
- `approval_state` when Microsoft To Do task promotion or other outbound action requires approval

Connector context:
- when Microsoft 365 is active, inbox, calendar, and Microsoft To Do should share the same tenant, client ID, and operator account context

1. ingest inbox metadata, calendar events, and optional Microsoft To Do context
2. detect deadlines, blockers, meeting conflicts, and task gaps
3. classify urgency/importance
4. generate prioritized action list and recommended next actions for the day
5. prepare candidate Microsoft To Do items with suggested priority where recommendations should become tracked tasks
6. route Microsoft To Do task creation/priority writes and other high-risk outbound actions to CEO approval
7. create/update approved Microsoft To Do items and draft suggested quick replies and prep notes

## Corporate Function Workflows
### Workflow 6 - Billing and Collections
Start event:
- `invoice.triggered`

State objects:
- `approval_state`
- `run_state`

1. collect approved delivery/time records
2. generate invoice draft
3. validate pricing and tax fields
4. route CEO approval
5. issue invoice
6. track payment status and reminders

### Workflow 7 - Finance Reporting
Start event:
- scheduled finance reporting cadence

State objects:
- `run_state`

1. ingest revenue/expense records
2. generate cashflow and margin summary
3. flag anomalies and forecast risks
4. route report to CEO

### Workflow 8 - Procurement (PO)
Start event:
- purchase request intake

State objects:
- `approval_state`
- `run_state`

1. intake purchase request
2. validate budget and vendor data
3. generate PO draft
4. route CEO approval
5. issue approved PO

### Workflow 9 - Accounting Close and Reconciliation
Start event:
- `month_end.started`

State objects:
- `run_state`

1. ingest invoices, payments, and expenses
2. reconcile ledger entries and detect mismatches
3. generate close checklist and exception report
4. route unresolved exceptions to CEO

### Workflow 10 - CFO Financial Strategy Review
Start event:
- scheduled executive finance review

State objects:
- `run_state`

1. consolidate financial and delivery KPIs
2. run profitability and cashflow scenarios
3. generate strategic recommendations (pricing, cost, investment)
4. route decision options to CEO

## Service Delivery Workflows
### Workflow 11 - Project Delivery Control
Start event:
- `deal.won` or `project.created`

State objects:
- `project_state`
- `run_state`
- `approval_state` where release gating applies

1. ingest project scope and milestones
2. PMO / Project Control Agent establishes control structure, milestones, and RAID baseline
3. Project Management / Delivery Coordination Agent turns scope and milestones into active tasks, checkpoints, and follow-ups
4. monitor progress and risks
5. trigger quality gate
6. route release recommendation to CEO

### Workflow 12 - Quality and Testing Gate
Start event:
- `build.completed` or milestone review

State objects:
- `project_state`
- `run_state`
- `approval_state` if release requires sign-off

1. gather acceptance criteria
2. run test checklist
3. capture defects and severity
4. summarize release readiness
5. route final go/no-go to CEO

### Workflow 13 - Documentation and Handover
Start event:
- `qa.passed` or handover preparation trigger

State objects:
- `project_state`
- `run_state`

1. collect project artifacts
2. generate structured documentation pack
3. validate completeness
4. route handover package for CEO review

### Workflow 14 - CTO/CIO Counsel and Platform Improvement
Start event:
- operator launch, proposal support request, or strategic review cadence

State objects:
- `run_state`

1. ingest client scope, constraints, and business goals
2. generate technology strategy options and trade-offs
3. propose architecture and implementation guidance
4. generate internal platform improvement recommendations
5. prioritize roadmap actions by impact, risk, and effort
6. route strategic recommendations to CEO for approval

### Workflow 15 - Chief AI/Digital Strategy Advisory and Delivery Plan
Start event:
- operator launch, discovery completion, or proposal support request

State objects:
- `run_state`

1. ingest customer business scope, processes, and data context
2. identify high-impact AI/digitalization opportunities
3. generate AI engineering and data engineering implementation options
4. define phased delivery roadmap, dependencies, and risks
5. produce consulting recommendations and execution playbook
6. route strategic plan to CEO for approval before external commitment
