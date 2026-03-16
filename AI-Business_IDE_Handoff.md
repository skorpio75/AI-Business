<!-- Copyright (c) Dario Pizzolante -->
# AI-Business IDE Handoff

## Purpose
This document is the authoritative handoff for continuing the integration of the newer **agent-run consulting firm blueprint** into the current `AI-Business` repository.

It is written for use by an IDE coding agent (Codex or equivalent) so it can continue implementation **without re-deriving the architecture**.

This handoff covers:
1. current repository baseline
2. what has already been verified
3. exact gaps between the current repo and the target blueprint
4. target operating model to integrate
5. concrete file changes to make
6. implementation sequence aligned with the current roadmap
7. rules and constraints that must not be broken

---

## 1. Repository currently in scope

Repository:
- `skorpio75/AI-Business`

Current repository concept:
- enterprise agent platform
- Track A = internal instance for the freelance / consulting company
- Track B = isolated client template / deployable instance
- workflow-first, AI inside selected workflow steps
- one high-risk human approval authority in MVP
- React mission control + FastAPI backend + LangGraph orchestration + PostgreSQL/pgvector memory stack

Core docs already present:
- `README.md`
- `ROADMAP.md`
- `EPICS.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `WORKFLOWS.md`
- `DECISIONS.md`
- `TODO.md`
- `MEMORY_MODEL.md`
- `INTEGRATIONS.md`

Important current reality:
- repository is already relatively mature on MVP implementation
- it is stronger on executive/business specialist roles than the newer blueprint
- it is weaker on formal operating meta-model, state/event definitions, autonomy tiers, and explicit pod structure

---

## 2. What was confirmed in the sanity check

The repository is **compatible** with the newer blueprint. There is no architectural contradiction.

### Current repository strengths
The repo already includes:
- Track A / Track B separation
- workflow-first philosophy
- approval-first for risky external actions
- specialist agents such as CFO, Accountant, CTO/CIO, Chief AI / Digital Strategy, Compliance, Procurement
- initial mission-control UI
- live connector work for inbox/calendar
- implemented internal MVP slices such as email operations, knowledge Q&A, proposal generation

### Main confirmed gaps still remaining
The repo still lacks or only implies the following:
1. explicit **4-pod operating model**
   - Growth
   - Delivery
   - Ops
   - Executive
2. explicit **agent handoff / interaction map**
   - who invokes whom
   - what event causes handoff
   - what state is passed
3. distinct first-class delivery agents for:
   - BA / Requirements
   - Architect
   - Build / Automation
   - Mission Control as an actual operating supervisor, not only UI concept
4. normalized **tool taxonomy / permission model**
5. formal **event and trigger model**
6. formal **state model**
   - opportunity_state
   - project_state
   - run_state
   - approval_state
7. explicit **autonomy classes**
   - assistant
   - supervised_executor
   - bounded_autonomous
   - approval_gated
8. business-scaling **maturity model**
   - solo operator
   - solo + subcontractors
   - micro-firm 2–4
   - boutique 5–7
   - 10-person agent-augmented firm

These are the concepts that now need to be integrated into the repo without breaking the current roadmap or implementation logic.

---

## 3. Target operating model to integrate

The target model is not “random autonomous agents.”

It is:
- workflow backbone first
- specialist agents second
- mission control visibility third
- approvals and policies for commitments
- reusable internal + client-isolated operating patterns
- progressive autonomy

### 3.1 Four-pod structure to add
The repo currently uses:
- corporate functions
- service delivery functions

Keep that, but formalize the sharper operating model below.

#### Pod A — Growth
Purpose:
- acquire and convert business

Agents:
- Lead Intake Agent
- Account Research Agent
- Qualification Agent
- Outreach Draft Agent
- Proposal / SOW Agent
- CRM Hygiene Agent

#### Pod B — Delivery
Purpose:
- execute consulting / IT / digital / AI client work

Agents:
- PMO / Project Control Agent
- BA / Requirements Agent
- Architect Agent
- Build / Automation Agent
- QA / Review Agent
- Documentation Agent

#### Pod C — Ops
Purpose:
- run the company

Agents:
- Finance Ops Agent
- Invoice / Receivables Agent
- Vendor / Procurement Agent
- Admin / HR Ops Agent
- Company Reporting Agent

#### Pod D — Executive
Purpose:
- provide leadership visibility, prioritization, escalation, risk control

Agents:
- CEO Briefing Agent
- Strategy / Opportunity Agent
- Risk / Watchdog Agent
- Mission Control Agent

### 3.2 Relationship to current repo roles
Do **not** remove the existing specialist roles such as:
- CFO Agent
- Accountant Agent
- CTO/CIO Agent
- Chief AI / Digital Strategy Agent
- Compliance/Contract Agent
- Procurement Agent

Instead:
- keep them
- map them into the pod model
- decide which are pod-native vs specialist overlays

Suggested mapping:

#### Growth pod overlays
- Chief AI / Digital Strategy Agent can assist on AI/digital opportunity shaping
- CTO/CIO Agent can assist pre-sales technical strategy

#### Delivery pod overlays
- CTO/CIO Agent remains strategic technical counsel
- Chief AI / Digital Strategy Agent remains specialist consulting support
- Compliance/Contract may be consulted for delivery constraints

#### Ops pod overlays
- CFO Agent
- Accountant Agent
- Procurement Agent
- Finance Agent
- Reporting Agent

#### Executive pod overlays
- CEO approval remains human
- Strategy / Opportunity Agent complements CFO and CTO/CIO outputs

---

## 4. Canonical concepts that must be added

The repo needs a more explicit platform meta-model.

### 4.1 Core platform objects
Introduce or document the following core objects:
- `Agent`
- `Tool`
- `Workflow`
- `Trigger`
- `Event`
- `Run`
- `Approval`
- `Task`
- `MemorySource`
- `Client`
- `Opportunity`
- `Project`
- `Policy`
- `Pod`

These can start as documentation and configuration contracts before they become full code objects.

### 4.2 Core design principle
Use this invariant:
- Agents think
- Tools act
- Workflows coordinate
- Policies constrain
- Mission Control observes
- Humans approve key commitments

This principle should be reflected in docs and later in code structure.

---

## 5. New docs / models to add

### 5.1 `PODS.md`
Purpose:
- define the 4-pod operating structure
- map current and target agents into pods
- show which pod owns what workflows
- show internal vs client-delivery vs later client-facing use

Minimum sections:
- purpose
- pod definitions
- pod-to-agent mapping
- pod boundaries
- internal vs Track B replication rules
- orchestrator strategy

### 5.2 `PLATFORM_MODEL.md`
Purpose:
- define the formal operating meta-model of the platform

Must include:
- platform objects
- how agents, workflows, tools, policies, triggers, and mission control relate
- principle that workflows govern execution
- difference between reasoning, execution, orchestration, and oversight

### 5.3 `STATE_MODEL.md`
Purpose:
- define canonical state objects

Must include at least:
- `opportunity_state`
- `project_state`
- `run_state`
- `approval_state`

Each state should define:
- required fields
- optional fields
- who owns updates
- which workflows consume it
- which agents write it

### 5.4 `TOOLS.md`
Purpose:
- define a normalized tool taxonomy and permissions model

Must include namespaces such as:

#### Communication
- `email.read`
- `email.draft`
- `email.send_internal`
- `email.send_external`
- `calendar.read`
- `calendar.write`
- `meetings.ingest_transcript`

#### Commercial
- `crm.read`
- `crm.write`
- `contacts.read`
- `proposals.read_template`
- `pricing.read_rules`
- `pricing.run_estimate`
- `research.web_search`

#### Delivery
- `pm.read`
- `pm.write`
- `tasks.read`
- `tasks.write`
- `docs.read`
- `docs.write`
- `repo.read`
- `repo.write`
- `code.run_sandbox`
- `workflow.deploy_nonprod`

#### Operations
- `finance.read`
- `finance.write_draft`
- `invoices.generate_draft`
- `payments.read`
- `vendors.read`
- `vendors.write`
- `hr.read`
- `hr.write_limited`

#### Core
- `memory.search`
- `memory.write`
- `state.read`
- `state.write`
- `approval.request`
- `reporting.generate`
- `audit.log`

Also define:
- allowed vs denied tools per agent type
- approval gating for powerful actions

### 5.5 `AUTONOMY_MODEL.md`
Purpose:
- define agent autonomy classes

Minimum classes:
- `assistant`
- `supervised_executor`
- `bounded_autonomous`
- `approval_gated`

Each class must define:
- what it may do
- what it may not do
- whether it may write state
- whether it may call action tools
- whether human approval is mandatory

### 5.6 `EVENT_MODEL.md` or `TRIGGERS.md`
Purpose:
- define platform-wide events

Must include event families such as:

#### Sales
- `lead.received`
- `lead.enriched`
- `lead.qualified`
- `meeting.discovery.completed`
- `proposal.requested`
- `proposal.submitted`
- `deal.won`
- `deal.lost`

#### Delivery
- `project.created`
- `workshop.completed`
- `requirements.updated`
- `design.requested`
- `design.completed`
- `build.requested`
- `build.completed`
- `qa.failed`
- `qa.passed`
- `milestone.completed`
- `project.risk.detected`

#### Operations
- `invoice.triggered`
- `invoice.sent`
- `invoice.overdue`
- `vendor.renewal_approaching`
- `month_end.started`
- `timesheet.missing`

#### Executive
- `risk.alert`
- `approval.pending`
- `run.failed`
- `schedule.daily_brief`
- `schedule.weekly_review`
- `schedule.monthly_strategy`

#### Knowledge
- `document.ingested`
- `meeting.summary.created`
- `project.closed`
- `lessons_learned.created`

---

## 6. Changes to existing docs

### 6.1 Update `AGENTS.md`
Do not replace the existing catalog. Extend it.

#### Add explicit new first-class agents
Add these as named canonical agents:

##### Growth pod
- Lead Intake Agent
- Account Research Agent
- Qualification Agent
- Outreach Draft Agent
- Proposal / SOW Agent
- CRM Hygiene Agent

##### Delivery pod
- PMO / Project Control Agent
- BA / Requirements Agent
- Architect Agent
- Build / Automation Agent
- QA / Review Agent
- Documentation Agent

##### Ops pod
- Finance Ops Agent
- Invoice / Receivables Agent
- Vendor / Procurement Agent
- Admin / HR Ops Agent
- Company Reporting Agent

##### Executive pod
- CEO Briefing Agent
- Strategy / Opportunity Agent
- Risk / Watchdog Agent
- Mission Control Agent

#### Keep existing specialist roles and reposition them
Do not remove:
- CFO
- Accountant
- Finance
- CTO/CIO
- Chief AI / Digital Strategy
- Compliance/Contract
- Procurement
- Document Agent
- Knowledge Agent
- Project Management Agent
- Delivery Agent
- Quality Management Agent
- Consulting Support Agent
- Testing/QA Agent
- Ops Agent

Instead:
- either map them to the new pod structure
- or label them as specialist overlays / transitional roles

#### Add structure per agent
Each agent entry should evolve toward a more formal contract:
- Purpose
- Pod
- Internal / Client Delivery / Client Facing flags
- Responsibilities
- Non-responsibilities
- Trigger patterns
- Inputs
- Outputs
- Tool permissions
- Approval conditions
- Autonomy class
- State ownership
- Replication rule for Track B

At minimum this formal contract should be introduced for the new first-class agents.

### 6.2 Update `WORKFLOWS.md`
Current workflows are useful, but still too step-list oriented.

Add:
- which agent owns each step
- which event starts the workflow
- what event each workflow emits
- what approval gate exists
- what state object is updated

#### Add cross-agent handoff logic
Example target choreography:

##### Opportunity to proposal
- Lead Intake Agent -> Account Research Agent -> Qualification Agent -> Outreach Draft Agent -> Proposal / SOW Agent -> Finance check -> CEO approval

##### Delivery flow
- PMO Agent -> BA Agent -> Architect Agent -> Build Agent -> QA Agent -> Documentation Agent -> PMO Agent -> Finance trigger

This handoff structure does not need to be fully coded yet, but it must be documented precisely.

### 6.3 Update `ARCHITECTURE.md`
Keep the existing architecture. Extend it.

Add a section for:
- pod-based operating model
- formal event/state layer
- tool permission layer
- autonomy and approval layer
- Mission Control as operating supervisor, not only UI surface

Clarify that the architecture stack now includes:
- interfaces
- workflows
- agents
- tools/actions
- policies/approvals
- state/event model
- memory
- infrastructure

### 6.4 Update `ROADMAP.md`
The roadmap currently tracks implementation phases well.

Do not discard that structure. Add a new **architecture integration stream**.

#### Add new tasks under current or next phases for blueprint integration

##### Phase 0 / documentation backlog
- add `PODS.md`
- add `PLATFORM_MODEL.md`
- add `STATE_MODEL.md`
- add `TOOLS.md`
- add `AUTONOMY_MODEL.md`
- add `EVENT_MODEL.md`

##### Phase 2 or 3 follow-up
- define first-class contracts for Lead Intake, PMO, BA, Architect, Build, Risk, Mission Control
- align agent registry/config with pod model
- define normalized event names for workflow triggers
- define state ownership and persistence model
- define tool permission matrix

##### Phase 5 / observability and control
- align audit model with state/event layer
- expose event/run traces in Mission Control
- track tool usage by normalized tool IDs
- capture autonomy class and approval class in run logs

##### Phase 6 / ops maturity
- introduce role-based policy model
- delegated authority beyond single CEO if required later
- prompt/model governance by workflow and agent class

### 6.5 Update `EPICS.md`
Add epics if missing for:
- platform operating meta-model
- state/event formalization
- pod model and agent taxonomy
- autonomy and policy control
- business scaling maturity model

### 6.6 Update `DECISIONS.md`
Add ADR-style entries for:
- adopting pod-based operating model
- keeping specialist executive agents while introducing pod-first structure
- event/state normalization
- tool permission taxonomy
- autonomy class framework
- explicit separation of strategic advisor agents vs operational execution agents

### 6.7 Update `TODO.md`
Ensure the short execution view includes the new documentation and architecture tasks derived from `ROADMAP.md`.

---

## 7. Concrete target agent definitions to integrate

These are the most important missing first-class agents. These definitions should be introduced in docs/config first.

### 7.1 Lead Intake Agent
Purpose:
- ingest inbound lead signals and create structured opportunity records

Responsibilities:
- read inbound message/form
- classify lead type
- extract contact, company, need, urgency, likely budget
- write structured opportunity entry
- emit `lead.enriched`

Tools:
- `email.read`
- `crm.write`
- `memory.write`

Autonomy:
- `supervised_executor`

State ownership:
- initial `opportunity_state`

### 7.2 Account Research Agent
Purpose:
- enrich opportunity with company and market context

Responsibilities:
- prepare account brief
- identify likely pain points
- support qualification and discovery

Tools:
- `research.web_search`
- `crm.read`
- `memory.write`

Autonomy:
- `assistant`

### 7.3 Qualification Agent
Purpose:
- decide fit and next commercial path

Responsibilities:
- score fit
- match services
- recommend reject / nurture / discovery / proposal

Tools:
- `crm.read`
- `pricing.read_rules`
- `memory.search`

Autonomy:
- `assistant` or `supervised_executor` depending on whether it updates CRM directly

### 7.4 Proposal / SOW Agent
Purpose:
- prepare commercial draft package

Responsibilities:
- generate scope and assumptions
- prepare proposal draft
- prepare SOW draft
- suggest effort envelope

Tools:
- `proposals.read_template`
- `pricing.run_estimate`
- `docs.write`
- `memory.search`

Autonomy:
- `supervised_executor`
- external send requires approval

### 7.5 PMO / Project Control Agent
Purpose:
- own project governance and operational control

Responsibilities:
- maintain status
- track milestones
- track RAID
- generate weekly reporting
- detect slippage

Tools:
- `pm.write`
- `tasks.read`
- `tasks.write`
- `docs.write`
- `calendar.read`

Autonomy:
- `supervised_executor`

State ownership:
- `project_state` governance fields

### 7.6 BA / Requirements Agent
Purpose:
- transform workshops and docs into structured requirements

Responsibilities:
- extract requirements
- define acceptance criteria
- identify gaps and assumptions
- emit `requirements.updated`

Tools:
- `docs.read`
- `docs.write`
- `memory.search`
- `meetings.ingest_transcript`

Autonomy:
- `assistant`

### 7.7 Architect Agent
Purpose:
- convert requirements into target solution structure

Responsibilities:
- define architecture option(s)
- describe integration and data flows
- identify technical risks
- emit `design.completed`

Tools:
- `docs.read`
- `docs.write`
- `memory.search`
- `repo.read`

Autonomy:
- `assistant`

### 7.8 Build / Automation Agent
Purpose:
- implement scripts, automations, low-code flows, configuration, scaffolds

Responsibilities:
- produce code/config/workflow artifacts
- work from approved requirements/design
- emit `build.completed`

Tools:
- `repo.write`
- `code.run_sandbox`
- `workflow.deploy_nonprod`

Autonomy:
- `supervised_executor`
- no production deployment without approval

### 7.9 QA / Review Agent
Purpose:
- validate quality and consistency before external release or milestone close

Responsibilities:
- compare deliverables with requirements/design
- run checklists
- summarize defects or missing items
- emit `qa.passed` or `qa.failed`

Tools:
- `docs.read`
- `repo.read`
- `state.read`
- `reporting.generate`

Autonomy:
- `assistant`

### 7.10 Mission Control Agent
Purpose:
- supervise runs, approvals, escalation queues, and operating visibility

Responsibilities:
- observe workflows and exceptions
- route failed runs
- show pending approvals
- maintain operational visibility
- emit `approval.pending`, `run.failed`, `risk.alert` where relevant

Tools:
- `state.read`
- `state.write`
- `approval.request`
- `audit.log`
- `reporting.generate`

Autonomy:
- `supervised_executor`

---

## 8. Canonical state objects to define

The platform is currently memory-aware but needs explicit operating state.

### 8.1 `opportunity_state`
Fields to include:
- `id`
- `client_id` or `prospect_id`
- `owner`
- `stage`
- `lead_score`
- `qualification_status`
- `estimated_value`
- `service_type`
- `next_action`
- `last_contact_at`
- `risks`
- `memory_refs`

Used by:
- Lead Intake
- Research
- Qualification
- Outreach
- Proposal

### 8.2 `project_state`
Fields to include:
- `id`
- `client_id`
- `status`
- `project_manager`
- `current_phase`
- `milestone_health`
- `budget_health`
- `risk_level`
- `overdue_actions_count`
- `next_steerco_date`
- `deliverables`
- `memory_refs`

Used by:
- PMO
- BA
- Architect
- Build
- QA
- Docs
- Finance

### 8.3 `run_state`
Fields to include:
- `run_id`
- `workflow_id`
- `agent_id`
- `status`
- `started_at`
- `confidence`
- `tool_calls`
- `output_ref`
- `blocking_reason`
- `audit_ref`

Used by:
- Mission Control
- audit layer
- approval layer
- observability

### 8.4 `approval_state`
Fields to include:
- `approval_id`
- `approval_class`
- `related_run_id`
- `related_entity_type`
- `related_entity_id`
- `requested_by_agent`
- `approver_role`
- `status`
- `requested_at`
- `decided_at`
- `decision`
- `notes`

Used by:
- approval queue
- mission control
- risky workflows

---

## 9. Canonical workflow upgrades to apply

### 9.1 Opportunity to proposal workflow
Document this explicitly.

#### Start event
- `lead.received`

#### Flow
1. Lead Intake Agent
2. Account Research Agent
3. Qualification Agent
4. Outreach Draft Agent or Discovery scheduling
5. Proposal / SOW Agent
6. Finance review if pricing implications
7. CEO approval
8. external send

#### State updates
- create and enrich `opportunity_state`
- create `approval_state` when needed
- update `run_state` per step

### 9.2 Delivery workflow
#### Start event
- `deal.won`

#### Flow
1. PMO Agent opens project structure
2. BA Agent extracts requirements
3. Architect Agent produces design
4. Build Agent implements
5. QA / Review Agent validates
6. Documentation Agent packages handover / working docs
7. PMO Agent updates delivery status
8. Finance trigger if milestone reached

#### State updates
- create `project_state`
- milestone and risk updates
- generate approval if release or sensitive outbound delivery requires review

### 9.3 Ops workflows
Billing and finance workflows should be updated to refer to:
- state ownership
- normalized tool IDs
- approval class
- event triggers

---

## 10. How to align this with the current roadmap

The goal is **not** to derail the current implementation roadmap.

The goal is to add a formal architectural layer that future implementation can rely on.

### 10.1 Immediate roadmap additions
Add these documentation tasks first.

#### Documentation / architecture integration stream
- create `PODS.md`
- create `PLATFORM_MODEL.md`
- create `STATE_MODEL.md`
- create `TOOLS.md`
- create `AUTONOMY_MODEL.md`
- create `EVENT_MODEL.md`

These are low-risk, high-value, and unblock later implementation quality.

### 10.2 Agent taxonomy alignment tasks
Then add:
- formalize first-class contracts for Lead Intake, PMO, BA, Architect, Build, Mission Control, Risk
- map existing specialist agents to the pod structure
- decide which current agents become aliases, transitional labels, or overlays

### 10.3 Workflow and state alignment tasks
Then add:
- define normalized workflow events
- define state ownership
- update workflow specs to show agent ownership and state writes
- update approval model to reference approval classes

### 10.4 Code alignment tasks after docs
Only after docs and contracts are aligned:
- update config registries
- update Pydantic models
- update API contracts if needed
- update mission control surfaces to use new normalized metadata
- capture tool IDs, autonomy classes, approval classes in run traces

---

## 11. Recommended implementation order for the IDE agent

Use this exact order unless strong code reality forces a small variation.

### Step 1 — Documentation meta-model
Create:
- `PODS.md`
- `PLATFORM_MODEL.md`
- `STATE_MODEL.md`
- `TOOLS.md`
- `AUTONOMY_MODEL.md`
- `EVENT_MODEL.md`

### Step 2 — Update canonical docs
Update:
- `AGENTS.md`
- `WORKFLOWS.md`
- `ARCHITECTURE.md`
- `ROADMAP.md`
- `EPICS.md`
- `DECISIONS.md`
- `TODO.md`

### Step 3 — Registry/config alignment
Review and update:
- agent registry config
- workflow registry config
- any base YAML files for agents/workflows
- ensure new first-class agents exist at config level even if code implementation is partial

### Step 4 — Contract/model alignment
Review backend contracts and add normalized definitions for:
- event names
- state models
- approval classes
- autonomy classes
- tool IDs or tool categories

### Step 5 — Mission Control metadata alignment
Ensure UI/backend can later surface:
- workflow ID
- agent ID
- event source
- approval class
- autonomy class
- routing path
- fallback mode
- normalized tool usage

### Step 6 — Future implementation phases
After the architecture layer is integrated, continue with current roadmap phases without breaking momentum.

---

## 12. Constraints and non-goals

### 12.1 Do not break current MVP direction
Do not remove or rework existing implemented flows just to fit the new taxonomy.

The integration must be additive and clarifying.

### 12.2 Do not remove existing specialist roles
Existing roles are valuable and already reflect the repo’s business ambition.

The new pod structure is a higher-level operating model, not a replacement for specialist business agents.

### 12.3 Do not over-engineer code before documentation is aligned
The repo is at a stage where architectural clarification will prevent future drift.

Documentation and contracts come first.

### 12.4 Preserve Track A / Track B isolation principle
Any new state, pod, tool, or workflow definition must preserve:
- isolated deployments
- no shared client operational state
- replicated agent patterns, not shared cross-client runtime state

### 12.5 Preserve approval-first model for sensitive actions
Do not accidentally introduce autonomous external commitments.

---

## 13. What “done” looks like for this integration phase

This integration phase is complete when:
1. the repo includes the missing meta-model docs
2. the docs clearly describe the 4-pod operating model
3. the agent taxonomy includes first-class Growth / Delivery / Ops / Executive agents
4. workflows explicitly show agent ownership, triggers, outputs, and approvals
5. state, event, autonomy, and tool models are documented
6. roadmap and TODO include the architecture-alignment tasks
7. existing specialist roles remain mapped and preserved
8. the resulting repository gives a coding agent enough context to continue implementation without ambiguity

---

## 14. Suggested immediate execution prompt for IDE Codex

Use the following operating brief inside the IDE if needed:

> You are continuing work on the `AI-Business` repository.
> Your task is to integrate the agent-run consulting firm blueprint into the current repository without breaking the existing roadmap or MVP.
> Work additively.
> First create the missing meta-model documentation files: `PODS.md`, `PLATFORM_MODEL.md`, `STATE_MODEL.md`, `TOOLS.md`, `AUTONOMY_MODEL.md`, and `EVENT_MODEL.md`.
> Then update `AGENTS.md`, `WORKFLOWS.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `EPICS.md`, `DECISIONS.md`, and `TODO.md` so they reflect:
> - the 4-pod model
> - explicit first-class agents for Growth / Delivery / Ops / Executive
> - event/trigger definitions
> - state ownership
> - autonomy classes
> - normalized tool taxonomy
> - mission control as an operating supervisor
> Preserve Track A / Track B isolation, the single-approver MVP model, and the current implementation progress.
> Do not delete existing specialist agents such as CFO, Accountant, CTO/CIO, Chief AI / Digital Strategy, Compliance, Procurement, or Document Agent.
> Map them into the new model.
> Prefer precise, internally consistent markdown and configuration-aligned terminology.
> Update all affected governance files in the same work session to avoid drift.

---

## 15. Final strategic note

The key architectural move is:

**evolve the repository from a strong set of agents and workflows into a formal operating system model for an agent-run consulting firm.**

The missing layer is not more AI.
It is:
- structure
- ownership
- state
- events
- permissions
- autonomy boundaries
- scaling model

That is what this integration must deliver.
