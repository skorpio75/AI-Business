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
- `AGENT_LLM_ROUTING_MATRIX.md` is the family-level planning reference for LLM execution posture by agent family.
- Mission Control UI should derive per-agent operating-model and routing-posture labels from governed metadata so operator descriptions stay consistent with runtime behavior.
- At minimum, review `ROADMAP.md`, `TODO.md`, `AGENT_LLM_ROUTING_MATRIX.md`, `ARCHITECTURE.md`, `EPICS.md`, `INTEGRATIONS.md`, and `DECISIONS.md` for drift whenever a material change is made.

## Governed Agentic Company Principle
This company may become highly agentic, but it must remain governed.

- Agents should use LLM capacity heavily for reasoning, internal counseling, client-facing consulting, synthesis, drafting, and deliverable support.
- Governance is not optional around that reasoning: workflows, approval policy, tool permissions, autonomy class, state boundaries, tenant isolation, and auditability still apply.
- The target operating model is not deterministic-only control and not free-form autonomous behavior. It is LLM-centered agent capability inside explicit business guardrails.
- Growth in autonomy must happen through governed runtime design, step boundaries, and approval-safe promotion rather than by letting agents act outside policy.

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

## Prompt Model
`AGENTS.md` is the operating catalog for agent families and runtime boundaries, not the primary home of agent prompts.

- This document defines role, scope, pod, mode, autonomy, state ownership, tool boundary, and approval expectations.
- Base prompts for agent families should live in a separate runtime prompt layer.
- Workflow or step prompts should also live separately so a single family can be reused across multiple bounded tasks without one oversized static prompt.
- Runtime execution should combine:
  - family-level base prompt
  - workflow-step prompt
  - injected state, tool, approval, tenant, and output-schema context
- Prompt authoring is part of the target operating model, but full prompt expansion should follow contract, state, and workflow-boundary stabilization.

## Commercial Reuse Policy
Reusable agent families may support both internal company operations and billable client delivery work, but only through separate scoped instances.

- Internal agents help run the company itself, such as pipeline control, delivery capacity monitoring, margin visibility, internal reporting, and operational follow-up.
- Client-delivery agents help produce engagement outputs that may be billed as part of a service, such as project plans, RAID logs, status reports, steering packs, architecture notes, requirements packs, QA findings, or handover documentation.
- The commercial unit is the service outcome produced with agent assistance, not the sharing of an internal agent with a client.
- A client-delivery instance must remain isolated by `tenant`, `project_state`, memory, tool permissions, approval policy, and audit trail.
- The same family may later appear in a `client_facing_service` mode, but that is still a separate client-scoped runtime instance, not a shared Track 1 internal agent.

Example:
- `Internal PMO Agent` monitors your company portfolio, capacity, deadlines, and margin pressure.
- `Client PMO Agent - Acme ERP Rollout` produces billable delivery artifacts for that engagement, such as project plans, status packs, RAID updates, and follow-up actions.

## Pod Model
The canonical operating model uses four pods:

- `Growth`
- `Delivery`
- `Ops`
- `Executive`

Existing specialist roles remain valid and can overlay pod workflows.

## Multi-Agent Structure
The intended multi-agent structure is:

- a workflow orchestrator layer that remains the top-level control model
- specialized agents that execute bounded reasoning or action steps
- optional supervisor/orchestrator agents for pod-level oversight where justified
- structured agent-to-agent handoffs mediated by workflows, shared state, and approval policy

This is not a free-form peer-agent mesh. Agents do not discover, negotiate, or commit work arbitrarily outside workflow boundaries.

### Orchestrator Layer
- The workflow layer is the primary orchestrator today.
- `Mission Control Agent` is the clearest supervisor/orchestrator agent and may supervise pod-level runtime behavior later.
- Dedicated pod supervisors such as a future `Growth Supervisor` are optional and should only be introduced when they add operational value beyond workflow control.

### Specialized Agents
- Specialized agents perform bounded tasks with distinct reasoning modes, tool profiles, and state responsibilities.
- Examples include PMO, delivery coordination, BA, architect, build, QA, documentation, lead intake, research, qualification, and proposal.

### Structured A2A
Agent-to-agent handoff is allowed only in a structured form:

