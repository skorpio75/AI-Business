# Epics

## Status Legend
- `NOT_STARTED`
- `IN_PROGRESS`
- `DONE`

## Epic 1 - Project Foundation
- Status: `IN_PROGRESS`
### Outcome
A clean repo, documentation system, and project conventions.

### Main tech components
- Markdown
- Git
- Docker Compose

### Acceptance criteria
- starter docs exist
- repo structure is fixed
- naming conventions are documented
- two-track scope is documented

## Epic 2 - Core Platform Foundation
- Status: `DONE`
### Outcome
A runnable backend with config, persistence, and model access.

### Main tech components
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- LiteLLM
- Pydantic Settings

### Acceptance criteria
- API starts locally
- DB migrations work
- config loads from files and env
- model gateway can answer a test prompt

## Epic 3 - Workflow Engine
- Status: `DONE`
### Outcome
Reusable deterministic workflows with approval checkpoints.

### Main tech components
- LangGraph
- Pydantic

### Acceptance criteria
- workflow graph runs end to end
- approval checkpoint exists
- workflow state is persisted

## Epic 4 - Knowledge Layer
- Status: `DONE`
### Outcome
Documents can be ingested and used for grounded answers.

### Main tech components
- LlamaIndex
- Unstructured
- pgvector
- PostgreSQL

### Acceptance criteria
- documents ingest successfully
- embeddings are stored
- retrieval returns relevant chunks

## Epic 5 - Track A Internal Operations MVP
- Status: `DONE`
### Outcome
The internal business can run key workflows with one human approver.

### Main tech components
- React
- `shadcn/ui`
- Tailwind
- FastAPI
- LangGraph
- LiteLLM
- Langfuse

### Acceptance criteria
- inbox workflow works
- knowledge workflow works
- proposal workflow produces drafts
- approval UI is usable
- provider-backed inbox/calendar context is visible in Mission Control
- approved Outlook replies can execute through Microsoft Graph after approval

## Epic 6 - Track B Client Template MVP
- Status: `DONE`
### Outcome
A reproducible isolated client platform can be deployed quickly.

### Main tech components
- Docker Compose
- YAML
- FastAPI
- PostgreSQL

### Acceptance criteria
- client config pack exists
- client contract defines tenant, governance, deployment, storage, connectors, model routing, and default workflow/service packaging
- deployment can be cloned from the template env + compose overlay
- seed scripts prepare first instance
- runtime enforces tenant-scoped env, secret, storage, and prompt-root boundaries for Track B instances
- workflows run with client-specific context, with portability coverage proven for seeded `knowledge-qna` and `email-operations` instances while `document-intake` and `reporting` remain governed contract entries in the Track B workflow pack
- an operator runbook documents the real bootstrap sequence for seeded Track B instances, including tenant env activation, startup, connector bootstrap, verification, and cleanup
- client-facing advisory agents can analyze a client problem statement, context, and history before recommending services
- client-facing advisory agents can frame the active consulting mission and detect bounded upsell opportunities that help grow the account
- client-facing advisory agents use governed LLM reasoning for consulting analysis, with deterministic fallback reserved for resilience and guardrails

## Epic 7 - Observability
- Status: `IN_PROGRESS`
### Outcome
The platform provides traces and debugging visibility.

### Main tech components
- Langfuse

### Acceptance criteria
- workflow traces visible, starting with Langfuse spans for the current reusable workflow services
- prompt traces visible through nested `ModelGateway` generation observations
- model usage visible in both API responses and Langfuse trace metadata
- `AUDIT_MODEL.md` defines canonical audit objects and event families for agent execution, approvals, tools, routing, and outbound traceability

## Epic 8 - Testing Foundation
- Status: `IN_PROGRESS`
### Outcome
Reliable automated tests for core modules and workflows.

### Main tech components
- pytest
- httpx

