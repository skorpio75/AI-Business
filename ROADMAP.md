# ROADMAP

## Purpose
Track implementation progress, phase status, and actionable tasks for the enterprise agent platform MVP.

## Status Legend
- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `DONE`

## Current Snapshot
- Updated: 2026-03-09
- Overall Status: `IN_PROGRESS`
- Active Phase: `Phase 2 - Workflow + Knowledge Foundation`

## Phase Tracker

| Phase | Objective | Status | Owner | Target | Progress |
|---|---|---|---|---|---|
| Phase 0 | Documentation and repo skeleton | IN_PROGRESS | dpizz | TBD | 9/12 tasks done |
| Phase 1 | Platform core (FastAPI, config, DB, LiteLLM) | DONE | dpizz | TBD | 8/8 tasks done |
| Phase 2 | Workflow + knowledge foundation | IN_PROGRESS | dpizz | TBD | 8/14 tasks done |
| Phase 3 | Track A internal MVP workflows (React UI) | NOT_STARTED | dpizz | TBD | 0/14 tasks done |
| Phase 4 | Track B client template MVP | NOT_STARTED | dpizz | TBD | 0/6 tasks done |
| Phase 5 | Observability + testing | NOT_STARTED | dpizz | TBD | 0/10 tasks done |
| Phase 6 | Later ops layer (CI/CD, LLMOps/MLOps) | NOT_STARTED | dpizz | TBD | 0/7 tasks done |

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
- [ ] P2-T09: Define workflow templates for billing, finance, PO, PM, quality/testing, documentation handover
- [ ] P2-T10: Add inbox connector interface for personal assistant workflow
- [ ] P2-T11: Add calendar connector interface for personal assistant workflow
- [ ] P2-T12: Define CTO/CIO counsel contract (strategy options, architecture advice, internal improvement backlog)
- [ ] P2-T13: Define Accountant/CFO contracts (reconciliation rules, close process, scenario planning outputs)
- [ ] P2-T14: Define Chief AI/Digital Strategy contract (AI opportunity map, AI/data delivery blueprint, maturity model)

### Phase 3 - Track A Internal MVP Workflows (React UI)
- [ ] P3-T01: Scaffold React mission-control app (`app/ui` or `frontend`)
- [ ] P3-T02: Build workflow monitor page
- [ ] P3-T03: Build approval queue page
- [ ] P3-T04: Build agent activity page
- [ ] P3-T05: Implement email operations workflow end-to-end
- [ ] P3-T06: Implement knowledge Q&A workflow end-to-end
- [ ] P3-T07: Implement proposal generation workflow baseline
- [ ] P3-T08: Connect approval actions from UI to API
- [ ] P3-T09: Add Agents org view with avatars/status for corporate + delivery agents
- [ ] P3-T10: Add KPI widgets (billing, cashflow, delivery health, quality gate status)
- [ ] P3-T11: Add personal assistant panel (today priorities, schedule conflicts, quick actions)
- [ ] P3-T12: Add CTO/CIO panel (customer scope insights, strategy options, internal tech improvement queue)
- [ ] P3-T13: Add finance cockpit panels (accounting exceptions, close status, CFO scenario cards)
- [ ] P3-T14: Add Chief AI/Digital Strategy panel (opportunity portfolio, AI/data roadmap, delivery guidance cards)

### Phase 4 - Track B Client Template MVP
- [ ] P4-T01: Create client deployment template pack
- [ ] P4-T02: Finalize `config/client-template/client.yaml`
- [ ] P4-T03: Build seed script for client initialization
- [ ] P4-T04: Isolate storage/credentials per client instance
- [ ] P4-T05: Validate workflow portability across instances
- [ ] P4-T06: Document client bootstrap runbook

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

### Phase 6 - Later Ops Layer (CI/CD, LLMOps/MLOps)
- [ ] P6-T01: Define git branching and release workflow
- [ ] P6-T02: Add CI pipeline (lint + tests)
- [ ] P6-T03: Add Ruff + mypy + pre-commit config
- [ ] P6-T04: Define model/prompt versioning process
- [ ] P6-T05: Define evaluation dataset strategy
- [ ] P6-T06: Define rollback and incident process
- [ ] P6-T07: Define agent-assisted release checklist

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

## Next Action
Start `P2-T09`: define workflow templates for billing, finance, PO, PM, quality/testing, documentation handover.
