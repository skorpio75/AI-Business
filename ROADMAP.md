# ROADMAP

## Purpose
Track implementation progress, phase status, and actionable tasks for the enterprise agent platform MVP.

## Status Legend
- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `DONE`

## Current Snapshot
- Updated: 2026-03-16
- Overall Status: `IN_PROGRESS`
- Active Phase: `Phase 5 - Observability + Testing`
- Active Cross-Cutting Stream: `AI-Business IDE handoff integration`

## Phase Tracker

| Phase | Objective | Status | Owner | Target | Progress |
|---|---|---|---|---|---|
| Phase 0 | Documentation and repo skeleton | IN_PROGRESS | dpizz | TBD | 17/22 tasks done |
| Phase 1 | Platform core (FastAPI, config, DB, LiteLLM) | DONE | dpizz | TBD | 8/8 tasks done |
| Phase 2 | Workflow + knowledge foundation | DONE | dpizz | TBD | 20/20 tasks done |
| Phase 3 | Track A internal MVP workflows (React UI) | DONE | dpizz | TBD | 20/20 tasks done |
| Phase 4 | Track B client template MVP | DONE | dpizz | TBD | 10/10 tasks done |
| Phase 5 | Observability + testing | IN_PROGRESS | dpizz | TBD | 0/12 tasks done |
| Phase 6 | Later ops layer (CI/CD, LLMOps/MLOps) | NOT_STARTED | dpizz | TBD | 0/10 tasks done |

## Completed Baseline Items
- [x] Create repository folder skeleton
- [x] Create base markdown docs (`README.md`, `EPICS.md`, `ARCHITECTURE.md`, `AGENTS.md`, `WORKFLOWS.md`, `DECISIONS.md`, `TODO.md`)
- [x] Add `.env.example`, `docker-compose.yml`, `Makefile`
- [x] Add initial agent spec: `agents/email-agent.md`
- [x] Add initial workflow spec: `workflows/email-operations.md`

## Task Register By Phase

### Phase 0 - Documentation and Repo Skeleton
- [x] P0-T01: Create directory structure from blueprint
- [x] P0-T02: Create top-level markdown docs
- [x] P0-T03: Create `docs/` markdown files
- [x] P0-T04: Create config YAML baseline files
- [x] P0-T05: Create `.env.example`
- [x] P0-T06: Create `docker-compose.yml`
- [x] P0-T07: Create `Makefile`
- [ ] P0-T08: Add remaining agent specs (`knowledge`, `document`, `reporting`, `ops`)
- [ ] P0-T09: Add remaining workflow specs (`knowledge-qna`, `document-intake`, `reporting`)
- [ ] P0-T10: Clean blueprint encoding artifacts and typos
- [x] P0-T11: Define explicit memory/shared-brain model in `MEMORY_MODEL.md`
- [x] P0-T12: Define external integration boundaries in `INTEGRATIONS.md`
- [x] P0-T13: Add `PODS.md` for the 4-pod operating structure and family/mode/instance reuse model
- [x] P0-T14: Add `PLATFORM_MODEL.md` for the formal operating meta-model
- [x] P0-T15: Add `STATE_MODEL.md` for canonical operating state contracts
- [x] P0-T16: Add `TOOLS.md` for normalized tool taxonomy and permissions
- [x] P0-T17: Add `AUTONOMY_MODEL.md` for agent autonomy classes
- [x] P0-T18: Add `EVENT_MODEL.md` for normalized event families and trigger patterns
- [x] P0-T19: Update agent and workflow markdown specs to consistently reference pod, event, state, autonomy, and tool models
- [x] P0-T19A: Clarify the distinction between `PMO / Project Control Agent` and `Project Management / Delivery Coordination Agent`
- [ ] P0-T20: Define business-scaling maturity guidance across solo, micro-firm, and boutique operating stages
- [ ] P0-T21: Clean `AI-Business_IDE_Handoff.md` encoding artifacts and align it with canonical terminology