- explicit `agent_id`
- workflow step boundary
- standardized handoff payload
- shared-state read/write contract
- approval-policy enforcement when required

This means A2A is workflow-mediated, not autonomous peer networking.

### Review and Gate Pattern
Bounded review or judge-style behavior is valid in later multi-agent workflows, but only as an explicit step pattern:

- a review/gate agent receives a bounded artifact plus rubric
- it returns finite outcomes such as `approve`, `revise`, `escalate`, or `human_review`
- it does not become a universal always-on second pass for every task
- it does not replace CEO approval for sensitive external commitments

## Multi-Agent Suitability Matrix
The following families are currently assessed as high-suitability candidates for bounded multi-agent runtime use. This matrix is an implementation prioritization aid, not a mandate to promote every listed family immediately.

LLM routing and direct-Ollama adoption are tracked separately in `AGENT_LLM_ROUTING_MATRIX.md`. Multi-agent suitability does not by itself determine whether a family should use compact direct-Ollama, richer governed `ModelGateway` reasoning, or deterministic/tool-first execution.

| Agent / Family | Suitability | Why |
|---|---:|---|
| `Lead Intake Agent` | High | Starts structured opportunity flow and feeds downstream research, qualification, and proposal work. |
| `Account Research Agent` | High | Specialist enrichment role before qualification and proposal. |
| `Qualification Agent` | High | Decision point that routes toward outreach, proposal, or discard. |
| `Outreach Draft Agent` | High | Natural downstream specialist after qualification. |
| `Proposal / SOW Agent` | High | Depends on prior enrichment and often needs pricing and review handoffs. |
| `PMO / Project Control Agent` | High | Control-tower role across project state, milestones, RAID, and escalations. |
| `Project Management / Delivery Coordination Agent` | High | Converts plans into active follow-ups and checkpoints. |
| `BA / Requirements Agent` | High | Upstream specialist feeding architect, build, and test roles. |
| `Architect Agent` | High | Distinct reasoning mode between requirements and implementation. |
| `Build / Automation Agent` | High | Execution specialist after design. |
| `QA / Review Agent` | High | Independent validation role after build. |
| `Documentation Agent` | High | End-of-chain packaging and handover specialist. |
| `Mission Control Agent` | High | Natural supervisor, escalation, and visibility orchestrator. |
| `Risk / Watchdog Agent` | High | Cross-agent monitoring and escalation role. |
| `CEO Briefing Agent` | High | Cross-pod synthesis agent. |
| `Strategy / Opportunity Agent` | High | Synthesizes outputs from growth, delivery, and finance. |
| `Accountant Agent` | High | Reconciliation and exception handling often need upstream and downstream handoffs. |
| `CFO Agent` | High | Scenario synthesis over multiple internal signals. |
| `CTO/CIO Agent` | High | Cross-domain strategist drawing from knowledge, architecture, delivery, and roadmap context. |
| `Chief AI / Digital Strategy Agent` | High | Advisory synthesis across business, process, data, and AI dimensions. |

### Medium Suitability Set

| Agent / Family | Suitability | Why |
|---|---:|---|
| `CRM Hygiene Agent` | Medium | Often deterministic, but can be part of Growth pod cleanup and validation. |
| `Finance Ops Agent` | Medium | Good in the Ops pod, but much can remain rules-based. |
| `Invoice / Receivables Agent` | Medium | Useful with exception, review, and escalation loops. |
| `Vendor / Procurement Agent` | Medium | Strong when combined with budget, policy, and approval agents. |
| `Admin / HR Ops Agent` | Medium | Useful for bounded operational workflows, less for autonomous collaboration. |
| `Company Reporting Agent` | Medium | Often more of a synthesizer than a full collaborator. |
| `Billing Agent` | Medium | Stronger when disputes, approvals, and accounting checks exist. |
| `Finance Agent` | Medium | Better as a feeder into CFO and reporting than a standalone swarm participant. |
| `Procurement Agent` | Medium | Strong as an approval and policy-routing specialist. |
| `Reporting Agent` | Medium | Often a terminal summarizer fed by other agents. |
| `Compliance / Contract Agent` | Medium | Strong when linked with deadline, risk, and review chains. |
| `Document Agent` | Medium | Good in extraction to validation to routing chains. |
| `Knowledge Agent` | Medium | Very useful as a shared specialist, but often service-style rather than autonomous peer behavior. |
| `Delivery Agent` | Medium | Works as a coordinator wrapper, but overlaps with PM and PMO roles. |
| `Quality Management Agent` | Medium | Strong gating role, though often a fixed step rather than a dynamic agent. |
| `Consulting Support Agent` | Medium | Good feeder agent for advisory chains. |
| `Testing / QA Agent` | Medium | Useful in build, validation, and release chains, but can remain a fixed stage. |
| `Personal Assistant Agent` | Medium | Good candidate for internal sub-agents later across inbox, calendar, prioritization, and drafting. |

