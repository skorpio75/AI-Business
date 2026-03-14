# Agents

## Purpose
This document lists the canonical agents used to run an IT freelancer company with one human CEO.

## Governance
- CEO is the sole human approver for high-risk decisions.
- Agents can execute routine tasks within workflow and policy constraints.
- No autonomous external commitment in MVP without CEO approval.
- Track 1 internal agents own their own state and memory. If an agent pattern is reused for Track 2 client services, it must be replicated as a separate agent/instance, not shared.
- When implementation, architecture, workflow scope, integrations, or priorities change, update all affected markdown governance files in the same work session to keep them aligned.
- `ROADMAP.md` is the implementation status source of truth. `TODO.md` is the short execution view derived from it.
- At minimum, review `ROADMAP.md`, `TODO.md`, `ARCHITECTURE.md`, `EPICS.md`, `INTEGRATIONS.md`, and `DECISIONS.md` for drift whenever a material change is made.

## Agent Model
The platform models reusable capability through:

- `family`: the reusable capability pattern
- `mode`: the operating context, such as `internal_operating` or `client_delivery`
- `instance`: the concrete runtime identity with isolated state, memory, tools, and approvals

This allows the same family to exist in both internal-operating and client-delivery forms without sharing runtime state.

Example:
- `PMO / Project Control Agent` is a family
- `Internal PMO Agent` is a Track A instance
- `Client PMO Agent - Acme` is a separate Track B instance

## Pod Model
The canonical operating model uses four pods:

- `Growth`
- `Delivery`
- `Ops`
- `Executive`

Existing specialist roles remain valid and can overlay pod workflows.

## First-Class Pod Agents
The following agents are canonical first-class pod agents that complement the existing specialist catalog.

### Growth Pod
#### Lead Intake Agent
- Purpose: ingest inbound lead signals and create structured opportunity records
- Pod: `Growth`
- Modes: `internal_operating`, later `client_delivery` where relevant
- Autonomy class: `supervised_executor`
- State ownership: initializes `opportunity_state`

#### Account Research Agent
- Purpose: enrich opportunities with account and market context
- Pod: `Growth`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant`
- State ownership: enriches `opportunity_state`

#### Qualification Agent
- Purpose: score fit and recommend next commercial path
- Pod: `Growth`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant` or `supervised_executor` depending on write path
- State ownership: updates qualification fields in `opportunity_state`

#### Outreach Draft Agent
- Purpose: prepare bounded outreach drafts and follow-up messaging
- Pod: `Growth`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant`
- State ownership: contributes next-step outputs to `opportunity_state`

#### Proposal / SOW Agent
- Purpose: prepare commercial scope, proposal, and SOW drafts
- Pod: `Growth`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `supervised_executor`
- State ownership: updates proposal-related fields in `opportunity_state`

#### CRM Hygiene Agent
- Purpose: keep commercial records structured and current
- Pod: `Growth`
- Modes: `internal_operating`, later `client_delivery`
- Autonomy class: `supervised_executor`
- State ownership: maintains CRM-aligned opportunity metadata

### Delivery Pod
#### PMO / Project Control Agent
- Purpose: own project governance and operational control
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`, `client_facing_service`
- Autonomy class: `supervised_executor`
- State ownership: governance fields in `project_state`
- Replication rule: internal PMO and client PMO are separate instances even when they share the same family

#### BA / Requirements Agent
- Purpose: turn workshops and documents into structured requirements
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant`
- State ownership: updates requirements-related project fields

#### Architect Agent
- Purpose: convert requirements into solution structure
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant`
- State ownership: updates design and risk fields in `project_state`

#### Build / Automation Agent
- Purpose: implement scripts, automations, configuration, and scaffolds
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `supervised_executor`
- State ownership: updates build/progress fields in `project_state`

#### QA / Review Agent
- Purpose: validate quality and consistency before release or milestone close
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `assistant`
- State ownership: updates quality and readiness fields in `project_state`

#### Documentation Agent
- Purpose: produce working documentation and handover packs
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `supervised_executor`
- State ownership: updates documentation and handover readiness fields

### Ops Pod
#### Finance Ops Agent
- Purpose: run internal finance operations and exceptions
- Pod: `Ops`
- Modes: `internal_operating`

#### Invoice / Receivables Agent
- Purpose: manage invoice drafts, receivable tracking, and payment reminders
- Pod: `Ops`
- Modes: `internal_operating`

#### Vendor / Procurement Agent
- Purpose: control vendor requests and procurement flows
- Pod: `Ops`
- Modes: `internal_operating`

#### Admin / HR Ops Agent
- Purpose: support bounded administrative and people-ops workflows
- Pod: `Ops`
- Modes: `internal_operating`