### Phase 1 - Platform Core
- [x] P1-T01: Scaffold FastAPI app entrypoint (`app/api`)
- [x] P1-T02: Add health endpoint (`GET /healthz`)
- [x] P1-T03: Implement settings loader with Pydantic Settings
- [x] P1-T04: Add SQLAlchemy base/session wiring
- [x] P1-T05: Add Alembic configuration
- [x] P1-T06: Initialize PostgreSQL + pgvector schema setup
- [x] P1-T07: Add LiteLLM gateway service wrapper
- [x] P1-T08: Document local startup steps in `README.md`

### Phase 2 - Workflow + Knowledge Foundation
- [x] P2-T01: Define workflow state contracts (Pydantic)
- [x] P2-T02: Build LangGraph runner base
- [x] P2-T03: Add document ingestion pipeline placeholder
- [x] P2-T04: Add retrieval service interface
- [x] P2-T05: Add prompt/template loading utility
- [x] P2-T06: Wire pgvector retrieval baseline
- [x] P2-T07: Add workflow run persistence model
- [x] P2-T08: Define shared agent contract for corporate and delivery functions (capabilities, KPIs, approval class)
- [x] P2-T09: Define workflow templates for billing, finance, PO, PM, quality/testing, documentation handover
- [x] P2-T10: Add inbox connector interface for personal assistant workflow
- [x] P2-T11: Add calendar connector interface for personal assistant workflow
- [x] P2-T12: Define CTO/CIO counsel contract (strategy options, architecture advice, internal improvement backlog)
- [x] P2-T13: Define Accountant/CFO contracts (reconciliation rules, close process, scenario planning outputs)
- [x] P2-T14: Define Chief AI/Digital Strategy contract (AI opportunity map, AI/data delivery blueprint, maturity model)
- [x] P2-T15: Align agent registry and base contracts with pod model, family/mode/instance identity, and specialist overlay mapping
- [x] P2-T16: Define normalized event names, approval classes, and autonomy classes in backend contracts/config
- [x] P2-T17: Define state ownership and persistence mapping for `opportunity_state`, `project_state`, `run_state`, and `approval_state`
- [x] P2-T18: Define normalized tool permission profiles by agent family and operating mode
- [x] P2-T19: Define the runtime prompt-layer model: family base prompts, workflow-step prompts, and context-injection rules
- [x] P2-T20: Define prompt asset naming, storage, and loading conventions without requiring full prompt authoring for every documented agent

### Phase 3 - Track A Internal MVP Workflows (React UI)
- [x] P3-T01: Scaffold React mission-control app (`app/ui` or `frontend`)
- [x] P3-T02: Build workflow monitor page
- [x] P3-T03: Build approval queue page
- [x] P3-T04: Build agent activity page
- [x] P3-T05: Implement email operations workflow end-to-end
- [x] P3-T06: Implement knowledge Q&A workflow end-to-end
- [x] P3-T07: Implement proposal generation workflow baseline
- [x] P3-T08: Connect approval actions from UI to API
- [x] P3-T09: Add Agents org view with avatars/status for corporate + delivery agents
- [x] P3-T10: Add KPI widgets (billing, cashflow, delivery health, quality gate status)
- [x] P3-T11: Add personal assistant panel (today priorities, schedule conflicts, quick actions)
- [x] P3-T12: Add CTO/CIO panel (customer scope insights, strategy options, internal tech improvement queue)
- [x] P3-T13: Add finance cockpit panels (accounting exceptions, close status, CFO scenario cards)
- [x] P3-T14: Add Chief AI/Digital Strategy panel (opportunity portfolio, AI/data roadmap, delivery guidance cards)
- [x] P3-T15: Replace null-only inbox/calendar placeholders with provider-backed fetch connectors (Gmail, Google Calendar, Microsoft Graph)
- [x] P3-T16: Add OAuth/bootstrap flow and secret management for external inbox/calendar providers
- [x] P3-T17: Add connector diagnostics and live inbox/calendar detail views in mission control
- [x] P3-T18: Launch email workflows from live inbox messages with source metadata attached
- [x] P3-T19: Send approved Outlook replies end-to-end through Microsoft Graph `Mail.Send`
- [x] P3-T20: Add explicit UI routing indicators for local model, cloud route, fallback-rule execution, and local LLM invocation status