### How To Use This Matrix
- High suitability means the family is a strong candidate for later bounded multi-agent runtime behavior.
- Medium suitability means the family is a good candidate where collaboration or exception handling adds value, but it may remain workflow-stage-oriented or rules-based for longer.
- High suitability does not override the workflow-first rule.
- Promotion to runtime should still follow the phased path in `ROADMAP.md`: step identity, handoff payloads, shared-state contracts, execution logs, and approval metadata first.
- The matrix helps decide runtime-splitting order when multiple families are documented but not yet represented in registry/config/backend contracts.

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
- Operating distinction: acts as the control tower for milestones, RAID, steering summaries, slippage detection, and portfolio visibility rather than the deepest execution specialist

#### Project Management / Delivery Coordination Agent
- Purpose: keep day-to-day execution moving across tasks, checkpoints, and follow-ups
- Pod: `Delivery`
- Modes: `internal_operating`, `client_delivery`, `client_facing_service`
- Autonomy class: `supervised_executor`
- State ownership: execution-follow-up and checkpoint-readiness fields in `project_state`
- Replication rule: internal and client-delivery coordination instances are separate even when they share the same family
- Operating distinction: unlike PMO, this role is execution-oriented and turns plans, meeting notes, and milestone decisions into active tasks, reminders, and next checkpoints

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
- Operator visibility role: surface readable operating-model and execution-posture context for the agents shown in Mission Control
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
- read inbox, calendar, and task context within the same provider/account boundary when configured
- detect commitments, deadlines, and conflicts
- generate prioritized daily action list and candidate follow-up tasks
- turn approved recommendations into prioritized Microsoft To Do items when Microsoft 365 is the active provider stack
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
- analyze explicit client problem statements, client context, and engagement history before recommending services or architecture paths
- act like a consulting-company advisor embedded with the client for the duration of a mission
- identify adjacent consulting opportunities that could responsibly expand the account once the current mission is understood
- provide architecture and delivery counsel for proposals and execution
- continuously assess and improve internal platform architecture, reliability, and tooling
- identify technical debt, optimization opportunities, and modernization priorities
- internal-first contract; replicate later for Track 2 CIO/CTO service offers without sharing Track 1 state

### Chief AI / Digital Strategy Agent
- advise clients on AI, digitalization, AI engineering, and data engineering opportunities
- analyze explicit client problem statements, client context, process history, and delivery constraints before recommending AI services or strategy
- act like an AI consulting advisor embedded with the client around a concrete mission, use case, or problem statement
- identify adjacent AI, data, automation, or governance opportunities that can grow the account after the initial mission is framed
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
- transitional note: this legacy label maps most closely to `Project Management / Delivery Coordination Agent` and should be treated as that family during later registry/config alignment

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
- Project Management / Delivery Coordination Agent
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

For advisory families such as `CTO/CIO Agent` and `Chief AI / Digital Strategy Agent`, the client-scoped instance should ingest a bounded client brief that includes:
- problem statement
- client context and relevant history
- constraints, goals, and known delivery conditions

Those agents should analyze that brief before recommending services, roadmaps, or implementation paths.
They should also:
- frame the active consulting mission clearly
- recommend the best-fit initial service path
- surface bounded upsell or follow-on opportunities that could grow the account responsibly

## Approval Principle
No sensitive external action is sent automatically in MVP. CEO approval is required before execution for:
- money movement, invoicing release, and purchasing commitments
- contract/legal communications
- client-facing final deliverables