### Acceptance criteria
- unit tests run locally
- a shared unit-test base structure exists for common settings, temp-dir, in-memory DB, and Track B seeded-client setup
- a shared sample-data layer exists for repeated request payloads, connector responses, and Track B runtime settings in tests
- `README.md` documents how to run the full suite plus the unit, integration, and workflow layers locally
- integration tests cover the current FastAPI endpoints with an in-process client plus dependency overrides for DB and external dependencies
- workflow tests cover the current approval and escalation branches for reusable workflow surfaces

## Epic 9 - Later Ops Automation
- Status: `NOT_STARTED`
### Outcome
Controlled delivery pipeline with agent support for repetitive engineering work.

### Main tech components
- Git
- GitHub Actions or GitLab CI
- Ruff
- mypy
- pre-commit

### Acceptance criteria
- CI runs on push
- lint and tests run automatically
- release checklist is documented
- ops automation backlog exists

## Epic 10 - Platform Operating Meta-Model
- Status: `IN_PROGRESS`
### Outcome
The repository has a formal operating model for pods, workflows, state, events, tools, approvals, and prompt composition boundaries.

### Main tech components
- Markdown
- Pydantic contracts
- YAML config

### Acceptance criteria
- meta-model docs exist
- platform objects are defined consistently
- family/mode/instance reuse model is documented
- prompt-layer target model is documented separately from the business agent catalog
- prompt-layer runtime contracts are defined without requiring broad prompt authoring
- prompt naming, storage, and loading conventions are defined with legacy-path compatibility
- roadmap and governance docs reference the same model

## Epic 11 - Pod Model and Agent Taxonomy
- Status: `IN_PROGRESS`
### Outcome
The platform distinguishes pod-native agents, specialist overlays, and reusable agent families across internal and client-delivery modes.

### Main tech components
- Markdown
- agent registry/config

### Acceptance criteria
- 4-pod model is documented
- first-class Growth, Delivery, Ops, and Executive agents are defined
- existing specialist roles are preserved and mapped
- Track A and Track B reuse rules are explicit

## Epic 12 - State, Event, Tool, and Autonomy Control Layer
- Status: `IN_PROGRESS`
### Outcome
Workflow and agent execution is described through normalized state, event, tool, autonomy, and prompt-composition contracts.

### Main tech components
- Markdown
- FastAPI contracts
- Pydantic
- LangGraph

### Acceptance criteria
- canonical state objects are documented
- event families and trigger patterns are defined
- normalized tool IDs and permission profiles are defined
- autonomy classes and approval implications are defined
- family-level base prompts and workflow-step prompts are planned as separate runtime concerns
- prompt composition and context-injection contracts are defined in backend/config
- prompt naming, storage, and loader fallback rules are defined
- audit object, event-family, and linkage rules are defined for later `agent_runs`, `audit_events`, and Mission Control trace surfaces
- hybrid retrieval source classes and provenance rules are defined so internal, client, and external evidence remain distinguishable
- bounded review/gate agent behavior is defined as a workflow checkpoint pattern rather than a free-form supervisor override
- specialist advisory contracts can carry client briefs, context signals, and service recommendations
- specialist advisory contracts can also carry consulting mission assessments and upsell opportunities
- agent-family LLM routing posture is documented so compact direct-Ollama, guarded local drafting, richer governed gateway reasoning, and deterministic hybrids are planned explicitly by family
- Mission Control can map governed routing posture into operator-facing agent operating-model labels without inventing a separate UI-only taxonomy
- personal assistant task-activation flows define same-tenant Microsoft Graph To Do promotion with approval and audit boundaries

## Epic 13 - Business Scaling Maturity Model
- Status: `NOT_STARTED`
### Outcome
The operating model supports growth from solo operator use to a boutique agent-augmented consulting firm.

### Main tech components
- Markdown
- policy model
- operating runbooks

### Acceptance criteria
- maturity stages are described
- delegation and scaling implications are documented
- pod model remains valid across stages