### Phase 4 - Track B Client Template MVP
- [x] P4-T01: Create client deployment template pack
- [x] P4-T01A: Add typed specialist client-context analysis endpoints so client-facing advisory agents can assess a problem statement, context/history, and recommend relevant services
- [x] P4-T01B: Extend client-facing advisory agents with consulting-style mission framing and upsell opportunity detection so they can help grow client accounts
- [x] P4-T01C: Route specialist advisory analysis through the governed prompt/model layer so consulting agents use LLM reasoning with deterministic fallback guardrails
- [x] P4-T01D: Route internal CTO/CIO and Chief AI specialist panels through the governed prompt/model layer and surface routing metadata in Mission Control
- [x] P4-T02: Finalize `config/client-template/client.yaml`
- [x] P4-T03: Build seed script for client initialization
- [x] P4-T04: Isolate storage/credentials per client instance
- [x] P4-T05: Validate workflow portability across instances
- [x] P4-T06: Document client bootstrap runbook

### Phase 5 - Observability + Testing
- [ ] P5-T01: Add Langfuse trace integration
- [ ] P5-T02: Add unit test base structure
- [ ] P5-T03: Add API integration tests
- [ ] P5-T04: Add workflow branch tests (approval/escalation)
- [ ] P5-T05: Add test fixtures and sample data
- [ ] P5-T06: Add test execution instructions in `README.md`
- [ ] P5-T07: Define `AUDIT_MODEL.md` for agent execution, approvals, and decision traceability
- [ ] P5-T08: Add `agent_runs` persistence for per-agent execution history
- [ ] P5-T09: Add `audit_events` persistence for step-level actions, tool usage, and approval events
- [ ] P5-T10: Expose audit/trace endpoints for workflow, agent, and approval inspection
- [ ] P5-T11: Align audit/trace model with normalized events, tool IDs, autonomy classes, and approval classes
- [ ] P5-T12: Expose event/run traces in Mission Control with source event, routing path, and escalation visibility

### Phase 6 - Later Ops Layer (CI/CD, LLMOps/MLOps)
- [ ] P6-T01: Define git branching and release workflow
- [ ] P6-T02: Add CI pipeline (lint + tests)
- [ ] P6-T03: Add Ruff + mypy + pre-commit config
- [ ] P6-T04: Define model/prompt versioning process
- [ ] P6-T05: Define evaluation dataset strategy
- [ ] P6-T06: Define rollback and incident process
- [ ] P6-T07: Define agent-assisted release checklist
- [ ] P6-T08: Introduce role-based policy model and delegated authority beyond the MVP single-approver model
- [ ] P6-T09: Define workflow- and agent-class-specific model/prompt governance controls
- [ ] P6-T10: Add managed prompt versioning, evaluation, and rollback process for family and workflow-step prompts

### Cross-Cutting Stream - AI-Business IDE Handoff Integration
- [x] H-T01: Create the missing meta-model docs from `AI-Business_IDE_Handoff.md`
- [x] H-T02: Update governance docs to adopt the 4-pod model, reusable family/mode/instance agent model, and normalized event/state/tool/autonomy language
- [x] H-T03: Align markdown agent/workflow specs more fully with the new contracts and cross-agent handoff choreography
- [ ] H-T04: Reflect normalized metadata in registry/config and later runtime/UI surfaces without disrupting current MVP delivery work