#### Company Reporting Agent
- Purpose: generate internal reporting and KPI views
- Pod: `Ops`
- Modes: `internal_operating`, later `client_delivery` in scoped reporting-service form

### Executive Pod
#### CEO Briefing Agent
- Purpose: summarize leadership-relevant activity, blockers, and decisions
- Pod: `Executive`
- Modes: `internal_operating`

#### Strategy / Opportunity Agent
- Purpose: synthesize strategic options across growth, delivery, and financial signals
- Pod: `Executive`
- Modes: `internal_operating`, later `client_facing_service` in advisory form

#### Risk / Watchdog Agent
- Purpose: detect, summarize, and escalate operational or delivery risks
- Pod: `Executive`
- Modes: `internal_operating`, `client_delivery`

#### Mission Control Agent
- Purpose: supervise runs, approvals, escalations, and operating visibility
- Pod: `Executive`
- Modes: `internal_operating`, `client_delivery`
- Autonomy class: `supervised_executor`
- State ownership: supervises `run_state` and `approval_state` visibility, but does not own business entity state
- Replication rule: if used for client delivery supervision, it must run as a separate tenant-specific supervisor instance

## Corporate Function Agents
### Email Agent
- classify inbound email
- retrieve context
- draft replies
- escalate low-confidence cases

### Personal Assistant Agent
- read inbox and calendar events
- detect commitments, deadlines, and conflicts
- generate prioritized daily action list
- draft quick replies and meeting prep notes

### Billing Agent
- generate invoices from approved timesheets/deliverables
- track payment status and reminders
- escalate overdue receivables

### Accountant Agent
- maintain bookkeeping records and journal consistency
- reconcile invoices, payments, and expense entries
- prepare accounting-ready exports and period-close checklists

### CFO Agent
- provide financial strategy recommendations and scenario planning
- monitor profitability, pricing, and cashflow risk
- advise CEO on investment, cost control, and growth decisions

### Finance Agent
- produce cashflow snapshots
- track revenue, expenses, and runway
- flag financial risks and anomalies

### Procurement (PO) Agent
- draft and track purchase orders
- validate budget limits before submission
- route approval for external commitments

### Reporting Agent
- generate weekly/monthly business reports
- consolidate operations and delivery KPIs

### Compliance/Contract Agent
- track contract obligations and milestones
- flag legal/compliance deadlines
- draft non-binding summaries for CEO review

### CTO/CIO Agent
- advise on client technology strategy based on scope and context
- provide architecture and delivery counsel for proposals and execution
- continuously assess and improve internal platform architecture, reliability, and tooling
- identify technical debt, optimization opportunities, and modernization priorities
- internal-first contract; replicate later for Track 2 CIO/CTO service offers without sharing Track 1 state

### Chief AI / Digital Strategy Agent
- advise clients on AI, digitalization, AI engineering, and data engineering opportunities
- translate customer scope into practical AI/data roadmaps and delivery plans
- provide implementation guidance for AI products, automations, and data platforms
- track AI capability maturity and prioritize continuous improvement actions
- internal-first contract; replicate later for Track 2 AI/digital strategy service offers without sharing Track 1 state

### Document Agent
- classify documents
- extract structured data
- route for processing

## Service Delivery Agents
### Knowledge Agent
- answer grounded questions from internal documents
- provide evidence-backed outputs

### Project Management Agent
- maintain project plan, tasks, and deadlines
- produce delivery forecasts and risk flags

### Delivery Agent
- orchestrate delivery checklists per engagement
- track milestone readiness and handoff state

### Quality Management Agent
- run quality gates before deliverable release
- enforce definition-of-done checks

### Consulting Support Agent
- prepare research-backed draft recommendations
- retrieve relevant internal/external context

### Documentation Agent
- generate and maintain project documentation packs
- ensure versioned artifacts for handover

### Testing/QA Agent
- generate and execute test plans
- summarize defects and release-readiness signals

### Ops Agent
- assist with internal operations and runbooks
- support release checklists and execution hygiene

## Reuse Guidance for Track B
The following families are strong candidates for replicated client-delivery or client-facing service use:

- PMO / Project Control Agent
- BA / Requirements Agent
- Architect Agent
- Build / Automation Agent
- QA / Review Agent
- Documentation Agent
- Knowledge Agent
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent
- Reporting Agent
- Document Agent

These are reused as separate instances per client, not shared Track A agents.

## Approval Principle
No sensitive external action is sent automatically in MVP. CEO approval is required before execution for:
- money movement, invoicing release, and purchasing commitments
- contract/legal communications
- client-facing final deliverables