### Backlog - Multi-Agent Runtime Evolution
- [ ] M-T01: Keep multi-agent runtime evolution workflow-first; do not introduce autonomous peer-agent orchestration as the MVP control model
- [ ] M-T02: Add per-step `agent_id` assignment and persistence for workflow execution steps
- [ ] M-T03: Add step-level agent execution logs, shared state read/write metadata, and standardized handoff payloads
- [ ] M-T04: Define explicit approval policy metadata per workflow step
- [ ] M-T05: Promote `Email Agent`, `Knowledge Agent`, and `Mission Control Agent` to bounded runtime agents inside workflow execution without changing approval-first controls
- [ ] M-T06: Build Growth as the first true multi-agent pod over `opportunity_state`, with bounded routing between intake, research, qualification, outreach, and proposal paths
- [ ] M-T07: Let `Mission Control Agent` supervise the first Growth pod runtime before adding a dedicated pod supervisor
- [ ] M-T08: Build Delivery as the flagship multi-agent runtime, with PMO governance, delivery coordination, BA, architect, build, QA, and documentation handoffs
- [ ] M-T09: Add executive and finance synthesis agents only after Growth and Delivery produce sufficiently rich operational signals
- [ ] M-T10: Replicate advisory and delivery-support runtime agents into Track B only after the Track A runtime model, approval policy, and state isolation are stable
- [ ] M-T11: Maintain a multi-agent suitability matrix and use it to prioritize runtime splitting order rather than promoting all documented agents equally
- [ ] M-T12: Treat the current high-suitability set as the primary candidate pool for Growth, Delivery, Executive synthesis, and advisory runtime promotion when foundational controls are ready

### Backlog - Model Routing
- [ ] B-T01: Define multi-provider routing rules for cloud model usage via LiteLLM (task type, risk, cost, latency, fallback order, local-only policy)
- [x] B-T01-INV: Create the initial broader direct-Ollama local-first candidate inventory by agent family and capture it in `AGENT_LLM_ROUTING_MATRIX.md`
- [ ] B-T01A: Apply the compact direct-Ollama local-first pattern to `KnowledgeQnAService`, using short grounded answer prompts and preserving citation-bound output
- [ ] B-T01B: Apply the compact direct-Ollama local-first pattern to `ProposalWorkflowService`, likely by splitting long proposal drafting into smaller draft sections before assembly
- [ ] B-T01C: Evaluate `EmailWorkflowService` for compact direct-Ollama local-first routing, with explicit guardrails for tone, approval safety, and outbound draft quality
- [ ] B-T01D: Evaluate client-facing CTO/CIO and Chief AI analysis endpoints for section-assembled direct-Ollama local-first execution without losing richer consulting reasoning quality
- [ ] B-T01E: Decide whether the finance/CFO panel should remain deterministic-only or gain an LLM-backed advisory mode before any direct-Ollama migration work is queued there
- [ ] B-T01F: Extend the candidate pool to Executive and Ops synthesis families where outputs are internal-facing and bounded, especially `CEO Briefing Agent`, `Strategy / Opportunity Agent`, `Risk / Watchdog Agent`, `Company Reporting Agent`, `Finance Agent`, `Accountant Agent`, and `CFO Agent`
- [ ] B-T01G: Extend the candidate pool to Delivery and client-delivery authoring families where work products are structured and can be section-assembled, especially `PMO / Project Control Agent`, `Project Management / Delivery Coordination Agent`, `BA / Requirements Agent`, `Architect Agent`, `Documentation Agent`, `QA / Review Agent`, `Testing/QA Agent`, `Delivery Agent`, and `Consulting Support Agent`
- [ ] B-T01H: Extend the candidate pool to Growth and commercial drafting families where outputs are bounded but externally consequential, especially `Lead Intake Agent`, `Account Research Agent`, `Qualification Agent`, `Outreach Draft Agent`, `Proposal / SOW Agent`, `Billing Agent`, `Procurement Agent`, and `Compliance / Contract Agent`
- [ ] B-T01I: Track `Document Agent`, `Knowledge Agent`, and later `Reporting Agent` client-facing-service variants as separate direct-Ollama candidates because Track A and Track B instances must not share runtime assumptions
- [ ] B-T01J: Define rollout waves for the direct-Ollama pattern: Wave 1 bounded internal/grounded outputs; Wave 2 internal synthesis panels; Wave 3 delivery-authoring families; Wave 4 externally consequential or richer client-facing consulting surfaces

### Backlog - Connector Diagnostics
- [ ] B-T02: Add connector diagnostics endpoint/view for current token load state, provider selection, inbox health, and calendar health

### Backlog - Authorization and Approval Policy
- [ ] B-T03: Define generalized role-based access control model for operators, approvers, and tenant-level roles
- [ ] B-T04: Add multi-approver and delegated-approval model for workflow execution and outbound actions
- [ ] B-T05: Define approval classes by workflow risk level
- [ ] B-T06: Add workflow-specific approval policy enforcement model
- [ ] B-T07: Prevent sensitive action execution outside explicit approval policy

### Backlog - Observability and Failure Diagnosis
- [ ] B-T08: Implement structured application logging across API, workflow, approval, and connector boundaries
- [ ] B-T09: Add per-workflow execution metrics, including success, escalation, failure, and retry counts
- [ ] B-T10: Add connector health metrics and explicit status persistence
- [ ] B-T11: Add model latency, error, route, and fallback metrics
- [ ] B-T12: Add alerting thresholds for send failures, approval failures, connector failures, and retrieval failures

### Backlog - Model Governance
- [ ] B-T13: Define approved model catalog by environment and workflow type
- [ ] B-T14: Formalize prompt versioning and routing policy versioning
- [ ] B-T15: Persist model/provider/routing/fallback decisions for workflow runs
- [ ] B-T16: Create small evaluation datasets per workflow
- [ ] B-T17: Define rollback rules for prompt/model regressions

### Backlog - Input / Output Safety Controls
- [ ] B-T18: Add prompt-injection defensive patterns for retrieval and external-content workflows
- [ ] B-T19: Add outbound content validation rules before external send
- [ ] B-T20: Add structured workflow-input validation for risky or externally sourced inputs
- [ ] B-T21: Add attachment and document validation rules in ingestion and email-derived workflows
- [ ] B-T22: Add grounded-output checks and explicit risky-output review gates

### Backlog - Frontend Operational Maturity
- [ ] B-T23: Improve loading, empty, degraded, and error states across Mission Control pages
- [ ] B-T24: Add approval history view with execution trail context
- [ ] B-T25: Add workflow search and filtering capabilities
- [ ] B-T26: Surface connector state and failure reasons clearly in UI
- [ ] B-T27: Extend UI routing indicators for local model, cloud route, and fallback execution paths

### Backlog - Data Lifecycle Management
- [ ] B-T28: Define retention periods by data class
- [ ] B-T29: Add archive and deletion procedures for workflow, document, and communication records
- [ ] B-T30: Define backup frequency and restore validation process
- [ ] B-T31: Document residency and storage-boundary assumptions

### Backlog - CI/CD and Reliability Hardening
- [ ] B-T32: Add schema migration validation in CI
- [ ] B-T33: Add send/reply safety tests for approval-gated communication workflows
- [ ] B-T34: Add incident and rollback playbooks
- [ ] B-T35: Define release tagging/version process

### Backlog - Multi-Tenant Hardening
- [ ] B-T36: Add tenant bootstrap automation
- [ ] B-T37: Enforce tenant-specific secret, storage, and runtime-config separation
- [ ] B-T38: Add backup and restore procedures per tenant instance
- [ ] B-T39: Add tenant-specific observability and operational controls


## Status Log

### 2026-03-09
- Created repository folder structure from blueprint.
- Created baseline markdown docs and config scaffolding.
- Added roadmap tracker with phase-by-phase tasks.
- Implemented MVP backend slice for `email-operations` with local-first model routing and cloud fallback.
- Added FastAPI endpoints for workflow run, run history, pending approvals, and approval decisions.
- Switched workflow persistence to SQLAlchemy-backed storage and added DB init script.
- Added Alembic migration system with initial schema revision and migration-based DB init.
- Added pgvector extension migration and switched Postgres defaults to port 5433 to avoid local DB conflicts.
- Completed Postgres validation end-to-end (`healthz`, run workflow, list pending approvals, approval decision) on port 5433.
- Expanded docs to define full IT freelancer operating model: corporate agents + service delivery agents.

### 2026-03-15
- Completed `P4-T01` by creating the first Track B client deployment template pack under `config/client-template/`, including a pack README, a client-scoped environment template, a compose overlay, and a storage/secret path map that can be cloned for isolated client instances.
- Completed `P4-T02` by expanding `config/client-template/client.yaml` into a fuller Track B client contract covering tenant identity, governance, deployment, storage, connectors, model routing posture, and default workflow/service packaging for later seed automation.
- Completed `P4-T03` by replacing the `scripts/seed_config.py` placeholder with a real client initialization seed flow that generates tenant-specific client contracts and runtime env files under `config/clients/` and creates the tenant storage, prompt, and secret directory roots.
- Completed `P4-T04` by enforcing tenant-scoped runtime storage and credential boundaries: Track B settings now require a client-scoped runtime env file, storage and prompt roots are validated against the tenant path, provider token persistence follows the active client env file, and startup creates tenant-scoped runtime directories.
- Completed `P4-T01D` by routing the internal CTO/CIO and Chief AI specialist panels through the shared prompt/model layer and surfacing provider/model routing metadata in Mission Control.
- Completed `P4-T01C` by routing CTO/CIO and Chief AI specialist analysis through the shared prompt/model layer so consulting reasoning can use LLM capacity while retaining deterministic fallback, output schemas, and approval/governance guardrails.
- Completed `P4-T01B` by extending CTO/CIO and Chief AI advisory analysis with consulting-style mission framing and upsell opportunity outputs so client-facing agents can solve a mission and discover adjacent growth paths for the account.
- Completed `P4-T01A` by adding typed CTO/CIO and Chief AI advisory-analysis contracts and API endpoints that assess client problem statements, context/history, and recommend relevant services.
- Added prompt-layer target architecture guidance: prompts are planned as a dedicated runtime layer with family-level base prompts plus workflow-step prompts rather than being embedded directly into the business agent catalog.
- Completed `P2-T15` by aligning the runtime agent registry with the pod model, family/mode identity, and specialist-overlay mapping, and mirrored the same metadata into `config/base/agents.yaml`.
- Completed `H-T03` / `P0-T19` for the current markdown spec set by aligning existing agent and workflow specs with pod ownership, operating modes, state objects, emitted events, approval gates, and cross-agent handoff roles.
- Completed `P2-T16` by adding a shared backend control-plane contract for normalized events, approval classes, and autonomy classes, and by enriching workflow config with trigger, emitted-event, approval, and autonomy metadata.
- Completed `P3-T16` by adding shared provider bootstrap and secret-management plumbing for Google and Microsoft connectors, including refresh-token lifecycle support, bootstrap-status diagnostics, and Google local-loopback OAuth onboarding.
- Completed `P2-T17` by adding typed backend ownership and persistence contracts for `opportunity_state`, `project_state`, `run_state`, and `approval_state`, and mirrored the same mapping into `config/base/state_registry.yaml`.
- Completed `P2-T18` by adding normalized tool-permission profile contracts and config bindings by agent family and operating mode, and surfaced tool-profile metadata in the agent activity UI.
- Completed `P2-T19` by adding typed prompt-layer contracts and config bindings for family-base assets, workflow-step assets, and runtime context injection, and wired the implemented email, knowledge, and proposal prompt flows through the composable prompt loader.
- Completed `P2-T20` by formalizing canonical prompt asset naming, storage, and loader resolution conventions, including explicit legacy-path compatibility so current prompt files remain valid during migration.
- Completed `P3-T12` by adding a typed CTO/CIO specialist advisory endpoint and mission-control panel for customer scope insight, architecture guidance, strategy options, and internal improvement priorities.
- Completed `P3-T13` by adding a typed finance cockpit endpoint and mission-control panel for accounting exceptions, close-readiness review, and CFO scenario cards.
- Completed `P3-T14` by adding a typed Chief AI / Digital Strategy endpoint and mission-control panel for AI opportunity portfolio, delivery blueprinting, and maturity guidance.
- Added Personal Assistant scope (inbox + calendar triage + prioritized daily list) to agent/workflow model.
- Added CTO/CIO agent scope for customer technology counsel and internal continuous platform improvement.
- Added Accountant and CFO scopes for operational accounting and strategic finance decision support.
- Added Chief AI / Digital Strategy scope for AI engineering, digitalization, and data engineering consulting/delivery.
- Added explicit shared-brain and memory-layer model in `MEMORY_MODEL.md`.
- Added integration boundary model in `INTEGRATIONS.md`, including OpenClaw positioning as edge runtime/channel layer.
- Added reusable workflow-state contracts and refactored `email-operations` to use them internally.
- Added LangGraph runner base and migrated `email-operations` to execute through the shared orchestration layer.
- Added executable document ingestion baseline for local markdown/text knowledge files.
- Added retrieval service contract and baseline keyword retrieval implementation over ingested documents.
- Added file-based prompt/template loader and moved `email-operations` prompt text into `prompts/email/`.
- Added pgvector-backed knowledge document storage and similarity retrieval baseline in PostgreSQL.
- Added persisted workflow state snapshots in PostgreSQL for LangGraph-backed workflow runs.
- Added shared agent contract models and registry service for reusable corporate, delivery, and platform agents.
- Added roadmap coverage for governance and auditability: audit model, agent execution history, audit events, and trace endpoints.

### 2026-03-11
- Added workflow template specs for billing operations, finance review, procurement PO, project management control, quality/testing gate, and documentation handover.
- Registered the new workflow templates in `config/base/workflows.yaml`.
- Added normalized inbox and calendar connector interfaces plus null connectors for personal assistant workflow integration.
- Added a personal assistant context assembly service to combine inbox and calendar inputs into one typed snapshot.
- Added a Vite/React `frontend/` scaffold for mission control.
- Built the initial workflow monitor page against `GET /workflows/runs`.
- Built the initial approval queue page against `GET /approvals/pending`, keeping decision mutations deferred to `P3-T08`.
- Added explicit typed specialist contracts for CTO/CIO, Accountant, CFO, and Chief AI / Digital Strategy outputs.
- Added internal-first agent specs for those roles, including replication-only notes for later Track 2 reuse of CTO/CIO and Chief AI / Digital Strategy patterns.
- Expanded the agent registry and base agent config to include the new specialist contracts.
- Added `GET /agents` for agent activity visibility in the UI.
- Added knowledge Q&A and proposal generation backend services plus their API endpoints.
- Added agent activity, email operations, knowledge Q&A, and proposal generation pages to the React mission-control UI.
- Wired approval actions from the approval queue page to the backend decision API.
- Expanded the agent registry to reflect a fuller corporate and delivery roster for mission-control views.
- Added a dedicated Agents org view with grouped avatar/status cards.
- Added dashboard KPI widgets for billing, cashflow, delivery health, and quality gate status.
- Added a personal assistant summary panel fed by a new dashboard summary endpoint.
- Replaced null-only personal assistant connector wiring with configurable Gmail, Google Calendar, and Microsoft Graph fetch connectors.
- Added environment-driven connector selection, account/calendar IDs, and token-based configuration placeholders in `.env.example`.
- Hardened personal assistant context assembly to use inbox lookback windows and degrade gracefully when connector fetches fail.
- Added unit coverage for connector selection, normalization helpers, and assistant context error handling.
- Added a dedicated mission-control inbox/calendar view backed by live personal-assistant context reads, including connector health, recent messages, and agenda items.
- Extended email workflow persistence to carry source message metadata, approval/send status, and sent timestamps.
- Wired Outlook approval completion to `Mail.Send` via Microsoft Graph reply calls so approved inbox-derived drafts can send end-to-end.
- Added a schema migration for email source/send tracking and applied it locally.

### 2026-03-14
- Integrated the AI-Business IDE handoff into the roadmap as an explicit cross-cutting architecture stream.
- Added the missing meta-model docs: `PODS.md`, `PLATFORM_MODEL.md`, `STATE_MODEL.md`, `TOOLS.md`, `AUTONOMY_MODEL.md`, and `EVENT_MODEL.md`.
- Formalized the reusable agent `family -> mode -> instance` model so the same agent family can exist in internal-operating and client-delivery forms without shared runtime state.
- Extended governance docs to reflect the 4-pod operating model, normalized event/state/tool/autonomy language, and Mission Control as an operating supervisor.
- Clarified that `PMO / Project Control Agent` is the governance/control-tower role, while `Project Management / Delivery Coordination Agent` is the day-to-day execution coordination role.
- Carried the PMO split into runtime-facing layers by adding distinct agent contracts, config entries, and frontend metadata fields for pod, family, and operating modes.

### 2026-03-15
- Evaluated a phased multi-agent runtime proposal against the current workflow-first architecture and accepted it as a bounded roadmap direction rather than an immediate architecture rewrite.
- Added a dedicated multi-agent runtime evolution backlog with explicit guardrails: workflow-first control, per-step agent identity, handoff payloads, step-level logs, and approval-policy metadata before richer pod-level runtime behavior.
- Confirmed Growth is the best first true multi-agent pod and Delivery remains the flagship multi-agent runtime after the foundational execution-contract and observability work is in place.
- Added a multi-agent suitability matrix to guide runtime-splitting priority, with a high-suitability set covering Growth specialists, Delivery specialists, Mission Control, Risk, executive synthesis, and selected finance/advisory families.
- Added a medium-suitability tier for families that are valuable in bounded collaboration, exception handling, or synthesis chains but may remain workflow-stage-oriented or rules-based longer.

### 2026-03-16
- Made the shared model timeout configurable through `MODEL_TIMEOUT_SECONDS` in runtime settings and `.env`.
- Refactored the internal CTO/CIO and Chief AI specialist panels to assemble their outputs from smaller section-level prompt/model calls rather than one oversized panel generation request.
- Simplified those internal panel prompts into compact line-oriented local calls and pinned them to the faster `qwen2.5:1.5b-instruct-q4_K_M` local model path so both panels now complete fully through Ollama in this environment.
- Preserved routing and fallback visibility for the section-assembled panels by aggregating per-section model diagnostics back into one Mission Control response.
- Reviewed the remaining LLM-backed services and queued the next direct-Ollama rollout candidates: Knowledge Q&A, proposal drafting, email drafting, and later the richer client-facing specialist analysis endpoints; finance/CFO remains a separate product-direction decision because it is still deterministic today.
- Expanded that rollout planning from a service-level shortlist into a broader agent-family candidate inventory aligned with `AGENTS.md`, including Delivery, Executive, Growth, Ops, and client-facing service families that may later adopt the same compact local-first Ollama pattern.
- Created `AGENT_LLM_ROUTING_MATRIX.md` as the family-level routing reference for compact direct-Ollama, guarded local drafting, richer governed gateway reasoning, and deterministic/tool-first hybrids, and synced the main governance docs to reference it.
- Validated Track B workflow portability across seeded client instances by activating tenant-scoped runtime env files, running the reusable `knowledge-qna` and `email-operations` services under seeded client settings, and checking that `document-intake` and `reporting` remain preserved in the seeded Track B workflow pack contract.
- Documented the Track B bootstrap operator flow in `docs/track-b-bootstrap-runbook.md`, including tenant seeding, `RUNTIME_ENV_FILE` activation, database and API startup, Google and Microsoft connector bootstrap, verification, and cleanup guidance.

## Next Action
Start `P5-T01` to add Langfuse trace integration now that Phase 4 Track B template work is complete.
